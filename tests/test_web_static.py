#!/usr/bin/env python3
"""The shipped interface: what it references, what it says, and what it escapes.

`src/llossless/web/static/` is `index.html`, `app.css` and `app.js`, no
build step, no dependency and no framework. There is no browser in this suite,
so nothing here renders anything. What it checks instead is the set of
properties that are true of the *files* and would each be invisible until an
operator hit them:

**that the page reaches nothing off this machine.** A self-hosted tool that
fetches a font, a stylesheet or a script from a third party has told that third
party who is running it and when. The scan is by shape rather than by a
denylist of hosts, and it has a must-fire probe per file type, because a scan
that has never fired has not been shown to work -- this repository has shipped
a green leak scan twice over a file that was leaking.

**that the page and the server agree about what exists.** Four vocabularies
cross the boundary: the `data-cc` hooks the script looks up, the `data-t` keys
the markup carries, the `/api/` paths the script calls, and the event kinds it
subscribes to. Each of them fails silently in its own way -- a missing hook is
an exception in one handler, a missing string is a key printed where a sentence
should be, a wrong path is a 404 the operator sees as "nothing happened", and
an unsubscribed event kind is dropped by `EventSource` without a trace. All
four are checked in both directions.

**that nothing from a document or a model can become markup.** `html_report.py`
treats escaping as a security property and holds a `<script>` probe against its
own output. The same material reaches this page, so the same probe runs here:
one merge with a hostile document label, through a real server, asserted
escaped in what the server hands out and asserted *present and raw* in the JSON
the page consumes -- which is what makes the page's own escaping load-bearing
rather than decorative.

**that "not checked" is not rendered as "clean".** `structural.ran` and
`decisions.ran` are booleans, and an empty findings list under a false one
means nobody looked. The chip vocabulary is asserted to keep the two apart.

Run with `python3 tests/test_web_static.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs. Two servers are bound below -- this
# tool's own and the scripted endpoint behind it -- so this is the module's
# claim that the only sockets it opens are the ones it bound itself;
# `tests/test_socket_guard.py` asserts every test module states it in exactly
# this shape.
socket_guard.install()

from llossless import (config, decompose, html_report, merge,  # noqa: E402
                        reconcile, report, segment, verify)
from llossless.web import (catalogue, commands, credentials,  # noqa: E402
                            discover, events, i18n, server)

import rank_scale_floor  # noqa: E402
from fake_endpoint import FakeEndpoint  # noqa: E402
from test_cli import CLEAN, SOURCE_A, SOURCE_B, Script  # noqa: E402

STATIC = ROOT / "src" / "llossless" / "web" / "static"
INDEX = STATIC / "index.html"
APP_CSS = STATIC / "app.css"
APP_JS = STATIC / "app.js"

failures: list[str] = []
unmeasured: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def decline(message: str) -> None:
    """A third outcome beside pass and fail, for what this machine cannot ask.

    `run_all.py` reads the marker at the start of a line the same way it does
    for every other declining tool. Unknown is not clean.
    """
    unmeasured.append(message)


# --------------------------------------------------------------------------
# reading the three files
# --------------------------------------------------------------------------

# Long enough that a loaded machine running the whole suite does not fail a
# check about a state transition, short enough that a genuine hang is reported
# as one. The same number `tests/test_web_server.py` uses, for the reason it
# gives there.
PATIENCE = 60.0

# The label a hostile document is submitted under. Deliberately the exact
# string `tests/test_html_report.py` probes with, so that a reader comparing
# the two checks is comparing them on the same input.
HOSTILE = "<script>alert(1)</script>"


def source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_comments(js: str) -> str:
    """JavaScript with `/* */` and `//` comments blanked out, offsets preserved.

    Blanked rather than removed so that every offset into the result is still
    an offset into the original -- the API-path check answers "is this
    occurrence inside the routes table", and that question is meaningless once
    the text has moved. Prose is excluded because this file documents the
    endpoints it calls in its own docstrings, and a rule that could not tell a
    sentence about `/api/v1/config` from a call to it would be a rule that
    banned explaining the code.
    """
    out = list(js)
    index = 0
    quote = ""
    while index < len(js):
        character = js[index]
        if quote:
            # Inside a string literal nothing is a comment. Without this the
            # seeded probe for a protocol-relative URL -- a literal beginning
            # `//` -- blanks the rest of its own line, takes the closing quote
            # with it, and every literal after it in the file is parsed one
            # quote out of step. The scan still fired, for the wrong reason,
            # which is the shape of a check that has stopped measuring what it
            # names.
            if character == "\\":
                index += 2
                continue
            if character == quote:
                quote = ""
            index += 1
            continue
        if character in "\"'`":
            quote = character
            index += 1
            continue
        pair = js[index:index + 2]
        if pair == "/*":
            end = js.find("*/", index + 2)
            end = len(js) if end < 0 else end + 2
            for position in range(index, end):
                if out[position] != "\n":
                    out[position] = " "
            index = end
            continue
        if pair == "//":
            end = js.find("\n", index)
            end = len(js) if end < 0 else end
            for position in range(index, end):
                out[position] = " "
            index = end
            continue
        index += 1
    return "".join(out)


def strip_css_comments(css: str) -> str:
    """CSS with `/* */` blanked, offsets preserved. Same reason as above.

    The stylesheet's own header explains that it carries no `@import`, and a
    scan that could not tell that sentence from an import would make the file
    undocumentable.
    """
    return re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)),
                  css, flags=re.S)


def strip_html_comments(html: str) -> str:
    """Markup with `<!-- -->` blanked, offsets preserved."""
    return re.sub(r"<!--.*?-->", lambda m: re.sub(r"[^\n]", " ", m.group(0)),
                  html, flags=re.S)


def scannable(path: Path) -> str:
    """One file's text with its comments blanked out, whatever kind it is."""
    text = source(path)
    if path.suffix == ".css":
        return strip_css_comments(text)
    if path.suffix == ".html":
        return strip_html_comments(text)
    return strip_comments(text)


def block(js: str, declaration: str) -> tuple[int, int]:
    """The span of one top-level `const X = {...};`, as offsets into `js`."""
    start = js.index(declaration)
    depth = 0
    for position in range(start, len(js)):
        if js[position] == "{":
            depth += 1
        elif js[position] == "}":
            depth -= 1
            if depth == 0:
                return start, position + 1
    raise AssertionError(f"{declaration} is never closed")


def table(js: str, declaration: str) -> dict[str, str]:
    """A flat `const X = { a: "b", "c.d": "e" };` table as a dict.

    Both key spellings, because JavaScript allows both and the file uses both:
    an identifier where the key is one, a quoted string where it carries a dot.
    A parser that read only quoted keys returned an empty dict for
    `FORWARD_STATUS` and compared it, successfully, against nothing.
    """
    start, end = block(js, declaration)
    body = js[start:end]
    pattern = re.compile(r'(?:"((?:[^"\\]|\\.)*)"|([A-Za-z_$][\w$]*))'
                         r':\s*"((?:[^"\\]|\\.)*)"')
    # `or`, not `is not None`: `findall` hands back an empty string for a
    # group that did not participate, so the quoted branch is always truthy in
    # the wrong direction and every row came back keyed "".
    return {quoted or bare: value for quoted, bare, value in pattern.findall(body)}


def array(js: str, declaration: str) -> list[str]:
    """A flat `const X = ["a", "b"];` array as a list of its strings."""
    start = js.index(declaration)
    end = js.index("];", start)
    return re.findall(r'"([^"]*)"', js[start:end])


class TextByHook(HTMLParser):
    """The text of every element carrying `data-t`, keyed by the key it names.

    Elements are matched by attribute rather than by tag, and nesting is
    tracked, because the markup puts `data-t` on headings, buttons, spans and
    labels and a reader adding a fifth should not have to come back here.

    **One key may label several elements**: the picker and the
    scorecard share their column headers, and the empty picker's Credentials
    button is the top bar's. Each occurrence is collected on its own, so two
    that agree read as one text and two that differ read as both, which the
    comparison below then fails on.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.texts: dict[str, list[str]] = {}
        self._stack: list[tuple[str, int] | None] = []

    def handle_starttag(self, tag, attributes) -> None:
        if tag in ("meta", "link", "input", "br", "img", "hr"):
            return
        found = dict(attributes).get("data-t")
        if found is None:
            self._stack.append(None)
            return
        self.texts.setdefault(found, []).append("")
        self._stack.append((found, len(self.texts[found]) - 1))

    def handle_endtag(self, tag) -> None:
        if self._stack:
            self._stack.pop()

    def handle_data(self, data) -> None:
        for entry in self._stack:
            if entry is not None:
                key, at = entry
                self.texts[key][at] += data


def html_text_by_key(html: str) -> dict[str, str]:
    parser = TextByHook()
    parser.feed(html)
    out = {}
    for key, values in parser.texts.items():
        seen = []
        for value in values:
            text = " ".join(value.split())
            if text not in seen:
                seen.append(text)
        out[key] = " | ".join(seen)
    return out


# --------------------------------------------------------------------------
# the external-origin scan
# --------------------------------------------------------------------------

# What an off-box reference looks like, whatever the file type. `data:` is the
# one scheme that names no host and is the page's own inline icon; everything
# else is refused, including a protocol-relative `//host/path`, which is the
# spelling people reach for precisely because it does not say `https`.
OFF_BOX = re.compile(
    r"""(?:@import\s+|url\(\s*|src\s*=\s*|href\s*=\s*|["'(])\s*["']?"""
    r"""(?P<target>(?:[a-zA-Z][a-zA-Z0-9+.-]*:)?//[^"')\s>]+)""")

# Schemes that name nothing outside this process. `data:` carries its payload;
# `blob:` is this document's own object URL. Neither reaches a network.
INLINE_SCHEMES = ("data:", "blob:")


def off_box_hits(text: str) -> list[str]:
    """Every reference in markup or a stylesheet that would leave this machine."""
    hits = []
    for match in OFF_BOX.finditer(text):
        target = match.group("target")
        if any(target.startswith(scheme) for scheme in INLINE_SCHEMES):
            continue
        hits.append(target)
    for match in re.finditer(r"@import[^;\n]*", text):
        hits.append(match.group(0).strip())
    return sorted(set(hits))


# Every string literal in the script, in all three spellings.
JS_LITERAL = re.compile(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\''
                        r'|`((?:[^`\\]|\\.)*)`', re.S)


def off_box_hits_js(js: str) -> list[str]:
    """The same question of a script, asked of its string literals only.

    Not of the text. A protocol-relative URL begins `//`, which is also how a
    JavaScript line comment begins, so a scan over the whole file either has to
    strip comments first -- which deletes the probe along with them -- or has
    to read `// a note about fonts` as a reference to a host called `a`. Asking
    only the literals removes the ambiguity: a URL that is not in a literal is
    not a URL the page can fetch.
    """
    hits = []
    for match in JS_LITERAL.finditer(js):
        literal = next(group for group in match.groups() if group is not None)
        if not re.match(r"\A(?:[a-zA-Z][a-zA-Z0-9+.-]*:)?//", literal):
            continue
        if any(literal.startswith(scheme) for scheme in INLINE_SCHEMES):
            continue
        hits.append(literal)
    return sorted(set(hits))


def off_box(path: Path, text: str = None) -> list[str]:
    """One file's off-box references, asked the way its file type needs."""
    body = source(path) if text is None else text
    if path.suffix == ".js":
        return off_box_hits_js(body)
    return off_box_hits(scannable(path) if text is None else body)


def test_no_asset_reaches_off_this_machine() -> None:
    """No CDN, no font host, no analytics, in any of the three files.

    The rule is the product's, not this test's: a self-hosted merge tool that
    loads a script from somebody else's server has published the fact that it
    ran, and has handed that third party the ability to change what it does.
    """
    for path in (INDEX, APP_CSS, APP_JS):
        hits = off_box(path)
        check(not hits,
              f"{path.name} references {hits}, which is off this machine")


def test_the_off_box_scan_fires_on_each_of_the_three_shapes() -> None:
    """Seeded, one per file type, because a scan that never fired proves nothing.

    Three shapes rather than one: a `<script src>` in markup, an `@import` in a
    stylesheet and a URL in a string literal are three different ways for the
    same mistake to arrive, and a scan that catches only the first is a scan
    that passes over a stylesheet.
    """
    probes = {
        "a script tag": (INDEX, strip_html_comments(source(INDEX).replace(
            "<title>LLossless</title>",
            '<title>LLossless</title><script src="https://cdn.invalid/x.js"></script>'))),
        "a stylesheet import": (APP_CSS, strip_css_comments(
            '@import url("https://fonts.invalid/x.css");\n' + source(APP_CSS))),
        "a protocol-relative fetch": (APP_JS, source(APP_JS).replace(
            '  health: "/api/v1/health",',
            '  health: "//cdn.invalid/api/v1/health",')),
        "a font host in a literal": (APP_JS, source(APP_JS).replace(
            '  config: "/api/v1/config",',
            '  config: "https://fonts.invalid/css",')),
    }
    for what, (path, seeded) in probes.items():
        check(bool(off_box(path, seeded)),
              f"the off-box scan does not fire on {what}; it cannot catch what "
              f"it was built for")
    # And the other direction, on the real files, so the pattern is not simply
    # broad enough to fire on everything.
    for path in (INDEX, APP_CSS, APP_JS):
        check(not off_box(path),
              f"the off-box scan fires on the shipped {path.name}")


# --------------------------------------------------------------------------
# markup is never assigned
# --------------------------------------------------------------------------

# Every way a string becomes markup or code in a browser. `textContent` is the
# only channel this page uses and the only one that escapes by construction.
MARKUP_SINKS = ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write",
                "eval(", "new Function", "createContextualFragment")


def sink_hits(js: str) -> list[str]:
    return [sink for sink in MARKUP_SINKS if sink in js]


def test_the_script_never_assigns_markup() -> None:
    """No sink anywhere in `app.js`'s code, and one funnel for everything else.

    Two halves, and the second is what makes the first worth having. No sink
    means no value can become markup; **exactly one** `.textContent =`
    assignment in the whole file means every value that reaches the page goes
    through one function, `setText`, rather than through forty call sites that
    each have to be right. A reviewer checks one line instead of auditing a
    thousand.

    Comments are stripped first. This module's own docstrings name the sinks in
    order to explain the rule, and a scan that could not tell the explanation
    from the thing explained would forbid writing it down.
    """
    code = strip_comments(source(APP_JS))
    hits = sink_hits(code)
    check(not hits, f"app.js reaches for {hits}; every value goes through textContent")
    funnel = code.count(".textContent =")
    check(funnel == 1,
          f"{funnel} assignments to textContent; there is meant to be one, in "
          f"setText, so that every string reaching the page goes through it")


def test_the_markup_sink_scan_fires() -> None:
    """Seeded, because a list of forbidden words proves nothing until it fires."""
    seeded = strip_comments(source(APP_JS).replace(
        "function setText(target, text) {\n  target.textContent = text;",
        "function setText(target, text) {\n  target.innerHTML = text;"))
    check("innerHTML" in seeded, "the seeded probe did not take")
    check(bool(sink_hits(seeded)), "the markup-sink scan does not fire on innerHTML")
    check(strip_comments(source(APP_JS)).count(".textContent =") == 1
          and seeded.count(".textContent =") == 0,
          "removing the one textContent assignment does not fail the funnel check")


# --------------------------------------------------------------------------
# the four vocabularies
# --------------------------------------------------------------------------

def hooks_in_html() -> set[str]:
    return set(re.findall(r'data-cc="([^"]+)"', source(INDEX)))


# Every helper that turns a hook name into an element. Named rather than
# guessed: this is the set whose argument has to exist in the markup, and a
# rule that accepted any string literal as a hook would accept `"POST"`.
ACCESSORS = ("el", "clone", "input", "select", "openIf")


def hooks_in_js() -> set[str]:
    """Hooks the script looks up by name, through one of the accessors."""
    js = strip_comments(source(APP_JS))
    found = set(re.findall(r'\b(?:' + "|".join(ACCESSORS) + r')\(\s*"([^"]+)"', js))
    found |= set(re.findall(r'\bfind\([^,()]+,\s*"([^"]+)"\)', js))
    return found


def hooks_reachable_in_js() -> set[str]:
    """Every string literal in the script, for the other direction.

    A hook is dead when its name does not occur in the script at all. That is a
    weaker question than "is it passed to an accessor", and deliberately so:
    the accessor list above is a list, and a hook read through a helper nobody
    added to it would be reported as dead markup and deleted.
    """
    js = strip_comments(source(APP_JS))
    return set(re.findall(r'"((?:[^"\\\n]|\\.)*)"', js))


def test_every_hook_is_written_on_one_side_and_read_on_the_other() -> None:
    """`data-cc` parity, both ways.

    A hook in the markup that nothing reads is dead weight that reads like an
    interface. A hook the script looks up that the markup does not carry is an
    exception thrown inside one handler, which in a page this size means one
    button quietly stops working.
    """
    written, read = hooks_in_html(), hooks_in_js()
    check(len(written) >= 60,
          f"only {len(written)} hooks found in index.html; discovery has drifted")
    check(not (read - written),
          f"app.js looks up hooks the markup does not carry: {sorted(read - written)}")
    dead = sorted(written - read - hooks_reachable_in_js())
    check(not dead, f"index.html carries hooks nothing reads: {dead}")


def test_the_hook_parity_check_fires_in_both_directions() -> None:
    """Seeded both ways, because parity that only fails one way is half a check."""
    written, read = hooks_in_html(), hooks_in_js()
    check(bool((read | {"ghost-hook"}) - written),
          "a hook read and never written does not fail the parity check")
    check(bool((written | {"ghost-hook"}) - read - hooks_reachable_in_js()),
          "a hook written and never read does not fail the parity check")


def strings_table(tag: str = i18n.DEFAULT_TAG) -> dict[str, str]:
    """One catalogue's strings, off disk.

    This used to parse a `const STRINGS = {` table out of `app.js`. The table
    is now `web/locales/en.json` and there is a second file beside it, so the
    parse is a `json.loads` and the checks below run against every catalogue
    rather than against the one that happened to be compiled into the script.
    Keeping them pointed at the reference file alone would mean a German page
    could render a key where a sentence belongs and no check would notice.

    `read` rather than `load`: the file is wanted here as it is on disk, not as
    it would be served. Whether it validates is `tests/test_web_i18n.py`'s
    question and it reports the answer in one line; a `load` here would raise
    instead, and every check below would go from "de.json is missing
    run.submit" to a traceback that names none of them.
    """
    return i18n.read(tag)["strings"]


def catalogues() -> dict[str, dict[str, str]]:
    """Every catalogue this server can serve, keyed by tag."""
    return {tag: strings_table(tag) for tag in i18n.available()}


def keys_named_in_js() -> tuple[set[str], set[str]]:
    """Keys the script hands to `t` by name, and the prefixes it builds on.

    This is the half that answers "is there a string for everything rendered",
    so it has to be the *named* set rather than every literal in the file: a
    rule that counted every literal would count `"POST"` as a missing string.
    A literal ending in a dot is a family -- `t("kind." + finding.kind)` -- and
    is returned separately, because what can be checked about a family is that
    it has members, not that a particular one was named.
    """
    js = strip_comments(source(APP_JS))
    direct = set(re.findall(r'\bt\(\s*"((?:[^"\\]|\\.)*)"', js))
    start, end = block(js, "const CHIP_STATES = {")
    direct |= set(re.findall(r'key:\s*"([^"]+)"', js[start:end]))
    prefixes = {key for key in direct if key.endswith(".")}
    return direct - prefixes, prefixes


def keys_used_in_js() -> set[str]:
    """Every string key the script can render, however it reaches `t`.

    "Used" is "appears as a string literal in the script", not "appears inside
    a `t(...)` call". Three of the four ways this file names a key are indirect
    -- a literal in a row of the checks array, a literal in a ternary handed to
    `t`, a literal held in `CHIP_STATES` -- and a rule that only recognised the
    direct call would report two dozen live strings as dead and train the next
    reader to delete them.

    The prefix form is the fourth: `t("kind." + finding.kind)` names a family
    whose members are the reconciler's, so a literal ending in a dot marks
    every key under it as used.

    No part of the script is excluded any more. It used to skip the span of
    `const STRINGS = {`, because a table of keys mapped to sentences would
    otherwise have declared every one of its own keys used; the table is a
    JSON file now and the script holds nothing but the keys it renders.
    """
    js = strip_comments(source(APP_JS))
    literals = set(re.findall(r'"((?:[^"\\]|\\.)*)"', js))
    prefixes = {literal for literal in literals if literal.endswith(".")}
    used = set(literals)
    for key in strings_table():
        if any(key.startswith(prefix) for prefix in prefixes):
            used.add(key)
    return used


def catalogue_parity(tag: str, strings: dict[str, str]) -> list[str]:
    """Every way one catalogue and the page disagree, as messages. Empty is pass.

    A function rather than the body of a test because `tests/test_web_i18n.py`
    seeds catalogues through it -- a catalogue with a key removed, a catalogue
    with one added -- and a probe that re-implements the predicate it is
    probing proves only that the copy fires. The one predicate is here, beside
    the helpers that read the markup and the script; the live catalogues and
    the seeded ones go through the same call.
    """
    from_html = set(html_text_by_key(source(INDEX)))
    named, prefixes = keys_named_in_js()
    used = keys_used_in_js() | from_html
    problems = []
    if len(strings) < 100:
        problems.append(f"only {len(strings)} strings in {tag}.json; the parse "
                        f"has drifted")
    missing = sorted((named | from_html) - set(strings))
    if missing:
        problems.append(f"these keys are rendered and {tag}.json has no string "
                        f"for them: {missing}")
    for prefix in sorted(prefixes):
        if not any(key.startswith(prefix) for key in strings):
            problems.append(f"the script builds keys under {prefix!r} and "
                            f"{tag}.json has none")
    unused = sorted(set(strings) - used)
    if unused:
        problems.append(f"these strings are in {tag}.json and never rendered: "
                        f"{unused}")
    return problems


def test_every_string_is_in_the_table_and_the_table_is_all_used() -> None:
    """Every catalogue, reachable in both directions.

    A sentence built at a call site is a sentence no catalogue can ever reach,
    and a key in a catalogue that nothing renders is a line a translator is
    paid to translate twice. Both directions are asked of **each** catalogue
    rather than of the reference alone: `tests/test_web_i18n.py` holds the two
    files to the same key set, and this is the half of the question that file
    cannot answer, which is whether that shared key set is the set the page
    actually renders.
    """
    named, _ = keys_named_in_js()
    check(len(named) >= 20,
          f"only {len(named)} keys named directly; the parse has drifted")
    found = catalogues()
    check(len(found) >= 2,
          f"only {sorted(found)} found in web/locales/; the discovery has drifted")
    for tag, strings in sorted(found.items()):
        for problem in catalogue_parity(tag, strings):
            check(False, problem)


def test_the_markup_and_the_table_say_the_same_thing() -> None:
    """A `data-t` element's own text is the same sentence the table holds.

    The markup carries the text as well as the key so the page still reads with
    the script blocked, which makes it a second copy -- and a second copy of a
    sentence is a sentence that drifts. This is the check that they have not.

    Against the reference catalogue only, and that is the whole point of there
    being a reference: `index.html` is served in one language whatever the
    browser asks for, because it is fetched before anything has negotiated
    anything. English is the language it is in and `en.json` is the file that
    says what English is.
    """
    strings = strings_table()
    texts = html_text_by_key(source(INDEX))
    check(len(texts) >= 40,
          f"only {len(texts)} data-t elements parsed; discovery has drifted")
    for key, text in sorted(texts.items()):
        if key not in strings:
            continue
        want = strings[key].replace("\\\"", "\"")
        check(text == want,
              f"index.html says {text!r} for {key} and the table says {want!r}")


def test_the_markup_and_table_drift_check_fires() -> None:
    """Seeded: one word changed in the markup must fail the comparison."""
    strings = strings_table()
    texts = html_text_by_key(source(INDEX).replace(
        ">Merge and check<", ">Merge and inspect<"))
    key = "run.submit"
    check(key in strings and key in texts, "the probe's anchor has moved")
    check(texts.get(key) != strings.get(key),
          "a changed button label does not fail the markup/table comparison")
    # A key on two elements (still true after the picker was given its
    # own short column keys and left only "Model" shared): one of them
    # drifting must still fail.
    markup = source(INDEX)
    anchor = 'data-cc="picker-sort-name" data-sort="name" data-t="models.col.model">Model<'
    check(markup.count(anchor) == 1 and 'data-t="models.col.model"' in
          markup.replace(anchor, ""), "the repeated-key probe's anchor has moved")
    texts = html_text_by_key(markup.replace(
        anchor, 'data-cc="picker-sort-name" data-sort="name" data-t="models.col.model">Models<'))
    check(texts.get("models.col.model") != strings.get("models.col.model"),
          "one of two elements under one key drifting does not fail the comparison")
    check(html_text_by_key(markup).get("models.col.model") == strings.get("models.col.model"),
          "two elements under one key that agree must read as one text")


def test_the_event_kinds_are_the_server_s_own() -> None:
    """`EventSource` drops a named event with no listener, in silence.

    That makes an unsubscribed kind the one failure a progress stream must not
    have: the run carries on, the page shows nothing, and no error is raised
    anywhere. The kinds are not served by `/config`, so parity with
    `web/events.py` is the only thing that holds them together.
    """
    listed = set(array(source(APP_JS), "const EVENT_KINDS = ["))
    check(listed == set(events.KINDS),
          f"app.js listens for {sorted(listed)}; the server emits "
          f"{sorted(events.KINDS)}")


def test_the_status_words_are_the_report_s_own() -> None:
    """The claims table's status column is `report.py`'s vocabulary, not a synonym.

    The same finding means opposite things by direction -- `partially_dropped`
    is "partly kept" one way and nothing at all the other -- so the two
    are mirrored separately and asserted word for word. A synonym here would
    make the interface and the downloadable report disagree about what happened
    to the same claim.

    In two halves since the strings moved out of the script. `app.js` keeps the
    *membership* -- which findings each direction defines -- because that is
    not a sentence and does not translate; `en.json` keeps the words, under
    `status.forward.<finding>`. Both halves are pinned here, so the pair still
    fails as one thing when the report's vocabulary changes.

    """
    PAGE_PLAINER: dict[str, str] = {}
    js = source(APP_JS)
    strings = strings_table()
    for name, direction, wanted in (("FORWARD_FINDINGS", "forward",
                                     report.FORWARD_STATUS),
                                    ("REVERSE_FINDINGS", "reverse",
                                     report.REVERSE_STATUS)):
        listed = array(js, f"const {name} = [")
        check(listed == list(wanted),
              f"app.js's {name} is {listed}; report.py defines {list(wanted)}")
        for finding, word in wanted.items():
            key = f"status.{direction}.{finding}"
            expected = PAGE_PLAINER.get(key, word)
            check(strings.get(key) == expected,
                  f"en.json says {strings.get(key)!r} for {key} and the "
                  f"expected word is {expected!r}")
    check(strings.get("status.notchecked") == report.NOT_CHECKED,
          f"en.json says {strings.get('status.notchecked')!r} for "
          f"status.notchecked and report.py says {report.NOT_CHECKED!r}")


def test_every_finding_class_is_rendered_in_exactly_one_section() -> None:
    """The two sections partition the engine's findings, with nothing left over.

    A class in neither list renders nowhere: the merge produced a finding, the
    report carries it, and the page shows a clean section over it. A class in
    both renders twice and inflates the count beside the heading. The union and
    the disjointness are both asserted, against the engine's own tuples.
    """
    js = source(APP_JS)
    omitted = set(array(js, "const OMITTED_FINDINGS = ["))
    conflict = set(array(js, "const CONFLICT_FINDINGS = ["))
    check(omitted | conflict == set(report.FINDING_ORDER),
          f"the verdict findings rendered are {sorted(omitted | conflict)}; the "
          f"engine produces {sorted(report.FINDING_ORDER)}")
    check(not (omitted & conflict),
          f"these verdict findings render in both sections: {sorted(omitted & conflict)}")

    omitted_kinds = set(array(js, "const OMITTED_KINDS = ["))
    conflict_kinds = set(array(js, "const CONFLICT_KINDS = ["))
    check(omitted_kinds | conflict_kinds == set(reconcile.FINDING_KINDS),
          f"the structural kinds rendered are "
          f"{sorted(omitted_kinds | conflict_kinds)}; the reconciler produces "
          f"{sorted(reconcile.FINDING_KINDS)}")
    check(not (omitted_kinds & conflict_kinds),
          f"these structural kinds render in both sections: "
          f"{sorted(omitted_kinds & conflict_kinds)}")

    # The kinds with a section of their own, outside the partition.
    # `reconcile.MISATTRIBUTED` is deliberately not a `FINDING_KINDS` member,
    # so the union above cannot see it; this is where it is held to the page.
    own = array(js, "const ATTRIBUTION_KINDS = [")
    check(own == [reconcile.MISATTRIBUTED],
          f"the page's own-section kinds are {own}; the engine's is "
          f"{reconcile.MISATTRIBUTED!r}")
    check(not (set(own) & (omitted_kinds | conflict_kinds)),
          f"{sorted(set(own) & (omitted_kinds | conflict_kinds))} render in "
          f"their own section and in a partition")

    strings = strings_table()
    for kind in (*reconcile.FINDING_KINDS, reconcile.MISATTRIBUTED):
        check(f"kind.{kind}" in strings,
              f"{kind} has no label in the strings table and would render as its key")


def test_the_finding_partition_check_fires() -> None:
    """Seeded: a kind dropped from both lists must fail the union."""
    js = source(APP_JS)
    kinds = set(array(js, "const OMITTED_KINDS = [")) | set(
        array(js, "const CONFLICT_KINDS = ["))
    check(kinds == set(reconcile.FINDING_KINDS), "the probe's anchor has moved")
    dropped = kinds - {reconcile.FINDING_KINDS[0]}
    check(dropped != set(reconcile.FINDING_KINDS),
          "dropping a kind from both lists does not fail the partition check")


# --------------------------------------------------------------------------
# not checked is not clean
# --------------------------------------------------------------------------

def test_not_checked_reads_differently_from_checked_and_clean() -> None:
    """The distinction this project has got wrong more often than any other.

    An empty findings list under `ran: false` means nobody looked. The chip
    vocabulary has to keep that apart from a check that ran and found nothing,
    the words have to differ, and the colour has to differ too -- green over
    "not checked" is the failure, and green over nothing is no better, because
    this repository's own rule is that colour never carries meaning alone.
    """
    strings = strings_table()
    for key in ("chip.notchecked", "chip.clean", "section.notchecked"):
        check(key in strings, f"{key} is missing from the strings table")
    check(strings.get("chip.notchecked") != strings.get("chip.clean"),
          "a check that did not run and a check that found nothing say the same word")

    js = source(APP_JS)
    states = block(js, "const CHIP_STATES = {")
    body = js[states[0]:states[1]]
    for state in ("notchecked", "ungraded", "measured"):
        found = re.search(state + r":\s*\{\s*tone:\s*\"([^\"]*)\"", body)
        check(found is not None and found.group(1) == "",
              f"the {state} chip is given a colour; only a result may have one")
    found = re.search(r"clean:\s*\{\s*tone:\s*\"([^\"]*)\"", body)
    check(found is not None and found.group(1) == "ok",
          "the clean chip is not the ok colour")

    # And the rule is actually applied: the one function that decides a
    # section's chip must branch on `ran` before it looks at the count.
    start, end = block(js, "function sectionState(")
    decision = js[start:end]
    check("!ran ? \"notchecked\"" in decision,
          "sectionState no longer decides on `ran` before it counts findings")


def drive_adds_at_level(js: str, report: dict, levels: list) -> object:
    """The shipped `addsAtThisLevel` under node, over a fake `store.config`."""
    node = node_command()
    if node is None:
        return None
    body = js[js.index("function addsAtThisLevel("):]
    body = body[:body.index("\n}\n") + 3]
    program = ("const store = { config: { fidelity: { levels: "
               + json.dumps(levels) + " } } };\n" + body
               + "process.stdout.write(JSON.stringify(addsAtThisLevel("
               + json.dumps(report) + ")));")
    run = subprocess.run(node + ["-e", program], capture_output=True, text=True,
                         timeout=60, cwd=ROOT)
    return json.loads(run.stdout) if run.returncode == 0 else {"error": run.stderr[-300:]}


def test_a_check_that_does_not_apply_reads_differently_from_one_that_did_not_run() -> None:
    """`report.additions` is empty both when a level never asks the merge
    for one and when `open`/`sourced` asked and it declared none; the report
    alone cannot tell those two apart, so `addsAtThisLevel` reads `/config`'s
    own per-level `adds` flag (`merge.ADDS`, served by `api.fidelity_levels`)
    rather than a level's name, the rule every picker on this page follows.

    The distinction reaches the reader as a fourth chip, `notapplicable`,
    read apart from `notchecked`: the summary tile's "N did not run" must
    count a check that genuinely did not run and not one this level never
    asks for.
    """
    js = source(APP_JS)
    strings = strings_table()
    for key in ("chip.notapplicable", "check.additions.notapplicable"):
        check(key in strings, f"{key} is missing from the strings table")
    check(strings.get("chip.notapplicable") != strings.get("chip.notchecked"),
          "a check that does not apply here and one that did not run say the same word")
    states = block(js, "const CHIP_STATES = {")
    body = js[states[0]:states[1]]
    found = re.search(r"notapplicable:\s*\{\s*tone:\s*\"([^\"]*)\"", body)
    check(found is not None and found.group(1) == "",
          "the notapplicable chip is given a colour; only a result may have one")

    checks_body = js_function("renderChecks", js)
    check("addsAtThisLevel(report)" in checks_body
          and '!addsHere ? "notapplicable"' in checks_body,
          "renderChecks no longer reads addsAtThisLevel before choosing the "
          "additions row's chip")

    levels = [{"value": "high", "adds": False}, {"value": "open", "adds": True}]
    for fidelity, want in (("high", False), ("open", True), ("missing-level", True)):
        report = {"provenance": {"merge_policy": {"fidelity": fidelity}}}
        got = drive_adds_at_level(js, report, levels)
        if got is None:
            decline("UNMEASURED: no node here, so addsAtThisLevel was not driven")
            return
        check(got == want, f"addsAtThisLevel at {fidelity!r} reads {got!r}, want {want!r}")

    # Must-fire: a script that stops reading the served flag and falls back
    # to "always applicable" no longer tells `high` apart from `open`.
    seeded = js.replace("  return level ? Boolean(level.adds) : true;\n",
                        "  return true;\n", 1)
    check(seeded != js, "the probe for a script that ignores the served flag did not take")
    got = drive_adds_at_level(seeded, {"provenance": {"merge_policy": {"fidelity": "high"}}}, levels)
    check(got is not False, "addsAtThisLevel still reads false at high with the served flag ignored")


# --------------------------------------------------------------------------
# the two bounds on how many documents a merge may carry
# --------------------------------------------------------------------------

def body_of(js: str, declaration: str) -> str:
    """One function's source, braces balanced, from a comment-stripped script."""
    start, end = block(js, declaration)
    return js[start:end]


# Anything that reads like a document count. Used to ask the *file-wide*
# version of "neither bound is written down": a bare `2` is also an exit code
# and a `toFixed` argument, so the value alone cannot be banned, but a line
# that holds the value and talks about documents is the shape the ban is for.
COUNT_CONTEXT = re.compile(r"doc|pane", re.I)


def literal_bounds_in_document_context(js: str, bounds: list[int]) -> list[str]:
    """Lines that hold a bound as a bare number and are about documents."""
    hits = []
    for line in js.splitlines():
        if not COUNT_CONTEXT.search(line):
            continue
        for value in bounds:
            if re.search(r"(?<![\w.])" + str(value) + r"(?![\w.])", line):
                hits.append(line.strip())
    return hits


def test_the_document_bounds_are_the_server_s_and_are_written_down_nowhere() -> None:
    """`min_documents` and `max_documents` are read, never remembered.

    Both are `merge.MIN_SOURCES` and `merge.MAX_SOURCES`, served through
    `/api/v1/config`, and the page is the second enforcer rather than the
    first: the server refuses the same submission on its own. That makes a
    copy here worse than useless -- it would keep enforcing the old number
    after the server's changed, and the page would look right and be wrong.

    Three questions, because the copy could live in three places. The two
    accessors have to name the config path and hold no number but `0`, which
    is what they answer before `/config` arrives; the config path has to be
    read in exactly those two places; and no line anywhere in the file may
    hold either value as a bare number while talking about documents. The
    last one is the file-wide form, aimed rather than absolute, because `2` is
    also an exit code, a `toFixed` argument and a picker's option count in
    this same file and a blanket ban on the digit would be unmeetable.
    """
    js = strip_comments(source(APP_JS))
    with tempfile.TemporaryDirectory() as raw:
        built, thread = live(work=Path(raw) / "work")
        try:
            _, _, payload = request(origin(built) + "/api/v1/config")
            limits = json.loads(payload)["limits"]
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)

    check(limits.get("min_documents") == merge.MIN_SOURCES,
          f"/config serves min_documents {limits.get('min_documents')!r} and "
          f"merge.MIN_SOURCES is {merge.MIN_SOURCES!r}")
    check(limits.get("max_documents") == merge.MAX_SOURCES,
          f"/config serves max_documents {limits.get('max_documents')!r} and "
          f"merge.MAX_SOURCES is {merge.MAX_SOURCES!r}")
    # Without this the whole check could be satisfied by one number standing
    # for both bounds, which is the one arrangement under which hardcoding
    # either is undetectable.
    check(merge.MIN_SOURCES != merge.MAX_SOURCES,
          "the two bounds are the same number, so nothing below can tell a "
          "read of one from a copy of the other")

    for name, field in (("maxDocuments", "max_documents"),
                        ("minDocuments", "min_documents")):
        found = body_of(js, f"function {name}(")
        check(f"store.config.limits.{field}" in found,
              f"{name} does not read store.config.limits.{field}")
        numbers = re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])", found)
        check(numbers == ["0"],
              f"{name} holds the number(s) {numbers}; the only number it may "
              f"hold is the 0 it answers before /config has arrived")
        check(js.count(f"limits.{field}") == 1,
              f"limits.{field} is read in {js.count(f'limits.{field}')} places; "
              f"{name} is meant to be the only one")

    stray = literal_bounds_in_document_context(
        js, [merge.MIN_SOURCES, merge.MAX_SOURCES])
    check(not stray,
          f"these lines hold a document bound as a bare number: {stray}")

    # And the guards go through the accessors rather than through a local.
    check("maxDocuments()" in body_of(js, "function addDocument("),
          "addDocument does not ask maxDocuments() before adding")
    check("minDocuments()" in body_of(js, "function removeDocument("),
          "removeDocument does not ask minDocuments() before removing")


def test_the_hardcoded_bound_check_fires() -> None:
    """Seeded three ways, one per place a copy of a bound could hide."""
    js = strip_comments(source(APP_JS))
    bounds = [merge.MIN_SOURCES, merge.MAX_SOURCES]

    # 1. the fallback these two accessors used to carry.
    seeded = js.replace("store.config.limits.min_documents) || 0;",
                        f"store.config.limits.min_documents) || {merge.MIN_SOURCES};")
    check(seeded != js, "the fallback probe's anchor has moved")
    numbers = re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])",
                         body_of(seeded, "function minDocuments("))
    check(numbers != ["0"],
          "a numeric fallback in minDocuments does not fail the accessor check")

    # 2. a second reader of the config path, which is how one copy becomes two.
    seeded = js.replace("function refreshIdleStatus() {",
                        "function refreshIdleStatus() {\n"
                        "  const floor = store.config.limits.min_documents;")
    check(seeded.count("limits.min_documents") == 2,
          "a second read of the config path is not counted")

    # 3. the bound written out at a call site that talks about documents.
    seeded = js.replace("if (store.docs.length >= maxDocuments()) {",
                        f"if (store.docs.length >= {merge.MAX_SOURCES}) {{")
    check(seeded != js, "the call-site probe's anchor has moved")
    check(bool(literal_bounds_in_document_context(seeded, bounds)),
          "a bound written out beside `store.docs.length` is not found")
    check(not literal_bounds_in_document_context(js, bounds),
          "the document-context scan fires on the shipped app.js")


def test_both_bounds_are_refused_with_a_reason_the_catalogue_holds() -> None:
    """Neither bound is enforced in silence, and neither reason is built here.

    A bound enforced by a disabled control is a control that looks broken: the
    press that would have asked "why not?" never reaches a handler, so the
    operator gets a greyed button and no sentence. Both controls stay
    clickable, are marked `aria-disabled` so a screen reader still says they
    are unavailable, and answer a press with the reason -- which is a catalogue
    string, named with the bound it hit, in every language this server serves.
    """
    js = strip_comments(source(APP_JS))
    for function, key, placeholder in (
            ("addDocument", "documents.refused.max", "{max}"),
            ("removeDocument", "documents.refused.min", "{min}")):
        found = body_of(js, f"function {function}(")
        check(f'refuse(t("{key}"' in found.replace("\n", " ").replace("  ", " ")
              or f'"{key}"' in found,
              f"{function} does not reach for {key} when it refuses")
        check("refuse(" in found,
              f"{function} refuses without writing a reason anywhere")
        for tag, strings in sorted(catalogues().items()):
            check(key in strings, f"{tag}.json has no string for {key}")
            check(placeholder in strings.get(key, ""),
                  f"{tag}.json's {key} does not name the bound it hit; it says "
                  f"{strings.get(key)!r}")

    # The refusal has somewhere to appear, and the next render takes it away
    # again so it never reads as a standing complaint.
    check('data-cc="doc-refusal"' in source(INDEX),
          "there is no element for a refusal to be written into")
    check('refuse("");' in body_of(js, "function renderDocuments("),
          "renderDocuments does not clear the last refusal")

    # `aria-disabled`, not `disabled`: the second swallows the press.
    for function in ("renderDocuments", "documentTab", "documentPane"):
        found = body_of(js, f"function {function}(")
        check(".disabled = " not in found,
              f"{function} disables a document control; a disabled button "
              f"cannot answer the press that asks why it is disabled")


def test_the_refusal_check_fires_on_a_silent_bound() -> None:
    """Seeded: a bound that returns without saying anything must be caught."""
    js = strip_comments(source(APP_JS))
    seeded = js.replace(
        '    refuse(t("documents.refused.min",\n'
        '             { min: minDocuments(), n: store.docs.length }));\n', "")
    check(seeded != js, "the silent-refusal probe's anchor has moved")
    check("refuse(" not in body_of(seeded, "function removeDocument("),
          "a removeDocument that refuses in silence still looks like it speaks")

    seeded = js.replace(
        '  addButton.setAttribute("aria-disabled",',
        '  addButton.disabled = store.docs.length >= maxDocuments();\n'
        '  addButton.setAttribute("aria-disabled",')
    check(seeded != js, "the disabled-button probe's anchor has moved")
    check(".disabled = " in body_of(seeded, "function renderDocuments("),
          "a control disabled back into silence is not caught")


def remove_hint_problems(js: str, tables: dict) -> list[str]:
    """The two remove controls speak about *fields*, not a count that used
    to conflate an empty pane with a document, and say so before the
    press as well as after it: a `title` set from the same catalogue string
    whenever the floor is hit."""
    found = []
    for fn, hook in (("documentTab", "close"), ("documentPane", "remove")):
        body = body_of(js, f"function {fn}(")
        if f'{hook}.title = t("documents.refused.min"' not in body:
            found.append(f"{fn} does not set a title from documents.refused.min "
                         f"when the floor is hit")
        if f'{hook}.removeAttribute("title")' not in body:
            found.append(f"{fn} does not clear the title once the floor is left")
    for tag, table in sorted(tables.items()):
        text = table.get("documents.refused.min", "")
        if re.search(r"\{n\}", text):
            found.append(f"{tag}: documents.refused.min still names a count "
                         f"of panes as though it were a count of documents: {text!r}")
    return found


def test_the_remove_hint_speaks_of_fields_and_reaches_the_pointer() -> None:
    """The operator: *"the remove control's hint speaks of panes"* --
    `documents.refused.min` used to open "A merge takes at least {min}
    documents and there are {n}", naming the pane count as if every pane held
    one. The sentence no longer counts anything; it just says the floor and
    that this one stays. Both remove controls (the tab's `x` and the pane's
    `Remove` button) now carry that sentence in `title` whenever they are at
    the floor, so hovering says why before a press finds out by being
    refused, and clear it the moment there is a pane to spare.
    """
    js = strip_comments(source(APP_JS))
    tables = catalogues()
    for problem in remove_hint_problems(js, tables):
        check(False, problem)


def test_the_remove_hint_check_fires() -> None:
    """Seeded: a title left unset at the floor, and the old panes-as-documents
    phrasing put back, must each be caught."""
    js = strip_comments(source(APP_JS))
    tables = catalogues()
    seeded = js.replace(
        'if (atFloor) close.title = t("documents.refused.min", { min: minDocuments() });\n'
        '  else close.removeAttribute("title");\n', "")
    check(seeded != js, "the tab-title probe's anchor has moved")
    check(bool(remove_hint_problems(seeded, tables)),
          "a tab remove control with no title at the floor is not caught")

    seeded_tables = {tag: dict(table) for tag, table in tables.items()}
    seeded_tables["en"]["documents.refused.min"] = (
        "A merge takes at least {min} documents and there are {n}, so this "
        "one stays.")
    check(bool(remove_hint_problems(js, seeded_tables)),
          "the old panes-as-documents phrasing is not caught")


# --------------------------------------------------------------------------
# which document the page opens on
# --------------------------------------------------------------------------

def test_the_page_opens_on_the_first_document() -> None:
    """Document 1, not the last one the seeding loop happened to make.

    `addDocument` opens the pane it just created, which is right for a click
    and wrong for `boot`'s loop: seeding up to `min_documents` left `active`
    pointing at the last pane, so a fresh page opened on document 2 and the
    operator's first paste went into their second source. The reset is
    asserted *between* the loop and the render, because before the loop it is
    overwritten and after the render it is too late.

    The subject is `start` rather than `boot` since the login gate arrived:
    `boot` now answers "is there a gate in front of this page" and `start` is
    everything behind it, called once at load and again after a sign-in. The
    mechanism moved with it, so this moved too -- a probe left aimed at `boot`
    would have gone on passing over a `boot` that no longer seeds anything.
    """
    js = strip_comments(source(APP_JS))
    adder = body_of(js, "function addDocument(")
    check("store.active = store.docs.length - 1;" in adder,
          "addDocument no longer opens the pane it made, so this check is "
          "aimed at a mechanism that has moved")

    boot = body_of(js, "async function start(")
    loop = boot.find("while (store.docs.length < minDocuments())")
    reset = boot.find("store.active = 0;")
    render = boot.find("renderDocuments();")
    check(loop >= 0, "start no longer seeds the panes; the probe has moved")
    check(reset >= 0, "start never resets the open pane to the first one")
    check(loop < reset < render,
          f"start's reset of the open pane is not between the seeding loop and "
          f"the render (loop {loop}, reset {reset}, render {render})")
    check(store_field_default(js, "active") == "0",
          "the store no longer starts on the first pane either")


def store_field_default(js: str, field: str) -> str:
    """One field's initial value in the `store` literal."""
    found = re.search(field + r":\s*([^,\n]+),", body_of(js, "const store = {"))
    return found.group(1).strip() if found else ""


def test_the_first_document_check_fires() -> None:
    """Seeded both ways: the reset removed, and the reset moved before the loop."""
    js = strip_comments(source(APP_JS))
    seeded = js.replace("  store.active = 0;\n  renderDocuments();\n"
                        "  void refreshHistory();", "  renderDocuments();\n"
                        "  void refreshHistory();")
    check(seeded != js, "the removal probe's anchor has moved")
    check(body_of(seeded, "async function start(").find("store.active = 0;") < 0,
          "a start with no reset still passes the check")

    moved = js.replace(
        "  while (store.docs.length < minDocuments()) addDocument();",
        "  store.active = 0;\n  while (store.docs.length < minDocuments()) addDocument();"
    ).replace("  store.active = 0;\n  renderDocuments();", "  renderDocuments();")
    boot = body_of(moved, "async function start(")
    check(moved != js, "the reordering probe's anchor has moved")
    check(not (boot.find("while (store.docs.length < minDocuments())")
               < boot.find("store.active = 0;")),
          "a reset that happens before the loop that undoes it still passes")


# --------------------------------------------------------------------------
# dropping files
# --------------------------------------------------------------------------

def test_a_drop_is_one_document_per_file_and_the_picker_takes_more_than_one() -> None:
    """Both paths hand `loadFiles` the whole set, in the order it arrived.

    The shipped page took `files[0]` from the `DataTransfer` and threw the
    rest away without a word: three files dropped produced one document, one
    file's text, and no explanation anywhere on the page.

    Asserted of the two call sites rather than of the loop, because the loop
    is not the part that was wrong -- there was no loop. The order is the
    second half: `DataTransfer.files` is the order the operator selected
    them, that order becomes document order, and `merge` defaults the base to
    the first document, so a `sort` anywhere on this path would change a
    merge's result and nothing on the page would say so.
    """
    js = strip_comments(source(APP_JS))
    pane = body_of(js, "function documentPane(")
    check("loadFiles(Array.from((transfer && transfer.files) || []), doc)" in pane,
          "the drop handler no longer hands the whole DataTransfer to loadFiles")
    check("files[0]" not in pane and "files && transfer.files[0]" not in pane,
          "the drop handler still reaches for one file out of the set")
    check("void loadFiles(chosen, doc);" in pane,
          "the file picker does not go through loadFiles")

    loader = body_of(js, "async function loadFiles(")
    check("for (const file of files) {" in loader,
          "loadFiles no longer walks every file it was given")
    for sorter in (".sort(", ".reverse(", "Array.prototype.sort"):
        check(sorter not in loader,
              f"loadFiles reorders the files with {sorter}; drop order is "
              f"document order and document order decides the base")

    markup = source(INDEX)
    check('<input type="file" multiple data-cc="doc-file"' in markup,
          "the pane's file picker does not accept more than one file, so the "
          "two ways of loading a document disagree")
    check('associate(find(pane, "file-label"), fileInput);' in pane,
          "the file picker has no label tied to it")


def test_the_one_document_per_file_check_fires_on_a_handler_that_takes_the_first() -> None:
    """Seeded: the bug this replaced, and a sort that changes the base."""
    js = strip_comments(source(APP_JS))
    seeded = js.replace(
        "    void loadFiles(Array.from((transfer && transfer.files) || []), doc);",
        "    const file = transfer && transfer.files && transfer.files[0];\n"
        "    if (file) void loadFiles([file], doc);")
    check(seeded != js, "the first-file probe's anchor has moved")
    check("files[0]" in body_of(seeded, "function documentPane("),
          "a drop handler that keeps only the first file is not caught")

    seeded = js.replace("  for (const file of files) {\n",
                        "  for (const file of files.slice().sort()) {\n")
    check(seeded != js, "the sort probe's anchor has moved")
    check(".sort(" in body_of(seeded, "async function loadFiles("),
          "a loadFiles that sorts the files it was handed is not caught")

    seeded = source(INDEX).replace('<input type="file" multiple data-cc="doc-file"',
                                   '<input type="file" data-cc="doc-file"')
    check('<input type="file" multiple data-cc="doc-file"' not in seeded,
          "a picker that went back to one file at a time is not caught")


def test_a_drop_never_writes_over_a_document_that_already_has_text() -> None:
    """Empty panes first, then new panes, and the one passed over is named.

    Filling an empty pane is obviously right and overwriting what somebody
    typed is obviously wrong, so the walk skips anything with text in it --
    including the pane the files were dropped on. That makes the placement
    surprising in exactly one case, which is why the pane that was skipped is
    named in the line under the documents rather than left to be noticed.
    """
    js = strip_comments(source(APP_JS))
    loader = body_of(js, "async function loadFiles(")
    check("while (at < store.docs.length && store.docs[at].text.trim()) {" in loader,
          "loadFiles no longer walks past documents that already have text")
    check("if (!skipped) skipped = paneLabel(at);" in loader,
          "a document that was passed over is not remembered, so nothing can "
          "say it was")
    check('refuse(t("documents.dropped.kept"' in loader.replace("\n", " ")
          or '"documents.dropped.kept"' in loader,
          "nothing reaches for the sentence that names the document it left alone")

    # The reason is written *after* the render, because the render's first act
    # is to clear the line it would be written into.
    render = loader.find("renderDocuments();")
    said = loader.find("if (problems.length) refuse(")
    check(render >= 0 and said > render,
          f"loadFiles writes its reason before the render that clears it "
          f"(render {render}, reason {said})")


def test_the_never_clobber_check_fires() -> None:
    """Seeded: a walk that stops skipping, and a reason written too early."""
    js = strip_comments(source(APP_JS))
    seeded = js.replace(
        "    while (at < store.docs.length && store.docs[at].text.trim()) {\n"
        "      if (!skipped) skipped = paneLabel(at);\n"
        "      at += 1;\n"
        "    }\n", "")
    check(seeded != js, "the clobber probe's anchor has moved")
    check("text.trim()" not in body_of(seeded, "async function loadFiles("),
          "a loadFiles that writes over whatever is in the pane is not caught")

    # Spliced inside `loadFiles` and nowhere else: `renderDocuments();` appears
    # in six other functions, so a file-wide replace would have moved a line in
    # `addDocument` and left this function untouched -- and the probe would
    # then have passed on a `loadFiles` nobody seeded.
    live = body_of(js, "async function loadFiles(")
    moved = live.replace('  if (problems.length) refuse(problems.join(" "));\n', "")
    check(moved != live, "the ordering probe's anchor has moved")
    moved = moved.replace('  renderDocuments();\n',
                          '  if (problems.length) refuse(problems.join(" "));\n'
                          '  renderDocuments();\n', 1)
    loader = body_of(js.replace(live, moved), "async function loadFiles(")
    check('if (problems.length) refuse(' in loader,
          "the reordering probe lost the line it was moving")
    check(not (loader.find("renderDocuments();")
               < loader.find("if (problems.length) refuse(")),
          "a reason written before the render that erases it still passes")


def test_every_file_that_is_not_loaded_is_named_with_the_bound_it_hit() -> None:
    """Four ways to refuse a file, four sentences, and none of them silent.

    A user who drops ten files and gets four documents with no explanation has
    been lied to. Each refusal names the files by name and the bound by number,
    and the bounds are the server's -- `max_documents` and `max_body_bytes`
    out of `/api/v1/config`, never written down here.
    """
    js = strip_comments(source(APP_JS))
    loader = body_of(js, "async function loadFiles(")
    for key, placeholders in (("documents.dropped.kept", ("{name}",)),
                              ("documents.dropped.notext", ("{names}",)),
                              ("documents.dropped.toolarge", ("{names}", "{max}")),
                              ("documents.dropped.overmax", ("{names}", "{max}"))):
        check(f'"{key}"' in loader, f"loadFiles never reaches for {key}")
        for tag, strings in sorted(catalogues().items()):
            check(key in strings, f"{tag}.json has no string for {key}")
            for placeholder in placeholders:
                check(placeholder in strings.get(key, ""),
                      f"{tag}.json's {key} does not carry {placeholder}; it "
                      f"says {strings.get(key)!r}")
    check("max: maxDocuments()" in loader and "max: bytes" in loader,
          "the two bounds in the refusals are not the served ones")
    check("surplus.push(file.name)" in loader,
          "a file past the document ceiling is dropped rather than named")


def test_a_file_that_is_not_text_is_refused_rather_than_pasted() -> None:
    """`File.text()` decodes anything; a PDF arrives as a string of mojibake.

    The shipped page pasted it into the textarea and named the document after
    it, so the merge would have run on it. The test is by content and not by
    extension: a drop ignores the picker's `accept` list, and `.csv` or no
    extension at all is still text.
    """
    js = strip_comments(source(APP_JS))
    binary = body_of(js, "function looksBinary(")
    check('indexOf("\\u0000")' in binary,
          "looksBinary no longer looks for a NUL byte")
    check('indexOf("\\uFFFD")' in binary,
          "looksBinary no longer looks for the decoder's replacement character")
    loader = body_of(js, "async function loadFiles(")
    check("if (looksBinary(text)) { notext.push(name); continue; }" in loader,
          "loadFiles does not refuse a file that decoded to something that is "
          "not text")
    place = loader.find("store.docs[at].text = file.text;")
    refuse_at = loader.find("looksBinary(text)")
    check(refuse_at >= 0 and place > refuse_at,
          "a file is placed before anything asks whether it is text")


def test_the_binary_refusal_check_fires() -> None:
    """Seeded: a looksBinary that says everything is text."""
    js = strip_comments(source(APP_JS))
    seeded = js.replace(
        '  return text.indexOf("\\u0000") >= 0 || text.indexOf("\\uFFFD") >= 0;',
        "  return false;")
    check(seeded != js, "the mojibake probe's anchor has moved")
    check('indexOf("\\u0000")' not in body_of(seeded, "function looksBinary("),
          "a looksBinary that waves a PDF through is not caught")


# --------------------------------------------------------------------------
# the model table's colours
# --------------------------------------------------------------------------

def rank_scales() -> dict[str, dict[str, float]]:
    """`RANK_SCALES` out of the script, as numbers."""
    found = body_of(strip_comments(source(APP_JS)), "const RANK_SCALES = {")
    return {name: {"good": float(good), "poor": float(poor),
                   **({"poorInclusive": True} if inclusive else {}),
                   **({"ideal": float(ideal)} if ideal else {})}
            for name, good, poor, inclusive, ideal in re.findall(
                r"(\w+):\s*\{\s*good:\s*([\d.]+),\s*poor:\s*([\d.]+)"
                r"(?:,\s*poorInclusive:\s*(true))?"
                r"(?:,\s*ideal:\s*([\d.]+))?\s*\}", found)}


def band_of(value, scale: dict[str, float]) -> str:
    """The band `app.js`'s `band()` gives this value. Unmeasured is no band.

    `poorInclusive` puts the boundary value itself in poor rather
    than fair; every other scale keeps the plain `value > scale["poor"]` split.
    """
    if value is None:
        return ""
    if "ideal" in scale and value == scale["ideal"]:
        return "excellent"
    if value <= scale["good"]:
        return "good"
    poor_hit = value >= scale["poor"] if scale.get("poorInclusive") else value > scale["poor"]
    if poor_hit:
        return "poor"
    return "fair"


def catalogue_columns(models: list[dict]) -> dict[str, list]:
    """What each banded column actually holds, over the shipped catalogue.

    Two of the four are rates the catalogue does not publish as such. They are
    formed here the way the page forms them -- the count over that row's own
    `pairs` -- because the question this feeds is whether the bands have rows
    in them, and a band judged against the raw counts would be a band judged
    against a different quantity than the one the page colours.
    """
    columns: dict[str, list] = {name: [] for name in
                                ("usd_per_merge", "seconds_per_merge",
                                 "silent_loss_per_pair", "deviations_per_pair")}
    for entry in models:
        measured = entry.get("measured")
        if not measured:
            continue
        pairs = measured.get("pairs") or 0
        columns["usd_per_merge"].append(measured.get("usd_per_merge"))
        columns["seconds_per_merge"].append(measured.get("seconds_per_merge"))
        columns["deviations_per_pair"].append(measured.get("deviations_per_pair"))
        loss = measured.get("silent_loss")
        columns["silent_loss_per_pair"].append(
            loss / pairs if pairs and isinstance(loss, (int, float)) else None)
    return columns


# An operator ruling overrides occupancy for this one column: its bands are anchored to
# the mechanical-union floor, not fitted to where the catalogue's rows
# happen to sit, so an unoccupied band (`good`, at or under half the floor --
# every hosted row so far is worse than that) is not a defect to catch here.
FLOOR_ANCHORED = frozenset({"deviations_per_pair"})

# Removing `claude-opus-5` (retired, no longer credible on the card by
# operator ruling) took the only row over $0.50/merge with it. `RANK_SCALES`'
# usd_per_merge thresholds are deliberately round money, not fitted to the
# catalogue ("a scale fitted to this catalogue would move every time a row
# was added"), so this gap is left open rather than moved to force an
# occupant: it closes again the day a pricier hosted row is measured, the
# same kind of expected, documented gap carved out above, at one
# band's granularity since usd_per_merge's other two bands are still held.
# Pinned to the real, shipped threshold (not a bare column:band name) so a
# scale seeded away from it, a `poor` set somewhere nothing could ever
# reach, is still caught rather than swallowed by this exception.
REMOVED_ROW_GAP_POOR = 0.5


def empty_bands(scales: dict[str, dict[str, float]],
                columns: dict[str, list]) -> list[str]:
    """Every (column, band) pair the shipped catalogue never lands in."""
    missing = []
    for name, scale in sorted(scales.items()):
        if name in FLOOR_ANCHORED:
            continue
        seen = {band_of(value, scale) for value in columns.get(name, [])
                if value is not None}
        for wanted in ("good", "fair", "poor"):
            # Empty by construction, not by a threshold nobody reaches: the
            # one value at or under `good` is the ideal, which reads
            # "excellent". "excellent" itself is never required -- it
            # is the ideal, there for the day a row reaches it.
            if wanted == "good" and scale.get("ideal") == scale["good"]:
                continue
            pair = f"{name}:{wanted}"
            if (pair == "usd_per_merge:poor"
                    and scale.get("poor") == REMOVED_ROW_GAP_POOR):
                continue
            if wanted not in seen:
                missing.append(pair)
    return missing


def floor_anchored_problems(scale: dict[str, float], expected: dict[str, float]) -> list[str]:
    """The rule, checked rather than assumed: `poor` is exactly the union
    floor, inclusive; `good` is exactly half of it. `expected` comes from
    `rank_scale_floor.derive()`, the script that recomputes the floor from
    `lineup_figures.baselines` -- never a number typed in by hand here."""
    out = []
    if scale.get("poor") != expected["poor"]:
        out.append(f"poor is {scale.get('poor')}, the union floor is {expected['poor']}")
    if not scale.get("poorInclusive"):
        out.append("poor is not inclusive of the floor value itself")
    if scale.get("good") != expected["good"]:
        out.append(f"good is {scale.get('good')}, half the floor is {expected['good']}")
    return out


def test_every_band_of_every_scale_has_a_row_in_it() -> None:
    """The thresholds are chosen against the catalogue's real spread, except one.

    A band no model occupies is a colour the table can never show, which makes
    the legend under it describe a scale that is not the one being applied --
    and it is the shape a threshold takes when it was picked to look tidy
    rather than measured against the data. Every column but `deviations_per_pair`
    is asked of every band, in both directions: nothing empty, and nothing so
    wide that one band swallows the lot.

    An operator ruling (2026-09-28) overrides occupancy for `deviations_per_pair`: its
    bands are anchored to the mechanical-union floor, not fitted to the
    catalogue, and the shipped catalogue's `good` band is empty as of this
    writing (every hosted row so far is worse than half the floor) -- which is
    the anchoring working as intended, not a gap to fill. That column is held
    to the floor rule instead, checked against `rank_scale_floor.derive()`
    (the same arithmetic `tests/rank_scale_floor.py --check` runs).

    An operator ruling (2026-09-28) overrides occupancy for `usd_per_merge:poor` alone, and
    only at its real, shipped threshold ($0.50): removing `claude-opus-5`
    (retired, no longer credible on the card, by operator ruling) took the
    only row over it with it, and that threshold is deliberately not
    refitted to the catalogue's current spread (see `RANK_SCALES`' own
    comment). `test_the_empty_band_check_fires` below still proves a
    genuinely empty band, including a seeded `usd_per_merge.poor`, is caught.
    """
    scales = rank_scales()
    check(len(scales) == 4,
          f"{len(scales)} scales parsed out of RANK_SCALES; the parse has drifted")
    models = catalogue.models()
    columns = catalogue_columns(models)
    check(len(models) >= 4, f"only {len(models)} models in the catalogue")

    missing = empty_bands(scales, columns)
    check(not missing, f"these bands hold no row in the shipped catalogue: {missing}")

    expected = rank_scale_floor.derive()
    # Must-not-fire: the shipped scale, as parsed, matches the derived floor.
    check(not floor_anchored_problems(scales["deviations_per_pair"], expected),
          f"deviations_per_pair is not anchored to the union floor: "
          f"{floor_anchored_problems(scales['deviations_per_pair'], expected)}")
    # Must-fire: a scale whose poor has drifted off the floor is caught.
    seeded = dict(scales["deviations_per_pair"], poor=expected["poor"] + 1)
    check(floor_anchored_problems(seeded, expected),
          "a deviations_per_pair scale with poor off the union floor is not caught")
    seeded_good = dict(scales["deviations_per_pair"], good=expected["good"] + 1)
    check(floor_anchored_problems(seeded_good, expected),
          "a deviations_per_pair scale with good off half the union floor is not caught")
    seeded_incl = dict(scales["deviations_per_pair"])
    seeded_incl.pop("poorInclusive", None)
    check(floor_anchored_problems(seeded_incl, expected),
          "a deviations_per_pair scale with poor no longer inclusive is not caught")

    for name, scale in sorted(scales.items()):
        check(scale["good"] < scale["poor"],
              f"{name}'s bands overlap: good ends at {scale['good']} and fair "
              f"ends at {scale['poor']}")
        bands = [band_of(value, scale) for value in columns[name] if value is not None]
        check(len(set(bands)) > 1,
              f"every measured row lands in the same band on {name}, so the "
              f"colour says nothing")

    # The two rate columns, and the reason they are rates: the rows were not
    # measured over the same number of pairs, so a raw count is a count of
    # different things.
    pairs = {entry["measured"]["pairs"] for entry in models
             if entry.get("measured") and entry["measured"].get("pairs")}
    check(len(pairs) > 1,
          f"every catalogue row was measured over {pairs}, so this suite can no "
          f"longer tell a per-pair ranking from a raw one")


def test_the_deviations_floor_script_agrees_with_the_shipped_file() -> None:
    """`tests/rank_scale_floor.py --check` is the ruling-16 floor's own gate:
    it recomputes the union floor from `lineup_figures.baselines` and fails if
    `app.js` disagrees, so the number can drift only if this test is red.
    """
    run = subprocess.run([sys.executable, "tests/rank_scale_floor.py", "--check"],
                         cwd=ROOT, capture_output=True, text=True)
    check(run.returncode == 0,
          f"tests/rank_scale_floor.py --check exited {run.returncode}: "
          f"{run.stdout}{run.stderr}")


def node_command() -> list[str] | None:
    """How to run a line of JavaScript here, or None where nothing can."""
    for prefix in (["node"], ["flatpak-spawn", "--host", "node"]):
        try:
            probe = subprocess.run(prefix + ["-e", "process.stdout.write('ok')"],
                                   capture_output=True, timeout=60, cwd=ROOT)
        except (OSError, subprocess.SubprocessError):
            continue
        if probe.returncode == 0 and probe.stdout == b"ok":
            return prefix
    return None


def shipped_bands(js: str, probes: list[tuple[str, float]]) -> list[str] | None:
    """`band()` and `RANK_SCALES` as shipped, run under node over `probes`."""
    node = node_command()
    if node is None:
        return None
    start = js.index("function band(")
    band = js[start:js.index("\n}\n", start) + 3]
    scales = js[js.index("const RANK_SCALES = {"):]
    scales = scales[:scales.index("\n};\n") + 4]
    program = (band + scales + "process.stdout.write(JSON.stringify("
               + json.dumps(probes) + ".map(([c, v]) => band(v, RANK_SCALES[c]))));")
    run = subprocess.run(node + ["-e", program], capture_output=True, text=True,
                         timeout=60, cwd=ROOT)
    return json.loads(run.stdout) if run.returncode == 0 else [run.stderr[-200:]]


def test_the_excellent_band_is_the_ideal_alone() -> None:
    """The operator: a figure that scores perfect should not read "good".

    "excellent" is the band of a figure exactly at its column's ideal, and only
    the two rate columns have one: no silent loss, no deviation. Cost and speed
    have no ideal and never reach it. The boundaries are asked of the shipped
    `band()` under node: 0 is excellent, and the smallest positive value falls
    to the next band -- fair for silent loss, whose good band is the ideal
    alone, and good for deviations. An unmeasured figure stays uncoloured.
    """
    scales = rank_scales()
    check({name for name, scale in scales.items() if "ideal" in scale}
          == {"silent_loss_per_pair", "deviations_per_pair"},
          f"the columns with an ideal moved: {scales}")
    check(all(scale.get("ideal", 0) == 0 for scale in scales.values()),
          "an ideal other than zero; the two ideals are no loss and no deviation")
    tiny = 0.01
    want = [("silent_loss_per_pair", 0, "excellent"), ("silent_loss_per_pair", tiny, "fair"),
            ("deviations_per_pair", 0, "excellent"), ("deviations_per_pair", tiny, "good"),
            ("usd_per_merge", 0, "good"), ("seconds_per_merge", 0, "good")]
    for column, value, expected in want:
        check(band_of(value, scales[column]) == expected,
              f"band_of({value}) on {column} is {band_of(value, scales[column])!r}, "
              f"want {expected!r}")
    js = strip_comments(source(APP_JS))
    got = shipped_bands(js, [(c, v) for c, v, _ in want] + [("deviations_per_pair", None)])
    if got is None:
        print("  UNMEASURED: no node to run the shipped band() under; its Python "
              "mirror was checked instead")
    else:
        check(got == [e for _, _, e in want] + [""],
              f"the shipped band() gives {got}, want {[e for _, _, e in want] + ['']}")
        # Must-fire: the same program over a band() without the ideal line.
        seeded = js.replace('  if (scale.ideal !== undefined && value === scale.ideal) '
                            'return "excellent";\n', "")
        check(seeded != js and shipped_bands(seeded, [("deviations_per_pair", 0)]) == ["good"],
              "the probe cannot tell a band() with no ideal from the shipped one")
    for tag, strings in catalogues().items():
        word = strings.get("models.band.excellent", "")
        check(bool(word), f"{tag}.json has no models.band.excellent")
        check(word and strings.get("models.bands", "").count(word) >= 2,
              f"{tag}.json's band legend does not say which figures are {word!r}")
    css = source(STATIC / "app.css")
    check("td.rank-excellent" in css and "td.rank-excellent .rank-word" in css,
          "the excellent band has no colour class of its own, or no word colour")


def test_the_empty_band_check_fires() -> None:
    """Seeded: a threshold nothing reaches must be reported as an empty band."""
    scales = rank_scales()
    columns = catalogue_columns(catalogue.models())
    check(not empty_bands(scales, columns), "the shipped scales already leave a gap")
    widened = dict(scales)
    widened["usd_per_merge"] = {"good": scales["usd_per_merge"]["good"], "poor": 99.0}
    check("usd_per_merge:poor" in empty_bands(widened, columns),
          "a poor band no row reaches is not reported")
    narrowed = dict(scales)
    narrowed["seconds_per_merge"] = {"good": 0.0, "poor": 0.5}
    check("seconds_per_merge:good" in empty_bands(narrowed, columns),
          "a good band no row reaches is not reported")


def test_no_unmeasured_cell_is_coloured_and_every_colour_carries_a_word() -> None:
    """The two halves of this project's one rule about colour.

    An absent measurement gets no band, ever: shading a missing figure green
    or red is a judgement invented out of an absence, which is the failure
    class this repository repeats most and the reason the `notchecked` chip is
    neutral. And a band that has a colour also has a word, because a
    colour-only signal is nothing at all to a colourblind reader and nothing
    at all in print.

    Both are held by construction rather than by convention. `band()` answers
    `""` for anything that is not a finite number and `rankCell` paints
    nothing on `""`, so an unmeasured figure cannot reach a colour through any
    call site; and `rankCell` is the only writer of a `rank-` class and writes
    the word in the same three lines, so the two cannot be separated by an
    edit to one cell builder.
    """
    js = strip_comments(source(APP_JS))

    painted = js.count('classList.add("rank-')
    check(painted == 1,
          f"{painted} places write a rank class; there is meant to be one, in "
          f"rankCell, so that no colour can be applied without its word")
    painter = body_of(js, "function rankCell(")
    check('classList.add("rank-' in painter,
          "rankCell is no longer the function that writes the rank class")
    check('setText(word, t("models.band." + name));' in painter,
          "rankCell no longer writes the band's word beside its colour")
    check("if (!name) return;" in painter,
          "rankCell no longer refuses to paint a cell with no band")

    bander = body_of(js, "function band(")
    for guard in ('typeof value !== "number"', "!isFinite(value)", "!scale"):
        check(guard in bander,
              f"band() no longer answers no-band for {guard}")
    check(bander.count('return "";') == 3,
          f"band() has {bander.count('return ' + chr(34) * 2 + ';')} no-band "
          f"answers; three inputs have no band: not a number, not finite, and "
          f"no scale to measure against")

    for builder in ("measuredCell", "costCell", "silentLossCell", "deviationCell"):
        found = body_of(js, f"function {builder}(")
        check("models.unmeasured" in found,
              f"{builder} no longer renders the unmeasured case")
        check("unmeasured" in found.split("models.unmeasured")[0],
              f"{builder} says unmeasured without marking the cell as one")
        # The branch that says "unmeasured" has to leave before the one that
        # paints. Asked as "is there a return between the two" rather than by
        # reading the control flow, because what has to be true is that no
        # path from here reaches a colour, and a return is the only way out of
        # a cell builder.
        before_rank = found.split("rankCell(")[0]
        check("return cell;" in before_rank.split("models.unmeasured")[-1],
              f"{builder} can reach rankCell on its unmeasured path")

    for tag, strings in sorted(catalogues().items()):
        for name in ("good", "fair", "poor"):
            word = strings.get(f"models.band.{name}", "")
            check(bool(word.strip()),
                  f"{tag}.json has no word for models.band.{name}, so that band "
                  f"would render as a colour and a key")
        check(len({strings.get(f"models.band.{n}") for n in ("good", "fair", "poor")}) == 3,
              f"{tag}.json gives two bands the same word")

    # Nothing in the stylesheet paints a neutral cell either.
    css = strip_css_comments(source(APP_CSS))
    for neutral in ("unmeasured", "notpriced"):
        for rule in re.findall(r"([^{}]*\." + neutral + r"[^{}]*)\{([^}]*)\}", css):
            check("background" not in rule[1],
                  f"the .{neutral} rule `{rule[0].strip()}` gives a neutral cell "
                  f"a background; it is meant to look like the notchecked chip")


def test_the_colour_rules_fire() -> None:
    """Seeded four ways, one per way colour and meaning could come apart."""
    js = strip_comments(source(APP_JS))

    seeded = js.replace('  setText(word, t("models.band." + name));\n', "")
    check(seeded != js, "the wordless-colour probe's anchor has moved")
    check('setText(word, t("models.band." + name));'
          not in body_of(seeded, "function rankCell("),
          "a rankCell that paints without a word still passes")

    seeded = js.replace('function costCell(model) {\n'
                        '  const cell = document.createElement("td");',
                        'function costCell(model) {\n'
                        '  const cell = document.createElement("td");\n'
                        '  cell.classList.add("rank-good");')
    check(seeded != js, "the second-painter probe's anchor has moved")
    check(seeded.count('classList.add("rank-') == 2,
          "a second writer of a rank class is not counted")

    seeded = js.replace("function rankCell(cell, name) {\n  if (!name) return;",
                        "function rankCell(cell, name) {")
    check(seeded != js, "the missing-guard probe's anchor has moved")
    check("if (!name) return;" not in body_of(seeded, "function rankCell("),
          "a rankCell with no guard on the empty band still passes")

    seeded = js.replace('    cell.classList.add("unmeasured");\n'
                        '    setText(cell, t("models.unmeasured"));\n'
                        '    return cell;\n'
                        '  }\n'
                        '  const number = document.createElement("span");\n'
                        '  number.className = "mono";\n'
                        '  setText(number, value);\n'
                        '  cell.appendChild(number);\n'
                        '  const pairs = perPairDenominator(measured);',
                        '    cell.classList.add("unmeasured");\n'
                        '    setText(cell, t("models.unmeasured"));\n'
                        '  }\n'
                        '  const number = document.createElement("span");\n'
                        '  number.className = "mono";\n'
                        '  setText(number, value);\n'
                        '  cell.appendChild(number);\n'
                        '  const pairs = perPairDenominator(measured);')
    check(seeded != js, "the falling-through probe's anchor has moved")
    found = body_of(seeded, "function silentLossCell(")
    before_rank = found.split("rankCell(")[0]
    check("return cell;" not in before_rank.split('classList.add("unmeasured")')[1],
          "an unmeasured path that falls through into rankCell is not caught")

    css = strip_css_comments(source(APP_CSS)).replace(
        ".unmeasured, .notpriced {\n  color: var(--ink-soft);",
        ".unmeasured, .notpriced {\n  background: var(--ok-bg);\n  color: var(--ink-soft);")
    painted = [rule for rule in re.findall(r"([^{}]*\.unmeasured[^{}]*)\{([^}]*)\}", css)
               if "background" in rule[1]]
    check(bool(painted), "a background on the unmeasured cell is not caught")


def test_the_ranking_reads_the_rate_and_never_the_raw_count() -> None:
    """Deviations and silent loss are ranked per pair, never as totals.

    The catalogue's vendor rows were measured over nine pairs and its
    self-hosted rows over two and three, and each row's own `notes` say the raw
    `deviations` is not comparable across rows on its own. A column ranked on
    the raw number would therefore rank the sample size: 15 deviations over two
    pairs would read as better than 26 over nine, which is the wrong way round
    by a factor of two and a half.

    `deviations_per_pair` is published for exactly that reason and is what the
    page reads. `silent_loss` has one too: the renderer used to form that
    rate itself for a day, which put the arithmetic somewhere no Python test
    could reach and no `validate()` rule could check. It reads the published
    field now, and `catalogue.validate` refuses either rate that disagrees with
    its own numerator over `pairs`.

    The assertion is that neither raw count reaches a band, which is the
    property. The earlier version of this check asserted that `silentLossCell`
    *divides* -- it pinned the workaround, so it failed the moment the
    workaround was replaced by the better thing.
    """
    js = strip_comments(source(APP_JS))
    raw = [line.strip() for line in js.splitlines()
           if re.search(r"\.deviations(?!_per_pair)\b", line)]
    check(not raw, f"app.js reads the raw deviation count at: {raw}")
    check("measured.deviations_per_pair" in js,
          "app.js no longer reads deviations_per_pair at all")

    scales = rank_scales()
    check("deviations_per_pair" in scales and "deviations" not in scales,
          f"RANK_SCALES bands {sorted(scales)}; the deviations band has to be "
          f"the per-pair one")

    loss = body_of(js, "function silentLossCell(")
    check("measured.silent_loss_per_pair" in loss,
          "silentLossCell must band the published per-pair rate")
    banded = [line.strip() for line in loss.splitlines()
              if "band(" in line and re.search(r"silent_loss(?!_per_pair)\b", line)]
    check(not banded,
          f"silentLossCell bands the raw loss count at: {banded}; 19 over 9 "
          f"pairs must not rank below 10 over 3")
    check("RANK_SCALES.silent_loss_per_pair" in loss,
          "silentLossCell no longer bands on the per-pair scale")
    denominator = body_of(js, "function perPairDenominator(")
    check("pairs > 0 ? pairs : 0" in denominator,
          "a missing pair count no longer becomes 0, so a rate could be formed "
          "over an assumed denominator")

    # And the figures this depends on are really in the catalogue.
    for entry in catalogue.models():
        measured = entry.get("measured")
        if not measured:
            continue
        pairs, total = measured.get("pairs"), measured.get("deviations")
        rate = measured.get("deviations_per_pair")
        if not (pairs and isinstance(total, (int, float))
                and isinstance(rate, (int, float))):
            continue
        check(abs(total / pairs - rate) < 0.01,
              f"{entry['id']}'s deviations_per_pair is {rate} and "
              f"{total}/{pairs} is {total / pairs:.3f}")


def test_the_raw_count_check_fires() -> None:
    """Seeded: a cell that went back to the raw total must be found."""
    js = strip_comments(source(APP_JS))
    seeded = js.replace("measured.deviations_per_pair, 2)", "measured.deviations, 2)")
    check(seeded != js, "the raw-count probe's anchor has moved")
    check([line for line in seeded.splitlines()
           if re.search(r"\.deviations(?!_per_pair)\b", line)],
          "a read of the raw deviation count is not found")
    check(not [line for line in js.splitlines()
               if re.search(r"\.deviations(?!_per_pair)\b", line)],
          "the raw-count scan fires on the shipped app.js")

    seeded = js.replace("measured.silent_loss / pairs", "measured.silent_loss")
    check("measured.silent_loss / pairs" not in body_of(seeded, "function silentLossCell("),
          "a silent-loss band taken on the raw count is not caught")


def test_a_row_with_no_price_reads_as_metered_and_never_as_free() -> None:
    """`usd_per_merge: null` on a self-hosted row is a third state, not a zero.

    `catalogue.py` states the rule it comes from: that hardware bills per
    minute of wall-clock GPU time rather than per token, so there is no
    per-merge dollar figure to attribute without assuming a utilisation rate
    nobody knows. The page has to keep three things apart in one column -- a
    price, a price nobody measured, and a row with no price to measure -- and
    the third is the one that inverts a cost comparison if it renders as
    `$0.000` or as a green cell.
    """
    js = strip_comments(source(APP_JS))
    found = body_of(js, "function costCell(")
    check("SELF_HOSTED" in found,
          "costCell no longer asks whether the row is one of the metered ones")
    check('t(metered ? "models.notpriced" : "models.unmeasured")' in found,
          "costCell no longer says which of the two absences this is")
    before_rank = found.split("rankCell(")[0]
    check("return cell;" in before_rank.split("metered ?")[-1],
          "costCell can reach rankCell on a row that has no price")

    for tag, strings in sorted(catalogues().items()):
        word = strings.get("models.notpriced", "")
        check(bool(word.strip()), f"{tag}.json has no string for models.notpriced")
        check(word != strings.get("models.unmeasured"),
              f"{tag}.json gives the same word to a row nobody measured and a "
              f"row there is no price for")
        check("0" not in word and "free" not in word.lower(),
              f"{tag}.json's models.notpriced is {word!r}, which reads as a price")
        check(bool(strings.get("models.notpriced.note", "").strip()),
              f"{tag}.json has no sentence saying why that cell is empty")

    # The assumption the branch rests on, asked of the shipped catalogue: the
    # rows with no price are exactly the self-hosted ones.
    self_hosted = re.search(r'const SELF_HOSTED = "([^"]+)";', js)
    check(self_hosted is not None, "SELF_HOSTED is no longer a named constant")
    name = self_hosted.group(1) if self_hosted else ""
    priced, metered = 0, 0
    for entry in catalogue.models():
        measured = entry.get("measured")
        if not measured:
            continue
        if entry.get("provider") == name:
            metered += 1
            check(measured.get("usd_per_merge") is None,
                  f"{entry['id']} is {name} and carries a per-merge price; "
                  f"catalogue.py says that row never gets one")
        elif measured.get("billed") == "free-tier":
            # A vendor's free tier: measured, billed nothing, and
            # rendered as its own word by costCell's first branch.
            check(measured.get("usd_per_merge") is None,
                  f"{entry['id']} is billed on a free tier and carries a price")
        else:
            priced += 1
            check(isinstance(measured.get("usd_per_merge"), (int, float)),
                  f"{entry['id']} is measured, is not {name}, and has no price, "
                  f"so costCell would call it unmeasured")
    check(metered > 0 and priced > 0,
          f"the catalogue holds {metered} metered and {priced} priced rows; both "
          f"branches of costCell need a row to be exercised by")


def test_the_metered_price_check_fires() -> None:
    """Seeded both ways: a zero in the cell, and a metered row priced as free."""
    js = strip_comments(source(APP_JS))
    seeded = js.replace('t(metered ? "models.notpriced" : "models.unmeasured")',
                        't("models.unmeasured")')
    check(seeded != js, "the collapsed-state probe's anchor has moved")
    check('t(metered ? "models.notpriced" : "models.unmeasured")'
          not in body_of(seeded, "function costCell("),
          "a cost cell that stopped telling the two absences apart still passes")

    for word in ("$0.000", "free"):
        check("0" in word or "free" in word.lower(),
              f"the price-shaped probe {word!r} would not be caught as one")

    rows = [dict(entry) for entry in catalogue.models()]
    rows[-1] = json.loads(json.dumps(rows[-1]))
    rows[-1]["measured"]["usd_per_merge"] = 0.0
    bad = [entry["id"] for entry in rows
           if entry.get("provider") == "self-hosted" and entry.get("measured")
           and entry["measured"].get("usd_per_merge") is not None]
    check(bool(bad),
          "a self-hosted row given a per-merge price is not caught")


# --------------------------------------------------------------------------
# the palette
# --------------------------------------------------------------------------

def palette(css: str) -> tuple[dict[str, str], dict[str, str]]:
    """The light and dark custom properties of a stylesheet, as two dicts."""
    marker = "@media (prefers-color-scheme: dark)"
    head, _, tail = css.partition(marker)
    pattern = re.compile(r"--([a-z-]+):\s*([^;]+);")
    light = {name: value.strip() for name, value in pattern.findall(head)}
    dark = {name: value.strip() for name, value in pattern.findall(tail)}
    return light, dark


def test_the_app_and_the_report_share_one_palette() -> None:
    """Lifted, not re-picked. The two artefacts are one product.

    The operator works in this page and sends the downloadable report to
    somebody else; two palettes would make those two things look like two
    tools. The app is allowed its own additions -- the report has no
    interactive surface and therefore no accent -- but every property the
    report defines has to hold the same value here, in both schemes.
    """
    report_light, report_dark = palette(html_report.STYLE)
    app_light, app_dark = palette(source(APP_CSS))
    check(len(report_light) >= 12,
          f"only {len(report_light)} properties parsed out of html_report.STYLE")
    for name, value in sorted(report_light.items()):
        check(app_light.get(name) == value,
              f"--{name} is {app_light.get(name)!r} in app.css and {value!r} in "
              f"the report, in the light scheme")
    for name, value in sorted(report_dark.items()):
        check(app_dark.get(name) == value,
              f"--{name} is {app_dark.get(name)!r} in app.css and {value!r} in "
              f"the report, in the dark scheme")


def test_the_palette_check_fires_on_a_drifted_value() -> None:
    """Seeded: one changed hex must fail the comparison."""
    report_light, _ = palette(html_report.STYLE)
    app_light, _ = palette(source(APP_CSS).replace("--ok: #1f7a3d;", "--ok: #00ff00;"))
    check(app_light.get("ok") != report_light.get("ok"),
          "a drifted palette value does not fail the comparison")


# --------------------------------------------------------------------------
# the readiness line
# --------------------------------------------------------------------------

# What the status line used to say about empty panes and the word it put in
# front of it. "ready" in front of "2 of the panes still have no text in them"
# was not true, and "of the panes" read as a count of something required.
OLD_READINESS = ("still have no text", "still has no text", "of the panes",
                 "Paste or upload at least")


def phrase_in_shipped_files(phrase: str) -> list[str]:
    """Every shipped file under `web/` that carries this phrase.

    The whole tree rather than the one catalogue, because a sentence in this
    page lives in up to three places -- the catalogue, the markup's no-script
    copy, and any string the script still builds at a call site -- and a fix
    applied to one of them leaves the other two saying the old thing.
    """
    root = ROOT / "src" / "llossless" / "web"
    found = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in (".json", ".html", ".js", ".py"):
            continue
        if phrase in path.read_text(encoding="utf-8"):
            found.append(str(path.relative_to(ROOT)))
    return found


READINESS_DRIVE = r"""
;(() => {
  if (!El.prototype.addEventListener) El.prototype.addEventListener = function () {};
  const out = {};
  for (const [tag, table] of Object.entries(INPUT.strings)) {
    strings = table;
    locale.tag = tag;
    store.config = INPUT.config;
    store.mergeModel = INPUT.model; store.checkModel = INPUT.model; store.splitRoles = false;
    const doc = (name, text) => ({ name, text });
    const cases = {
      none: [doc("", ""), doc("", "")],
      second: [doc("", "text"), doc("", "")],
      named: [doc("a.md", "text"), doc("b.md", " "), doc("", "")],
      ready: [doc("", "text"), doc("", "more text"), doc("c.md", "and more")],
    };
    out[tag] = {};
    for (const [name, docs] of Object.entries(cases)) {
      store.docs = docs;
      store.runId = "";
      refreshIdleStatus();
      out[tag][name] = { answer: readiness(), word: hooks["status-word"].textContent,
                         tone: hooks["status"].attributes["data-state"] || hooks["status"].className || "",
                         disabled: Boolean(hooks["submit"].disabled) };
    }
  }
  process.stdout.write(JSON.stringify(out));
})();
"""


def drive_readiness(js: str) -> dict | None:
    """The shipped `readiness` and `refreshIdleStatus`, in both languages."""
    node = node_command()
    if node is None:
        return None
    payload = served_config_with_routes()
    # A served command route: reachable, with a window, so only the
    # documents decide.
    model = "command:" + payload["commands"]["routes"][0]["id"]
    program = (EFFORT_DOM + "\nconst INPUT = " + json.dumps(
        {"strings": catalogues(), "config": payload, "model": model}) + ";\n" + js + READINESS_DRIVE)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
        handle.write(program)
        path = handle.name
    try:
        run = subprocess.run(node + [path], capture_output=True, text=True, timeout=120, cwd=ROOT)
    finally:
        os.unlink(path)
    if run.returncode != 0:
        return {"error": run.stderr[-600:]}
    return json.loads(run.stdout)


def readiness_problems(driven: dict | None, tables: dict) -> list[str]:
    """What the readiness line must say, per case and language."""
    if driven is None:
        return []
    if "error" in driven:
        return [f"readiness did not run under node: {driven['error']}"]
    found = []
    for tag, table in sorted(tables.items()):
        at = driven.get(tag) or {}
        untitled = table["documents.untitled"]
        want = {
            "none": (False, table["status.needdocs"].replace("{min}", "2")),
            "second": (False, table["status.empty.one"].replace(
                "{name}", untitled.replace("{n}", "2"))),
            "named": (False, table["status.empty.many"].replace(
                "{names}", "b.md " + table["word.and"] + " " + untitled.replace("{n}", "3"))),
            "ready": (True, table["status.ready"].replace("{n}", "3")),
        }
        for case, (ready, text) in want.items():
            got = at.get(case) or {}
            answer = got.get("answer") or {}
            if answer.get("ready") is not ready or answer.get("text") != text:
                found.append(f"{tag} {case}: readiness is {answer}, not {ready} {text!r}")
            word = table["word.ready" if ready else "word.notready"]
            if got.get("word") != word:
                found.append(f"{tag} {case}: the status word is {got.get('word')!r}, not {word!r}")
            if got.get("disabled") is ready:
                found.append(f"{tag} {case}: the submit button is "
                             f"{'disabled' if ready else 'enabled'}")
    return found


def test_the_readiness_line_says_what_is_missing_in_both_languages() -> None:
    """The phrase "more input needed" and the sentence that says what, or "ready".

    Driven under node through the shipped `refreshIdleStatus`, over no text,
    one empty untitled pane, two empty panes (one named), and three with text,
    in English and German. Must-fire: an empty pane that reads ready, and the
    two words swapped, are each caught; and none of the old wording is
    shipped anywhere under `web/`.
    """
    tables = catalogues()
    js = source(APP_JS)
    driven = drive_readiness(js)
    if driven is None:
        decline("UNMEASURED: no node here, so the readiness line was not driven")
        return
    for problem in readiness_problems(driven, tables):
        check(False, problem)
    for phrase in OLD_READINESS:
        stale = phrase_in_shipped_files(phrase)
        check(not stale, f"{phrase!r} is still shipped in {stale}")
    body = strip_comments(js)
    check('say(state.ready ? "ok" : "warn",' in body_of(body, "function refreshIdleStatus("),
          "refreshIdleStatus no longer colours the line green when ready and amber when not")
    seeds = {
        "an empty pane that reads ready":
            js.replace("  if (empty.length === 1) {\n    return { ready: false,",
                       "  if (empty.length === 1) {\n    return { ready: true,"),
        "the two words swapped":
            js.replace('t(state.ready ? "word.ready" : "word.notready")',
                       't(state.ready ? "word.notready" : "word.ready")'),
    }
    for what, seeded in seeds.items():
        check(seeded != js, f"the seed {what!r} did not change the script")
        check(bool(readiness_problems(drive_readiness(seeded), tables)),
              f"the readiness check did not fire on {what}")


def test_an_untitled_document_follows_the_language_and_keeps_the_base() -> None:
    """The count "document 2" becomes "Dokument 2" on a language change, because the
    readiness line names it; a typed name is left alone, and the base moves
    with the rename. Must-fire: the base left behind, and every name renamed."""
    def problems(js: str) -> list[str]:
        body = body_of(strip_comments(js), "async function changeLocale(")
        found = []
        if "if (!numbered[index]) return;" not in body:
            found.append("changeLocale renames documents nobody left untitled")
        if "if (store.base === doc.name) store.base = renamed;" not in body:
            found.append("changeLocale renames the base document without moving the base")
        if body.find("doc.name = renamed;") < body.find("await loadLocale(tag);"):
            found.append("the rename happens before the new catalogue is loaded")
        return found
    js = source(APP_JS)
    for problem in problems(js):
        check(False, problem)
    seeded = js.replace("    if (store.base === doc.name) store.base = renamed;\n", "")
    check(seeded != js and bool(problems(seeded)), "a base left behind by the rename is not caught")
    seeded = js.replace("    if (!numbered[index]) return;\n", "")
    check(seeded != js and bool(problems(seeded)), "renaming typed names is not caught")


DOCUMENT_COUNT_PLACEHOLDERS = {
    "documents.count.none": ("{min}", "{max}"),
    "documents.count.one": ("{n}", "{min}"),
    "documents.count.some": ("{n}", "{min}"),
    "documents.count.ready": ("{n}", "{max}"),
}


def document_count_phrasing_problems(tables: dict) -> list[str]:
    """Each count sentence, in every catalogue: named to a real string,
    never "n of a required total", carrying the values its own state
    needs and no others."""
    found = []
    for tag, table in sorted(tables.items()):
        for key, wanted in DOCUMENT_COUNT_PLACEHOLDERS.items():
            text = table.get(key, "")
            if not text:
                found.append(f"{tag}: no string for {key}")
                continue
            if re.search(r"\{n\} (of|von) \{max\}", text):
                found.append(f"{tag}: {key} reads as n of a required total: {text!r}")
            for piece in wanted:
                if piece not in text:
                    found.append(f"{tag}: {key} has no {piece}")
    return found


def count_wiring_problems(js: str) -> list[str]:
    """`renderDocTotal` counts documents with text and picks its sentence by
    that count, not by how many panes are open, and both `renderDocuments`
    and the text-input handler call it -- the count has to move as soon as
    an operator types, not only when a pane is added or removed."""
    found = []
    total = body_of(js, "function renderDocTotal(")
    if "store.docs.filter((doc) => doc.text.trim().length > 0).length" not in total:
        found.append("renderDocTotal does not count documents with text")
    if '"documents.count." + variant' not in total:
        found.append("renderDocTotal does not pick the count sentence by "
                      "how many documents have text")
    if "renderDocTotal();" not in body_of(js, "function renderDocuments("):
        found.append("renderDocuments no longer refreshes the document count")
    if "renderDocTotal();" not in body_of(js, "textArea.addEventListener(\"input\","):
        found.append("typing into a document no longer refreshes its count, "
                      "so the line goes stale until the next add or remove")
    return found


def test_the_document_count_matches_documents_with_text_not_panes() -> None:
    """A fresh page has two empty panes, and `documents.count`
    read "2 documents added (up to 12). A merge needs at least 2." over zero
    characters typed anywhere: true of the panes, not of what the operator had
    done. The operator: *"having a fresh page implies that there are already 2
    documents, when there are only 2 empty tabs."*

    One template becomes four, keyed by how many documents actually hold text:
    "none" and "some" are states the old wording never had reason to say anything about,
    and "ready" (two or more filled) no longer repeats "needs at least" --
    the readiness line already says what is missing, in its own words,
    whenever every pane is empty, and repeating it there was the other half
    of what read wrong.
    """
    js = strip_comments(source(APP_JS))
    for problem in count_wiring_problems(js):
        check(False, problem)

    tables = catalogues()
    for problem in document_count_phrasing_problems(tables):
        check(False, problem)

    seeded = {tag: dict(table) for tag, table in tables.items()}
    seeded["de"]["documents.count.ready"] = "{n} von {max} Dokumenten. Mindestens {min}."
    check(bool(document_count_phrasing_problems(seeded)),
          "the old German 'n of max' phrasing is not caught")
    seeded = {tag: dict(table) for tag, table in tables.items()}
    seeded["en"]["documents.count.ready"] = "{n} of {max} documents. A merge takes at least {min}."
    check(bool(document_count_phrasing_problems(seeded)),
          "the old English 'n of max' phrasing is not caught")


def test_the_document_count_wiring_check_fires() -> None:
    """Seeded: counting panes (`store.docs.length`) again, instead of
    documents with text, must be caught."""
    js = strip_comments(source(APP_JS))
    seeded = js.replace(
        "const filledCount = store.docs.filter((doc) => doc.text.trim().length > 0).length;",
        "const filledCount = store.docs.length;")
    check(seeded != js, "the filled-count probe's anchor has moved")
    check(bool(count_wiring_problems(seeded)), "counting panes again is not caught")


# --------------------------------------------------------------------------
# the API paths
# --------------------------------------------------------------------------

def routes() -> dict[str, str]:
    return table(source(APP_JS), "const ROUTES = {")


def test_no_api_path_is_written_outside_the_routes_table() -> None:
    """One table, so the set of paths is enumerable and therefore checkable.

    A path built at a call site cannot be listed, cannot be asked of a running
    server, and is discovered by an operator as a request that did nothing.
    Comments are excluded before the search: this file explains the endpoints
    it calls, and a rule that banned that would be a rule against documenting
    the code.
    """
    js = strip_comments(source(APP_JS))
    start, end = block(js, "const ROUTES = {")
    stray = [match.start() for match in re.finditer(r"/api/", js)
             if not start <= match.start() < end]
    check(not stray,
          f"{len(stray)} `/api/` path(s) are written outside the routes table, at "
          f"offsets {stray}")


def test_the_stray_path_check_fires() -> None:
    """Seeded: one path built at a call site must be found."""
    js = strip_comments(source(APP_JS)).replace(
        'async function refreshHealth() {',
        'async function refreshHealth() {\n  const x = "/api/v1/health";')
    start, end = block(js, "const ROUTES = {")
    stray = [match.start() for match in re.finditer(r"/api/", js)
             if not start <= match.start() < end]
    check(bool(stray), "a path written outside the table is not found")


# --------------------------------------------------------------------------
# a running server
# --------------------------------------------------------------------------

def live(environ=None, work=None):
    """A serving `Server` on an ephemeral port. Returns (server, thread, dir)."""
    built = server.build(port=0, work_dir=work, environ=environ or {})
    thread = server.background(built)
    return built, thread


def origin(built) -> str:
    return f"http://127.0.0.1:{built.server_address[1]}"


def request(url: str, *, method: str = "GET", payload=None, headers=None,
            timeout: float = PATIENCE):
    """One HTTP call. Returns (status, headers, bytes). Never raises on 4xx."""
    body = None
    sent = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        sent.setdefault("Content-Type", "application/json")
    call = urllib.request.Request(url, data=body, method=method, headers=sent)
    try:
        with urllib.request.urlopen(call, timeout=timeout) as answer:
            return answer.status, dict(answer.headers), answer.read(2 * 1024 * 1024)
    except urllib.error.HTTPError as refusal:
        return refusal.code, dict(refusal.headers), refusal.read(2 * 1024 * 1024)


def test_every_asset_is_served_with_the_right_type() -> None:
    """The three files, off a real server, by the paths the page names.

    Over a socket and not by reading the directory, because the thing being
    checked is the server's static route: an extension its table does not carry
    is not served at all, and a page whose stylesheet 404s renders as unstyled
    markup rather than as an error.
    """
    with tempfile.TemporaryDirectory() as raw:
        built, thread = live(work=Path(raw) / "work")
        try:
            base = origin(built)
            wanted = {
                "/": ("text/html; charset=utf-8", b"<!doctype html>"),
                "/index.html": ("text/html; charset=utf-8", b"<!doctype html>"),
                "/app.css": ("text/css; charset=utf-8", b"/* LLossless"),
                "/app.js": ("text/javascript; charset=utf-8", b"// @ts-check"),
            }
            for path, (content_type, opening) in wanted.items():
                status, headers, body = request(base + path)
                check(status == 200, f"{path} answered {status}")
                check(headers.get("Content-Type") == content_type,
                      f"{path} is served as {headers.get('Content-Type')!r}, "
                      f"not {content_type!r}")
                check(body.startswith(opening),
                      f"{path} does not begin {opening!r}")
            # And the file on disk is the file served, byte for byte. A build
            # step is exactly what this project does not have, and a served
            # asset that differs from its source is how one arrives by accident.
            for path, disk in (("/app.js", APP_JS), ("/app.css", APP_CSS),
                               ("/index.html", INDEX)):
                _, _, body = request(base + path)
                check(body == disk.read_bytes(),
                      f"{path} is not byte for byte the file in static/")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


def test_every_path_the_page_calls_is_a_path_the_server_routes() -> None:
    """Each entry in the routes table, asked of a real server.

    The assertion is against the refusal *code* rather than the status. A run
    id that does not exist and a path that does not exist are both 404s, and
    only the code tells them apart -- `no_route` is the failure being looked
    for and `no_run` is the correct answer to asking about a job nobody
    submitted. The two credential routes may not be mounted on an older server,
    so they are asserted either to route or to be handled: the page treats a
    404 there as "this server has no credential endpoint" and says so, which is
    a state rather than an error.
    """
    with tempfile.TemporaryDirectory() as raw:
        built, thread = live(work=Path(raw) / "work")
        try:
            base = origin(built)
            for name, template in sorted(routes().items()):
                path = (template.replace("{id}", "0" * 32)
                                .replace("{name}", "probe")
                                .replace("{tag}", "probe"))
                status, _, body = request(base + path)
                payload = json.loads(body) if body.startswith(b"{") else {}
                code = payload.get("error", {}).get("code", "")
                if name in ("keys", "key") and code == "no_route":
                    check("loadProviders" in source(APP_JS),
                          "the credential routes are unmounted and the page has no "
                          "path that handles their absence")
                    continue
                check(code != "no_route",
                      f"the page calls {path} and the server answers no_route")
                check(status in (200, 400, 404, 405),
                      f"{path} answered {status}, which the page does not expect")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


def test_the_page_cannot_frame_the_report_under_this_policy() -> None:
    """An `<iframe>` here would be blocked, silently, by the server's own policy.

    The report styles `body`, `main` and unscoped element selectors, so it has
    to be a document of its own rather than markup injected into this page --
    and a frame is the obvious way to do that. It does not work: the static
    policy is `default-src 'none'` with no `frame-src` and no `child-src`, so a
    frame falls back to `'none'` and never loads, and the report's own response
    carries `X-Frame-Options: DENY` besides. The page therefore opens the
    report in a tab.

    This check is the pin on that reasoning. If somebody adds a frame without
    the server change that would make it work, it fails here rather than in a
    browser showing an empty box.
    """
    with tempfile.TemporaryDirectory() as raw:
        built, thread = live(work=Path(raw) / "work")
        try:
            _, headers, _ = request(origin(built) + "/")
            policy = headers.get("Content-Security-Policy", "")
            framed = "frame-src" in policy or "child-src" in policy
            check("default-src 'none'" in policy,
                  f"the static policy is not default-src 'none': {policy!r}")
            if not framed:
                for path in (INDEX, APP_JS):
                    check("<iframe" not in source(path).lower(),
                          f"{path.name} frames a document under a policy with no "
                          f"frame-src; it will render empty. The server has to "
                          f"grant frame-src 'self' first.")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


def test_a_hostile_document_label_is_escaped_on_the_way_out() -> None:
    """One merge, labelled `<script>alert(1)</script>`, through a real server.

    Two assertions and the second is the one that matters here. The served
    report must carry the label escaped and not raw, which is
    `html_report.py`'s property and is re-checked because this page links
    straight to that artefact. And the JSON report must carry it **raw**: that
    is what the page consumes, so the page's own `textContent`-only rule is the
    only thing between a model-adjacent string and the DOM. A test that found
    the JSON pre-escaped would mean the page was being protected by somebody
    else and would stop meaning anything the day that changed.
    """
    with FakeEndpoint(Script(**CLEAN)) as endpoint, \
            tempfile.TemporaryDirectory() as raw:
        environ = {"LLOSSLESS_BASE_URL": endpoint,
                   "LLOSSLESS_STRUCTURED": "prompt"}
        built, thread = live(environ=environ, work=Path(raw) / "work")
        try:
            base = origin(built)
            status, _, body = request(base + "/api/v1/runs", method="POST", payload={
                "documents": [{"name": HOSTILE, "text": SOURCE_A},
                              {"name": "notes-b.md", "text": SOURCE_B}],
                "base": HOSTILE, "model": "test-model", "merge_model": "test-model",
            })
            check(status == 202, f"the hostile submission answered {status}")
            job_id = json.loads(body)["id"]

            deadline = time.time() + PATIENCE
            state, payload = "", {}
            while time.time() < deadline:
                _, _, raw_body = request(f"{base}/api/v1/runs/{job_id}")
                payload = json.loads(raw_body)
                state = payload.get("state", "")
                if state in ("done", "failed"):
                    break
                time.sleep(0.1)
            check(state == "done", f"the hostile run ended {state!r}: {payload.get('error')}")

            serialised = json.dumps(payload.get("report") or {})
            check(HOSTILE in serialised,
                  "the JSON report does not carry the label raw, so this check no "
                  "longer measures the page's own escaping")
            check(json.loads(serialised)["documents"].get("source_a.md") == HOSTILE,
                  "the label no longer arrives in the report's documents map, so "
                  "this probe is aimed at a field that has moved")

            status, _, page = request(f"{base}/api/v1/runs/{job_id}/report.html")
            check(status == 200, f"the report answered {status}")
            text = page.decode("utf-8")
            check(HOSTILE not in text,
                  "a document's script tag reached the served report unescaped")
            # It is not on the page escaped either: `html_report` renders the
            # canonical names rather than the operator's labels, so the label
            # never reaches that artefact at all. Asserted rather than assumed,
            # because the day it does start being rendered is the day the
            # escaping of *this* field starts mattering there too.
            check("alert(1)" not in text,
                  "the report has begun rendering document labels; the escaping "
                  "check above has to become a check that it escapes them")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


# --------------------------------------------------------------------------
# the type check
# --------------------------------------------------------------------------

def a_compiler() -> list[str] | None:
    """A TypeScript compiler this machine already has, or None. Never a download.

    Resolution order, and every step of it is offline: an explicit
    `LLOSSLESS_TSC`, a compiler inside the checkout, then `npx --offline`,
    which fails rather than fetching. The suite runs with no network and this
    check is not the place to introduce one; a machine with nothing cached
    declines instead of failing, because "there is no compiler here" is not the
    same answer as "the annotations are wrong".
    """
    explicit = os.environ.get("LLOSSLESS_TSC")
    if explicit:
        return [explicit]
    local = ROOT / "node_modules" / ".bin" / "tsc"
    if local.is_file():
        return [str(local)]
    for prefix in (["npx"], ["flatpak-spawn", "--host", "npx"]):
        try:
            probe = subprocess.run(prefix + ["--offline", "-p", "typescript", "tsc",
                                             "--version"],
                                   capture_output=True, timeout=180, cwd=ROOT)
        except (OSError, subprocess.SubprocessError):
            continue
        if probe.returncode == 0 and b"Version" in probe.stdout:
            return prefix + ["--offline", "-p", "typescript", "tsc"]
    return None


def test_the_script_type_checks() -> None:
    """`tsc --noEmit` over the annotated JavaScript, with zero errors.

    The shipped file is the written file: there is no build step, no compiled
    artefact and no `.ts` anywhere, because a self-hoster must need no
    toolchain to run this and this repository pins hashes specifically to stop
    a source and an output drifting apart. The types are JSDoc and the compiler
    is only ever a checker.

    `--target es2022` is on the command line rather than in a config file for
    the same reason: a `tsconfig.json` in the served directory would be a build
    artefact in the one place that must not have one. The default target is
    ES5, under which `Promise` is not declared and every `async` function in
    the file is an error about the target rather than about the code.
    """
    compiler = a_compiler()
    if compiler is None:
        decline("UNMEASURED: no offline TypeScript compiler on this machine, so "
                "app.js's annotations were not checked here. Set LLOSSLESS_TSC "
                "to one, or run `npx -p typescript tsc --noEmit --allowJs "
                "--checkJs --target es2022 src/llossless/web/static/app.js`.")
        return
    try:
        answer = subprocess.run(
            compiler + ["--noEmit", "--allowJs", "--checkJs", "--target", "es2022",
                        "src/llossless/web/static/app.js"],
            capture_output=True, timeout=600, cwd=ROOT)
    except (OSError, subprocess.SubprocessError) as problem:
        decline(f"UNMEASURED: the type check could not be run: {problem}")
        return
    output = (answer.stdout + answer.stderr).decode("utf-8", "replace").strip()
    check(answer.returncode == 0 and not output,
          f"tsc reports errors in app.js:\n{output}")


def test_the_type_check_is_a_check_and_not_a_formality() -> None:
    """The annotations are actually read: `@ts-check` is on the file.

    Without it `--checkJs` is the only thing switching the analysis on, and a
    future invocation that dropped the flag would type-check nothing while
    still exiting 0.
    """
    check(source(APP_JS).startswith("// @ts-check"),
          "app.js does not open with // @ts-check")


# --------------------------------------------------------------------------
# the picker: one radio, a wire name, a typed model, and what is reachable
# --------------------------------------------------------------------------

def test_one_radio_in_the_first_column_sets_both_roles() -> None:
    """The operator's complaint, pinned. Must fire and must not fire.

    Two radios per row asked the operator to make one decision twice -- "the
    user would expect not to click two option bullets to switch the model" --
    so the first column is one radio and its handler writes both roles. The
    second column exists only while the split is asked for.

    Checked against the source because there is no DOM here. Three properties,
    each of which would break silently: only one radio group is written
    unconditionally, the unconditional one writes `checkModel` as well as
    `mergeModel`, and the second group is behind `store.splitRoles`. The
    must-not-fire half is the split itself -- `checkCell` still exists and
    still writes `checkModel`, so this check cannot be satisfied by deleting
    the capability.
    """
    js = source(APP_JS)
    use = body_of(js, "function useCell(model, open)")
    check('radio.name = "model-use"' in use,
          "useCell no longer writes the single picker's radio group")
    check("store.mergeModel = model.id" in use and "store.checkModel = model.id" in use,
          "the first column's radio no longer sets both roles, which is the "
          "whole of what the operator asked for")
    check("store.splitRoles" in use.split("addEventListener")[1],
          "the first column sets the check role unconditionally; it must leave "
          "it alone once the operator has split the two")

    split = body_of(js, "function checkCell(model, open)")
    check("store.splitRoles" in split and 'radio.name = "model-check"' in split,
          "the per-role override is gone; splitting the two roles is a real "
          "capability and provenance.models reports both")
    check("cell.hidden = !store.splitRoles" in split,
          "the check column is rendered whether or not it was asked for")

    # Must not fire: the picker writes exactly two radio groups, one of which
    # only exists once the split has been asked for. Scoped to the `model-`
    # prefix because the fidelity and title-policy controls are radios too and
    # are not what this is about.
    groups = sorted(re.findall(r'radio\.name = "(model-[a-z]+)"', js))
    check(groups == ["model-check", "model-use"],
          f"the picker writes radio groups {groups}; it must write exactly the "
          f"one that sets both roles and the one behind the split")


def test_the_split_override_reaches_provenance_as_two_models() -> None:
    """One merge with two different models, and the report has to name both.

    The capability the single radio replaces is not deleted, it is moved
    behind a checkbox, and "moved" is only true if the two still arrive
    separately. `provenance.models` is where that is visible, so it is what is
    asserted rather than the request body.

    The must-not-fire half is the joined case in the same run: one model for
    both roles has to come back as one model in all three slots, or this check
    would pass on a server that ignored the merge model entirely.
    """
    with FakeEndpoint(Script(**CLEAN)) as endpoint, \
            tempfile.TemporaryDirectory() as raw:
        environ = {"LLOSSLESS_BASE_URL": endpoint,
                   "LLOSSLESS_STRUCTURED": "prompt"}
        built, thread = live(environ=environ, work=Path(raw) / "work")
        try:
            base = origin(built)
            split = finished(base, {"merge_model": "merge-model",
                                    "model": "check-model"})
            models = ((split.get("report") or {}).get("provenance") or {}).get("models") or {}
            check(models.get("merge") == "merge-model",
                  f"the merge role did not carry its own model: {models}")
            check(models.get("verify") == "check-model",
                  f"the check role did not carry its own model: {models}")

            joined = finished(base, {"merge_model": "one-model",
                                     "model": "one-model"})
            same = ((joined.get("report") or {}).get("provenance") or {}).get("models") or {}
            check(set(same.values()) == {"one-model"},
                  f"one model for both roles did not arrive as one: {same}")
        finally:
            shut(built, thread)


def test_the_picker_sends_the_wire_name_and_never_the_catalogue_id() -> None:
    """`claude-haiku-4-5` is a label; `claude-haiku-4-5-20251001` is the model.

    The two differ on four of the six shipped rows, and sending the id is what
    produced a run that failed two steps in on a model name the operator had
    never typed. `chosenModel` reads `api_model`, and the row's own monospace
    line shows the same string, so what is sent is what is displayed.

    Must not fire: at least one shipped row where the two genuinely differ, so
    a catalogue that quietly collapsed them could not make this vacuous.
    """
    js = source(APP_JS)
    chosen = body_of(js, "function chosenModel(role)")
    check("wireName(model)" in chosen,
          "the submitted model is no longer the row's wire name")
    wire = body_of(js, "function wireName(model)")
    check("model.api_model" in wire,
          "wireName no longer reads the catalogue's api_model field")
    # Both tables show it: the picker, where the row is chosen, and the
    # scorecard, where it is compared.
    for where in ("function pickerRow(", "function scorecardRow("):
        check("wireName(model)" in body_of(js, where),
              f"{where[9:-1]}: the row displays something other than the string that is sent")

    differ = [entry for entry in catalogue.models()
              if entry.get("api_model") != entry.get("id")]
    check(len(differ) >= 1,
          "no shipped row has a wire name that differs from its id, so this "
          "check proves nothing about which of the two is sent")


def test_a_typed_model_id_overrides_the_table_and_names_its_endpoint() -> None:
    """Quick and dirty, and it has to say where it is going.

    Two halves. The typed id reaches the request -- asserted through a real
    server, on the model the endpoint was actually asked for -- and the page
    names the endpoint it will be sent to, out of the catalogue rather than out
    of a sentence in this file.

    Must not fire: the same run with nothing typed sends the picked row
    instead, so a field that was ignored would fail here.
    """
    js = source(APP_JS)
    chosen = body_of(js, "function chosenModel(role)")
    check("typedId()" in chosen and "if (typed) return typed" in chosen,
          "a typed model id no longer overrides the picked row")
    render = body_of(js, "function renderCustomModel()")
    check('t("models.custom.active"' in render and "url: endpointLabel()" in render,
          "the page no longer names the endpoint a typed model is sent to")
    for key in ("models.custom.active", "models.custom.default"):
        for tag, strings in catalogues().items():
            check(key in strings, f"{tag}.json has no {key!r}")
            check("{url}" in strings[key],
                  f"{tag}.json's {key!r} does not carry the endpoint it names")

    with FakeEndpoint(Script(**CLEAN)) as endpoint, \
            tempfile.TemporaryDirectory() as raw:
        environ = {"LLOSSLESS_BASE_URL": endpoint,
                   "LLOSSLESS_STRUCTURED": "prompt"}
        built, thread = live(environ=environ, work=Path(raw) / "work")
        try:
            base = origin(built)
            typed = finished(base, {"merge_model": "qwen3:8b", "model": "qwen3:8b"})
            models = ((typed.get("report") or {}).get("provenance") or {}).get("models") or {}
            check(set(models.values()) == {"qwen3:8b"},
                  f"a typed model id did not reach the request: {models}")
        finally:
            shut(built, thread)


def test_a_model_with_no_endpoint_cannot_be_submitted() -> None:
    """Must fire on the server, must fire on the page, must not fire otherwise.

    A catalogue model is sent to the endpoint stored for its provider and to
    nowhere else, so a provider with no endpoint is a model with nowhere to go.
    The server refuses it at submit with a 400 naming the provider, and the
    page refuses to submit it at all -- the second is what stops the operator
    uploading two documents first.

    The must-not-fire half is the same request with the provider's endpoint
    configured: it has to be accepted, or the refusal would be a refusal of
    everything.
    """
    entry = next(model for model in catalogue.models() if model.get("provider"))
    wire, provider = entry["api_model"], entry["provider"]
    variable = credentials.url_env(provider)

    with FakeEndpoint(Script(**CLEAN)) as endpoint, \
            tempfile.TemporaryDirectory() as raw:
        built, thread = live(environ={"LLOSSLESS_BASE_URL": endpoint},
                             work=Path(raw) / "work")
        try:
            status, _, body = request(origin(built) + "/api/v1/runs", method="POST",
                                      payload=submission_for(wire))
            check(status == 400,
                  f"a model whose provider has no endpoint was accepted with "
                  f"{status}; it will fail two steps into the run instead")
            check(provider in body.decode("utf-8"),
                  f"the refusal does not name the provider: {body[:200]!r}")
        finally:
            shut(built, thread)

        built, thread = live(environ={"LLOSSLESS_BASE_URL": endpoint,
                                      variable: endpoint,
                                      "LLOSSLESS_STRUCTURED": "prompt"},
                             work=Path(raw) / "work2")
        try:
            status, _, body = request(origin(built) + "/api/v1/runs", method="POST",
                                      payload=submission_for(wire))
            check(status == 202,
                  f"the same model with {variable} set answered {status}; the "
                  f"refusal is refusing everything: {body[:200]!r}")
        finally:
            shut(built, thread)

    # And the page's half: the reason is a catalogue string, not a sentence
    # written into the script, so it is a refusal a German reader can read.
    js = source(APP_JS)
    blocked = body_of(js, "function unreachableChoice()")
    check('t("models.unreachable.blocked"' in blocked,
          "the page's refusal is not read out of the string catalogue")
    # Through `readiness`: a stranded choice is not ready, and the
    # button is disabled exactly when the line says not ready.
    check("if (stranded) return { ready: false, text: stranded };" in body_of(js, "function readiness()")
          and "button.disabled = !state.ready;" in body_of(js, "function refreshIdleStatus()"),
          "the submit button is not disabled for a model that cannot be reached")
    for tag, strings in catalogues().items():
        for key in ("models.unreachable", "models.unreachable.blocked"):
            check(key in strings, f"{tag}.json has no {key!r}")
        check("{provider}" in strings["models.unreachable"],
              f"{tag}.json's models.unreachable does not name the provider")


def test_an_unreachable_row_says_so_in_words_and_not_only_in_grey() -> None:
    """The house rule, applied to the one state this milestone adds.

    A row the server cannot reach is dimmed *and* carries its reason beside the
    name. Colour alone is not a signal here -- `rankCell` writes the band's
    word beside its colour and the chips do the same -- so an availability
    state that existed only as a class would be the first exception.

    Must fire: the reason is written through `setText` into the row.
    Must not fire: the class is still applied, so the check cannot be passed by
    deleting the styling and keeping the words.
    """
    # The scorecard's row: the picker lists no unreachable row at all.
    render = body_of(source(APP_JS), "function scorecardRow(")
    check('t("models.unreachable"' in render and "setText(why" in render,
          "an unreachable row no longer carries its reason in words")
    check('row.classList.add("unreachable")' in render,
          "the unreachable class is gone, so the words are all there is")
    css = source(STATIC / "app.css")
    check("tr.unreachable" in css,
          "app.css has no rule for an unreachable row, so the class does nothing")


def submission_for(model: str) -> dict:
    """A minimal two-document submit body naming one model for both roles."""
    return {"documents": [{"name": "a.md", "text": SOURCE_A},
                          {"name": "b.md", "text": SOURCE_B}],
            "merge_model": model, "model": model}


def finished(base: str, extra: dict) -> dict:
    """Submit one merge, wait for it, and return the final status payload."""
    body = {"documents": [{"name": "a.md", "text": SOURCE_A},
                          {"name": "b.md", "text": SOURCE_B}]}
    body.update(extra)
    status, _, raw_body = request(base + "/api/v1/runs", method="POST", payload=body)
    if status != 202:
        return {"state": f"refused {status}", "error": raw_body.decode("utf-8")}
    job_id = json.loads(raw_body)["id"]
    deadline = time.time() + PATIENCE
    payload: dict = {}
    while time.time() < deadline:
        _, _, polled = request(f"{base}/api/v1/runs/{job_id}")
        payload = json.loads(polled)
        if payload.get("state") in ("done", "failed"):
            break
        time.sleep(0.1)
    return payload


def shut(built, thread) -> None:
    built.shutdown()
    built.server_close()
    built.store.close()
    thread.join(timeout=5)


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------

def test_the_text_under_the_table_folds_and_the_table_stays_open() -> None:
    """The operator: "Just that long text below it", and all of it.

    An earlier fix folded the catalogue's note alone, and the legend, the caveats and the
    two notes stayed under the closed summary -- so to the operator the fold
    "only affects the title but not the text below it". Every explanatory
    paragraph under the table now sits inside one closed `<details>`, the
    table is inside none, and the controls under it stay outside the fold.
    """
    markup = source(INDEX)
    anchor = 'id="about-list"'
    check(anchor in markup, "the text under the table is no longer in a <details>")
    if anchor not in markup:
        return
    opening = markup[:markup.index(anchor)].rsplit("<", 1)[1] \
        + markup[markup.index(anchor):].split(">", 1)[0]
    check(opening.startswith("details") and " open" not in opening,
          f"the fold must be a closed <details>: <{opening}>")
    fold = markup[markup.index(anchor):].split("</details>", 1)[0]
    check('data-t="models.about"' in fold, "the fold's summary is not models.about")
    for hook in ('data-cc="catalogue-note"', 'data-cc="model-bands"',
                 'data-cc="route-caveats"', 'data-cc="commands-hint"',
                 'data-t="models.notpriced.note"'):
        check(hook in fold, f"{hook} is outside the fold")
    for hook in ('data-cc="split-models"', 'data-cc="custom-toggle"'):
        check(hook not in fold, f"{hook} is a control and is inside the fold")
    before = markup[:markup.index('data-cc="model-rows"')]
    check(before.count("<details") == before.count("</details>"),
          "the models table is inside a <details>; it must stay open")
    for tag, strings in catalogues().items():
        check(bool(strings.get("models.about", "").strip()),
              f"{tag}.json has no models.about summary")
    js = strip_comments(source(APP_JS))
    render = body_of(js, "function renderScorecard()")
    check('el("catalogue-note").hidden = !notes' in render,
          "an empty catalogue note must hide rather than leave a gap")
    check('el("catalogue-about").hidden' not in render,
          "the fold holds the legend too and must not hide with the note")
    # Must-fire: a paragraph moved back out of the fold is seen.
    moved = fold.replace('data-cc="model-bands"', "")
    check('data-cc="model-bands"' not in moved, "the probe cannot see its anchor")


def test_the_loss_ceiling_sits_directly_above_the_title_policy() -> None:
    """The operator: the ceiling "looks a little bit lost" at the end of the
    grid; "maybe above 'What happens to the title'?"

    The two share one grid cell, ceiling first, so they stay together at every
    width and the source order -- which is the tab order -- reads ceiling, then
    title. The cell holds those two fields and nothing else.
    """
    markup = source(INDEX)
    stack = markup.find('<div class="field-stack">')
    check(stack >= 0, "the ceiling and the title policy no longer share a cell")
    if stack < 0:
        return
    cell = markup[stack:markup.index("</div>\n\n    </div>", stack)]
    loss, title = cell.find('id="loss-budget"'), cell.find('id="title-policy-label"')
    check(0 <= loss < title,
          "the cell must hold the ceiling first and the title policy under it")
    check(cell.count('<div class="field">') == 2,
          f"the cell holds {cell.count('<div class=\"field\">')} fields; it is "
          f"for these two alone")
    for key in ("controls.loss", "controls.loss.hint", "controls.title"):
        check(f'data-t="{key}"' in cell, f"{key} left the cell")


def test_a_subscription_row_shows_its_route_figures_or_unmeasured() -> None:
    """A command route's figures come from `command_routes`, matched on
    id, model and profile together, and a route with none reads "unmeasured".

    The cost cell stays the plan's word: `costCell` answers a route before it
    reads `measured`, so a route's null `usd_per_merge` can never print $0.00.
    """
    js = strip_comments(source(APP_JS))
    rows = body_of(js, "function pickable()")
    check("measured: routeFigures(route)" in rows,
          "a command route's row does not take its figures from routeFigures")
    figures = body_of(js, "function routeFigures(")
    for field in ("row.route === route.id", "row.model === route.model",
                  "row.profile === route.profile", "command_routes"):
        check(field in figures, f"routeFigures does not match on {field}")
    check("|| null" in figures, "a route with no figures must be null, not {}")
    cost = body_of(js, "function costCell(")
    check(cost.index("routeOf(model)") < cost.index("model.measured"),
          "costCell reads a route's measured block before answering with the plan")
    for entry in catalogue.load().get("command_routes") or []:
        measured = entry.get("measured")
        check(measured is None or measured.get("usd_per_merge") is None,
              f"{entry['route']} carries a per-merge price")


def test_a_disabled_split_box_says_why_from_the_condition_that_disables_it() -> None:
    """The operator: a tooltip on "Use a different model for the checks" when
    it is disabled, saying why and how to use it.

    The box is disabled under one condition -- a command route picked for the
    merge -- and the sentence comes from the same value: `split.disabled` is
    `Boolean(blocked)` where `blocked` is the sentence. It is the `title`, the
    visible hint and the `aria-describedby` target at once, and all three go
    when the box is enabled.
    """
    js = strip_comments(source(APP_JS))
    render = body_of(js, "function renderModels()")
    check("split.disabled = Boolean(blocked)" in render,
          "the split box is disabled by something other than splitBlocked's sentence")
    check(render.count("split.disabled =") == 1,
          "a second assignment disables the split box without a reason")
    for piece in ("split.title = blocked", 'split.setAttribute("aria-describedby", "split-blocked")',
                  'split.removeAttribute("title")', 'split.removeAttribute("aria-describedby")',
                  "why.hidden = !blocked"):
        check(piece in render, f"renderModels no longer does {piece!r}")
    reason = body_of(js, "function splitBlocked(")
    check("chosenRoute()" in reason and 't("models.split.blocked.route"' in reason,
          "splitBlocked must read the condition and write the catalogue's sentence")
    others = [line.strip() for line in js.splitlines()
              if "split-models" in line and ".disabled" in line]
    check(not others, f"the split box is disabled elsewhere: {others}")
    markup = source(INDEX)
    hint = markup[markup.index('data-cc="split-blocked"') - 60:markup.index('data-cc="split-blocked"') + 40]
    check('id="split-blocked"' in hint and " hidden" in hint,
          "the reason needs an id to be described by, and starts hidden")
    for tag, strings in catalogues().items():
        text = strings.get("models.split.blocked.route", "")
        check("{name}" in text and len(text) > 80,
              f"{tag}.json's reason must name the row and say what enables the box")
    # Must-fire: a disabling assignment with no reason is seen.
    seeded = render.replace("split.disabled = Boolean(blocked)", "split.disabled = true")
    check("split.disabled = Boolean(blocked)" not in seeded,
          "the probe cannot see its own anchor")


def test_the_typed_id_and_its_destination_appear_together_behind_a_checkbox() -> None:
    """The operator: "make that combo box appear once the user selects the
    checkbox".

    A picked model routes by its provider, so a `Send it to` select sitting
    open beside the table offered a choice that was not the reader's -- the
    operator read `Send it to: <the local endpoint>` under a selected
    `gpt-5.6-terra` whose run had already gone to OpenAI. The select now lives
    with the field, both behind "Use a model id not in the table", hidden until
    it is ticked. Unticking clears the id, so the request carries none, and the
    one reader every consumer uses counts an id only while the box is ticked.
    """
    markup = source(INDEX)
    anchor = 'data-cc="custom-block"'
    check(anchor in markup, "the typed-id block needs a container to hide")
    if anchor not in markup:
        return
    opening = markup[markup.index(anchor):].split(">", 1)[0]
    check(" hidden" in opening,
          "the typed-id block must start hidden: the page opens with the box "
          "unticked and a row picked from the table")
    toggle = 'data-cc="custom-toggle"'
    check(toggle in markup and markup.index(toggle) < markup.index(anchor),
          "the checkbox must sit before the block it reveals")
    block = markup[markup.index(anchor):markup.index('data-cc="custom-model-note"')]
    for hook in ("custom-model", "custom-endpoint"):
        check(f'data-cc="{hook}"' in block,
              f"{hook} is not inside the block the checkbox reveals")

    js = strip_comments(source(APP_JS))
    render = body_of(js, "function renderCustomModel(")
    check('el("custom-block").hidden = !store.customOn' in render,
          "renderCustomModel must tie the block's visibility to the checkbox")
    reader = body_of(js, "function typedId(")
    check("store.customOn ?" in reader,
          "typedId must count a typed id only while the box is ticked")
    check(js.count("store.customModel.trim()") == 1,
          "a second reader of the typed id bypasses the checkbox")
    wiring = body_of(js, "function wire(")
    handler = wiring[wiring.index('toggle.addEventListener("change"'):]
    handler = handler[:handler.index("});")]
    check('store.customModel = ""' in handler and 'input("custom-model").value = ""' in handler,
          "unticking must clear the typed id, in the store and in the field")

    # Must-fire: the probe has to be able to see the assignment missing.
    check('el("custom-block").hidden = !store.customOn'
          not in render.replace('el("custom-block").hidden = !store.customOn', "noop()"),
          "the probe cannot see its own anchor, so the check above passed over "
          "nothing")


def toggle_pair_problems(html: str, css: str) -> list[str]:
    """The operator: "Use a different model for the checks" and "Use a
    model id not in the table" "in one row instead of below each other,
    which will give us another line back." `flex-wrap` on the row lets the
    two fall back to stacked, gracefully rather than overflowing, at a
    phone width or under the longer German labels; the typed-id reveal
    block stays full width below both, since it is a two-column block of
    its own once ticked.
    """
    found = []
    marker = '<div class="toggle-pair">'
    if html.count(marker) != 1:
        found.append(f"there is no single .toggle-pair row ({html.count(marker)} found)")
        return found
    start = html.index(marker)
    if 'data-cc="split-blocked"' not in html[start:]:
        found.append("split-blocked has moved out of reach of the toggle-pair probe")
        return found
    stop = html.index('data-cc="split-blocked"', start)
    pair = html[start:stop]
    for hook in ('data-cc="split-models"', 'data-cc="custom-toggle"'):
        if hook not in pair:
            found.append(f"{hook} is not inside the toggle-pair row")
    if 'data-cc="custom-block"' in pair:
        found.append("the typed-id reveal block is inside the toggle-pair row; "
                      "it must stay full width below both toggles")
    rule = re.search(r"\.toggle-pair \{([^}]*)\}", css)
    if not rule or "flex-wrap: wrap" not in rule.group(1):
        found.append("the toggle-pair row has no flex-wrap: wrap, so it cannot "
                      "fall back to stacked")
    return found


def test_the_two_toggles_share_one_row() -> None:
    """The split-model and typed-id checkboxes sit side by side.

    Must-fire: a toggle pulled back out of the shared row, and the row's own
    wrap rule dropped, are each caught.
    """
    markup, css = source(INDEX), source(APP_CSS)
    for problem in toggle_pair_problems(markup, css):
        check(False, problem)
    seeded = markup.replace(
        '<div class="toggle-pair">\n      <div class="check-row">',
        '<div class="check-row">', 1)
    check(seeded != markup and bool(toggle_pair_problems(seeded, css)),
          "a toggle pulled back out of the shared row is not caught")
    seeded_css = css.replace(
        ".toggle-pair { display: flex; flex-wrap: wrap; gap: .5rem 1.5rem; }",
        ".toggle-pair { display: flex; gap: .5rem 1.5rem; }", 1)
    check(seeded_css != css and bool(toggle_pair_problems(markup, seeded_css)),
          "a toggle-pair row that can no longer wrap is not caught")


def test_a_typed_id_naming_a_retired_row_is_warned_and_not_blocked() -> None:
    """A hand-typed `claude-opus-5` still goes to Anthropic, routed by its
    retired row, and is refused on every merge. The page warns beside the
    field and again above the button, in the page's language, out of the row's
    own `retired` block -- and does not block, so nothing retired is added to
    what disables the button. Driven in Chromium,
    in English and German.
    """
    markup = source(INDEX)
    for hook in ("custom-model-retired", "submit-retired-warning"):
        tag = f'<p class="hint warn" data-cc="{hook}" hidden></p>'
        check(tag in markup, f"{hook} must be a hidden warning paragraph")
    # Bounded by the next field after custom-block (window-block), not by a
    # closing-`</div>` pair: an earlier change dropped the `.field custom-field` wrapper
    # that pair used to close, once the checkbox row it held moved into
    # .toggle-pair, and the old pair-based bound started matching a
    # coincidental, unrelated pair of closing tags far later in the page.
    block = markup[markup.index('data-cc="custom-block"'):]
    check(block.index('data-cc="custom-model-retired"') < block.index('data-cc="window-block"'),
          "the field's warning must sit inside the typed-id block")
    run = markup[markup.index('data-cc="run-card"'):]
    check(run.index('data-cc="submit-retired-warning"') < run.index('data-cc="submit"'),
          "the run bar's warning must sit above the button it applies to")

    js = strip_comments(source(APP_JS))
    render = body_of(js, "function renderCustomModel(")
    fires = "row && isRetired(row) ? retiredWarning(typed, row.retired)"
    check(fires in render, "renderCustomModel no longer warns on a retired typed row")
    for hook in ("custom-model-retired", "submit-retired-warning"):
        check(f'"{hook}"' in render, f"renderCustomModel no longer writes {hook}")
    warning = body_of(js, "function retiredWarning(")
    check('t("models.custom.retired"' in warning and "retiredSentence(retired)" in warning,
          "the warning must be the catalogue sentence, in the page's language")
    # Warn, never block: nothing about retirement may reach the button.
    for gate in ("function unreachableChoice(", "function refreshIdleStatus("):
        check("etired" not in body_of(js, gate), f"{gate} now blocks on a retired id")
    # The typed id finds the retired row: `typedRow` reads `pickable()`, which
    # keeps retired rows (disabled). A filter there would silence the warning.
    check("isRetired" not in body_of(js, "function typedRow("),
          "typedRow filters retired rows, so a typed retired id is never warned")

    for tag, strings in catalogues().items():
        text = strings.get("models.custom.retired", "")
        for name in ("{model}", "{why}", "{replacement}"):
            check(name in text, f"{tag}.json's models.custom.retired lacks {name}")
    # claude-opus-5 (this test's real-data example until now) was
    # removed from the card entirely rather than kept retired, so no shipped
    # row exercises this data path any more; the shape itself stays held to
    # `catalogue.validate_retired` (tests/test_catalogue.py). Generic here
    # instead: whichever rows are retired, if any, carry what the warning
    # template needs.
    rows = {row["id"]: row for row in json.loads(
        (ROOT / "src" / "llossless" / "web" / "catalogue.json").read_text("utf-8"))["models"]}
    retired_rows = {row_id: row["retired"] for row_id, row in rows.items() if row.get("retired")}
    for row_id, retired in retired_rows.items():
        check(bool(retired.get("replacement")),
              f"{row_id}: the warning's words come from replacement, which reads {retired}")

    # Must-fire: the anchor above has to be able to see the warning go.
    seeded = render.replace(fires, "false ? retiredWarning(typed, row.retired)")
    check(fires not in seeded, "the probe cannot see its own anchor")


def test_the_typed_id_states_a_window_where_its_endpoint_cannot_report_one() -> None:
    """A typed vendor id ran its merge and then every check refused.

    A vendor has no `/api/ps` and a model the catalogue does not know carries
    no window, so the page now offers "Context window (tokens)" beside the id
    and "Send it to". Required where the server says the destination cannot
    report a window, optional elsewhere, refused before submit when missing or
    out of the server's bounds. Driven in Chromium in both languages;
    this pins the wiring.

    The field was moved out from behind the typed-id checkbox so a row picked
    straight from the table can use it too (next test); `windowFieldActive` is
    now the one gate, not `typedId()` alone, but the field, its validation and
    the request's `window` are the same ones this entry built.
    """
    markup = source(INDEX)
    row = markup[markup.index('data-cc="custom-model"'):
                 markup.index('data-cc="custom-model-note"')]
    check('data-cc="custom-window"' not in row,
          "the window field moved out of the typed-id row; it must not "
          "still be there")
    start = markup.index('data-cc="window-block"')
    block = markup[start:markup.index('data-cc="custom-window-note"', start)]
    field = 'data-cc="custom-window"'
    check(field in block, "the window field must exist, wherever it now sits")
    check('type="number"' in block and 'aria-describedby="custom-window-note"' in block,
          "the window field must be a number field described by its note")
    check('data-t="models.custom.window"' in block,
          "the window field's label must come from the catalogue")

    js = strip_comments(source(APP_JS))
    check("window: typedWindow()" in body_of(js, "function submission("),
          "the request must carry the window from the one reader")
    check("if (!windowFieldActive()) return undefined" in body_of(js, "function typedWindow("),
          "a window must be sent only while the field is in charge of something")
    check("window_required" in body_of(js, "function windowNeed("),
          "whether the window is required must be the server's answer")
    refusal = body_of(js, "function windowRefusal(")
    check("min_window" in refusal and "max_window" in refusal,
          "the page must refuse on the bounds the server serves")
    check("windowRefusal()" in body_of(js, "function unreachableChoice("),
          "a missing or bad window must stop the button")
    wiring = body_of(js, "function wire(")
    handler = wiring[wiring.index('toggle.addEventListener("change"'):]
    handler = handler[:handler.index("});")]
    check('store.customWindow = ""' in handler
          and 'input("custom-window").value = ""' in handler,
          "unticking must clear the window, in the store and in the field")
    # Must-fire: the probe has to see the one reader missing.
    check("window: typedWindow()" not in body_of(js, "function submission(")
          .replace("window: typedWindow()", "window: undefined"),
          "the probe cannot see its own anchor")


def test_a_row_the_catalogue_does_not_know_states_its_window_from_the_table_too() -> None:
    """Picking such a row was the ordinary way to reach it, but until now only

    a *typed* copy of the same id had somewhere to state the window: a name
    an endpoint listed but the catalogue does not was refused only after the
    merge had run and every check failed. `pickedUnknownModel` finds the row
    -- either role, when the checks are split -- and every function the typed-id
    feature wrote now keys off it exactly as it already keyed off `typedRow`, so this is one
    field, one validation and one request field (`window`), not a second set.
    """
    js = strip_comments(source(APP_JS))
    picked = body_of(js, "function pickedUnknownModel(")
    check("model.context_window == null" in picked, "an unknown row is one "
          "with no context_window -- the reason it needs the field at all")
    check("!routeOf(model)" in picked and "model.provider" in picked,
          "a route states its own window (`route_plan` refuses one beside it) "
          "and a row with no provider is not from the catalogue; neither "
          "counts")
    check("store.splitRoles" in picked and "store.checkModel" in picked,
          "the check role can name such a row too, not only the merge role")

    active = body_of(js, "function windowFieldActive(")
    check("store.customOn" in active and "pickedUnknownModel()" in active,
          "the field is active for a typed id or a picked row, "
          "not the checkbox alone")

    need = body_of(js, "function windowNeed(")
    check("pickedUnknownModel()" in need,
          "a picked row's need -- required or optional -- must be read off "
          "the row `pickedUnknownModel` finds, the same `window_required` "
          "lookup already made for a typed one")

    render = body_of(js, "function renderCustomWindow(")
    check('el("window-block").hidden = !active' in render
          and "windowFieldActive()" in render,
          "the block's own visibility must be `windowFieldActive`, not the "
          "checkbox alone")

    check("renderCustomWindow()" in body_of(js, "function useCell("),
          "picking a merge row must re-render the window field: "
          "`renderModels` is only called on a route crossing, so a plain pick "
          "would otherwise leave the previous row's answer on screen")
    check("renderCustomWindow()" in body_of(js, "function checkCell("),
          "picking a check row must do the same")

    unreachable = body_of(js, "function unreachableChoice(")
    check("const stated = windowRefusal();" in unreachable
          and unreachable.index("const stated = windowRefusal()")
          > unreachable.index("for (const id of roles)"),
          "a picked row's missing or bad window must stop the button too, "
          "checked after reachability and before the split-role guard")

    # Must-fire: the probe has to see the one predicate missing.
    check("model.context_window == null" not in picked
          .replace("model.context_window == null", "false"),
          "the probe cannot see its own anchor")


def test_a_conflict_candidate_is_rendered_as_text_not_as_an_object() -> None:
    """`[object Object]`, in the section that exists to show the disagreement.

    A candidate is an object: `merge._CANDIDATE_ITEM` gives it `text` and
    `document`, and `parsing.CANDIDATE_FIELDS` requires both. `String(one)` on
    it renders `[object Object]`, and that is what shipped -- the operator's
    first real run showed "Candidates: [object Object] [object Object]" under
    every one of eleven conflicts.

    Nothing else caught it because nothing else reads the shape:
    `html_report.py` renders no candidates at all, so this page is its only
    reader and it was reading it wrong. A renderer that is the sole consumer of
    a shape needs a test against the shape, not against a sibling that agrees.
    """
    js = strip_comments(source(APP_JS))
    body = body_of(js, "function renderConflicts(")
    check("one.text" in body,
          "a candidate's text is under `.text`; renderConflicts must read it")
    check("one.document" in body,
          "a candidate names the document it came from, and a conflict that "
          "does not say which source said what is not showing the conflict")

    # The property, not the absence of a spelling. `String(one)` survives as
    # the fallback for a candidate that arrived as a bare string -- worth
    # showing badly rather than not at all -- so banning the call outright
    # would forbid the correct branch along with the defective one. What must
    # be true is that the object case is *distinguished* before anything is
    # stringified.
    mapped = body[body.index("record.candidates"):][:700]
    check('typeof one === "object"' in mapped,
          "renderConflicts must tell an object candidate from a bare string "
          "before rendering either; without that test `String(one)` is reached "
          "for the object and prints [object Object]")

    # Must-fire: the probe has to be able to see the guard missing.
    check('typeof one === "object"' not in mapped.replace('typeof one === "object"', "false"),
          "the probe cannot see its own anchor, so the check above passed over "
          "nothing")


# What the engine puts in `provenance` that the page deliberately does not
# show, and why each one. An exemption is a sentence, not a name: the point of
# the check below is that a field added to the block reaches a reader, and a
# list you can append to without saying why is a list that grows until the
# check means nothing.
PROVENANCE_NOT_SHOWN = {
    # Per-call rows: the right shape for a spend analysis and the wrong one
    # for a summary block. `counts` and `tokens_described` carry the totals a
    # reader wants here, and both are rendered.
    "ledger": "per-call detail; the totals beside it are what a summary owes",
    # A digest per prompt file. It belongs to a report a reader is comparing
    # against another run, which is the downloadable artefact's job rather
    # than this panel's.
    "prompts": "file digests; for comparing two runs, not for reading one",
    # Already summarised by `counts.calls`, and the split by role answers a
    # question -- did the merge role run at all -- that the page answers by
    # showing the merged document.
    "calls_by_role": "summarised by Calls; the split answers a question the "
                     "page answers by showing the document",
    # The measured/unmeasured split behind `tokens_described`, which renders
    # the same fact as a sentence.
    "tokens": "rendered as the sentence in tokens_described",
    # Structured as three fields and rendered as one row, so the keys differ
    # from the row name by design.
    "merge_policy": "rendered as Fidelity, Title policy and Base document",
    # The two token totals under `counts`, present only when a call reported
    # them. Rendered as the sentence in `tokens_described`, like `tokens`.
    "prompt_tokens": "rendered as the sentence in tokens_described",
    "completion_tokens": "rendered as the sentence in tokens_described",
    # Per-role endpoint ids, present only when the roles were sent to
    # different addresses. The Endpoint row names the merge's, and each
    # role's model row names what it asked for; three hashes in a summary
    # answer a question the report's JSON is for.
    "by_role": "per-role endpoint hashes; the report's JSON carries them",
    # Present only when the tree moved between `Client.__init__` and the
    # report being written, a benchmark-integrity signal for
    # whoever compares this report against its cassettes, not a per-run
    # condition the summary panel's reader needs. `claimcheck_commit` above,
    # which is rendered, is the commit the run actually started under either
    # way.
    "claimcheck_commit_end": "diagnostic: the commit a mid-run change left "
                             "the tree at; claimcheck_commit is what the run started under",
    "claimcheck_commit_changed": "diagnostic: whether the tree moved mid-run; "
                                 "see claimcheck_commit_end",
    # Per role, under `isolation`: the environment variable *names*
    # a command backend's child did not receive. An audit trail for whoever
    # checks a run for a credential leak, not a fact the summary panel's
    # Isolation row needs to state -- that row already says safe mode and the
    # tools grant, which is what a reader is isolating documents from.
    "env_dropped": "diagnostic: the env var names withheld from the command "
                   "backend's child; not part of the Isolation row",
    # Per role, present only when some call named an answering model:
    # the same fact `model_said` already renders into the Model row's
    # sentence (`opus -> claude-opus-5-5`), as data rather than only text.
    # `models` above, which the row reads, is the label; this is not a second
    # row to add, it is the first row's own source made machine-readable.
    "models_answered": "diagnostic: which model id(s) actually answered per "
                       "role; rendered already, as part of the Model row",
    # Per role, under `isolation`: the seconds one
    # call on a command route got. An audit figure for a reader comparing a
    # stopped run against its configured route, not a fact the summary
    # panel's Isolation row states -- that row is about what the model could
    # reach, not how long it was given.
    "timeout": "diagnostic: the command route's call_timeout; not part of "
              "the Isolation row",
    # The benchmark's reading of a run's time and cost: the
    # answering attempts' seconds and price, what was excluded (platform
    # retries, blank re-asks, waits), what awaits a ruling, and the live
    # calls that never reached the ledger. Inputs to the figure scripts that
    # build the lineup table, not conditions of the run a reader of the
    # summary panel needs: the panel's Duration and Cost rows already state
    # the run's wall time and its priced ledger.
    "answering_seconds": "benchmark accounting: the answering attempts' "
                         "seconds; the panel shows Duration",
    "answering_cost": "benchmark accounting: the answering attempts' "
                      "price; the panel shows Cost",
    "excluded": "benchmark accounting: platform retries, blank "
                "re-asks and waits, kept out of speed and cost",
    "unruled": "benchmark accounting: attempts awaiting the "
               "operator's ruling, in neither total",
    "discarded_calls": "benchmark accounting: live calls that never "
                       "reached the ledger, for the figure scripts",
}


def provenance_keys(source: str) -> set[str]:
    """Every key `as_dict` writes, including the ones it writes conditionally.

    The pattern used to be `"key":` at the start of a line, and a conditional
    key is written `**({"key": value} if ... else {})`, so every field the
    engine emits only when it has something to say was invisible to this
    check: `effort`, `effort_ignored`, `reasoned_anyway` and `profile` among
    them. `decoding.effort` went unrendered on the page for a long stretch
    with this check green.
    """
    return set(re.findall(r'^\s*(?:\*\*\(\{)?"([a-z_]+)":', source, re.M))


def test_the_provenance_key_pattern_sees_a_conditional_key() -> None:
    """Seeded with the shape that hid `effort`, and with the plain one."""
    conditional = '                **({"effort": effort} if effort else {}),\n'
    plain = '                "temperature": self._wire_temperature(),\n'
    check(provenance_keys(conditional) == {"effort"},
          f"a conditional key is not seen: {provenance_keys(conditional)}")
    check(provenance_keys(plain) == {"temperature"},
          f"a plain key is not seen: {provenance_keys(plain)}")


def test_the_page_shows_every_provenance_field_the_engine_emits() -> None:
    """The run's conditions reach a reader, or the panel is decoration.

    The operator's complaint was that the page said little more than the
    command it had run, while the CLI's block names the model, the endpoint,
    the tier and the window. A panel that omits those does not say the run was
    unremarkable -- it says nothing, and a reader cannot tell the two apart.

    Written as a check against the *engine's own keys* rather than a list of
    labels, because the failure this guards is a field being added to
    `Provenance.as_dict` and never reaching the page. A label list would have
    stayed green through exactly that.
    """
    import inspect

    from llossless import provenance as provenance_module

    source = inspect.getsource(provenance_module.Provenance.as_dict)
    emitted = provenance_keys(source)
    check(len(emitted) >= 12,
          f"only {len(emitted)} provenance key(s) found in as_dict; the "
          f"pattern has drifted and this check is passing vacuously")

    app = APP_JS.read_text(encoding="utf-8")
    body = app[app.index("function renderProvenance("):]
    body = body[:body.index("\n}\n")]

    missing = sorted(key for key in emitted
                     if key not in PROVENANCE_NOT_SHOWN and key not in body)
    check(not missing,
          f"renderProvenance never reads {missing}; a field the engine records "
          f"and the page drops is a run condition the operator cannot see")

    stale = sorted(key for key in PROVENANCE_NOT_SHOWN if key not in emitted)
    check(not stale,
          f"{stale} is exempted from the provenance panel and the engine no "
          f"longer emits it; an exemption for a field that does not exist "
          f"hides the next one that takes its name")


def effort_problems(body: str) -> list[str]:
    """Every way the Decoding row stops reporting the run's own effort."""
    problems = []
    for read in ("decoding.effort ||", "decoding.effort_ignored ||",
                 "decoding.reasoned_anyway ||"):
        if read not in body:
            problems.append(f"renderProvenance no longer reads `{read[:-3]}`")
    # A level spelled in the script is a level the run did not report. The
    # three roles and five levels are `config.ROLES` and `EFFORT_LEVELS`.
    for role in ("merge", "decompose", "verify"):
        for level in ("low", "medium", "high", "xhigh", "max"):
            if f"{role}={level}" in body:
                problems.append(f"renderProvenance spells `{role}={level}` "
                                f"itself rather than reading it")
    for key in ("provenance.effort", "provenance.effort_ignored",
                "provenance.reasoned_anyway"):
        if f't("{key}"' not in body:
            problems.append(f"renderProvenance no longer renders {key}")
    return problems


def test_the_decoding_row_reads_effort_from_the_run() -> None:
    """The level the run recorded, never one the page supplies.

    The substring check above cannot tell a field read from a field named:
    `effort` is "in" a body that hard-codes `merge=medium` beside
    `t("provenance.effort")`. So the read itself is pinned, and a spelled
    level is refused. Seeded with the exact hard-coding an earlier browser
    drive was seeded with, which rendered AUTO_EFFORT's default and passed that
    drive only when the run happened to use the default.
    """
    app = APP_JS.read_text(encoding="utf-8")
    body = app[app.index("function renderProvenance("):]
    body = body[:body.index("\n}\n")]
    for problem in effort_problems(body):
        check(False, problem)
    read = ('Object.entries(decoding.effort || {})\n'
            '    .map(([role, level]) => role + "=" + String(level))')
    check(read in body, "the probe's anchor has moved")
    seeded = body.replace(read, '["decompose=low", "merge=medium", "verify=low"]')
    check(seeded != body and bool(effort_problems(seeded)),
          "a hard-coded level in place of the read is not caught")
    seeded = body.replace('t("provenance.effort")', '"effort"')
    check(bool(effort_problems(seeded)),
          "the label taken out of the catalogue is not caught")


def test_every_findings_list_the_engine_publishes_reaches_a_section() -> None:
    """A finding the page counts and never shows.

    `report.as_dict` publishes findings in three places: `structural`, and
    then `prompt_leaks` and `restated_claims`, which are kept out of
    `structural` on purpose because they are not among the nine mechanical
    checks. The page read the first and counted all three -- so a long
    document whose one finding was a restated claim showed "Restated claims, 1
    to read" in the checks table and had no section containing it anywhere.
    The operator looked, could not find it, and reasonably concluded the tool
    was wrong.

    Asserted against the engine's own blocks rather than a list of names,
    because the failure to prevent is a *fourth* block being added and the
    page reading three.
    """
    import inspect

    from llossless import report as report_module

    source = inspect.getsource(report_module.as_dict)
    # A block that publishes findings looks like `"findings": [...]` nested
    # under a named key. The names are what `structuralFindings` has to cover.
    publishing = sorted(set(re.findall(
        r'"([a-z_]+)": \{[^{}]*?"findings":', source, re.S)))
    check(len(publishing) >= 3,
          f"only {publishing} publish findings; the pattern has drifted and "
          f"this check is passing vacuously")

    app = APP_JS.read_text(encoding="utf-8")
    body = app[app.index("function structuralFindings("):]
    body = body[:body.index("\n}\n")]

    # `attributions` was the fourth block, and this check fired on it;
    # it was carried as a strict expected failure until the page read the
    # block, and the mark is gone with the debt.
    missing = [name for name in publishing if name not in body]
    check(not missing,
          f"structuralFindings reads {sorted(n for n in publishing if n in body)} "
          f"and not {missing}; a findings list the checks table counts and no "
          f"section renders is a chip pointing at nothing")


def attribution_problems(js: str) -> list[str]:
    """Every way a misattribution stops reaching a section. Empty is pass."""
    js = strip_comments(js)
    problems = []
    if "(report.attributions || {}).findings" not in js_function("structuralFindings", js):
        problems.append("structuralFindings does not collect report.attributions")
    section = js_function("renderAttributions", js)
    if ("ATTRIBUTION_KINDS.indexOf(f.kind)" not in section
            or 'el("attributions-section")' not in section
            or "attributionItem(report, finding)" not in section):
        problems.append("renderAttributions does not render the collected "
                        "misattributions into their section")
    if 't("section.attributions.note")' not in section:
        problems.append("the section does not say what its rows are")
    item = js_function("attributionItem", js)
    if 't("detail.credited")' not in item or "stackPanel(finding)" not in item:
        problems.append("a misattribution row does not name the credited source "
                        "and stack the two texts")
    if 't("detail.source")' in item:
        problems.append("a misattribution row labels the credited document as "
                        "its source, which is the one that does not carry it")
    if "renderAttributions(report);" not in js_function("renderReport", js):
        problems.append("renderReport never renders the Attributions section")
    if ('ATTRIBUTION_KINDS.indexOf(finding.kind) >= 0 ? "results.attributions"'
            not in js_function("renderReview", js)):
        problems.append("the review list points a misattribution at another "
                        "section")
    # The review row and the card it jumps to have to agree on the same
    # id, or a click lands nowhere (or, worse, on some other finding).
    if "structuralFindingId(finding)" not in item:
        problems.append("a misattribution card carries no findingId for the "
                        "review list to jump to")
    if '"check.attributions", attributions.ran ? "clean" : "notchecked"' \
            not in js_function("renderChecks", js):
        problems.append("the checks table does not say whether the attribution "
                        "check ran")
    return problems


def test_a_misattribution_reaches_a_section_that_names_it() -> None:
    """A run whose only finding is a misattribution says what it was."""
    for problem in attribution_problems(source(APP_JS)):
        check(False, problem)
    markup = (STATIC / "index.html").read_text(encoding="utf-8")
    check('data-cc="attributions-section" hidden' in markup
          and 'data-cc="attributions-chip"' in markup
          and 'data-cc="attributions"' in markup,
          "index.html has no Attributions section for renderAttributions to fill")


def test_the_attribution_guard_fires_on_each_piece_removed() -> None:
    """Seeded against the shipped functions, one piece at a time."""
    js = source(APP_JS)
    check(not attribution_problems(js), "the shipped page fails its own check")
    for piece, seed, what in (
            ("    ...((report.attributions || {}).findings || []),\n", "",
             "the collector's fourth block"),
            ("attributionItem(report, finding)", "structuralItem(finding)",
             "the row"),
            ('t("detail.credited")', 't("detail.source")', "the credited label"),
            ("  renderAttributions(report);\n", "", "the section's render call"),
            ('ATTRIBUTION_KINDS.indexOf(finding.kind) >= 0 ? "results.attributions"',
             'false ? "results.attributions"', "the review list's pointer"),
            # The first of app.js's three `stackPanel(finding), structuralFindingId(finding))`
            # closings is `attributionItem`'s own; `replace(..., 1)` takes it
            # and leaves `structuralItem`'s and `renderNumbers`'s alone.
            ("rows, \"bad\", stackPanel(finding), structuralFindingId(finding));\n}\n\n"
             "/**\n * How each document writes its decimals",
             "rows, \"bad\", stackPanel(finding));\n}\n\n"
             "/**\n * How each document writes its decimals", "the card's own findingId")):
        check(piece in js, f"the probe cannot find {what}: {piece!r}")
        check(bool(attribution_problems(js.replace(piece, seed, 1))),
              f"{what} removed is not caught")



def number_problems(js: str) -> list[str]:
    """Every way a number-format row stops reaching its section. Empty is pass."""
    js = strip_comments(js)
    problems = []
    if "(report.number_format || {}).findings" not in js_function("structuralFindings", js):
        problems.append("structuralFindings does not collect report.number_format")
    section = js_function("renderNumbers", js)
    if ("NUMBER_KINDS.indexOf(f.kind)" not in section
            or 'el("numbers-section")' not in section
            or "findingItem(" not in section):
        problems.append("renderNumbers does not render the collected rows into "
                        "their section")
    if 't("section.numbers.note")' not in section:
        problems.append("the section does not say what its rows are")
    if "block.documents" not in section or 't("numbers.convention"' not in section:
        problems.append("the section does not show what each document was "
                        "decided to be, which every row is relative to")
    if "block.faults" not in section or '? "bad" : "warn"' not in section:
        problems.append("a warning and a fault render in one tone, or the "
                        "tone is not read from the engine's faults")
    if "renderNumbers(report);" not in js_function("renderReport", js):
        problems.append("renderReport never renders the Number format section")
    if ('NUMBER_KINDS.indexOf(finding.kind) >= 0 ? "results.numbers"'
            not in js_function("renderReview", js)):
        problems.append("the review list points a number-format row at another "
                        "section")
    # The review row and the card it jumps to have to agree on the same id.
    if "structuralFindingId(finding)" not in section:
        problems.append("a number-format card carries no findingId for the "
                        "review list to jump to")
    if '"check.numbers", numbers.ran ? "clean" : "notchecked"' \
            not in js_function("renderChecks", js):
        problems.append("the checks table does not say whether the number "
                        "format was checked")
    return problems


def test_a_number_format_row_reaches_a_section_that_names_it() -> None:
    """The page shows each document's convention and every flagged numeral."""
    from llossless import numerals

    for problem in number_problems(source(APP_JS)):
        check(False, problem)
    markup = (STATIC / "index.html").read_text(encoding="utf-8")
    check('data-cc="numbers-section" hidden' in markup
          and 'data-cc="numbers-chip"' in markup
          and 'data-cc="numbers"' in markup,
          "index.html has no Number format section for renderNumbers to fill")
    js = source(APP_JS)
    kinds = array(js, "const NUMBER_KINDS = [")
    check(kinds == list(numerals.KINDS),
          f"the page's number kinds are {kinds}; the engine's are "
          f"{list(numerals.KINDS)}")
    partition = set(array(js, "const OMITTED_KINDS = [")) | set(
        array(js, "const CONFLICT_KINDS = ["))
    check(not (set(kinds) & partition),
          f"{sorted(set(kinds) & partition)} render in their own section and in "
          f"a partition")
    strings = strings_table()
    for kind in numerals.KINDS:
        check(f"kind.{kind}" in strings,
              f"{kind} has no label in the strings table and would render as its key")


def test_the_number_guard_fires_on_each_piece_removed() -> None:
    """Seeded against the shipped functions, one piece at a time."""
    js = source(APP_JS)
    check(not number_problems(js), "the shipped page fails its own check")
    for piece, seed, what in (
            ("    ...((report.number_format || {}).findings || []),\n", "",
             "the collector's fifth block"),
            ('? "bad" : "warn"', '? "bad" : "bad"', "the warning tone"),
            ("  renderNumbers(report);\n", "", "the section's render call"),
            ('NUMBER_KINDS.indexOf(finding.kind) >= 0 ? "results.numbers"',
             'false ? "results.numbers"', "the review list's pointer"),
            ('t("numbers.convention", {', 't("numbers.conventions", {',
             "the documents' decisions"),
            ("stackPanel(finding), structuralFindingId(finding));\n    }))]);\n}",
             "stackPanel(finding));\n    }))]);\n}", "the card's own findingId")):
        check(piece in js, f"the probe cannot find {what}: {piece!r}")
        check(bool(number_problems(js.replace(piece, seed, 1))),
              f"{what} removed is not caught")

def test_the_banner_no_longer_names_sections_itself() -> None:
    """An earlier version named sections in prose; this dropped that in favour of the review
    list doing it, one item at a time, by click rather than by paragraph.

    `advice.look` used to read "Conflicts and omitted content below need a
    look", true only when those two sections were where the findings were,
    then grew a `.named` form that listed whichever sections actually held
    something -- until the operator read its German rendering, a mid-sentence
    list of capitalised section names ("Konflikte, Ausgelassene Inhalte"),
    and asked what "Konflikte" was doing there. The review list above the
    sections already names each item's own section and now jumps a reader
    straight to it (`reviewItem`, `jumpToFinding`), which is what the
    interpolated list existed to approximate in prose; keeping both said the
    same thing twice; this asserts only one of them still does.
    """
    app = APP_JS.read_text(encoding="utf-8")
    check("advice.look.named" not in app,
          "the retired key or its word is still in app.js")
    check('t("advice.look")' in app,
          "adviceFor must still return the one plain sentence for an "
          "otherwise-unplaced exit 1")
    advice = js_function("adviceFor", app)
    check("where.push" not in advice and "where.length" not in advice,
          "adviceFor still builds a list of which sections hold something, "
          "the mechanism the operator asked to be dropped")

    # One function, two callers. The banner and the status line carried the
    # same four-line expression twice, which is how they would drift.
    check(app.count("function adviceFor(") == 1,
          "the advice is built in one place")
    callers = app.count("const advice = adviceFor(report);")
    check(callers == 2,
          f"and both the banner and the status line read it: {callers} "
          f"caller(s); the expression they replaced appeared twice, which is "
          f"how two views of one run drift apart")


def test_the_review_list_indexes_every_section_that_can_hold_a_finding() -> None:
    """One list of what needs a decision, above the sections.

    A long document produces dozens of green rows and one amber chip, and the
    chip is as likely to be in Structure as in Conflicts. Sorting helps inside
    one table and cannot help across six.

    The property asserted is that the list draws from the *same* collectors
    the sections do. A review index built from its own idea of where findings
    live would be the `restated_claims` bug again, one layer up: a reader
    trusting the index would miss exactly the family the index forgot.
    """
    app = APP_JS.read_text(encoding="utf-8")
    body = app[app.index("function renderReview("):]
    body = body[:body.index("\n}\n")]

    for source in ("report.findings", "structuralFindings(report)", "report.additions"):
        check(source in body,
              f"the review list must read {source}; a source it does not read "
              f"is a finding a reader trusting this list will never see")

    check("section.hidden = items.length === 0" in body,
          "and it hides itself when empty, because a standing empty panel "
          "headed `what needs your attention` teaches a reader to skip it")

    # It indexes, it does not move. Every entry is rendered in its own section
    # too, and a list that removed its targets would make those sections lie
    # about what they contain.
    markup = (STATIC / "index.html").read_text(encoding="utf-8")
    for hook in ("conflicts-section", "omitted-section", "additions-section"):
        check(hook in markup,
              f"{hook} must still exist: the review list is an index and the "
              f"sections are what it points at")
    check('data-cc="review-section" hidden' in markup,
          "the section starts hidden, so a clean run never shows it")

    check(app.count("renderReview(report);") == 1,
          "and it is called once, from `renderReport`")


def review_jump_problems(app: str, markup: str) -> list[str]:
    """Each review row is a click, or Enter or Space, away from its card.

    "What needs your attention" used to be an index a reader had to read and
    then go find by hand -- a bold label, a shortened claim, and "In section:
    Conflicts", with nothing to click. The operator asked for a jump: select
    a row, land on the matching card, wherever it lives.
    """
    problems = []
    template = markup[markup.index('<template data-cc="tpl-review-item">'):]
    template = template[:template.index("</template>")]
    if "<button" not in template:
        problems.append("tpl-review-item is not a button; a row that only "
                        "looks clickable is not reachable by Tab, Enter or Space")
    if 'data-cc="review-jump"' not in template:
        problems.append("tpl-review-item carries no review-jump hook for "
                        "reviewItem to put a click handler on")
    if 'data-cc="review-decide"' not in template:
        problems.append("tpl-review-item has nowhere to hold the one-line decision")

    body = js_function("reviewItem", app)
    if 'find(item, "review-jump").addEventListener(' not in body:
        problems.append("reviewItem never wires a click handler onto its own row")
    if "jumpToFinding(jumpId, tab)" not in body:
        problems.append("reviewItem's click handler does not call jumpToFinding")
    if 't(sectionKey.replace("results.", "review.decide."))' not in body:
        problems.append("reviewItem does not set a one-line decision from "
                        "review.decide.<section>")

    jump = js_function("jumpToFinding", app)
    for needed, why in (
        ('selectTab(el("finding-tabs"), finTab)', "switch to the card's own tab"),
        ("scrollIntoView", "scroll the card into view"),
        ('classList.add("just-found")', "flash the card so a sighted reader finds it"),
        ("stack.open = true", "open the card's own collapsed comparison, if it has one"),
        ("target.focus(", "move keyboard focus onto the card itself"),
    ):
        if needed not in jump:
            problems.append(f"jumpToFinding does not {why}: {needed!r} is missing")
    return problems


def test_the_review_list_jumps_to_the_finding_it_names() -> None:
    app, markup = source(APP_JS), source(INDEX)
    for problem in review_jump_problems(app, markup):
        check(False, problem)

    strings = strings_table()
    for key in ("review.decide.conflicts", "review.decide.omitted",
                "review.decide.attributions", "review.decide.numbers",
                "review.decide.additions"):
        check(bool(strings.get(key)),
              f"{key} is missing from en.json; a review row would print its raw key")
        check(bool(catalogues().get("de", {}).get(key)),
              f"{key} is missing from de.json")

    seeds = {
        "no button in the template": (
            markup,
            '<template data-cc="tpl-review-item">\n  <li class="finding review-item">\n'
            '    <button type="button" class="review-jump" data-cc="review-jump">',
            '<template data-cc="tpl-review-item">\n  <li class="finding review-item">\n'
            '    <span class="review-jump" data-cc="review-jump">'),
        "the click handler never calls jumpToFinding": (
            app, "jumpToFinding(jumpId, tab)", "null"),
        "the jump never opens the stacked comparison": (
            app, "stack.open = true", "false"),
        "the jump never moves focus to the card": (
            app, 'target.focus({ preventScroll: true })', "null"),
    }
    for what, (text, old, new) in seeds.items():
        seeded = text.replace(old, new, 1)
        check(seeded != text, f"the probe for {what} did not take")
        if text is markup:
            check(bool(review_jump_problems(app, seeded)),
                  f"the review-jump check does not fire on {what}")
        else:
            check(bool(review_jump_problems(seeded, markup)),
                  f"the review-jump check does not fire on {what}")


def test_a_clean_run_says_what_held_and_how_much_was_checked() -> None:
    """The clean message is positive, quantified, and not narrower than the check.

    It read "Nothing was dropped, contradicted or invented that this tool
    could find", which had three faults. Negative, where the result is
    positive. **It named three failure classes and not the fourth** --
    `partially_dropped` -- which is exactly the narrowing
    `report.verdict_line`'s own comment records having had to fix in the CLI's
    version of this sentence; a headline listing fewer classes than the check
    that produced it overstates the check. And "that this tool could find"
    hedges without informing: a reader cannot act on it, while the number of
    claims examined is the thing that tells them what the clean result is
    worth.

    The zero case is separated because "every claim survived" over no claims
    is true and worthless, and a clean banner over an empty check is how a
    reader is most easily misled.
    """
    strings = json.loads(
        (ROOT / "src" / "llossless" / "web" / "locales" / "en.json"
         ).read_text(encoding="utf-8"))["strings"]
    clean = strings["advice.clean"]

    for token in ("{forward}", "{reverse}"):
        check(token in clean,
              f"the clean message must carry {token}: a claim about a run "
              f"with no denominator cannot be weighed")
    check("could find" not in clean,
          f"and must not hedge with `could find`, which narrows the claim "
          f"without telling a reader anything they can act on: {clean!r}")

    # The failure-class trap. If the sentence enumerates classes at all it has
    # to enumerate every one the exit code covers, and the fourth is the one
    # that gets left out.
    named = [word for word in ("dropped", "contradicted", "invented")
             if word in clean.lower()]
    check(not named or "part" in clean.lower(),
          f"the message names {named} and not the partial case; either list "
          f"every class the check covers or describe the result without "
          f"enumerating them: {clean!r}")

    check("advice.clean.nothing" in strings,
          "a run with nothing to check needs its own sentence, because a "
          "clean banner over an empty check is the easiest way to mislead")
    app = APP_JS.read_text(encoding="utf-8")
    check("function cleanAdvice(" in app and "advice.clean.nothing" in app,
          "and it has to be reachable: the zero case is chosen in code, not "
          "left to a template that would render `0 source claim(s)` as though "
          "that were a result")


def test_the_claims_table_sorts_by_status_and_says_so_to_a_screen_reader() -> None:
    """The operator asked for sortable by status; this is that.

    The review list answers "what must I look at" across every section. This
    answers the other half, inside the one table long enough to hide a row:
    140 claims on the `unrelated` run, all but a handful green.

    Three properties worth pinning, and the third is the one most easily lost.
    """
    app = APP_JS.read_text(encoding="utf-8")
    markup = (STATIC / "index.html").read_text(encoding="utf-8")

    # A button, not a click handler on the `th`. A sort control has to be
    # reachable from the keyboard, and `all: unset` in the stylesheet removes
    # the focus ring the global rule provides, so it is put back explicitly.
    check('data-cc="claims-sort"' in markup and "<button" in markup,
          "the sort control must be a button, so it is focusable and operable "
          "without a mouse")
    css = (STATIC / "app.css").read_text(encoding="utf-8")
    check(".claims th button.sort:focus-visible" in css,
          "and must keep a focus ring: `all: unset` drops the one the global "
          "rule gives every other control")
    check('aria-sort' in markup and 'aria-sort' in app,
          "and must announce its state: `aria-sort` on the header is what a "
          "screen reader reads, and it has to be updated when the order does")

    # Two states, not three. A third that sorted the clean rows to the top
    # would be a control whose only use is hiding the findings, and reading
    # order is already what the reader gets without touching anything.
    body = app[app.index("function claimNeedsReview("):]
    body = body[:body.index("\n}\n")]
    check("return 1" in body and "return verdict.finding" in body,
          "an absent verdict ranks between a finding and a clean claim: it is "
          "not clean, and it is the one place a green-looking table can be "
          "hiding something")

    # Renumbered on sort. Leaving the original ordinals would make a sorted
    # table read as a shuffled one.
    check('setText(find(entry.row, "claim-n")' in app,
          "the `#` column is the reader's position in what they are looking "
          "at, so it is rewritten when the order changes")


def test_the_banner_event_is_rendered_from_its_fields() -> None:
    """The first line of a run, saying what the run is.

    `web/events.py`'s `banner` sends six fields and its docstring says why:
    *"here they are six fields, because the page has six places to put
    them"*. The page had none. `appendEvent` rendered every event as its kind
    plus `message`, and a banner's `message` is the short form of the merge
    invocation under the tool's old name -- so the first thing an operator saw
    of their run was **"BANNER / merge"**. That was the original complaint
    about this line, and expanding the provenance panel answered a different
    question: the panel is what the run *was*, read afterwards; this is what
    it *is*, read while waiting.

    Two things are asserted, and the second is the one that cost a round trip.
    """
    app = APP_JS.read_text(encoding="utf-8")
    check("function bannerRow(" in app,
          "the banner needs its own renderer; the generic one shows a kind "
          "and a message, and for this kind the message is the short form")
    check('kind === "banner" ? bannerRow(payload) : eventRow(kind, payload)' in app,
          "and `appendEvent` has to route the kind to it")

    # `Event.as_dict` nests everything that is not a lifecycle key under
    # `fields`. Reading them off the top level returns `undefined` five times
    # and falls back to the short message -- which looks exactly like the bug,
    # and did, for one round trip.
    body = js_function("bannerFields", app)
    check("payload.fields" in body,
          "the fields are under `fields`, not on the payload; reading the top "
          "level fails silently into the fallback")
    # `depth` joined them with the picker. It is the field that says which
    # questions this run is going to ask, it cannot change once the run has
    # started, and a reader who learns it afterwards from the provenance block
    # has already waited for an answer that means less than they thought.
    for field in ("model", "endpoint", "fidelity", "depth", "window"):
        check(f"f.{field}" in body,
              f"the line must name {field}: it is one of the things an "
              f"operator reads this for")

    # Each of the six under its own name, which is what makes this a header
    # for the run rather than a step in the list. The operator's complaint was
    # that the row "looks odd, and it is not clear to the user why that is":
    # it carried the word BANNER in the column every other row uses for STEP,
    # and five dot-separated values in the column every other row uses for a
    # sentence. A label key missing here is a field rendered with no name.
    strings = strings_table()
    for field in ("command", "model", "endpoint", "fidelity", "depth", "window"):
        check(f'"banner.{field}"' in body,
              f"the {field} field needs the catalogue key it is named under, "
              f"or it renders as a bare value in a row of labelled ones")
        check(f"banner.{field}" in strings,
              f"banner.{field} must be in the catalogue")
    check("banner.heading" in strings,
          "the run header needs its own label, which is what says the row is "
          "not one of the steps under it")
    row = js_function("bannerRow", app)
    check("run-header" in row,
          "the header is styled deliberately rather than left looking like a "
          "step that came out wrong")
    check("eventRow(\"banner\", payload)" in row,
          "an event with no fields has to fall back to the old row; an older "
          "server would otherwise get a heading over an empty box")

    # And the server has to send them. The CLI passed `window` from the day
    # the banner existed; the web call site never did, so the line named the
    # model and the endpoint and stopped.
    jobs = (ROOT / "src" / "llossless" / "web" / "jobs.py").read_text(encoding="utf-8")
    call = jobs[jobs.index("console.banner("):]
    call = call[:call.index(")\n")]
    for field in ("window=", "fidelity=", "depth="):
        check(field in call,
              f"web/jobs.py must pass {field} to `console.banner`, or the page "
              f"cannot show what it was never sent")
    check("banner_endpoint" in call,
          "and the endpoint must be the banner form: this event reaches a "
          "browser and is kept for the job's lifetime, and a base URL can "
          "carry userinfo and a pasted token")


def test_the_run_header_names_each_role_in_the_buttons_words() -> None:
    """The page half of the run header naming each role.

    `jobs.banner_roles` decides when the Model and Endpoint rows describe one
    role and not the run (`test_web_jobs` holds that); the page has to put the
    groups where those rows stood, drop the rows, and say each group's route
    in the words the submit button used. Driven in Chromium in both locales;
    these pin the pieces the drive exercised.
    """
    app = APP_JS.read_text(encoding="utf-8")
    body = js_function("bannerFields", app)
    check("f.roles" in body and "roleField" in body,
          "bannerFields must read the role groups the server sends")
    check('key === "banner.model" || key === "banner.endpoint"' in body,
          "and drop the single Model and Endpoint rows when it has them: kept, "
          "the check's model reads as the run's")
    field = js_function("roleField", app)
    check("routeLabel(endpointKind(group.route))" in field,
          "the route is the button's word for the recorded kind, through the "
          "one function that tolerates a kind this page does not know")
    for key in ("banner.role.merge", "banner.role.check"):
        check(f'"{key}"' in field, f"roleField must name a group {key}")
        for tag in ("en", "de"):
            check(key in strings_table(tag), f"{key} must be in {tag}.json")
    # The labels are the button's own words for the two roles.
    for tag in ("en", "de"):
        table = strings_table(tag)
        button = table["run.submit.split"]
        check(button.startswith(table["banner.role.merge"])
              and table["banner.role.check"].lower() in button.lower(),
              f"{tag}: the header's role names must be the button's: "
              f"{table['banner.role.merge']!r}, {table['banner.role.check']!r} "
              f"against {button!r}")
    check("literal || t(key)" in js_function("bannerRow", app),
          "a group the catalogue has no name for is labelled by its roles")

    jobs = (ROOT / "src" / "llossless" / "web" / "jobs.py").read_text(encoding="utf-8")
    call = jobs[jobs.index("console.banner("):]
    call = call[:call.index(")\n\n")]
    check("roles=banner_roles(settings, billed)" in call,
          "web/jobs.py must send the role groups, computed from `billed`")
    check('banner_endpoint_for("verify")' in call,
          "and the Endpoint row must be the verify role's, beside its model, "
          "not the server's default address")


# --------------------------------------------------------------------------
# the verification depth
# --------------------------------------------------------------------------

# The four functions that render or read the depth. Named here so the check
# below is about each of them rather than about whichever one somebody
# remembered, and so that a fifth is a deliberate addition to this list.
DEPTH_FUNCTIONS = ("renderVerifyDepth", "renderDepthEstimate", "callsAt",
                   "suspendedGuarantee")


def js_function(name: str, js: str = None) -> str:
    """One top-level function's body, by the same brace-free rule used above."""
    js = source(APP_JS) if js is None else js
    body = js[js.index(f"function {name}("):]
    return body[:body.index("\n}\n")]


def test_the_depth_picker_holds_no_depth_vocabulary_of_its_own() -> None:
    """The page renders the picker from `/config` and knows no depth by name.

    Same rule the fidelity ladder follows and for the same reason: a page that
    names a level is a page that has to be edited when one is added, and the
    edit nobody makes is the one that decides which option gets the warning.
    Here the stakes are higher than a label, because the thing derived from the
    name would be whether a clean result means "nothing was invented" --
    `detects_invention` is served precisely so nothing has to guess that from
    the string `coverage`.

    Scoped to the functions that render and read the depth rather than to the
    whole file: `coverage` is also the name of a report section and of one of
    the nine checks, and a file-wide ban would fail on those and teach the next
    reader to weaken it.
    """
    # `renderDepthDelta` joins the name ban and not the word ban below it: it
    # reads `quality_delta` by name, and it is the one renderer that
    # shows a measured figure -- about depths it must still not name.
    for name in DEPTH_FUNCTIONS + ("renderDepthDelta",):
        body = js_function(name)
        for value in config.VERIFY_DEPTHS:
            check(f'"{value}"' not in body and f"'{value}'" not in body,
                  f"{name} names the depth {value!r} itself; the depths, their "
                  f"sentences and the flag saying which of them checks for "
                  f"invention all come from /config")
    check("detects_invention" in js_function("suspendedGuarantee"),
          "the suspended-guarantee sentence must be decided by the server's "
          "flag, which is the only thing here that can be right about a depth "
          "this page has never heard of")


def test_the_depth_vocabulary_ban_fires() -> None:
    """Seeded: a depth name written into one of those functions must be found."""
    js = source(APP_JS).replace(
        "function suspendedGuarantee(report) {",
        'function suspendedGuarantee(report) {\n  const cheap = "coverage";')
    body = js_function("suspendedGuarantee", js)
    check(any(f'"{value}"' in body for value in config.VERIFY_DEPTHS),
          "a depth name written into the renderer is not found")


def test_each_depth_option_carries_its_own_limitation() -> None:
    """The warning is in the option, not in a footnote under the group.

    A sentence below a set of radios that changes when you pick one is a
    sentence a reader can change the setting without having read, and what is
    at stake here is not a nuance of degree: one of these options stops asking
    whether the merge invented anything. So the option renders its own
    explanation, and the explanation of any depth that does not check for
    invention has to say so in words rather than leaving it to the flag.
    """
    body = js_function("renderVerifyDepth")
    # From the catalogue by value, so German reads German.
    check('t("depth." + String(depth.value || "") + ".explains")' in body
          and "label.appendChild(body)" in body,
          "the depth's sentence must be rendered inside the option's own label")
    check("stacked-explains" in source(APP_CSS),
          "and it needs the style that makes it part of the option rather than "
          "a line of small print below the set")

    for value, shape in config.VERIFY_DEPTH_SHAPES.items():
        if shape.detects_invention:
            continue
        check("invention" in shape.explains.lower(),
              f"{value} does not check for invention and its own sentence never "
              f"says the word; the flag tells the page, and this is what tells "
              f"the person: {shape.explains!r}")
        check("only" in shape.explains.lower(),
              f"{value}'s sentence has to bound what it does check, not just "
              f"describe it: {shape.explains!r}")


def test_the_tagline_is_bounded_in_every_language() -> None:
    """This fix reverses an earlier one. The operator disliked the clipped line
    the tagline used to get: a fixed `max-width` with an ellipsis, next to the
    wordmark, because sharing that row let the German sentence's extra length
    (about a third longer than English) push `.topbar-right` onto a second
    row at a width English never reached. This moves the sentence to a row of
    its own, `.topbar-tagline`, below the wordmark/version/controls row
    instead of inside it: that row (`.topbar-inner`) is the one held to
    one height across languages, and the tagline is no longer part of
    it, so it is free to show the full sentence and wrap to however many
    lines German needs. No clipping, so no `title` mirror either -- the text
    on the page already is the whole sentence.
    """
    css = strip_css_comments(source(APP_CSS))
    rule = re.search(r"(?<!-)\.tagline\s*\{([^}]*)\}", css)
    check(bool(rule), "no .tagline rule in app.css")
    body = rule.group(1) if rule else ""
    for forbidden in ("max-width", "overflow: hidden", "text-overflow: ellipsis",
                      "white-space: nowrap"):
        check(forbidden not in body,
              f".tagline still has `{forbidden}`, so the sentence is clipped "
              f"again instead of shown in full")

    check(not re.search(r"max-width:\s*30rem\s*\)\s*\{\s*\.tagline\s*\{\s*display:\s*none",
                         css),
          "the tagline is hidden under 30rem again; the operator asked for it "
          "to wrap at a narrow width, not disappear")

    row = re.search(r"\.topbar-tagline\s*\{([^}]*)\}", css)
    check(bool(row),
          "no .topbar-tagline rule -- the tagline needs a row of its own, "
          "separate from .topbar-inner, so its height cannot move the row "
          "pinned to equal height across languages")

    js = strip_comments(source(APP_JS))
    check('classList.contains("tagline")' not in js,
          "app.js still mirrors the tagline into a title attribute; the full "
          "sentence is on the page now, so the mirror is dead code that can "
          "only go stale")

    html = source(INDEX)
    check('title="Merge documents, then check nothing was lost"' not in html,
          "index.html still carries the static title fallback on the "
          "tagline span")


def test_the_tagline_bound_check_fires() -> None:
    """Seeded: reintroducing the old ellipsis rule on .tagline must be caught."""
    css = strip_css_comments(source(APP_CSS))
    clipped = css.replace(
        '.tagline { display: block; color: var(--ink-soft); font-size: .8rem; }',
        '.tagline {\n'
        '  color: var(--ink-soft); font-size: .88rem;\n'
        '  max-width: 15rem; min-width: 0;\n'
        '  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;\n'
        '}')
    check(clipped != css, "the tagline-bound probe's anchor has moved")
    rule = re.search(r"(?<!-)\.tagline\s*\{([^}]*)\}", clipped)
    body = rule.group(1) if rule else ""
    still_full = all(forbidden not in body for forbidden in
                      ("max-width", "overflow: hidden", "text-overflow: ellipsis",
                       "white-space: nowrap"))
    check(not still_full, "reintroducing the ellipsis rule on .tagline is not caught")


ACCOUNT_BOUNDS = (
    (r"\.topbar-account \.ghost\s*\{([^}]*)\}", ("white-space: nowrap", "flex: none")),
    (r'\.topbar-account \[data-cc="open-settings"\]\s*\{([^}]*)\}', ("min-width",)),
    (r'\.topbar-account \[data-cc="sign-out"\]\s*\{([^}]*)\}', ("min-width",)),
    (r"\.session-field\s*\{([^}]*)\}", ("flex: 0 1 ", "min-width: 0")),
    (r"\.locale-field\s*\{([^}]*)\}", ("width:", "flex: none")),
    (r"\.topbar-right\s*\{([^}]*)\}", ("min-width: 0",)),
)


def account_bound_problems(css: str) -> list[str]:
    """Each logged-in piece of the top bar whose width can follow the language."""
    found = []
    for pattern, needed in ACCOUNT_BOUNDS:
        rule = re.search(pattern, css)
        body = rule.group(1) if rule else ""
        for want in needed:
            if want not in body:
                found.append(f"{pattern} lacks `{want}`")
    return found


def session_problems(js: str) -> list[str]:
    """The session line shows the bare name, and the sentence around it,
    which is the part that changes with the language, goes to a screen reader
    and to `title`. So the name is never cut off and the row cannot differ by
    language."""
    body = body_of(strip_comments(js), "function renderSession()")
    found = []
    if 'setText(el("session-user"), name);' not in body:
        found.append("the session line does not show the bare name")
    if 'setText(el("session-said"), said);' not in body:
        found.append("the session sentence does not reach a screen reader")
    if 'el("session-field").setAttribute("title", said)' not in body:
        found.append("the session sentence is not in a title")
    return found


def test_the_signed_in_top_bar_is_bounded_in_every_language() -> None:
    """The tagline was bounded already; the account group was left.

    Signed in, the bar kept one row at 1024px in English and took two in
    German ("Zugangsdaten", "Abmelden", "Angemeldet als" are each longer), and
    at 380px "Sign out" and the session line wrapped inside themselves in one
    language and not the other: 160.4px against 156.2px. Each piece now has a
    width the sentence cannot change: the buttons do not wrap and are at least
    as wide as the longer language needs, the language picker has a fixed
    width, and the session line takes a fixed share and ends in an ellipsis,
    with the whole sentence in its `title`. The heights were measured in
    Chromium at 1280/1024/800/380, both languages, signed in and out; this is
    the part of that a source read can hold.
    """
    css = strip_css_comments(source(APP_CSS))
    for problem in account_bound_problems(css):
        check(False, f"app.css: {problem}, so the signed-in bar can differ by language")
    # This replaced the ellipsis: the visible session text is the name alone,
    # which is the same in every language, so it is shown whole.
    for problem in session_problems(source(APP_JS)):
        check(False, problem)


def test_the_signed_in_bound_check_fires() -> None:
    """Seeded: the session line allowed to wrap, and a button allowed to wrap, must be found."""
    css = strip_css_comments(source(APP_CSS))
    js = source(APP_JS)
    seeded = js.replace('setText(el("session-user"), name);', 'setText(el("session-user"), said);')
    check(seeded != js, "the session-name probe's anchor has moved")
    check(bool(session_problems(seeded)),
          "a session line showing the language-dependent sentence is not caught")
    seeds = (
        ("a button wraps",
         "font-size: .85rem; white-space: nowrap; flex: none; }",
         "font-size: .85rem; }"),
        ("the session field loses its shrink bound",
         "  flex: 0 1 auto; min-width: 0; color: var(--ink-soft);\n",
         "  color: var(--ink-soft);\n"),
    )
    for what, anchor, replacement in seeds:
        seeded = css.replace(anchor, replacement)
        check(seeded != css, f"the signed-in bound probe's anchor has moved: {what}")
        check(account_bound_problems(seeded),
              f"an unbounded signed-in bar is not caught: {what}")

def test_the_limitation_check_fires_on_a_sentence_that_omits_it() -> None:
    """Seeded: a depth that hides its hole in the prose must be caught."""
    bland = "Extracts each source's claims and judges them in one call."
    check("invention" not in bland.lower(),
          "the probe's own sentence mentions invention, so it measures nothing")


def test_the_cost_falls_with_the_depth_and_is_counted_in_calls() -> None:
    """The entire reason to pick the cheap depth, and the reason it is not a price.

    `config.merge_model_calls` counts one merge call and one call per source at
    either depth, and three more at `full`. Six against three on a
    two-document merge, which is what `tests/test_cli.py` measures through the
    command against a real scripted endpoint.

    At `full` that six is a **floor**, not the price: `verify_claims` batches
    at 25 claims, so each of the two verify passes is one call per batch and a
    long pair of documents costs more, correcting an earlier figure. The fixtures all
    fit one batch each way, which is why measuring it agreed with publishing
    it. `coverage` has nothing to batch -- one fused call carries a whole
    source -- so there the figure is the number, and the page renders the two
    cases in different words off the `exact` flag it is served.

    It is a count of calls and not dollars because the calls are not the same
    size -- a fused coverage call carries the merged document a decompose call
    does not -- so a figure formed by scaling the model table's measured cost
    per merge would be invented. Naming what is exact and declining the rest is
    `pricing.py`'s rule, and this is the same rule applied to a different
    quantity.
    """
    cheap = [value for value, shape in config.VERIFY_DEPTH_SHAPES.items()
             if not shape.detects_invention]
    check(cheap, "no depth is cheaper than the default, so the picker offers "
                 "a choice with nothing on the other side of it")
    for value in cheap:
        for sources in (2, 3, 5):
            spent = config.merge_model_calls(value, sources)
            full = config.merge_model_calls(config.DEFAULT_VERIFY_DEPTH, sources)
            check(spent < full,
                  f"{value} over {sources} sources costs {spent} calls against "
                  f"{full}; a depth that checks less and costs the same is a "
                  f"strictly worse run")

    # The page forms the figure from both halves the server sends, so the count
    # is for the documents actually loaded rather than for an assumed two.
    body = js_function("callsAt")
    check("calls.fixed" in body and "calls.per_source" in body,
          "the page must price a depth from the fixed and per-source counts "
          "it was served")
    check("store.docs.length" in body,
          "and over the documents actually loaded: a merge of five documents "
          "costs five of the per-source calls, not two")

    # A floor rendered in the words of a quote is read as a quote. Both
    # spellings have to exist, the page has to choose between them from the
    # served flag rather than from the depth's name, and the floor's own
    # wording has to say it is one.
    strings = strings_table()
    for key in ("controls.depth.calls", "controls.depth.estimate"):
        check(f"{key}.atleast" in strings,
              f"{key} has no floor spelling, so a depth that batches would be "
              f"priced as though it did not")
    floor = strings.get("controls.depth.estimate.atleast", "")
    check("at least" in floor.lower(),
          f"the floor wording must say it is a minimum: {floor!r}")
    chooser = js_function("exactCalls")
    check("calls.exact" in chooser,
          "the page must choose the wording from the flag the server sends")
    for depth in config.VERIFY_DEPTHS:
        check(depth not in chooser,
              f"`exactCalls` names the depth {depth!r}; the page is served its "
              f"vocabulary and must not carry a depth's name in the function "
              f"that reads it")
    check("renderVerifyDepth()" in js_function("renderDocuments"),
          "adding or removing a document changes the price, so the picker has "
          "to be redrawn when the document set is")


def test_the_depth_delta_is_the_served_block_or_unmeasured() -> None:
    """**What the cheap depth costs in detection comes from `/config` or not at all.**

    The measured figures are the catalogue's `verify_depth` block, served
    as `quality_delta` and validated with its provenance on the server. With no
    block the page says "unmeasured" -- never a zero or a blank, which a reader
    completes as "no difference". `pricing.py` keeps this rule for costs, and it
    is the same rule applied to the figure this control most obviously invites.

    Asserted in the places where leaving one out makes the sentence true of the
    file and false of the page: the fallback string exists, says the word and
    is in the markup for a reader with the script blocked; the script chooses
    between the two states from the served field; every sentence it
    renders is a catalogue string; and the renderer composes no figure of its
    own and names no depth.
    """
    strings = strings_table()
    said = strings.get("controls.depth.unmeasured", "")
    check("measured" in said.lower(),
          f"the depth picker must state that the quality difference is "
          f"unmeasured when no figures are served, in words; got {said!r}")
    check("benchmark" in said.lower(),
          f"and say what is missing rather than leaving a gap: {said!r}")
    check("controls.depth.unmeasured" in html_text_by_key(source(INDEX)),
          "the sentence has to be in the markup, not only in the catalogue; "
          "this page renders its settings with the script blocked")

    # The sentence is chosen by the served field. It used to be a static
    # `data-t` binding, so a measured delta on the server would have left the
    # picker saying "unmeasured" and nothing would have gone red.
    body = js_function("renderDepthDelta")
    check("quality_delta" in body,
          "the paragraph under the picker must be chosen by /config's "
          "`quality_delta`; a static string cannot disagree with the server "
          "out loud")
    check('"unmeasured"' in body,
          "`renderDepthDelta` must branch on the one value that means there "
          "is no figure, rather than rendering whatever arrives")
    for key in ("controls.depth.unmeasured", "controls.depth.measured.keeps",
                "controls.depth.measured.saves", "controls.depth.measured.caveat"):
        check(key in body,
              f"`renderDepthDelta` must reach {key!r}; every sentence it shows "
              f"belongs to the catalogue and not to the script")
    check("delta.comparator" in body,
          "the measured depths are the block's entries against its comparator")
    # The benchmark sentence about what a depth cannot catch is gone
    # from the page; the option's own short line says it.
    check("controls.depth.cannot." not in body,
          "`renderDepthDelta` renders the removed sentence about what a depth "
          "cannot catch")
    for problem in depth_delta_arithmetic(body):
        check(False, problem)

    # And nothing else composes a score for a depth. The served rows carry
    # call counts and nothing else numeric (`tests/test_web_server.py` holds
    # that end); here it is the page. The renderer above is the one function
    # that may show a detection figure, and only the published ones.
    for name in DEPTH_FUNCTIONS:
        body = js_function(name)
        for word in ("accuracy", "score", "detection_rate", "quality"):
            check(word not in body,
                  f"{name} renders {word!r} for a depth; the measured figures "
                  f"are `renderDepthDelta`'s, read from the served block")


# Division, multiplication and the rounding helpers. `+` is left out on
# purpose: it builds the `controls.depth.cannot.` key from a served value.
DEPTH_ARITHMETIC = re.compile(r"[\w\])]\s*[/*]\s*[\w(]|Math\.|\.toFixed\(")


def depth_delta_arithmetic(body: str) -> list[str]:
    """Every place the depth renderer computes a figure rather than showing one."""
    return [f"`renderDepthDelta` computes a figure ({match.group(0)!r}); every "
            f"number it shows is a published field, formatted by `figure`"
            for match in DEPTH_ARITHMETIC.finditer(body)]


def test_the_depth_delta_arithmetic_check_fires() -> None:
    """Seeded: a rate formed in the renderer from two published counts."""
    seeded = source(APP_JS).replace(
        "caught: shown(mine.plants_detected),",
        "caught: shown(mine.plants_detected / mine.plants),")
    check(seeded != source(APP_JS), "the probe's anchor has moved")
    check(bool(depth_delta_arithmetic(js_function("renderDepthDelta", seeded))),
          "a division in the depth renderer is not caught")


def depth_brief_problems(tables: dict[str, dict[str, str]]) -> list[str]:
    """The picker says what a depth does not check in the option's own
    short line; the benchmark sentence that said it under the picker is gone,
    with its keys."""
    found = []
    for tag, strings in sorted(tables.items()):
        stale = sorted(key for key in strings if key.startswith("controls.depth.cannot."))
        if stale:
            found.append(f"{tag}.json still carries the removed sentence: {stale}")
        for value, shape in config.VERIFY_DEPTH_SHAPES.items():
            brief = strings.get(f"brief.depth.{value}", "")
            if not brief:
                found.append(f"{tag}.json has no short line for the {value} depth")
            elif not shape.detects_invention and tag == "en" and "invent" not in brief.lower():
                found.append(f"the {value} option's short line hides that it does not "
                             f"check for invention: {brief!r}")
    return found


def test_a_depth_that_misses_invention_says_so_in_its_option() -> None:
    """The limitation stays in the option, in one short line."""
    tables = catalogues()
    for problem in depth_brief_problems(tables):
        check(False, problem)
    seeded = {tag: dict(strings) for tag, strings in tables.items()}
    seeded["en"]["brief.depth.coverage"] = "Checks that nothing was lost."
    check(bool(depth_brief_problems(seeded)),
          "a coverage line that drops the invention caveat is not caught")
    seeded = {tag: dict(strings) for tag, strings in tables.items()}
    seeded["de"]["controls.depth.cannot.hallucination"] = "{depth} {missed} {plants}"
    check(bool(depth_brief_problems(seeded)),
          "the removed benchmark sentence coming back is not caught")
    body = js_function("renderVerifyDepth")
    check('t("brief.depth." + String(depth.value || ""))' in body,
          "the option does not render its short line")


def test_the_unmeasured_wording_check_fires() -> None:
    """Seeded: a picker that drops the word `measured` must fail."""
    said = "The cheaper depth makes fewer calls."
    check("measured" not in said.lower(),
          "a sentence that never says the difference is unmeasured passes the "
          "check, which would make it decoration")


def test_the_verdict_says_when_nothing_looked_for_invention() -> None:
    """Where a clean result is read, not only where the run is described.

    This is the project's most-repeated distinction -- "not checked" is not
    "checked and clean" (`sectionState`, whose chip vocabulary exists for
    exactly this) -- raised from one section to the whole run, because at this
    depth the reverse pass did not run at all. It sits beside `open`'s
    `advice.additions` for the same reason that one does: a caveat that appears
    only on a clean exit is a caveat missing from the report anyone reads
    carefully, so it goes on every verdict.
    """
    app = source(APP_JS)
    strings = strings_table()
    check("function suspendedGuarantee(" in app,
          "the sentence needs a function of its own; inlining it in the banner "
          "is how it ends up under one exit code")
    check("suspendedGuarantee(report)" in js_function("renderVerdict"),
          "and `renderVerdict` has to use it, on every exit code")
    body = js_function("suspendedGuarantee")
    check("merge_policy" in body and "verify_depth" in body,
          "the depth comes off the report's own provenance block, so a run "
          "opened from the history says what that run did rather than what "
          "the picker currently says")
    check('t("advice.noinvention")' in body,
          "the sentence is a catalogue string like every other sentence here")

    said = strings.get("advice.noinvention", "")
    check("invent" in said.lower(),
          f"the sentence has to name what was not checked: {said!r}")
    check("clean result" in said.lower(),
          f"and has to say what a clean result therefore means, which is the "
          f"whole point of raising it here rather than in provenance: {said!r}")

    # The provenance block carries it too, and that is not a duplicate: the
    # panel is what the run *was*, and this is what its verdict *means*.
    check('t("provenance.verify_depth")' in js_function("renderProvenance"),
          "the provenance panel must name the depth as well; the guard over "
          "`Provenance.as_dict`'s keys covers the field, and this covers the "
          "row a reader actually sees")


def test_a_clean_run_claims_only_the_directions_it_checked() -> None:
    """Found by driving the page, not by reading it.

    At `--verify-depth coverage` the verdict read *"Every claim in your
    documents survived into the merge, and nothing in the merge goes beyond
    them. 2 source claim(s) and 0 merged claim(s) were checked, in both
    directions."* -- over a run in which the merged document was never read
    back. The one sentence on the page that states outright what this depth
    does not check, said about a run that did not check it, with the
    suspended-guarantee sentence following two words later and contradicting
    it.

    The fix keys on the reverse count rather than on the depth, which is the
    more general statement: a `full` run whose reverse pass returned nothing is
    in exactly the same position, and the forward-only sentence is true of
    every way of arriving there. That is `sectionState`'s rule -- an empty list
    under a pass that did not run is not a clean result -- applied to the one
    line most readers stop at.
    """
    app = source(APP_JS)
    strings = strings_table()
    body = js_function("cleanAdvice", app)
    check('t("advice.clean.forward"' in body,
          "a clean run with no reverse verdicts needs a sentence of its own; "
          "`advice.clean` claims both directions unconditionally")
    check("if (!reverse)" in body,
          "and the branch has to be on the reverse count, so a full run whose "
          "reverse pass came back empty is covered by the same sentence")

    both = strings.get("advice.clean", "")
    forward = strings.get("advice.clean.forward", "")
    check("both directions" in both,
          f"the two-directional sentence no longer claims both directions, so "
          f"the split below is guarding nothing: {both!r}")
    check("both directions" not in forward and "beyond them" not in forward,
          f"the forward-only sentence still claims the reverse direction: "
          f"{forward!r}")
    check("{forward}" in forward and "{reverse}" not in forward,
          f"the forward-only sentence must count what was checked and must not "
          f"have a slot for what was not: {forward!r}")


def submitted_at_depth(depth: str) -> dict:
    """One merge through a real server at `depth`. Returns the finished payload."""
    with FakeEndpoint(Script(**COVERABLE)) as endpoint, \
            tempfile.TemporaryDirectory() as raw:
        environ = {"LLOSSLESS_BASE_URL": endpoint,
                   "LLOSSLESS_STRUCTURED": "prompt"}
        built, thread = live(environ=environ, work=Path(raw) / "work")
        try:
            base = origin(built)
            status, _, body = request(base + "/api/v1/runs", method="POST", payload={
                "documents": [{"name": "notes-a.md", "text": SOURCE_A},
                              {"name": "notes-b.md", "text": SOURCE_B}],
                "model": "test-model", "merge_model": "test-model",
                "verify_depth": depth,
            })
            if status != 202:
                return {"state": "refused", "status": status, "body": body}
            job_id = json.loads(body)["id"]
            deadline = time.time() + PATIENCE
            payload = {}
            while time.time() < deadline:
                _, _, raw_body = request(f"{base}/api/v1/runs/{job_id}")
                payload = json.loads(raw_body)
                if payload.get("state") in ("done", "failed"):
                    break
                time.sleep(0.1)
            _, _, events_body = request(f"{base}/api/v1/runs/{job_id}/events")
            payload["event_text"] = events_body.decode("utf-8")
            return payload
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


# The scripted endpoint's replies, plus the fused prompt's. `CLEAN` answers the
# four `full` prompts; a `coverage` run sends a fifth that `Script` dispatches
# on separately, and without a reply for it the cheap run errors and this
# comparison would be between a working depth and a broken one.
COVERABLE = dict(CLEAN)
COVERABLE["coverage"] = lambda n: json.dumps({"claims": [
    {"text": "The relay listens on port 8443.", "line": 1,
     "span": "The relay listens on port 8443", "verdict": "SUPPORTED",
     "evidence": "The relay listens on port 8443",
     "evidence_source": "merged.md", "rationale": "Checked against the merge."}]})


def test_both_depths_run_through_the_server_and_report_which_one_ran() -> None:
    """Two real runs, same session, same fixture, same module.

    A depth is only meaningful against the one it replaces, and "the cheap one
    records its hole" is two measurements: the hole has to be there at
    `coverage` and absent at `full`, or the check is passing on a report shape
    that never varies. Both arms are here rather than one here and one
    remembered from another file, for the reason
    `tests/test_cli.py:test_full_depth_is_unchanged_and_is_the_default` gives.

    Through the HTTP contract rather than through `pipeline`, because the web
    path had already been wired wrong once: the setting resolved,
    the flag existed, the branch worked, and the server passed none of it --
    which looked exactly like `full` running correctly.
    """
    arms = {depth: submitted_at_depth(depth) for depth in config.VERIFY_DEPTHS}
    for depth, payload in arms.items():
        check(payload.get("state") == "done",
              f"the {depth} run ended {payload.get('state')!r}: "
              f"{str(payload.get('error'))[:300]}")
        report = payload.get("report") or {}
        policy = ((report.get("provenance") or {}).get("merge_policy") or {})
        check(policy.get("verify_depth") == depth,
              f"the report of a {depth} run says it ran at "
              f"{policy.get('verify_depth')!r}; a run that cannot say which "
              f"questions it asked cannot be read against another one")
        # The banner reaches the browser as an event, and the depth has to be
        # one of its fields rather than something the page infers.
        frames = [json.loads(line[len("data: "):])
                  for line in payload.get("event_text", "").splitlines()
                  if line.startswith("data: ")]
        banners = [frame for frame in frames if frame.get("kind") == "banner"]
        check(banners and (banners[0].get("fields") or {}).get("depth") == depth,
              f"the {depth} run's banner event does not carry the depth: "
              f"{banners[:1]}")

        steps = {step["name"]: step for step in report.get("steps", [])}
        reverse = steps.get("verify (reverse)", {})
        shape = config.VERIFY_DEPTH_SHAPES[depth]
        if shape.detects_invention:
            check(reverse.get("state") == "ok",
                  f"at {depth} the reverse pass must run; it is "
                  f"{reverse.get('state')!r}")
        else:
            check(reverse.get("state") == "skipped",
                  f"at {depth} the reverse pass must be *recorded* as skipped "
                  f"rather than quietly absent; it is {reverse.get('state')!r}")
            check("invention" in str(reverse.get("detail", "")),
                  f"and the reason must name what went unchecked: "
                  f"{reverse.get('detail')!r}")

    # The two arms must differ, which is the half a single-arm check cannot
    # answer: a report shape that says `full` whatever was asked for would pass
    # every assertion above if only the `full` arm ran.
    depths = {payload.get("report", {}).get("provenance", {})
                     .get("merge_policy", {}).get("verify_depth")
              for payload in arms.values()}
    check(len(depths) == len(config.VERIFY_DEPTHS),
          f"both arms reported the same depth ({depths}); the setting is not "
          f"reaching the run through the server")


# --------------------------------------------------------------------------
# the operator's interface review, 2026-09-21
# --------------------------------------------------------------------------


class InputsAndLabels(HTMLParser):
    """Every `<input>` inside one element, and the label text over each.

    Written against the credentials sheet, where six fields were labelled by a
    `visually-hidden` span apiece. A screen reader heard them; the person
    typing did not -- *"there are two unlabeled fields. I suppose that is
    username and password or similar"*. Tracking nesting rather than matching
    a sibling pattern, because the two shapes in that sheet differ and a third
    should not have to come back here.
    """

    def __init__(self, inside: str) -> None:
        super().__init__(convert_charrefs=True)
        self._inside = inside
        self._depth = 0        # how deep inside the target element we are
        self._label: dict | None = None
        self._pending: list[dict] = []
        # hook -> (label attributes, label text)
        self.labels: dict[str, tuple[dict, str]] = {}
        self.inputs: list[dict] = []

    def handle_starttag(self, tag, attributes) -> None:
        attrs = dict(attributes)
        if attrs.get("data-cc") == self._inside:
            self._depth = 1
            return
        if not self._depth:
            return
        if tag not in ("meta", "link", "input", "br", "img", "hr"):
            self._depth += 1
        if tag == "label":
            self._label = {"attrs": attrs, "text": ""}
        if tag == "input":
            self.inputs.append(attrs)
            # The nearest label that has been opened and closed, or the one
            # wrapping this field. Either is an association a browser honours.
            if self._pending:
                self.labels[attrs.get("data-cc", "")] = self._pending[-1]
            elif self._label is not None:
                self.labels[attrs.get("data-cc", "")] = (self._label["attrs"],
                                                         self._label["text"])

    def handle_endtag(self, tag) -> None:
        if not self._depth:
            return
        if tag == "label" and self._label is not None:
            self._pending.append((self._label["attrs"], self._label["text"]))
            self._label = None
        if tag not in ("meta", "link", "input", "br", "img", "hr"):
            self._depth -= 1

    def handle_data(self, data) -> None:
        if self._label is not None:
            self._label["text"] += data


def test_every_field_in_the_credentials_sheet_carries_a_visible_label() -> None:
    """A label a sighted user cannot see is not a label to them.

    The operator opened Credentials, reached the row that adds an account and
    had to guess: *"I suppose that is username and password or similar. Can
    you label them properly?"* All six fields in that sheet were in the same
    state, and the two they hit were only the two they reached.

    Two defects, not one. The text was `visually-hidden`, which is a class for
    a label whose meaning is already carried by an icon or a heading and is
    the wrong answer for a bare text field. And `associate` was writing the
    generated `for` onto a `<span>`, where the attribute means nothing -- so
    the association the code claimed to make was being made by the `<label>`
    wrapped around the pair, and would have vanished the moment anybody
    unwrapped it.

    A placeholder is not accepted as the answer either: it disappears at the
    first keystroke, which is exactly when the field is being filled in.
    """
    html = source(INDEX)
    parser = InputsAndLabels("settings-dialog")
    parser.feed(html)
    # The provider rows are a `<template>`, which is markup the sheet clones
    # rather than markup inside it, so both are read. The operator met four of
    # these six on one screen.
    rows = InputsAndLabels("tpl-provider")
    rows.feed(html)
    parser.inputs += rows.inputs
    parser.labels.update(rows.labels)
    check(len(parser.inputs) >= 6,
          f"the sheet should hold at least six fields; found "
          f"{len(parser.inputs)}")
    for field in parser.inputs:
        hook = field.get("data-cc", "")
        check(hook in parser.labels, f"the {hook!r} field has no label at all")
        attrs, text = parser.labels.get(hook, ({}, ""))
        classes = (attrs.get("class") or "").split()
        check("visually-hidden" not in classes,
              f"the {hook!r} field's label is visually hidden; the operator "
              f"had to guess what to type into two of these")
        check(bool(text.strip()),
              f"the {hook!r} field's label carries no text")
        check(bool(attrs.get("data-t")),
              f"the {hook!r} field's label is not in the catalogues, so it "
              f"stays English on a German page")
        check(not field.get("placeholder") or hook == "provider-url",
              f"the {hook!r} field leans on a placeholder; a placeholder is "
              f"gone the moment somebody types into the field")

    # The generated `for` has to land on a `<label>`. Writing it onto a span
    # is the silent half of this defect and would survive any check that only
    # looked at whether the attribute was set.
    app = source(APP_JS)
    for hook in ("provider-url-label", "provider-input-label",
                 "new-account-name-label", "new-account-password-label",
                 "current-password-label", "new-password-label"):
        check(f'data-cc="{hook}"' in html, f"{hook} is gone from the markup")
        opening = html[:html.index(f'data-cc="{hook}"')].rsplit("<", 1)[-1]
        check(opening.startswith("label"),
              f"{hook} is on a <{opening.split()[0]}>, and `for` on anything "
              f"but a <label> is inert")
        check(f'associate(' in app and hook in app,
              f"{hook} is never associated with its field")


def test_a_command_route_is_never_silently_the_second_choice() -> None:
    """Two mechanisms preselect the subscription, and neither may vanish quietly.

    The two mistakes are not symmetric: firing at a metered API when you
    believed you were on a plan spends money you did not mean to spend, and the
    reverse costs a run against a plan you are already paying for. So a command
    route is preselected where one exists, and there is no arrangement of this
    page in which the metered row is the default while a command route sits
    above it.

    **Both mechanisms are pinned by source here, and that is the point of this
    check rather than an accident of how it is written.** Driving the page
    catches the two of them together and neither of them alone -- `pickable`
    puts command routes first, so `renderModels` finding "the first reachable
    row" finds one anyway, and deleting either leaves the browser check green.
    A seeded run proved exactly that, and a defence that is only
    observable when both halves are gone is a defence one half of which can be
    removed in a refactor with nothing going red.
    """
    app = source(APP_JS)
    rows = js_function("pickable", app)
    check("rows.unshift(" in rows,
          "command routes must go to the *front* of the one list; a route that "
          "costs nothing per token belongs above the rows that do")
    picker = js_function("renderModels", app)
    check("reachable(model) && routeOf(model)" in picker,
          "the preselection must prefer a command route explicitly, rather "
          "than relying on the order `pickable` happens to build")
    check("|| models.find(" in picker,
          "and must still fall back to the first reachable row where there is "
          "no command route, which is every deployment until an operator "
          "writes a routes file")
    # Must-fire: the probe has to be able to see its own anchors missing.
    check("reachable(model) && routeOf(model)" not in
          picker.replace("reachable(model) && routeOf(model)", "..."),
          "the probe cannot see its own anchor, so the check above passed over "
          "nothing")


def test_a_command_route_is_one_selection_and_not_two() -> None:
    """The label on the button and the field in the body read one value.

    "It needs to be simple for the user to pick the correct one and to be clear
    which one is selected so they don't get bad surprises when they think they
    fire against the sub when in reality we would accidentally burn tokens."

    A model picker with a route toggle beside it is a second piece of state to
    misread, which is the failure being described. So there is one selection --
    `store.mergeModel`, holding either a catalogue id or a prefixed route id --
    and `chosenRoute` is the only thing that reads a route out of it. The
    button's label and the submitted body both go through it, so a page showing
    one route and sending another is not a state this file can be edited into
    without deleting one of the two calls.
    """
    app = source(APP_JS)
    check(app.count("function chosenRoute(") == 1,
          "there must be exactly one reader of the route selection")
    submission = js_function("submission", app)
    check("command_route: chosenRoute() || undefined" in submission,
          "the request must carry the route from the one reader")
    check("command:" not in submission,
          "the request body must never carry a command")
    kind = js_function("chosenRouteKind", app)
    check("store.mergeModel" in kind,
          "the button's route word must come from the same selection the "
          "request carries, not from a second field")
    check("COMMAND_PREFIX" in js_function("chosenRoute", app),
          "the route is read off the prefixed row id, which is what makes the "
          "route and the model one choice rather than two")


def test_the_run_button_shows_a_spinner_and_also_says_so() -> None:
    """The only in-flight signal was the word RUNNING at .78rem.

    A merge takes between 23 and 4,559 seconds. The button greyed out and the
    status line beside it changed a word; the operator's report was that it
    "is easy to miss". Colour and motion still never carry it alone, which is
    this page's standing rule: the label on the button changes with the
    spinner, and `aria-busy` says the same to a reader who sees neither.
    """
    app = source(APP_JS)
    body = js_function("setRunning", app)
    check('el("submit-spinner").hidden = !running' in body,
          "the spinner has to be shown and hidden by the run state")
    check('running ? t("run.running") : submitLabel()' in body,
          "and the label has to change with it, because an animation is not "
          "a word and this page never signals with one alone")
    # The idle half of that label names the route, which is the highest-
    # value disclosure: the irreversible moment is the click, and the control
    # at that moment used to say the same five words whether the next four
    # minutes billed a metered API or spent a subscription.
    check('t("run.submit.route", { route: routeLabel(chosenRouteKind()) })'
          in js_function("submitLabel", app),
          "the idle label must name the route, from the same selection the "
          "request carries")
    # And through `routeLabel`, which is total. The expression here used to
    # build the key -- `t("route." + chosenRouteKind())` -- which renders a
    # kind the catalogues have no string for as the key itself, and was the
    # shape that let `metered` stand in for every route this page could not
    # classify. `routeLabel` throws on a kind it has no label for, and
    # `test_every_route_kind_has_a_label` is what keeps that unreachable.
    check('t("route." + ' not in app,
          "no route word may be built from a concatenated key; `routeLabel` "
          "is the one reader and it is exhaustive")
    check('aria-busy' in body,
          "a screen reader sees no spinner; `aria-busy` is what it gets")
    check("button.disabled = running" in body,
          "and the button must refuse a second press while the first is in "
          "flight")
    strings = strings_table()
    check("run.running" in strings, "the running label is not in the catalogue")
    # The submit handler must go through it rather than setting `disabled`
    # itself, which is what every re-enable site used to do.
    submit = js_function("submit", app)
    check("setRunning(true)" in submit,
          "`submit` must raise the run state through the one function that "
          "owns it")
    check(app.count("(el(\"submit\")).disabled = false") == 0,
          "nothing may lower `disabled` behind `setRunning`'s back; that is "
          "how the spinner outlives the run")


def route_kinds_in_js() -> list[str]:
    """The kinds `app.js` declares, read out of `const ROUTE_KINDS = [...]`."""
    js = strip_comments(source(APP_JS))
    # Past the `[`, or the declaration's own name is parsed as a member.
    start = js.index("const ROUTE_KINDS = [") + len("const ROUTE_KINDS = [")
    end = js.index("]", start)
    names = re.findall(r"ROUTE_([A-Z]+)", js[start:end])
    return [name.lower() for name in names]


def route_label_keys_in_js(js: str = None) -> dict[str, str]:
    """The `ROUTE_LABEL_KEYS` table, as a mapping from kind to catalogue key."""
    text = strip_comments(source(APP_JS) if js is None else js)
    start, end = block(text, "const ROUTE_LABEL_KEYS = {")
    return dict(re.findall(r'(\w+):\s*"([^"]+)"', text[start:end]))


def label_map_problems(kinds, labels, strings) -> list[str]:
    """Every way the kinds, the label table and a catalogue disagree.

    A predicate rather than a test body, so the seeded probes below drive the
    same expression the live check does. A probe that re-implements the rule
    it is probing proves only that the copy fires.
    """
    problems = []
    missing = sorted(set(kinds) - set(labels))
    if missing:
        problems.append(f"route kind(s) {missing} have no entry in "
                        f"ROUTE_LABEL_KEYS, so the button would render a blank "
                        f"where the route belongs")
    orphan = sorted(set(labels) - set(kinds))
    if orphan:
        problems.append(f"ROUTE_LABEL_KEYS names {orphan}, which is not in "
                        f"ROUTE_KINDS")
    for kind in sorted(set(kinds) & set(labels)):
        if labels[kind] not in strings:
            problems.append(f"route kind {kind!r} reads {labels[kind]!r} and "
                            f"the catalogue has no such string")
    return problems


def test_every_route_kind_has_a_label_and_every_label_has_a_string() -> None:
    """The guard the operator asked for, and the reason it is worth having.

    *"When we are on local we should say this too like 'Merge and check -
    local'. That makes it safe in each case."* The value of the button naming
    its route is destroyed by the button naming *some* routes: a label that
    appears for two cases out of three teaches a reader that its absence means
    nothing in particular, which is worse than no label at all.

    So the set of kinds and the set of labels are asserted equal, the way
    `merge.MAY_CHOOSE` and `report.FINDING_ORDER` are asserted against their
    consumers on the Python side. `app.js` runs the same comparison when it
    loads and throws; this is the copy that fails in CI instead of in a
    browser, and it goes one step further by checking each key against the
    catalogue -- a mapped kind whose string does not exist would render the
    key.
    """
    kinds = route_kinds_in_js()
    check(len(kinds) >= 4, f"only {kinds} parsed out of ROUTE_KINDS")
    for problem in label_map_problems(kinds, route_label_keys_in_js(),
                                      strings_table()):
        check(False, problem)


def test_the_route_label_guard_fires_in_three_directions() -> None:
    """Seeded: a kind with no label, a label with no kind, a label with no string.

    The first is the regression this exists for -- a fifth route class added
    to the constants and not to the table -- and it is the one the operator
    named: adding a route must fail here rather than ship a blank.
    """
    kinds = route_kinds_in_js()
    labels = route_label_keys_in_js()
    strings = strings_table()
    check(not label_map_problems(kinds, labels, strings),
          "the predicate fires on the shipped tables")

    short = {kind: key for kind, key in labels.items() if kind != "selfhosted"}
    check(any("selfhosted" in problem
              for problem in label_map_problems(kinds, short, strings)),
          "a route kind dropped from the label table is not found")

    extra = dict(labels)
    extra["invented"] = "route.invented"
    check(any("invented" in problem
              for problem in label_map_problems(kinds, extra, strings)),
          "a label for a kind that does not exist is not found")

    wrong = dict(labels)
    wrong["metered"] = "route.nosuchstring"
    check(any("nosuchstring" in problem
              for problem in label_map_problems(kinds, wrong, strings)),
          "a label key the catalogue has no string for is not found")


# --------------------------------------------------------------------------
# the Check column offers only what the merge's route can reach
# --------------------------------------------------------------------------

# Found by driving the page: with the split on under a metered merge, the Check
# column had a live radio on every subscription row, and picking one sent that
# route's model name, as a model, down the metered route -- `haiku` to the
# server's own endpoint, where it failed, and on an operator route whose model
# is `claude-opus-5`, to the metered API itself -- while the button named the
# metered API alone. The server cannot refuse it: the request is byte for byte
# one a reader makes by picking the metered row. So the
# page owns it, in four places, and each is pinned here and seeded below.


def check_route_problems(js: str) -> list[str]:
    """Every way the page stops keeping the checks on the merge's route."""
    js = strip_comments(js)
    problems = []
    cell = js_function("checkCell", js)
    disabled = next((line for line in cell.splitlines()
                     if "radio.disabled =" in line), "")
    if "answersChecks(model)" not in cell or "!answers" not in disabled:
        problems.append("checkCell offers a row the merge's route cannot reach: "
                        "its radio is not disabled by answersChecks")
    rule = js_function("answersChecks", js)
    if "chosenRoute()" not in rule or "routeOf(model)" not in rule:
        problems.append("answersChecks no longer decides by the merge's route "
                        "and the row's")
    render = js_function("renderModels", js)
    if ("answersChecks(checking)" not in render
            or "store.checkModel = store.mergeModel" not in render):
        problems.append("renderModels keeps a check selection the Check column "
                        "would not offer")
    blocked = js_function("unreachableChoice", js)
    if ("!answersChecks(check)" not in blocked
            or 't("models.split.blocked"' not in blocked):
        problems.append("the submit button is not refused for a check row the "
                        "merge's route cannot reach")
    label = js_function("submitLabel", js)
    if ("check !== chosenRouteKind()" not in label
            or 't("run.submit.split"' not in label):
        problems.append("the button names the merge's route alone when the "
                        "checks are billed differently")
    if "store.checkModel" not in js_function("checkRouteKind", js):
        problems.append("checkRouteKind does not read the selection the request "
                        "sends for the checks")
    shown = js_function("renderProvenance", js)
    if "endpoint.billed" not in shown or 't("provenance.route")' not in shown:
        problems.append("the provenance panel does not say how each role was "
                        "billed")
    return problems


def test_the_check_column_offers_only_what_the_merges_route_can_reach() -> None:
    """The pairing the engine cannot run is not offered, sent or unnamed."""
    for problem in check_route_problems(source(APP_JS)):
        check(False, problem)
    # One vocabulary before the click and after it: the button's kinds are the
    # server's recorded kinds, and the report's words are the button's.
    from llossless import provenance
    from llossless.web import jobs
    check(set(route_kinds_in_js()) == set(jobs.ROUTE_KINDS),
          f"the page's route kinds {sorted(route_kinds_in_js())} and the ones "
          f"the server records {sorted(jobs.ROUTE_KINDS)} differ")
    labels = route_label_keys_in_js()
    strings = strings_table()
    for kind in jobs.ROUTE_KINDS:
        check(provenance.ROUTE_WORDS.get(kind) == strings.get(labels.get(kind, "")),
              f"the report calls the {kind} route "
              f"{provenance.ROUTE_WORDS.get(kind)!r} and the page's button "
              f"calls it {strings.get(labels.get(kind, ''))!r}")


def test_the_check_column_guard_fires_on_each_piece_removed() -> None:
    """Seeded against the shipped functions, one piece at a time."""
    js = source(APP_JS)
    check(not check_route_problems(js), "the shipped page fails its own check")
    for piece, seed, what in (
            (" || !answers;", ";", "the disabled radio"),
            ("!answersChecks(checking)", "false", "the re-join in renderModels"),
            ("!answersChecks(check)", "false", "the refusal on the button"),
            ("if (check !== chosenRouteKind()) {", "if (false) {",
             "the two-route label"),
            ("store.checkModel);\n  return routeKind(model);",
             "store.mergeModel);\n  return routeKind(model);",
             "the check role's own route"),
            ("endpoint.billed", "endpoint.nothing", "the provenance row")):
        check(piece in js, f"the probe cannot find {what}: {piece!r}")
        check(bool(check_route_problems(js.replace(piece, seed))),
              f"{what} removed is not caught")


def test_the_page_never_falls_through_to_a_route_it_did_not_establish() -> None:
    """Three classifiers, and none of them answers `metered` from an absence.

    This is the defect the operator's message describes from the other side. A
    picked row with no match, a typed model with no endpoint named, and a
    provider row that is not literally called `self-hosted` all used to read as
    a metered API -- a claim about where the money goes, made where the page
    had nothing to go on. The classification now comes from the server's own
    `discover.kind_of`, and the unclassifiable case has a word of its own.
    """
    app = source(APP_JS)
    kind = js_function("routeKind", app)
    check("ROUTE_UNKNOWN" in kind,
          "`routeKind` must have an answer for a row it cannot classify")
    chosen = js_function("chosenRouteKind", app)
    check("ROUTE_METERED" not in chosen,
          "`chosenRouteKind` must not name a route kind directly; every "
          "answer comes from a row or from the server's classification")
    typed = js_function("typedModelKind", app)
    check("default_kind" in typed,
          "a typed model with no endpoint named goes to the server's default, "
          "so the label has to read the server's word for that default")
    check("provider.kind" in typed,
          "and a named endpoint's kind is the server's, not a test on the "
          "provider's name")
    # The server's vocabulary and the page's are the same three words for the
    # two they share. A rename on one side that missed the other would make
    # every endpoint read `unknown`.
    check(discover.KIND_SELFHOSTED in route_label_keys_in_js()
          and discover.KIND_METERED in route_label_keys_in_js()
          and discover.KIND_UNKNOWN in route_label_keys_in_js(),
          f"the server classifies endpoints as "
          f"{discover.KIND_SELFHOSTED}/{discover.KIND_METERED}/"
          f"{discover.KIND_UNKNOWN} and the page has no label for one of them")


def test_start_over_never_clears_anything_without_asking() -> None:
    """The confirmation is the control; `startOver` is only its consequence.

    The operator asked for a way to begin again without reloading, *"with a
    confirmation dialog warning that data will be cleared/lost"*. So the
    button is wired to the question and not to the clearing, and every way of
    dismissing the question -- the other button, Escape, the backdrop --
    resolves to keeping everything.
    """
    app = source(APP_JS)
    check('el("start-over").addEventListener("click", () => void confirmStartOver())'
          in app,
          "the button must be wired to the question, not to the clearing")
    body = js_function("confirmStartOver", app)
    check("if (answer) startOver()" in body,
          "and the clearing must happen only on the affirmative answer")
    check("dialog.onclose = () => finish(false)" in body,
          "Escape and the backdrop are dismissals; a dialog that cleared the "
          "form on Escape would be worse than no dialog")
    # One call site. A second one somewhere else is a path around the question.
    check(app.count("startOver()") == 2,
          f"`startOver` is called {app.count('startOver()') - 1} time(s) "
          f"outside its own definition; there is exactly one way to it and it "
          f"goes through the dialog")
    strings = strings_table()
    for key in ("confirm.startover.heading", "confirm.startover.text",
                "confirm.startover.ok", "confirm.keep", "run.startover"):
        check(key in strings, f"{key} is not in the catalogue")
    # `window.confirm` would put two untranslatable buttons on a page whose
    # every other string is in a catalogue. Matched on a word boundary, so
    # `confirmStartOver(` is not mistaken for a call to the native one.
    code = strip_comments(app)
    native = re.findall(r"(?<![A-Za-z.])confirm\s*\(", code)
    check("window.confirm" not in code and not native,
          f"a native confirm paints its buttons in the browser's language, "
          f"which no catalogue on this server can reach: {native}")


def test_every_download_goes_through_a_fetch_that_can_report_a_refusal() -> None:
    """The operator's report: *"user only gets failed downloads"*, and nothing said.

    An `<a download href="...">` pointed at a route has no failure path. A
    non-200 is not saved, not rendered and not reported -- the click simply
    does nothing -- and the only control that did explain itself was the
    "Full report" link, because that one navigates and the browser renders the
    JSON body. So the one route with a sentence in it was the one they were
    least likely to click.

    What this pins is the shape of the fix rather than its wording: every
    download anchor is wired through one function, and that function looks at
    the status before it saves anything.
    """
    app = source(APP_JS)
    code = strip_comments(app)
    wiring = js_function("wire", app)
    for hook, route in (("download-merged", "ROUTES.merged"),
                        ("download-report", "ROUTES.report"),
                        ("download-bundle", "ROUTES.bundle")):
        check(f'wireDownload(el("{hook}"), {route})' in wiring,
              f"{hook} is not wired through `wireDownload`, so a refusal on it "
              f"is a click that does nothing")
    saver = js_function("saveFrom", app)
    check("await fetch(" in saver,
          "the save must fetch the artefact, or there is nothing to check")
    check("if (!answer.ok)" in saver,
          "`saveFrom` does not look at the status; a refused download would "
          "be silent again")
    check("errorMessage(body, answer.status)" in saver,
          "a refusal must reach the reader in the server's own words -- which "
          "is where the sentence naming the retention flag comes from")
    check("forgetShownRun()" in saver,
          "a 410 must also take the dead controls off the page; three buttons "
          "that all answer 410 is the same bug with more clicks")
    check("URL.createObjectURL" in saver and "anchor.download = filename" in saver,
          "the fetched bytes must be handed over as a file, or the fetch has "
          "replaced a working download with a checked one that saves nothing")
    # And the anchors still name the routes they point at, so a reader copying
    # a link address gets the artefact rather than the page.
    body = js_function("showResult", app)
    check("everything.href = route(ROUTES.bundle, { id: id })" in body,
          "the bundle control must point at the bundle route")
    check('bundle: "/api/v1/runs/{id}/bundle.zip"' in code,
          "the bundle route is not in the route table in that spelling")


def test_the_download_failure_check_fires_when_the_status_goes_unread() -> None:
    """Seeded on the shipped function: the `ok` branch taken back out of it.

    That is the state the page was in when the operator met this, so the probe
    is the regression rather than a resemblance to it.
    """
    saver = js_function("saveFrom", source(APP_JS))
    seeded = saver.replace("if (!answer.ok)", "if (false && !answer.ok)")
    check(seeded != saver, "the seeded probe did not take")
    check("if (!answer.ok)" not in seeded,
          "removing the status check does not fail the check above")


def test_the_page_is_told_the_retention_window_and_never_writes_one_down() -> None:
    """How long a run is kept is this server's setting, not this tool's.

    A page carrying "deleted after an hour" would be wrong on every deployment
    that passed `--retention`, and wrong silently -- which is the same class of
    defect as the document bounds this page refuses to guess: it renders
    nothing until `/config` has told it, and `0` rather than the real number is
    what it falls back to there.
    """
    app = source(APP_JS)
    code = strip_comments(app)
    reader = js_function("retentionBlock", app)
    check("store.config" in reader and "retention" in reader,
          "the window must come from `/config`")
    check("undefined" in reader,
          "a page that has not been told the window must say nothing, rather "
          "than fall back to a number nobody configured")
    render = js_function("renderRetention", app)
    # The four states, as four catalogue keys. A window rendered as one
    # sentence with a number in it would make "kept until you delete them" and
    # "deleted in two days" the same sentence with a very large number.
    for key in ("retention.window", "retention.window.only", "retention.off",
                "retention.soon", "retention.gone"):
        check(f't("{key}"' in render,
              f"{key} is not rendered; the four retention states are four "
              f"sentences, not one with a number in it")
    check("retentionWarnAt()" in render,
          "the page must warn at the threshold the server serves, not at one "
          "it picked")
    warn = js_function("retentionWarnAt", app)
    check("warn_seconds" in warn,
          "the warning threshold must come from `/config`; derived from the "
          "window there, so it still makes sense at `--retention 600`")
    # No hour, day or minute count written into the script. The spans are
    # chosen by unit, and the numbers in them are divisors rather than
    # thresholds somebody picked.
    check("86400" not in render and "3600" not in render,
          "`renderRetention` carries a time constant of its own; the window "
          "and the threshold are both the server's")


def test_the_countdown_subtracts_elapsed_time_and_never_two_clocks() -> None:
    """Clock skew, answered in the shape of the data rather than by tolerating it.

    The server sends seconds remaining. A page that instead subtracted
    `finished_at` from `Date.now()` would be measuring the gap between the
    browser's clock and the server's as well as the gap between two moments --
    and the laptop half an hour out is the ordinary case, not the exotic one.
    """
    app = source(APP_JS)
    left = js_function("remaining", app)
    check("store.expiresIn" in left and "monotonic()" in left,
          "the countdown must be the server's remaining seconds minus elapsed "
          "time here")
    check("finished_at" not in left and "Date.now()" not in left,
          "the countdown reads a clock it should not: a difference between "
          "two machines' clocks is not a duration")
    clock = js_function("monotonic", app)
    check("performance" in clock,
          "the elapsed reading must come from a monotonic clock, or an NTP "
          "step moves the countdown with it")
    note = js_function("noteExpiry", app)
    check("expires_in" in note and "forgotten_at" in note,
          "the page must read both the countdown and the tombstone flag; "
          "`expires_in` is null for a forgotten run and for a server that "
          "deletes nothing, and those are not the same state")
    forget = js_function("forgetShownRun", app)
    check("store.forgotten = true" in forget,
          "a 410 must outrank the countdown -- a suspended tab under-counts, "
          "so the server's answer is the one that decides")


def test_the_report_downloads_as_one_file() -> None:
    """Saving the report must not depend on the browser's Save Page As.

    The operator's words: it *"does not always offer this"* and *"feels
    clumsy"*. `html_report.render` is already one document with its stylesheet
    inline and nothing fetched, so the download is those bytes and nothing
    else -- one renderer, which is what would have drifted.

    Two routes, though, and the second one arrived when the operator asked the
    same question about the report page itself: *"I thought I mentioned that I
    want a download button on the report page too"*. `report.html` is the file
    and `report` is the page that shows it, and the page is the only copy that
    carries a control -- one it fills with the report itself, because a
    sandboxed page cannot ask this server for anything (`api.report_page`).

    The self-contained half is asserted against a rendered report rather than
    against the docstring that claims it: the same off-box scan the shipped
    files get, over the bytes a reader would open from their disk.
    """
    html = source(INDEX)
    check('data-cc="download-report"' in html and 'download="report.html"' in html,
          "the download anchor is missing or does not name the file")
    app = source(APP_JS)
    body = js_function("showResult", app)
    check('save.href = route(ROUTES.report, { id: id })' in body,
          "the download must point at the report route the server already "
          "serves; a second renderer is a second report")
    check('open.href = route(ROUTES.reportPage, { id: id })' in body,
          "the View report link must open the page that carries the control; "
          "pointed at the file it opens the one copy with no way to save "
          "itself -- which is the complaint this route exists to answer")
    check('reportPage: "/api/v1/runs/{id}/report"' in app
          and 'report: "/api/v1/runs/{id}/report.html"' in app,
          "the two routes are the file and the page, in that spelling")

    rendered = html_report.render(_clean_run())
    hits = off_box_hits(rendered)
    check(not hits,
          f"the downloaded report reaches off this machine: {hits}. It is "
          f"opened from a disk, and a stylesheet or font fetched over a "
          f"network the reader does not have is a report that does not render")
    check("<style" in rendered,
          "the stylesheet has to be inline, or the file is not self-contained")
    # An inline `<script>` is self-contained and stays: it is the report's
    # own filter box and it fetches nothing. What may not appear is a script
    # or a stylesheet that names a source, which is the thing a disk with no
    # network cannot supply.
    check("<script src" not in rendered and 'rel="stylesheet"' not in rendered,
          "no external asset; this file is opened from a disk")


def _clean_run():
    """A `Run` with one carried claim and one dropped one. Local to two checks."""
    run = report.Run(command="merge",
                     paths={"source_a.md": "source_a.md",
                            "source_b.md": "source_b.md"},
                     merged="# t\n\nbody\n", segments=1)
    claim = decompose.Claim
    run.claims = {
        "source_a.md": [claim("A-001", "source_a.md", "a carried claim", 1, "a carried claim", True)],
        "merged.md": [claim("M-001", "merged.md", "a merged claim", 1, "a merged claim", True)],
    }
    run.forward = [verify.Verdict("A-001", "MISSING", "", "", "not there",
                                  verify.SOURCE_TO_MERGED, verify.NOT_GRADED)]
    run.reverse = [verify.Verdict("M-001", "SUPPORTED", "a merged claim",
                                  "source_a.md", "it is stated",
                                  verify.MERGED_TO_SOURCES, verify.GROUNDED)]
    return run


def test_a_rationale_says_which_document_it_was_written_about() -> None:
    """The word "reference" means opposite documents in the two directions.

    The operator read a finding whose rationale said *"The reference describes
    the group as easy-to-remember words, not letters"* and asked: *"What is
    the 'reference' here? Source document 1?"* -- then, on a second one, *"it
    appears that the reference is the merged document? Or is that outside
    knowledge?"*

    Both were forward verdicts, so both meant `merged.md`. The word is the
    prompt's: `prompts/verify.md` calls the merged document the reference text
    and `prompts/verify_reverse.md` gives the same role to the sources. The
    rationale is the model's own prose and all three surfaces print it
    verbatim, so the fix is beside it rather than inside it.

    The prompts are not touched, and that is the decision rather than an
    omission: `prompt_sha256` is a cassette key component and 334 recorded
    verify responses would be re-keyed by a word change, taking the offline
    replay of the whole corpus with them.
    """
    app = source(APP_JS)
    item = js_function("verdictItem", app)
    check('t("detail.against")' in item,
          "each finding on the page has to name the document it was judged "
          "against; the operator asked twice and the answer was on no surface")
    against = js_function("judgedAgainst", app)
    check('direction !== "merged_to_sources"' in against,
          "the answer is the direction's, and the direction is on the verdict")
    check("report.documents" in against,
          "the reverse direction's answer is every source, by the label the "
          "submitter gave it")
    # The page's one literal for the engine's own document name, pinned.
    check(f'const MERGED_DOCUMENT = "{segment.MERGED_NAME}"' in app,
          f"the page's merged-document name must be {segment.MERGED_NAME!r}, "
          f"which is `segment.MERGED_NAME`")
    strings = strings_table()
    for key in ("detail.against", "detail.against.sources", "results.judged"):
        check(key in strings, f"{key} is not in the catalogue")
    # And the note that answers the second question, which is about outside
    # knowledge rather than about which file. It says what the prompt asks for
    # and says that nothing here checks it -- claiming the model ignored what
    # it knows would be an assertion with no check behind it.
    note = strings["results.judged"]
    check("prove" in note or "cannot" in note,
          f"the note must not claim outside knowledge was ruled out; nothing "
          f"here checks that: {note!r}")
    check('el("judged-note").hidden = (report.verdicts || []).length === 0' in app,
          "a sentence about how verdicts were reached, over a run with no "
          "verdicts, is furniture")

    # Both written reports say it too, and say it the same way.
    run = _clean_run()
    markdown = report.render(run)
    page = html_report.render(run)
    check("checked against: `merged.md`" in markdown,
          f"the markdown finding does not name the document it was judged "
          f"against")
    check("Checked against" in page and "<code>merged.md</code>" in page,
          "the HTML finding card does not name it")
    check(report.REFERENCE_NOTE in markdown,
          "the markdown findings section needs the note about what the "
          "rationales are written against")
    for text in (markdown, page):
        check("read against" in text,
              "the inventory tables print the rationale in a Note column and "
              "have to caption which document it is about")


def test_the_judged_against_checks_fire() -> None:
    """Must-fire, for the three above. A detector nobody has broken is a claim.

    Each probe is the shipped source with one thing removed, run through the
    same predicate the check uses -- not a re-implementation of it.
    """
    app = source(APP_JS)
    html = source(INDEX)

    # The finding stops naming the document.
    broken = app.replace('t("detail.against"), judgedAgainst(report, verdict.direction)',
                         't("detail.source"), ""')
    check('t("detail.against")' not in js_function("verdictItem", broken),
          "the judged-against probe did not change what it was aimed at")

    # The spinner is shown and the word is not changed with it.
    broken = app.replace('t(running ? "run.running" : "run.submit")',
                         't("run.submit")')
    check('t(running ? "run.running" : "run.submit")'
          not in js_function("setRunning", broken),
          "the label probe did not change what it was aimed at")

    # A second path to the clearing, around the dialog.
    broken = app.replace('el("start-over").addEventListener("click", () => void confirmStartOver())',
                         'el("start-over").addEventListener("click", () => startOver())')
    check(broken.count("startOver()") == 3,
          "the unconfirmed-path probe did not add a second call site")

    # The label goes back to being hidden.
    broken = html.replace('<label data-cc="new-account-name-label"',
                          '<label class="visually-hidden" data-cc="new-account-name-label"')
    parser = InputsAndLabels("settings-dialog")
    parser.feed(broken)
    attrs, _ = parser.labels.get("new-account-name", ({}, ""))
    check("visually-hidden" in (attrs.get("class") or "").split(),
          "the hidden-label probe did not hide the label the check reads")

    # The report gains an external asset.
    rendered = html_report.render(_clean_run())
    seeded = rendered.replace(
        "<style", '<link rel="stylesheet" href="https://example.invalid/a.css"><style')
    check(off_box_hits(seeded),
          "the self-contained probe did not put a reachable asset in the "
          "report the scan reads")


def test_the_result_actions_read_view_then_save_narrow_then_wide() -> None:
    """The operator's order, and the label that named a size.

    Their report: *"the rows 'Download report / Download everything / Full
    report' have the wrong order. It should be 'View report', 'Download
    report' and 'Download everything'."* Two faults in one group. The free
    action sat last, after two controls that put a file on somebody's disk;
    and `Full report` named a *size* where its three neighbours name an
    *action*, which is what made it read as a fourth kind of download rather
    than as the thing you do before deciding to save one.

    Asserted on the document order rather than on a rendered page, because
    that is where the order is decided -- the script fills these anchors in
    and never reorders them. Seeded by swapping two.
    """
    markup = source(INDEX)
    # `copy-merged` joins the front of the group on the same rule: the
    # free action goes before the ones that put a file on a disk, and copying
    # does not even open a window.
    wanted = ["copy-merged", "download-merged", "open-report",
              "download-report", "download-bundle"]
    found = [name for name in re.findall(r'data-cc="([a-z-]+)"', markup)
             if name in wanted]
    check(found == wanted,
          f"the result actions must read copy, markdown, view, report, "
          f"everything: {found}")

    said = strings_table()
    check(said.get("results.report") == "View report",
          f"the view control names an action, not a size: "
          f"{said.get('results.report')!r}")
    for key in ("results.download", "results.download.report",
                "results.download.bundle"):
        check(said.get(key, "").startswith("Download"),
              f"{key} names the action it performs: {said.get(key)!r}")

    # Seeded: the order this refuses.
    swapped = list(wanted)
    swapped[1], swapped[3] = swapped[3], swapped[1]
    check(swapped != wanted,
          "seeded check: the swap produced the same order, so the comparison "
          "above is comparing a list with itself")


def test_the_commands_panel_has_one_render_owner() -> None:
    """Two owners painted the old state for about 110 ms on every toggle.

    The operator's report was that the enable/disable checkboxes flicker. Two
    causes were possible and they want opposite fixes; the one it turned out to
    be is **two renders racing**, measured in Chromium with a
    `MutationObserver` on the list and a `requestAnimationFrame` sampler: two
    rebuilds per toggle, and the first of them built the panel from a
    `store.config` the toggle had just been clicked out of.

    `loadProviders` rendered the commands panel on its way past, and
    `reloadAfterSettings` rendered it again after refetching `/config`. So the
    rule pinned here is the fix: **`loadProviders` renders the provider rows
    and nothing else**, and whoever needs the commands panel renders it.

    Pinned by source because the flicker itself is only visible in a browser,
    and a check that asserted the settled state would pass on the tree this
    was found on.
    """
    app = source(APP_JS)
    body = js_function("loadProviders", app)
    check("renderCommandTools()" not in body,
          "loadProviders must not render the commands panel: that is a second "
          "owner, and it renders from a /config nobody has refetched")
    check("renderCommandTools();" in js_function("reloadAfterSettings", app),
          "the toggle path renders it once, after its refetch")
    opened = app[app.index('el("open-settings").addEventListener'):]
    opened = opened[:opened.index("\n  });")]
    check("renderCommandTools();" in opened,
          "and opening the sheet renders it, unconditionally -- a server with "
          "no credential endpoint can still have a command route, so the "
          "panel must not depend on which branch loadProviders took")

    # The second defect the same measurement found: the rebuild destroys the
    # control that was just used, so focus landed on `body` after all four
    # toggles and the next Tab started from the top of the sheet.
    row = js_function("commandToolRow", app)
    check('toggle.setAttribute("data-command"' in row,
          "the toggle has to say which route it is, or the rebuilt panel "
          "cannot be asked for the same one")
    check("document.activeElement === toggle" in row and "again.focus()" in row,
          "focus goes back to the control that was used; by id and not by "
          "position, because a retired route shortens the list")


def test_the_single_render_owner_check_fires() -> None:
    """Seeded: give the panel its second owner back."""
    app = source(APP_JS)
    seeded = app.replace("""  fill(el("providers"), items);
}""", """  fill(el("providers"), items);
  renderCommandTools();
}""")
    check(seeded != app, "seeded check: the loadProviders anchor moved")
    check("renderCommandTools()" in js_function("loadProviders", seeded),
          "seeded check: a second render owner must be found")
    quiet = app.replace("document.activeElement === toggle", "false")
    check("document.activeElement === toggle" not in quiet,
          "seeded check: a handler that never restores focus must be found")


def test_the_copy_control_has_a_path_for_a_page_that_is_not_secure() -> None:
    """`navigator.clipboard` is absent over plain http to a LAN address.

    The operator asked for a *"'Copy Merge to clipboard' or similar in the
    Merged document section"*. The API that does it is gated on a **secure
    context**: present on `localhost`, absent over plain http to any other
    host, which is how this tool is reached on a local network and is a
    deployment this project supports and documents. So the control needs a
    second path, and the one rule it may not break is that it must never go
    quiet -- a control that does nothing and says nothing is one somebody
    presses again and then distrusts.

    Driven in Chromium on both, and the browser run is what actually proves it;
    this pins the shape so a later edit cannot quietly remove the fallback.
    Seeded three ways below.
    """
    markup = source(INDEX)
    check('<button type="button" class="ghost" data-cc="copy-merged"' in markup,
          "the copy control must be a real button: Enter and Space have to "
          "work on it, and a copy button only a mouse can hit is half a "
          "feature")
    check('data-cc="copy-note"' in markup and 'role="status"' in markup
          and 'aria-live="polite"' in markup,
          "the control needs somewhere to say what happened, announced rather "
          "than only painted")

    body = js_function("copyMerged")
    check("window.isSecureContext" in body and "navigator.clipboard" in body,
          "both have to be tested: a browser can expose the object and refuse "
          "the write, and the two read the same to a user")
    check("copyBySelection()" in body,
          "the fallback must be reached, or a LAN deployment has a control "
          "that does nothing")
    for key in ("results.copy.done", "results.copy.manual",
                "results.copy.nothing"):
        check(key in body, f"{key} is never said, so one path is silent")

    fallback = js_function("copyBySelection")
    check('document.execCommand("copy")' in fallback,
          "the deprecated command is the only thing left that can complete a "
          "copy without a secure context")
    check("selectMerged()" in fallback,
          "and where even that refuses, the text has to be left selected so "
          "the reader can finish the copy themselves")

    said = strings_table()
    check("Ctrl+C" in said.get("results.copy.manual", ""),
          "the manual path has to name the shortcut, or 'it is selected' is "
          f"an instruction with no verb: {said.get('results.copy.manual')!r}")
    for tag, strings in catalogues().items():
        for key in ("results.copy", "results.copy.done", "results.copy.manual",
                    "results.copy.nothing", "detail.stack"):
            check(strings.get(key),
                  f"{tag} has no string for {key}; the German is "
                  f"agent-authored and stays so, but it has to exist")


def test_the_copy_control_checks_fire() -> None:
    """Seeded: take away the fallback, the note and the shortcut in turn."""
    js = source(APP_JS)
    gone = js.replace("  const how = copyBySelection();", "  return;")
    check(gone != js, "seeded check: the fallback anchor moved")
    check("copyBySelection()" not in js_function("copyMerged", gone),
          "seeded check: a copyMerged with no fallback must be found")

    quiet = js.replace('document.execCommand("copy")', "false")
    check(quiet != js, "seeded check: the execCommand anchor moved")
    check('document.execCommand("copy")' not in js_function("copyBySelection", quiet),
          "seeded check: a fallback that cannot copy must be found")

    markup = source(INDEX).replace(
        '<button type="button" class="ghost" data-cc="copy-merged"', "<span")
    check('data-cc="copy-merged"' not in markup,
          "seeded check: removing the control must remove the hook the page "
          "looks up, or the markup check is reading something else")


def test_ctrl_a_is_scoped_to_the_merged_box_and_never_to_the_page() -> None:
    """The operator's second request, and what the element actually is.

    Their words: *"if we select the text box and press ctrl+a it would select
    the text in the box and not the entire website"*. The symptom says it is
    not a `<textarea>`, and it is not: it is a `<pre>`, which is right -- the
    merged document is a read-only artefact and making it editable to win a
    keyboard shortcut would be trading the wrong thing away.

    So the shortcut is written, and the element is made focusable so that it
    can carry the `keydown` at all. `tabindex="0"` is load-bearing twice over:
    without it the handler never fires, and a scrollable box a keyboard cannot
    reach is a box a keyboard cannot read.
    """
    markup = source(INDEX)
    box = markup[markup.index('data-cc="merged"'):]
    box = box[:box.index(">")]
    check('tabindex="0"' in box,
          f"the merged box must be able to hold focus, or the keydown on it "
          f"never fires: <pre {box}>")
    # Over the markup with its comments blanked, because the comment above
    # this element explains the choice and names the element it rejected.
    # Exempting the scanner from its own prose is the house answer; splitting
    # the literal to dodge it is not.
    real = strip_html_comments(markup)
    check("<textarea" not in real[real.index('data-cc="results"'):
                                  real.index('data-cc="mismatch"')],
          "the merged document stays a read-only artefact; a textarea would "
          "scope Ctrl+A for free and make it editable, which is the trade "
          "this does not make")
    check('role="region"' in box and "aria-labelledby" in box,
          "a focusable scroller needs a name, or the keyboard lands somewhere "
          "the reader cannot identify")

    app = source(APP_JS)
    check('el("merged").addEventListener("keydown"' in app,
          "the handler goes on the box, not on the document: a document-level "
          "one would own Ctrl+A everywhere else on the page")
    handler = app[app.index('el("merged").addEventListener("keydown"'):]
    handler = handler[:handler.index("\n  });")]
    check("key.altKey || key.shiftKey" in handler,
          "Ctrl+Shift+A and Ctrl+Alt+A are other shortcuts; swallowing them "
          "would be this handler taking keys it was not given")
    check("selectMerged()" in handler and "preventDefault" in handler,
          "the shortcut has to replace the browser's answer, not run beside it")
    check("selectNodeContents" in js_function("selectMerged"),
          "the selection is the box's contents; anything narrower is a "
          "shortcut that selects part of the document")


def test_the_ctrl_a_checks_fire() -> None:
    """Seeded: take the tabindex away, and take the modifier guard away."""
    markup = source(INDEX).replace(' data-cc="merged" tabindex="0"',
                                   ' data-cc="merged"')
    check('data-cc="merged" tabindex="0"' not in markup,
          "seeded check: the tabindex anchor moved, so the check above is "
          "reading a string that is not there")
    app = source(APP_JS).replace("key.altKey || key.shiftKey", "false")
    check("key.altKey || key.shiftKey" not in app,
          "seeded check: a handler that swallows every Ctrl+A must be found")


def test_a_findings_two_sides_stack_and_escape_dismisses_them() -> None:
    """One directly above the other, and Escape closes it.

    The operator asked for the source line and the merged line *"one directly
    above the other ... so the difference can be read by scanning down a column
    rather than along a sentence"*. A column needs a monospaced box and labels
    of one width, which is what `<pre class="stack">` and the padding are for.

    A `<details>`, not a lightbox: the Markdown report and the terminal have no
    lightbox, and the rule is that everything dismissible on this page agrees
    with Escape. `<summary>` is focusable and toggles on Enter and Space with
    no script, which is the keyboard half for free.
    """
    markup = source(INDEX)
    check('<template data-cc="tpl-stack">' in markup,
          "the stacked view needs a template; built in script it would be the "
          "one piece of this page's markup that is not in the markup")
    block = markup[markup.index('<template data-cc="tpl-stack">'):]
    block = block[:block.index("</template>")]
    check("<details" in block and "<summary" in block,
          "an expanded row rather than a dialog: it degrades to an open block "
          "with no script and takes nothing over")
    check('<pre class="stack"' in block and 'data-cc="finding-stack"' in block,
          "the stack is monospaced, or the padded labels line up in nothing")

    css = source(APP_CSS)
    check("white-space: pre-wrap" in css[css.index(".stack-panel > pre.stack"):
                                         css.index(".stack-panel > pre.stack") + 400],
          "the stack wraps rather than scrolls sideways, and the "
          "browser drive asserts scrollWidth against clientWidth on it")

    body = js_function("stackPanel")
    check(body.index('t("detail.insource")') < body.index('t("detail.inmerge")'),
          "the source goes above the merge, which is the direction the reader "
          "is scanning")
    check('t("detail.changed")' in body and body.index('t("detail.inmerge")')
          < body.index('t("detail.changed")'),
          "and the difference goes last, under the two texts it is about")
    check("padEnd" in body,
          "the labels are padded to one width, or the two texts start in "
          "different columns and the stack is two sentences again")
    check("if (rows.length < 2) return null;" in body,
          "no disclosure over a single line: a control that hides one line is "
          "a control that costs more than it saves")
    check("finding.difference" in body,
          "the diff is the engine's published one; a page that diffed the two "
          "texts itself would be a second implementation of the rule")

    app = source(APP_JS)
    check('panel.open = false' in app and '"Escape"' in app,
          "Escape must close the stack, which is the rule for everything "
          "dismissible on this page")
    escape = app[app.index('if (key.key !== "Escape"'):]
    escape = escape[:escape.index("\n  });")]
    check('closest(\'[data-cc="stack-panel"]\')' in escape,
          "only when the keyboard is inside the open one: Escape over the "
          "page at large belongs to the dialogs")
    check("summary.focus()" in escape,
          "focus goes back to the summary, because the element the keyboard "
          "was on is inside the part that just disappeared")


def test_the_stacked_view_checks_fire() -> None:
    """Seeded: collapse the stack, and make Escape ignore it."""
    app = source(APP_JS)
    flat = app.replace("  if (rows.length < 2) return null;", "  return null;")
    check(flat != app, "seeded check: the stack anchor moved")
    check("if (rows.length < 2) return null;" not in js_function("stackPanel", flat),
          "seeded check: a stackPanel that never renders must be found")
    deaf = app.replace('if (key.key !== "Escape" || key.defaultPrevented) return;',
                       "if (true) return;")
    check(deaf != app, "seeded check: the Escape anchor moved")
    check('if (key.key !== "Escape"' not in deaf,
          "seeded check: a page where Escape does not reach the stack must "
          "be found")
    markup = source(INDEX).replace('<template data-cc="tpl-stack">', "<template>")
    check('<template data-cc="tpl-stack">' not in markup,
          "seeded check: removing the template must remove the hook")


def sheet_source() -> str:
    """Everything between the credential sheet's own tags.

    Scoped rather than file-wide because three of the checks below are about
    what is and is not *in* this dialog, and the page has five other dialogs
    and a dozen panels that carry the same class names.
    """
    html = source(INDEX)
    start = html.index('<dialog class="sheet settings"')
    return html[start:html.index("</dialog>", start)]


def test_the_way_out_of_the_credentials_sheet_is_at_the_foot_and_stays_there() -> None:
    """One dismissal, at the bottom, stuck there -- and no second button.

    The operator asked for two: *"I think it should be two buttons 'Close &
    Discard' and 'Close & Save' or whatever is the modern equivalent. It is
    also confusing that the button is on top."* The second half is a real
    fault and the first half describes a sheet this is not. **Nothing here
    buffers.** Every row commits itself the moment its own control is used --
    a `PUT` per key, a `PUT`/`DELETE` per endpoint and per command toggle, a
    `POST` per account -- and closing the sheet sends no request at all. That
    was measured in a browser before anything was designed: typing into five
    fields sent nothing, one toggle click sent `PUT
    /api/v1/settings/commands/claude-haiku` on its own, and the close sent
    nothing. A `Close & Discard` beside a `Close & Save` would offer to undo
    what is already written to the server's disk, which is a worse sentence
    than the one the operator was complaining about.

    So there is one control, and the fix is where it sits. At the foot of this
    sheet the old top-right button was 1,753px above the viewport: 2,705px of
    content scrolls inside an 860px box, and the only way out was in the part
    that leaves first. It is now the last element in the sheet and `sticky`,
    which is both halves of the complaint -- at the bottom, and never gone.

    Five properties, because each fails on its own. Order and stickiness are
    two different things and only the pair is the fix; the sheet's own
    `padding-bottom` has to be the footer's or the rows scroll through the
    strip underneath it; the count is what keeps the answer to "where is the
    way out" one answer; and the clearing hangs on the dialog's `close` so
    that Escape cannot quietly differ from the button.
    """
    html = source(INDEX)
    sheet = sheet_source()
    css = strip_css_comments(source(APP_CSS))
    app = strip_comments(source(APP_JS))

    # One way out, not two. This is the check that refuses the pair.
    check(html.count('data-cc="close-settings"') == 1,
          f"the sheet offers {html.count('data-cc=\"close-settings\"')} dismissal "
          f"controls; one thing that closes this sheet means one place to look "
          f"for it, and a duplicate is a second tab stop and a second "
          f"announcement for one action")

    # At the foot: after the last thing in the sheet, not before the first.
    check(sheet.index('data-cc="close-settings"') > sheet.index('data-cc="accounts-note"'),
          "the way out must come after the sheet's content in document order; "
          "at the top it is the first thing to scroll away, which is the "
          "operator's report")
    check('class="sheet-foot"' in sheet,
          "the control lives in the sheet's footer, which is the element the "
          "stylesheet makes sticky")
    check('aria-describedby="settings-autosave"' in sheet
          and 'id="settings-autosave"' in sheet,
          "the footer sentence has to be the control's description: `autofocus` "
          "lands on the button, and reading order puts the sentence before it, "
          "so a screen reader would announce 'Done, button' and nothing about "
          "what closing does")
    head = sheet[sheet.index('class="sheet-head"'):sheet.index("</div>")]
    check("<button" not in head,
          "the header must not carry a copy of the control; two buttons doing "
          "one thing is what the footer replaced")

    # And stays there.
    foot = css[css.index(".sheet-foot {"):]
    foot = foot[:foot.index("}")]
    check("position: sticky" in foot and "bottom: 0" in foot,
          f"the footer must be pinned to the bottom of the sheet's scrollport; "
          f"without it the control sits 1,753px above a reader who scrolled "
          f"down: {foot.strip()!r}")
    check(".sheet.settings { padding-bottom: 0; }" in css,
          "the sheet's bottom padding has to be the footer's own: a sticky "
          "child is clamped to its parent's content box, so a sheet that keeps "
          "its `padding-bottom` holds the footer clear of the edge and lets "
          "the rows scroll through the strip underneath")
    check('<dialog class="sheet settings"' in html,
          "the rule above is scoped to this sheet, so this sheet has to carry "
          "the class; `.sheet.confirm` is two buttons under one sentence and "
          "must keep its padding")

    # Every way out is the same way out.
    wire = js_function("wire", app)
    check('dialog.addEventListener("close"' in wire,
          "the unsaved fields are cleared on the dialog's own `close` event, "
          "which is the one Escape fires too; on the button's click instead, "
          "Escape would silently keep what the button drops")
    for hook in ("new-account-name", "new-account-password",
                 "current-password", "new-password"):
        check(app.count(f'"{hook}"') >= 2,
              f"{hook} is never cleared, so a password typed and not saved "
              f"stands in the DOM of a closed sheet")

    # The words, in both catalogues.
    for tag, strings in sorted(catalogues().items()):
        check("settings.close" not in strings,
              f"{tag}.json still holds settings.close; the control is `done` "
              f"now and a key nothing renders is a line translated twice")
        for key in ("settings.done", "settings.autosave"):
            check(bool(strings.get(key, "").strip()),
                  f"{tag}.json has no sentence for {key}")


def test_the_credentials_footer_checks_fire() -> None:
    """Must-fire, five ways. Each probe is the shipped file with one thing moved.

    Written as mutations of the real bytes rather than as re-implementations,
    for the reason every probe in this file is: one that rebuilds the predicate
    it is aimed at proves the copy fires. The browser drive that accompanies
    this ran two of them through Chromium as well -- the sticky rule deleted
    put the control at 2,666px in an 860px box, and the sentence rewritten came
    back as `Close & Save`.
    """
    html = source(INDEX)
    css = strip_css_comments(source(APP_CSS))
    app = strip_comments(source(APP_JS))

    # 1. a second control, back in the header.
    seeded = html.replace(
        '<h2 id="settings-heading" data-t="settings.heading">Credentials</h2>',
        '<h2 id="settings-heading" data-t="settings.heading">Credentials</h2>\n'
        '    <button type="button" data-cc="close-settings">Close</button>')
    check(seeded.count('data-cc="close-settings"') == 2,
          "the duplicate-control probe did not add a second control")

    # 1b. the description unhooked, which is invisible to a sighted reader.
    seeded = html.replace(' aria-describedby="settings-autosave"', "")
    check(seeded != html, "the description probe's anchor has moved")
    check('aria-describedby="settings-autosave"' not in seeded,
          "a control with no description still passes, and the sentence would "
          "go unread by the reader who most needs it")

    # 2. the footer moved back above the content.
    start = html.index('<div class="sheet-foot">')
    end = html.index("</div>", html.index("<button", start)) + len("</div>")
    block_html = html[start:end]
    seeded = html.replace(block_html, "")
    seeded = seeded.replace('<ul class="providers" data-cc="providers"></ul>',
                            block_html + '\n  <ul class="providers" data-cc="providers"></ul>')
    top = seeded[seeded.index('<dialog class="sheet settings"'):]
    top = top[:top.index("</dialog>")]
    check(top.index('data-cc="close-settings"') < top.index('data-cc="accounts-note"'),
          "the document-order probe did not move the control above the content")

    # 3. the sticky rule deleted.
    seeded = css.replace("  position: sticky; bottom: 0; z-index: 1;",
                         "  position: static;")
    check(seeded != css, "the sticky probe's anchor has moved")
    foot = seeded[seeded.index(".sheet-foot {"):]
    foot = foot[:foot.index("}")]
    check("position: sticky" not in foot,
          "a footer that is not sticky still passes the pinning check")

    # 4. the sheet keeps its own bottom padding, which lets rows scroll under.
    seeded = css.replace(".sheet.settings { padding-bottom: 0; }", "")
    check(seeded != css, "the padding probe's anchor has moved")
    check(".sheet.settings { padding-bottom: 0; }" not in seeded,
          "a sheet that keeps its bottom padding still passes")

    # 5. the clearing moved onto the button, where Escape does not reach it.
    seeded = app.replace('dialog.addEventListener("close", () => {',
                         'el("close-settings").addEventListener("click", () => {')
    check(seeded != app, "the exit-path probe's anchor has moved")
    check('dialog.addEventListener("close"' not in js_function("wire", seeded),
          "a clearing that only the button reaches still passes, and Escape "
          "would keep what the button drops")


def test_every_number_the_page_formats_uses_the_page_s_language() -> None:
    """The German page showed "4,096": `toLocaleString(undefined, ...)`

    reads the browser's configured language, which routinely disagrees with
    the one the page is rendering in -- exactly what LLossless's own
    number-convention check exists to flag in a *document*. `figure`
    is already the one place every number on this page is formatted through;
    the fix is that one function reading `locale.tag` (set from what the
    server actually served, never guessed) instead of `undefined`, and it has
    to stay the only formatting path or a second one can drift back to the
    browser's guess unnoticed.
    """
    js = strip_comments(source(APP_JS))
    figure = body_of(js, "function figure(")
    check("new Intl.NumberFormat(locale.tag" in figure,
          "figure must format in the page's own language, not the browser's")
    check("toLocaleString" not in figure,
          "the old, browser-locale call must be gone from figure")

    # The one other locale-sensitive call in the file: a run's timestamp. Not
    # `figure`'s shape, but the same defect class, so it takes the same tag.
    calls = [line for line in js.splitlines() if "toLocaleString(" in line]
    check(len(calls) == 1 and "locale.tag" in calls[0],
          f"every toLocaleString call must pass locale.tag; found {calls!r}")

    # The whole file: no bare `.toLocaleString()` and no `toLocaleString(undefined`
    # anywhere, and no hand-written thousands separator standing in for one.
    check("toLocaleString()" not in js and "toLocaleString(undefined" not in js,
          "an unlocalised toLocaleString call reads the browser's language "
          "again, the exact regression this entry closes")
    check(re.search(r"replace\(/[^)]*\\d\{3\}", js) is None,
          "a hand-rolled thousands-separator regex is a second formatting "
          "path `figure` cannot see, and it will not track the page's language")

    # Must-fire: the probe has to see the anchor it is built on.
    check("new Intl.NumberFormat(locale.tag" not in figure
          .replace("new Intl.NumberFormat(locale.tag", "undefined && ("),
          "the probe cannot see its own anchor")


# --------------------------------------------------------------------------
# the merge effort slider and its card
# --------------------------------------------------------------------------

# A document just big enough for the shipped script to run under node: every
# `data-cc` hook resolves to an element made on first use, and `readyState`
# is "loading" so `boot` waits for an event that never comes. What the page
# does with the DOM is then read back off these elements, the way a browser's
# `innerText` would be, rather than off the functions' return values.
EFFORT_DOM = r"""
class El {
  constructor(tag) {
    this.tagName = tag; this.childNodes = []; this.hidden = false;
    this.textContent = ""; this.value = ""; this.attributes = {};
    // Custom properties set through the CSSOM (the `--at` on a stop word).
    const props = {};
    this.style = { setProperty: (n, v) => { props[n] = String(v); },
                   getPropertyValue: (n) => (n in props ? props[n] : "") };
    const names = new Set();
    this.classList = { add: (n) => names.add(n), remove: (...n) => n.forEach((x) => names.delete(x)),
                       contains: (n) => names.has(n), toggle: (n, on) => on ? names.add(n) : names.delete(n) };
  }
  get firstChild() { return this.childNodes[0] || null; }
  appendChild(child) { this.childNodes.push(child); return child; }
  removeChild(child) { this.childNodes = this.childNodes.filter((c) => c !== child); return child; }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return name in this.attributes ? this.attributes[name] : null; }
  removeAttribute(name) { delete this.attributes[name]; }
  get innerText() {
    return this.childNodes.length ? this.childNodes.map((c) => c.innerText).join("\n") : this.textContent;
  }
}
const hooks = {};
globalThis.document = {
  readyState: "loading",
  addEventListener() {},
  querySelector(selector) {
    const hook = /data-cc="([^"]+)"/.exec(selector);
    if (!hook) return null;
    return hooks[hook[1]] || (hooks[hook[1]] = new El("div"));
  },
  querySelectorAll() { return []; },
  createElement(tag) { return new El(tag); },
  createTextNode(text) { const node = new El("#text"); node.textContent = text; return node; },
  documentElement: { lang: "en" },
};
"""

# Selects each route, reads the card at the route's own default, then moves the
# slider to every stop and reads the card and the submitted `effort` again.
EFFORT_DRIVE = r"""
;(() => {
  strings = INPUT.strings;
  locale.tag = INPUT.tag;
  store.config = INPUT.config;
  store.fidelity = INPUT.fidelity;
  store.docs = [{ name: "a.md", text: "A.", id: "a" }, { name: "b.md", text: "B.", id: "b" }];
  // Every hook `index.html` carries, touched once up front so each exists
  // before the loop below reads any of them: a route whose card is
  // never rendered at all -- a single-level model, first in the served list
  // since Haiku -- must read as empty, not crash on an element nothing has
  // queried yet. A real page has every element from the moment it loads;
  // this fake DOM only vivifies one on its first `querySelector`, which is
  // otherwise however `renderEffort` happens to have been called so far.
  for (const hook of INPUT.hooks) { el(hook); }
  const read = () => ({
    level: store.effort,
    shown: !hooks["effort-block"].hidden,
    title: hooks["effort-card-title"].textContent,
    valuetext: hooks["effort-slider"].getAttribute("aria-valuetext"),
    rows: hooks["effort-figures"].hidden ? [] : hooks["effort-figures"].childNodes.map((c) => c.textContent),
    unmeasured: hooks["effort-unmeasured"].hidden ? "" : hooks["effort-unmeasured"].textContent,
    maxWarning: hooks["effort-max-warning"].hidden ? "" : hooks["effort-max-warning"].textContent,
    submitMaxWarning: hooks["effort-submit-max-warning"].hidden ? "" : hooks["effort-submit-max-warning"].textContent,
    warning: hooks["effort-warning"].hidden ? "" : hooks["effort-warning"].textContent,
    caveat: hooks["effort-caveat"].hidden ? "" : hooks["effort-caveat"].textContent,
    model: hooks["effort-model"].hidden ? "" : hooks["effort-model"].textContent,
    // The one-level line a single-level route shows in the
    // slider's place.
    singleLevel: hooks["effort-single-level"].hidden ? "" : hooks["effort-single-level"].textContent,
    // Each pinned section as its children's texts, a `dl` as its terms
    // and descriptions in order.
    pinned: hooks["effort-pinned"].hidden ? [] : hooks["effort-pinned"].childNodes.map(
      (section) => section.childNodes.map((c) => c.tagName === "dl"
        ? c.childNodes.map((x) => x.textContent) : c.textContent)),
    current: hooks["effort-current"].hidden ? [] : hooks["effort-current"].childNodes.map(
      (section) => section.childNodes.map((c) => c.tagName === "dl"
        ? c.childNodes.map((x) => x.textContent) : c.textContent)),
    submitted: submission().effort === undefined ? null : submission().effort,
  });
  const out = {};
  for (const id of INPUT.routes) {
    store.mergeModel = COMMAND_PREFIX + id;
    store.checkModel = store.mergeModel;
    renderEffort();
    const at = { initial: read(), stops: [] };
    const slider = hooks["effort-slider"];
    for (let stop = Number(slider.min); stop <= Number(slider.max); stop += 1) {
      slider.value = String(stop);
      slider.oninput();
      at.stops.push(read());
    }
    out[id] = at;
  }
  // And off every route: a metered row hides the slider and sends nothing.
  store.mergeModel = "claude-opus-5";
  renderEffort();
  out.metered = read();
  process.stdout.write(JSON.stringify(out));
})();
"""


def served_config_with_routes() -> dict:
    """`/config` from a real server holding the four discovered `claude` routes."""
    from test_web_server import claude_routes, request as server_request
    with claude_routes() as (built, _calls):
        status, _headers, body = server_request(f"{built.url}/api/v1/config")
    check(status == 200, f"/config answered {status}")
    return json.loads(body.decode("utf-8"))


def drive_effort_card(js: str, payload: dict, tag: str, fidelity: str) -> dict | None:
    """The shipped script under node over the served `/config`, or None."""
    node = node_command()
    if node is None:
        return None
    routes = [row["id"] for row in payload["commands"]["routes"]
              if row["id"].startswith("claude-")]
    program = (EFFORT_DOM + "\nconst INPUT = " + json.dumps(
        {"strings": catalogues()[tag], "tag": tag, "config": payload,
         "fidelity": fidelity, "routes": routes,
         "hooks": sorted(hooks_in_html())}) + ";\n" + js + EFFORT_DRIVE)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as handle:
        handle.write(program)
        path = handle.name
    try:
        run = subprocess.run(node + [path], capture_output=True, text=True,
                             timeout=120, cwd=ROOT)
    finally:
        os.unlink(path)
    if run.returncode != 0:
        check(False, f"the effort card did not run under node: {run.stderr[-600:]}")
        return {}
    return json.loads(run.stdout)


def expected_card(strings: dict, block: dict | None, level: str) -> list[str] | None:
    """The card's dt/dd texts for `level`, formed here from the catalogue block.

    The same templates the page fills, with the block's own numbers put in by
    hand: the check is that every figure on the card is the block's figure at
    that level, not that two formatters agree.
    """
    at = ((block or {}).get("levels") or {}).get(level)
    if not at:
        return None

    def fill(key: str, **values) -> str:
        text = strings[key]
        for name, value in values.items():
            text = text.replace("{" + name + "}", str(value))
        return text

    def duration(seconds: float) -> str:
        # `Math.round`, which rounds a half up; Python's `round` rounds it to
        # even and read 278.5 s as 4m 38s where the page says 4m 39s.
        whole = max(0, int(seconds + 0.5))
        return (fill("time.seconds", n=whole) if whole < 60
                else fill("time.minutes", m=whole // 60, s=whole % 60))

    rows, shown = [], [pair for pair in ("voyager", "bip39") if pair in at["pairs"]]
    for pair in shown:
        cell = at["pairs"][pair]
        said = fill("effort.card.fixed", fixed=cell["fixed"]["median"],
                    planted=cell["planted"], min=cell["fixed"]["min"],
                    max=cell["fixed"]["max"], runs=cell["draws"])
        if "licence_fixed" in cell:
            said += " " + fill("effort.card.licence", n=cell["licence_fixed"],
                               runs=cell["draws"])
        rows += [strings[f"effort.pair.{pair}"], said]
    rows += [strings["effort.card.time"], ", ".join(
        fill("effort.card.time.pair", time=duration(at["pairs"][pair]["seconds"]["median"]),
             pair=strings[f"effort.pair.short.{pair}"]) for pair in shown)]
    rows += [strings["effort.card.searched"],
             fill("effort.card.searched.value", n=at["searched"], runs=at["runs"])]
    return rows


def fill_template(strings: dict, key: str, **values) -> str:
    text = strings[key]
    for name, value in values.items():
        text = text.replace("{" + name + "}", str(value))
    return text


def times_text(ratio: float) -> str:
    """The page's `timesText`, restated: whole above one and a half."""
    return str(round(ratio)) if ratio >= 1.5 else f"{ratio:.1f}"


def expected_comparison(strings: dict, block: dict) -> str | None:
    """`max` against `xhigh` in one block, in the page's plain words.

    Formed here from the block's own numbers and the registered overlap rule:
    ranges that overlap are no difference, whatever the medians say.
    """
    levels = block.get("levels") or {}
    at, below = levels.get("max"), levels.get("xhigh")
    if not at or not below:
        return None
    pair = next((p for p in ("voyager", "bip39") if p in at["pairs"] and p in below["pairs"]),
                None)
    if pair is None:
        return None
    mine, theirs = at["pairs"][pair], below["pairs"][pair]
    words = {"level": strings["effort.level.xhigh"], "fixed": mine["fixed"]["median"],
             "other": theirs["fixed"]["median"], "planted": mine["planted"]}
    overlap = (mine["fixed"]["min"] <= theirs["fixed"]["max"]
               and theirs["fixed"]["min"] <= mine["fixed"]["max"])
    if overlap:
        key = ("effort.card.vs.same" if mine["fixed"]["median"] == theirs["fixed"]["median"]
               else "effort.card.vs.within")
    else:
        key = ("effort.card.vs.more" if mine["fixed"]["median"] > theirs["fixed"]["median"]
               else "effort.card.vs.fewer")
    time = times_text(mine["seconds"]["median"] / theirs["seconds"]["median"])
    usage = (times_text(at["api_equivalent_usd"]["median"] / below["api_equivalent_usd"]["median"])
             if "api_equivalent_usd" in at and "api_equivalent_usd" in below else "")
    cost = (fill_template(strings, "effort.card.vs.cost.time", n=time) if not usage
            else fill_template(strings, "effort.card.vs.cost.both", n=time) if usage == time
            else fill_template(strings, "effort.card.vs.cost.split", time=time, usage=usage))
    return fill_template(strings, "effort.card.vs.value",
                         result=fill_template(strings, key, **words), cost=cost)


def max_measured_dearer(blocks: list) -> bool:
    for block in blocks:
        levels = (block or {}).get("levels") or {}
        at, below = levels.get("max"), levels.get("xhigh")
        if at and below and any(
                p in at["pairs"] and p in below["pairs"]
                and at["pairs"][p]["seconds"]["median"] > below["pairs"][p]["seconds"]["median"]
                for p in ("voyager", "bip39")):
            return True
    return False


def expected_pinned(strings: dict, route: dict, primary: dict | None, block: dict,
                    level: str, now: dict | None = None,
                    current_model: str | None = None) -> list:
    """One pinned section's texts at `level`, formed from the block.

    `current_model` is what the route runs today (`currentRouteModel`
    app.js-side): `now["model"]` when the alias has moved past the route's
    own figures, else the route's own `resolved_model`, so a pinned block
    reads as "current" whether that answer came from an alias check or,
    once the two agree, from the route's own `resolved_model` directly.
    """
    alias = route.get("model") or ""
    is_current = bool(current_model) and current_model == block["requested_model"]
    head = (fill_template(strings, "effort.card.model.current", model=block["requested_model"],
                          alias=alias, date=now["checked_on"])
            if is_current and now
            else fill_template(strings, "effort.card.model.pinned.bare",
                               model=block["requested_model"], alias=alias)
            if is_current
            else fill_template(strings, "effort.card.model.pinned",
                               model=block["requested_model"],
                               alias=alias, resolved=primary["resolved_model"])
            if primary and primary.get("resolved_model")
            else fill_template(strings, "effort.card.model.pinned.bare",
                               model=block["requested_model"], alias=alias))
    out: list = [head]
    rows = expected_card(strings, block, level)
    if rows is not None:
        said = expected_comparison(strings, block) if level == "max" else None
        if said:
            rows += [fill_template(strings, "effort.card.vs",
                                   level=strings["effort.level.xhigh"]), said]
        out.append(rows)
    else:
        out.append(strings["effort.card.unmeasured"])
    old = next((row for row in route.get("cli_too_old") or []
                if row["model"] == block["requested_model"]), None)
    if old:
        out.append(fill_template(strings, "effort.card.cli_old", needs=old["needs"],
                                 found=route.get("cli_version") or ""))
    pairs = [p for p in ("voyager", "bip39")
             if any(p in (lv or {}).get("pairs", {}) for lv in block["levels"].values())]
    out.append(fill_template(
        strings, "effort.card.caveat.pinned.isolated" if block["safe_mode"]
        else "effort.card.caveat.pinned", date=block["measured_on"],
        pairs=strings["effort.card.and"].join(strings[f"effort.pair.{p}"] for p in pairs)))
    return out


def effort_card_problems(driven: dict, payload: dict, strings: dict,
                         fidelity: dict) -> list[str]:
    """Every route and every stop, against the catalogue block at that level."""
    out = []
    entries = {entry["route"]: entry for entry in payload["catalogue"]["command_routes"]}
    blocks = {route: entry.get("measured_by_effort") for route, entry in entries.items()}
    pinned_blocks = {route: entry.get("pinned_by_effort") or []
                     for route, entry in entries.items()}
    alias_now = {route: entry.get("alias_now") for route, entry in entries.items()}
    # What each route runs today, whether that answer came from
    # `alias_now` or, once the alias and `resolved_model` agree, from
    # `resolved_model` directly, mirroring app.js's `currentRouteModel`.
    current_model = {}
    for route, entry in entries.items():
        now = alias_now.get(route)
        current_model[route] = str(now["model"]) if now else str(entry.get("resolved_model") or "")
    routes = {row["id"]: row for row in payload["commands"]["routes"]}
    for route, at in driven.items():
        if route == "metered":
            continue
        choice = routes[route]["effort"]
        if choice.get("single_level"):
            # No slider, no card, one line instead -- checked
            # on its own terms rather than against `choice["levels"]`, which
            # this shape does not carry.
            if at["initial"]["shown"] or at["stops"]:
                out.append(f"{route}: a single-level route must not show the "
                           f"effort slider: {at['initial']}, {at['stops']}")
            if at["initial"]["singleLevel"] != strings["effort.single_level"]:
                out.append(f"{route}: the single-level line reads "
                           f"{at['initial']['singleLevel']!r}, want "
                           f"{strings['effort.single_level']!r}")
            continue
        if at["initial"]["singleLevel"]:
            out.append(f"{route}: the single-level line must be empty on a "
                       f"route that takes a scale: {at['initial']['singleLevel']!r}")
        block = blocks.get(route)
        if at["initial"]["level"] != choice["default"]:
            out.append(f"{route}: the slider starts at {at['initial']['level']!r}, "
                       f"the route's default is {choice['default']!r}")
        levels = [stop["level"] for stop in at["stops"]]
        if levels != choice["levels"]:
            out.append(f"{route}: the slider's stops are {levels}, the route "
                       f"offers {choice['levels']}")
        for stop in at["stops"]:
            level, name = stop["level"], strings[f"effort.level.{stop['level']}"]
            where = f"{route} at {level}"
            if not stop["shown"]:
                out.append(f"{where}: the slider is hidden on a route that takes a level")
            if stop["submitted"] != level:
                out.append(f"{where}: the submitted effort is {stop['submitted']!r}")
            if stop["valuetext"] != name or name not in stop["title"]:
                out.append(f"{where}: the slider and the card do not name the "
                           f"level: {stop['valuetext']!r}, {stop['title']!r}")
            want = expected_card(strings, block, level)
            if want is None:
                if stop["rows"] or stop["unmeasured"] != strings["effort.card.unmeasured"]:
                    out.append(f"{where}: nothing was measured here and the card "
                               f"shows {stop['rows']} / {stop['unmeasured']!r}")
            elif stop["rows"] != want or stop["unmeasured"]:
                out.append(f"{where}: the card shows {stop['rows']}, the catalogue "
                           f"gives {want}")
            caveat = (strings["effort.card.caveat"].replace("{date}", block["measured_on"])
                      .replace("{runs}", str(block["draws"])) if block else "")
            if stop["caveat"] != caveat:
                out.append(f"{where}: the caveat reads {stop['caveat']!r}, want {caveat!r}")
            warned = fidelity.get("retrieves") and level in choice["not_at_sourced"]
            if bool(stop["warning"]) != bool(warned):
                out.append(f"{where}: the low-at-sourced line is "
                           f"{'shown' if stop['warning'] else 'hidden'} at fidelity "
                           f"{fidelity.get('value')!r}")
            # The cost warning shows only at `max`, in the card and again
            # by the submit button, both in the catalogue's own words -- and
            # nowhere else, so picking any of the four measured levels clears
            # both.
            #
            # Where a block on the card measured `max` dearer than
            # `xhigh`, the warning says so rather than calling it untested.
            at_max = level == "max"
            pinned = pinned_blocks.get(route) or []
            warning = strings["effort.max_warning.measured" if max_measured_dearer(
                [block, *pinned]) else "effort.max_warning"]
            for field, name in (("maxWarning", "card"), ("submitMaxWarning", "submit")):
                shown = stop[field]
                if at_max and shown != warning:
                    out.append(f"{where}: the {name} max warning reads {shown!r}, "
                               f"want {warning!r}")
                elif not at_max and shown:
                    out.append(f"{where}: the {name} max warning must be hidden "
                               f"off max, and shows {shown!r}")
            # Each pinned block in its own section, and the route's own
            # block headed by its model only when one sits beside it.
            # Where the alias answers as another model now, the route's own
            # block is headed as history and that model's block comes first.
            now = alias_now.get(route)
            key = ("effort.card.model.route" if not now
                   else "effort.card.model.history.before_safe_mode"
                   if block and block.get("safe_mode") is False
                   else "effort.card.model.history")
            want_model = (fill_template(strings, key, model=block["resolved_model"],
                                        alias=routes[route].get("model") or "")
                          if pinned and block and block.get("resolved_model") else "")
            if stop["model"] != want_model:
                out.append(f"{where}: the route's own heading reads {stop['model']!r}, "
                           f"want {want_model!r}")
            this_model = current_model.get(route)
            first = [each for each in pinned
                    if this_model and each["requested_model"] == this_model]
            want_current = [expected_pinned(strings, routes[route], block, each, level, now,
                                            this_model) for each in first]
            want_pinned = [expected_pinned(strings, routes[route], block, each, level, now,
                                           this_model)
                           for each in pinned if each not in first]
            if stop["current"] != want_current:
                out.append(f"{where}: the current model's section reads {stop['current']}, "
                           f"want {want_current}")
            if stop["pinned"] != want_pinned:
                out.append(f"{where}: the pinned sections read {stop['pinned']}, "
                           f"want {want_pinned}")
    if driven.get("metered", {}).get("shown") or driven.get("metered", {}).get("submitted"):
        out.append(f"a metered row shows the slider or sends a level: {driven.get('metered')}")
    if driven.get("metered", {}).get("submitMaxWarning"):
        out.append(f"a metered row leaves the submit max warning shown: {driven.get('metered')}")
    return out


def test_the_effort_card_shows_the_catalogue_s_figures_at_every_level() -> None:
    """The shipped script under node, over a real server's `/config`.

    Every discovered `claude` route, the slider moved to every stop: the card
    shows the catalogue block's figures at that level and nothing else; a
    level with no figures reads "not measured at this level" (Fable
    everywhere), never a blank or a zero; the submitted `effort` is the stop;
    the slider starts at the route's served default; a metered row hides it
    and sends nothing. `max` is a fifth stop nobody ran: unmeasured like
    Fable, plus a cost warning in the card and again by the submit button,
    nowhere else. In English at `sourced`, where the `low` line must show, and
    in German at the default level, where it must not.

    Haiku is first in the served list and takes no level at
    all any more: neither the slider nor the card may show for it, and the
    one-level line must instead, in the caller's own words -- the reason every
    other route's read is asserted to carry no such line, since a card and a
    single-level line showing together would be two contradictory answers to
    "does this route take a level".

    Must-fire, each on the same drive: a card that reads the maximum as the
    median, a slider whose handler forgets the level, an unmeasured level
    rendered as an empty list of figures, and a `max` warning that never
    fires.
    """
    js = source(APP_JS)
    payload = served_config_with_routes()
    fidelity = {level["value"]: level for level in payload["fidelity"]["levels"]}
    sourced = next(level for level in fidelity.values() if level.get("retrieves"))
    plain = next(level for level in fidelity.values() if level.get("default"))
    runs = {}
    for tag, level in (("en", sourced), ("de", plain)):
        driven = drive_effort_card(js, payload, tag, level["value"])
        if driven is None:
            decline("UNMEASURED: no node to drive the effort card under; it was "
                    "not checked here")
            return
        runs[tag] = driven
        found = effort_card_problems(driven, payload, catalogues()[tag], level)
        check(not found, f"the {tag} effort card: {found[:6]}")
    opus = runs["en"].get("claude-opus", {}).get("stops", [])
    # opus lost its own measured_by_effort grid (Claude Opus 5's own K=3
    # grid, removed with the row itself); its card now lives entirely in the
    # pinned section (opus-max, xhigh and max only), so the top card
    # ("effort-figures") reads unmeasured at every one of the five stops, and
    # uniqueness is checked over the pinned section instead, at the two
    # stops it actually covers.
    measured_levels = ("xhigh", "max")
    distinct = {json.dumps(stop["current"]) for stop in opus if stop["level"] in measured_levels}
    check(len(distinct) == len(measured_levels),
          "moving the Opus slider between its two measured stops must change the "
          "pinned section each time")
    check(all(stop["rows"] == [] for stop in opus),
          "opus carries no measured_by_effort any more; its own card must be "
          "unmeasured at every level")

    # Pinned as literals as well as formed: the operator's sentence for
    # Opus 5.5 at `max`, from the shipped catalogue, and the warning that no
    # longer calls `max` untested on that route.
    at_max = next((stop for stop in opus if stop["level"] == "max"), {})
    pinned_rows = [row for section in at_max.get("current", []) + at_max.get("pinned", [])
                   for part in section if isinstance(part, list) for row in part]
    # The opus alias and its own resolved_model agree (claude-opus-5-5),
    # so its one pinned block (opus-max) always reads as current, and there
    # is no route-level block left to head as history.
    check(bool(at_max.get("current")) and not at_max.get("pinned"),
          f"the Opus 5.5 block is not shown as current: {at_max}")
    check(at_max.get("model", "") == "",
          f"opus carries no measured_by_effort block, so the route's own heading "
          f"must be empty: {at_max.get('model')!r}")
    check("No gain over extra high on this test (38 of 44 either way); about 2x the time "
          "and usage." in pinned_rows,
          f"Opus 5.5 at max does not say what was measured: {pinned_rows}")
    check(at_max.get("maxWarning") == catalogues()["en"]["effort.max_warning.measured"],
          f"the Opus card at max keeps the untested warning: {at_max.get('maxWarning')!r}")
    check(at_max.get("unmeasured") == catalogues()["en"]["effort.card.unmeasured"],
          "opus's own card must say nothing was measured at max too")

    # The CLI note, on a payload whose Opus route runs a CLI too old for
    # the pinned model: formed by `expected_pinned` from the served fields.
    old_cli = json.loads(json.dumps(payload))
    for row in old_cli["commands"]["routes"]:
        if row["id"] == "claude-opus":
            row["cli_version"] = "2.1.274"
            row["cli_too_old"] = [{"model": "claude-opus-5-5", "needs": "2.1.280"}]
    driven = drive_effort_card(js, old_cli, "en", sourced["value"])
    check(bool(driven) and not effort_card_problems(driven, old_cli, catalogues()["en"],
                                                    sourced),
          "the card with an old CLI does not match the served fields")
    noted = [part for stop in (driven or {}).get("claude-opus", {}).get("stops", [])
             for section in stop["current"] + stop["pinned"] for part in section]
    check("Needs Claude Code 2.1.280 or newer; this server has 2.1.274." in noted,
          "an old CLI is not noted on the Opus 5.5 section")
    unnoted = js.replace("  if (old) {\n    const note", "  if (false) {\n    const note")
    check(unnoted != js, "the seed for a missing CLI note did not change the script")
    driven = drive_effort_card(unnoted, old_cli, "en", sourced["value"])
    check(bool(driven) and bool(effort_card_problems(driven, old_cli, catalogues()["en"],
                                                     sourced)),
          "the card check did not fire on a missing CLI note")

    # opus no longer carries a measured_by_effort block, so the "route's
    # own heading, history vs current" code path two of the seeds below probe
    # has no real route left to exercise it against. Built synthetically
    # here on claude-sonnet instead: its own real measured_by_effort grid,
    # plus a copy of opus's real pinned block under a fabricated alias_now,
    # the same construction test_route_label.py uses, a once-shelved attempt
    # safe now that the underlying current/pinned split reads a grid's own
    # resolved_model rather than alias_now alone.
    dual_payload = json.loads(json.dumps(payload))
    sonnet_entry = next(e for e in dual_payload["catalogue"]["command_routes"]
                        if e["route"] == "claude-sonnet")
    opus_entry = next(e for e in payload["catalogue"]["command_routes"]
                      if e["route"] == "claude-opus")
    sonnet_entry["alias_now"] = {"model": "claude-opus-5-5", "checked_on": "2026-09-26",
                                 "cli_version": "2.1.283"}
    sonnet_entry["pinned_by_effort"] = json.loads(json.dumps(opus_entry["pinned_by_effort"]))
    driven = drive_effort_card(js, dual_payload, "en", sourced["value"])
    check(bool(driven) and not effort_card_problems(driven, dual_payload,
                                                    catalogues()["en"], sourced),
          "the fabricated dual-block payload does not match the shipped script")

    seeds = {
        "the pinned max comparison dropped":
            (js.replace("    if (said) rows.push(", "    if (false) rows.push("), payload),
        "a pinned section without its model":
            (js.replace("  section.appendChild(head);\n", "", 1), payload),
        "usage read off a different figure":
            (js.replace("at.api_equivalent_usd.median / below.api_equivalent_usd.median",
                       "3 * at.api_equivalent_usd.median / below.api_equivalent_usd.median"),
             payload),
        "the untested warning where max was measured":
            (js.replace("maxMeasuredDearer([block, ...pinned])", "false"), payload),
        "the current model's block not put first":
            (js.replace(
                "  const current = pinned.filter((each) => currentModel "
                "&& each.requested_model === currentModel);",
                "  const current = [];"), payload),
        "the history heading dropped":
            (js.replace('t(now ? history : "effort.card.model.route", {',
                       't("effort.card.model.route", {'), dual_payload),
        "the route's own figures with no model beside a pinned block":
            (js.replace("  model.hidden = !(pinned.length && block && block.resolved_model);",
                       "  model.hidden = true;"), dual_payload),
        "the median read as the maximum":
            (js.replace("fixed: figure(cell.fixed.median)", "fixed: figure(cell.fixed.max)"),
             payload),
        "a slider that forgets the level":
            (js.replace("    store.effort = picked;\n", "", 1), payload),
        "an unmeasured level as an empty list":
            (js.replace("  if (!at || !at.pairs) return null;",
                       "  if (!at || !at.pairs) return [];"), payload),
        "a max warning that never fires":
            (js.replace('  const atMax = level === "max";', '  const atMax = false;'), payload),
    }
    for what, (seeded, use_payload) in seeds.items():
        check(seeded != js, f"the seed {what!r} did not change the script")
        driven = drive_effort_card(seeded, use_payload, "en", sourced["value"])
        check(bool(driven) and bool(effort_card_problems(driven, use_payload,
                                                         catalogues()["en"], sourced)),
              f"the card check did not fire on {what}")



ROUTE_MARK_DRIVE = r"""
;(() => {
  strings = INPUT.strings;
  locale.tag = "en";
  store.config = { commands: { routes: [], per_user: false }, catalogue: INPUT.catalogue };
  const out = {};
  for (const [name, route] of Object.entries(INPUT.routes)) {
    out[name] = routeMarks({ id: "command:" + route.id, command: route }).map((m) => m.text);
  }
  process.stdout.write(JSON.stringify(out));
})();
"""


def test_a_route_marks_a_model_its_cli_is_too_old_for() -> None:
    """A route whose own model the server's CLI is too old for says so on
    its row, in the served numbers; a route whose CLI is new enough, or whose
    model has no minimum, carries no such mark. Must-fire: the mark removed."""
    node = node_command()
    if node is None:
        decline("UNMEASURED: no node to drive the route marks under")
        return
    base = {"comparable": True, "retrieval": [], "profile": "subscription",
            "cost": "plan", "cli_version": "2.1.274",
            "cli_too_old": [{"model": "claude-opus-5-5", "needs": "2.1.280"}]}
    routes = {"old": {**base, "id": "opus55", "model": "claude-opus-5-5"},
              "new": {**base, "id": "opus55", "model": "claude-opus-5-5",
                      "cli_version": "2.1.283", "cli_too_old": []},
              "alias": {**base, "id": "claude-opus", "model": "opus"},
              "sonnet": {**base, "id": "claude-sonnet", "model": "sonnet"}}
    want = catalogues()["en"]["models.route.mark.cli_old"].replace(
        "{needs}", "2.1.280").replace("{found}", "2.1.274")
    shipped = json.loads((ROOT / "src" / "llossless" / "web" / "catalogue.json")
                         .read_text(encoding="utf-8"))
    # No shipped route carries `alias_now` any more (opus's own
    # resolved_model caught up with its alias), so the history-mark check
    # below fabricates one on the real claude-opus entry, the same route the
    # "alias" test-route above already targets. This never touches
    # `cli_too_old`, which the driven routes carry directly, not through the
    # catalogue. A synthetic model row supplies the display name the mark
    # quotes, since the real claude-opus-5 row was removed from the card too.
    opus_entry = next(e for e in shipped["command_routes"] if e["route"] == "claude-opus")
    opus_entry["alias_now"] = {"model": "claude-opus-5-5", "checked_on": "2026-09-26",
                               "cli_version": "2.1.283"}
    opus_entry["resolved_model"] = "claude-opus-5"
    shipped["models"].append({"id": "claude-opus-5", "api_model": "claude-opus-5",
                              "display_name": "Claude Opus 5", "provider": "anthropic",
                              "profile": "anthropic", "context_window": 200000,
                              "measured": None})

    def drive(js: str) -> dict:
        program = (EFFORT_DOM + "\nconst INPUT = " + json.dumps(
            {"strings": catalogues()["en"], "routes": routes, "catalogue": shipped})
            + ";\n" + js + ROUTE_MARK_DRIVE)
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as handle:
            handle.write(program)
            path = handle.name
        try:
            run = subprocess.run(node + [path], capture_output=True, text=True,
                                 timeout=120, cwd=ROOT)
        finally:
            os.unlink(path)
        check(run.returncode == 0, f"the route marks did not run: {run.stderr[-600:]}")
        return json.loads(run.stdout or "{}")

    js = source(APP_JS)
    marks = drive(js)
    check(want in marks.get("old", []), f"an old CLI is not marked: {marks.get('old')}")
    check(want not in marks.get("new", []), f"a new CLI is marked: {marks.get('new')}")
    check(not any("Claude Code" in m for m in marks.get("alias", [])),
          f"a route whose own model has no minimum is marked: {marks.get('alias')}")
    seeded = js.replace('    if (old) say(t("models.route.mark.cli_old", old));\n', "")
    check(seeded != js, "the seed did not change the script")
    check(want not in drive(seeded).get("old", []), "the check cannot see the mark it pins")

    # Fabricated, since no shipped route still has this: an alias_now
    # naming a model the route's own figures do not mark the route's figures
    # as that other model's, by the model's catalogue name; Sonnet's
    # alias has not moved and its row carries no such mark. `measured_by_effort`
    # is absent on this fabricated entry, so the plain history string
    # applies, not the "before safe mode" variant.
    history = "measured on Claude Opus 5"
    check(history in marks.get("alias", []),
          f"the Opus route's figures are not marked as history: {marks.get('alias')}")
    check(not any(m.startswith("measured on") for m in marks.get("sonnet", [])),
          f"a route whose alias has not moved is marked as history: {marks.get('sonnet')}")
    unmarked = js.replace("  if (measuredOnOtherModel(model)) {",
                          "  if (false && measuredOnOtherModel(model)) {")
    check(unmarked != js, "the history seed did not change the script")
    check(history not in drive(unmarked).get("alias", []),
          "the check cannot see the history mark it pins")


# --------------------------------------------------------------------------
# the picker and the model scorecard
# --------------------------------------------------------------------------

# Every question is asked of the shipped script under node, over a `/config`
# a real server served, with its endpoints and routes varied per scenario.
# The expectations are formed here from the payload, not read back from the
# page, and every property gets a seeded breakage of the shipped `app.js`.
SCORECARD_DRIVE = r"""
;(() => {
  // The picker's rows carry radios with listeners; the drive never fires one.
  if (!El.prototype.addEventListener) El.prototype.addEventListener = function () {};
  strings = INPUT.strings;
  locale.tag = "en";
  const kept = {};
  const out = {};
  for (const [name, config] of Object.entries(INPUT.scenarios)) {
    store.config = config;
    store.mergeModel = ""; store.checkModel = ""; store.splitRoles = false;
    const rows = scorecardRows();
    const at = {
      picker: pickerRows(pickable()).map((m) => m.id),
      scorecard: rows.map((m) => m.id),
      orders: {}, aria: {}, titles: {},
    };
    for (const key of Object.keys(SCORECARD_SORTS)) {
      for (const direction of ["ascending", "descending"]) {
        at.orders[key + " " + direction] = scorecardOrder(rows, key, direction).map((m) => m.id);
        scorecardSort.key = key; scorecardSort.direction = direction;
        paintSortHeads(scorecardSort);
        at.aria[key + " " + direction] = Object.fromEntries(Object.keys(SCORECARD_SORTS).map(
          (other) => [other, hooks[SCORECARD_SORT_HEADS[other].head].getAttribute("aria-sort")]));
      }
      at.titles[key] = hooks[SCORECARD_SORT_HEADS[key].control].title;
    }
    scorecardSort.key = ""; scorecardSort.direction = "";
    paintSortHeads(scorecardSort);
    at.aria.served = Object.fromEntries(Object.keys(SCORECARD_SORTS).map(
      (key) => [key, hooks[SCORECARD_SORT_HEADS[key].head].getAttribute("aria-sort")]));
    // The picker: its own headers, through the shared sorter, drawn by
    // the renderer a header click calls, with a selection that is not the
    // first row so a sort that moved it would be seen.
    const offered = at.picker;
    store.mergeModel = offered.length ? offered[offered.length - 1] : "";
    at.chosen = store.mergeModel;
    at.pickerNames = Object.fromEntries(pickerRows(pickable()).map(
      (m) => [m.id, String(m.display_name || m.id || "")]));
    at.pickerOrders = {}; at.pickerAria = {}; at.pickerChecked = {}; at.pickerTitles = {};
    for (const key of Object.keys(PICKER_SORT_HEADS)) {
      for (const direction of ["ascending", "descending"]) {
        pickerSort.key = key; pickerSort.direction = direction;
        renderPickerRows();
        const drawn = hooks["picker-rows"].childNodes.map((row) => row.childNodes[0].childNodes[0]);
        at.pickerOrders[key + " " + direction] = drawn.map((radio) => radio.value);
        at.pickerChecked[key + " " + direction] = drawn.filter((radio) => radio.checked).map((radio) => radio.value);
        at.pickerAria[key + " " + direction] = Object.fromEntries(Object.keys(PICKER_SORT_HEADS).map(
          (other) => [other, hooks[PICKER_SORT_HEADS[other].head].getAttribute("aria-sort")]));
      }
      at.pickerTitles[key] = hooks[PICKER_SORT_HEADS[key].control].title;
    }
    pickerSort.key = ""; pickerSort.direction = "";
    renderPickerRows();
    at.pickerServed = hooks["picker-rows"].childNodes.map((row) => row.childNodes[0].childNodes[0].value);
    out[name] = at;
  }
  // A click sorts ascending, the next one descending, and the choice is kept.
  globalThis.window = { localStorage: {
    getItem: (k) => (k in kept ? kept[k] : null), setItem: (k, v) => { kept[k] = String(v); } } };
  const clicks = [];
  for (let n = 0; n < 3; n += 1) {
    sortBy(scorecardSort, "cost");
    clicks.push(scorecardSort.key + " " + scorecardSort.direction);
  }
  sortBy(scorecardSort, "loss");
  clicks.push(scorecardSort.key + " " + scorecardSort.direction);
  const stored = kept[scorecardSort.storage] || "";
  // The picker's sort is its own, kept under its own key.
  sortBy(pickerSort, "cost");
  sortBy(pickerSort, "cost");
  const picker = pickerSort.key + " " + pickerSort.direction;
  const pickerStored = kept[pickerSort.storage] || "";
  const scorecardAfter = scorecardSort.key + " " + scorecardSort.direction;
  pickerSort.key = ""; pickerSort.direction = "";
  loadSort(pickerSort);
  const pickerReloaded = pickerSort.key + " " + pickerSort.direction;
  scorecardSort.key = ""; scorecardSort.direction = "";
  loadSort(scorecardSort);
  const reloaded = scorecardSort.key + " " + scorecardSort.direction;
  // Storage that throws on every access: the sort still applies.
  globalThis.window = { localStorage: {
    getItem: () => { throw new Error("blocked"); }, setItem: () => { throw new Error("blocked"); } } };
  let blocked = "";
  try {
    scorecardSort.key = ""; scorecardSort.direction = "";
    loadSort(scorecardSort);
    sortBy(scorecardSort, "speed");
    blocked = scorecardSort.key + " " + scorecardSort.direction;
  } catch (error) {
    blocked = "threw: " + String(error);
  }
  out.clicks = { clicks, stored, reloaded, blocked, picker, pickerStored,
                 scorecardAfter, pickerReloaded,
                 keys: [scorecardSort.storage, pickerSort.storage] };
  process.stdout.write(JSON.stringify(out));
})();
"""


def scorecard_scenarios(payload: dict) -> dict:
    """Three `/config`s from one served payload: none, one of each, all.

    `none`: no endpoint and no command route. `one`: the OpenAI endpoint and
    the Opus subscription route, beside a Google row that lists a model while
    unconfigured -- a listing is no endpoint. `all`: every provider configured,
    every route, and a self-hosted listing holding one name a measured row
    already claims and one it does not.
    """
    import copy

    def with_providers(config: dict, configured: set, listed: dict) -> dict:
        for row in config["endpoints"]["providers"]:
            row["configured"] = row["name"] in configured
            row["models"] = list(listed.get(row["name"], []))
        return config

    names = {row["name"] for row in payload["endpoints"]["providers"]}
    check({"openai", "google", "self-hosted", "anthropic"} <= names,
          f"the served providers are {sorted(names)}; the scenarios need all four")
    wire = next(entry["api_model"] for entry in catalogue.models()
                if entry.get("provider") == "self-hosted")
    none = with_providers(copy.deepcopy(payload), set(), {})
    none["commands"]["routes"] = []
    one = with_providers(copy.deepcopy(payload), {"openai"}, {"google": ["gemini-unlisted-x"]})
    one["commands"]["routes"] = [route for route in payload["commands"]["routes"]
                                 if route["id"] == "claude-opus"]
    every = with_providers(copy.deepcopy(payload), set(names),
                           {"self-hosted": ["qwen3:8b", wire]})
    return {"none": none, "one": one, "all": every}


def drive_scorecard(js: str, scenarios: dict) -> dict | None:
    """The shipped script under node over `scenarios`, or None without node."""
    node = node_command()
    if node is None:
        return None
    program = (EFFORT_DOM + "\nconst INPUT = " + json.dumps(
        {"strings": catalogues()["en"], "scenarios": scenarios}) + ";\n" + js
        + SCORECARD_DRIVE)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as handle:
        handle.write(program)
        path = handle.name
    try:
        run = subprocess.run(node + [path], capture_output=True, text=True,
                             timeout=120, cwd=ROOT)
    finally:
        os.unlink(path)
    if run.returncode != 0:
        return {"error": run.stderr[-600:]}
    return json.loads(run.stdout)


def expected_picker(config: dict) -> list[str]:
    """The rows the picker must list, formed from the payload alone."""
    configured = {row["name"] for row in config["endpoints"]["providers"] if row["configured"]}
    routes = config["commands"]["routes"]
    known = {route.get("model") or "" for route in routes}
    rows = ["command:" + route["id"] for route in routes]
    for entry in config["catalogue"]["models"]:
        known.add(entry.get("api_model") or entry["id"])
        retired = bool((entry.get("retired") or {}).get("on"))
        if not retired and (not entry.get("provider") or entry["provider"] in configured):
            rows.append(entry["id"])
    for row in config["endpoints"]["providers"]:
        for name in row["models"]:
            if name in known:
                continue
            known.add(name)
            if row["configured"]:
                rows.append(row["name"] + ":" + name)
    return rows


def scorecard_figures(config: dict) -> dict:
    """Each scorecard id's retired flag and sort figures, formed from the payload.

    `other` marks a route row whose figures were measured on a model its alias
    no longer answers as: `alias_now.model` differs from `resolved_model`.
    """
    fields = ("usd_per_merge", "seconds_per_merge", "silent_loss_per_pair",
              "deviations_per_pair")

    def numbers(measured, route: bool) -> dict:
        out = {}
        for field in fields:
            value = (measured or {}).get(field)
            ok = isinstance(value, (int, float)) and not isinstance(value, bool)
            out[field] = None if (not ok or (route and field == "usd_per_merge")) else value
        return out

    def other(entry: dict) -> bool:
        now = (entry.get("alias_now") or {}).get("model")
        return bool(now and entry.get("resolved_model") and now != entry["resolved_model"]
                    and entry.get("measured"))

    def name_now(entry: dict) -> str:
        now = (entry.get("alias_now") or {}).get("model")
        if not now:
            return entry.get("display_name") or entry["route"]
        row = next((m for m in config["catalogue"]["models"]
                    if now in (m.get("id"), m.get("api_model"))), {})
        return f"{row.get('display_name') or now} (subscription)"

    rows = {}
    block = config["catalogue"].get("command_routes") or []
    for route in config["commands"]["routes"]:
        entry = next((row for row in block if row["route"] == route["id"]
                      and row["model"] == route.get("model")
                      and row["profile"] == route.get("profile")), {})
        rows["command:" + route["id"]] = {"retired": False, "name": route["label"],
                                          "other": other(entry),
                                          **numbers(entry.get("measured"), True)}
    served = {(route["id"], route.get("model"), route.get("profile"))
              for route in config["commands"]["routes"]}
    for entry in block:
        if (entry["route"], entry["model"], entry["profile"]) in served:
            continue
        rows["catalogue-route:" + entry["route"]] = {
            "retired": False, "name": name_now(entry), "other": other(entry),
            **numbers(entry.get("measured"), True)}
    for entry in config["catalogue"]["models"]:
        rows[entry["id"]] = {"retired": bool((entry.get("retired") or {}).get("on")),
                             "name": entry.get("display_name") or entry["id"],
                             "other": False,
                             **numbers(entry.get("measured"), False)}
    return rows


SORT_FIELDS = {"cost": ("usd_per_merge",), "speed": ("seconds_per_merge",),
               "loss": ("silent_loss_per_pair", "deviations_per_pair"),
               "deviations": ("deviations_per_pair",), "name": ()}


def order_problems(order: list[str], key: str, direction: str, rows: dict) -> list[str]:
    """Every way one sorted order breaks the rules. Empty is pass.

    Retired rows after every live one; within each, a row with no figure on a
    field after every row with one, in both directions; a row measured on a
    model its route no longer runs after every row with a figure of its
    own, before every row with none; the figures in order.
    """
    problems = []
    tag = f"{key} {direction}"
    if sorted(order) != sorted(rows):
        return [f"{tag}: the order is not a permutation of the scorecard's rows"]
    flags = [rows[i]["retired"] for i in order]
    if flags != sorted(flags):
        problems.append(f"{tag}: a retired row sorts above a live one: {order}")
    sign = 1 if direction == "ascending" else -1
    for group in (False, True):
        ids = [i for i in order if rows[i]["retired"] is group]
        for a, b in zip(ids, ids[1:]):
            for field in SORT_FIELDS[key]:
                left, right = rows[a][field], rows[b][field]
                if left is None and right is None:
                    continue
                if left is None:
                    problems.append(f"{tag}: unmeasured {a} sorts above {b}")
                    break
                if right is None:
                    break
                if rows[a]["other"] != rows[b]["other"]:
                    if rows[a]["other"]:
                        problems.append(f"{tag}: {a}, measured on another model, "
                                        f"sorts above {b}")
                    break
                if sign * (left - right) > 0:
                    problems.append(f"{tag}: {a} ({left}) above {b} ({right}) on {field}")
                if left != right:
                    break
    return problems


def scorecard_problems(driven: dict | None, scenarios: dict, strings: dict) -> list[str]:
    """Everything the picker and scorecard must satisfy, over one drive."""
    if driven is None:
        return []
    if "error" in driven:
        return [f"the scorecard did not run under node: {driven['error']}"]
    problems = []
    every_model = [entry["id"] for entry in catalogue.models()]
    every_route = [entry["route"] for entry in catalogue.load().get("command_routes") or []]
    for name, config in scenarios.items():
        at = driven[name]
        want = expected_picker(config)
        if at["picker"] != want:
            problems.append(f"{name}: the picker lists {at['picker']}, not {want}")
        shown = set(at["scorecard"])
        missing = [i for i in every_model if i not in shown]
        missing += [r for r in every_route
                    if "command:" + r not in shown and "catalogue-route:" + r not in shown]
        if missing:
            problems.append(f"{name}: the scorecard leaves out {missing}")
        listed = [i for i in shown if i not in scorecard_figures(config)]
        if listed:
            problems.append(f"{name}: the scorecard shows rows with no catalogue entry: {listed}")
        rows = scorecard_figures(config)
        for tag, order in at["orders"].items():
            key, direction = tag.split(" ")
            problems += [f"{name}: {problem}" for problem in
                         order_problems(order, key, direction, rows)]
            aria = at["aria"][tag]
            wrong = {k: v for k, v in aria.items() if v != (direction if k == key else "none")}
            if wrong:
                problems.append(f"{name}: sorted by {tag}, aria-sort reads {aria}")
        # By name, not by id: two routes may share a label, and a tie keeps
        # the served order whichever way.
        live = [rows[i]["name"] for i in at["orders"]["name ascending"] if not rows[i]["retired"]]
        down = [rows[i]["name"] for i in at["orders"]["name descending"] if not rows[i]["retired"]]
        if down != live[::-1]:
            problems.append(f"{name}: name descending is not name ascending reversed")
        if set(at["aria"]["served"].values()) != {"none"}:
            problems.append(f"{name}: the served order reads aria-sort {at['aria']['served']}")
        for key, title in at["titles"].items():
            want_key = "scorecard.sort.perpair" if key == "deviations" else f"scorecard.sort.{key}"
            if title != strings.get(want_key):
                problems.append(f"{name}: the {key} header's tooltip is {title!r}")
        # The picker: the same rules over its own rows, the selection
        # never moved by a sort, and the served order when nothing is chosen.
        blank = {field: None for fields in SORT_FIELDS.values() for field in fields}
        picker_rows = {i: rows.get(i, {"retired": False, "name": at["pickerNames"].get(i, i),
                                       "other": False, **blank}) for i in at["picker"]}
        if set(at["pickerOrders"]) != {f"{k} {d}" for k in
                                       ("name", "cost", "speed", "loss", "deviations")
                                       for d in ("ascending", "descending")}:
            problems.append(f"{name}: the picker sorts on {sorted(at['pickerOrders'])}")
        for tag, order in at["pickerOrders"].items():
            key, direction = tag.split(" ")
            problems += [f"{name}: picker {problem}" for problem in
                         order_problems(order, key, direction, picker_rows)]
            aria = at["pickerAria"][tag]
            wrong = {k: v for k, v in aria.items() if v != (direction if k == key else "none")}
            if wrong:
                problems.append(f"{name}: picker sorted by {tag}, aria-sort reads {aria}")
            want_checked = [at["chosen"]] if at["chosen"] else []
            if at["pickerChecked"][tag] != want_checked:
                problems.append(f"{name}: sorting the picker by {tag} selects "
                                f"{at['pickerChecked'][tag]}, not {want_checked}")
        if at["picker"] and at["pickerServed"] != at["picker"]:
            problems.append(f"{name}: the picker's served order is {at['pickerServed']}")
        for key, title in at["pickerTitles"].items():
            want_key = "scorecard.sort.perpair" if key == "deviations" else f"scorecard.sort.{key}"
            if title != strings.get(want_key):
                problems.append(f"{name}: the picker's {key} header's tooltip is {title!r}")
    clicks = driven["clicks"]
    if clicks["clicks"] != ["cost ascending", "cost descending", "cost ascending", "loss ascending"]:
        problems.append(f"a header click does not toggle ascending and descending: {clicks['clicks']}")
    if json.loads(clicks["stored"] or "null") != {"key": "loss", "direction": "ascending"}:
        problems.append(f"the sort is not kept per browser: {clicks['stored']!r}")
    if clicks["reloaded"] != "loss ascending":
        problems.append(f"a kept sort does not come back: {clicks['reloaded']!r}")
    if clicks["blocked"] != "speed ascending":
        problems.append(f"blocked storage breaks the sort: {clicks['blocked']!r}")
    if clicks["picker"] != "cost descending" or clicks["pickerReloaded"] != "cost descending":
        problems.append(f"the picker's header clicks do not toggle and keep: {clicks}")
    if json.loads(clicks["pickerStored"] or "null") != {"key": "cost", "direction": "descending"}:
        problems.append(f"the picker's sort is not kept per browser: {clicks['pickerStored']!r}")
    if clicks["scorecardAfter"] != "loss ascending":
        problems.append(f"sorting the picker moved the scorecard's sort: {clicks['scorecardAfter']!r}")
    if len(set(clicks["keys"])) != 2:
        problems.append(f"the picker and the scorecard keep their sort under one key: {clicks['keys']}")
    return problems


def test_the_picker_lists_what_can_run_and_the_scorecard_lists_everything() -> None:
    """Driven: the picker holds only configured rows, the scorecard every
    catalogue row, and the scorecard's sorts put unmeasured and retired rows
    last in both directions with `aria-sort` saying which way. The
    picker's headers sort through the same code, never move the selection,
    and keep their own sort under their own key.

    Must-fire: nine breakages of the shipped script, each alone. Must-not-fire:
    the shipped script over the same three scenarios.
    """
    payload = served_config_with_routes()
    # No shipped row is retired and no shipped route carries alias_now
    # any more (Opus 5 was removed from the card entirely rather than kept
    # retired, and opus's own resolved_model caught up with its alias), so
    # the "retired row" and "measured on another model" sort rules below have
    # no real data left to exercise them. Fabricated instead: a retired model
    # row (a copy of a live one, still measured, matching the "kept, dated,
    # not offered" shape `validate_retired` holds every retired row to), and
    # an alias_now on claude-sonnet, the same construction test_route_label.py
    # and the effort-card test above use.
    import copy as _copy
    template = next(e for e in payload["catalogue"]["models"] if e.get("measured"))
    retired_row = _copy.deepcopy(template)
    retired_row["id"] = "test-retired-model"
    retired_row["api_model"] = "test-retired-model-wire"
    retired_row["display_name"] = "Test Retired Model"
    retired_row["retired"] = {"on": "2026-09-25", "decision": 618,
                              "replacement": "Test Successor"}
    payload["catalogue"]["models"].append(retired_row)
    sonnet_route = next(e for e in payload["catalogue"]["command_routes"]
                        if e["route"] == "claude-sonnet")
    sonnet_route["alias_now"] = {"model": "claude-opus-5-5", "checked_on": "2026-09-26",
                                 "cli_version": "2.1.283"}
    scenarios = scorecard_scenarios(payload)
    strings = catalogues()["en"]
    js = source(APP_JS)
    driven = drive_scorecard(js, scenarios)
    if driven is None:
        decline("UNMEASURED: no node here, so the picker and scorecard were not driven")
        return
    for problem in scorecard_problems(driven, scenarios, strings):
        check(False, problem)
    # The three scenarios must be able to tell the rules apart at all.
    check(len(expected_picker(scenarios["none"])) == 0
          and len(expected_picker(scenarios["one"])) < len(expected_picker(scenarios["all"])),
          "the scenarios no longer vary what the picker lists")
    unserved = [i for i in driven["none"]["scorecard"] if i.startswith("catalogue-route:")]
    check(len(unserved) == len(catalogue.load().get("command_routes") or []),
          f"with no route served, the scorecard shows {unserved}")
    seeds = {
        "a picker that ignores the endpoint":
            js.replace("    reachable(model) && !isRetired(model));",
                       "    !isRetired(model));"),
        "a picker that offers a retired row":
            js.replace("    reachable(model) && !isRetired(model));",
                       "    reachable(model));"),
        "a scorecard of configured rows only":
            js.replace("filter((/** @type {any} */ model) => !model.listed);",
                       "filter((/** @type {any} */ model) => !model.listed && reachable(model));"),
        "a scorecard without the routes this server does not serve":
            js.replace("return rows.slice(0, at).concat(unserved, rows.slice(at));",
                       "return rows;"),
        "an unmeasured figure sorted as zero":
            js.replace("      if (left === null) return 1;\n      if (right === null) return -1;\n",
                       "      if (left === null || right === null) return sign * ((left || 0) - (right || 0));\n"),
        "unmeasured last only when ascending":
            js.replace("      if (left === null) return 1;\n      if (right === null) return -1;\n",
                       "      if (left === null) return sign;\n      if (right === null) return -sign;\n"),
        "retired rows sorted among the live ones":
            js.replace("    if (retired) return retired;\n", ""),
        "figures measured on another model ranked as current":
            js.replace("      if (other) return other;\n", ""),
        "aria-sort never set":
            js.replace("state.key === key ? state.direction : \"none\"", "\"none\""),
        "a click that never reverses":
            js.replace("&& state.direction === \"ascending\" ? \"descending\" : \"ascending\";",
                       "? \"ascending\" : \"ascending\";"),
        "a sort that is never kept":
            js.replace("window.localStorage.setItem(state.storage,",
                       "void (state.storage,"),
        # The picker's own half.
        "a picker that is never sorted":
            js.replace("const rows = scorecardOrder(offered, pickerSort.key, pickerSort.direction);",
                       "const rows = offered;"),
        "a picker sort that clears the selection":
            js.replace("  paintSortHeads(pickerSort);\n  return rows.length;",
                       "  paintSortHeads(pickerSort);\n  store.mergeModel = \"\";\n  return rows.length;"),
        "a picker sorted by the scorecard's state":
            js.replace("const rows = scorecardOrder(offered, pickerSort.key, pickerSort.direction);",
                       "const rows = scorecardOrder(offered, scorecardSort.key, scorecardSort.direction);"),
        "a picker kept under the scorecard's key":
            js.replace('storage: "llossless.picker.sort"', 'storage: "llossless.scorecard.sort"'),
    }
    for what, seeded in seeds.items():
        check(seeded != js, f"the seed {what!r} did not change the script")
        check(bool(scorecard_problems(drive_scorecard(seeded, scenarios), scenarios, strings)),
              f"the picker and scorecard check did not fire on {what}")


def test_the_scorecard_is_a_dialog_with_real_sort_buttons() -> None:
    """The scorecard opens from a button beside the picker, is a
    `<dialog>` on the credentials sheet's pattern, and every sortable header
    is a `<button>` inside a `<th>` that carries `aria-sort`.

    Must-fire: a header turned back into bare text, and `aria-sort` removed
    from one `<th>`, are each seen.
    """
    markup = source(INDEX)

    def problems(html: str) -> list[str]:
        found = []
        dialog = html[html.find('<dialog class="sheet scorecard"'):]
        dialog = dialog[:dialog.find("</dialog>")]
        if not dialog:
            return ["there is no scorecard <dialog>"]
        for key in ("name", "cost", "speed", "loss", "deviations"):
            head = re.search(r'<th [^>]*data-cc="sort-head-' + key + r'"[^>]*>(.*?)</th>',
                             dialog, re.S)
            if not head:
                found.append(f"no <th> for the {key} sort")
                continue
            if 'aria-sort="none"' not in head.group(0).split(">", 1)[0]:
                found.append(f"the {key} <th> starts without aria-sort")
            if not re.search(r'<button type="button" class="sort" data-cc="sort-' + key + '"',
                             head.group(1)):
                found.append(f"the {key} header is not a <button>")
        if 'data-cc="close-scorecard"' not in dialog or "autofocus" not in dialog:
            found.append("the scorecard's way out is missing or not focused on open")
        if 'id="about-list"' not in dialog:
            found.append("'About this list' is not in the scorecard")
        if 'data-cc="model-rows"' not in dialog:
            found.append("the full table is not in the scorecard")
        page = html[:html.find("<dialog")]
        if 'data-cc="open-scorecard"' not in page or 'data-cc="picker-rows"' not in page:
            found.append("the picker and its scorecard button are not on the page")
        return found

    for problem in problems(markup):
        check(False, problem)
    seeded = markup.replace('<button type="button" class="sort" data-cc="sort-cost"',
                            '<span class="sort" data-cc="sort-cost"')
    check(seeded != markup and bool(problems(seeded)), "a header that is not a button is not caught")
    seeded = markup.replace('aria-sort="none" data-cc="sort-head-loss"', 'data-cc="sort-head-loss"')
    check(seeded != markup and bool(problems(seeded)), "a <th> without aria-sort is not caught")
    css = source(STATIC / "app.css")
    check("table.models th button.sort:focus-visible" in css,
          "the scorecard's sort buttons must keep a focus ring after `all: unset`")
    js = strip_comments(source(APP_JS))
    wired = body_of(js, "function wire()")
    for piece in ('el("open-scorecard").addEventListener("click"', "scorecard.showModal()",
                  'scorecard.addEventListener("close", () => el("open-scorecard").focus())'):
        check(piece in wired, f"wire() no longer does {piece!r}")


def test_the_picker_shows_all_four_figures_again() -> None:
    """The picker was earlier narrowed to configured rows only; dropping seconds
    and deviations from it was never part of that ask, and the operator
    called it out as an overreach. Speed and deviations come back beside cost
    and silent loss, banded and worded like silent loss already was -- no raw
    number, no test count, so the row stays one line and the table stays
    compact.

    Must-fire: one of the two returning columns removed from `pickerRow` or
    from the picker's own sort headers.
    """
    js = strip_comments(source(APP_JS))
    html = source(INDEX)
    row = body_of(js, "function pickerRow(")
    for field, scale in (("seconds_per_merge", "RANK_SCALES.seconds_per_merge"),
                         ("deviations_per_pair", "RANK_SCALES.deviations_per_pair")):
        check(f'bandOnlyCell(model.measured, "{field}",' in row and scale in row,
              f"pickerRow no longer bands {field}")
    for key in ("speed", "deviations"):
        check(key in picker_sort_heads_keys(js),
              f"the picker's sort headers no longer include {key}")
    picker = html[html.find('<table class="models picker"'):]
    picker = picker[:picker.find("</table>")]
    for hook in ("picker-sort-head-speed", "picker-sort-head-deviations"):
        check(f'data-cc="{hook}"' in picker, f"the picker's markup has no {hook}")

    seeded = js.replace(
        '  row.appendChild(bandOnlyCell(model.measured, "seconds_per_merge",\n'
        '                               RANK_SCALES.seconds_per_merge));\n', "")
    check(seeded != js, "the seconds-cell probe's anchor has moved")
    check('bandOnlyCell(model.measured, "seconds_per_merge"' not in body_of(
        strip_comments(seeded), "function pickerRow("),
        "dropping the seconds cell from pickerRow is not caught")


def picker_sort_heads_keys(js: str) -> set:
    """The keys `PICKER_SORT_HEADS` declares, read out of the shipped script."""
    start, end = block(js, "const PICKER_SORT_HEADS = {")
    return set(re.findall(r"^\s*(\w+):\s*\{", js[start:end], re.M))


PICKER_SHORT_HEADS = {
    "models.picker.col.cost": "cost",
    "models.picker.col.speed": "speed",
    "models.picker.col.loss": "loss",
    "models.picker.col.deviations": "deviations",
}


def test_the_pickers_headers_are_one_word_and_the_scorecards_stay_precise() -> None:
    """The operator, seeing the picker's German header row squeeze the
    model name: *"'Speed', 'Cost', 'Loss' and 'Deviations' is sufficient."*
    The picker's four figure headers move to their own keys
    (`models.picker.col.*`), one word in either language ("Tempo", "Kosten",
    "Verlust", "Abweichungen"), with the unit and the full meaning in the "?"
    beside each. **The scorecard keeps its longer, precise headers**
    (`models.col.*`, unchanged: "Cost / merge", "Seconds / merge", "Silent
    loss", "Deviations / test") -- the dialog has the width for them and is
    where a reader goes to read rather than scan, so the two tables are
    deliberately inconsistent with each other rather than both compromising.
    """
    html = source(INDEX)
    picker = html[html.find('<table class="models picker"'):]
    picker = picker[:picker.find("</table>")]
    tables = catalogues()
    for key, col in PICKER_SHORT_HEADS.items():
        check(f'data-t="{key}"' in picker,
              f"the picker's {col} header no longer names {key}")
        check(f'data-t="models.col.{col}"' not in picker,
              f"the picker's {col} header still shares the scorecard's long key")
        for tag, strings in sorted(tables.items()):
            text = strings.get(key, "")
            check(bool(text), f"{tag}.json has no string for {key}")
            check(" " not in text.strip(),
                  f"{tag}.json's {key} is {text!r}, not one word")

    scorecard = html[html.find('<dialog class="sheet scorecard"'):]
    scorecard = scorecard[:scorecard.find("</dialog>")]
    for col, want in (("cost", "Cost / merge"), ("speed", "Seconds / merge"),
                      ("loss", "Silent loss"), ("deviations", "Deviations / test")):
        check(f'data-t="models.col.{col}">{want}<' in scorecard,
              f"the scorecard's {col} header is no longer the long, precise one")

    seeded = html.replace('data-t="models.picker.col.cost">Cost<',
                          'data-t="models.col.cost">Cost / merge<')
    check(seeded != html, "the short-header probe's anchor has moved")
    seeded_picker = seeded[seeded.find('<table class="models picker"'):]
    seeded_picker = seeded_picker[:seeded_picker.find("</table>")]
    check('data-t="models.picker.col.cost"' not in seeded_picker,
          "the picker's cost header reverting to the scorecard's long key is not caught")


# Every figure column's help icon: both tables, `models.help.*` its
# meaning. Never "name" -- the model column is not a figure -- and never
# "Use"/"Check", which hold radios.
FIGURE_HELP_ICONS = (
    ("picker", "cost", "models.help.cost"),
    ("picker", "speed", "models.help.speed"),
    ("picker", "loss", "models.help.loss"),
    ("picker", "deviations", "models.help.deviations_per_pair"),
    ("scorecard", "cost", "models.help.cost"),
    ("scorecard", "speed", "models.help.speed"),
    ("scorecard", "loss", "models.help.loss"),
    ("scorecard", "deviations", "models.help.deviations_per_pair"),
)


def figure_help_problems(html: str) -> list[str]:
    """Every figure column's help icon: present, a sibling of its sort
    button rather than nested inside it (a click on it must not sort the
    column), focusable, described, and pointed at a paragraph holding the
    column's own catalogue key."""
    found = []
    for table, col, key in FIGURE_HELP_ICONS:
        hook = f"help-{table}-{col}"
        icon_tag = f'data-cc="{hook}"'
        if icon_tag not in html:
            found.append(f"no element carries {icon_tag}")
            continue
        icon_at = html.index(icon_tag)
        span_start = html.rfind("<span", 0, icon_at)
        span_end = html.index(">", icon_at) + 1
        span = html[span_start:span_end]
        if not span.startswith('<span class="col-help"'):
            found.append(f'{hook}: not on a <span class="col-help">')
        if 'tabindex="0"' not in span:
            found.append(f"{hook}: not focusable -- no tabindex")
        if f'aria-describedby="{hook}-why"' not in span:
            found.append(f"{hook}: no aria-describedby")
        # A sibling of the sort button, never its child: between the <th>
        # and the icon, every <button> opened must already be closed --
        # otherwise the icon is inside one and a click on it would sort.
        th_start = html.rfind("<th", 0, span_start)
        between = html[th_start:span_start]
        if between.count("<button") != between.count("</button>"):
            found.append(f"{hook}: sits inside an unclosed <button> -- "
                         f"clicking it would sort the column")
        why_id = f"{hook}-why"
        why_tag = f'id="{why_id}"'
        if why_tag not in html:
            found.append(f"{hook}: no #{why_id} paragraph")
            continue
        p_start = html.rfind("<p", 0, html.index(why_tag))
        p_end = html.index("</p>", p_start) + len("</p>")
        para = html[p_start:p_end]
        if f'data-t="{key}"' not in para:
            found.append(f"{hook}: #{why_id} does not carry data-t=\"{key}\"")
    return found


def test_every_figure_column_has_a_help_icon_on_both_tables() -> None:
    """The operator: *"add a tiny help icon for hover in the header row
    that explains the meaning. e.g. I am not sure what the 'pair' column
    meant and neither will a user."* Every figure column -- cost, speed,
    silent loss, deviations -- on the picker and on the scorecard carries a
    small "?" that is a sibling of the sort button rather than nested in it
    (the same pattern used for a row marker, on a header instead): `title` for a
    pointer (`paintColumnHelp`), `tabindex="0"` and `aria-describedby` a
    hidden paragraph in the same language for a screen reader. Sibling and
    not child is what keeps a click on the icon from also sorting the column
    it explains.
    """
    html = source(INDEX)
    for problem in figure_help_problems(html):
        check(False, problem)

    seeded = html.replace(
        '<button type="button" class="sort" data-cc="picker-sort-cost" data-sort="cost" data-t="models.picker.col.cost">Cost</button><span class="col-help" tabindex="0" data-cc="help-picker-cost"',
        '<button type="button" class="sort" data-cc="picker-sort-cost" data-sort="cost" data-t="models.picker.col.cost">Cost<span class="col-help" tabindex="0" data-cc="help-picker-cost"')
    check(seeded != html, "the nested-icon probe's anchor has moved")
    check(bool(figure_help_problems(seeded)),
          "an icon nested inside the sort button is not caught")

    seeded = html.replace(
        '<span class="col-help" tabindex="0" data-cc="help-scorecard-loss"',
        '<span class="col-help" data-cc="help-scorecard-loss"')
    check(seeded != html, "the missing-tabindex probe's anchor has moved")
    check(bool(figure_help_problems(seeded)),
          "a help icon with no tabindex is not caught")

    seeded = html.replace(
        'id="help-scorecard-deviations-why" data-t="models.help.deviations_per_pair"',
        'id="help-scorecard-deviations-why" data-t="models.help.loss"')
    check(seeded != html, "the wrong-key probe's anchor has moved")
    check(bool(figure_help_problems(seeded)),
          "a description paragraph pointed at the wrong catalogue key is not caught")


def test_a_headers_help_icon_never_breaks_onto_its_own_line() -> None:
    """The operator: *"can we force the question mark to be in the same
    line as the text? For Cost & Deviations it is in a new line, which looks
    stupid."* `th.num`'s `white-space: normal` lets a long scorecard
    phrase wrap at its own space, and the newline `index.html`'s indentation
    left between `</button>` and `<span class="col-help">` was exactly such
    a space -- a break point nothing asked for, found in a browser at a
    width no rule over these files would have caught. Both now sit inside
    one `<span class="col-label">`, `white-space: nowrap`, with no
    whitespace text node between the button and the icon inside it: one
    atomic inline box a line can break before or after but never inside.
    """
    css = strip_css_comments(source(APP_CSS))
    rule = re.search(r"table\.models th \.col-label\s*\{([^}]*)\}", css)
    check(bool(rule), "no table.models th .col-label rule in app.css")
    check("white-space: nowrap" in (rule.group(1) if rule else ""),
          ".col-label is missing `white-space: nowrap`, so the label and its "
          "icon can still be split across two lines")

    html = source(INDEX)
    for table, col in (("picker", "cost"), ("picker", "speed"), ("picker", "loss"),
                       ("picker", "deviations"), ("scorecard", "cost"),
                       ("scorecard", "speed"), ("scorecard", "loss"),
                       ("scorecard", "deviations")):
        hook = f"help-{table}-{col}"
        icon_at = html.index(f'data-cc="{hook}"')
        span_start = html.rfind("<span", 0, icon_at)
        before = html[max(0, span_start - 12):span_start]
        check(before.endswith("</button>"),
              f"{hook}: whitespace sits between the sort button and the "
              f"icon ({before!r}); a collapsed space there is a break point")
        label_start = html.rfind('<span class="col-label"', 0, span_start)
        check(label_start >= 0 and "</span>" not in html[label_start:span_start],
              f"{hook}: is not inside an (unclosed-so-far) .col-label wrapper")

    seeded = css.replace(
        "table.models th .col-label {\n"
        "  display: inline-flex; align-items: baseline; white-space: nowrap;\n"
        "}",
        "table.models th .col-label {\n"
        "  display: inline-flex; align-items: baseline;\n"
        "}")
    check(seeded != css, "the nowrap-wrapper probe's anchor has moved")
    rule = re.search(r"table\.models th \.col-label\s*\{([^}]*)\}", seeded)
    check("white-space: nowrap" not in (rule.group(1) if rule else ""),
          "a .col-label with no nowrap is not caught")


def test_the_catalogues_top_level_note_is_rendered_from_a_locale_key() -> None:
    """`/config` serves `catalogue.notes` in English, and `renderScorecard`
    printed it as served, so "About this list" showed an English paragraph on
    the German page, the same kind of leak over a different field. It now reads
    `models.catalogue.notes` (held to the shipped catalogue's own text by
    `tests/test_contract_parity.py`) and only falls back to hiding the
    paragraph when the served catalogue carries no note at all.
    """
    js = strip_comments(source(APP_JS))
    body = body_of(js, "function renderScorecard(")
    check('setText(el("catalogue-note"), notes ? t("models.catalogue.notes") : "");' in body,
          "renderScorecard no longer prints the note from the locale catalogue")

    seeded = js.replace(
        'setText(el("catalogue-note"), notes ? t("models.catalogue.notes") : "");',
        'setText(el("catalogue-note"), notes || "");')
    check(seeded != js, "the served-notes probe's anchor has moved")
    check('t("models.catalogue.notes")' not in body_of(seeded, "function renderScorecard("),
          "printing the served field again is not caught")


def test_a_rows_english_notes_are_marked_on_a_non_english_page() -> None:
    """`rowNotes` is a per-row *measurement record* -- who ran it, at
    which commit, over how many pairs -- not page prose, and stays English
    on every page rather than being translated (`text.lang = "en"` says so
    to a screen reader). That attribute is invisible to a sighted reader, so
    a German page showed a fold labelled "Anmerkungen" that opened on an
    English paragraph with no visible reason -- read as a forgotten
    translation, not a deliberate one. The fold's own summary now says so in
    words, on any page not in English, closed or open: "Anmerkungen (auf
    Englisch)".
    """
    js = strip_comments(source(APP_JS))
    row = body_of(js, "function scorecardRow(")
    check('locale.tag && locale.tag !== "en"' in row,
          "scorecardRow no longer checks the page's own language for the notes fold")
    check('t("scorecard.notes") + " " + t("scorecard.notes.foreign")' in row,
          "scorecardRow no longer marks the notes fold on a non-English page")
    check("text.lang = \"en\";" in row,
          "the notes paragraph no longer carries lang=\"en\" for a screen reader")

    for tag, strings in sorted(catalogues().items()):
        check("scorecard.notes.foreign" in strings,
              f"{tag}.json has no string for scorecard.notes.foreign")

    seeded = js.replace(
        '    const label = locale.tag && locale.tag !== "en"\n'
        '      ? t("scorecard.notes") + " " + t("scorecard.notes.foreign")\n'
        '      : t("scorecard.notes");\n'
        '    setText(summary, label);\n',
        '    setText(summary, t("scorecard.notes"));\n')
    check(seeded != js, "the foreign-notes-label probe's anchor has moved")
    check('t("scorecard.notes.foreign")' not in body_of(seeded, "function scorecardRow("),
          "a notes fold with no language marker is not caught")


def test_a_free_tier_row_keeps_its_metered_badge_and_says_so_beside_it() -> None:
    """A row measured on a vendor's free tier is still badged `metered API`.

    `routeKind` classifies the *endpoint*: a paid key at the same address is
    billed per token, so relabelling the badge from what `measured.billed`
    happened to be on one run would be a claim about the wrong thing.
    What changed is what these particular figures cost to make, and that is
    said beside the badge (`freeTierNote`, on both the picker and the
    scorecard row) and once in full under the scorecard table
    (`renderRouteCaveats`), not by touching `routeKind` or `routeLabel`.
    """
    js = strip_comments(source(APP_JS))

    # `routeKind` must not read `measured` or `billed` at all: the endpoint
    # kind is a property of the route, and this is the "do not relabel" half
    # of the fix, asserted at the one function that decides the badge word.
    kind = body_of(js, "function routeKind(")
    check("measured" not in kind and "billed" not in kind,
          "routeKind reads measured/billed; the badge must stay the endpoint's own kind")

    note = body_of(js, "function freeTierNote(")
    check('"free-tier"' in note and "models.route.mark.freetier" in note,
          "freeTierNote no longer checks measured.billed against catalogue.py's own value")

    for owner in ("function pickerRow(", "function scorecardRow("):
        found = body_of(js, owner)
        check("appendFreeTierNote(" in found,
              f"{owner} no longer shows the free-tier note beside the badge")

    caveats = body_of(js, "function renderRouteCaveats(")
    check("models.route.caveat.freetier" in caveats and "freeTierNote" in caveats,
          "renderRouteCaveats no longer explains the free-tier marker")

    for tag, strings in sorted(catalogues().items()):
        mark = strings.get("models.route.mark.freetier", "")
        caveat = strings.get("models.route.caveat.freetier", "")
        check(bool(mark.strip()), f"{tag}.json has no string for models.route.mark.freetier")
        check(bool(caveat.strip()), f"{tag}.json has no string for models.route.caveat.freetier")
        check(mark != strings.get("models.cost.freetier.cell"),
              f"{tag}.json gives the badge-side note and the cost cell the same word")

    # Seeded both ways: the note dropped from a row, and the caveat dropped
    # from under the table. Each must be caught by the checks above.
    dropped_row = js.replace(
        '  appendFreeTierNote(name, model);\n  row.appendChild(name);\n  row.appendChild(costCell(model));',
        '  row.appendChild(name);\n  row.appendChild(costCell(model));')
    check(dropped_row != js, "the pickerRow free-tier-note probe's anchor has moved")
    check("appendFreeTierNote(" not in body_of(dropped_row, "function pickerRow("),
          "dropping the free-tier note from pickerRow is not caught")

    raw = source(APP_JS)
    dropped_caveat = strip_comments(raw.replace(
        '  if (scorecardRows().some(\n'
        '      (/** @type {any} */ model) => Boolean(freeTierNote(model)))) {\n'
        '    said.push(t("models.route.caveat.freetier"));\n  }\n', ''))
    check(dropped_caveat != js, "the renderRouteCaveats free-tier probe's anchor has moved")
    check("models.route.caveat.freetier"
          not in body_of(dropped_caveat, "function renderRouteCaveats("),
          "dropping the free-tier caveat from renderRouteCaveats is not caught")


def test_loading_accounts_does_not_ask_a_server_with_no_account_store() -> None:
    """`loadAccounts` reads `session.tenanted` before it asks `/api/v1/accounts`.

    A server built with no account store serves no `/api/v1/accounts` route
    at all, a finding that predates this fix, so the request always
    404d there and the credentials sheet logged a console error on every
    open. `session.tenanted` is settled by the page's first request, before
    the sheet can be opened, so the fix is to ask it rather than the network.
    """
    js = strip_comments(source(APP_JS))

    def guards_before_fetching(text: str) -> bool:
        found = body_of(text, "async function loadAccounts()")
        guard, sep, _ = found.partition("getJson(ROUTES.accounts)")
        return bool(sep) and "session" in guard and "tenanted" in guard

    check(guards_before_fetching(js),
          "loadAccounts calls getJson(ROUTES.accounts) before checking "
          "session.tenanted, or checks something else")

    guard = ("  if (!(store.session && store.session.tenanted)) {\n"
             "    section.hidden = true;\n    return;\n  }\n")
    seeded = js.replace(guard, "")
    check(seeded != js, "the untenanted-guard probe's anchor has moved")
    check(not guards_before_fetching(seeded),
          "removing the tenanted guard is not caught")


# --------------------------------------------------------------------------
# the UI pass
# --------------------------------------------------------------------------

# The models field, top to bottom, as the operator asked for it. Each is
# a marker that occurs once in `index.html`. The scorecard button left this
# field for the step-nav beside Back/Next; its position is pinned
# separately, by nav_button_problems below.
MODELS_FIELD_ORDER = (
    ("the sentence saying what is listed", 'data-t="controls.models.hint"'),
    ("the picker table", 'data-cc="picker-box"'),
    ("the split checkbox", 'data-cc="split-models"'),
    ("the typed-id checkbox", 'data-cc="custom-toggle"'),
    ("the typed-id field and Send it to", 'data-cc="custom-endpoint"'),
    ("the window field", 'data-cc="window-block"'),
    ("the effort slider", 'data-cc="effort-block"'),
    ("the effort card", 'data-cc="effort-card-title"'),
)


def models_field_order_problems(html: str) -> list[str]:
    """Where the models field's pieces are out of the operator's order."""
    found = []
    at = []
    for name, marker in MODELS_FIELD_ORDER:
        if html.count(marker) != 1:
            found.append(f"{name} ({marker}) occurs {html.count(marker)} times")
            at.append(-1)
            continue
        at.append(html.index(marker))
    for (earlier, _), (later, _), a, b in zip(MODELS_FIELD_ORDER, MODELS_FIELD_ORDER[1:],
                                            at, at[1:]):
        if a >= 0 and b >= 0 and a > b:
            found.append(f"{later} comes before {earlier}")
    return found


def test_the_models_field_reads_in_the_operators_order() -> None:
    """Sentence, table, the two checkboxes and what they reveal, then
    the effort slider and card (the scorecard button's own place is checked
    separately, by test_the_detail_buttons_sit_beside_back_next below).

    Must-fire: the effort block back between the table and the checkboxes is
    caught.
    """
    markup = source(INDEX)
    for problem in models_field_order_problems(markup):
        check(False, problem)
    start = markup.index('      <div class="field effort-block" data-cc="effort-block" hidden>')
    end = markup.index("      </div>\n", markup.index('data-cc="effort-caveat"')) + len("      </div>\n")
    effort = markup[start:end]
    without = markup[:start] + markup[end:]
    split = without.index('      <label class="inline-check">\n        <input type="checkbox" data-cc="split-models">')
    seeded = without[:split] + effort + without[split:]
    check(bool(models_field_order_problems(seeded)),
          "the effort block above the checkboxes is not caught")


def picker_head_problems(html: str, js: str) -> list[str]:
    """The picker's sortable headers as markup and as wiring."""
    found = []
    table = html[html.find('<table class="models picker"'):]
    table = table[:table.find("</thead>")]
    for key in ("name", "cost", "loss"):
        head = re.search(r'<th [^>]*data-cc="picker-sort-head-' + key + r'"[^>]*>(.*?)</th>',
                         table, re.S)
        if not head:
            found.append(f"the picker has no <th> for the {key} sort")
            continue
        if 'aria-sort="none"' not in head.group(0).split(">", 1)[0]:
            found.append(f"the picker's {key} <th> starts without aria-sort")
        if not re.search(r'<button type="button" class="sort" data-cc="picker-sort-' + key + '"',
                         head.group(1)):
            found.append(f"the picker's {key} header is not a <button>")
    wired = body_of(strip_comments(js), "function wire()")
    for piece in ("loadSort(pickerSort);", "for (const state of [scorecardSort, pickerSort])",
                  'addEventListener("click", () => sortBy(state, key))'):
        if piece not in wired:
            found.append(f"wire() no longer does {piece!r}")
    return found


def test_the_picker_headers_sort_through_the_scorecards_code() -> None:
    """`<button>` in `<th>` with `aria-sort`, wired to the one sorter.

    Must-fire: a picker header turned back into text, and the picker's
    listeners left unwired, are each caught.
    """
    markup, js = source(INDEX), source(APP_JS)
    for problem in picker_head_problems(markup, js):
        check(False, problem)
    seeded = markup.replace('<button type="button" class="sort" data-cc="picker-sort-loss"',
                            '<span class="sort" data-cc="picker-sort-loss"')
    check(seeded != markup and bool(picker_head_problems(seeded, js)),
          "a picker header that is not a button is not caught")
    seeded = js.replace("for (const state of [scorecardSort, pickerSort])",
                        "for (const state of [scorecardSort])")
    check(seeded != js and bool(picker_head_problems(markup, seeded)),
          "a picker whose headers are never wired is not caught")
    check("function renderPickerRows(" in js and "renderPickerRows(models) === 0" in js,
          "renderModels no longer draws the picker through renderPickerRows")


# Where the two "open a dialog with more detail" buttons sit now: in
# their own step's Back/Next row, not on a row of their own above the
# control they explain. Superseded here: an earlier right-aligned `.models-head`
# row, which this button left.
NAV_BUTTON_PLACEMENT = (
    ("the Model scorecard button", "step-model",
     'class="ghost open-detail-btn" data-cc="open-scorecard"'),
    ("the See examples button", "step-settings",
     'class="ghost open-detail-btn" data-cc="open-compare"'),
)


def nav_button_problems(html: str) -> list[str]:
    """The operator: "put the Model scorecard button next to Back/Next
    buttons" and "put the See examples button also next to back/next so it
    is consistent." Both keep the shared open-detail-btn class and sit
    in the same position relative to Back/Next on both steps: before it.
    """
    found = []
    if "models-head" in html:
        found.append("models-head is still in the markup; the scorecard button left it")
    for name, panel_id, marker in NAV_BUTTON_PLACEMENT:
        panel_anchor = f'id="{panel_id}"'
        if panel_anchor not in html:
            found.append(f"{panel_id} is missing")
            continue
        panel_start = html.index(panel_anchor)
        nav_marker = '<div class="step-nav">'
        window = html[panel_start:panel_start + 2000]
        if nav_marker not in window:
            found.append(f"{panel_id} has no step-nav within reach")
            continue
        nav_start = html.index(nav_marker, panel_start)
        nav_end = html.index("</div>", nav_start)
        nav = html[nav_start:nav_end]
        if marker not in nav:
            found.append(f"{name} is not in {panel_id}'s step-nav, beside Back/Next")
            continue
        back = nav.find('data-step-go="')
        if back == -1 or nav.index(marker) > back:
            found.append(f"{name} does not come before Back in {panel_id}'s step-nav")
    return found


def test_the_detail_buttons_sit_beside_back_next() -> None:
    """Both detail buttons free the row they used to occupy alone, and
    read as one consistent pattern across the two steps.

    Must-fire: a button left back on a row of its own above the control it
    explains, `.models-head` markup reappearing, is each caught.
    """
    markup = source(INDEX)
    for problem in nav_button_problems(markup):
        check(False, problem)
    button_line = ('        <button type="button" class="ghost open-detail-btn" data-cc="open-scorecard" '
                   'aria-haspopup="dialog" data-t="scorecard.open">Model scorecard</button>\n')
    check(button_line in markup, "the scorecard button probe's anchor has moved")
    hint = markup.index('<p class="hint" data-t="controls.models.hint">')
    seeded = markup.replace(button_line, "", 1)
    seeded = seeded[:hint] + '      <div class="models-head">\n' + button_line + '      </div>\n' + seeded[hint:]
    check(seeded != markup and bool(nav_button_problems(seeded)),
          "the scorecard button back on its own row above the table is not caught")
    seeded = markup.replace(
        'class="ghost open-detail-btn" data-cc="open-compare"',
        'class="ghost compare-open" data-cc="open-compare"', 1)
    check(seeded != markup and bool(nav_button_problems(seeded)),
          "the See examples button losing the shared class is not caught")


def css_tokens(css: str) -> dict[str, dict[str, str]]:
    """The colour tokens of `:root`, light and dark, from `app.css`."""
    light = re.search(r"^:root \{(.*?)^\}", css, re.S | re.M)
    dark = re.search(r"@media \(prefers-color-scheme: dark\) \{\s*:root \{(.*?)\}", css, re.S)

    def read(block):
        return dict(re.findall(r"(--[a-z-]+):\s*(#[0-9a-fA-F]{6})", block.group(1) if block else ""))
    return {"light": read(light), "dark": {**read(light), **read(dark)}}


def contrast(one: str, two: str) -> float:
    """WCAG 2 contrast ratio of two #rrggbb colours."""
    def lum(colour: str) -> float:
        parts = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        parts = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in parts]
        return 0.2126 * parts[0] + 0.7152 * parts[1] + 0.0722 * parts[2]
    high, low = sorted((lum(one), lum(two)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def metered_badge_problems(css: str) -> list[str]:
    """The metered badge is amber and legible in both themes."""
    found = []
    rule = re.search(r"table\.models \.route-badge\.metered \{([^}]*)\}", css)
    if not rule:
        return ["there is no rule for the metered badge"]
    body = rule.group(1)
    for want in ("color: var(--warn)", "background: var(--warn-bg)", "border-color: var(--warn)"):
        if want not in body:
            found.append(f"the metered badge's rule has no {want!r}")
    subscription = re.search(r"table\.models \.route-badge\.subscription,\s*table\.models "
                             r"\.route-badge\.command \{([^}]*)\}", css)
    if subscription and "var(--warn)" in subscription.group(1):
        found.append("the subscription badge is amber too")
    for theme, tokens in css_tokens(css).items():
        for ground in ("--warn-bg", "--bg", "--panel"):
            if "--warn" not in tokens or ground not in tokens:
                found.append(f"{theme}: token --warn or {ground} is missing")
                continue
            ratio = contrast(tokens["--warn"], tokens[ground])
            if ratio < 4.5:
                found.append(f"{theme}: the metered badge's text is {ratio:.2f}:1 on {ground}")
    if not re.search(r"table\.models \.route-badge\.unknown \{[^}]*border-style: dashed", css):
        found.append("an unidentified route's badge is not dashed, so it reads as local")
    return found


def test_the_metered_badge_is_amber_and_legible() -> None:
    """Amber against the subscription's blue, 4.5:1 or better for its
    text on its fill and on the page, in light and dark.

    Must-fire: the rule removed, a light amber too pale to read, and the
    unidentified route's dashed border dropped are each caught.
    """
    css = source(APP_CSS)
    for problem in metered_badge_problems(css):
        check(False, problem)
    seeded = re.sub(r"table\.models \.route-badge\.metered \{[^}]*\}", "", css)
    check(seeded != css and bool(metered_badge_problems(seeded)), "a grey metered badge is not caught")
    seeded = css.replace("--warn: #8a5a00;", "--warn: #d9a441;", 1)
    check(seeded != css and bool(metered_badge_problems(seeded)), "a pale amber is not caught")
    seeded = css.replace("table.models .route-badge.unknown { border-style: dashed; }", "")
    check(seeded != css and bool(metered_badge_problems(seeded)),
          "an unknown route badge like the local one is not caught")


MARKS_DRIVE = r"""
;(() => {
  if (!El.prototype.addEventListener) El.prototype.addEventListener = function () {};
  strings = INPUT.strings;
  locale.tag = "en";
  const walk = (node, found) => {
    if (node.attributes && node.getAttribute("aria-describedby")) found.push(node);
    for (const child of node.childNodes || []) walk(child, found);
    return found;
  };
  const text = (node) => node.childNodes.length ? node.childNodes.map(text).join("") : node.textContent;
  const out = [];
  for (const config of Object.values(INPUT.scenarios)) {
    store.config = config;
    for (const model of scorecardRows()) {
      const route = routeOf(model);
      if (!route) continue;
      for (const [where, build] of [["picker", pickerRow], ["scorecard", scorecardRow]]) {
        if (where === "picker" && !pickerRows(pickable()).some((m) => m.id === model.id)) continue;
        const row = build(model);
        out.push({ id: model.id, where, comparable: Boolean(route.comparable), unserved: Boolean(route.unserved),
                   row: text(row),
                   explained: walk(row, []).map((n) => ({ text: n.textContent, title: n.title,
                     describedby: n.getAttribute("aria-describedby"), tabindex: n.getAttribute("tabindex") })) });
      }
    }
  }
  process.stdout.write(JSON.stringify(out));
})();
"""


def drive_marks(js: str, scenarios: dict) -> list | dict | None:
    """Every command row's markers as the shipped builders draw them."""
    node = node_command()
    if node is None:
        return None
    program = (EFFORT_DOM + "\nconst INPUT = " + json.dumps(
        {"strings": catalogues()["en"], "scenarios": scenarios}) + ";\n" + js + MARKS_DRIVE)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
        handle.write(program)
        path = handle.name
    try:
        run = subprocess.run(node + [path], capture_output=True, text=True, timeout=120, cwd=ROOT)
    finally:
        os.unlink(path)
    if run.returncode != 0:
        return {"error": run.stderr[-600:]}
    return json.loads(run.stdout)


def marks_problems(driven, strings: dict, html: str) -> list[str]:
    """The comparability marker in plain words, explained on hover and focus."""
    if driven is None:
        return []
    if isinstance(driven, dict):
        return [f"the markers did not run under node: {driven['error']}"]
    found = []
    mark = strings["models.route.mark.incomparable"]
    why = strings["models.route.mark.incomparable.why"]
    seen = 0
    for row in driven:
        tag = f"{row['id']} in the {row['where']}"
        if "(prompt)" in row["row"]:
            found.append(f"{tag} still shows the tier's identifier: {row['row']!r}")
        want = not row["comparable"] and not row["unserved"]
        got = [n for n in row["explained"] if n["text"] == mark]
        if want and len(got) != 1:
            found.append(f"{tag} has {len(got)} explained comparability markers")
            continue
        if not want:
            continue
        seen += 1
        node = got[0]
        if node.get("title") != why:
            found.append(f"{tag}: the marker's title is {node.get('title')!r}")
        if node["describedby"] != f"incomparable-why-{row['where']}":
            found.append(f"{tag}: aria-describedby is {node['describedby']!r}")
        if node["tabindex"] != "0":
            found.append(f"{tag}: the marker cannot be reached by keyboard")
    if not seen:
        found.append("no command row carried the comparability marker; the scenarios test nothing")
    for where in ("picker", "scorecard"):
        target = re.search(r'<p [^>]*id="incomparable-why-' + where + r'"[^>]*>', html)
        if not target or 'data-t="models.route.mark.incomparable.why"' not in target.group(0):
            found.append(f"there is no hidden explanation for the {where}'s marker to point at")
    return found


def test_the_comparability_marker_says_what_it_means() -> None:
    """The mark: "not directly comparable", no tier identifier, and the reason on
    the marker itself, by `title` and by `aria-describedby`.

    Must-fire: the tier put back in brackets, the `aria-describedby` dropped,
    the `title` dropped, and a hidden explanation removed are each caught.
    """
    scenarios = scorecard_scenarios(served_config_with_routes())
    strings, js, html = catalogues()["en"], source(APP_JS), source(INDEX)
    driven = drive_marks(js, scenarios)
    if driven is None:
        decline("UNMEASURED: no node here, so the route markers were not driven")
        return
    for problem in marks_problems(driven, strings, html):
        check(False, problem)
    seeds = {
        "the tier in brackets":
            js.replace('marks.push({ text: t("models.route.mark.incomparable"),',
                       'marks.push({ text: t("models.route.mark.incomparable") + " (prompt)",'),
        "no aria-describedby":
            js.replace('      piece.setAttribute("aria-describedby", describedBy);\n', ""),
        "no title": js.replace("      piece.title = t(mark.why);\n", ""),
    }
    for what, seeded in seeds.items():
        check(seeded != js, f"the seed {what!r} did not change the script")
        check(bool(marks_problems(drive_marks(seeded, scenarios), strings, html)),
              f"the marker check did not fire on {what}")
    seeded = html.replace('id="incomparable-why-scorecard"', 'id="elsewhere"')
    check(seeded != html and bool(marks_problems(driven, strings, seeded)),
          "a missing hidden explanation is not caught")


def cancel_ui_problems(html: str, js: str, strings: dict[str, dict[str, str]]) -> list[str]:
    """The page's real cancel: a button, a confirm, the route, the state."""
    found = []
    runbar = html[html.find('data-cc="run-card"'):]
    runbar = runbar[:runbar.find("</section>")]
    if 'data-cc="cancel-run"' not in runbar:
        found.append("there is no Cancel run button in the run bar")
    dialog = html[html.find('<dialog class="sheet confirm" data-cc="cancel-dialog"'):]
    dialog = dialog[:dialog.find("</dialog>")]
    if not dialog:
        found.append("there is no confirm step before a cancel")
    elif not re.search(r'data-cc="cancel-keep"[^>]*autofocus', dialog):
        found.append("the cancel dialog does not focus the button that keeps the run")
    for tag, words in (("en", ("billed", "cannot be undone", "stops any further calls")),
                       ("de", ("abgerechnet", "nicht rückgängig", "weiteren Aufrufe"))):
        text = strings.get(tag, {}).get("confirm.cancel.text", "")
        for word in words:
            if word not in text:
                found.append(f"{tag}: the cancel dialog does not say {word!r}")
    code = strip_comments(js)
    if 'cancel: "/api/v1/runs/{id}/cancel"' not in code:
        found.append("the cancel route is not in ROUTES")
    if 'sendJson("POST", route(ROUTES.cancel, { id: id }), {})' not in body_of(code, "async function requestCancel("):
        found.append("requestCancel does not POST the cancel route")
    if "showCancelRun(true);" not in body_of(code, "function watch("):
        found.append("watch() does not show the Cancel run button")
    if "showCancelRun(false);" not in body_of(code, "function stopWatching("):
        found.append("stopWatching() does not hide the Cancel run button")
    polled = body_of(code, "async function poll(")
    if 'status.state === "cancelled"' not in polled or "status.calls_made" not in polled:
        found.append("poll() does not land a cancelled run with its call count")
    if 'el("cancel-run").addEventListener("click", () => void confirmCancel());' not in body_of(code, "function wire()"):
        found.append("the Cancel run button is not wired to the confirm step")
    return found


def test_a_running_merge_can_be_cancelled_from_the_page() -> None:
    """The button: "Cancel run" while a run is followed, a confirm that says calls
    already made are billed, the cancel route, and a `cancelled` landing.

    Must-fire: the button never shown, the cancelled branch gone from the
    poll, and the billing sentence dropped from German are each caught.
    """
    html, js, strings = source(INDEX), source(APP_JS), catalogues()
    for problem in cancel_ui_problems(html, js, strings):
        check(False, problem)
    seeded = js.replace("  showCancelRun(true);\n", "")
    check(seeded != js and bool(cancel_ui_problems(html, seeded, strings)),
          "a Cancel run button that is never shown is not caught")
    seeded = js.replace('if (status.state === "cancelled") {', 'if (false) {')
    check(seeded != js and bool(cancel_ui_problems(html, seeded, strings)),
          "a poll that never lands a cancelled run is not caught")
    german = {tag: dict(table) for tag, table in strings.items()}
    german["de"]["confirm.cancel.text"] = "Wirklich abbrechen?"
    check(bool(cancel_ui_problems(html, js, german)),
          "a German cancel dialog that says nothing about billing is not caught")


# Internal words a reader of the page has no use for, and German's
# informal address, which the page does not use. "free tier" is the vendors'
# own name for a quota and stays.
JARGON = (
    ("a DECISIONS number", r"DECISIONS|\(\d{3}\)"),
    ("the structured-output tier", r"(?<!free )(?<!kostenlose )\btier\b"),
    ("json_schema", r"\bjson_schema\b"),
    ("argv", r"\bargv\b"),
    ("a cassette", r"\bcassette|\bKassette"),
    ("UNMEASURED in capitals", r"\bUNMEASURED\b|\bUNGEMESSEN\b"),
)
INFORMAL_GERMAN = r"\b(du|dich|dir|dein|deine|deiner|deinem|deinen|deines)\b|\b(Installiere|ändere|schreibe|Melde|Richte)\b"


def jargon_problems(tables: dict[str, dict[str, str]]) -> list[str]:
    """Every user-facing string that carries internal jargon."""
    found = []
    for tag, table in sorted(tables.items()):
        for key, text in sorted(table.items()):
            for name, pattern in JARGON:
                if re.search(pattern, text):
                    found.append(f"{tag}.json {key} carries {name}: {text[:80]!r}")
            if tag == "de" and re.search(INFORMAL_GERMAN, text):
                found.append(f"de.json {key} says du, and the page says Sie: {text[:80]!r}")
    return found


def test_the_page_speaks_to_a_reader_not_a_developer() -> None:
    """No DECISIONS number, tier name, argv, cassette or capitalised
    UNMEASURED in any string, and one form of address in German.

    Must-fire: the retired row's old "(DECISIONS {decision})", the old
    "{tier} tier" sentence, and one German "du" are each caught.
    """
    tables = catalogues()
    for problem in jargon_problems(tables):
        check(False, problem)
    for key, text, tag in (
            ("models.retired", "retired {date}: deprecated in favour of {replacement} (DECISIONS {decision})", "en"),
            ("models.route.incomparable", "answers at the {tier} tier with no temperature and no seed", "en"),
            ("accounts.none", "Kein Konto außer deinem.", "de")):
        seeded = {name: dict(table) for name, table in tables.items()}
        seeded[tag][key] = text
        check(bool(jargon_problems(seeded)), f"the old {tag} {key} is not caught")


COPY_DRIVE = r"""
;(() => {
  if (!El.prototype.addEventListener) El.prototype.addEventListener = function () {};
  const text = (node) => node.childNodes.length ? node.childNodes.map(text).join(" ") : node.textContent;
  const out = {};
  for (const [tag, table] of Object.entries(INPUT.strings)) {
    strings = table; locale.tag = tag;
    store.config = INPUT.config;
    out[tag] = { depths: [], titles: {} };
    renderVerifyDepth();
    out[tag].depths = hooks["verify-depth"].childNodes.map(text);
    out[tag].delta = hooks["depth-delta"].textContent;
    for (const policy of INPUT.config.title_policy.policies) {
      store.titlePolicy = policy.value;
      renderTitlePolicy();
      out[tag].titles[policy.value] = hooks["title-explains"].textContent;
    }
  }
  process.stdout.write(JSON.stringify(out));
})();
"""


def drive_copy(js: str) -> dict | None:
    """The shipped depth picker and title explanation, rendered in each language."""
    node = node_command()
    if node is None:
        return None
    program = (EFFORT_DOM + "\nconst INPUT = " + json.dumps(
        {"strings": catalogues(), "config": served_config_with_routes()}) + ";\n" + js + COPY_DRIVE)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
        handle.write(program)
        path = handle.name
    try:
        run = subprocess.run(node + [path], capture_output=True, text=True, timeout=120, cwd=ROOT)
    finally:
        os.unlink(path)
    if run.returncode != 0:
        return {"error": run.stderr[-600:]}
    return json.loads(run.stdout)


def copy_problems(driven: dict | None, tables: dict, config_payload: dict) -> list[str]:
    """No served English sentence on the German page, in the depth picker or
    the title explanation, and each language's own copy where it belongs."""
    if driven is None:
        return []
    if "error" in driven:
        return [f"the copy did not render under node: {driven['error']}"]
    found = []
    served = [depth["name"] for depth in config_payload["verify_depth"]["depths"]]
    served += [depth["explains"] for depth in config_payload["verify_depth"]["depths"]]
    served += [policy["explains"] for policy in config_payload["title_policy"]["policies"]]
    for tag, table in sorted(tables.items()):
        at = driven.get(tag) or {}
        depths = " ".join(at.get("depths") or [])
        for depth in config_payload["verify_depth"]["depths"]:
            for part in ("name", "explains"):
                want = table.get(f"depth.{depth['value']}.{part}", "")
                if not want or want not in depths:
                    found.append(f"{tag}: the depth picker does not show depth.{depth['value']}.{part}")
        for policy, shown in sorted((at.get("titles") or {}).items()):
            if shown != table.get(f"title.{policy}.explains"):
                found.append(f"{tag}: the {policy} explanation reads {shown[:60]!r}")
        if tag != "de":
            continue
        rendered = depths + " " + " ".join((at.get("titles") or {}).values()) + " " + (at.get("delta") or "")
        for sentence in served:
            if sentence in rendered:
                found.append(f"de: an English string from /config is on the German page: {sentence[:60]!r}")
    return found


def test_the_depth_and_title_copy_is_german_on_the_german_page() -> None:
    """The depth picker, the depth comparison and the title explanation
    render from the catalogue by value, so no English sentence `/config`
    serves is left on the German page.

    Must-fire: the depth sentence and the title sentence each put back to the
    served English are caught.
    """
    tables = catalogues()
    payload = served_config_with_routes()
    js = source(APP_JS)
    driven = drive_copy(js)
    if driven is None:
        decline("UNMEASURED: no node here, so the depth and title copy were not driven")
        return
    for problem in copy_problems(driven, tables, payload):
        check(False, problem)
    seeds = {
        "the served depth sentence":
            js.replace('setText(explains, t("depth." + String(depth.value || "") + ".explains"));',
                       'setText(explains, String(depth.explains || ""));'),
        "the served title sentence":
            js.replace('active ? t("title." + String(active.value) + ".explains") : ""',
                       'active ? active.explains : ""'),
        "the served depth name":
            js.replace("  return t(\"depth.\" + value + \".name\");",
                       "  return String(((store.config.verify_depth || {}).depths || []).find((d) => d.value === value).name);"),
    }
    for what, seeded in seeds.items():
        check(seeded != js, f"the seed {what!r} did not change the script")
        check(bool(copy_problems(drive_copy(seeded), tables, payload)),
              f"the copy check did not fire on {what}")


STORAGE_DRIVE = r"""
const kept = {};
globalThis.window = { localStorage: {
  getItem: (k) => (k in kept ? kept[k] : null),
  setItem: (k, v) => { kept[k] = String(v); },
  removeItem: (k) => { delete kept[k]; } } };
const out = {};
kept["claimcheck.locale"] = "de";
out.oldOnly = storedLocale();
kept["llossless.locale"] = "en";
out.newRead = storedLocale();
rememberLocale("");
out.afterClear = { neu: kept["llossless.locale"] || "", read: storedLocale() };
rememberLocale("de");
out.afterChoice = kept["llossless.locale"] || "";
globalThis.window = { localStorage: {
  getItem: () => { throw new Error("blocked"); },
  setItem: () => { throw new Error("blocked"); },
  removeItem: () => { throw new Error("blocked"); } } };
try { out.blocked = storedLocale(); rememberLocale("de"); out.blockedThrew = false; }
catch (error) { out.blockedThrew = true; }
process.stdout.write(JSON.stringify(out));
"""

STORAGE_EXPECTED = {
    "oldOnly": "", "newRead": "en",
    "afterClear": {"neu": "", "read": ""}, "afterChoice": "de",
    "blocked": "", "blockedThrew": False,
}


def drive_storage(js: str):
    """The shipped storage helpers under node, over `STORAGE_DRIVE`."""
    node = node_command()
    if node is None:
        return None
    names = ("storedLocale", "rememberLocale")
    key = js[js.index("const LOCALE_STORAGE_KEY = "):]
    key = key[:key.index("\n") + 1]
    program = key + "".join(js_function(n, js) + "\n}\n" for n in names) + STORAGE_DRIVE
    run = subprocess.run(node + ["-e", program], capture_output=True, text=True,
                         timeout=60, cwd=ROOT)
    return json.loads(run.stdout) if run.returncode == 0 else {"error": run.stderr[-300:]}


def test_browser_storage_ignores_the_old_keys() -> None:
    """`llossless.*` keys only; a value kept under the pre-rename prefix is not read.

    The code used to read the pre-rename key when the new one was empty; the operator's
    fresh-start ruling removed that. The language and both sorts are kept
    under `llossless.*`, a value under the old key is ignored, and storage
    that throws is never fatal.

    MUST FIRE: the shipped script with a fallback to the old key put back, and
    with the old key name.
    """
    js = source(APP_JS)
    for key in ('const LOCALE_STORAGE_KEY = "llossless.locale";',
                'storage: "llossless.scorecard.sort"', 'storage: "llossless.picker.sort"',
                "const raw = window.localStorage.getItem(state.storage);"):
        check(key in js, f"app.js no longer carries {key!r}")
    check("claimcheck." not in strip_comments(js) and "legacyStorageKey" not in js
          and "readStored" not in js,
          "app.js still names a `claimcheck.` storage key or its fallback reader")
    got = drive_storage(js)
    if got is None:
        decline("UNMEASURED: the storage-rename check needs node, and none runs here")
        return
    check(got == STORAGE_EXPECTED,
          f"the storage helpers as shipped: {got}, expected {STORAGE_EXPECTED}")
    seeds = {
        "a fallback to the old key":
            js.replace('    return window.localStorage.getItem(LOCALE_STORAGE_KEY) || "";\n',
                       '    return window.localStorage.getItem(LOCALE_STORAGE_KEY)\n'
                       '      || window.localStorage.getItem("claimcheck.locale") || "";\n'),
        "the old key name":
            js.replace('const LOCALE_STORAGE_KEY = "llossless.locale";',
                       'const LOCALE_STORAGE_KEY = "claimcheck.locale";'),
    }
    for what, seeded in seeds.items():
        check(seeded != js, f"the seed {what!r} did not change the script")
        check(drive_storage(seeded) != STORAGE_EXPECTED,
              f"the storage-rename check did not fire on {what}")


SEND_DRIVE = r"""
const out = { read: {}, answered: {} };
for (const status of [204, 200]) {
  let read = false;
  globalThis.fetch = async () => ({
    status: status, ok: true,
    arrayBuffer: async () => { read = true; return new ArrayBuffer(0); },
    json: async () => { read = true; return { fine: true }; },
    text: async () => { read = true; return ""; },
  });
  out.answered[status] = await sendJson("DELETE", "/api/v1/session", undefined);
  out.read[status] = read;
}
process.stdout.write(JSON.stringify(out));
"""

SEND_EXPECTED = {"read": {"204": True, "200": True},
                 "answered": {"204": None, "200": {"fine": True}}}


def drive_send(js: str):
    """The shipped `sendJson` under node, with a `fetch` that says whether the body was read."""
    node = node_command()
    if node is None:
        return None
    program = ("async " + js_function("sendJson", js) + "\n}\n"
               + "function errorMessage() { return 'x'; }\n"
               + "(async () => {" + SEND_DRIVE + "})();")
    run = subprocess.run(node + ["-e", program], capture_output=True, text=True,
                         timeout=60, cwd=ROOT)
    return json.loads(run.stdout) if run.returncode == 0 else {"error": run.stderr[-300:]}


def test_a_204_is_read_before_it_is_answered() -> None:
    """`sendJson` reads a 204's empty body before it returns `null`.

    Returning on the status alone left the response unread, and Chromium then
    reported sign-out's `DELETE /api/v1/session` as `net::ERR_ABORTED` although
    its 204 had arrived and the sign-out worked. Every `DELETE` and most `PUT`s
    on this page answer 204, so the fix is in the one helper they share.

    MUST FIRE: the shipped script with the read removed.
    """
    js = source(APP_JS)
    got = drive_send(js)
    if got is None:
        decline("UNMEASURED: the 204 check needs node, and none runs here")
        return
    check(got == SEND_EXPECTED, f"sendJson as shipped: {got}, expected {SEND_EXPECTED}")
    seeded = js.replace("    await answer.arrayBuffer().catch(() => null);\n", "")
    check(seeded != js, "the seed 'the 204 left unread' did not change the script")
    check(drive_send(seeded) != SEND_EXPECTED,
          "the 204 check did not fire on a sendJson that leaves the body unread")


# --------------------------------------------------------------------------
# the persisted queue on the page
# --------------------------------------------------------------------------


def state_word_gaps(js: str) -> list[str]:
    """Job states the server can report that the page has no word for."""
    from llossless.web import jobs
    words = table(js, "const STATE_KEYS = {")
    return [state for state in jobs.STATES if state not in words]


def test_every_job_state_has_a_word_on_the_page() -> None:
    """`interrupted` and every other state reads in the reader's language.

    Must fire on the shipped script with the new state's row taken out.
    """
    js = source(APP_JS)
    check(state_word_gaps(js) == [],
          f"job states with no word on the page: {state_word_gaps(js)}")
    seeded = js.replace('  interrupted: "state.interrupted",\n', "", 1)
    check(seeded != js and state_word_gaps(seeded) == ["interrupted"],
          "must fire: a STATE_KEYS without interrupted passed")


def function_body(js: str, name: str) -> str:
    """The text of one top-level function declaration, braces balanced."""
    start = re.search(r"\n(?:async )?function " + re.escape(name) + r"\(", js)
    if start is None:
        return ""
    depth = 0
    opened = False
    for position in range(js.index("{", start.end()), len(js)):
        if js[position] == "{":
            depth += 1
            opened = True
        elif js[position] == "}":
            depth -= 1
            if opened and depth == 0:
                return js[start.start():position + 1]
    return ""


def notification_problems(js: str) -> list[str]:
    """Where the page asks for notification permission, and what it shows."""
    problems = []
    asks = js.count("requestPermission(")
    body = function_body(js, "askToNotify")
    if asks != 1 or "requestPermission(" not in body:
        problems.append(f"requestPermission is called {asks} time(s), and must be "
                        f"called once, inside askToNotify")
    callers = [m.start() for m in re.finditer(r"askToNotify\(", js)]
    wired = 'el("notify").addEventListener("click", () => void askToNotify());'
    if len(callers) != 2 or wired not in js:
        problems.append("askToNotify is reached from somewhere other than the "
                        "Notify me click")
    announce = function_body(js, "announceLanding")
    shown = re.findall(r"new window\.Notification\(([\s\S]*?)\);", announce)
    if len(shown) != 1 or "{ body: id.slice(0, 8), tag: id }" not in shown[0] \
            or not re.search(r'"notify\.failed"\s*:\s*"notify\.done"', shown[0]):
        problems.append(f"the notification must carry only its title and the "
                        f"short id: {shown}")
    if js.count("new window.Notification(") != 1:
        problems.append("a notification is constructed outside announceLanding")
    return problems


def test_notifications_are_asked_for_on_a_click_and_carry_no_content() -> None:
    """Permission only on "Notify me", never on load; title and short id only.

    Must fire on the shipped script with a permission request added at load,
    and with the document's text put into the notification body.
    """
    js = source(APP_JS)
    check(notification_problems(js) == [],
          f"notifications: {notification_problems(js)}")
    on_load = js.replace("function wire() {\n",
                         "function wire() {\n  void window.Notification.requestPermission();\n", 1)
    check(any("requestPermission" in p for p in notification_problems(on_load)),
          "must fire: a permission request on load passed")
    leaky = js.replace("{ body: id.slice(0, 8), tag: id }",
                       "{ body: store.merged, tag: id }", 1)
    check(any("short id" in p for p in notification_problems(leaky)),
          "must fire: a notification carrying the merged document passed")


def test_the_retry_and_notify_controls_are_translated_in_both_languages() -> None:
    """The pinned pairs: every new string exists in English and German."""
    catalogues = {tag: json.loads((ROOT / "src" / "llossless" / "web" / "locales"
                                   / f"{tag}.json").read_text(encoding="utf-8"))["strings"]
                  for tag in ("en", "de")}
    keys = ("run.retry", "run.notify", "run.notify.on", "status.queued.position",
            "status.interrupted", "error.retry", "word.interrupted",
            "state.interrupted", "history.follow", "history.log", "history.retry",
            "history.position", "history.retryof", "notify.done", "notify.failed",
            "confirm.retry.heading", "confirm.retry.text", "confirm.retry.ok",
            "confirm.retry.keep")
    for key in keys:
        english, german = catalogues["en"].get(key), catalogues["de"].get(key)
        check(bool(english) and bool(german) and english != german,
              f"{key} is missing or untranslated: {english!r} / {german!r}")
    check("billed again" in catalogues["en"]["confirm.retry.text"]
          and "erneut abgerechnet" in catalogues["de"]["confirm.retry.text"],
          "the retry confirmation must say the new run may be billed again, in both")


def output_tab_problems(app: str, markup: str) -> list[str]:
    """Both output tabs are always on the page, and a disabled one still answers Tab.

    "This run" and "Earlier runs" become "Current run" and "Previous
    runs", and the second tab stops hiding itself: both are shown from the
    first load, `aria-disabled` rather than `hidden` until there is a run or a
    history entry behind them, each with its own tooltip that says what will
    happen once it is live. `disabled` would pull the tab out of the Tab
    order; `aria-disabled` keeps it reachable, which is the point.
    """
    problems = []
    for tab_id, hint_id in (("output-tab-run", "output-tab-run-hint"),
                            ("output-tab-history", "output-tab-history-hint")):
        if f'id="{tab_id}"' not in markup:
            problems.append(f"{tab_id} is missing from index.html")
            continue
        tag = markup[markup.index(f'id="{tab_id}"'):]
        tag = tag[:tag.index(">")]
        if "hidden" in tag:
            problems.append(f"{tab_id} carries `hidden`; both output tabs must "
                            f"stay on the page and reachable, merely disabled")
        if 'aria-disabled="true"' not in tag:
            problems.append(f"{tab_id} does not start `aria-disabled`, so it "
                            f"looks live before anything is behind it")
        if f'aria-describedby="{hint_id}"' not in tag:
            problems.append(f"{tab_id} is not described by its own tooltip")
        if f'id="{hint_id}"' not in markup:
            problems.append(f"{hint_id} -- the tab's explanation -- is missing")

    body = js_function("enableRunTab", app)
    if 'setAttribute("aria-disabled", "false")' not in body:
        problems.append("enableRunTab does not clear the Current run tab's "
                        "aria-disabled")
    for name, why in (("submit", "starting a run"), ("follow", "following a "
                      "run from the list"), ("replay", "replaying a past run")):
        fn = js_function(name, app)
        if "enableRunTab();" not in fn:
            problems.append(f"{name} never calls enableRunTab, so {why} would "
                            f"leave the Current run tab looking disabled")

    show = js_function("showOutput", app)
    if 'getAttribute("aria-disabled") === "true"' not in show:
        problems.append("showOutput does not refuse a click or an arrow-key "
                        "selection on a disabled tab")

    sync = js_function("syncHistoryTab", app)
    if 'setAttribute("aria-disabled"' not in sync:
        problems.append("syncHistoryTab no longer drives the Previous runs "
                        "tab's aria-disabled from whether the list is empty")
    if "tab.hidden = " in sync:
        problems.append("syncHistoryTab still hides the tab outright instead "
                        "of disabling it in place")
    return problems


def test_the_output_tabs_are_always_shown_and_disabled_until_live() -> None:
    app, markup = source(APP_JS), source(INDEX)
    for problem in output_tab_problems(app, markup):
        check(False, problem)

    strings = strings_table()
    german = catalogues().get("de", {})
    for key, must_not_equal_english in (
        ("layout.output.run", True), ("layout.output.history", True),
        ("layout.output.run.hint", True), ("layout.output.history.hint", True)):
        english, translated = strings.get(key), german.get(key)
        check(bool(english) and bool(translated),
              f"{key} is missing in English or German")
        if must_not_equal_english:
            check(english != translated, f"{key} is not translated: {english!r}")
    check(strings.get("layout.output.run") == "Current run",
          "layout.output.run should read 'Current run'")
    check(strings.get("layout.output.history") == "Previous runs",
          "layout.output.history should read 'Previous runs'")

    seeds = {
        "the history tab keeps hidden instead of aria-disabled": (
            "aria-selected=\"false\" tabindex=\"-1\" aria-disabled=\"true\" "
            "aria-describedby=\"output-tab-history-hint\"\n"
            "                data-t=\"layout.output.history\">Previous runs</button>",
            "aria-selected=\"false\" tabindex=\"-1\" aria-disabled=\"true\" "
            "aria-describedby=\"output-tab-history-hint\" hidden\n"
            "                data-t=\"layout.output.history\">Previous runs</button>"),
    }
    for what, (old, new) in seeds.items():
        seeded = markup.replace(old, new, 1)
        check(seeded != markup, f"the probe for {what} did not take")
        check(bool(output_tab_problems(app, seeded)),
              f"the output-tab check does not fire on {what}")

    no_enable = app.replace(
        "  const keep = input(\"save-defaults\").checked ? currentDefaults() : null;\n"
        "  store.defaultsNote = null;\n  enableRunTab();\n",
        "  const keep = input(\"save-defaults\").checked ? currentDefaults() : null;\n"
        "  store.defaultsNote = null;\n", 1)
    check(no_enable != app, "the probe for submit() dropping enableRunTab did not take")
    check(bool(output_tab_problems(no_enable, markup)),
          "the output-tab check does not fire when submit() never enables the tab")


def save_defaults_problems(app: str) -> list[str]:
    """The save-defaults box tracks agreement with the saved set, not a one-shot tick.

    It used to untick itself the instant a save succeeded, which read as "your
    settings were not saved" to the operator mid-run. It now stays exactly as
    the reader left it, and instead follows whether the settings the page
    would submit right now still equal what is saved -- ticked after a run
    started with it ticked, unticked the moment a setting changes away from
    the saved set, and ticked again on reload whenever they still agree.
    """
    problems = []
    if "function sameShape(" not in app:
        problems.append("sameShape is missing: order-independent equality is "
                        "needed because a value read back from the server is "
                        "not guaranteed the same key order as one built here")
    if "function syncSaveDefaultsChecked(" not in app:
        problems.append("syncSaveDefaultsChecked is missing")
    sync = js_function("syncSaveDefaultsChecked", app)
    if "sameShape(currentDefaults(), store.defaults)" not in sync:
        problems.append("syncSaveDefaultsChecked does not compare the current "
                        "settings against the saved ones")

    save = js_function("saveDefaults", app)
    if 'input("save-defaults").checked = false' in save:
        problems.append("saveDefaults still unticks the box on a successful "
                        "save; it must leave the box as the reader set it")

    idle = js_function("refreshIdleStatus", app)
    if idle.count("syncSaveDefaultsChecked();") < 2:
        problems.append("refreshIdleStatus does not call syncSaveDefaultsChecked "
                        "from both of its branches (a run in view, and idle), so "
                        "a page load would not tick the box even when the loaded "
                        "settings already equal the saved ones")

    layout_fn = js_function("wireLayout", app)
    if "syncSaveDefaultsChecked();" not in layout_fn:
        problems.append("wireLayout's input-pane edit handler never calls "
                        "syncSaveDefaultsChecked, so editing a setting away "
                        "from the saved set would leave the box wrongly ticked")

    for caller in ("startOver", "resetDefaults"):
        fn = js_function(caller, app)
        if 'input("save-defaults").checked = false' not in fn:
            problems.append(f"{caller} must still explicitly untick the box: "
                            f"there is nothing left to compare it against")
    return problems


def test_the_save_defaults_box_tracks_agreement_not_a_one_shot_tick() -> None:
    app = source(APP_JS)
    for problem in save_defaults_problems(app):
        check(False, problem)

    seeds = {
        "the old behaviour, unticking on every successful save": (
            'store.defaultsNote = { key: "defaults.saved", tone: "ok", detail: "" };\n',
            'store.defaultsNote = { key: "defaults.saved", tone: "ok", detail: "" };\n'
            '    input("save-defaults").checked = false;\n'),
        "syncSaveDefaultsChecked dropped from refreshIdleStatus": (
            "  renderStepStates();\n  renderSaveDefaults();\n  syncSaveDefaultsChecked();\n}",
            "  renderStepStates();\n  renderSaveDefaults();\n}"),
        "syncSaveDefaultsChecked dropped from the input-pane edit handler": (
            'const onEdit = () => { renderStepStates(); syncSaveDefaultsChecked(); };',
            'const onEdit = () => { renderStepStates(); };'),
    }
    for what, (old, new) in seeds.items():
        seeded = app.replace(old, new, 1)
        check(seeded != app, f"the probe for {what} did not take")
        check(bool(save_defaults_problems(seeded)),
              f"the save-defaults check does not fire on {what}")


def reset_defaults_dialog_problems(html: str, js: str) -> list[str]:
    """The operator: "the reset settings button should ask with a
    confirmation dialog if the user really wants to reset the settings and
    lose their custom configuration." `resetDefaults` forgets the saved set
    on the server (`DELETE` on the defaults route) and puts every live
    control on the page back to the built-in defaults at once
    (`clearSettings`), so it is asked for the same way `confirmStartOver`
    asks before `startOver`: a `<dialog>`, "Keep my settings" first and
    focused, Escape and the backdrop both keeping everything as it was.
    """
    found = []
    dialog = 'data-cc="reset-defaults-dialog"'
    if dialog not in html:
        found.append("there is no reset-defaults-dialog")
        return found
    if "</dialog>" not in html[html.index(dialog):]:
        found.append("reset-defaults-dialog is never closed")
        return found
    block_ = html[html.index(dialog):html.index("</dialog>", html.index(dialog))]
    if 'data-t="confirm.resetdefaults.heading"' not in block_:
        found.append("the dialog has no heading string")
    if 'data-t="confirm.resetdefaults.text"' not in block_:
        found.append("the dialog has no body text saying what is lost")
    keep = re.search(r'<button[^>]*data-cc="reset-defaults-keep"[^>]*>', block_)
    if keep is None or "autofocus" not in keep.group(0) or 'class="ghost"' not in keep.group(0):
        found.append("Keep my settings must be the ghost button, focused on open")
    ok = re.search(r'<button[^>]*data-cc="reset-defaults-ok"[^>]*>', block_)
    if ok is None or 'class="primary"' not in ok.group(0):
        found.append("the confirm button must be the primary button")

    wired = body_of(strip_comments(js), "function wire()")
    if ('el("defaults-reset").addEventListener("click", '
        '() => void confirmResetDefaults());') not in wired:
        found.append("defaults-reset is not wired to confirmResetDefaults")
    if ('el("defaults-reset").addEventListener("click", '
        '() => void resetDefaults());') in wired:
        found.append("defaults-reset still resets without asking first")

    js_clean = strip_comments(js)
    if "async function confirmResetDefaults()" not in js_clean:
        found.append("there is no confirmResetDefaults function")
        return found
    confirm = body_of(js_clean, "async function confirmResetDefaults()")
    for piece in ('el("reset-defaults-dialog")', "showModal()",
                  'el("reset-defaults-ok").onclick = () => finish(true)',
                  'el("reset-defaults-keep").onclick = () => finish(false)',
                  "dialog.onclose = () => finish(false)",
                  "if (answer) await resetDefaults();"):
        if piece not in confirm:
            found.append(f"confirmResetDefaults no longer does {piece!r}")
    return found


def test_resetting_saved_settings_asks_first() -> None:
    """A reset that skips the dialog, or a dialog with no way to say no,
    must each fail this check.

    Must-fire: the click handler wired straight to resetDefaults again, and
    the dialog missing its "keep" text, are each caught.
    """
    markup, js = source(INDEX), source(APP_JS)
    for problem in reset_defaults_dialog_problems(markup, js):
        check(False, problem)
    seeded = js.replace(
        'el("defaults-reset").addEventListener("click", () => void confirmResetDefaults());',
        'el("defaults-reset").addEventListener("click", () => void resetDefaults());', 1)
    check(seeded != js and bool(reset_defaults_dialog_problems(markup, seeded)),
          "a reset wired straight past the confirm dialog is not caught")
    seeded = markup.replace('data-t="confirm.resetdefaults.text"', 'data-t="confirm.resetdefaults.note"', 1)
    check(seeded != markup and bool(reset_defaults_dialog_problems(seeded, js)),
          "a dialog that stops saying what is lost is not caught")
    seeded = js.replace("if (answer) await resetDefaults();", "await resetDefaults();", 1)
    check(seeded != js and bool(reset_defaults_dialog_problems(markup, seeded)),
          "a reset that runs whether or not the dialog was answered yes is not caught")


def favicon_problems(markup: str) -> list[str]:
    """The page names its icons, and every icon it names is a file here."""
    named = re.findall(r'<link rel="icon" href="([^"]+)"', markup)
    found = []
    if not any(name.endswith(".svg") for name in named):
        found.append(f"no SVG favicon is named: {named}")
    if not any(name.endswith(".png") for name in named):
        found.append(f"no PNG fallback favicon is named: {named}")
    found += [f"a named favicon is not in static/: {name}" for name in named
              if not name.startswith("data:") and not (STATIC / name).is_file()]
    return found


def test_the_page_names_its_favicon() -> None:
    """The favicon (2026-09-29): "LL" on the header's amber, SVG plus a 32 px PNG."""
    markup = INDEX.read_text(encoding="utf-8")
    check(not favicon_problems(markup), f"favicon: {favicon_problems(markup)}")
    seeded = re.sub(r'<link rel="icon"[^>]*>\n?', "", markup)
    seeded = seeded.replace("<title>", '<link rel="icon" href="data:,">\n<title>', 1)
    check(bool(favicon_problems(seeded)),
          "must fire: the empty placeholder icon passed")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_static" and callable(function):
            function()
    for line in unmeasured:
        print(line)
    if failures:
        print(f"web static: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web static: {checks} checks pass"
          + (f", {len(unmeasured)} declined" if unmeasured else ""))
    return 3 if unmeasured else 0


def test_web_static() -> None:
    """pytest entry point."""
    assert main() in (0, 3), "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
