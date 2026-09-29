"""Which way a document writes its decimals, and the numerals that break it.

`internal/docs/number-convention.md` is the account of why this exists; this
note is what the code does. The `voyager` pair carries four planted errors that
change nothing but a separator -- "4.5" written "4,5", "17,560" written
"17.560" -- and across the stored runs the models fixed each in one or two of
eighteen. A model reads "4,5" as the same quantity in European notation, so to
it nothing changed. To a reader the same characters can differ by a factor of
1,000: "17.560" is seventeen point five six in English and seventeen thousand
five hundred and sixty in German.

**No model is asked anything here, and no number is ever rewritten.** Every
figure is a regular expression, a count and a `Decimal`. The check reports; the
merge model and the user decide.

## The rule

1. **A numeral that can only be read one way votes.** A single separator
   followed by one, two, or four or more digits is a decimal mark ("4,5",
   "3.14", "3,1415"), as is one after a lone `0` or after four or more digits,
   where no thousands group can stand ("0,560", "1234.5"). Two or more of one
   separator, each before exactly three digits, is grouping ("1,000,000",
   "1.000.000"); both separators together show both ("12.345,67"). A single
   separator before exactly three digits ("17.560", "50,640") is **ambiguous**
   and has no vote, nor has an integer without separators, a year, a time, a
   version string, an address or anything else this reads past.
2. **Votes that agree decide.** A document whose voting numerals are all one
   convention is that convention -- even where its language writes the other,
   which is then reported once for the document (`against_language`, below)
   and changes nothing else.
3. **Otherwise the language decides**: English writes a decimal point and
   German a decimal comma. "Otherwise" is an empty vote, a tie, *and a split
   vote*: a document that writes decimals both ways contradicts itself, and its
   numerals are then no witness to its convention. That last case departs from
   the rule as first agreed, which let a majority decide a split; DECISIONS
   601 records why (`voyager`'s source outvotes its one correct decimal two to one
   with its two planted ones).
4. **With no language either, a split vote goes to its majority**, and a tie or
   an empty vote has no winner. Every ambiguous numeral is then flagged as
   readable two ways, and the user is asked.

## What it reports

* `against_language`: one row per document, where its numerals decided the
  convention its language does not write -- an English text whose every
  voting numeral is a decimal comma, or a German one whose every voting
  numeral is a decimal point. It names each of those numerals. A warning, and
  rule 2 still stands: the numerals keep the decision, so an English text
  written with decimal commas on purpose is read as its author wrote it and
  costs one row, not one per numeral. Where the language is unknown or mixed
  nothing is contradicted and nothing fires. A split vote in a known language
  never reaches it: the language decided that document, and its numerals in
  the other convention are each an `other_convention` row already.
* `other_convention`: a voting numeral written in the convention its document
  did not decide. A warning.
* `readable_two_ways`: an ambiguous numeral whose separator is its document's
  own *decimal* mark ("17.560" in a decimal-point document), which that
  convention reads as a three-place fraction and the other as a thousands
  group; or any ambiguous numeral in a document with no winner. A warning. An
  ambiguous numeral whose separator is the document's own *grouping* mark
  ("17,560" under a decimal point) is that convention's ordinary thousands and
  is not flagged -- that is the asymmetry that keeps the check quiet on
  ordinary English.
* `reading_changed`: a merged numeral whose value differs from the source
  numeral it stands for -- the same digits beside the same word -- where the
  source's value was settled: a source's "17,560 miles" under a decimal point
  that the merge writes "17.560 miles". A document fault, and the only kind
  that moves the exit code.
* `reading_resolved`: the same, where the source numeral was itself flagged
  above and the merge wrote its other reading -- `voyager`'s "17.560 miles"
  written "17,560 miles". A warning: the merge took one side of a question the
  source left open, and whether it took the right one is the user's call.
  Were this a fault, every merge that fixed `voyager`'s planted errors would
  fail and every one that kept them would pass.

## Limits, stated rather than approximated

* The language test is a stop-word count over English and German and nothing
  else. A French, Spanish or Portuguese document is "unknown"; so is a text too
  short to count and a merge of an English and a German source. Unknown is
  safe: it asks rather than guesses.
* A list written without spaces ("items 4,5") is read as a decimal comma, and a
  product version outside the designation words below ("Claude 3.5") votes as
  a decimal.
* The two reading kinds pair numerals by their digits and the word after or
  the word before them. A value reworded ("17.56 thousand"), moved to another unit, or
  rewritten without a separator ("4,5" as "45") is not paired, and a numeral
  with no separator on either side is never compared: that is numeric drift,
  and the verbatim check owns it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

from .reconcile import Finding
from .segment import (
    CODE,
    CODE_BLOCK,
    HEADING,
    PATH,
    TITLE,
    URL,
    document_letter,
    find_spans,
    segment_document,
)

# The two conventions, named for their decimal mark. The grouping mark is the
# other separator in each.
POINT = "point"
COMMA = "comma"
CONVENTIONS = (POINT, COMMA)
NAMES = {POINT: "decimal point", COMMA: "decimal comma"}
DECIMAL_MARK = {POINT: ".", COMMA: ","}
GROUP_MARK = {POINT: ",", COMMA: "."}

# How a document's convention was decided. One of these on every document, so
# a reader can see whether the numerals or the words made the call.
BY_VOTES = "votes"          # every voting numeral agrees
BY_LANGUAGE = "language"    # no vote, a tie or a split, and the language decided
BY_MAJORITY = "majority"    # a split vote, no language, one side larger
UNDECIDED = "none"          # no winner: every ambiguous numeral is flagged

OTHER_CONVENTION = "other_convention"
READABLE_TWO_WAYS = "readable_two_ways"
READING_CHANGED = "reading_changed"
READING_RESOLVED = "reading_resolved"
AGAINST_LANGUAGE = "against_language"
KINDS = (OTHER_CONVENTION, READABLE_TWO_WAYS, READING_CHANGED, READING_RESOLVED,
         AGAINST_LANGUAGE)
# The one kind that is a fault in the merged document rather than a warning
# about a text: the merge now states a different value from the source it
# carries it from. 490's rule for a declared correction applies unchanged --
# nothing here can tell a correction from a corruption, so it stays a finding.
FAULTS = frozenset({READING_CHANGED})

# A candidate numeral: digits, optionally separated by single points or commas.
# Not preceded by a word character (`v1.2`, `A4`, `x86`), a separator (the tail
# of a longer token) or a slash or colon (`HTTP/1.1`, `1/2`, `17:59`); not
# followed by a separator, colon or slash that continues with a digit. A letter
# may follow, so "4,5km" is read; a letter may not precede.
_NUMERAL = re.compile(r"(?<![\w.,/:\x00])\d+(?:[.,]\d+)*(?![.,:/]\d)(?!\x00)")

# The word a numeral designates rather than measures: a version, a section, a
# figure. Matched against the word directly before it, lower-cased, trailing
# full stop dropped. "Python 3.12" and "Abschnitt 2.3" are not decimals.
_DESIGNATIONS = frozenset({
    "version", "versions", "release", "v", "ver", "rev", "revision", "build",
    "firmware", "kernel", "ios", "android", "macos", "windows", "python",
    "java", "node", "php", "http", "tls", "ssl", "bluetooth", "usb", "section",
    "sections", "chapter", "chapters", "figure", "fig", "table", "appendix",
    "step", "rule", "item", "clause", "article", "paragraph", "page", "pages",
    "pp", "p", "§", "no", "nr", "abschnitt", "kapitel", "abbildung", "abb",
    "tabelle", "anhang", "schritt", "regel", "punkt", "seite", "seiten", "s",
})
# A numeral followed by one of these is a clock time ("15.30 Uhr", "3.30 pm").
_TIME_WORDS = frozenset({"uhr", "am", "pm", "a.m", "p.m", "o'clock", "h."})

# The word beside a numeral, across spaces, brackets, quotes and a currency
# sign but not across another word or number.
_WORD_BEFORE = re.compile(r"([^\W\d_][\w'’.-]*|§)[\s(\[\"'“‘$€£]*$")
_WORD_AFTER = re.compile(r"^[\s)\]\"'”’%]*([^\W\d_][\w'’.-]*)")

# Stop words that are frequent in one language and rare or absent in the other.
# Deliberately left out: in, an, was, will, also, war, so, am, um, man -- each
# is a common word in both.
_ENGLISH = frozenset({
    "the", "and", "of", "to", "is", "that", "it", "for", "with", "as", "on",
    "by", "this", "are", "be", "from", "which", "were", "has", "have", "or",
    "not", "but", "its", "their", "they", "would", "been", "these", "than",
})
_GERMAN = frozenset({
    "der", "die", "das", "und", "ist", "nicht", "mit", "von", "zu", "den",
    "dem", "des", "ein", "eine", "einer", "einem", "eines", "auf", "für",
    "sich", "auch", "wird", "sind", "bei", "aus", "dass", "daß", "oder",
    "nach", "werden", "wurde", "über", "noch", "wie", "sie", "wir",
})
# Words too common to pair a merged numeral with a source one (`beside`): the
# stop words of both languages and the hedges a quantity takes.
_FUNCTION_WORDS = _ENGLISH | _GERMAN | frozenset({
    "a", "an", "in", "at", "about", "only", "some", "approximately", "around",
    "nearly", "almost", "over", "under", "up", "ca", "etwa", "rund", "um",
    "fast", "knapp", "über", "unter", "bis", "am", "im",
})
# A language is decided when its stop words are at least this many and this
# many times the other's. Below either, "unknown": a short or mixed text asks.
LANGUAGE_MINIMUM = 5
LANGUAGE_RATIO = 3
LANGUAGE_CONVENTION = {"en": POINT, "de": COMMA}
LANGUAGE_NAMES = {"en": "English", "de": "German"}
_WORDS = re.compile(r"[a-zäöüß]+")

# Shapes, from the separators alone.
_DECIMAL = "decimal"      # one separator, and it can only be a decimal mark
_GROUPED = "grouped"      # the separator(s) can only be grouping, or both are shown
_AMBIGUOUS = "ambiguous"  # one separator before exactly three digits
_MALFORMED = "malformed"  # neither convention: a version, a date, a list


def _shape(token: str) -> tuple[str, str]:
    """(shape, the convention it votes for, or "").

    Pure string work, so it is tested on the tokens alone.
    """
    separators = [c for c in token if c in ".,"]
    groups = re.split(r"[.,]", token)
    if not separators:
        return "", ""
    head = groups[0]
    if len(set(separators)) == 2:
        # Both marks: the last is the decimal and every earlier one groups.
        last = separators[-1]
        earlier = separators[:-1]
        if (any(mark == last for mark in earlier)
                or not 1 <= len(head) <= 3 or head.startswith("0")
                or any(len(group) != 3 for group in groups[1:-1])):
            return _MALFORMED, ""
        return _GROUPED, POINT if last == "." else COMMA
    mark = separators[0]
    votes = POINT if mark == "." else COMMA
    if len(separators) >= 2:
        if (1 <= len(head) <= 3 and not head.startswith("0")
                and all(len(group) == 3 for group in groups[1:])):
            # "1,000,000" groups with commas: the decimal-point convention.
            return _GROUPED, COMMA if votes == POINT else POINT
        return _MALFORMED, ""
    tail = groups[1]
    if len(tail) != 3 or head == "0" or head.startswith("0") or len(head) > 3:
        return _DECIMAL, votes
    return _AMBIGUOUS, ""


def read(token: str, convention: str) -> Decimal | None:
    """The value a reader of `convention` takes `token` for, or None.

    A careless reader and not a validating one: under a decimal point "4,5"
    is 45, because the comma is taken for grouping. That is the misreading the
    report has to name. None only where the token has two decimal marks, or a
    grouping mark after its decimal one, and no reading exists at all.
    """
    decimal, group = DECIMAL_MARK[convention], GROUP_MARK[convention]
    if token.count(decimal) > 1:
        return None
    if decimal in token and group in token.split(decimal, 1)[1]:
        return None
    try:
        return Decimal(token.replace(group, "").replace(decimal, "."))
    except InvalidOperation:  # pragma: no cover - the pattern admits digits only
        return None


def _plain(value: Decimal | None) -> str:
    """A value as a reader would say it: no exponent, no trailing zeros."""
    if value is None:
        return "not a number"
    text = format(value.normalize(), "f")
    return text


@dataclass(frozen=True)
class Numeral:
    """One numeral with a separator, where it stands, and how it can be read."""

    text: str
    document: str
    segment: str
    line: int
    shape: str
    votes: str
    # The words beside it, lower-cased: what pairs a merged numeral with the
    # source numeral it stands for.
    before: str
    after: str
    segment_text: str

    @property
    def digits(self) -> str:
        return re.sub(r"[.,]", "", self.text)

    def beside(self, other: "Numeral") -> str:
        """The word both numerals share a side with, or "" where none.

        The word after first, since a unit follows its value, then the word
        before. A function word pairs nothing: "is 1,250" and "is 1.250" are
        two sentences that happen to share a verb, not one value rewritten.
        """
        for mine, theirs in ((self.after, other.after), (self.before, other.before)):
            if mine and mine == theirs and mine not in _FUNCTION_WORDS:
                return mine
        return ""

    def plausible(self) -> frozenset[Decimal]:
        """Its value in either convention: every reading a reader could take."""
        return frozenset(value for value in (read(self.text, POINT),
                                             read(self.text, COMMA))
                         if value is not None)

    def readings(self, convention: str) -> frozenset[Decimal]:
        """Every value this numeral can have in a document of `convention`.

        One value for a voting numeral, whatever the document: its shape fixes
        it. One for an ambiguous numeral under a decided convention, and two
        under none -- which is the case the user is asked about.
        """
        if self.votes:
            value = read(self.text, self.votes)
            return frozenset({value}) if value is not None else frozenset()
        if convention:
            value = read(self.text, convention)
            return frozenset({value}) if value is not None else frozenset()
        return frozenset(value for value in (read(self.text, POINT),
                                             read(self.text, COMMA))
                         if value is not None)


@dataclass(frozen=True)
class Convention:
    """What one document was decided to be, and on what evidence."""

    document: str
    convention: str
    decided_by: str
    point_votes: tuple[str, ...]
    comma_votes: tuple[str, ...]
    language: str
    english_words: int
    german_words: int
    numerals: tuple[Numeral, ...] = field(default=(), compare=False, repr=False)

    def as_dict(self) -> dict:
        """For the JSON report. Every field a reader needs to redo the call."""
        return {
            "document": self.document,
            "convention": NAMES.get(self.convention, ""),
            "decided_by": self.decided_by,
            "votes": {"decimal_point": list(self.point_votes),
                      "decimal_comma": list(self.comma_votes)},
            "language": self.language,
            "stop_words": {"en": self.english_words, "de": self.german_words},
        }

    @property
    def why(self) -> str:
        """The decision in words, for a finding's detail and the report table."""
        points, commas = len(self.point_votes), len(self.comma_votes)
        tally = f"{points} numeral(s) voting decimal point, {commas} decimal comma"
        language = {"en": "English", "de": "German"}.get(self.language, "")
        if self.decided_by == BY_VOTES:
            return f"by its numerals ({tally})"
        if self.decided_by == BY_LANGUAGE:
            return f"by its language, {language} ({tally})"
        if self.decided_by == BY_MAJORITY:
            return f"by the majority of its numerals, language unknown ({tally})"
        return f"undecided: {tally}, and its language is unknown"


