"""Measure what a merge did to its sources, without asking a model anything.

The instrument, and it predates the cure on purpose. Every figure here is a
set operation or a string comparison over two texts that already exist, so it
can be run over the merges already on disk and say how large the problem is
before a single prompt is changed.

Five questions, each with its denominator attached:

    coverage      how many of a source's segments are in the merge, of how many
    near-matches  of the absent ones, which look reworded and which look gone
    verbatim      does every invariant-core token survive unchanged
    duplication   does the merge state the same thing twice
    order         did anything actually get merged, or were the sources stapled

## What an absence means, and the two ways to read it

**On its own, an absent segment is unexplained rather than wrong.** The
corpus this was first run over was produced under a prompt that granted the
merge model wide licence to restructure and reword, and carries no disposition
records to check an absence against. Over that corpus the absent count is an
*upper bound on silent loss* and nothing stronger. Read as a defect count it
would repeat an old mistake in the opposite direction: a number that sounds
like it measures fidelity while measuring something else.

`findings` is the other reading, and it needs the merge to have declared
something. Given the merge's disposition records it splits
that same count in two: an absence the merge owned up to goes to the review
queue with its reason, and an absence it did not is the finding the whole design
exists to produce. Everything above `findings` still works without any of that,
because the instrument has to be able to measure a corpus recorded before the
cure existed.

**No model is consulted anywhere in this module**, `findings` included. Every
one of its nine checks is a set operation, a string containment, a division or
an equality test.
That is the point of the disposition model: the merger writes down what it did,
and checking the claim needs arithmetic rather than a second opinion.

## Matching, and why it is this lenient and no more

A segment counts as present when its text occurs in the merge after whitespace
is collapsed on both sides, allowing the first character's capitalisation to
differ. That is exactly the tolerance check 2 below applies,
and it is the tolerance a reader would grant: a sentence lifted into a list, a
paragraph rewrapped, or a clause that now opens with a lower-case letter because
it was folded into an attributing sentence has not lost a fact.

Nothing else is normalised. Case inside the segment, punctuation, digits and
word order all have to match, because those are the things whose change is the
defect being looked for.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import TYPE_CHECKING, Sequence

from . import config, parsing
from . import segment as segment_module
from .segment import (
    CODE_BLOCK,
    HEADING,
    Document,
    Segment,
    Span,
    TITLE,
    document_id,
    plain,
    segment_document,
)

if TYPE_CHECKING:  # pragma: no cover - a type name, never a runtime import
    # Under the annotation only. `decompose` reaches an endpoint and this
    # module must stay clear of everything that does -- the reconciliation is
    # mechanical, and `test_the_reconciler_asks_nothing_of_a_model` reads this
    # file to prove it. `restatements` reads three fields off a Claim and
    # nothing else, so no import is needed at runtime.
    from .decompose import Claim

# How alike an absent segment and its closest counterpart in the merge must be
# before the absence is called a probable rewording rather than a probable
# silent loss.
#
# Plotted, not guessed. Over the first corpus's 72 merges, 1422 source segments
# were examined and 1293 found outright; the 129 that were not are 26 distinct
# cases repeated across samples and conditions, and their best ratios cluster
# at 0.3548-0.5915 and at 0.7765-0.8732 with nothing at all in between. That
# gap is 0.1849 wide, nearly twice the next largest at 0.0968, and any
# threshold inside it produces the identical split — 42 reworded, 87 absent.
# 0.68 sits mid-gap (the exact midpoint is 0.6840), so the classification is
# the one that survives the largest perturbation of the corpus rather than the
# one that happens to hold at a round number.
#
# 26 cases, not 129 observations, is the honest count of the evidence: the
# sweep recorded three samples of two conditions per fixture and the same
# segment recurs across them, so treating each observation as independent
# would inflate the support for this constant sixfold.
#
# What sits on each side is the reason to trust it. Above: `The relay listens
# on port 8443.` against `The Vandrell Relay listens on port 8443.`, and a
# title superseded by one naming both documents. Below: titles matched against
# whatever sentence they least resembled, which is what a dropped title looks
# like, and `dropped_claim`'s planted omission.
#
# One class is misfiled and is named here rather than left to be found: the
# `paraphrase` fixture restates the same facts in different words by
# construction, and 7 of its segments score 0.3548-0.5556 against the merge
# text that does carry them. Character similarity cannot see a paraphrase, so
# those land in `absent` — 21 of the corpus's 87 absent observations, the
# largest single share, and the same blind spot `tests/analyse_merges.py`
# records for duplication, in the same corpus, for the same reason.
NEAR_MATCH = 0.68

# The merge's own segments are lettered `m`. It is not a source and never gets
# a disposition record; the letter exists so that a segment printed in a report
# can be told from the source segments beside it.
MERGE_LETTER = "m"

# Two segments may only be called counterparts by containment if they are close
# enough in length that `similarity` could have reached NEAR_MATCH on its own.
# difflib's ratio cannot exceed 2m/(m+M) for lengths m <= M, so that condition
# is exactly m/M >= NEAR_MATCH / (2 - NEAR_MATCH), and the guard is derived from
# the threshold rather than being a second constant to keep in step with it.
#
# Without it, attribution is nonsense on short segments: the heading `Times` is
# contained in `He also lost his orientation several times.`, `Work` in `she
# worked in the rosegarden`, and `Winter` in half the sentences of a document
# about seasons. Each spurious match drags an unrelated ordinal into the order
# check, and `disjoint_sources` — a hand-built staple — came back non-monotone
# on matches like those rather than on anything the merge had actually done.
LENGTH_FLOOR = NEAR_MATCH / (2 - NEAR_MATCH)

# The comment above diagnosed the containment problem and `comparable` fixed it
# for `order`, which compares two segments. `locate` compares a segment against
# the *whole flattened merge*, where `comparable` is meaningless -- one segment
# is never a comparable length to an entire document -- so `locate` went on
# asking a bare `occurs` and the heading `## Limits` counted as present because
# the merge contained "Concurrency limits apply during peak windows."
#
# A title or a heading is a label: it names a slot in the document's structure,
# and it survives a merge only if the merge still has that slot. Its words
# turning up inside a sentence is not survival, it is a coincidence of
# vocabulary -- which is exactly the case above. So a label is looked for among
# the merge's labels, and nothing else changes.
#
# List items and table rows are *not* labels, though they are just as short.
# They carry content rather than name a slot, and a merge that folds a
# five-item list into one prose sentence has kept every one of them: on the
# recorded corpus that fold is real (`tests/responses/pairs/`,
# `merge-639edb26f70bc957`, five list items in one sentence) and treating them
# as labels calls a content-complete merge five absences. They stay exposed to
# the coincidence this fixes for labels; closing that costs false accusations
# and is not closed here.
LABEL_KINDS = (TITLE, HEADING)

_WORD_EDGE = re.compile(r"\w")


def comparable(first: str, second: str) -> bool:
    """Are these two flattened texts of similar enough length to compare?"""
    shorter, longer = sorted((len(first), len(second)))
    return longer > 0 and shorter / longer >= LENGTH_FLOOR


def flatten(text: str) -> str:
    """Whitespace collapsed, line-leading notation removed. The only normalisation.

    Both halves are here rather than at the call sites because every comparison
    in this module has the same two sides: a `Segment.text`, which carries no
    notation and never has, and a stretch of the merge, which carries whatever
    the model wrote. `plain` is a no-op on the first — there is no `## ` left to
    take off — and on the second it undoes exactly what `render_sources` showed
    the model. One function, so a new comparison cannot be added that normalises
    one side and not the other.

    Fenced blocks survive it byte for byte, which is what keeps the invariant
    core honest: a code block is one token here and `plain` does not reach
    inside a fence.
    """
    return " ".join(plain(text).split())


def code_exact(text: str) -> str:
    """A fenced block, normalised only for line endings and trailing spaces.

    `flatten` collapses every run of whitespace, which is right for prose and
    wrong for code: it made check 5 -- the one check promising a fenced block
    survives byte for byte -- pass a block whose indentation had been rewritten.
    Re-indenting a YAML block from four spaces to two changes what it means and
    produced no finding at all.

    CRLF and trailing whitespace are still normalised, because neither is
    visible and neither changes what the block says. Interior whitespace is
    not, because inside a fence it is content.
    """
    return "\n".join(line.rstrip()
                     for line in text.replace("\r\n", "\n").split("\n")).strip()



def _uncapitalised(text: str) -> str:
    return text[:1].swapcase() + text[1:]


def _index(needle: str, haystack: str) -> int:
    """Where this needle starts, or -1. The one place the leniency lives."""
    at = haystack.find(needle)
    return at if at >= 0 else haystack.find(_uncapitalised(needle))


def occurs(needle: str, haystack: str) -> bool:
    """Is this segment's text in that merge, to the tolerance described above?

    Both arguments are already flattened. The first-character retry is the
    whole of the leniency: a segment folded into an attributing sentence keeps
    every word and loses one capital, and `merge.md` says in as many words that
    wrapping a segment in the attribution a disagreement requires is not a
    departure.
    """
    return _index(needle, haystack) >= 0


def resolves(replacement: str, merged_flat: str) -> bool:
    """Does this replacement point at a span of the merged document?

    A replacement is capped (`parsing.REPLACEMENT_MAX`), and a longer span is
    given as its two ends with the middle elided, so this asks `occurs` of each
    end in turn and looks for the second only after the first. Asking it of the
    whole string would fail on the marker, and asking it of the ends
    independently would accept two ends in the wrong order, or taken from two
    unrelated places in the merge. An unelided replacement is one part and this
    is `occurs`.
    """
    rest = merged_flat
    for part in parsing.anchor_parts(replacement):
        at = _index(part, rest)
        if at < 0:
            return False
        rest = rest[at + len(part):]
    return True


def token_present(token: str, haystack: str) -> bool:
    """Does this invariant-core token appear in the merge, whole?

    Bounded on both sides where the token itself ends in a word character, so
    `512` is not found inside `5120` and `30` is not found inside `30s`. The
    second is the point: `30 seconds` rendered as `30s` is the abbreviation
    the invariant core forbids, and an unbounded search would call it survival.
    """
    left = r"(?<!\w)" if _WORD_EDGE.match(token[:1]) else ""
    right = r"(?!\w)" if _WORD_EDGE.match(token[-1:]) else ""
    return re.search(left + re.escape(token) + right, haystack) is not None


def similarity(left: str, right: str) -> float:
    """Character-level similarity of two flattened texts, case-insensitively."""
    return SequenceMatcher(None, left.casefold(), right.casefold()).ratio()


# How a word-level difference is marked, and the one rule the notation has to
# meet: **it must survive being plain**. The report renders on three
# surfaces and one of them is a terminal with no colour guarantee, so a
# difference carried by styling alone would be a difference two of the three
# readers never see. `wdiff`'s notation is the form that carries itself --
# removed words inside `[-...-]`, added words inside `{+...+}` -- and it is
# already what anyone who has used a word diff expects.
REMOVED = ("[-", "-]")
ADDED = ("{+", "+}")

# Above this a word diff stops being shorter than the two texts it replaces.
# Measured on the operator's own finding rather than chosen: their reworded
# segment is 96 characters against a merge segment at 0.99 similarity, and its
# diff is 8 words. A pair at 0.6 similarity diffs to nearly every word marked
# twice, which is longer than printing both and harder to read -- so below this
# ratio the surfaces print the two texts instead, and say which is which.
#
# It is the same figure `NEAR_MATCH` uses, and deliberately: `Located.verdict`
# already calls anything at or above it *reworded*, which is exactly the claim
# a diff illustrates. A second threshold here would be a second opinion about
# when two texts are versions of one text.
DIFF_FLOOR = 0.8

# Past this a rendered difference is a paragraph rather than a row, and the
# rule for table cells applies: the table stays readable and the detail goes once, nearby. A
# diff longer than this is truncated with an ellipsis and the two texts stay
# available in their own fields, so nothing is lost by the cap.
DIFF_MAX = 600

# How alike the two halves of one changed run must be before the run is marked
# character by character instead of whole. A character diff was rejected once,
# rightly for the case it was judged on: run over the *whole* text it marks
# the insides of unrelated words and is unreadable. This is the other case.
# The word diff still decides which run changed; this only says where inside
# that run, and only where the two halves are versions of each other.
#
# The operator's report is the measurement that asks for it: their entire
# difference was one space, `(Mingg)verwendet.` against `(Mingg) verwendet.`,
# and a word diff renders that as two whole tokens swapped -- so a
# one-character change reads as a rewritten clause and the reader has to
# compare the two tokens letter by letter themselves, which is the work the
# diff exists to do.
CHAR_FLOOR = 0.5

# And how much of the run may be marked before printing it twice is clearer.
# The property, stated before the number: the fine form is an **annotation on
# a run the reader can still read**, so it is right exactly while the unchanged
# part dominates. Past that the run has been rewritten, and a rewrite is
# legible as two whole texts rather than as a run with most of its letters
# bracketed.
#
# Measured on the cases this project has in hand rather than chosen: one space
# marks 1 of 18 characters (6%) and `8443.` against `8444.` marks 1 of 5
# (20%), and both are annotations;
# the rejected case, `The breeding` against `Breeding`, marks 5 of 12 (42%)
# and reads worse than the two words whole, which is why a character diff was
# rightly rejected there.
CHAR_SHARE = 0.34


def _balanced(text: str) -> bool:
    """Does every marker this text opens also close in it?

    Counted rather than parsed, which is the same reading `DIFF_LEGEND` teaches
    and the same one a person does. A document that itself contains `[-` would
    fool it, and would have fooled every earlier version of this rule too.
    """
    return (text.count(REMOVED[0]) == text.count(REMOVED[1])
            and text.count(ADDED[0]) == text.count(ADDED[1]))


def _refine(left: str, right: str) -> str | None:
    """One changed run, marked character by character, or None to leave it whole.

    Three clauses, all mechanical, because a threshold argued from taste is a
    threshold the next reader cannot check:

    1. The two halves must be at least `CHAR_FLOOR` alike. Below that they are
       not versions of one another and marking their insides is unreadable.
    2. At most `CHAR_SHARE` of the run may end up inside markers, so what is
       shown is a run with a difference in it rather than a bracketed rewrite.
    3. The marked form must be **shorter** than printing both halves whole.
       Where it is not, the fine detail has cost more than it showed and the
       coarse form is the better answer by the surfaces' own measure.
    """
    if not left or not right:
        return None
    if SequenceMatcher(None, left, right).ratio() < CHAR_FLOOR:
        return None
    out: list[str] = []
    marked = 0
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, left, right).get_opcodes():
        if tag == "equal":
            out.append(left[i1:i2])
            continue
        marked = max(marked, i2 - i1, j2 - j1)
        if tag in ("replace", "delete"):
            out.append(REMOVED[0] + left[i1:i2] + REMOVED[1])
        if tag in ("replace", "insert"):
            out.append(ADDED[0] + right[j1:j2] + ADDED[1])
    if marked > CHAR_SHARE * max(len(left), len(right)):
        return None
    fine = "".join(out)
    coarse = REMOVED[0] + left + REMOVED[1] + " " + ADDED[0] + right + ADDED[1]
    return fine if len(fine) < len(coarse) else None


def difference(source: str, merge: str, floor: float = DIFF_FLOOR) -> str:
    """What changed between two texts, word by word, or `` when it would not help.

    **Shows the difference rather than asserting one.** The operator's report
    is the requirement in one sentence: *"it would be very helpful to highlight
    how it was reworded. So that the user can directly see the difference."* The
    reconciler already holds both strings and the similarity, so this costs no
    new comparison -- it renders one that was already made.

    Word-level rather than character-level, because a character diff over
    prose marks the inside of words and is unreadable; `SequenceMatcher` over a
    whitespace split is the form that produces "these three words became those
    two". Whitespace is normalised on both sides first, for `flatten`'s reason:
    a line break that moved is not a rewording and would otherwise mark the
    whole paragraph.

    **Words decide what changed; characters say where inside it.** A
    `replace` run whose two halves are versions of each other is marked
    character by character by `_refine`, so a one-space difference renders as
    one space rather than as two whole tokens swapped. Every other opcode is
    unchanged, and `_refine` declines wherever the fine form would be longer or
    the halves are too far apart -- so the top-level diff stays word-level and
    the judgement against a character diff over whole prose stands.

    Empty when the two are too far apart to diff usefully (`floor`), when
    either side is missing, or when they are identical. An empty answer is the
    signal to print the two texts instead, which every surface does.
    """
    left, right = " ".join((source or "").split()), " ".join((merge or "").split())
    if not left or not right or left == right:
        return ""
    if similarity(left, right) < floor:
        return ""
    left_words, right_words = left.split(), right.split()
    matcher = SequenceMatcher(None, left_words, right_words)
    out: list[str] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            out.extend(left_words[i1:i2])
            continue
        gone, came = " ".join(left_words[i1:i2]), " ".join(right_words[j1:j2])
        if tag == "replace":
            fine = _refine(gone, came)
            if fine is not None:
                out.append(fine)
                continue
        if tag in ("replace", "delete"):
            out.append(REMOVED[0] + gone + REMOVED[1])
        if tag in ("replace", "insert"):
            out.append(ADDED[0] + came + ADDED[1])
    rendered = " ".join(out)
    if len(rendered) > DIFF_MAX:
        # Cut on a word boundary, never mid-marker: a `[-` with no `-]` after
        # it reads as a broken renderer rather than as a truncation.
        #
        # **A word boundary is not enough on its own.** A refined run puts
        # markers inside a word and can mark a space -- `{+ +}` is the
        # operator's own case -- so `rsplit` on a space can now cut inside a
        # marker and leave exactly the dangling `{+` this rule forbids. So the
        # cut is walked back until the markers balance, which is a property of
        # the string rather than a guess about where words are.
        cut = rendered[:DIFF_MAX].rsplit(" ", 1)[0]
        while cut and not _balanced(cut):
            cut = cut[:-1]
        rendered = cut + " ..."
    return rendered


@dataclass(frozen=True)
class Located:
    """One source segment, and what became of it as far as text can tell."""

    segment: Segment
    # present | reworded | absent. `reworded` is a reading of a similarity
    # score and not an observation, which is why it is not called `changed`.
    verdict: str
    ratio: float = 0.0
    # The merge segment it most resembles, for a reader who has to judge the
    # call themselves. Empty when it was found outright.
    nearest: str = ""
    # And its text. Carried rather than looked up again by the caller: the
    # finding has to show the reader what the merge says instead, and a second
    # lookup by id is a second chance to name a different segment.
    nearest_text: str = ""

    @property
    def found(self) -> bool:
        return self.verdict == PRESENT


PRESENT = "present"
REWORDED = "reworded"
ABSENT = "absent"


@dataclass(frozen=True)
class Coverage:
    """One source's segments, located in the merge. The denominator is `total`."""

    document: Document
    located: tuple[Located, ...]

    @property
    def total(self) -> int:
        return len(self.located)

    @property
    def present(self) -> int:
        return sum(1 for item in self.located if item.verdict == PRESENT)

    @property
    def reworded(self) -> int:
        return sum(1 for item in self.located if item.verdict == REWORDED)

    @property
    def absent(self) -> int:
        return sum(1 for item in self.located if item.verdict == ABSENT)

    def of(self, verdict: str) -> tuple[Located, ...]:
        return tuple(item for item in self.located if item.verdict == verdict)

    def line(self) -> str:
        """One line carrying the figure and its denominator, never one without."""
        name = self.document.filename or self.document.id
        return (
            f"{name}: {self.present}/{self.total} segments present, "
            f"{self.reworded} near, {self.absent} absent"
        )


