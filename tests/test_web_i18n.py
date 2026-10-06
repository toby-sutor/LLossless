#!/usr/bin/env python3
"""The two catalogues, the endpoint that serves them, and what must not move.

W8 is the German translation of the web interface. It is three files --
`web/locales/en.json`, `web/locales/de.json` and `web/i18n.py` -- plus a route
and a picker, and almost everything that can go wrong with it is silent:

**A half-translated catalogue looks translated.** The obvious design is a
lookup that falls back to English for a key the chosen language does not
carry, and it is the wrong one: the operator reads the English sentences as
deliberate, as terms of art left in English on purpose, rather than as the gap
they are, and nobody ever files it. So `i18n.validate` refuses a catalogue
with a missing key **and** one with an orphan key, and the checks here are the
proof that it does -- seeded both ways, because a parity check that only fails
one way is half a check.

**A placeholder is part of the string.** `{n} of {max} documents` carries two
values the renderer substitutes, and a translation spelling one of them
`{maximum}` renders the brace and the word to the operator. The page loads,
the layout is right, and one sentence has `{max}` in the middle of it. Nothing
else in this suite would see that.

**A catalogue is the one input to the escaping funnel that arrives as data.**
`app.js` puts every string on the page through a single `.textContent =`
assignment; `tests/test_web_static.py` counts that assignment to keep it at
one. A `<` in a catalogue value would render as literal text at best, and
would tempt the next person to reach for `innerHTML` to make a `<br>` work.
The rule is therefore restated here as a property of the data.

**A record whose language depends on who downloaded it is not reproducible.**
`report.json`, `merged.md` and `report.html` are records. They are read by
scorers, by the paper and by the rest of this suite, and their identifiers --
`silent_loss`, `contradicted`, the finding kinds -- are machine-readable in
exactly the places that would break if they were words in whichever language a
browser happened to ask for. The check below fetches all three of them twice
through one running server, once under a German `Accept-Language` and once
under an English one, and asserts the bytes are the same. Beside it is the
check that makes that mean something: the *locale* endpoint, asked with the
same two headers, must answer differently. Two identical answers from a server
that ignores the header entirely would prove nothing at all.

Run with `python3 tests/test_web_i18n.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs. Servers are bound below -- this tool's
# own and the scripted endpoint behind it -- so this is the module's claim that
# the only sockets it opens are the ones it bound itself;
# `tests/test_socket_guard.py` asserts every test module states it in exactly
# this shape.
socket_guard.install()

from llossless.web import api, i18n  # noqa: E402

# The markup and script helpers live next door, where the files they parse do.
# Imported rather than copied: `catalogue_parity` is the predicate the seeded
# probes below fire, and a probe that re-implements the predicate it is probing
# proves only that the copy fires.
from test_web_static import (  # noqa: E402
    APP_JS, EFFORT_DOM, INDEX, PATIENCE, a_compiler, block, catalogue_parity,
    catalogues, live, node_command, origin, request, sink_hits, source,
    strip_comments)

from fake_endpoint import FakeEndpoint  # noqa: E402
from test_cli import CLEAN, SOURCE_A, SOURCE_B, Script  # noqa: E402

LOCALES = ROOT / "src" / "llossless" / "web" / "locales"

# The two headers every artefact check below is run under. Spelled out as a
# browser sends them, quality values and all, because the negotiation is over
# the whole header and a test that sent a bare tag would not exercise it.
GERMAN = "de-DE,de;q=0.9,en;q=0.8"
ENGLISH = "en-GB,en;q=0.9"

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


def raw_strings(tag: str) -> dict[str, str]:
    """One catalogue's strings as they are on disk, parsed and not validated.

    Every comparison below wants the file as written rather than as it would be
    served. `i18n.load` raises on a file that does not validate, and a raise
    here would turn "de.json is missing run.submit" -- which is the sentence
    somebody can act on -- into a traceback that names no key at all. Whether a
    file validates is asked separately, once, and answered in one line.
    """
    return i18n.read(tag)["strings"]


def catalogue(tag: str) -> dict:
    """One catalogue file as it is on disk, parsed and unvalidated."""
    return json.loads((LOCALES / f"{tag}.json").read_text(encoding="utf-8"))


def seeded(tag: str, mutate) -> tuple[Path, object]:
    """A temporary `locales/` holding the real files with one of them mutated.

    Returns the directory and the mutated payload, so a probe can hand either
    to `i18n` -- `validate` takes the payload, `load` and `negotiate` take the
    directory -- without either having to reconstruct the other.

    A copy on disk rather than a patched module global: `i18n` resolves the
    directory per call precisely so that a caller can point it somewhere else,
    and a probe that monkey-patched `LOCALES_DIR` would be testing a code path
    the server never takes.
    """
    directory = Path(tempfile.mkdtemp(prefix="cc-locales-"))
    for name in sorted(LOCALES.glob("*.json")):
        (directory / name.name).write_text(name.read_text(encoding="utf-8"),
                                           encoding="utf-8")
    payload = catalogue(tag)
    mutate(payload)
    (directory / f"{tag}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    return directory, payload


# --------------------------------------------------------------------------
# the two catalogues agree
# --------------------------------------------------------------------------

def test_every_catalogue_has_the_reference_s_key_set_exactly() -> None:
    """No missing string, no orphan, in either direction, for every file.

    Discovered rather than listed: a third language added to `locales/` is
    checked the day it lands, without anybody remembering to name it here.
    """
    reference = raw_strings(i18n.DEFAULT_TAG)
    check(len(reference) >= 100,
          f"the reference catalogue has {len(reference)} strings; the read has "
          f"drifted")
    tags = i18n.available()
    check(len(tags) >= 2,
          f"only {list(tags)} in web/locales/; there is meant to be a second "
          f"language")
    for tag in tags:
        strings = raw_strings(tag)
        missing = sorted(set(reference) - set(strings))
        orphans = sorted(set(strings) - set(reference))
        check(not missing, f"{tag}.json is missing {missing}")
        check(not orphans, f"{tag}.json carries strings nothing else has: {orphans}")


def test_the_key_set_check_fires_on_a_missing_key_and_on_an_orphan() -> None:
    """Seeded both ways. A parity check that fails one way is half a check.

    Both probes go through `i18n.load`, which is the call the server makes, so
    what is being shown is that a server handed either of these files refuses
    to serve it rather than serving a page half in English.
    """
    reference = raw_strings(i18n.DEFAULT_TAG)
    victim = sorted(reference)[0]

    directory, _ = seeded("de", lambda data: data["strings"].pop(victim))
    try:
        i18n.load("de", directory)
        check(False, "a catalogue with a key removed loads without complaint")
    except i18n.InvalidLocale as refusal:
        check(victim in str(refusal),
              f"the refusal does not name the missing key: {refusal}")

    directory, _ = seeded(
        "de", lambda data: data["strings"].update({"ghost.key": "x"}))
    try:
        i18n.load("de", directory)
        check(False, "a catalogue with an orphan key loads without complaint")
    except i18n.InvalidLocale as refusal:
        check("ghost.key" in str(refusal),
              f"the refusal does not name the orphan key: {refusal}")

    # And the other direction, on the shipped files, so the validator is not
    # simply refusing everything.
    for tag in i18n.available():
        try:
            i18n.load(tag)
        except i18n.InvalidLocale as refusal:
            check(False, f"the shipped {tag}.json does not validate: {refusal}")


def test_every_placeholder_survives_translation() -> None:
    """`{n}` is part of the string, so it is part of the parity check.

    A translation that drops or renames one renders the brace and the word to
    the operator, in the middle of an otherwise correct sentence. The sets have
    to match; the order does not, because German moves them.
    """
    reference = raw_strings(i18n.DEFAULT_TAG)
    for tag in i18n.available():
        strings = raw_strings(tag)
        for key in sorted(reference):
            wanted = set(i18n.PLACEHOLDER.findall(reference[key]))
            got = set(i18n.PLACEHOLDER.findall(strings.get(key, "")))
            check(wanted == got,
                  f"{tag}.json's {key!r} substitutes {sorted(got)} where the "
                  f"reference substitutes {sorted(wanted)}")


def test_the_placeholder_check_fires_on_a_renamed_placeholder() -> None:
    """Seeded: one `{max}` spelled `{maximum}` must be refused."""
    reference = raw_strings(i18n.DEFAULT_TAG)
    key = next(k for k, v in sorted(reference.items()) if "{max}" in v)

    def rename(data) -> None:
        data["strings"][key] = data["strings"][key].replace("{max}", "{maximum}")

    directory, _ = seeded("de", rename)
    try:
        i18n.load("de", directory)
        check(False, "a renamed placeholder loads without complaint")
    except i18n.InvalidLocale as refusal:
        check("max" in str(refusal),
              f"the refusal does not name the placeholder: {refusal}")


# --------------------------------------------------------------------------
# the catalogues and the page agree
# --------------------------------------------------------------------------

def test_every_rendered_key_exists_in_every_catalogue() -> None:
    """The key set the two files share is the key set the page renders.

    The predicate is `test_web_static.catalogue_parity`, where the markup and
    script parsers are. What this adds is that it is asked of **every**
    catalogue: a key set shared by two files that the page does not render is
    two translations of a dead string, and a page that renders a key neither
    file has prints the key.
    """
    found = catalogues()
    check(len(found) >= 2, f"only {sorted(found)} to check")
    for tag, strings in sorted(found.items()):
        for problem in catalogue_parity(tag, strings):
            check(False, problem)


def test_the_rendered_key_check_fires_in_both_directions() -> None:
    """Seeded both ways, through the same predicate the live check uses."""
    strings = dict(catalogues()[i18n.DEFAULT_TAG])
    check(not catalogue_parity("probe", strings),
          "the parity predicate fires on an unmodified catalogue")

    victim = "run.submit"
    check(victim in strings, "the probe's anchor has moved out of the catalogue")
    short = {key: value for key, value in strings.items() if key != victim}
    problems = catalogue_parity("probe", short)
    check(any(victim in problem for problem in problems),
          f"a catalogue missing {victim} does not fail the parity predicate")

    long = dict(strings)
    long["ghost.key"] = "nothing renders this"
    problems = catalogue_parity("probe", long)
    check(any("ghost.key" in problem for problem in problems),
          "a catalogue carrying a string nothing renders does not fail the "
          "parity predicate")


# --------------------------------------------------------------------------
# nothing becomes markup
# --------------------------------------------------------------------------

def test_no_catalogue_value_contains_markup() -> None:
    """Asserted of the data, because the data is what a translator edits.

    `app.js` escapes by construction and this is the assertion that it never
    has to: a `<` or `>` in a value renders as literal text at best, and at
    worst is the reason somebody reaches for `innerHTML` to make a `<br>` work.
    """
    for tag in i18n.available():
        for key, value in sorted(raw_strings(tag).items()):
            found = [mark for mark in i18n.MARKUP if mark in value]
            check(not found,
                  f"{tag}.json's {key!r} contains {found} and would reach the "
                  f"page as literal text")


def test_the_markup_scan_fires_on_a_seeded_tag() -> None:
    """Seeded: one `<br>` in one value must stop the whole file being served."""
    def inject(data) -> None:
        data["strings"]["run.submit"] = "Merge<br>and check"

    directory, _ = seeded("de", inject)
    try:
        i18n.load("de", directory)
        check(False, "a catalogue value carrying a tag loads without complaint")
    except i18n.InvalidLocale as refusal:
        check("run.submit" in str(refusal),
              f"the refusal does not name the offending key: {refusal}")


def test_the_escaping_funnel_the_catalogues_pass_through_still_exists() -> None:
    """One `.textContent =` and no sink, restated where the catalogue arrives.

    `tests/test_web_static.py` holds this too and seeds it. It is asserted
    again here because the catalogue changed what the funnel carries: the
    strings used to be literals in the script, reviewed with the code that
    renders them, and they are now a file a translator edits without ever
    opening `app.js`. The funnel is the only thing that makes that safe, so
    the file that introduced the arrangement asserts it rather than assuming
    the neighbour will keep doing so.
    """
    code = strip_comments(source(APP_JS))
    hits = sink_hits(code)
    check(not hits, f"app.js reaches for {hits}; every value goes through textContent")
    funnel = code.count(".textContent =")
    check(funnel == 1,
          f"{funnel} assignments to textContent; there is meant to be one, in "
          f"setText, so that every catalogue string reaching the page goes "
          f"through it")
    check("let strings = {}" in code,
          "app.js no longer holds the catalogue in a single table; the funnel "
          "check above is aimed at an arrangement that has moved")


def templated_keys() -> set[str]:
    """Every `data-t` key that lives inside a `<template>` in the markup."""
    html = source(INDEX)
    inside = re.findall(r"<template\b.*?</template>", html, re.S)
    found: set[str] = set()
    for fragment in inside:
        found |= set(re.findall(r'data-t="([^"]+)"', fragment))
    return found


def test_no_german_value_spells_an_umlaut_out_in_ascii() -> None:
    """`fuer` for `fur`, and the seven other transliterations that read as typos.

    German written without diacritics is what you get when a catalogue is typed
    on a keyboard that has none, or pasted through something that stripped them.
    It is not wrong in the sense a missing key is wrong -- the page renders, the
    parity check passes, `validate` is happy -- which is exactly why nothing
    caught it. A native reader sees a typo on every occurrence.

    This shipped: `controls.title.notitle` read "ist fuer einen Leser ein Titel
    und fuer die Heuristik" until 2026-09-19, having passed 858 other checks.

    The walk is recursive on purpose. The first pass over this file was written
    against `dict.items()`, the catalogue is nested, and it reported zero while
    `grep` was finding two -- a scan that cannot reach half its own subject is
    worse than none, because its silence reads as a clean result.
    """
    suspicious = re.compile(
        r"(?:fuer|ueber|koennen|muessen|waehrend|groesse|zurueck|loeschen|"
        r"schluessel|naechst|moeglich|aendern|erklaert|hoehe|pruefung)",
        re.IGNORECASE)

    def strings(node, path=""):
        if isinstance(node, dict):
            for key, value in node.items():
                yield from strings(value, f"{path}.{key}" if path else key)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                yield from strings(value, f"{path}[{index}]")
        elif isinstance(node, str):
            yield path, node

    catalogue = json.loads((LOCALES / "de.json").read_text(encoding="utf-8"))
    values = list(strings(catalogue))
    check(len(values) > 100,
          f"the walk reached {len(values)} values; a catalogue this small means "
          f"it stopped at a nesting level and is not scanning what it claims to")
    bad = [path for path, value in values if suspicious.search(value)]
    check(not bad, f"German values spelling an umlaut out in ASCII: {bad}")

    # Must-fire. Without it this passes on a catalogue the walk never entered,
    # and passing over nothing is the failure mode above.
    seeded = dict(catalogue)
    seeded["__probe__"] = "ist fuer einen Leser ein Titel"
    fired = [path for path, value in strings(seeded) if suspicious.search(value)]
    check(fired == ["__probe__"],
          f"the detector must fire on a seeded transliteration, got {fired}")


def test_a_row_cloned_out_of_a_template_is_translated_too() -> None:
    """The one place a missing translation is invisible in the reference language.

    `document.querySelectorAll("[data-t]")` does not descend into a
    `<template>`: its content is an inert fragment and not part of the
    document. So the boot-time pass translates the page and misses every row
    that is cloned afterwards, and the row arrives carrying the English text
    the markup holds as its no-script fallback. In English that is the right
    answer by accident; in German it is a document pane labelled "Upload a
    file" under a German heading, which is exactly what a real browser showed
    before `clone` was made to fill them.

    Nothing here renders anything, so what is pinned is the source property:
    the templates carry keys, and `clone` -- the one function that copies them
    -- applies the catalogue to the copy.
    """
    keys = templated_keys()
    check(len(keys) >= 5,
          f"only {sorted(keys)} found inside <template>; the discovery has drifted")
    reference = raw_strings(i18n.DEFAULT_TAG)
    missing = sorted(keys - set(reference))
    check(not missing, f"a template names keys no catalogue has: {missing}")
    js = strip_comments(source(APP_JS))
    start, end = block(js, "function clone(")
    check("applyStringsIn(" in js[start:end],
          "clone() no longer fills a cloned row's strings, so every template "
          "in index.html renders in the markup's language whatever the picker "
          "says")


def test_the_cloned_template_check_fires() -> None:
    """Seeded: `clone` without the call must fail, and with it must not."""
    js = strip_comments(source(APP_JS))
    start, end = block(js, "function clone(")
    body = js[start:end]
    check("applyStringsIn(" in body, "the probe's anchor has moved")
    check("applyStringsIn(" not in body.replace("applyStringsIn(", "noop("),
          "removing the call from clone() does not fail the check above")


# --------------------------------------------------------------------------
# the validator refuses what it cannot stand behind
# --------------------------------------------------------------------------

def test_the_validator_refuses_a_file_that_disagrees_with_its_own_name() -> None:
    """The filename is the tag a URL is matched against, so it is the tag."""
    directory, _ = seeded("de", lambda data: data.update({"tag": "fr"}))
    try:
        i18n.load("de", directory)
        check(False, "a catalogue calling itself another language loads")
    except i18n.InvalidLocale as refusal:
        check("fr" in str(refusal), f"the refusal does not say what it found: {refusal}")


def test_the_validator_refuses_a_file_with_no_label_for_the_picker() -> None:
    """A picker entry with no label is an option nobody can choose on purpose."""
    directory, _ = seeded("de", lambda data: data.update({"label": "  "}))
    try:
        i18n.load("de", directory)
        check(False, "a catalogue with a blank label loads")
    except i18n.InvalidLocale:
        check(True, "")


def test_the_validator_accepts_the_shipped_files_unchanged() -> None:
    """The must-not-fire for every probe above, stated once as its own check."""
    for tag in i18n.available():
        try:
            data = i18n.load(tag)
        except i18n.InvalidLocale as refusal:
            check(False, f"{tag}.json does not validate: {refusal}")
            continue
        check(data["tag"] == tag, f"{tag}.json calls itself {data['tag']!r}")
        check(bool(data["label"].strip()), f"{tag}.json has no label")


def test_a_broken_catalogue_is_dropped_from_the_picker_rather_than_listed() -> None:
    """An option that 409s when chosen is worse than one that was never there.

    The operator cannot tell a refusal on a chosen option from a network fault,
    so `describe` offers only what `load` would actually serve.
    """
    directory, _ = seeded("de", lambda data: data["strings"].clear())
    listed = [entry["tag"] for entry in i18n.describe(directory)]
    check("de" not in listed,
          f"a catalogue that does not validate is offered in the picker: {listed}")
    check(i18n.DEFAULT_TAG in listed,
          f"the reference language is not offered: {listed}")


# --------------------------------------------------------------------------
# negotiation
# --------------------------------------------------------------------------

def test_accept_language_decides_when_nothing_was_chosen() -> None:
    """The header, read as a header: weights, subtags and all."""
    cases = {
        GERMAN: "de",
        ENGLISH: "en",
        "de": "de",
        "de-AT": "de",
        "en;q=0.2, de;q=0.9": "de",
        "de;q=0.9, en;q=0.2": "de",
        "fr-FR,fr;q=0.9": "en",
        "*": "en",
        "": "en",
        "de;q=0": "en",
        "de;q=banana": "en",
    }
    for header, wanted in sorted(cases.items()):
        got = i18n.negotiate(header)
        check(got == wanted,
              f"Accept-Language {header!r} negotiated {got!r}, not {wanted!r}")


def test_the_negotiation_never_answers_with_a_locale_this_server_lacks() -> None:
    """Seeded: a directory with only English must answer English to everything.

    The must-fire is the pair of it -- the same header against the real
    directory answers German -- so what is shown is that negotiation depends on
    what is installed rather than on the header alone.
    """
    directory, _ = seeded("de", lambda data: data["strings"].clear())
    (directory / "de.json").unlink()
    check(i18n.negotiate(GERMAN, directory) == "en",
          "a server with no German catalogue negotiates German")
    check(i18n.negotiate(GERMAN) == "de",
          "the same header against the shipped catalogues does not reach German")


# --------------------------------------------------------------------------
# the endpoint
# --------------------------------------------------------------------------

def test_the_endpoint_serves_every_catalogue_whole() -> None:
    """Each tag, off a real server, with the strings the file holds."""
    with tempfile.TemporaryDirectory() as raw:
        built, thread = live(work=Path(raw) / "work")
        try:
            base = origin(built)
            for tag in i18n.available():
                status, _, body = request(f"{base}{api.API_PREFIX}/locales/{tag}")
                check(status == 200, f"/locales/{tag} answered {status}")
                payload = json.loads(body)
                check(payload.get("tag") == tag,
                      f"/locales/{tag} answered for {payload.get('tag')!r}")
                check(payload.get("strings") == raw_strings(tag),
                      f"/locales/{tag} does not serve the file's own strings")
                listed = [entry["tag"] for entry in payload.get("available", [])]
                check(sorted(listed) == sorted(i18n.available()),
                      f"/locales/{tag} lists {listed}, not {list(i18n.available())}")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


def test_an_unknown_locale_is_refused_rather_than_answered_in_english() -> None:
    """The refusal is what makes the page's fallback a decision it took.

    A server that answered `fr` with English under a `"tag": "fr"` the page
    believed would render English text under a French picker, and the operator
    would go looking for a translation nobody ever installed.
    """
    with tempfile.TemporaryDirectory() as raw:
        built, thread = live(work=Path(raw) / "work")
        try:
            base = origin(built)
            for tag in ("fr", "xx-YY", "zz"):
                status, _, body = request(f"{base}{api.API_PREFIX}/locales/{tag}")
                check(status == 404, f"/locales/{tag} answered {status}, not 404")
                payload = json.loads(body) if body.startswith(b"{") else {}
                code = payload.get("error", {}).get("code", "")
                check(code == "no_locale",
                      f"/locales/{tag} refused with {code!r}, not 'no_locale'")
                check("strings" not in payload,
                      f"/locales/{tag} answered with strings anyway")
            # And the same shape with a tag that exists, so the refusal is not
            # simply what this route always does.
            status, _, body = request(
                f"{base}{api.API_PREFIX}/locales/{i18n.DEFAULT_TAG}")
            check(status == 200, f"a known locale answered {status}")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


def test_config_names_the_locales_and_which_one_is_the_default() -> None:
    """A client that reads only `/config` still knows what it can ask for."""
    with tempfile.TemporaryDirectory() as raw:
        built, thread = live(work=Path(raw) / "work")
        try:
            status, _, body = request(f"{origin(built)}{api.API_PREFIX}/config")
            check(status == 200, f"/config answered {status}")
            block = json.loads(body).get("locales", {})
            check(block.get("default") == i18n.DEFAULT_TAG,
                  f"/config names {block.get('default')!r} as the default locale")
            listed = [entry["tag"] for entry in block.get("available", [])]
            check(sorted(listed) == sorted(i18n.available()),
                  f"/config lists {listed}, not {list(i18n.available())}")
            check(all("label" in entry for entry in block.get("available", [])),
                  "/config lists a locale with no label for the picker")
            check("strings" not in json.dumps(block),
                  "/config carries the catalogues themselves; one page load "
                  "would then fetch every translation to render one")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


def test_the_bare_route_negotiates_and_the_tagged_route_does_not() -> None:
    """`GET /locales` reads the header; `GET /locales/<tag>` overrides it.

    The second is the one an explicit, persisted choice asks for, and it has to
    win over the header -- a German speaker on an English-configured work
    laptop is the ordinary case, not the exotic one.
    """
    with tempfile.TemporaryDirectory() as raw:
        built, thread = live(work=Path(raw) / "work")
        try:
            base = origin(built)
            for header, wanted in ((GERMAN, "de"), (ENGLISH, "en")):
                _, _, body = request(f"{base}{api.API_PREFIX}/locales",
                                     headers={"Accept-Language": header})
                check(json.loads(body).get("tag") == wanted,
                      f"Accept-Language {header!r} was served "
                      f"{json.loads(body).get('tag')!r}")
            _, _, body = request(f"{base}{api.API_PREFIX}/locales/de",
                                 headers={"Accept-Language": ENGLISH})
            check(json.loads(body).get("tag") == "de",
                  "an explicit tag lost to the browser's Accept-Language")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


# --------------------------------------------------------------------------
# the records do not move
# --------------------------------------------------------------------------

def finished_run(base: str, language: str) -> str:
    """One merge, submitted under `language`, waited out. Returns its id.

    Submitted under `language`; **polled in English, always**. The poll is this
    harness finding out when to look, not part of what is being measured, and a
    defect that localised `state` itself would otherwise make this function
    wait out its deadline rather than fail -- a hang is a failure a test may
    not have, because the tool that runs it would sit on it.
    """
    status, _, body = request(f"{base}{api.API_PREFIX}/runs", method="POST",
                              payload={"documents": [
                                  {"name": "source_a.md", "text": SOURCE_A},
                                  {"name": "notes-b.md", "text": SOURCE_B}],
                                  "base": "source_a.md",
                                  "model": "test-model",
                                  "merge_model": "test-model"},
                              headers={"Accept-Language": language})
    if status != 202:
        return ""
    job_id = json.loads(body).get("id", "")
    deadline = time.time() + PATIENCE
    while time.time() < deadline:
        _, _, raw = request(f"{base}{api.API_PREFIX}/runs/{job_id}",
                            headers={"Accept-Language": ENGLISH})
        if json.loads(raw).get("state") in ("done", "failed"):
            return job_id
        time.sleep(0.1)
    return job_id


def settled(body: bytes) -> bytes:
    """One response with the retention countdown taken out of it, if it has one.

    Anything that is not a JSON object carrying `expires_in` comes back
    unchanged, so the two file routes are compared byte for byte exactly as
    they were before this existed. The caller checks that the run payload does
    carry one before handing it here.
    """
    try:
        payload = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return body
    if not isinstance(payload, dict) or "expires_in" not in payload:
        return body
    payload.pop("expires_in")
    return json.dumps(payload, sort_keys=True).encode("utf-8")


def test_a_recorded_artefact_does_not_change_with_the_browser_s_language() -> None:
    """One run, three artefacts, two `Accept-Language` headers, same bytes.

    This is the property the whole milestone is constrained by. `report.json`
    is read by scorers and by the paper; `merged.md` is the operator's own
    text; `report.html` is what gets sent to somebody else. A record whose
    language depends on which browser asked for it cannot be compared with one
    from another day, and its identifiers -- `silent_loss`, `contradicted`,
    the finding kinds -- stop being machine-readable the moment they are words
    in a language nobody recorded.

    The run is *submitted* in German too, not merely fetched in German, so that
    a server which resolved a language at submission time and baked it into the
    stored report would fail here rather than in six months.
    """
    with FakeEndpoint(Script(**CLEAN)) as endpoint, \
            tempfile.TemporaryDirectory() as raw:
        environ = {"LLOSSLESS_BASE_URL": endpoint,
                   "LLOSSLESS_STRUCTURED": "prompt"}
        built, thread = live(environ=environ, work=Path(raw) / "work")
        try:
            base = origin(built)
            job_id = finished_run(base, GERMAN)
            check(bool(job_id), "the German submission was not accepted")
            if not job_id:
                return
            paths = (f"{api.API_PREFIX}/runs/{job_id}",
                     f"{api.API_PREFIX}/runs/{job_id}/merged",
                     f"{api.API_PREFIX}/runs/{job_id}/report.html")
            for path in paths:
                status, _, german = request(base + path,
                                            headers={"Accept-Language": GERMAN})
                check(status == 200, f"{path} answered {status} in German")
                _, _, english = request(base + path,
                                        headers={"Accept-Language": ENGLISH})
                # `/runs/{id}` carries one field that is a live countdown --
                # `expires_in`, the seconds left before retention forgets the
                # run -- and two requests a moment apart differ in it whatever
                # language either asked in. It is dropped from both sides
                # rather than compared, and the comparison is still every other
                # byte of the payload including the whole report.
                if path.endswith(job_id):
                    # Asserted, not assumed: a `settled` that stopped finding
                    # the field would turn this into a comparison with nothing
                    # removed, which is the old check passing by accident.
                    check(b'"expires_in"' in german and b'"expires_in"' in english,
                          "the run payload must carry the retention countdown, "
                          "or the removal below is removing nothing")
                german, english = settled(german), settled(english)
                check(german == english,
                      f"{path} is {len(german)} bytes under a German "
                      f"Accept-Language and {len(english)} under an English "
                      f"one; a record that changes with the reader is not a "
                      f"record")

            # And no German reached any of them. The byte comparison above
            # would pass just as well if the server localised *both* copies,
            # so the words themselves are looked for.
            german_strings = raw_strings("de")
            markers = [german_strings[key] for key in
                       ("verdict.clean", "results.claims", "chip.notchecked",
                        "results.merged")]
            check(all(marker for marker in markers),
                  "the German markers this probe looks for are empty")
            for path in paths:
                _, _, body = request(base + path,
                                     headers={"Accept-Language": GERMAN})
                text = body.decode("utf-8", "replace")
                found = [marker for marker in markers if marker in text]
                check(not found,
                      f"{path} carries the German {found}; the artefacts are "
                      f"not localised and must not become so")

            # The must-fire pair. Two identical answers from a server that
            # ignores Accept-Language entirely would prove nothing, so the one
            # endpoint that *is* meant to vary with it is asked the same way.
            _, _, german = request(f"{base}{api.API_PREFIX}/locales",
                                   headers={"Accept-Language": GERMAN})
            _, _, english = request(f"{base}{api.API_PREFIX}/locales",
                                    headers={"Accept-Language": ENGLISH})
            check(german != english,
                  "the locale endpoint answers the same bytes to a German and "
                  "an English browser, so the comparison above is between two "
                  "requests this server cannot tell apart")
            served = (json.loads(german).get("tag"), json.loads(english).get("tag"))
            check(served == ("de", "en"),
                  f"the locale endpoint served {served} to a German and an "
                  f"English browser; it does not honour Accept-Language, so "
                  f"nothing above measured what it claims to")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


# --------------------------------------------------------------------------
# the header follows a language switch
# --------------------------------------------------------------------------

def header_hooks(html: str) -> set[str]:
    """The `data-cc` hooks inside the page's `<header>`."""
    start = html.index('<header class="topbar">')
    end = html.index("</header>", start)
    return set(re.findall(r'data-cc="([^"]+)"', html[start:end]))