def language(text: str) -> tuple[str, int, int]:
    """("en" | "de" | "", English stop words, German stop words).

    A count, and it knows two languages. Anything else, anything short and
    anything mixed is "": the caller then asks rather than guesses.
    """
    words = _WORDS.findall(text.lower())
    english = sum(1 for word in words if word in _ENGLISH)
    german = sum(1 for word in words if word in _GERMAN)
    if english >= LANGUAGE_MINIMUM and english >= LANGUAGE_RATIO * german:
        return "en", english, german
    if german >= LANGUAGE_MINIMUM and german >= LANGUAGE_RATIO * english:
        return "de", english, german
    return "", english, german


def _masked(text: str) -> str:
    """The text with code, links, URLs, paths and versions blanked out."""
    # Not a link's text, which is prose, and not a version span: the
    # segmenter's version pattern takes "1.000.000" for one, and grouping is
    # a vote. "1.2.3" is refused by `_shape` instead.
    spans = [span for span in find_spans(text)
             if span.kind in (CODE, URL, PATH)]
    characters = list(text)
    for span in spans:
        for index in range(span.start, span.end):
            characters[index] = "\x00"
    return "".join(characters)


def numerals_of(text: str, document: str, letter: str) -> tuple[Numeral, ...]:
    """Every numeral with a separator in `text`, outside code and designations."""
    found: list[Numeral] = []
    for item in segment_document(text, letter, document).segments:
        if item.kind == CODE_BLOCK:
            continue
        body = _masked(item.text)
        for match in _NUMERAL.finditer(body):
            token = match.group(0)
            shape, votes = _shape(token)
            if not shape or shape == _MALFORMED:
                continue
            before = _WORD_BEFORE.search(body[:match.start()])
            word_before = (before.group(1).lower().rstrip(".")
                           if before else "")
            if word_before in _DESIGNATIONS:
                continue
            after = _WORD_AFTER.match(body[match.end():])
            word_after = after.group(1).lower() if after else ""
            if word_after in _TIME_WORDS or word_after.rstrip(".") in _TIME_WORDS:
                continue
            # A heading or title that opens with a section number: "2.3 Results".
            if (item.kind in (TITLE, HEADING) and match.start() == 0):
                continue
            found.append(Numeral(
                text=token, document=document, segment=item.id,
                line=item.line, shape=shape, votes=votes,
                before=word_before, after=word_after.rstrip(".,;:"),
                segment_text=item.text))
    return tuple(found)


