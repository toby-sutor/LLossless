#!/usr/bin/env python3
"""The models table stays inside its box: what a browser measured, pinned here.

The operator's report was *"the models table requires horizontal scroll now"*,
and the cause was found: two caveat sentences were being rendered into the Model cell
of every command row, `table.models .model-meta` sets `white-space: nowrap`, so
each sentence was one unwrapped line. Four subscription rows beside the six
catalogue ones took the Model column from 410px to 670px and the table from
1009px to 1320px inside a 1009px box -- 311px of horizontal scroll at a 1280px
viewport -- and the cost cell's `counts against your plan`, in a `td.num` that
also does not wrap, held a 95px column open at 215px.

**There is no browser in this suite, so nothing here measures a pixel.** The
widths above were measured by driving a real Chromium at 1280px and at 380px,
with every command route switched on, and they are recorded in the
scratch probe beside it. What this module holds are the three file-level
properties those measurements rest on, each of which is silent when it breaks:

**that no string rendered into a cell that cannot wrap is a sentence.** A
character count is a proxy for a width this suite cannot ask for, and the
budgets below are read off the measured layout rather than chosen for
tidiness: the table's box is 1009px, the Model column fits 410px of it, and at
the .8rem these spans are set in a character is about 6px. A 24-character
marker is about 145px; the sentence it replaced was 116.

**that the note under a model name wraps and the meta line above it does
not.** `.route-note` also carries `.model-meta`, whose rule is `nowrap`, so the
override is what keeps a long *translation* of a short marker from bringing the
scroll back. Both halves are asserted, and so is the order they appear in:
the two selectors have equal specificity, so the later rule is the one that
wins and moving it above its neighbour would silently undo it.

**that both facts are still said somewhere a reader can see them.** Shortening
a caveat to a marker is only honest if the sentence survives: a subscription
row really is not comparable with figures measured at `json_schema`, and it
really is shared by every account on the instance. So every marker the table
can put on a row must have a sentence under the table that names that marker --
and none of it may be a `title`, which does not exist on touch and is not
reliably announced.

Every rule has a seeded probe beside it. Run with
`python3 tests/test_web_table.py`, or collect with pytest.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# This module reads three files off disk and opens nothing. The guard is
# installed all the same, in the shape `tests/test_socket_guard.py` scans every
# test module for: a module that is exempt because it "obviously" has no
# network in it is the module somebody later adds a fetch to.
socket_guard.install()

from llossless.web import i18n  # noqa: E402

STATIC = ROOT / "src" / "llossless" / "web" / "static"
INDEX = STATIC / "index.html"
APP_CSS = STATIC / "app.css"
APP_JS = STATIC / "app.js"

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# reading the files
# --------------------------------------------------------------------------


def source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_comments(js: str) -> str:
    """The script with its comments gone, so a comment cannot satisfy a check.

    Every rule below asks whether the script *renders* something. A block
    comment naming the key it used to render would answer yes to a plain
    substring search, and this file's comments quote their own history at
    length. The `:` lookbehind is what keeps `https://` out of it.
    """
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    return re.sub(r"""(?m)(?<![:"'])//.*$""", "", js)


# The functions that build a row. The table used to be one loop inside
# `renderModels`; it is now the picker's row and the scorecard's row, built
# from one name line and one set of markers, and every row rule below is
# asserted against all of them together.
ROW_BUILDERS = ("modelNameLine", "routeMarks", "pickerRow", "scorecardRow",
                "renderScorecard")


def row_source(js: str | None = None) -> str:
    """The row builders' source, joined, as `js_function` reads each one."""
    return "\n".join(js_function(name, js) for name in ROW_BUILDERS)


def js_function(name: str, js: str | None = None) -> str:
    """One top-level function's source, to the first column-zero closing brace."""
    js = strip_comments(source(APP_JS)) if js is None else js
    marker = f"function {name}("
    check(marker in js, f"{name} is no longer a top-level function of app.js")
    if marker not in js:
        return ""
    body = js[js.index(marker):]
    end = body.find("\n}\n")
    return body[:end if end != -1 else len(body)]


def css_rule(css: str, selector: str) -> str:
    """One rule's declarations, by selector. `` where there is no such rule."""
    match = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css)
    return match.group(1) if match else ""