def function_bodies(js: str) -> dict[str, str]:
    """Every top-level function in the script, by name, braces balanced."""
    js = strip_comments(js)
    bodies = {}
    for match in re.finditer(r"^(?:async )?function (\w+)\(", js, re.M):
        start, end = block(js, match.group(0))
        bodies[match.group(1)] = js[start:end]
    return bodies


def reachable_from(bodies: dict[str, str], root: str) -> set[str]:
    """The functions `root` calls, directly or through others."""
    seen, todo = set(), [root]
    while todo:
        name = todo.pop()
        if name in seen or name not in bodies:
            continue
        seen.add(name)
        for called in re.findall(r"\b(\w+)\(", bodies[name]):
            if called in bodies and called not in seen:
                todo.append(called)
    return seen


def header_locale_problems(html: str, js: str) -> list[str]:
    """Every function that writes catalogue text into a header hook must be
    reached from `changeLocale`, or that text stays in the old language after
    a switch. That is how "Angemeldet als" stayed on an English page: the one
    writer of the session line ran at sign-in and never again."""
    bodies = function_bodies(js)
    switch = reachable_from(bodies, "changeLocale")
    found = []
    for hook in sorted(header_hooks(html)):
        for name, body in sorted(bodies.items()):
            if name == "changeLocale" or f'el("{hook}")' not in body:
                continue
            if not re.search(r'\bt\(\s*"', body):
                continue
            if name not in switch:
                found.append(f"{name} writes catalogue text into the header's "
                             f"{hook} and is not re-run on a language switch")
    return found