def decide(document: str, text: str, letter: str) -> Convention:
    """The convention of one document, by the rule in the module note."""
    numerals = numerals_of(text, document, letter)
    points = tuple(n.text for n in numerals if n.votes == POINT)
    commas = tuple(n.text for n in numerals if n.votes == COMMA)
    spoken, english, german = language(text)
    if points and not commas:
        convention, how = POINT, BY_VOTES
    elif commas and not points:
        convention, how = COMMA, BY_VOTES
    elif spoken:
        convention, how = LANGUAGE_CONVENTION[spoken], BY_LANGUAGE
    elif len(points) != len(commas):
        convention = POINT if len(points) > len(commas) else COMMA
        how = BY_MAJORITY
    else:
        convention, how = "", UNDECIDED
    return Convention(document, convention, how, points, commas, spoken,
                      english, german, numerals)


def _factor(before: Decimal, after: Decimal) -> str:
    """", 1,000 times larger", or "" where the ratio is no clean power of ten."""
    if not before or not after:
        return ""
    ratio = after / before
    for power in range(1, 7):
        scale = Decimal(10) ** power
        if ratio == scale:
            return f", {scale:,} times larger"
        if ratio * scale == 1:
            return f", {scale:,} times smaller"
    return ""


def _flag(numeral: Numeral, convention: Convention) -> str:
    """The warning kind this numeral earns in its own document, or ""."""
    decided = convention.convention
    if numeral.votes:
        return OTHER_CONVENTION if decided and numeral.votes != decided else ""
    if numeral.shape != _AMBIGUOUS:
        return ""
    # No winner: every ambiguous numeral is a question. A winner: only the
    # one whose separator is the winner's decimal mark, which the winner reads
    # as a three-place fraction and the other convention as thousands.
    if not decided or DECIMAL_MARK[decided] in numeral.text:
        return READABLE_TWO_WAYS
    return ""