def catalogues() -> dict[str, dict[str, str]]:
    """Every catalogue this server can serve, keyed by tag.

    `read` rather than `load`, for `tests/test_web_static.py`'s reason: whether
    a catalogue validates is `tests/test_web_i18n.py`'s question, and a `load`
    here would answer every check below with the same traceback.
    """
    return {tag: i18n.read(tag)["strings"] for tag in i18n.available()}


def reachable_in_js(key: str, js: str) -> bool:
    """Can the script name this key -- literally, or through a prefix it builds?

    `costCell` renders `t("models.cost." + String(route.cost) + ".cell")`, so
    the key `models.cost.plan.cell` appears nowhere in the file and is rendered
    on every subscription row. A rule that only looked for the whole literal
    would report it as dead and teach the next reader to delete it.
    """
    if f'"{key}"' in js:
        return True
    parts = key.split(".")
    return any(f'"{".".join(parts[:n])}."' in js for n in range(1, len(parts)))


# --------------------------------------------------------------------------
# no sentence goes in a cell that cannot wrap
# --------------------------------------------------------------------------

# Every catalogue string the models table renders inside a cell whose content
# cannot wrap, and the number of characters each is held to. Written out rather
# than discovered: what makes a string a cell string is which element it is
# appended to, which no scan of this file can see, and a rule that guessed
# would either miss the one that matters or fire on a hint.
#
# Three budgets, each from what the column has to spend.
CELL_BUDGETS: tuple[tuple[str, int], ...] = (
    # The two row markers, in the Model column beside a 410px name and meta
    # line. `models.route.mark.*` replaced two sentences of 116 and 81
    # characters; 24 is about 145px at .8rem, which the column has.
    ("models.route.mark.incomparable", 24),
    ("models.route.mark.shared", 24),
    # The Cost column, against a 95px header. `counts against your plan` held
    # it open at 215px; `on plan` is 7 characters and the two neutral words
    # beside it are 14.
    ("models.cost.plan.cell", 16),
    ("models.notpriced", 16),
    ("models.unmeasured", 16),
    # The three measured columns: a rate's denominator and a band word, both
    # `nowrap` spans under a figure.
    ("models.perpair", 16),
    ("models.band.good", 16),
    ("models.band.fair", 16),
    ("models.band.poor", 16),
    # The route badge on every row and the context window beside every name.
    # Wider, because the badge is the one piece of vocabulary a reader has to
    # be able to tell apart at a glance, and `command on this server` is 22.
    ("route.metered", 32),
    ("route.subscription", 32),
    ("route.command", 32),
    ("route.selfhosted", 32),
    ("route.unknown", 32),
    ("models.window", 24),
)

# The one string the table renders that is allowed to be a sentence, because
# `.unreachable-why` sets `white-space: normal` for it. Named here so that the
# list above reads as the complete set of the ones that cannot wrap.
WRAPS_IN_A_CELL = "models.unreachable"


def over_budget(strings: dict[str, str]) -> list[str]:
    """Every cell string in one catalogue that is longer than its budget."""
    return [f"{key} is {len(strings[key])} characters and the budget is {budget}"
            for key, budget in CELL_BUDGETS
            if key in strings and len(strings[key]) > budget]