@dataclass(frozen=True)
class Missing:
    """One invariant-core token that did not survive into the merge."""

    document: str
    segment: str
    kind: str
    text: str
    unit: str = ""


@dataclass(frozen=True)
class Duplicate:
    """Content the merge states more than once, and how many times."""

    text: str
    count: int
    exact: bool


@dataclass(frozen=True)
class Restatement:
    """One claim the merged document states on two or more of its own lines.

    The claim-level half of check 9, and the unit it is counted in: one entry
    per repeated claim text, carrying every line the decomposer anchored a copy
    of it to. `lines` is two or more by construction -- a text found on one line
    is not a restatement, whatever the decomposer did with it.
    """

    text: str
    lines: tuple[int, ...]


@dataclass(frozen=True)
class Order:
    """Whether the merge interleaved its sources or stapled them end to end.

    `runs` is the number of contiguous blocks the merge's located segments fall
    into by source document: two sources stapled together give 2, whatever else
    was dropped along the way, and a merge that consolidated even one section
    gives more. It replaces an earlier test, for the reason below.

    The predicate it replaces compared the merge against the two sources
    concatenated and called it a staple above a similarity ratio. That test
    passes only on a near-total concatenation, and the merge that prompted the
    change was a concatenation *that had dropped both titles and both
    summary fields* — enough deleted to pull the ratio down, not nearly enough
    to constitute merging. Counting runs asks the question the ratio was
    standing in for: did anything get interleaved?

    Runs alone over-accuse, and the corpus says so. `structure_added-off-0`
    resolves a conflict, attributes both values by filename and drops nothing
    that matters, yet its three attributable segments fall a, b, b — because
    two documents about one subject naturally contribute in blocks. So a staple
    also has to have kept each source's *internal order*, which that merge did
    not: it states source B's TLS line before source B's health-check line.
    `monotone` carries that second condition, and both are required.

    `attributed` is the evidence base. Segments both sources state identically
    are attributable to neither and are excluded, so `runs` of 2 over 3
    attributed segments is a far weaker observation than 2 over 40, and a
    reader cannot see which without the denominator.

    Below a certain evidence base the observation is not weak but empty, which
    is `conclusive`. `attribution_swapped-off-0` is a correct merge: it states
    the shared facts once, surfaces the disputed read timeout under both
    filenames and chooses neither. Both shared sentences are attributable to
    neither document, leaving one attributed segment per source — and one each
    can only ever come out as two runs of one, whatever the merge did. Calling
    that a staple would be reading the arithmetic, not the document.
    """

    sequence: tuple[str, ...]
    runs: int
    interleaved: bool
    monotone: bool
    attributed: int
    headings_total: int
    headings_present: int

    @property
    def conclusive(self) -> bool:
        """Could this evidence base have shown interleaving had there been any?"""
        return len(self.sequence) > len(set(self.sequence))

    @property
    def blocked(self) -> bool:
        """Every source contributed at least two segments. A block of one is not one.

        `runs == distinct` is satisfied for free by any source that contributed
        a single segment: one segment is trivially contiguous and trivially in
        its own order, so that source votes yes whatever the merge did. The
        docstring above already reasons about `structure_added-off-0`'s a, b, b
        and excludes it by `monotone` — but that merge is excluded by the
        *ordering* of B's two segments, which is luck rather than principle.
        `tests/fixtures/structure_added/merged.md` is the same shape with B's
        two segments in source order, and it is a correct merge that this
        predicate called a staple until this condition was added. So did
        `tests/fixtures/attribution_invented/merged.md`, a, a, b.

        Sized by the corpus and not by the arms: those two reference merges are
        the only false positives over all 19 control documents. The recorded arm
        units were not consulted in choosing it and are the check on it — of
        the 39 units the predicate fired on, this condition removes 4, and all
        4 are a single segment from one source against a block from the other:
        three `abb` at 3 attributed segments and one `a×12 b` at 13. It removes
        nothing at two or more each, which is the claim, and the largest
        excluded case being 13 segments rather than 3 is why the condition is
        the shape of the sequence and not a floor on its length.
        """
        counts = {letter: self.sequence.count(letter) for letter in set(self.sequence)}
        return bool(counts) and min(counts.values()) >= 2

    @property
    def stapled(self) -> bool:
        """Each source in one unbroken block, in its own original order."""
        distinct = len(set(self.sequence))
        return (
            distinct > 1
            and self.runs == distinct
            and self.monotone
            and self.conclusive
            and self.blocked
        )