def _warning(numeral: Numeral, convention: Convention, shown: str) -> Finding:
    """The sentence for a numeral `_flag` marked, naming both readings."""
    decided = convention.convention
    where = f"{shown}, line {numeral.line}"
    if numeral.votes:
        own = read(numeral.text, numeral.votes)
        theirs = read(numeral.text, decided)
        detail = (f"{numeral.text!r} ({where}) is written in the "
                  f"{NAMES[numeral.votes]} convention, where it reads "
                  f"{_plain(own)}; this document uses the {NAMES[decided]}, "
                  f"decided {convention.why}, and a reader of that "
                  f"convention takes it for {_plain(theirs)}")
        kind = OTHER_CONVENTION
    else:
        if decided:
            other = COMMA if decided == POINT else POINT
            here = read(numeral.text, decided)
            there = read(numeral.text, other)
            why = (f"this document uses the {NAMES[decided]}, decided "
                   f"{convention.why}, and reads it {_plain(here)}, a "
                   f"three-place fraction; in the {NAMES[other]} convention "
                   f"it is {_plain(there)}")
        else:
            why = (f"this document's convention is {convention.why}, so it "
                   f"is {_plain(read(numeral.text, POINT))} with a decimal "
                   f"point and {_plain(read(numeral.text, COMMA))} with a "
                   f"decimal comma")
        detail = (f"{numeral.text!r} ({where}) can be read two ways: {why}. "
                  f"Which is meant is the author's call")
        kind = READABLE_TWO_WAYS
    return Finding(kind, detail, segment=numeral.segment,
                   document=convention.document,
                   source_text=numeral.segment_text)