def test_no_string_in_a_cell_that_cannot_wrap_is_a_sentence() -> None:
    """Asked of every catalogue, not of the reference alone.

    The German is an agent's work rather than a translator's, which is the
    reason this runs against it: a translation that needs three words where
    English needed one is exactly how a marker becomes a sentence again, and
    nobody would see it on an English page.
    """
    found = catalogues()
    check(len(found) >= 2,
          f"only {sorted(found)} found in web/locales/; discovery has drifted")
    js = strip_comments(source(APP_JS))
    for key, _budget in CELL_BUDGETS:
        check(reachable_in_js(key, js),
              f"{key} is budgeted here and the script cannot name it; the "
              f"list has gone stale")
    for tag, strings in sorted(found.items()):
        for key, _budget in CELL_BUDGETS:
            check(key in strings, f"{tag}.json has no string for {key}")
        for problem in over_budget(strings):
            check(False, f"{tag}.json: {problem}")
    # And the one that is allowed to be long is allowed by a rule in the
    # stylesheet, not by being forgotten.
    check("white-space: normal" in css_rule(source(APP_CSS),
                                            "table.models .unreachable-why"),
          f"{WRAPS_IN_A_CELL} is exempt from the budgets and "
          f".unreachable-why no longer wraps")


def test_the_length_budget_fires_on_the_sentence_it_replaced() -> None:
    """Seeded with the real regression: the caveat put back in the cell.

    Not an invented 200-character string. The probe is the exact value 531
    took out of the Model cell, from the catalogue it is still in, so what is
    proved is that the budget catches *this* coming back.
    """
    for tag, strings in sorted(catalogues().items()):
        # `get` with the sentence written out: on a tree where the long key has
        # been dropped the probe still has something to seed with, and reports
        # a failed check rather than a KeyError from inside a probe.
        sentence = strings.get("models.route.incomparable", "x" * 116)
        seeded = dict(strings)
        seeded["models.route.mark.incomparable"] = sentence
        problems = over_budget(seeded)
        check(any("models.route.mark.incomparable" in problem
                  for problem in problems),
              f"the sentence back in the {tag} marker does not break the budget")
        seeded = dict(strings)
        seeded["models.cost.plan.cell"] = strings.get("models.cost.plan",
                                                      "x" * 24)
        check(any("models.cost.plan.cell" in problem
                  for problem in over_budget(seeded)),
              f"the sentence back in the {tag} cost cell does not break the "
              f"budget")
    # Must-not-fire: the shipped catalogues pass the same predicate.
    for tag, strings in sorted(catalogues().items()):
        check(not over_budget(strings),
              f"{tag}.json is over budget as shipped: {over_budget(strings)}")


def test_the_row_carries_the_marker_and_never_the_sentence() -> None:
    """Which of the two wordings the row builders put on a row.

    Both are still in the catalogues and both are still rendered: the sentence
    is what the credentials sheet says beside a tool that has not been switched
    on yet, where there is a paragraph's worth of room. The rule is about the
    table, so it is asserted against the function that builds a row rather than
    against the file.
    """
    rows = row_source()
    for key in ("models.route.mark.incomparable", "models.route.mark.shared"):
        check(f'"{key}"' in rows, f"a table row no longer renders {key}")
    for key in ("models.route.incomparable", "models.route.shared",
                "models.route.caveat.incomparable", "models.route.caveat.shared",
                "models.route.caveat.cost"):
        check(f'"{key}"' not in rows,
              f"{key} is a sentence and is being rendered into a table row")
    check("renderRouteCaveats()" in rows,
          "the row markers are rendered and the sentences under the table are "
          "not; a marker with nothing explaining it is the caveat deleted")


def test_the_marker_check_fires_in_both_directions() -> None:
    """Seeded: the sentence back on the row, and the footnote call removed."""
    rows = row_source()
    seeded = rows.replace('"models.route.mark.incomparable"',
                          '"models.route.incomparable"')
    check(seeded != rows, "the probe's anchor has moved")
    check('"models.route.incomparable"' in seeded
          and '"models.route.mark.incomparable"' not in seeded,
          "a row that went back to the sentence is not caught")
    check("renderRouteCaveats()" not in rows.replace("renderRouteCaveats()", ""),
          "the probe cannot see its own anchor, so the call check passed over "
          "nothing")