def _break_pair(item: Segment, at: int) -> tuple[str, str]:
    """The two words a recorded line break sits between.

    `flatten_with_breaks` leaves a space at every recorded index, so the break
    at `at` is the space in `item.text[at]` and the words either side of it are
    what a reader would see on the two lines.
    """
    return item.text[:at].rsplit(" ", 1)[-1], item.text[at + 1:].split(" ", 1)[0]


@dataclass(frozen=True)
class Reconciliation:
    """Everything this module can say about one merge, with its denominators."""

    coverages: tuple[Coverage, ...]
    missing: tuple[Missing, ...]
    tokens: int
    duplicates: tuple[Duplicate, ...]
    order: Order
    merged: tuple[Segment, ...]
    # The merged document as it arrived. Kept whole rather than rebuilt from
    # `merged`, because a replacement pointer is checked against what the model
    # wrote and not against what the segmenter made of it.
    merged_text: str = ""

    @property
    def added_breaks(self) -> tuple[tuple[str, str], ...]:
        """Line breaks inside merged segments that no source segment carries.

        Reported, not judged. `high.merge.md` licenses restructuring, and an
        interior line break is recorded notation rather than a segment
        boundary so that the partition does not move, which together mean a
        merge can add structure no source has and nothing in the tool says so.
        This is the saying-so, and deliberately not a finding: adding a break is
        permitted at every level, so there is no rule for a check to enforce.

        A break is identified by the two words it sits between rather than by
        its offset, because an offset is only comparable within one wording and
        the whole point is to compare a merged segment against source segments
        it is not byte-identical to. A merged break whose word pair occurs as a
        break in any source is carried; anything else the merge introduced.
        """
        carried = {
            _break_pair(item, at)
            for coverage in self.coverages
            for item in coverage.document.segments
            for at in item.breaks
        }
        return tuple(
            pair for item in self.merged for at in item.breaks
            if (pair := _break_pair(item, at)) not in carried
        )

    @property
    def total(self) -> int:
        return sum(item.total for item in self.coverages)

    @property
    def absent(self) -> int:
        return sum(item.absent for item in self.coverages)

    @property
    def reworded(self) -> int:
        return sum(item.reworded for item in self.coverages)

    @property
    def present(self) -> int:
        return sum(item.present for item in self.coverages)


def locate(document: Document, merged_flat: str, merged: tuple[Segment, ...]) -> Coverage:
    """Find each of one source's segments in the merge.

    A label -- a title or a heading -- is searched for among the merge's own
    labels rather than in the whole flattened merge. Everything else is
    searched for as before. See `LABEL_KINDS` for why the two are not the same
    question.
    """
    flattened = [(item.id, flatten(item.text), item.kind) for item in merged]
    labels = [text for _, text, kind in flattened if kind in LABEL_KINDS]
    located: list[Located] = []
    for source in document.segments:
        needle = flatten(source.text)
        found = (
            any(occurs(needle, label) for label in labels)
            if source.kind in LABEL_KINDS
            else occurs(needle, merged_flat)
        )
        if found:
            located.append(Located(source, PRESENT))
            continue
        best_id, best, best_text = "", 0.0, ""
        for identifier, candidate, _ in flattened:
            ratio = similarity(needle, candidate)
            if ratio > best:
                best_id, best, best_text = identifier, ratio, candidate
        verdict = REWORDED if best >= NEAR_MATCH else ABSENT
        located.append(Located(source, verdict, best, best_id, best_text))
    return Coverage(document, tuple(located))


def verbatim(documents: list[Document], merged_flat: str,
             merged_raw: str = "") -> tuple[tuple[Missing, ...], int]:
    """Every invariant-core token in every source, checked against the merge.

    It consults nothing but the two texts — no dispositions, no coverage
    result, no fidelity level. The invariant core sits outside the slider, so
    a token that moved is a finding at every level and needs no context to be
    read as one.

    A whole fenced block is one token here: the block is invariant as a whole, and
    checking its lines separately would let a merge reorder them and pass.
    """
    absent: list[Missing] = []
    total = 0
    for document in documents:
        for source in document.segments:
            spans: list[Span | Segment] = list(source.spans)
            if source.kind == CODE_BLOCK:
                spans = [source]
            merged_code = code_exact(merged_raw)
            for span in spans:
                kind = CODE_BLOCK if isinstance(span, Segment) else span.kind
                text = flatten(span.text)
                total += 1
                # A fenced block is invariant byte for byte, so it
                # is compared with its interior whitespace intact. Everything
                # else keeps the collapse, because in prose a run of spaces is
                # not content and a line wrap is not a change.
                if kind == CODE_BLOCK and merged_raw:
                    gone = code_exact(span.text) not in merged_code
                else:
                    gone = not token_present(text, merged_flat)
                if gone:
                    absent.append(
                        Missing(
                            document.filename or document.id,
                            source.id,
                            kind,
                            span.text,
                            getattr(span, "unit", ""),
                        )
                    )
    return tuple(absent), total


def duplication(merged: tuple[Segment, ...]) -> tuple[Duplicate, ...]:
    """Content the merge states twice.

    Exact repeats are counted first, then near-repeats among what is left, at
    the same threshold the coverage pass uses.

    **The near pass is measurement-only and stays that way; the question of
    promoting it is closed, and closed negatively.** It was first left
    unpromoted "until a threshold is chosen against controls, or until a corpus
    with deliberate paraphrased duplication exists to choose one on". Both now
    exist: the corpus is five real merges (`toby-test-2` low and mid,
    `toby-test-4` low, `toby-test-5` low and off) that state both sources'
    facts twice, and the answer is that no `NEAR_MATCH` works, because the
    distributions are inverted rather than merely overlapping. The highest
    intra-document body-segment similarity among the 23 documents the corpus
    asserts are correct is 0.970 (`tests/pairs/index_429/ideal.md`); the
    highest among the five real duplicated merges is 0.943 and the lowest is
    0.664. Control max exceeds positive max, so raising or lowering the
    constant cannot separate them either way. The pass is kept only because
    `measure_merges.py`, `analyse_merges.py` and
    `test_a_near_repeat_is_measured_and_deliberately_not_a_finding` read its
    output as a measurement; nothing downstream of it decides a finding or an
    exit code, and it must not be made to.

    Headings are excluded. Two sections legitimately named `Networking` is
    structure, not a fact stated twice, and counting them would put a duplicate
    on every well-formed merge in the corpus.
    """
    bodies = [
        (item.id, flatten(item.text))
        for item in merged
        if item.kind not in (TITLE,) and item.level == 0
    ]
    counts: dict[str, int] = {}
    for _, text in bodies:
        counts[text.casefold()] = counts.get(text.casefold(), 0) + 1
    found = [
        Duplicate(text, count, True)
        for text, count in sorted(counts.items())
        if count > 1
    ]

    singles = [text for _, text in bodies if counts[text.casefold()] == 1]
    paired: set[int] = set()
    for first in range(len(singles)):
        if first in paired:
            continue
        for second in range(first + 1, len(singles)):
            if second in paired:
                continue
            if similarity(singles[first], singles[second]) >= NEAR_MATCH:
                paired.update({first, second})
                found.append(Duplicate(singles[first], 2, False))
                break
    return tuple(found)


def restatements(claims: Sequence["Claim"]) -> tuple[Restatement, ...]:
    """The same claim, extracted from two different lines of the merge.

    Check 9's second half, and the one that catches the failure `duplication`
    above cannot see: a merge that keeps both sources' wordings of the same
    fact, so the document states everything twice. The two wordings are
    different strings, so no exact segment repeat exists and no near-repeat
    threshold separates them from a correct merge: the measured control
    maximum (0.970) sits *above* the worst real positive (0.943), an
    inversion no constant can fix. Asked one level up, at the claim, the same
    corpus separates cleanly, because the decomposer resolves both wordings to
    one sentence.

    **The predicate, and every clause of it is load-bearing.**

    * **Byte-identical claim text.** Not a similarity. The relaxation was
      measured and closed off: the four real positives repeat at 1.000, the
      one miss at 0.500, and eight correct documents sit between them
      (`conflict_surfaced` 0.976, three at 0.850, down to 0.740). Any threshold
      that reaches the miss fires on eight controls first. Exact equality is the
      only clean cut, and it is where the measurement is, not where taste is.
    * **Two different lines.** A decomposer that emits one fact twice from one
      line is noisy; a document that states it on two lines said it twice. The
      corpus carries both cases, and this clause is what tells them apart:
      `toby-test-2 mid`'s five repeats are all confined to one line and are
      deliberately missed, while `disjoint_domains/source_b.md` yields two
      one-line repeats in 3 of 3 samples and must stay silent.
    * **Both copies anchored.** `Claim.anchored` false means the span was not
      found in the document and the line is the model's unchecked hint, which
      `decompose.Claim`'s own docstring calls worse than no line at all. A
      finding is an accusation and it may not rest on two unverified numbers.
      It costs nothing measured: across the five real positives, 0 of 228
      merge claims came back unanchored, so all 28 firing pairs are anchored.

    **What it must not fire on, measured rather than argued.** Taking nothing
    from source B is acceptable and is not this defect; a correct merge of two
    complementary documents that carries both in full is also acceptable, and
    the corpus contains two of those -- `library_holds/ideal.md` (18 body
    segments, 9 from each source, none of the merge's own) and
    `freezer_alarm/ideal.md` (21 = 12 + 9). Both are answer keys the corpus
    asserts are correct, both are near-total concatenations, and every
    segment-level measure puts them on the same side as the real defect. Both
    are silent here, 3 samples each, because complementary documents do not
    state the same fact twice.

    Returns one `Restatement` per repeated text, in text order, so a report can
    say how many distinct facts were stated twice rather than how many claims
    were involved in it.
    """
    lines: dict[str, set[int]] = {}
    for item in claims:
        if not item.anchored:
            continue
        lines.setdefault(item.text, set()).add(item.line)
    return tuple(
        Restatement(text, tuple(sorted(seen)))
        for text, seen in sorted(lines.items())
        if len(seen) > 1
    )