def _against_language(convention: Convention, shown: str) -> Finding | None:
    """The document's row where its numerals outvoted its language, or None.

    Only a unanimous vote can get here: a split vote in a known language was
    decided by that language, and a majority decides only where the language
    is unknown, which contradicts nothing. The numerals keep the decision
    (rule 2); this names them, once, and moves nothing.
    """
    spoken = convention.language
    if not spoken or LANGUAGE_CONVENTION[spoken] == convention.convention:
        return None
    named = [n for n in convention.numerals if n.votes == convention.convention]
    expected = LANGUAGE_CONVENTION[spoken]
    listed = [f"{n.text!r} (line {n.line})" for n in named]
    listing = (listed[0] if len(listed) == 1
               else ", ".join(listed[:-1]) + " and " + listed[-1])
    language = LANGUAGE_NAMES[spoken]
    first = named[0]
    misread = read(first.text, expected)
    someone = {"en": "an English reader", "de": "a German reader"}[spoken]
    reader = (f"{someone} takes {first.text!r} for {_plain(misread)}"
              if misread is not None else
              f"{someone} has no reading of {first.text!r} at all")
    segments = ", ".join(dict.fromkeys(n.segment for n in named))
    detail = (f"{shown} is {language} by its words ({convention.english_words} "
              f"English and {convention.german_words} German stop words), and "
              f"every numeral in it that can be read only one way is written in "
              f"the {NAMES[convention.convention]} convention: {listing}. "
              f"{language} writes a {NAMES[expected]}, and {reader}. Those "
              f"numerals decided the document's convention, so none of them is "
              f"a row of its own; whether the {NAMES[convention.convention]} "
              f"is meant is the author's call")
    return Finding(AGAINST_LANGUAGE, detail, segment=segments,
                   document=convention.document)