# --------------------------------------------------------------------------
# the wrap rule, which is the structural half
# --------------------------------------------------------------------------

META = "table.models .model-meta"
NOTE = "table.models .route-note"


def wrap_problems(css: str) -> list[str]:
    """Every way the two wrap rules stop holding the markers in. Empty is pass."""
    problems = []
    if "white-space: nowrap" not in css_rule(css, META):
        problems.append(f"{META} no longer sets nowrap, so the note's override "
                        f"is now the only rule and reads as noise")
    if "white-space: normal" not in css_rule(css, NOTE):
        problems.append(f"{NOTE} no longer sets normal, so a long marker is "
                        f"one unwrapped line again")
    at_meta, at_note = css.find(META + " "), css.find(NOTE + " ")
    if at_meta == -1 or at_note == -1:
        problems.append("one of the two rules is gone from the stylesheet")
    elif at_note < at_meta:
        problems.append(f"{NOTE} now comes before {META}; the two selectors "
                        f"weigh the same, so the later one wins and this "
                        f"order silently restores nowrap")
    return problems


def test_the_marker_wraps_and_the_meta_line_it_sits_under_does_not() -> None:
    """The half that survives a translation nobody here can read.

    A budget is a rule about the strings that are in the file today. The
    override is a rule about the ones that are not: a two-word marker that
    becomes eight words in a language this project has no reader for still
    wraps instead of widening the column.
    """
    for problem in wrap_problems(source(APP_CSS)):
        check(False, problem)


def test_the_wrap_rules_fire_in_three_directions() -> None:
    """Seeded: each rule deleted, and the pair reordered.

    The third is the one a probe on either rule alone would miss. Equal
    specificity means source order decides, so a tidy-up that moved the note's
    rule up beside its neighbour would leave both declarations present and the
    override dead.
    """
    css = source(APP_CSS)
    check(bool(wrap_problems(css.replace(
        f"{NOTE} {{ color: var(--ink-soft); white-space: normal; }}",
        f"{NOTE} {{ color: var(--ink-soft); }}"))),
          "the note's rule deleted does not fail the wrap check")
    # Inside the meta rule, not the first `nowrap` in the file: `td.num` sets
    # one several rules earlier, and a seed that edited that one would prove
    # only that the probe can break a rule nothing here is about.
    meta_rule = re.search(re.escape(META) + r"\s*\{[^}]*\}", css)
    check(meta_rule is not None, "the meta line's rule is no longer matchable")
    if meta_rule:
        check(bool(wrap_problems(css.replace(
            meta_rule.group(0),
            meta_rule.group(0).replace("white-space: nowrap;", "")))),
              "the meta line's nowrap deleted does not fail the wrap check")
    note_rule = re.search(re.escape(NOTE) + r"\s*\{[^}]*\}", css)
    check(note_rule is not None, "the note's rule is no longer matchable")
    if note_rule:
        moved = css.replace(note_rule.group(0), "")
        moved = moved.replace(META, note_rule.group(0) + "\n" + META, 1)
        check(bool(wrap_problems(moved)),
              "the note's rule moved above the meta line's does not fail the "
              "wrap check")
    check(not wrap_problems(css), "the shipped stylesheet fails its own check")


# --------------------------------------------------------------------------
# where a line may break, which is what held the Check column open
# --------------------------------------------------------------------------

# The table once overflowed to 1027px inside a 1009px box at 1280px with the
# Check column on, in English, and a later drive found the German table 258px
# past it with the column *off*. Every cause was a phrase in a run that could
# not break: the wire name and window as one 376px line, the four figure
# headers under `th.num`'s `nowrap`, and a name and its route badge as one run.
# Measured in Chromium before and after; what is pinned here is the three
# break rules, because the widths themselves are not a thing this suite sees.

WIRE = "table.models .model-meta.model-wire"
WIRE_PART = "table.models .model-meta.model-wire > span"
NUM_HEAD = "table.models th.num"
NAME = "table.models .model-name"
NAME_PART = "table.models .model-name > span:first-child"