def restated_findings(claims: Sequence["Claim"]) -> tuple[Finding, ...]:
    """`restatements` as findings, one per fact the merge states twice.

    Emitted here beside check 9's own message rather than at the call site, so
    that the two halves of `DUPLICATED_CONTENT` are worded by one hand. The
    call site is `cli.one_pass`, not `findings` below, for a reason that is
    about order and not about ownership: the reconciler runs before the four
    model passes so that a mechanically wrong merge is known before the run
    spends anything, and the merged document's claims do not exist until the
    last of them. The prompt-example leak kind sets the precedent for a kind
    that no numbered check produces, and `CHECKS` stays 9 for the same reason
    it gives: the nine are comparisons of the merge against its sources, and
    this one compares the merge against itself.

    No segment and no document is named, as in the exact half: the fault is in
    the merge, which is not a source and carries no filename, and the repeated
    claim identifies it exactly.
    """
    return tuple(
        Finding(
            DUPLICATED_CONTENT,
            f"{found.text!r} is extracted from lines "
            f"{', '.join(str(line) for line in found.lines)} of the merged "
            f"document; the merge states the same fact more than once, in both "
            f"sources' wordings",
        )
        for found in restatements(claims)
    )


def order(coverages: tuple[Coverage, ...], merged: tuple[Segment, ...]) -> Order:
    """Did the merge interleave its sources, or set them end to end?

    Each merge segment is attributed to the source document whose segment it
    carries, by exact containment first and then by best similarity above the
    near threshold. Segments matching nothing are left out rather than guessed
    at — a merge is allowed its own connective prose, and forcing a document on
    to it would invent alternations that are not there.

    Segments *both* sources state are left out for the same reason in the other
    direction. Every fixture here shares a boilerplate line between its two
    sources, and attributing such a line to whichever document was checked first
    makes a genuine staple's second half alternate a, b, a, b against content it
    shares with the first. A segment two documents state identically is evidence
    about neither, so it is excluded and `attributed` records how many survived.
    """
    sources = [
        (coverage.document.id, item.ordinal, flatten(item.text))
        for coverage in coverages
        for item in coverage.document.segments
    ]

    attribution: list[tuple[str, int]] = []
    for item in merged:
        text = flatten(item.text)
        owners: dict[str, int] = {}
        best = 0.0
        for document_id, ordinal, source in sources:
            if comparable(source, text) and (occurs(source, text) or occurs(text, source)):
                if best < 1.0:
                    owners, best = {}, 1.0
                owners.setdefault(document_id, ordinal)
            elif best < 1.0:
                ratio = similarity(source, text)
                if ratio >= NEAR_MATCH and ratio >= best:
                    if ratio > best:
                        owners = {}
                    owners.setdefault(document_id, ordinal)
                    best = ratio
        if len(owners) == 1:
            attribution.append(next(iter(owners.items())))

    owners_resolved = [document_id for document_id, _ in attribution]
    runs = sum(
        1
        for index, owner in enumerate(owners_resolved)
        if index == 0 or owners_resolved[index - 1] != owner
    )
    distinct = len(set(owners_resolved))

    # Did each source keep its own order? Dropping segments preserves this, so
    # a *partial* concatenation stays monotone, which is the case this check
    # exists for, while a merge that reorders one source's material does not.
    seen: dict[str, int] = {}
    monotone = True
    for document_id, ordinal in attribution:
        if ordinal < seen.get(document_id, -1):
            monotone = False
        seen[document_id] = ordinal

    headings = [
        item
        for coverage in coverages
        for item in coverage.located
        if item.segment.kind in (HEADING, TITLE)
    ]
    return Order(
        sequence=tuple(owners_resolved),
        runs=runs,
        interleaved=runs > distinct,
        monotone=monotone,
        attributed=len(attribution),
        headings_total=len(headings),
        headings_present=sum(1 for item in headings if item.verdict != ABSENT),
    )


def reconcile(documents: dict[str, str], merged: str) -> Reconciliation:
    """Every measurement in this module, over one merge and its sources.

    `documents` maps filename to text, in the order the merge was given them,
    which is what fixes the document letters. The merge is segmented by the
    same function as the sources: two segmentations would put the numerator and
    the denominator on different footings, which is the kind of defect this
    module exists to expose.
    """
    sources = [
        segment_document(text, document_id(index), filename)
        for index, (filename, text) in enumerate(documents.items())
    ]
    merged_segments = segment_document(merged, MERGE_LETTER).segments
    merged_flat = flatten(merged)
    coverages = tuple(locate(source, merged_flat, merged_segments) for source in sources)
    absent, tokens = verbatim(sources, merged_flat, merged)
    return Reconciliation(
        coverages=coverages,
        missing=absent,
        tokens=tokens,
        duplicates=duplication(merged_segments),
        order=order(coverages, merged_segments),
        merged=merged_segments,
        merged_text=merged,
    )


# --------------------------------------------------------------------------
# The mechanical reconciliation
# --------------------------------------------------------------------------
#
# Everything below reads the merge's own disposition records and holds them
# against the two texts. Nine checks, no model, no threshold that was not
# fixed in the design before it was used. The ninth reads a measurement made above
# rather than a disposition record, which is the one exception and is argued
# where it is made.

UNDECLARED_ABSENCE = "undeclared_absence"
UNDECLARED_REWORDING = "undeclared_rewording"
# Check 2's third kind, and the one that is not about loss. The segment is
# in the merge; what is wrong is the record saying it left. Deliberately
# carries no "absence" in the name for that reason.
FALSE_DEPARTURE = "false_departure"
INVENTED_SEGMENT = "invented_segment"
UNRESOLVED_REPLACEMENT = "unresolved_replacement"
DISPOSITION_NOT_PERMITTED = "disposition_not_permitted"
VERBATIM_VIOLATION = "verbatim_violation"
# The dispositions whose records must name where the content went. Copied from
# `prompts/merge.md`: "Required for reworded, superseded, subsumed and
# duplicate; empty for dropped." `reconciled` is absent from the prompt's list
# and so is absent here.
NAMES_A_REPLACEMENT = ("reworded", "superseded", "subsumed", "duplicate")

DECLARED_LOSS_OVER_BUDGET = "declared_loss_over_budget"
# How many segments one replacement may absorb before the supersession stops
# being a replacement and becomes a deletion. Measured over `tests/pairs`: the
# highest legitimate fan-in in nine operator-authored ideal merges is 3, across
# 96 supersessions, and the 50-supersession pair never exceeds 2. Check 6a.
SUPERSESSION_FAN_IN = 3
TITLE_NOT_FROM_SOURCE = "title_not_from_source"
TITLE_NOT_SUPERSEDED = "title_not_superseded"
DUPLICATED_CONTENT = "duplicated_content"
# Named here with the other kinds and produced by none of the checks below.
# `merge.example_content_leaks` is what finds it, because the words it looks for are
# `merge.md`'s and this module has never read a prompt. The kind lives in this
# list anyway: `report.STRUCTURAL_HEADINGS` and the two renderers iterate
# `FINDING_KINDS` to decide what to print, so a kind kept outside it would
# either need a second vocabulary or go unrendered. What it must not join is
# `CHECKS` below -- see the comment there.
PROMPT_EXAMPLE_LEAK = "prompt_example_leak"

FINDING_KINDS = (
    UNDECLARED_ABSENCE,
    UNDECLARED_REWORDING,
    FALSE_DEPARTURE,
    INVENTED_SEGMENT,
    UNRESOLVED_REPLACEMENT,
    DISPOSITION_NOT_PERMITTED,
    VERBATIM_VIOLATION,
    DECLARED_LOSS_OVER_BUDGET,
    TITLE_NOT_FROM_SOURCE,
    TITLE_NOT_SUPERSEDED,
    DUPLICATED_CONTENT,
    PROMPT_EXAMPLE_LEAK,
)

# Which of the two questions a kind answers. It was split out because
# the exit code conflated "the merged document is wrong" with "the merge's
# account of itself is wrong", and on the operator's `universe` pair those two
# pointed in opposite directions -- every finding at every level was
# `FALSE_DEPARTURE`, a record kind, so the 26%-correct document exited 0 and the
# three 100%-correct ones exited 1.
#
# DOCUMENT means a reader holding the merged document has a problem in their
# hands: content is missing, invented, altered, stated twice, or gone in bulk.
# RECORD means the document may be perfectly good and the merge mis-described
# what it did. Both are faults and both are reported; they differ in what the
# reader does next, which is why they differ in the exit code.
#
# The three judgement calls, argued rather than left to the name:
#
# `DECLARED_LOSS_OVER_BUDGET` is DOCUMENT even though it is computed entirely
# from records. The records are honest and the arithmetic over them is right --
# what is wrong is that the content really is gone, at a volume past the
# declared-loss budget. The reader's problem is the document.
#
# `UNRESOLVED_REPLACEMENT` is RECORD, and it is the closest call here. A
# replacement that resolves to nothing is either a bad pointer or genuinely
# missing content, and this check cannot tell which. It is filed as RECORD
# because check 2 catches the second case on its own terms and would raise
# `UNDECLARED_ABSENCE` for it; what is left over here is the pointer.
#
# `PROMPT_EXAMPLE_LEAK` is DOCUMENT because `merge.example_content_leaks` reads
# the merged document as well as the reason fields, and the document half is
# invented content by another name. Filed under the worse of its two readings
# on purpose: a kind that can mean either should move the exit code as if it
# means the one that hurts.
DOCUMENT_FINDINGS = frozenset({
    UNDECLARED_ABSENCE,
    UNDECLARED_REWORDING,
    INVENTED_SEGMENT,
    VERBATIM_VIOLATION,
    DECLARED_LOSS_OVER_BUDGET,
    TITLE_NOT_FROM_SOURCE,
    DUPLICATED_CONTENT,
    PROMPT_EXAMPLE_LEAK,
})

RECORD_FINDINGS = frozenset({
    FALSE_DEPARTURE,
    UNRESOLVED_REPLACEMENT,
    DISPOSITION_NOT_PERMITTED,
    TITLE_NOT_SUPERSEDED,
})

# A partition, asserted at import rather than in a test. A kind added to
# `FINDING_KINDS` and to neither family would silently stop moving the exit
# code, which is the one failure mode this split introduces; a kind in both
# would make the exit code depend on which set was consulted first.
assert DOCUMENT_FINDINGS.isdisjoint(RECORD_FINDINGS), "a kind is in both families"
assert DOCUMENT_FINDINGS | RECORD_FINDINGS == set(FINDING_KINDS), (
    "every finding kind must be filed as document or record: "
    f"{set(FINDING_KINDS) ^ (DOCUMENT_FINDINGS | RECORD_FINDINGS)}")