def _readings(sources: dict[str, Convention], merged: Convention,
              shown: dict[str, str]) -> list[tuple[Numeral, Finding]]:
    """Merged numerals whose value differs from the source numeral they carry.

    Paired by their digits and a shared neighbouring word, and only where both
    carry a separator. A merged value that any paired source numeral already
    has is no change: the merge took that source's side. A change from a
    source numeral that was itself flagged, to a value it could be read as, is
    `reading_resolved`; any other change is `reading_changed`.
    """
    found: list[tuple[Numeral, Finding]] = []
    for numeral in merged.numerals:
        mine = numeral.readings(merged.convention)
        if not mine:
            continue
        partners = [(convention, candidate, word)
                    for convention in sources.values()
                    for candidate in convention.numerals
                    if candidate.digits == numeral.digits
                    for word in (candidate.beside(numeral),) if word]
        if not partners or any(candidate.readings(convention.convention) & mine
                               for convention, candidate, _ in partners):
            continue
        convention, source, word = partners[0]
        before = source.readings(convention.convention)
        resolved = bool(_flag(source, convention)) and mine <= source.plausible()
        factor = (_factor(next(iter(before)), next(iter(mine)))
                  if len(before) == 1 and len(mine) == 1 else "")
        name = shown.get(convention.document) or convention.document
        settled = ("a value that document itself left open, so the merge "
                   "took its other reading" if resolved else
                   "so the same digits now state a different value")
        found.append((numeral, Finding(
            READING_RESOLVED if resolved else READING_CHANGED,
            f"{name} writes {source.text!r} beside {word!r} (line "
            f"{source.line}), which reads "
            f"{' or '.join(sorted(_plain(v) for v in before))} in its "
            f"{NAMES.get(convention.convention, 'undecided')} convention; the "
            f"merge writes {numeral.text!r} (line {numeral.line}), which reads "
            f"{' or '.join(sorted(_plain(v) for v in mine))} in its own "
            f"{NAMES.get(merged.convention, 'undecided')} convention{factor}: "
            f"{settled}",
            segment=numeral.segment, document=convention.document,
            source_text=source.segment_text, merge_text=numeral.segment_text)))
    return found


