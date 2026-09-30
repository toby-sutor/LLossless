"""Split a source document into the segments a merge is accountable for.

This is the denominator. Its absence was measured once, and here is what it
cost: a merge that was a concatenation, that had dropped both titles and both
summary fields, scored 12/12 forward and 26/26 grounded, because the chain
`source -> decompose -> claims -> verify` only ever measured the verify half.
Nothing said what fraction of a source the claims covered, so the dropped
fields never entered a denominator and a check that examined nothing passed.

Segmentation is that missing fraction's bottom half, and it is mechanical: no
model, no randomness, same text in, same ids out. It is also shared. The merge
prompt renders these segments and these ids, and the coverage checker looks
for the same
ones, because two segmentations would mean the reconciler comparing two
different denominators — which is the original defect wearing a different hat.

## Segments partition; spans annotate

This splits a document into eight things: "title, headings, fenced
blocks, list items, sentences, links, code spans, numeric/version tokens". The
first five are ranges of the document that do not overlap; the last three sit
*inside* those ranges. Emitting all eight as segments would count a sentence
once and its link again, so the denominator would exceed the document, and the
prompt's rendering — one segment per line, id and pipe, "the prefix is not part
of the text" — has nowhere to put a segment nested in another.

So `Segment` is a partition and `Span` is an annotation on one. Coverage
counts segments; the verbatim integrity check reads spans and
consults nothing else. Both numbers are then about something, which is the
whole exercise.

## What is deliberately not recognised

*Indented code blocks.* Four-space indentation is CommonMark's other code
fence, and it is not honoured here. The one real input in hand that indents is
a JSON fragment whose three indented lines are three distinct fields — a
title, a summary, and a body — and folding them into one opaque block would
erase exactly the distinction this milestone exists to measure. Fenced blocks
are recognised because the invariant core names them; indentation is treated as leading
whitespace and stripped.

*Shell commands, configuration snippets and log output outside code.* The invariant core
calls all three invariant, and none is identifiable in running prose by any
rule that does not also catch ordinary sentences. Inside a fence or a code
span they are covered, and outside one they are not covered at all. Stated
rather than approximated: a check that silently covers three of eight verbatim
classes is the shape of the defect this module exists to prevent.

*The unit half of "numeric values with units".* A `numeric` span is the number
token and any suffix attached to it without a space — `8443`, `1.2`, `07:15`,
`30s`, `100%`. The following word is recorded as `unit` for the report and is
not part of what gets checked. Including it would demand "512 concurrent"
survive verbatim when only "512" is the value, and excluding the number's own
suffix would let "30 seconds" become "30s" unnoticed. The token is checked, the
unit is shown, and the report says which of the two it did.

*Setext headings underlined with dashes.* `=` underlines are recognised; `-`
underlines collide with horizontal rules and with YAML front matter, and
guessing between them is not deterministic enough to be worth a heading kind.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Segment kinds. A document is exactly the concatenation of its segments plus
# the notation between them, so this list is a partition and not a taxonomy.
TITLE = "title"
HEADING = "heading"
CODE_BLOCK = "code_block"
LIST_ITEM = "list_item"
TABLE_ROW = "table_row"
SENTENCE = "sentence"

KINDS = (TITLE, HEADING, CODE_BLOCK, LIST_ITEM, TABLE_ROW, SENTENCE)

# Span kinds: the inline members of the invariant core. `link` and `url`
# are the one pair allowed to nest: a link's display text may be reworded where
# the fidelity level permits, and its destination may never be, so the
# destination is checked whether or not the whole link survived intact.
CODE = "code"
LINK = "link"
URL = "url"
PATH = "path"
VERSION = "version"
NUMERIC = "numeric"

SPAN_KINDS = (CODE, LINK, URL, PATH, VERSION, NUMERIC)

# A first line this long is prose that happens to lack a full stop, not a
# title. Chosen well clear of both real inputs in hand (36 and 32 characters)
# and well under the shortest body line in either (120).
TITLE_MAX_CHARS = 120

# Words whose trailing period is not a sentence end. Deliberately short: an
# honorific is followed by a capitalised name, which is the one case the
# next-character rule cannot tell from a new sentence. "etc." and "e.g." are
# absent because they are covered by the single-letter rule or genuinely do end
# sentences, and because a wrong split costs one extra segment that is still
# found in the merge — visible, and cheap, unlike a wrong join.
#
# The German half is held to the same test: a word goes in only if it
# qualifies what *follows* it -- "bzw. X", "ca. 30", "vgl. Kapitel", "Nr. 5",
# "ggf. später" -- so a full stop after it is, in practice, never the end of a
# sentence. "usw." and "etc." close an enumeration and do end sentences, and
# "Jh." closes "19. Jh." the same way, so all three stay out: "... usw. Der
# nächste Satz" splits, and a wrong split is the cheap failure. The spaced
# two-letter forms, "z. B.", "d. h.", "u. a.", "z. T.", need no entry: each
# half is a single letter, and the single-letter rule in `_is_abbreviation`
# already holds them together.
ABBREVIATIONS = frozenset({
    "mr", "mrs", "ms", "dr", "prof", "st", "vs", "fig", "no",
    "bzw", "ca", "dt", "evtl", "ggf", "inkl", "nr", "vgl",
})

# What can open a parenthetical or a quotation in front of a word. Taken off
# the front of the word before a period only when nothing was taken off its
# back: "(z." is an abbreviation inside a bracket that is still open,
# while "(A)." is a closed parenthetical and the stop after it is a real end.
_OPENERS = "([\"'“„‚‘"

_FENCE = re.compile(r"^\s{0,3}(?P<marker>`{3,}|~{3,})")
# CommonMark 4.2: a closing sequence of hashes must be preceded by a space.
# Without that requirement `# C#` lost its trailing hash -- the non-greedy
# text group stopped at `C` and `#*` ate the rest -- so a heading naming a
# language came out as a different string than the document contained, and
# every downstream comparison was against text nobody wrote.
_ATX = re.compile(r"^\s{0,3}(?P<hashes>#{1,6})\s+(?P<text>.*?)(?:\s+#+)?\s*$")
_SETEXT = re.compile(r"^\s{0,3}=+\s*$")
_RULE = re.compile(r"^\s{0,3}([-*_])\s*(\1\s*){2,}$")
_BULLET = re.compile(r"^(?P<indent>\s*)(?P<marker>[-*+]|\d{1,9}[.)])\s+(?P<text>.*)$")
_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
_TABLE_DELIM = re.compile(r"^[\s|:-]*$")
_QUOTE = re.compile(r"^\s{0,3}>\s?")
_COMMENT = re.compile(r"^\s*<!--.*-->\s*$")

# The arrow put back in front of a quoted line. One space, whatever the source
# used: `Segment.notation` is a rendering, not a transcript, and `plain` takes
# any spacing back off again.
QUOTE_NOTATION = "> "

_CODE_SPAN = re.compile(r"`+[^`\n]+`+")
_MD_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*<?(?P<url>[^)\s>]+)>?(?:\s+\"[^\"\n]*\")?\s*\)")
_AUTOLINK = re.compile(r"<(?P<url>(?:https?|ftp|mailto):[^>\s]+)>")
_BARE_URL = re.compile(r"(?:https?|ftp)://[^\s<>()\[\]\"']+")
_PATHLIKE = re.compile(r"(?<![\w./~-])(?:\.{1,2}/|~/|/)?[\w.@+-]+(?:/[\w.@+-]+)+/?")
_VERSION = re.compile(r"(?<![\w.])(?:v\d+(?:\.\d+)*|\d+(?:\.\d+){2,})(?:[-+][\w.]+)?(?![\w])")
_NUMBER = re.compile(r"(?<![\w.])\d[\d,]*(?:[.:/-]\d+)*(?:%|°[CF]?|[A-Za-z]{1,4})?(?![\w])")
_UNIT_AFTER = re.compile(r"\s([A-Za-z][A-Za-z/]{0,14})")

# The terminator, any closing quotes or brackets, the gap, and a lookahead at
# something that can open a sentence. Anchored on what follows rather than on
# what precedes, because "port 8443. The" and "TLS 1.2. The" both end in a
# digit and only an abbreviation list could tell them from "1.2.3" — which the
# lookahead already excludes, since a digit-dot-digit has no space in it.
#
# The lookahead only finds a candidate; `_opens_sentence` decides. It used to
# be `[A-Z0-9]`, so a sentence opening on `Ä`, `Ö`, `Ü` or any other non-ASCII
# capital was joined to the one before it, and `re` has no class for "an
# uppercase letter in any script". `str.isupper` is that class.
#
# The closer class held only the straight and English-curly shapes (`"'’)]`)
# until this glyph directly glued onto the terminator, before the required
# gap, decided: a curly or guillemet character in that position is closing
# whatever quotation or parenthetical surrounded the sentence just ended,
# never opening one — an opener glued straight onto a full stop with no space
# before it does not occur. So the class also takes `“ ” ‘ » « › ‹`: German
# closes „ with “ and ‚ with ‘, French and Swiss close « with » and ‹ with ›,
# and German-style quoting closes » with « and › with ‹ — four conventions,
# eight glyphs, and every one of them is a closer at this position regardless
# of which role the same glyph plays as an opener elsewhere in the document
# (`_SENTENCE_OPENERS` decides that, separately, by what follows the gap).
# Before this, `„Nein.“ Dann` did not even match: the old class stopped at
# `“`, so `\s+` had to follow the bare terminator and found `“` instead — no
# candidate, and the two sentences stayed one segment with the second
# invisible inside the first, the dangerous direction.
_SENTENCE_END = re.compile(r"[.!?]+[\"'’”“‘»«›‹)\]]*\s+(?=\S)")

# What may stand in front of a sentence's first letter: brackets, and opening
# quotes in the English, German (`„`, `‚`, `»`), French and Swiss (`«`, `‹`)
# conventions. `»` and `›` open a German quotation and close a French one;
# either way nothing after the gap is closing the sentence before it.
_SENTENCE_OPENERS = "\"'“„«»‚‘‹›(["

# German writes an ordinal as a number and a full stop: "im 19. Jahrhundert",
# "am 3. Oktober". Followed by a capital that is exactly the shape of a
# sentence end, so the split is refused only for two closed lists. A
# month after a day number of 1 to 31 is a date. A noun from `_ORDINAL_NOUNS`
# after a number of up to three digits is an ordinal only when an article or
# an article-preposition contraction from `_ORDINAL_CONTEXT` comes before the
# number: "Siehe Seite 19. Kapitel 3 folgt" is two sentences, "im 19.
# Jahrhundert" is one. Everything outside the lists still splits: a wrong
# split is visible and cheap, a wrong join is not.
_GERMAN_MONTHS = frozenset({
    "januar", "jänner", "februar", "märz", "april", "mai", "juni", "juli",
    "august", "september", "oktober", "november", "dezember",
})
_ORDINAL_NOUNS = frozenset({
    "jahrhundert", "jahrhunderts", "jahrtausend", "jahrtausends", "jh",
    "jahr", "jahres", "jahrestag", "geburtstag", "tag", "tages", "woche",
    "monat", "monats", "quartal", "quartals", "mal", "platz", "rang", "runde",
    "spieltag", "stock", "stockwerk", "etage", "kapitel", "kapitels",
    "abschnitt", "abschnitts", "absatz", "band", "bandes", "auflage",
    "ausgabe", "klasse", "teil", "teils", "schritt", "stufe", "hand",
})
_ORDINAL_CONTEXT = frozenset({
    "der", "die", "das", "den", "dem", "des", "am", "im", "vom", "zum", "zur",
    "beim", "ins", "ans", "jeden", "jeder", "jede", "jedes",
})
# The number as a bare token at the end of the text before the stop, and the
# word before it if that word is all letters.
_ORDINAL_BEFORE = re.compile(
    r"(?:(?<=\s)|^)(?:(?P<context>[^\W\d_]+)\s+)?(?P<number>[1-9]\d{0,2})$")
_WORD_AFTER = re.compile(r"[^\W\d_]+")

_LAST_WORD = re.compile(r"(\S+)\s*$")


@dataclass(frozen=True)
class Span:
    """One occurrence of an invariant-core class inside a segment's text.

    `start` is an offset into `Segment.text`, not into the document: a span is
    only ever read together with the segment that carries it, and offsets into
    the original are one more thing to keep true across a join.
    """

    kind: str
    text: str
    start: int
    unit: str = ""

    @property
    def end(self) -> int:
        return self.start + len(self.text)


def flatten_with_breaks(
    text: str,
) -> tuple[str, tuple[int, ...], tuple[str, ...]]:
    """Collapse whitespace to single spaces, recording which spaces were newlines.

    The join at the heart of `emit` is what made a three-line signature block
    arrive as one segment whose text occurs nowhere in the source. The
    partition must not move -- segment counts are a registered denominator --
    so the break is recorded rather than made into a boundary, exactly as
    `notation` records a stripped bullet instead of dropping it.

    Each index in the returned tuple points at a space in the returned body
    that stood for a line break in the source. `rendered` puts them back.

    The third tuple is the **indentation that followed each break**, one entry
    per index, and it exists because a model cannot reproduce what it was
    never shown. Line breaks were recorded and restored from the start;
    the whitespace after them was not, so a merge of an indented document was
    handed every line flush left and wrote it back that way. Recorded here
    rather than kept in `text` for the same reason `breaks` is: `text` is what
    every comparison is made against and what the segment count is registered
    over, and neither may move.
    """
    out: list[str] = []
    breaks: list[int] = []
    indents: list[str] = []
    index, length = 0, len(text)
    while index < length and text[index].isspace():
        index += 1
    while index < length:
        if not text[index].isspace():
            out.append(text[index])
            index += 1
            continue
        stop, newline = index, False
        while stop < length and text[stop].isspace():
            newline = newline or text[stop] == "\n"
            stop += 1
        if stop < length:
            if newline:
                breaks.append(len(out))
                # What the next line was indented by: the whitespace after the
                # last newline in this run. A run holding two newlines is a
                # blank line, which the segmenter has already made a paragraph
                # boundary, so in practice there is one.
                run = text[index:stop]
                indents.append(run[run.rindex("\n") + 1:])
            out.append(" ")
        index = stop
    return "".join(out), tuple(breaks), tuple(indents)


@dataclass(frozen=True)
class Segment:
    """One unit of source content, with the id the merge model is told to use.

    `text` is what the merge is accountable for carrying: the content with its
    notation removed — no `#` markers, no list bullets, no blockquote arrows,
    no leading indent — because `README.md` is explicit that LLossless does
    not score notation. `code_block` is the exception and keeps every byte
    including its fences, since a fence is not notation around the content, it
    *is* the content's boundary and the invariant core makes the whole block invariant.

    `text` is the form the reconciler *matches* on, and no longer the form the
    merge model is *shown*. The rule that justified showing it was "a fact does
    not change when a bullet becomes a sentence", and a live merge of two real
    documents falsified it: shown a stripped list, the models tested fused
    adjacent items into one conjoined sentence, and the reverse pass then
    correctly reported the conjunction as invented, because it is. Two facts do
    change when two bullets become one sentence. So `notation` records what was
    stripped, `render_sources` puts it back for the model, and `plain` takes it
    off the merge again at comparison time.

    A segment never contains a newline except in a `code_block`. Wrapped lines
    are joined with a single space before sentences are split out, so that a
    merge which rewraps a paragraph still contains the segment; the comparison
    that finds it must normalise interior whitespace on both sides, exactly as
    `verify.locate` already does for evidence spans. Cited by name and not by
    line, since line citations are known to decay, and this
    module adds none.
    """

    id: str
    document: str
    ordinal: int
    kind: str
    text: str
    line: int
    # Which blank-line-separated block of the source this segment came out of.
    # 1-based and shared by every segment of one block, so equality between two
    # neighbours is "these shared a paragraph" and a change between them is a
    # paragraph boundary. Recorded here rather than recomputed from `line`
    # because the segmenter is the only thing that knows which blank lines it
    # consumed: a blank line inside a fence is content, not a boundary, and a
    # caller re-reading `Document.text` would have to re-derive the fence rule
    # to tell them apart. Required, with no default: a segment whose paragraph
    # is unknown would silently join whatever precedes it, which is the exact
    # loss this field exists to stop.
    paragraph: int
    level: int = 0
    # What was stripped from the front of the source line: `## `, `- `, `> `,
    # `> 1. `, or the indent that continues a list item. `render_sources` puts
    # it back so the model sees the document's shape; `plain` takes the same
    # notation off the merge so both sides of every comparison are `text`. Not
    # part of `text`, and so never part of a span or a token check. A
    # `code_block` carries none — its fences are inside `text` already.
    notation: str = ""
    # Where this segment's text had a line break in the source. Indices into
    # `text`, each naming a space that stood for a newline. Recorded rather
    # than made into a boundary: the partition is a registered denominator and
    # moving it would redefine a registered quantity. `rendered` puts
    # them back; nothing compares on them, since `text` is unchanged and stays
    # the form every match is made against.
    breaks: tuple[int, ...] = ()
    # The indentation each break was followed by, one entry per `breaks`
    # index. Empty for a document that indents nothing, which is every
    # prose fixture in this repository -- so this changes no rendering, no
    # cassette key and no comparison for any of them. `text` is untouched.
    indents: tuple[str, ...] = ()
    # The whitespace this segment's own first line began with. Shown by
    # `rendered`, absent from `text` for the reason `indents` is: `text` is
    # what every comparison searches for, and a leading space would make it
    # match nothing.
    indent: str = ""
    spans: tuple[Span, ...] = ()

    def spans_of(self, *kinds: str) -> tuple[Span, ...]:
        return tuple(span for span in self.spans if span.kind in kinds)


@dataclass(frozen=True)
class Document:
    """A source and its segmentation, in the order the segments appear."""

    id: str
    filename: str
    text: str
    segments: tuple[Segment, ...] = ()
    # Lines carrying no content, with the reason each was passed over. Recorded
    # rather than dropped: a denominator that quietly loses lines is the thing
    # this module exists to stop, even when the lines were only rules and
    # table separators.
    skipped: tuple[tuple[int, str], ...] = ()

    def by_id(self) -> dict[str, Segment]:
        return {segment.id: segment for segment in self.segments}


def document_id(index: int) -> str:
    """0 -> a, 25 -> z, 26 -> aa. Stable, and never runs out."""
    if index < 0:
        raise ValueError(f"document index must not be negative: {index}")
    letters = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(ord("a") + remainder) + letters
    return letters


# The filename a source takes once it is inside this tool, carrying the letter
# `document_id` just produced. Here rather than in `merge.py` so the name and
# the letter are one rule: `merge.source_names` writes these and
# `decompose.claim_id` reads them back, and a template in one module with a
# parser in another is two rules that agree until the day they do not.
SOURCE_TEMPLATE = "source_{letter}.md"
_SOURCE_NAME = re.compile(r"^source_([a-z]+)\.md$")

# And the name the merged document takes. It is not a source name and carries no
# document letter, which is what makes "every source" sayable as "everything but
# this" — the test three modules need once the source count stops being two.
MERGED_NAME = "merged.md"
assert not _SOURCE_NAME.match(MERGED_NAME)


def source_name(index: int) -> str:
    """The canonical filename for the source at this position. 0 -> source_a.md."""
    return SOURCE_TEMPLATE.format(letter=document_id(index))


def document_letter(filename: str) -> str:
    """The letter a canonical source name carries, or "" for any other name.

    Round-trips `source_name`, two-letter ids included, so `source_a.md` and
    `source_aa.md` stay distinct — which is why this is a match and not a first
    character. At twenty-seven documents a first character would give both `a`,
    and the claim ids built from it would collide inside one verify batch.
    """
    match = _SOURCE_NAME.match(filename)
    return match.group(1) if match else ""


def _mask(text: str, spans: list[Span]) -> str:
    """`text` with every found span blanked, so later patterns cannot see in.

    Same length throughout, so offsets stay valid. The replacement is `\\x00`
    rather than a letter or a space: no pattern here matches it, and a space
    would let a sentence split at a boundary that only exists because a URL
    was masked away.
    """
    if not spans:
        return text
    characters = list(text)
    for span in spans:
        for index in range(span.start, span.end):
            characters[index] = "\x00"
    return "".join(characters)


def _trim(token: str) -> str:
    """Drop the sentence punctuation a URL or path pattern swallowed.

    `/-/healthy.` at the end of a sentence is a path and a full stop, and both
    patterns here accept a dot inside a component because real paths and hosts
    contain them. Trimming is done on the match rather than in the pattern:
    the alternative is a lookahead that has to know it is not inside a version
    string, and this is one line.
    """
    return token.rstrip(".,;:!?")


def _unit_after(text: str, end: int) -> str:
    match = _UNIT_AFTER.match(text, end)
    return match.group(1) if match else ""


def find_spans(text: str) -> tuple[Span, ...]:
    """Every invariant-core occurrence in this text, ordered by position.

    Found most specific first and masked as they are found, so a number inside
    a URL is part of the URL and not a second finding. The single exception is
    a markdown link, which yields both itself and its destination — see the
    module note on nesting.
    """
    found: list[Span] = []
    working = text

    for match in _CODE_SPAN.finditer(working):
        found.append(Span(CODE, match.group(0), match.start()))
    working = _mask(working, found)

    for match in _MD_LINK.finditer(working):
        found.append(Span(LINK, match.group(0), match.start()))
        found.append(Span(URL, match.group("url"), match.start("url")))
    working = _mask(working, [span for span in found if span.kind == LINK])

    for pattern in (_AUTOLINK, _BARE_URL):
        for match in pattern.finditer(working):
            group = "url" if "url" in (pattern.groupindex or {}) else 0
            token = _trim(match.group(group))
            if token:
                found.append(Span(URL, token, match.start(group)))
        working = _mask(working, found)

    for match in _PATHLIKE.finditer(working):
        token = _trim(match.group(0))
        tail = token.rstrip("/").rsplit("/", 1)[-1]
        if token.startswith(("/", "./", "../", "~/")) or "." in tail:
            found.append(Span(PATH, token, match.start()))
    working = _mask(working, found)

    for match in _VERSION.finditer(working):
        found.append(Span(VERSION, match.group(0), match.start()))
    working = _mask(working, found)

    for match in _NUMBER.finditer(working):
        # Trailing sentence punctuation is not part of the number, and it is
        # `_trim`'s job here for the reason it is the URL pattern's: the token
        # is what has to survive into the merge, and a full stop or comma that
        # ended a sentence in the source is free to end a different one in the
        # merge. `AD 30-33,` is one token with an ASCII hyphen and two -- `30`
        # and `33,` -- with an en dash, which the range pattern does not know;
        # at `high` the model split the sentence, the comma became a stop, and
        # `33,` was reported as a numeral that did not survive.
        #
        # Trailing only. Interior separators are part of the value and must
        # not move: `2,000,000,000` keeps its commas and `30-33` its hyphen,
        # so a merge that wrote `2,000,000` is still a finding.
        token = _trim(match.group(0))
        if not token:
            continue
        found.append(
            Span(NUMERIC, token, match.start(), _unit_after(text, match.end()))
        )

    # Read back out of `text` rather than out of `working`. A span found in a
    # later pass is matched against a string with the earlier passes' spans
    # masked, so a link whose display text holds a code span comes back as
    # `[see \x00\x00\x00](/x)`. Masking keeps every offset valid, which is what
    # makes this a slice: same start, same length, original characters. Without
    # it the mask reached two places it must not — `token_present` searched the
    # merge for a needle containing NUL and never found it, so an intact link
    # was reported as a verbatim violation, and the finding printed the NULs.
    return tuple(
        Span(span.kind, text[span.start : span.end], span.start, span.unit)
        for span in sorted(found, key=lambda span: (span.start, -len(span.text)))
    )


def _is_abbreviation(word: str) -> bool:
    """Is this the word before a period that does not end a sentence?

    Three shapes, none of them a vocabulary list. A single letter is an initial
    (`J. Willis`). A short all-letter token with an interior dot is `e.g`,
    `i.e`, `a.m` — and the all-letter test is what keeps `TLS 1.2.` splitting,
    since `1.2` has an interior dot too. The rest is `ABBREVIATIONS`, which
    holds honorifics, for which the following capital is a name, and the
    German abbreviations that qualify what follows them.

    An opening bracket or quote in front of the word is not part of it.
    `(z. B. drei ...)` was read as the word `(z`, which is two characters and
    no initial, so the German "for example" ended a sentence at `(z.` and the
    merge was held to account for a fragment. The opener comes off only when
    nothing closed after the word: `(A).` is a whole parenthetical, and the
    full stop after it ends the sentence exactly as it did before.
    """
    trimmed = word.rstrip(".!?\"'’)]")
    if trimmed == word:
        trimmed = trimmed.lstrip(_OPENERS)
    bare = trimmed.lower()
    if not bare:
        return False
    if len(bare) == 1 and bare.isalpha():
        return True
    if "." in bare and len(bare) <= 4 and bare.replace(".", "").isalpha():
        return True
    return bare in ABBREVIATIONS


def _opens_sentence(masked: str, index: int) -> bool:
    """Can the text at `index` begin a sentence? Openers, then a capital in
    any script or an ASCII digit. A masked span (`\\x00`) is neither,
    as it was under the old `[A-Z0-9]` class."""
    while index < len(masked) and masked[index] in _SENTENCE_OPENERS:
        index += 1
    if index >= len(masked):
        return False
    first = masked[index]
    return first.isupper() or first in "0123456789"


def _is_ordinal(text: str, start: int, match: re.Match[str]) -> bool:
    """Is the stop at `match` a German ordinal's, not a sentence end?

    Read from the unmasked `text`, because `_mask` blanks every number. Only
    a bare `.` and a gap qualify: `19.)` or `19.“` closed something and ends
    the sentence. The rule and its limits are at `_GERMAN_MONTHS`.
    """
    if match.group().rstrip() != ".":
        return False
    before = _ORDINAL_BEFORE.search(text[start : match.start()])
    after = _WORD_AFTER.match(text, match.end())
    if not before or not after:
        return False
    number = int(before.group("number"))
    following = after.group().lower()
    if following in _GERMAN_MONTHS:
        return 1 <= number <= 31
    context = (before.group("context") or "").lower()
    return following in _ORDINAL_NOUNS and context in _ORDINAL_CONTEXT


def _sentences_with_offsets(text: str) -> list[tuple[int, str]]:
    """Sentences and where each one starts in `text`. See `split_sentences`."""
    masked = _mask(text, list(find_spans(text)))
    pieces: list[tuple[int, str]] = []
    start = 0
    for match in _SENTENCE_END.finditer(masked):
        if not _opens_sentence(masked, match.end()):
            continue
        word = _LAST_WORD.search(masked, start, match.start())
        if word and _is_abbreviation(word.group(1)):
            continue
        if _is_ordinal(text, start, match):
            continue
        piece = text[start : match.start() + 1]
        if piece.strip():
            pieces.append((start + len(piece) - len(piece.lstrip()), piece.strip()))
        start = match.end()
    tail = text[start:]
    if tail.strip():
        pieces.append((start + len(tail) - len(tail.lstrip()), tail.strip()))
    if pieces or not text.strip():
        return pieces
    return [(len(text) - len(text.lstrip()), text.strip())]


def split_sentences(text: str) -> list[str]:
    """One line of prose, split into sentences. Pure, and conservative.

    Splits only where a terminator is followed by whitespace and then something
    that can begin a sentence. Code spans and links are masked first, so a
    period inside `foo.bar` or inside a URL is not a boundary. Where the word
    before the terminator is a single letter or a known honorific the split is
    refused: initials and `e.g.` are followed by a capital and are otherwise
    indistinguishable from a new sentence.
    """
    return [piece for _, piece in _sentences_with_offsets(text)]


def _take_block(lines: list[str], index: int) -> tuple[list[tuple[int, str]], int]:
    """Gather one block of prose from `index`, with each line's 1-based number.

    Two rules decide where it ends, and the second is the interesting one.

    A block ends at anything that starts a different block — a blank line, a
    heading, a fence, a bullet, a table row. It *also* ends at a line whose
    last character is `.!?:;,`, because a line that closes on punctuation is a
    complete unit and the next line is not its continuation.

    Both rules apply to the first line as well as the rest, and that is the
    fix: they used to be skipped while the
    block was empty, so the one caller that starts mid-block — the bullet
    branch, gathering an item's continuation lines — swallowed whatever
    followed the item, including the next bullet. Two atomic facts written as
    two list items came back as one segment: one id, one line of the merge
    prompt, and a second fact in no denominator at all. It is in the corpus,
    not only in the field — `tests/fixtures/paraphrase/source_b.md` has a
    five-item list of defaults that segmented as three, two of them reading
    `Listen port: 8443 - Connect timeout: 30 seconds` and
    `Read timeout: 120 seconds - Maximum concurrent connections: 512`. A model
    shown that line writes the conjunction back out as one sentence, and the
    reverse pass calls it invented, which it is.

    That second rule exists for a shape that is not hard-wrapped prose at all:
    consecutive one-record-per-line text, such as the `"field": "value",` lines
    of a JSON fragment. Without it those lines join into one segment, and two
    fields that were separately droppable become one absence — which is exactly
    the distinction that used to go missing. The cost when
    it is wrong is one extra segment on a paragraph that wrapped after a comma,
    and an over-split segment is still found by a whitespace-normalised search
    of the merge, so it is visible rather than silent.
    """
    block: list[tuple[int, str]] = []
    while index < len(lines):
        stripped = lines[index].strip()
        if _is_block_start(lines[index]):
            break
        if index + 1 < len(lines) and _SETEXT.match(lines[index + 1]):
            break
        # The line with its indentation, not `stripped`. `emit` keeps
        # the leading whitespace and collapses only the interior, so the
        # indent survives as far as `flatten_with_breaks`, which records it
        # against the break it follows. Trailing whitespace goes here, since
        # nothing downstream can use it and it would reach the model as a
        # ragged right edge.
        block.append((index + 1, lines[index].rstrip()))
        index += 1
        if stripped and stripped[-1:] in ".!?:;,":
            break
    return block, index


def _is_block_start(line: str) -> bool:
    """Would this line begin a new block, rather than continue the last one?"""
    return bool(
        not line.strip()
        or _FENCE.match(line)
        or _ATX.match(line)
        or _RULE.match(line)
        or _BULLET.match(line)
        or _TABLE_ROW.match(line)
        or _COMMENT.match(line)
    )


def _table_cells(line: str) -> str:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return " | ".join(cell for cell in cells if cell)


class _Builder:
    """Accumulates segments for one document, assigning ids as it goes."""

    def __init__(self, letter: str) -> None:
        self.letter = letter
        self.segments: list[Segment] = []
        self.skipped: list[tuple[int, str]] = []
        # The block every segment emitted from now belongs to. Carried on the
        # builder rather than passed through `emit`, for the same reason
        # `ordinal` is: both are facts about the position in the document being
        # built, and a caller that had to supply one could supply a wrong one.
        self.paragraph = 1

    def end_paragraph(self) -> None:
        """A blank line was consumed: whatever comes next is a new block.

        Called for the blank line itself rather than for the next segment,
        because that is the byte that carries the meaning. Idempotence is not
        required and is not claimed: two blank lines in a row advance the
        counter twice, leaving a number no segment carries, and nothing reads
        the value except as "same as my neighbour, or not".
        """
        self.paragraph += 1

    def emit(
        self, kind: str, text: str, line: int, level: int = 0, notation: str = "",
        indent: str = "",
    ) -> None:
        if not text.strip():
            return
        if kind == CODE_BLOCK:
            body, breaks, indents = text, (), ()
        else:
            body, breaks, indents = flatten_with_breaks(text)
            # The segment's *own* opening indent. `flatten_with_breaks`
            # strips leading whitespace, which is right for `text` -- every
            # comparison is made against it and a segment that began with
            # spaces would match nothing. But a segment that opens a nested
            # line still has to be *shown* nested, or the model puts it back
            # flush left: the first live run after indents-after-breaks landed
            # restored five levels of nesting and left every `} else if` at
            # column 0, because those lines each begin a segment.
            indent = indent or text[:len(text) - len(text.lstrip())]
        ordinal = len(self.segments) + 1
        self.segments.append(
            Segment(
                id=f"{self.letter}{ordinal}",
                document=self.letter,
                ordinal=ordinal,
                kind=kind,
                text=body,
                line=line,
                paragraph=self.paragraph,
                level=level,
                notation="" if kind == CODE_BLOCK else notation,
                breaks=breaks,
                indents=indents,
                indent=indent,
                spans=find_spans(body),
            )
        )

    def emit_prose(
        self,
        block: list[tuple[int, str]],
        kind: str = SENTENCE,
        notation: str = "",
        continuation: str = "",
    ) -> None:
        """Emit one wrapped block of prose as sentences, each on its own line.

        `block` is the source lines with their 1-based numbers. They are joined
        with single spaces before splitting, so a sentence broken across a hard
        wrap comes back whole; the offsets of that join are kept so each
        sentence still reports the line it began on, which is the only thing a
        reader has to find it with.

        `notation` belongs to the first sentence only and `continuation` to the
        rest, because that is what the two mean in the source: one `- ` opens a
        list item and its later sentences are indented under it, while a `> `
        opens every line of the quote it is in. Giving each sentence the bullet
        would render one item as several, which is the invention this whole
        change exists to stop.
        """
        starts: list[tuple[int, int]] = []
        pieces: list[str] = []
        offset = 0
        for number, raw in block:
            # Leading whitespace kept, interior whitespace collapsed.
            # The indent is what tells a reader -- and a merge model -- how a
            # line sits under the one above it, and `flatten_with_breaks`
            # further down can only record what reaches it. Collapsing it here
            # is why an indented document arrived at the model flush left and
            # came back that way. Interior runs are still collapsed, because a
            # line wrapped at 80 columns must not carry its wrap.
            body = raw.strip()
            if not body:
                continue
            indent = raw[:len(raw) - len(raw.lstrip())]
            normalised = indent + " ".join(body.split())
            starts.append((offset, number))
            pieces.append(normalised)
            offset += len(normalised) + 1
        joined = "\n".join(pieces)
        for position, (start, sentence) in enumerate(
            _sentences_with_offsets(joined)
        ):
            line = next(
                (number for at, number in reversed(starts) if at <= start),
                block[0][0] if block else 0,
            )
            # The whitespace this sentence's own line began with. The
            # splitter hands back a sentence starting at its first non-space
            # character, so the indent has to be recovered here, from the
            # joined text between the preceding newline and `start`. Only
            # whitespace counts: a sentence beginning mid-line inherits the
            # indent of no line, and gets none.
            head = joined.rfind("\n", 0, start) + 1
            before = joined[head:start]
            self.emit(
                kind, sentence, line,
                notation=notation if position == 0 else continuation,
                indent=before if before.isspace() or not before else "",
            )

    def skip(self, line: int, reason: str) -> None:
        self.skipped.append((line, reason))


def segment_document(text: str, letter: str, filename: str = "") -> Document:
    """Split one document into segments. Pure: same text and letter, same ids.

    Ids are the document letter and a 1-based ordinal over every segment in
    reading order, `a1` through `a<n>`, with no gaps and no reuse. An id
    therefore moves if the document changes, which is correct — a disposition
    record naming `a4` is a claim about this text and no other.
    """
    builder = _Builder(letter)
    lines = text.splitlines()
    index = 0
    # Lines below this index had a `> ` taken off them and get it back at
    # render time. Held as an extent rather than a flag because the arrow is
    # stripped from the whole quote at once and the lines are then re-read one
    # at a time, several loop turns apart.
    quoted_until = 0

    while index < len(lines):
        raw = lines[index]
        number = index + 1
        stripped = raw.strip()
        quoted = QUOTE_NOTATION if index < quoted_until else ""

        if not stripped:
            # Not emitted and not skipped -- but no longer thrown away. The
            # blank line is the only thing in the source that says which
            # sentences shared a paragraph, and `render_sources` is graded on
            # showing the model the document's shape.
            builder.end_paragraph()
            index += 1
            continue

        fence = _FENCE.match(raw)
        if fence:
            marker = fence.group("marker")[0] * 3
            block = [raw]
            opened_at, closed = number, False
            index += 1
            while index < len(lines):
                block.append(lines[index])
                closes = lines[index].strip().startswith(marker)
                index += 1
                if closes:
                    closed = True
                    break
            if not closed:
                # Reported, never repaired. Everything after the opener is now
                # one code block, which is what the document literally says --
                # closing it at the next blank line would be the tool deciding
                # what the author meant, and the prose it swallowed would be
                # scored as code. Saying so leaves that decision with the
                # reader, who can see the line number.
                builder.skip(opened_at,
                             f"fence opened at line {opened_at} never closed; "
                             f"everything after it is one code block")
            # No notation: a fence is inside `text` already, and the invariant core makes
            # the block invariant byte for byte, arrows included or not at all.
            builder.emit(CODE_BLOCK, "\n".join(block), number)
            continue

        if _COMMENT.match(raw):
            builder.skip(number, "html comment")
            index += 1
            continue

        if _RULE.match(raw):
            builder.skip(number, "horizontal rule")
            index += 1
            continue

        atx = _ATX.match(raw)
        if atx:
            level = len(atx.group("hashes"))
            kind = TITLE if level == 1 and not builder.segments else HEADING
            builder.emit(
                kind, atx.group("text"), number, level,
                notation=f"{quoted}{'#' * level} ",
            )
            index += 1
            continue

        if _TABLE_ROW.match(raw):
            cells = _table_cells(raw)
            if not cells or _TABLE_DELIM.match(raw.strip().strip("|")):
                builder.skip(number, "table rule")
            else:
                builder.emit(TABLE_ROW, cells, number, notation=f"{quoted}| ")
            index += 1
            continue

        quote = _QUOTE.match(raw)
        if quote:
            # A blockquote arrow is notation around content that is otherwise
            # prose, so it is stripped and the remainder re-read as a line.
            #
            # The whole run of quoted lines is stripped in one go, not just
            # this one. A quote that wraps is gathered by `_take_block`, which
            # knows nothing about arrows and joined them into the middle of the
            # text: `conflict_surfaced`'s merge segmented as `**Unresolved:
            # default connect timeout.** > According to the Operator Guide...`,
            # so the reconciler was hunting a needle with notation in it.
            scan = index
            while scan < len(lines):
                arrow = _QUOTE.match(lines[scan])
                if not arrow:
                    break
                lines[scan] = lines[scan][arrow.end() :]
                scan += 1
            quoted_until = scan
            continue

        bullet = _BULLET.match(raw)
        if bullet:
            head = bullet.group("text").strip()
            marker = bullet.group("indent") + bullet.group("marker") + " "
            body = [(number, head)]
            index += 1
            if head[-1:] not in ".!?:;,":
                continuation, index = _take_block(lines, index)
                body.extend(continuation)
            builder.emit_prose(
                body, LIST_ITEM,
                notation=quoted + marker,
                continuation=quoted + " " * len(marker),
            )
            continue

        if index + 1 < len(lines) and _SETEXT.match(lines[index + 1]):
            kind = TITLE if not builder.segments else HEADING
            # Rendered back as `# `: a setext underline cannot be a prefix,
            # and what the model has to be shown is that the line is a heading.
            builder.emit(kind, stripped, number, 1, notation=f"{quoted}# ")
            index += 2
            continue

        paragraph, index = _take_block(lines, index)
        if not paragraph:
            # Unreachable: every block start is handled above, so the first
            # line of this call is never one. Here so that a future branch
            # cannot turn a returned empty block into a loop that never ends.
            index += 1
            continue
        joined = "\n".join(body for _, body in paragraph)
        if (
            not builder.segments
            and len(paragraph) == 1
            and len(joined) <= TITLE_MAX_CHARS
            and joined[-1:] not in ".!?,;:"
        ):
            # A short, unpunctuated first line standing alone is a title, and
            # says so without a `#`. Both real inputs in hand open this way;
            # neither is markdown. The alternative is that documents without
            # markup have no title segment at all, and a title that is not a
            # segment is a title nothing can report as dropped — which is one
            # of the two kinds of silent loss this tool exists to catch.
            builder.emit(TITLE, joined, number, notation=quoted)
        else:
            builder.emit_prose(paragraph, notation=quoted, continuation=quoted)

    return Document(
        id=letter,
        filename=filename,
        text=text,
        segments=tuple(builder.segments),
        skipped=tuple(builder.skipped),
    )


def segment_sources(documents: dict[str, str]) -> list[Document]:
    """Segment several sources at once, lettering them in the order given.

    The order is the caller's and is load-bearing: `a` and `b` are how the
    merge prompt names documents and how a disposition record points at one.
    `merge.check_sources` fixes it, by requiring the mapping's keys to be
    `source_name`'s output in `source_name`'s order — so the letters do not move
    between a recording and a replay of the same run, and a document's letter
    and its filename cannot disagree.
    """
    return [
        segment_document(text, document_id(index), filename)
        for index, (filename, text) in enumerate(documents.items())
    ]


def rendered(segment: Segment) -> str:
    """One segment as its source wrote it: `notation`, `text`, and nothing added.

    Not a general markdown writer. It restores what `segment_document` took
    off, which is why the table row is the one shape with a suffix: the cells
    were parsed out of `| a | b |` and joined with ` | `, so the two outer
    pipes are the only characters that cannot be carried in a prefix.
    """
    if segment.kind == CODE_BLOCK:
        return segment.text
    if segment.kind == TABLE_ROW:
        return f"{segment.notation}{segment.text} |"
    # The indent goes outside `notation`, which is where the source had it:
    # `  - item` is two spaces then a bullet, not a bullet then two spaces.
    return f"{segment.indent}{segment.notation}{with_breaks(segment)}"


def with_breaks(segment: Segment) -> str:
    """`text` with the source's own line breaks put back where they were.

    The inverse of the join `flatten_with_breaks` performs. Kept apart from
    `rendered` so that a caller wanting the text without notation -- the
    survival check is one -- does not have to strip a prefix back off.
    """
    if not segment.breaks:
        return segment.text
    out = list(segment.text)
    # Built back to front so an inserted indent does not move the indices of
    # the breaks still to be placed.
    for position, index in reversed(list(enumerate(segment.breaks))):
        if index < len(out) and out[index] == " ":
            indent = (segment.indents[position]
                      if position < len(segment.indents) else "")
            out[index] = "\n" + indent
    return "".join(out)


def plain(text: str) -> str:
    """`text` with line-leading notation removed. The merge side of a comparison.

    `Segment.text` is the stripped form and the merge is now shown the
    unstripped one, so the merge comes back carrying notation and every search
    for a segment, an invariant token, a title or a claim span would be looking
    for a needle the haystack no longer holds in that shape. This is the
    inverse of `rendered`, applied to a whole document at once: heading
    markers, bullets, arrows and the pipes around a table row come off, and
    nothing else is touched.

    Fenced blocks are copied out byte for byte. The invariant core makes a fence invariant,
    and a `#` comment or a `- item` inside a YAML block is content: stripping
    it would make the block's own verbatim check fail on the merge that kept it
    perfectly. That is the one place this function has to know about state, and
    it is the same fence rule `segment_document` uses.
    """
    out: list[str] = []
    marker = ""
    for raw in text.splitlines():
        if marker:
            out.append(raw)
            if raw.strip().startswith(marker):
                marker = ""
            continue
        fence = _FENCE.match(raw)
        if fence:
            marker = fence.group("marker")[0] * 3
            out.append(raw)
            continue
        line = raw
        while True:
            arrow = _QUOTE.match(line)
            if not arrow:
                break
            line = line[arrow.end() :]
        atx = _ATX.match(line)
        if atx:
            out.append(atx.group("text"))
            continue
        if _TABLE_ROW.match(line):
            out.append(_table_cells(line))
            continue
        bullet = _BULLET.match(line)
        if bullet:
            out.append(bullet.group("text"))
            continue
        out.append(line)
    return "\n".join(out)


def render_sources(documents: list[Document], base: str) -> str:
    """The sources as the merge prompt shows them: tagged, one segment per line,
    paragraphs kept apart by a blank line.

    The tag is what makes the injection guard sayable. `merge.md` tells the
    model that everything inside a <document> tag is data and that a sentence
    reading like an instruction is content to be merged like any other; that
    rule needs a boundary to point at, and this is it.

    The `<id>|` prefix is what makes a disposition record possible. A model that
    has to quote a sentence to refer to it can only ever be checked by finding
    that quote again; one that names `a4` can be checked by set membership,
    which is the difference between the reconciler needing an LLM and not.

    Rendered from `Segment.text` **with `Segment.notation` put back in front of
    it**, so the model sees a list as a list and a heading as a heading. It was
    the stripped form until it changed, on the argument that the model should be
    shown exactly the string the reconciler will look for; a live merge showed
    what that costs. Shown two list items as two bare lines, the models tested
    wrote one sentence carrying both, and the reverse pass reported the
    conjunction as invented — a correct finding about a document this function
    had made ambiguous.

    The reconciler still looks for `Segment.text`, and `plain` is the other
    half of this: it takes the same notation off the merge before any
    comparison, so both sides are the stripped form and the coverage checker is
    still measuring the merge rather than the segmenter. A `code_block` is
    rendered exactly as it was captured, fences and all, because the invariant core makes it
    invariant byte for byte; a table row gets its pipes back around the cells.

    A blank line separates one source paragraph from the next, inside the
    block. Until an earlier version there was none, anywhere, inside a `<document>`: the
    merge model was shown 23 sentences as 23 lines and had no way to know that
    seven of them shared a paragraph, so what it wrote back was a structure it
    invented rather than the document's. `decompose.number_lines` had treated a
    blank line as load-bearing since it was written, and `verify.reference_text`
    hands over the raw text untouched; the merge was the one pass blind to the
    structure it has to reproduce. Nothing here judges what the model does with
    it: added structure is counted and none of it graded, and `high`
    is licensed to restructure freely (`prompts/fidelity/high.merge.md`). This
    shows the shape; it does not require it.

    `base` is a filename, not an index: it arrives from a command line and is
    checked against the documents rather than trusted, because a base that
    matched nothing would silently render every document as non-base and no
    later check looks for the absence.
    """
    filenames = [document.filename for document in documents]
    if base not in filenames:
        raise ValueError(
            f"base document {base!r} is not one of the sources: {', '.join(filenames)}"
        )

    blocks = []
    for document in documents:
        attributes = f'id="{document.id}" filename="{document.filename}"'
        if document.filename == base:
            attributes += ' base="true"'
        lines = [f"<document {attributes}>"]
        previous = 0
        for segment in document.segments:
            # The source's own paragraph boundary, put back. Blank between two
            # blocks, nothing between two segments of one block, exactly as the
            # source wrote it. Before the id line rather than after, so a
            # document opening on a blank line still has no blank of its own.
            if previous and segment.paragraph != previous:
                lines.append("")
            previous = segment.paragraph
            shown = rendered(segment)
            if "\n" not in shown:
                lines.append(f"{segment.id}| {shown}")
                continue
            # A segment whose source spanned several lines is shown spanning
            # several lines, under a blank id. Without this the model is handed
            # a string that occurs nowhere in its input and is then graded on
            # reproducing the input exactly.
            head, *rest = shown.split("\n")
            lines.append(f"{segment.id}| {head}")
            lines += [f"{' ' * len(segment.id)}| {part}" for part in rest]
        lines.append("</document>")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)