# The numbered checks in `findings()`, which is not `len(FINDING_KINDS)`, though
# it once was. Check 2 now produces two kinds, so the two counts came apart:
# eleven names, nine checks. The eleventh name, `PROMPT_EXAMPLE_LEAK`, widens
# that gap for a second and different reason and this number does not move for
# it. Two reasons, and the first is the weaker one: every check below holds the
# merge against its *sources*, and a prompt leak is the merge held against the
# *prompt*, so counting it here would put a third referent under a denominator
# whose whole job is to say how many times two texts were compared. The second
# is the one that decides it. The graded run records (withheld with the paper) show `checks: 9` and
# the paper's own prose says "nine" too; those records describe a
# tool that made nine checks and that is a true fact about the day they were
# written. Moving this constant would silently restate every one of them as a
# reading taken on a ten-check instrument. A new check that has to rewrite the
# history of the old ones is not free, and this one is not worth it.
# Everything that says "N mechanical checks" to a reader
# -- the report's Structure preamble, the HTML summary, `structural.checks` in
# the JSON record -- means the checks that ran, and reading it off the kinds
# would inflate the denominator because one finding was given two names. That is
# the arithmetic refused in the other direction, where a check that cannot fire
# at a level leaves the count rather than passing; refusing it one way and
# not the other would be worse than doing neither. `tests/test_reconcile.py`
# counts the `# N.` comments in this module and holds them against this number,
# so a tenth check cannot be added without moving it.
CHECKS = 9

# The permitted dispositions by level. This is the same
# table the `prompts/fidelity/*.merge.md` fragments state in prose to the
# model, and a rule written twice is not a rule checked twice, so
# `tests/test_reconcile.py` reads the fragments and asserts they agree with
# this, rather than trusting that they were written from it.
#
# `dropped` is in none of the rows, and that is not the same as being an
# error at every level. The disposition model and the loss budget govern: a
# declared drop goes to the review queue with its reason, and becomes a
# finding only when the aggregate crosses the budget below. Putting it in this
# matrix as well would make every declared drop two findings at once and
# collapse exactly the split that makes declaring worth doing. The asserts
# after the table hold `dropped` out of every row, so it cannot creep back in.
# The dispositions that claim the segment is no longer carried as itself, for
# check 2's converse direction. `duplicate` is absent on purpose: it says
# another segment already carries this content, so finding that content in
# the merge is what it predicts rather than a contradiction of it. `reworded`
# and `dropped` are absent because the predicate is deliberately ruled at these
# two; both are reachable the same way and neither is claimed to be covered.
DEPARTED = ("subsumed", "superseded")

# `mid` gained `subsumed` later, and it is not a widening of what
# mid may write so much as the declaration for something the author's ladder
# always put here: an obvious detail merge, a closing clause carried into the
# sentence it belongs to. Combining two statements into one sentence absorbs
# one of them by construction, and `subsumed` is the only record that says so,
# so permitting the merge without permitting the record would have made the
# honest answer illegal and left the model choosing between an undeclared
# absence and a disposition it was told was a defect.
#
# It does not blur mid into high. Both statements a mid merge combines are
# already stated; high's `reconciled` is for a statement neither document makes
# on its own. The two dispositions are what keeps that line legible.
#
# `reconciled` is `high`'s alone, and the row is what keeps the two combining
# licences apart. A `mid` merge combines two statements that are both already
# stated, so the absorbed one is `subsumed`; a `high` merge may write a
# statement neither document makes on its own, and the segments that fed it are
# `reconciled`. Permitting `reconciled` at `mid` would erase the distinction
# the level split exists to draw, and the reverse pass reads the disposition to
# decide which entailment it must check -- a `subsumed` replacement is entailed
# by its own segment, a `reconciled` one only by the conjunction.
class _Permitted(dict):
    """The rows below, readable by either spelling of the strictest level.

    `off` was once published as `verbatim` and kept as an alias, so this
    table has to answer to both. A second row would have been the wrong shape:
    it would make `len(PERMITTED)` five and `tuple(PERMITTED)` disagree with
    `config.FIDELITY_LEVELS`, and every caller that iterates the levels --
    `sweep`, `merge.MAY_CHOOSE`'s assertion, the four-row budget proof --
    would silently gain a duplicate level.

    So the aliasing is on lookup only. Iteration, `len` and `.values()` still
    see exactly the four wire names; `PERMITTED["verbatim"]` and
    `"verbatim" in PERMITTED` resolve through `config.canonical_fidelity`. An
    unknown level still raises `KeyError` and still answers `False`, because
    `canonical_fidelity` returns what it does not recognise unchanged.
    """

    def __missing__(self, key):
        canonical = config.canonical_fidelity(key)
        if canonical == key:
            raise KeyError(key)
        return self[canonical]

    def __contains__(self, key) -> bool:
        return super().__contains__(config.canonical_fidelity(key))


PERMITTED = _Permitted({
    "off": ("superseded", "duplicate"),
    "low": ("reworded", "superseded", "duplicate"),
    "mid": ("reworded", "superseded", "subsumed", "duplicate"),
    "high": ("reworded", "superseded", "subsumed", "duplicate", "reconciled"),
    # `open` permits everything `high` does and widens what `reconciled` may
    # carry, rather than adding a disposition of its own. A disposition
    # names what happened to a *source segment*, and the two things `open`
    # adds -- a value covering both candidates, and a statement from outside
    # the documents -- are a wider licence for an existing record and a new
    # kind of record respectively. Neither is a sixth verb for a segment.
    "open": ("reworded", "superseded", "subsumed", "duplicate", "reconciled"),
    # `sourced` takes `open`'s row unchanged, and for the reason `open` took
    # `high`'s: a disposition names what happened to a *source segment*, and
    # what this level adds -- that a declared statement was retrieved rather
    # than recalled -- is a fact about an `additions` record. There is no sixth
    # verb for a segment in it.
    "sourced": ("reworded", "superseded", "subsumed", "duplicate", "reconciled"),
})

# Which levels may carry a value covering two disagreeing source figures,
# rather than choosing one of them. Separate from `PERMITTED` because it
# is not a disposition: `reconciled` is permitted at `high` too, and what
# `open` widens is what a reconciled record's replacement may *hold*.
#
# Written as a table with an assert rather than as `fidelity == "open"`, for
# the reason `parsing.DERIVES` is: an equality test is how a sixth level would
# join the ladder without anyone deciding whether it covers.
def covers_the_sources(replacement: str, source_texts: dict[str, str]) -> bool:
    """Is every number in this replacement a number some source states?

    The one exemption `open` adds to check 5, and it is deliberately the
    narrowest thing that lets a covering value through. Two documents
    giving a figure as 30-45% and 35-50% disagree about its edges, and
    carrying either alone tells a reader the other document was wrong.
    30-50% tells them what both support -- and destroys two source tokens
    doing it, which is what this check would otherwise refuse.

    **No arithmetic, and that is the point.** Nothing in this package
    parses a numeric value, and this does not start: it asks whether each
    number in the replacement occurs *as a token* in some source, which is
    `token_present` over `find_spans`. A merge widening 30-45% to 30-60%
    is refused here, not because 60 is too large -- this cannot know that
    -- but because no document wrote it.

    A replacement with no numbers in it is not covered by this at all. The
    exemption is for a value assembled from source figures; a sentence
    that merely happens to be declared `reconciled` gets nothing from it.
    """
    numbers = [span.text for span in segment_module.find_spans(replacement)
               if span.kind == segment_module.NUMERIC]
    if not numbers:
        return False
    return all(any(token_present(number, text) for text in source_texts.values())
               for number in numbers)


COVERS = {"off": False, "low": False, "mid": False, "high": False, "open": True,
          "sourced": True}

assert set(COVERS) == set(config.FIDELITY_LEVELS)
# Covering implies choosing: a level that may carry a value spanning both
# candidates may certainly carry one of them. Asserted so the two tables
# cannot drift into a level that covers without being allowed to choose.
assert all(not covers or PERMITTED[level]
           for level, covers in COVERS.items())

assert tuple(PERMITTED) == config.FIDELITY_LEVELS
assert PERMITTED["verbatim"] is PERMITTED["off"] and "verbatim" in PERMITTED
assert "nonsense" not in PERMITTED
assert all(set(row) <= set(parsing.DISPOSITIONS) for row in PERMITTED.values())
assert not any("dropped" in row for row in PERMITTED.values())

# The declared-loss budget, strictly greater and 3% by default (it was 5%): at
# 100 segments three declared drops pass and four fail. An aggregate guard, and
# it fires however well each individual drop was argued -- death by a thousand
# individually-reasonable omissions is the failure mode it exists for. It counts
# `dropped` only; `subsumed` is compression, which is the intended behaviour at
# `high`, and a ceiling on it would fail every correct high-fidelity merge.
#
# The figure lives in `config.DEFAULT_DECLARED_LOSS_BUDGET`, because it is a
# knob and config owns the knobs. It is deliberately *not* re-exported
# here: a module-level `DECLARED_LOSS_BUDGET` sitting next to `over_budget`
# reads like the value that governs, when after this change nothing is governed
# by anything but the argument. Importers were made to say which they meant.


def over_budget(drops: int, segments: int, budget: float) -> bool:
    """The declared-loss budget as one predicate, because it has a second caller.

    The report has to answer the same question this module does -- a review
    queue with no ceiling is a way of declaring your way to exit 0 -- and the
    rule has three parts a second implementation would get subtly wrong:
    strictly greater, the denominator is source segments rather than claims,
    and a zero denominator never fires rather than dividing.

    A RULE WRITTEN TWICE IS NOT CHECKED TWICE. So it is written once and
    imported, and the callers cannot drift.

    `budget` is required and has no default. A default here would be the
    module constant back again, one layer down and harder to see: every caller
    would read as though it had chosen a ceiling when it had only failed to
    name one, and a record written beside it could not be trusted to say which
    ceiling decided the outcome. The three semantics above are unchanged by it
    -- at any budget the comparison is still strict, still over source
    segments, and still declines to divide by zero.
    """
    return bool(segments) and drops / segments > budget


@dataclass(frozen=True)
class Finding:
    """One thing wrong with a merge, found without asking anything."""

    kind: str
    detail: str
    segment: str = ""
    document: str = ""
    # **The two sides, on the row.** The operator's report: *"That is
    # something I think could be made clearer in general in the report so the
    # user does not need to refer to sections or the documents but gets the
    # full understanding of the claims directly in one row. Issue, source,
    # merge, why it is how it is."*
    #
    # `detail` is the *why* and was the whole of what a row carried, so a
    # reader met "this is reworded" and had to go and find both texts to see
    # how. Both are already in hand at every site that raises a finding of a
    # kind where both exist, so carrying them is a field rather than a
    # computation.
    #
    # Empty on the kinds where there is no second side: a segment that is
    # simply absent has no merge text, and inventing one would be worse than
    # leaving the field out.
    source_text: str = ""
    merge_text: str = ""

    @property
    def difference(self) -> str:
        """The two sides as a word diff, or `` where that would not help.

        Computed rather than stored, so a finding read back out of a report
        and one built here render alike, and so the rule lives in one place
        for all three surfaces.
        """
        return difference(self.source_text, self.merge_text)

    def as_dict(self) -> dict:
        """For the JSON report. Every field, since none of them is derivable."""
        return {
            "kind": self.kind,
            "detail": self.detail,
            "segment": self.segment,
            "document": self.document,
            # Published rather than left for a consumer to recompute. The
            # report is the record, and a consumer that diffed the two texts
            # itself would be a second implementation of the rendering rule --
            # which is how the page and the report came to print `citation`
            # and *cited* for one column.
            "source_text": self.source_text,
            "merge_text": self.merge_text,
            "difference": self.difference,
        }