@dataclass(frozen=True)
class Checked:
    """Everything the check produced for one run."""

    conventions: tuple[Convention, ...]
    findings: tuple[Finding, ...]

    @property
    def faults(self) -> tuple[Finding, ...]:
        """The findings that move the exit code."""
        return tuple(f for f in self.findings if f.kind in FAULTS)


def check(documents: dict[str, str], merged: str | None, merged_name: str,
          shown: dict[str, str] | None = None) -> Checked:
    """Decide every document's convention and report what does not fit it.

    `documents` is the sources by canonical filename, `merged` the merged text
    or None where there is none, and `shown` the names the caller gave the
    files, used in the sentences a reader sees. Sources first, in the order
    given, then the merge; within a document, reading order.
    """
    shown = shown or {}
    sources = {name: decide(name, text, document_letter(name) or "x")
               for name, text in documents.items()}
    conventions = list(sources.values())
    findings: list[Finding] = []
    for name, convention in sources.items():
        # The document's own row first: every numeral row below it is read
        # against a decision this row says the language disputes.
        findings += [finding for finding in
                     (_against_language(convention, shown.get(name) or name),)
                     if finding]
        findings += [_warning(numeral, convention, shown.get(name) or name)
                     for numeral in convention.numerals
                     if _flag(numeral, convention)]
    if merged is not None:
        whole = decide(merged_name, merged, "m")
        conventions.append(whole)
        readings = _readings(sources, whole, shown)
        findings += [finding for finding in
                     (_against_language(whole, shown.get(merged_name) or merged_name),)
                     if finding]
        # A merged numeral a reading kind already names is not warned about a
        # second time: the pairing says more than the document alone can.
        paired = {numeral for numeral, _ in readings}
        findings += [_warning(numeral, whole, shown.get(merged_name) or merged_name)
                     for numeral in whole.numerals
                     if _flag(numeral, whole) and numeral not in paired]
        findings += [finding for _, finding in readings]
    return Checked(tuple(conventions), tuple(findings))

# What the check is, said once for the JSON report and the section note.
PREDICATE = (
    "each document's convention (decimal point or decimal comma) is decided by "
    "its numerals that can only be read one way when they all agree; "
    "otherwise by its language (English: point, German: comma, from a "
    "stop-word count); otherwise by the majority of its numerals; and on a tie "
    "with no language by nobody. A numeral in the other convention is "
    "reported, as is a separator before exactly three digits that the "
    "document's convention reads as a fraction, or any such numeral where "
    "nothing decided. A document whose numerals decided the convention its "
    "language does not write is reported once, naming them. A merged numeral "
    "with the same digits before the same word as a source numeral but a "
    "different value is a fault. No number is rewritten and no model is asked"
)