def break_problems(css: str, js: str) -> list[str]:
    """Every way the table's three break points stop holding. Empty is pass."""
    problems = []
    if "white-space: normal" not in css_rule(css, WIRE):
        problems.append(f"{WIRE} no longer wraps, so the wire name and window "
                        f"are one unbreakable run again")
    if "white-space: nowrap" not in css_rule(css, WIRE_PART):
        problems.append(f"{WIRE_PART} no longer keeps each half whole, so a "
                        f"model id can break at its hyphens")
    if "white-space: normal" not in css_rule(css, NUM_HEAD):
        problems.append(f"{NUM_HEAD} no longer wraps, so the figure headers "
                        f"are `th.num`'s nowrap phrases again")
    if "nowrap" in css_rule(css, NAME):
        problems.append(f"{NAME} is nowrap again, so the badge cannot leave "
                        f"the name's line")
    if "white-space: nowrap" not in css_rule(css, NAME_PART):
        problems.append(f"{NAME_PART} no longer keeps the name whole")
    rows = row_source(js)
    if '"model-meta mono model-wire"' not in rows:
        problems.append("the meta line no longer carries the class its wrap "
                        "rule is written against")
    if '" \\u00b7 " + t("models.window"' in rows:
        problems.append("the wire name and window are concatenated into one "
                        "text node again, so there is nothing to keep whole")
    if 'createElement("wbr")' not in rows:
        problems.append("the name line has no break opportunity before the "
                        "badge")
    return problems


def test_the_table_has_three_places_to_break_and_no_others() -> None:
    """Between the wire name and window, inside a figure header, before a badge."""
    for problem in break_problems(source(APP_CSS), strip_comments(source(APP_JS))):
        check(False, problem)


def test_the_break_rules_fire_when_each_is_undone() -> None:
    """Seeded: each rule deleted, and the meta line concatenated back to one run.

    The concatenation is the exact line 565 replaced, so what is proved is that
    the check catches *that* coming back rather than an invented regression.
    """
    css = source(APP_CSS)
    js = strip_comments(source(APP_JS))
    check(not break_problems(css, js), "the shipped files fail their own check")
    for selector, declaration in ((WIRE, "white-space: normal;"),
                                  (WIRE_PART, "white-space: nowrap;"),
                                  (NUM_HEAD, "white-space: normal;"),
                                  (NAME_PART, "white-space: nowrap;")):
        rule = re.search(re.escape(selector) + r"\s*\{[^}]*\}", css)
        check(rule is not None and declaration in rule.group(0),
              f"the probe cannot find {declaration} in {selector}")
        if rule:
            seeded = css.replace(rule.group(0),
                                 rule.group(0).replace(declaration, ""))
            check(bool(break_problems(seeded, js)),
                  f"{selector} without {declaration} is not caught")
    name_rule = re.search(re.escape(NAME) + r"\s*\{[^}]*\}", css)
    check(name_rule is not None, "the name's rule is no longer matchable")
    if name_rule:
        seeded = css.replace(name_rule.group(0), name_rule.group(0).replace(
            "font-weight: 600;", "font-weight: 600; white-space: nowrap;"))
        check(bool(break_problems(seeded, js)),
              "the name made nowrap again is not caught")
    seeded = js.replace('createElement("wbr")', 'createElement("span")')
    check(seeded != js and bool(break_problems(css, seeded)),
          "the badge's break opportunity removed is not caught")
    seeded = js.replace('"model-meta mono model-wire"', '"model-meta mono"')
    check(seeded != js and bool(break_problems(css, seeded)),
          "the meta line without its wrap class is not caught")
    rows = js_function("scorecardRow", js)
    seeded = js.replace(rows, rows + '\n  setText(meta, id + (window ? " \\u00b7 " '
                                     '+ t("models.window", { n: window }) : ""));')
    check(bool(break_problems(css, seeded)),
          "the wire name and window concatenated back into one run is not "
          "caught")