@dataclass(frozen=True)
class Reconciled:
    """The findings, and the declared drops that are not findings.

    Both, because a reconciler that returned only the findings would be the
    place declared losses go to be forgotten. The design keeps them apart: findings
    drive the exit code, resolved declared drops are informational, and
    keeping them apart requires carrying both.
    """

    findings: tuple[Finding, ...]
    declared_drops: tuple[dict, ...]
    segments: int
    # Line breaks the merge introduced that no source segment carries.
    # Third thing the reconciler returns and the first that is neither a
    # finding nor a declaration: it is a measurement of the merged document,
    # reported so a reader can see structure the merge added, and carrying no
    # verdict because every level permits adding it. `CHECKS` stays 9 and
    # `FINDING_KINDS` stays 12 for exactly that reason.
    added_breaks: tuple[tuple[str, str], ...] = ()

    @property
    def loss(self) -> float:
        """Declared drops as a fraction of the source segments. The denominator is real."""
        return len(self.declared_drops) / self.segments if self.segments else 0.0


def titles_of(segments: tuple[Segment, ...]) -> tuple[Segment, ...]:
    """The title segments, in order. A document has none or one; a merge, likewise."""
    return tuple(item for item in segments if item.kind == TITLE and item.text.strip())


def _title_checks(
    result: Reconciliation,
    declared: dict[str, dict],
    title_policy: str,
    base: str,
) -> list[Finding]:
    """The two title checks: where the merged title came from, and what happened to the rest.

    A title is the clearest case of content that lives in the shape of a
    document rather than in its claims, and it is what the original defect
    dropped. Nothing downstream can catch it -- `decompose.md` is told to skip
    headings, so no claim is ever extracted from a title, so neither verify pass
    can fail a dropped one at any level. These two checks are the only thing
    that does.

    Byte-identical means byte-identical: the merged title is copied from a
    source title, never written, never combined, never adjusted for clarity, at
    `high` too. So this is the one comparison in the module that does not go
    through `flatten`.
    """
    candidates = [
        (coverage.document, item)
        for coverage in result.coverages
        for item in titles_of(coverage.document.segments)
    ]
    found = titles_of(result.merged)
    if not candidates:
        # These two checks are the only thing that can see a title at all, so
        # returning early here made them blind in the one case where invention
        # is unconstrained: no source title to copy, and no claim drawn from the
        # one the merge wrote. Absence of a title
        # remains no finding -- nothing was kept from nothing.
        if not found:
            return []
        # ...but "no source has a title" is this module's reading, not the
        # documents'. A plain-text source whose first line runs straight into
        # the body has no *title segment* -- the heuristic wants a line standing
        # alone -- while the merge, which puts a blank line after it, does. The
        # line is then carried unchanged and reported as invented, which is a
        # finding about the tool's own definition rather than about the merge
        # itself. What survives is the guard on invention: fire only when the text
        # occurs in no source at all, which is invention by any reading.
        carried = any(
            flatten(found[0].text) in flatten(coverage.document.text)
            for coverage in result.coverages
        )
        if carried:
            # `keep-base` has no referent here, and that is a fact about the
            # input rather than a defect in the merge. Said in the
            # measurement the reader already has, not as a finding.
            return []
        if title_policy == "synthesise":
            # For the reason the `synthesise` branch below emits nothing: this
            # is the one policy that permits a written title, and a written
            # title is graded as a claim by `merge.verify_title`, never as a
            # string here.
            #
            # This early return predates that policy and did not know
            # about it, so it fired the copied-title rule on precisely the
            # output `synthesise` exists to produce. `TITLE_NOT_FROM_SOURCE` is
            # a document finding, so a *correct* synthesised title over sources
            # that happen to carry no heading exited 1 -- and untitled sources
            # are the common case for pasted text, which is what the web
            # interface receives.
            #
            # Nothing goes unchecked by returning here. `verify_title` guards
            # only on `merged_title in candidates`, and `candidates` is empty in
            # this branch, so the call is made and the title is graded against
            # both documents -- by the stronger of the two tests, since string
            # containment cannot see a claim at all.
            return []
        return [Finding(
            TITLE_NOT_FROM_SOURCE,
            f"the merged title {found[0].text!r} occurs in no source document: "
            "no source has a title segment and this text is in none of them",
        )]

    if not found:
        return [Finding(
            TITLE_NOT_FROM_SOURCE,
            f"the merge has no title; {len(candidates)} source title(s) were available, "
            f"the first being {candidates[0][1].text!r}",
        )]
    merged_title = found[0].text

    findings: list[Finding] = []
    if title_policy == "keep-base":
        # The base's title, always, with the policy's one carve-out, which covers
        # the only case where `keep-base` is plainly wrong without reopening the
        # merit question the policy exists to close.
        owned = [item for document, item in candidates if document.filename == base]
        expected = owned[0] if owned else candidates[0][1]
        if merged_title != expected.text:
            findings.append(Finding(
                TITLE_NOT_FROM_SOURCE,
                f"under keep-base the merged title must be {expected.text!r} "
                f"({'the base document' if owned else 'the base has none, so the first'}"
                f"'s title); it is {merged_title!r}",
                segment=expected.id,
            ))
    elif title_policy == "synthesise":
        # The one policy that permits a written title, and the only one where
        # byte-identity is not the test. A written title is a claim, and
        # this module grades no claims -- it is set differences, string
        # containment and division, with no reader. So a written title is
        # checked where claims are checked, against the sources, by
        # `merge.verify_title`. Taking a source title unchanged stays correct
        # and is not a finding here or there.
        #
        # Nothing is emitted in this branch on purpose. A deterministic
        # stand-in was tried and falsified: "every substantive word of the
        # title appears in the sources" accepts "A motorbike is more stable
        # than a quad" over sources saying the quad is the stable one. A check
        # that passes the dangerous case is worse than none, because its output
        # reads as verification.
        pass
    elif merged_title not in {item.text for _, item in candidates}:
        findings.append(Finding(
            TITLE_NOT_FROM_SOURCE,
            f"the merged title {merged_title!r} is not byte-identical to any source "
            f"title: {sorted({item.text for _, item in candidates})}",
        ))

    # Every title not taken is superseded and says so. A title is never dropped
    # in silence -- the failure that was observed was the silence, not the
    # choice, so a title that simply vanished is a finding even when the title
    # that replaced it was the right one.
    merged_flat = flatten(merged_title)
    for document, item in candidates:
        if item.text == merged_title:
            continue
        record = declared.get(item.id)
        why = ""
        if record is None:
            why = "no record"
        elif record.get("disposition") != "superseded":
            why = f"a {record.get('disposition')!r} record"
        elif not any(occurs(merged_flat, part) for part in
                     parsing.anchor_parts(flatten(str(record.get("replacement", ""))))):
            # The title policy is specific about the pointer, not only the verb: the record
            # names the chosen title *as its replacement*. Check 3 only asks that
            # a replacement resolve somewhere in the merge, which a record
            # pointing at an unrelated paragraph satisfies.
            #
            # This one reads the replacement as the haystack, so the anchor is
            # taken apart rather than resolved: a title has to sit inside one of
            # the ends, and a title long enough to straddle an elision is a title
            # over `parsing.ANCHOR_HALF` characters, which is not a heading.
            why = f"a superseded record replacing it with {record.get('replacement')!r}"
        if why:
            findings.append(Finding(
                TITLE_NOT_SUPERSEDED,
                f"source title {item.text!r} is not the merged title and carries {why}"
                "; every title not taken needs a superseded record naming what replaced it",
                segment=item.id,
                document=document.filename or document.id,
            ))
    return findings