def test_the_header_follows_a_language_switch() -> None:
    """The operator met "Angemeldet als ..." on an English page."""
    html, js = source(INDEX), source(APP_JS)
    hooks = header_hooks(html)
    check({"session-said", "status-pill-text"} <= hooks,
          f"the header's translated hooks have moved: {sorted(hooks)}")
    for problem in header_locale_problems(html, js):
        check(False, problem)
    # Must-fire: the call this fix added, taken back out.
    seeded = js.replace("  renderSession();\n  if (store.config) renderControls();",
                        "  if (store.config) renderControls();", 1)
    check(seeded != js, "the header-switch probe's anchor has moved")
    check(any("renderSession" in p for p in header_locale_problems(html, seeded)),
          "a session line that is never re-rendered on a switch is not caught")


# --------------------------------------------------------------------------
# the type check
# --------------------------------------------------------------------------

def test_the_type_check_fires_on_a_seeded_error() -> None:
    """`tsc` is a check here, not a formality, and this is the proof.

    `tests/test_web_static.py` runs the compiler over `app.js` and asserts zero
    errors. Nothing anywhere asserted that a real error would be *reported* --
    a wrong flag, a compiler that resolved to a stub, an invocation that
    silently type-checked nothing would all exit 0 over a file with a type
    error in it, and the green would mean nothing.

    The seed is aimed at the catalogue machinery on purpose: `strings` is the
    one value in the file whose type is carried by a JSDoc annotation rather
    than inferred from a literal, so indexing it wrongly is exactly the mistake
    `--checkJs` exists to catch and exactly the one a dropped annotation would
    stop catching.

    Declines rather than fails where there is no offline compiler, the same way
    its neighbour does: "there is no compiler here" is not the same answer as
    "the annotations are wrong".
    """
    compiler = a_compiler()
    if compiler is None:
        decline("UNMEASURED: no offline TypeScript compiler on this machine, so "
                "the seeded type error was not run past one. Set LLOSSLESS_TSC "
                "to one, or run `npx -p typescript tsc --noEmit --allowJs "
                "--checkJs --target es2022 src/llossless/web/static/app.js`.")
        return
    original = source(APP_JS)
    anchor = "function t(key, values) {\n  let text = strings[key];"
    check(anchor in original, "the probe's anchor has moved")
    if anchor not in original:
        return
    with tempfile.TemporaryDirectory() as raw:
        probe = Path(raw) / "app.js"
        probe.write_text(
            original.replace(anchor, anchor + "\n  const wrong = strings[key].nope;"),
            encoding="utf-8")
        try:
            # Capped. A compiler that hangs is a failure this check may not
            # have: `run_all.py` would sit on it for the rest of the suite.
            answer = subprocess.run(
                compiler + ["--noEmit", "--allowJs", "--checkJs", "--target",
                            "es2022", str(probe)],
                capture_output=True, timeout=300, cwd=ROOT)
        except (OSError, subprocess.SubprocessError) as problem:
            decline(f"UNMEASURED: the seeded type check could not be run: {problem}")
            return
    output = (answer.stdout + answer.stderr).decode("utf-8", "replace")
    check(answer.returncode != 0,
          "tsc exits 0 over a file with a type error in it; the invocation in "
          "test_web_static.py is checking nothing")
    check("nope" in output or "Property" in output,
          f"tsc failed without reporting the seeded error:\n{output.strip()[:400]}")


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# the access form's own table, inside the page
# --------------------------------------------------------------------------