# --------------------------------------------------------------------------
# the split control follows the route the radio moved to
# --------------------------------------------------------------------------

# `renderModels` sets `split.disabled` from `chosenRoute()`, and the Use
# column's handler called only `refreshIdleStatus`. Driven in Chromium: the
# button moved to `metered API` while the split stayed disabled from the
# preselected subscription row, and a ticked split kept its Check column under
# a command route. The fix re-renders on a crossing and puts focus back, and a
# drive with the focus line removed showed why the second half matters: after
# an ArrowUp onto a command route focus fell to the body and the next ArrowDown
# moved nothing.


def split_problems(js: str) -> list[str]:
    """Every way the Use column's handler stops owning the split. Empty is pass."""
    problems = []
    cell = js_function("useCell", js)
    if "renderModels()" not in cell:
        problems.append("the Use column's handler never re-renders, so the "
                        "split control keeps the route it was drawn under")
    if "chosenRoute()" not in cell:
        problems.append("the Use column's handler no longer asks whether the "
                        "selection crossed a command route")
    at_render = cell.find("renderModels()")
    if ".focus()" not in cell[max(at_render, 0):]:
        problems.append("the handler rebuilds the rows and does not put focus "
                        "back, so a keyboard reader is dropped on the body")
    return problems


def test_the_use_column_re_renders_the_split_on_a_route_crossing() -> None:
    for problem in split_problems(strip_comments(source(APP_JS))):
        check(False, problem)


def test_the_split_check_fires_on_each_half_removed() -> None:
    """Seeded against the shipped handler, not a copy of it."""
    js = strip_comments(source(APP_JS))
    check(not split_problems(js), "the shipped handler fails its own check")
    cell = js_function("useCell", js)
    for piece, what in (("renderModels();", "the re-render"),
                        ("chosen.focus();", "the focus restore")):
        check(piece in cell, f"the probe cannot find {what} in useCell")
        seeded = js.replace(cell, cell.replace(piece, ""))
        check(bool(split_problems(seeded)), f"{what} removed is not caught")


# --------------------------------------------------------------------------
# the facts are still on the page
# --------------------------------------------------------------------------

# Each marker the table can put on a row, and the sentence under the table that
# has to explain it. The pairing is the check: a caveat that does not quote its
# own marker is a footnote a reader cannot attach to the thing they are looking
# at, and it is how one of the two could be deleted without the other noticing.
MARKED: tuple[tuple[str, str], ...] = (
    ("models.route.mark.incomparable", "models.route.caveat.incomparable"),
    ("models.route.mark.shared", "models.route.caveat.shared"),
    ("models.cost.plan.cell", "models.route.caveat.cost"),
)

# Shortest a caveat may be. A sentence that has been trimmed to the length of
# the marker it explains has stopped being the explanation.
CAVEAT_MIN = 60


def caveat_problems(strings: dict[str, str]) -> list[str]:
    """Every way one catalogue's caveats stop carrying the facts."""
    problems = []
    for mark, caveat in MARKED:
        if caveat not in strings:
            problems.append(f"{caveat} is gone, so the {mark} marker has "
                            f"nothing explaining it")
            continue
        text = strings[caveat]
        if mark in strings and strings[mark] not in text:
            problems.append(f"{caveat} does not name the marker it explains, "
                            f"{strings.get(mark)!r}")
        if len(text) < CAVEAT_MIN:
            problems.append(f"{caveat} is {len(text)} characters; a caveat "
                            f"this short is not the sentence that was moved")
    # In plain words, not by the rung's name: the answer format is
    # only asked for in the prompt, and the figures are not to be set against
    # rows that use an API. Both words are the same in every catalogue.
    tier = strings.get("models.route.caveat.incomparable", "")
    for word in ("prompt", "API"):
        if word.lower() not in tier.lower():
            problems.append(f"the comparability caveat no longer says {word!r}: "
                            f"what the route is told in the prompt, and what its "
                            f"figures must not be set against, is the whole of "
                            f"why the row is not directly comparable")
    return problems