def findings(
    result: Reconciliation,
    dispositions: tuple[dict, ...],
    *,
    fidelity: str,
    title_policy: str,
    base: str,
    budget: float,
) -> Reconciled:
    """Hold a merge to what it declared.

    `result` is this module's own measurement of the two texts, `dispositions`
    is what the merge said it did, and the keyword arguments are the policy
    that was in force when it said it. `budget` is required for the same
    reason `fidelity` is: this function emits the finding that a ceiling
    decides, so a caller that did not name the ceiling has not said enough for
    the answer to be recorded. Every check is one of three
    things: a set difference, a string containment, or a division.

    The numbered comments below mark the checks, one to nine, in the
    order they run.
    """
    if fidelity not in PERMITTED:
        raise ValueError(f"unknown fidelity level {fidelity!r}; "
                         f"expected one of {config.FIDELITY_CHOICES}")
    # One spelling from here down. `PERMITTED` answers to both, but the `==
    # "off"` test in check 2 does not, and a level that arrived as `verbatim`
    # would take the wrong branch there while every other check took the right
    # one: the kind of split that reads as a check being flaky.
    fidelity = config.canonical_fidelity(fidelity)
    if title_policy not in config.TITLE_POLICIES:
        raise ValueError(
            f"unknown title policy {title_policy!r}; expected one of {config.TITLE_POLICIES}"
        )

    merged_flat = flatten(result.merged_text)
    segments = {
        item.id: (coverage, item)
        for coverage in result.coverages
        for item in coverage.document.segments
    }
    # First record wins. `parsing.check_merge` already rejects a duplicate
    # segment id, so a second one here means this was called on unchecked
    # output; silently taking the last would make which rule applied depend on
    # ordering, which is not a thing a reader could reconstruct.
    declared: dict[str, dict] = {}
    for record in dispositions:
        declared.setdefault(str(record.get("segment", "")).strip(), record)

    found: list[Finding] = []

    # 1. Every segment id in `dispositions` exists.
    for identifier, record in declared.items():
        if identifier not in segments:
            found.append(Finding(
                INVENTED_SEGMENT,
                f"disposition {record.get('disposition')!r} names segment {identifier!r}, "
                f"which is not in either source",
                segment=identifier,
            ))

    # 2. A record exists for a segment exactly when the merge did not keep it
    # character for character. `prompts/merge.md:125-128` states that as a
    # biconditional -- "emit one disposition record for each segment that is not
    # carried over character for character, and none at all for the segments
    # that are" -- and this check enforces both of its directions. Silence is
    # the claim of verbatim retention and a record is the claim of a departure;
    # each is checked against the same string comparison, in opposite
    # directions. It is one check and not a tenth, although the converse came
    # later than the forward direction: two directions of one
    # sentence are one rule, and this loop already had both operands in hand.
    #
    # Three kinds, not one, because the three are different accusations.
    #
    #   undeclared_absence   nothing said, and the merge does not carry it.
    #                        Material the merge lost.
    #   undeclared_rewording nothing said, and the merge carries it in altered
    #                        wording. Not loss, and counted apart from it: a
    #                        single total over both reads as loss whichever it
    #                        was made of, which is exactly how a headline
    #                        figure gets misread. Named for the
    #                        verdict rather than `undeclared_change`, because
    #                        `Located.verdict`'s own comment declines to call
    #                        `REWORDED` a change -- it is a reading of a
    #                        similarity score, and a kind named `change` would
    #                        assert more than the ratio supports.
    #   false_departure      a record claims the content departed, and the
    #                        merge carries the segment unchanged. Not loss
    #                        either, and not named for absence for the reason
    #                        it exists: the segment is *there*. What is wrong
    #                        is the merge's account of itself.
    #
    # The cross-source exclusion on the third kind is not a tolerance and has no
    # constant in it. `superseded` means another document's version was used
    # instead, so when an identical segment sits in another source the text in
    # the merge is that document's copy and this segment did depart -- string
    # equality on the flattened text, which is the same comparison `occurs`
    # makes. Without it the check fires on every merge of two documents that
    # share a title. Measured before it was written: it is the difference
    # between 123 firings and 79 on the recorded corpus, and the 44 it removes
    # are the negative control in `tests/test_reconcile.py`.
    carried: dict[str, set[str]] = {}
    for coverage in result.coverages:
        carried[coverage.document.id] = {
            flatten(item.text) for item in coverage.document.segments
        }

    for coverage in result.coverages:
        for located in coverage.located:
            record = declared.get(located.segment.id)
            if record is None:
                if located.found:
                    # The break survival check, and it runs at `off` alone.
                    # `flatten` collapses whitespace on both sides, so a merge
                    # that dropped a line break still matches and `found` is
                    # true, which left the tool restoring structure
                    # with no way to say whether the model kept it. At `off`
                    # nothing may be reworded, so a segment carried silently
                    # must carry its breaks too. No new kind: this is check
                    # 2's own converse, "carried, altered, undeclared", which
                    # is what UNDECLARED_REWORDING already names.
                    broken = segment_module.with_breaks(located.segment)
                    if (fidelity == "off" and located.segment.breaks
                            and broken not in result.merged_text):
                        found.append(Finding(
                            UNDECLARED_REWORDING,
                            f"{located.segment.id} spans {len(located.segment.breaks) + 1} "
                            f"lines in its source and the merge runs them "
                            f"together; at off a carried segment keeps its own "
                            f"line breaks and no record explains this",
                            segment=located.segment.id,
                            document=coverage.document.filename or coverage.document.id,
                        ))
                    continue
                found.append(Finding(
                    UNDECLARED_ABSENCE if located.verdict == ABSENT else UNDECLARED_REWORDING,
                    f"{located.segment.text!r} is {'not in' if located.verdict == ABSENT else 'reworded in'} "
                    f"the merge and no disposition record explains it (nearest merge "
                    f"segment {located.nearest or 'none'} at {located.ratio:.2f})",
                    segment=located.segment.id,
                    document=coverage.document.filename or coverage.document.id,
                    # Both sides on the row. The merge side is carried
                    # only where the verdict says there is one: a segment the
                    # merge does not have has no counterpart, and the nearest
                    # match at 0.3 is a coincidence rather than a version of it.
                    source_text=located.segment.text,
                    merge_text=("" if located.verdict == ABSENT
                                else located.nearest_text),
                ))
                continue
            disposition = str(record.get("disposition", ""))
            if not located.found or disposition not in DEPARTED:
                continue
            text = flatten(located.segment.text)
            if any(text in texts for name, texts in carried.items()
                   if name != coverage.document.id):
                continue
            found.append(Finding(
                FALSE_DEPARTURE,
                f"{located.segment.text!r} is declared {disposition!r} but the "
                f"merge carries it unchanged, and no other source has it to "
                f"have superseded it; the record describes a departure that "
                f"did not happen",
                segment=located.segment.id,
                document=coverage.document.filename or coverage.document.id,
                # Both sides, and here they are the *same* text -- which is
                # the finding. `difference` answers empty on two identical
                # strings, so the surfaces print the pair and the reader sees
                # at once that nothing moved.
                source_text=located.segment.text,
                merge_text=str(record.get("replacement", "")),
            ))

    # 3. Every replacement resolves to text actually in the merge. The prompt
    # says so in as many words, so a model that writes an unresolvable pointer
    # has been warned in its own instructions. `resolves` rather than `occurs`
    # because a replacement over the cap arrives as its two ends, and
    # both must be found, in order.
    # `NAMES_A_REPLACEMENT` is the prompt's own list: "Required for reworded,
    # superseded, subsumed and duplicate; empty for dropped." A record from that
    # list, on a segment the reconciler cannot find, that names nowhere for the
    # content to have gone, is a loss however it is labelled -- and the prompt
    # already promises exactly this treatment: "A declared departure whose
    # replacement cannot be found in the merged document is treated as an
    # undeclared drop, which is worse than declaring nothing." It was not.
    # A blank replacement produced no finding at all, and a missing one produced
    # `UNRESOLVED_REPLACEMENT`, a record fault at exit 3 -- a milder penalty than
    # the instruction threatens, on a document that really did lose content.
    # The operator's rule: "if it is genuinely-absent then it is lost."
    absent_ids = {
        located.segment.id
        for coverage in result.coverages
        for located in coverage.located
        if located.verdict == ABSENT
    }
    for identifier, record in declared.items():
        raw = record.get("replacement")
        replacement = str(raw) if raw is not None else ""
        if not replacement.strip():
            disposition = str(record.get("disposition", ""))
            if (disposition in NAMES_A_REPLACEMENT
                    and identifier in absent_ids):
                found.append(Finding(
                    UNDECLARED_ABSENCE,
                    f"{identifier} is not in the merge and its {disposition!r} "
                    f"record names no replacement, so nothing accounts for where "
                    f"the content went. A departure that points nowhere is a "
                    f"drop: the content is gone and the record does not say so",
                    segment=identifier,
                ))
            continue  # `dropped` names nothing, and the prompt says so
        if not resolves(flatten(replacement), merged_flat):
            found.append(Finding(
                UNRESOLVED_REPLACEMENT,
                f"segment {identifier} is declared {record.get('disposition')!r} with "
                f"replacement {replacement!r}, which is not in the merged document",
                segment=identifier,
                # The record's own side and no merge side, because the finding
                # is that there is no merge side: this replacement is in no
                # merged text. Naming the nearest thing to it would be the
                # invention the check exists to report.
                merge_text=replacement,
            ))

    # 4. Every disposition is permitted at the active level.
    for identifier, record in declared.items():
        value = str(record.get("disposition", ""))
        if value == "dropped" or value in PERMITTED[fidelity]:
            continue
        found.append(Finding(
            DISPOSITION_NOT_PERMITTED,
            f"segment {identifier} is declared {value!r}, which fidelity "
            f"{config.fidelity_name(fidelity)} "
            f"does not permit; permitted here: {', '.join(PERMITTED[fidelity])}",
            segment=identifier,
        ))

    # 5. The invariant core, which consults no level and exactly one
    # disposition. It sits outside the slider, so a token that moved is
    # a finding at `high` exactly as at `off`.
    #
    # Two exemptions, and they are one rule read twice: a token is excused when
    # the segment it was in did not lose its content, only its place. `dropped`
    # withdraws the content and the queue owns it; `superseded` keeps the
    # content in **another source segment's** wording, and the declared
    # replacement both being that wording and resolving in the merge is the
    # evidence that it did.
    #
    # The first exemption is `dropped`, and it became necessary when
    # wiring this module into the pipeline showed that a declared drop of any
    # segment carrying a number, unit, URL or fenced block was two findings at
    # once, and almost every segment worth dropping carries one. That would make
    # the findings/queue split unreachable and the loss budget never binding:
    # the queue would be empty of everything except prose. A dropped segment's
    # token did not *drift*; it was withdrawn along with the segment it was in,
    # and the review queue and the budget already own withdrawals.
    #
    # The second is `superseded`, and it narrows what this comment used to say.
    # It read that all four of `reworded`, `superseded`, `subsumed` and
    # `duplicate` assert the content survives, so their tokens must survive
    # with it. That holds for three of them, which keep this check. It does not
    # hold for `superseded` when two sources render one number differently:
    # `merge.md` requires a numeral copied character for character and one
    # fact in one sentence requires one wording to survive, and where the sources write "two
    # billion" against "2,000,000,000" both rules cannot hold at once. Keeping
    # either loses a numeral; keeping both states the fact twice. So the
    # verbatim rule yields exactly here, and only where the replacement is the
    # text of some *other source segment* and resolves in the merge -- a
    # `superseded` value whose replacement does not resolve is still a finding,
    # and check 3 reports the dangling pointer besides.
    #
    # The source-segment half is a narrow fix for B5 (`tests/test_reconcile.py`),
    # and without it the exemption was a hole rather than a carve-out. Until
    # then any span that merely `resolves` discharged the check, so a merge
    # could delete a segment outright, point `superseded` at a sentence of its
    # own prose, and the verbatim core would stand down -- at **all four**
    # levels, because no level is consulted here and `superseded` is permitted
    # everywhere. `prompts/merge.md:133` says what `superseded`
    # means: this segment was superseded *by another source's version*. So the
    # replacement has to be that version. It is a string containment against
    # the sources, not a threshold and not a similarity score, and it keeps the
    # rendering case above exempt, because there A's own wording is a source segment.
    #
    # Deliberately **not** one-to-one. The operator's answer keys use
    # `superseded` many-to-one within one document -- `rate_limits` nine times,
    # `bike_docks` folding three segments into one sentence -- so a uniqueness
    # condition would contradict the corpus's own ground truth. Any
    # number of segments may name the same other segment's wording.
    #
    # This is a **partial** repair and must not be read as closing B5. It
    # closes the hole for content carrying a verbatim-class token -- a number,
    # unit, URL, version, path or fenced block, which is most real
    # documentation -- and leaves prose-only loss invisible at every level,
    # because check 5 never looks at prose. The B5 test still passes.
    #
    # The rule for the review *queue* is untouched by this: it takes only
    # declared drops, which are omissions and never assertions, and a
    # rendering difference in a surviving fact is neither.
    #
    # The record is the whole test, and deliberately not "the segment is also
    # `ABSENT`". A drop that the merge actually reworded rather than removed
    # reads as `REWORDED` here whenever the nearest merge segment happens to
    # score above the threshold -- `Located.verdict` says so itself: reworded is
    # a reading of a similarity score and not an observation. Gating a finding
    # on it would put a heuristic in the one part of this module that is meant
    # to be checkable by hand. So the hole stays open and is closed elsewhere:
    # a `dropped` record over a segment the merge kept comes back **rejected**
    # from `verify.grade_declarations`, because its claims do not return
    # MISSING, and a changed value in a kept segment is a CONTRADICTED claim and
    # a finding on its own. Check 2 makes the same trade already -- any record
    # silences it -- so this is that trade applied consistently, not a new one.
    # Flattened once, outside the loop: `result.missing` runs to one entry per
    # absent token and `segments` to every segment of both sources, so doing it
    # inside would be quadratic on documents where this check matters most.
    source_texts = {
        identifier: flatten(item.text) for identifier, (_, item) in segments.items()
    }

    def superseded_by_a_source(identifier: str, replacement: str) -> bool:
        """Is this replacement the wording of a source segment other than this one?"""
        return any(resolves(replacement, text)
                   for other, text in source_texts.items() if other != identifier)

    def covered_by_the_sources(replacement: str) -> bool:
        """The lifted `covers_the_sources`, bound to this run's sources."""
        return covers_the_sources(replacement, source_texts)

    for missing in result.missing:
        record = declared.get(missing.segment)
        disposition = "" if record is None else str(record.get("disposition", ""))
        if disposition == "dropped":
            continue
        if disposition == "superseded":
            replacement = flatten(str(record.get("replacement", "")))
            if (resolves(replacement, merged_flat)
                    and superseded_by_a_source(missing.segment, replacement)):
                continue
        if (disposition == "reconciled" and COVERS[fidelity]
                and missing.kind == segment_module.NUMERIC):
            # Only at a level that permits covering, only on a numeric token,
            # and only where the replacement reached the merge and is built
            # from figures the documents wrote. Three conditions rather than
            # one because this is the only hole in the check that sits outside
            # the slider, and each is what stops it widening: the level, so no
            # lower level inherits it; the kind, so a moved URL or version
            # cannot be declared away as a reconciliation; and the containment,
            # so the declaration cannot license a number nobody stated.
            replacement = flatten(str(record.get("replacement", "")))
            if resolves(replacement, merged_flat) and covered_by_the_sources(replacement):
                continue
        found.append(Finding(
            VERBATIM_VIOLATION,
            f"{missing.kind} {missing.text!r}"
            + (f" ({missing.unit})" if missing.unit else "")
            + " does not survive into the merge unchanged",
            segment=missing.segment,
            document=missing.document,
        ))

    # 6. The declared-loss ceiling, measured two ways.
    #
    # 6a. Supersession fan-in. B5, and the operator's rule decides it: a
    # summary sentence is a valid replacement only if the detail survives
    # somewhere in the output. If it *replaces* the detail, information is
    # lost and the merge is wrong.
    #
    # So a replacement that absorbs many distinct segments has not replaced
    # them, it has deleted them -- which is how a merge declares its way to
    # exit 0: label every lost segment `superseded` by one
    # surviving sentence and every record is internally valid.
    #
    # The ceiling is measured, not guessed. Over the nine pairs in
    # `tests/pairs` -- 96 supersessions, operator-authored, not written for
    # this check -- one replacement never absorbs more than **3** segments,
    # and the largest pair (`rate_limits`, 50 supersessions) never exceeds 2.
    # Legitimate supersession is close to one-for-one because each dropped
    # segment is replaced by its own better version.
    #
    # Same finding kind as the budget below: this is the declared-loss ceiling
    # measured a second way, not a tenth check. `FINDING_KINDS` stays 12 and
    # `CHECKS` stays 9.
    # Keyed on the replacement, not on the disposition word. B5's fixture
    # expresses the same attack as `superseded` at `off`, `reworded` at `low`
    # and `mid`, and `subsumed` at `high`; a check that read the word would
    # close one level and leave three open. And on the *absent* records only:
    # a record whose segment is still in the merge has lost nothing, which is
    # `FALSE_DEPARTURE`'s subject rather than this one.
    gone = {
        located.segment.id
        for coverage in result.coverages
        for located in coverage.located
        if located.verdict == ABSENT
    }
    absorbed: dict[str, list[str]] = {}
    for segment_id, record in declared.items():
        if segment_id not in gone:
            continue
        # `.get(key, "")` does NOT protect against a key present with a null
        # value, and every model in the 36-cell matrix writes one: `str(None)`
        # is the non-empty string "None", so every replacement-less record
        # landed in one bucket and read as a funnel. All five firings on real
        # model output were that bug and none was a real collapse. Absence of a
        # replacement is its own fault, below -- not evidence of a shared one.
        raw = record.get("replacement")
        replacement = flatten(str(raw)).strip() if raw is not None else ""
        if replacement:
            absorbed.setdefault(replacement, []).append(segment_id)
    for replacement, segment_ids in sorted(absorbed.items()):
        if len(segment_ids) > SUPERSESSION_FAN_IN:
            found.append(Finding(
                DECLARED_LOSS_OVER_BUDGET,
                f"{len(segment_ids)} absent segments are declared replaced by the "
                f"same replacement ({', '.join(sorted(segment_ids))}), over the "
                f"ceiling of {SUPERSESSION_FAN_IN}. One replacement standing in "
                f"for that many segments has not replaced them, it has dropped "
                f"them: the detail it names is gone from the document",
            ))

    # 6b. The budget proper, over the whole merge rather than per source.
    drops = tuple(
        record for record in declared.values()
        if str(record.get("disposition", "")) == "dropped"
    )
    total = len(segments)
    # `budget * 100:g`, not `budget:.0%`: at a non-default ceiling the rounded
    # form names a budget that is not the one that fired -- 0.125 prints as
    # "12%" -- and this string is the reader's only account of why.
    if over_budget(len(drops), total, budget):
        found.append(Finding(
            DECLARED_LOSS_OVER_BUDGET,
            f"{len(drops)} of {total} segments are declared dropped "
            f"({len(drops) / total:.1%}), over the {budget * 100:g}% budget",
        ))

    # 7 and 8, together because they are one rule read from both ends.
    found += _title_checks(result, declared, title_policy, base)

    # 9. Content the merge states twice, character for character.
    #
    # This is a last mile, not a new detection. `duplication` above has run on
    # every merge since it was written and its result has been read by exactly one
    # line in `src/` -- the line that writes it. A value computed and never
    # reported is not a working check, and the reconciler has been here before:
    # an earlier version's eight checks were built, tested, and seven never
    # called. So this closes the loop rather than adding an instrument.
    #
    # **Exact repeats only, permanently.** `duplication` also runs a near-repeat
    # pass at `NEAR_MATCH`, kept for measurement only (see its docstring).
    # Promoting it was left open "until a threshold is chosen against
    # controls, or until a corpus with deliberate paraphrased duplication
    # exists to choose one on", and that question is now closed negatively. The
    # corpus is five real merges that restate both sources, and no threshold
    # separates them from the 23 documents the corpus asserts are correct: the
    # controls' highest intra-document similarity (0.970) exceeds the real
    # duplicated merges' highest (0.943), which exceeds their lowest (0.664).
    # A wrong pairing on the near pass is an accusation against a correct
    # document, and no constant value stops it being wrong in that direction.
    # The exact half fires on none of the 23.
    #
    # It is not routed into `parsing.check_merge` and so never reaches the model
    # as retry feedback. That boundary is deliberate and stated at
    # `parsing.py:727-735`: reconciler findings are the tool's verdict on the
    # merge, and feeding one back would be the tool negotiating its own result
    # away. A model that stated a fact twice is not making a shape error it can
    # be told to correct.
    #
    # No segment or document is named. The fault is in the merge, which is not a
    # source and carries no filename, and the repeated text identifies it
    # exactly. `declared_loss_over_budget` sets the same precedent.
    for repeat in result.duplicates:
        if not repeat.exact:
            continue
        found.append(Finding(
            DUPLICATED_CONTENT,
            f"{repeat.text!r} appears {repeat.count} times in the merged document, "
            f"identically; the merge states it more than once",
        ))

    return Reconciled(tuple(found), drops, total, result.added_breaks)