# The form that asks for the server's access token is drawn before any
# catalogue can be fetched, so its words live in `ACCESS_STRINGS` in the
# script. The first six entries repeat catalogue keys; the others are for the
# form alone.
ACCESS_CATALOGUE_KEYS = {
    "heading": "auth.access.heading", "hint": "auth.access.hint",
    "label": "auth.access", "kept": "auth.access.kept",
    "submit": "auth.access.submit", "refused": "auth.access.refused",
}


def access_table(js: str) -> dict | None:
    """`ACCESS_STRINGS` as the shipped script builds it, run under node."""
    node = node_command()
    if node is None:
        return None
    program = (EFFORT_DOM + "\n" + js
               + "\nprocess.stdout.write(JSON.stringify(ACCESS_STRINGS));")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as handle:
        handle.write(program)
        path = handle.name
    try:
        run = subprocess.run(node + [path], capture_output=True, text=True,
                             timeout=120, cwd=ROOT)
    finally:
        Path(path).unlink()
    return json.loads(run.stdout) if run.returncode == 0 else {"error": run.stderr[-300:]}


def access_table_problems(table: dict, tables: dict) -> list[str]:
    """Same keys in both languages, none empty, same placeholders, and the
    repeated entries equal to the catalogue's own strings."""
    if "error" in table:
        return [f"ACCESS_STRINGS did not load: {table['error']}"]
    holes = re.compile(r"\{[a-z_]+\}")
    found = []
    if sorted(table) != sorted(tables):
        found.append(f"languages {sorted(table)} are not the catalogues' {sorted(tables)}")
        return found
    reference = table["en"]
    for tag, entries in sorted(table.items()):
        if sorted(entries) != sorted(reference):
            found.append(f"{tag}: keys differ from en by "
                         f"{sorted(set(entries) ^ set(reference))}")
            continue
        for key, text in entries.items():
            if not text.strip():
                found.append(f"{tag}.{key} is empty")
            if sorted(holes.findall(text)) != sorted(holes.findall(reference[key])):
                found.append(f"{tag}.{key}: placeholders differ from en")
            if "<" in text or ">" in text:
                found.append(f"{tag}.{key} contains markup")
        for key, catalogue_key in ACCESS_CATALOGUE_KEYS.items():
            if entries.get(key) != tables[tag].get(catalogue_key):
                found.append(f"{tag}.{key} no longer says what {catalogue_key} says")
    return found