def test_every_marker_has_its_sentence_under_the_table() -> None:
    """Both facts kept, in every catalogue, and each tied to its marker."""
    for tag, strings in sorted(catalogues().items()):
        for problem in caveat_problems(strings):
            check(False, f"{tag}.json: {problem}")
    # And the element they are written into is under the table rather than in
    # it: inside the `.scroll` box it would be one more thing holding the box
    # open, which is the defect this whole module is about.
    html = source(INDEX)
    check('data-cc="route-caveats"' in html,
          "the element the caveats are written into is gone from the markup")
    box = html.find('<div class="scroll">')
    close = html.find("</table>", box)
    check(0 <= box < close < html.find('data-cc="route-caveats"'),
          "the caveats are inside the scrolling box rather than under it")
    said = js_function("renderRouteCaveats")
    for _mark, caveat in MARKED:
        check(f'"{caveat}"' in said, f"{caveat} is never rendered")


def test_the_caveat_check_fires_on_a_deletion_and_on_a_renamed_marker() -> None:
    """Seeded both ways, because this is the check that stops a silent cut."""
    for tag, strings in sorted(catalogues().items()):
        seeded = dict(strings)
        seeded.pop("models.route.caveat.shared", None)
        check(any("models.route.caveat.shared" in problem
                  for problem in caveat_problems(seeded)),
              f"the shared caveat deleted from {tag}.json is not caught")
        seeded = dict(strings)
        seeded["models.route.mark.shared"] = "elsewhere"
        check(bool(caveat_problems(seeded)),
              f"a {tag} marker its caveat does not name is not caught")
        seeded = dict(strings)
        seeded["models.route.caveat.incomparable"] = strings.get(
            "models.route.mark.incomparable", "short")
        check(bool(caveat_problems(seeded)),
              f"a {tag} caveat trimmed to its own marker is not caught")
        seeded = dict(strings)
        seeded["models.route.caveat.incomparable"] = strings.get(
            "models.route.caveat.incomparable", "").replace("API", "endpoint")
        check(bool(caveat_problems(seeded)),
              f"a {tag} caveat that no longer names what not to compare with is not caught")
        check(not caveat_problems(strings),
              f"{tag}.json fails its own caveat check as shipped")


def test_no_caveat_is_a_tooltip() -> None:
    """Visible but once, never hidden on demand.

    Hover does not exist on touch, `title` is not reliably announced by a
    screen reader, and a caveat only some readers can reach is the failure this
    text exists to prevent. The page does use `title` -- on the disabled radio
    of an unreachable row, where it repeats what the row already says in words
    -- so the ban is on these strings rather than on the attribute.
    """
    js = strip_comments(source(APP_JS))
    for line in js.splitlines():
        if ".title" in line and "=" in line:
            check("route.caveat" not in line and "route.mark" not in line
                  and "cost.plan" not in line,
                  f"a caveat is being written into a tooltip: {line.strip()}")
    said = js_function("renderRouteCaveats")
    check(".title" not in said,
          "renderRouteCaveats sets a tooltip; the sentences are meant to be "
          "read without reaching for them")
    html = source(INDEX)
    element = html[html.find('data-cc="route-caveats"'):]
    check("title=" not in element[:element.find(">")],
          "the caveats element carries a title attribute")


def test_the_tooltip_ban_fires() -> None:
    """Seeded: the sentence assigned to a `title`."""
    seeded = 'row.title = t("models.route.caveat.shared");'
    check("route.caveat" in seeded and ".title" in seeded and "=" in seeded,
          "the probe would not be recognised as a tooltip assignment")
    check(".title" in 'target.title = t("models.route.caveat.cost");',
          "the renderRouteCaveats probe would not be recognised")