# --------------------------------------------------------------------------
# A statement credited to a source that does not carry it
# --------------------------------------------------------------------------
#
# `attribution_invented` was undetectable by construction: the merge
# credits a fact from one source to another, `prompts/decompose.md` rightly
# reads "the guide states X" as a claim about X, so the attribution never
# became a claim and the verifier was never asked about it. Teaching the
# decomposer to keep it could not have worked at `coverage`, which never reads
# the merged document back; this reads the texts and needs no model at all, so
# it runs on `merge` and on `verify` and at both depths.
#
# Not one of `CHECKS` and not in `FINDING_KINDS`, and both on purpose.
# `CHECKS` counts the reconciler's comparisons of a merge against its own
# disposition records, and this reads none. `FINDING_KINDS` is a contract with
# the page, which partitions it into two sections and fails its own suite on a
# kind it does not list; until the page renders this family the report carries
# it under a heading of its own, and so does `report.json`.
MISATTRIBUTED = "misattributed"

# The two shapes of attribution this looks for, and only these. A wider net is
# a wider accusation: every sentence it matches is one the reader is about to
# be told misquotes a source. "According to NAME, CONTENT" is the shape every
# attribution in the fixture corpus takes and the one `merge.md` describes;
# "NAME states that CONTENT" is its commonest rewording. `that` is required in
# the second, so a sentence whose subject merely *says* something is not read
# as a citation.
_ACCORDING_TO = re.compile(
    r"^according to (?P<name>[^,]{1,80}),\s+(?P<content>\S.*?)[.!]?$",
    re.IGNORECASE)
_STATES_THAT = re.compile(
    r"^(?P<name>[^,]{1,80}?)\s+(?:states|says|notes|reports|specifies)\s+that\s+"
    r"(?P<content>\S.*?)[.!]?$",
    re.IGNORECASE)
# The separators a title uses between a product and a document's own name:
# "Vandrell Relay - Operator Guide". A name resolves to the whole title, to one
# of these parts, or to the filename, and never to a word inside a part --
# "the relay" is in both of that pair's titles and names neither of them.
_TITLE_PARTS = re.compile(r"\s+[-\u2013\u2014:|]\s+")


def _name_key(name: str) -> str:
    """A document name as a merge might write it, reduced for comparison."""
    words = name.strip().strip("\"'`*_").split()
    if words and words[0].lower() in ("the", "a", "an"):
        words = words[1:]
    return " ".join(words).lower()


def _names_of(filename: str, text: str, shown: str = "") -> set[str]:
    """Every name this source can be cited by: its title, a part of it, its file."""
    names = {_name_key(filename), _name_key(filename.rsplit(".", 1)[0])}
    if shown:
        base = shown.replace("\\", "/").rsplit("/", 1)[-1]
        names |= {_name_key(base), _name_key(base.rsplit(".", 1)[0])}
    for title in titles_of(segment_document(text, "x", filename).segments):
        names.add(_name_key(title.text))
        names |= {_name_key(part) for part in _TITLE_PARTS.split(title.text)}
    return {name for name in names if name}


def attribution_findings(documents: dict[str, str], merged: str,
                         shown: dict[str, str] | None = None) -> tuple[Finding, ...]:
    """Each merged sentence that credits a source with content it does not carry.

    `documents` is the sources by canonical filename, `merged` the merged text,
    and `shown` the names the caller gave the files, so "according to
    notes-a.md" resolves as well as "according to source_a.md" does.

    Fires only when all four hold, and each is a bound on who can be accused:

      1. the sentence is one of the two attribution shapes above;
      2. the sentence is in no source as written, so the attribution is the
         merge's own and not one it carried over from a document;
      3. the name resolves to **exactly one** source, by its title, a
         separated part of its title, or its filename -- a name that fits two
         sources or none is not something this can check;
      4. the content is in another source and **not** in the one named.

    The fourth is what makes a finding a finding. Content found in no source
    is left to the reverse pass, where it is an invention of fact rather than
    of attribution; content reworded past `occurs` is left alone, because a
    paraphrase cannot be told from a misquotation by string comparison and
    this module does not guess.
    """
    shown = shown or {}
    flat = {name: flatten(text) for name, text in documents.items()}
    names = {name: _names_of(name, text, shown.get(name, ""))
             for name, text in documents.items()}
    found: list[Finding] = []
    for item in segment_document(merged, MERGE_LETTER).segments:
        text = flatten(item.text)
        match = _ACCORDING_TO.match(text) or _STATES_THAT.match(text)
        if match is None:
            continue
        if any(occurs(text, source) for source in flat.values()):
            continue
        key = _name_key(match.group("name"))
        named = [name for name in documents if key in names[name]]
        if len(named) != 1:
            continue
        credited = named[0]
        content = match.group("content").strip()
        if occurs(content, flat[credited]):
            continue
        carriers = [name for name in documents
                    if name != credited and occurs(content, flat[name])]
        if not carriers:
            continue
        carrier = carriers[0]
        said = next((segment.text
                     for segment in segment_document(documents[carrier], "x",
                                                     carrier).segments
                     if occurs(content, flatten(segment.text))), "")
        found.append(Finding(
            MISATTRIBUTED,
            f"the merge credits {content!r} to {match.group('name').strip()} "
            f"({shown.get(credited) or credited}), which does not state it; "
            f"{shown.get(carrier) or carrier} does",
            segment=item.id,
            document=credited,
            source_text=said,
            merge_text=item.text,
        ))
    return tuple(found)