def test_the_access_form_has_the_same_words_in_both_languages() -> None:
    """The built-in table for the token form cannot drift from the catalogues or itself.

    MUST FIRE: a key missing in German, an empty string, a placeholder that
    differs, a copy that no longer matches the catalogue, and a language the
    catalogues lack.
    """
    js = source(APP_JS)
    tables = catalogues()
    table = access_table(js)
    if table is None:
        decline("UNMEASURED: no node here, so the access form's table was not read")
        return
    check(not access_table_problems(table, tables),
          f"access table: {access_table_problems(table, tables)}")
    import copy
    mutations = {
        "a missing German key": lambda t: t["de"].pop("empty"),
        "an empty string": lambda t: t["de"].update(unsendable=" "),
        "a placeholder only in German": lambda t: t["de"].update(empty="Geben Sie {n} ein."),
        "a copy that drifted": lambda t: t["en"].update(refused="Refused."),
        "a language the catalogues lack": lambda t: t.update(fr=copy.deepcopy(t["en"])),
    }
    for name, mutate in mutations.items():
        broken = copy.deepcopy(table)
        mutate(broken)
        check(bool(access_table_problems(broken, tables)),
              f"the access table check did not fire on {name}")
    check(table["en"]["empty"] != table["de"]["empty"],
          "the two languages of the access form say the same thing")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_i18n" and callable(function):
            function()
    for line in unmeasured:
        print(line)
    if failures:
        print(f"web i18n: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web i18n: {checks} checks pass"
          + (f", {len(unmeasured)} declined" if unmeasured else ""))
    return 3 if unmeasured else 0


def test_web_i18n() -> None:
    """pytest entry point."""
    assert main() in (0, 3), "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