# --------------------------------------------------------------------------
# the cost cell, which is a word and never a zero
# --------------------------------------------------------------------------


def cost_problems(strings: dict[str, str]) -> list[str]:
    """Every way the subscription cost cell stops being honest."""
    problems = []
    word = strings.get("models.cost.plan.cell", "")
    if not word.strip():
        problems.append("models.cost.plan.cell is empty, so the cost cell of "
                        "a subscription row renders as nothing")
    if any(character.isdigit() for character in word):
        problems.append(f"models.cost.plan.cell is {word!r}, which reads as a "
                        f"figure; a subscription reports no token counts at all")
    if word and word == strings.get("models.unmeasured"):
        problems.append("a subscription row and a row nobody measured now read "
                        "the same; one is an answer and the other is an absence")
    return problems


def test_a_subscription_cost_cell_is_a_word_and_never_a_zero() -> None:
    """`pricing.py`'s rule, at the one place the web page can break it.

    A zero reads as *measured, and free*, which inverts the comparison against
    every row that carries a real figure. `costCell` renders a word the server
    chose -- `route.cost` -- and there is no branch on the page that can
    produce a number for a route; this is the other half, that the word itself
    is not one.
    """
    for tag, strings in sorted(catalogues().items()):
        for problem in cost_problems(strings):
            check(False, f"{tag}.json: {problem}")
    cell = js_function("costCell")
    check('t("models.cost." + String(route.cost) + ".cell")' in cell,
          "the cost cell no longer reads the short form the server's own word "
          "names, so the column can go back to a sentence")


def test_the_zero_cost_check_fires() -> None:
    """Seeded: the cell as a zero, as a blank, and as the unmeasured word."""
    for tag, strings in sorted(catalogues().items()):
        for bad in ("$0.00", "   ", strings.get("models.unmeasured", "")):
            seeded = dict(strings)
            seeded["models.cost.plan.cell"] = bad
            check(bool(cost_problems(seeded)),
                  f"a {tag} cost cell reading {bad!r} is not caught")
        check(not cost_problems(strings),
              f"{tag}.json fails its own cost check as shipped")


def freetier_problems(strings: dict[str, str]) -> list[str]:
    """Every way the free-tier cost cell stops being honest: the `freetier`
    word that a free-tier row renders, checked as a string."""
    word = strings.get("models.cost.freetier.cell", "")
    problems = []
    if not word.strip():
        problems.append("models.cost.freetier.cell is empty")
    if any(character.isdigit() for character in word) or "$" in word:
        problems.append(f"models.cost.freetier.cell is {word!r}, which reads as a figure")
    if word and word in (strings.get("models.unmeasured"), strings.get("models.notpriced")):
        problems.append("a free-tier row reads like a row nobody measured, or a GPU-minute row")
    return problems


def test_a_free_tier_cost_cell_is_a_word_and_never_a_zero() -> None:
    """A run billed $0.00 is measured and not free: the page says which."""
    for tag, strings in sorted(catalogues().items()):
        for problem in freetier_problems(strings):
            check(False, f"{tag}.json: {problem}")
    cell = js_function("costCell")
    check('measured.billed === "free-tier"' in cell
          and 't("models.cost.freetier.cell")' in cell,
          "the cost cell no longer renders the free-tier word for a free-tier row")


def test_the_free_tier_cost_check_fires() -> None:
    """Seeded: the word as a zero, a blank and the unmeasured word."""
    for tag, strings in sorted(catalogues().items()):
        for bad in ("$0.00", " ", strings.get("models.unmeasured", "")):
            seeded = dict(strings)
            seeded["models.cost.freetier.cell"] = bad
            check(bool(freetier_problems(seeded)),
                  f"a {tag} free-tier cell reading {bad!r} is not caught")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_table" and callable(function):
            function()
    if failures:
        print(f"web table: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web table: {checks} checks pass")
    return 0


def test_web_table() -> None:
    """pytest entry point."""
    assert main() == 0, "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
