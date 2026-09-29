"""locales/*.json: every word the web interface says, in one file per language.

The page used to carry its own strings table inside `static/app.js`. That was
always the precondition for this module rather than a rival to it -- a sentence
built at a call site is a sentence no translator will ever see -- and the table
is now `locales/en.json`, byte for byte the same words, loaded over the wire
instead of shipped inside the script. What this module adds is the second file
and the check that the two agree.

**A catalogue is refused whole, never patched with English.** The obvious
design is a lookup that falls back to the reference language for a key the
chosen language does not carry. It is the wrong one here: a half-translated
page *looks translated*, so the operator reads the English sentences as
deliberate -- as terms of art left in English on purpose -- rather than as the
gap they are. Nobody files that. `validate()` therefore fails on a missing key
**and** on an orphan key, the server refuses to serve a catalogue that does not
validate, and the page either speaks one language throughout or says so.

**The reference is `en.json` and every other file is measured against it.**
Not against a schema written out here: the set of strings the page renders
changes whenever the page changes, and a hand-maintained list of keys is the
thing that goes stale first. The reference file is the list, which is why the
check runs in both directions -- a key added to `en.json` and not to `de.json`
is a missing translation, and a key left in `de.json` after `en.json` dropped
it is a line somebody will translate again the next time it is edited.

**Placeholders are part of the string, so they are part of the check.**
`{n} of {max} documents` carries two values the renderer will substitute, and a
translation that spells one of them `{maximum}` renders the brace and the word
to the operator. That is a defect with no symptom anywhere else: the page
loads, the layout is right, and one sentence has `{max}` in the middle of it.
The sets have to match; the order does not, because German moves them.

**No value may contain markup.** `static/app.js` puts every string on the page
through one `.textContent =` assignment and `tests/test_web_static.py` counts
that assignment to keep it at one. A catalogue is the one input to that funnel
that arrives as data rather than as code, so the rule is restated here as a
property of the data: a `<` or a `>` in a value would either render as literal
text -- which is the good case, and still wrong -- or tempt the next person to
reach for `innerHTML` to make a `<br>` work. Neither is worth a line break.

**The recorded artefacts are not localised and this module is not consulted
about them.** `report.json`, `merged.md` and `report.html` are records. A
record whose language depends on which browser asked for it is not
reproducible, cannot be compared with a record from another day, and would
make `report.json`'s machine-readable identifiers -- `silent_loss`,
`contradicted`, the finding kinds -- ambiguous in exactly the places
`tests/` and the paper read them. Only the *display* of a kind is translated,
under `kind.<identifier>` in the catalogues, and the identifier itself never
moves.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# The catalogues ship beside this module as package data, the same way
# `catalogue.json` does and for the same reason: they are data about the tool,
# distributed with it. A fork translating into a third language adds a file
# here; nothing goes looking in the operator's working directory, because a
# locale picked up from the current directory is a locale whose provenance
# nobody can state.
LOCALES_DIR = Path(__file__).resolve().parent / "locales"

# The language every other file is measured against, and the answer when
# nothing the browser asked for is available. English rather than "whichever
# file sorts first": the reference has to be the one the page's own markup
# carries as its `data-t` fallback text, or a page served with the script
# blocked would read in one language and the catalogue in another.
DEFAULT_TAG = "en"

# What a tag may be, as a filename and as a URL segment. Deliberately narrower
# than RFC 5646 -- this is the set of names that can be a filename in
# `locales/` without any escaping question arising -- and anchored with
# `\A`/`\Z` rather than `^`/`$`, because `$` also matches before a trailing
# newline and `de\n/../../etc/passwd` is a thing a URL can carry once
# percent-decoding has run. That is not hypothetical; it is the standard way
# this exact validation is defeated.
TAG = re.compile(r"\A[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*\Z")

# `{name}` as `t()` in `app.js` substitutes it. Lowercase and underscores only,
# which is every placeholder the catalogues use; a brace around anything else
# is prose about braces and not a substitution, and reporting it as one would
# make the parity check fire on a sentence nobody can fix.
PLACEHOLDER = re.compile(r"\{([a-z_]+)\}")

# The three keys a catalogue file carries at the top level. `label` is the
# language's name *in that language* -- "Deutsch", not "German" -- because it
# is rendered in a picker whose whole job is to be legible to somebody who
# cannot currently read the page.
REQUIRED_FIELDS = ("tag", "label", "strings")

# What a value may not contain. Not an escaping mechanism and not a substitute
# for one: `app.js` escapes by construction and this is the assertion that it
# never has to. See the module docstring.
MARKUP = ("<", ">")


class InvalidLocale(ValueError):
    """A catalogue failed validation and nothing here trusted any of it.

    Raised rather than logged, and the file is rejected whole rather than the
    bad key skipped, for the reason the module docstring gives at length: a
    catalogue that silently loses half its strings to an English fallback is a
    page that looks translated and is not. A raise reaches an operator; a
    fallback reaches nobody.
    """


def paths(directory: Path | None = None) -> dict[str, Path]:
    """Every catalogue file on disk, keyed by the tag its filename claims.

    The filename is the tag and the tag inside the file has to agree with it
    (`validate` asserts that). Two spellings of one fact, on purpose: the
    filename is what a URL segment is matched against, so it has to be
    authoritative, and the field inside is what a reader sees when the file is
    open in front of them with no path in view.
    """
    root = Path(directory) if directory is not None else LOCALES_DIR
    found = {}
    for path in sorted(root.glob("*.json")):
        tag = path.stem
        if TAG.match(tag):
            found[tag] = path
    return found


def available(directory: Path | None = None) -> tuple[str, ...]:
    """The tags this server can serve, `DEFAULT_TAG` first and the rest sorted.

    Ordered rather than a set because it is rendered as a picker, and a picker
    whose options move between page loads is a picker the operator clicks the
    wrong row of. The reference language leads because it is the fallback: a
    list whose first entry is not the one an unknown `Accept-Language` gets
    would misdescribe the server's own behaviour.
    """
    tags = set(paths(directory))
    rest = sorted(tags - {DEFAULT_TAG})
    return tuple(([DEFAULT_TAG] if DEFAULT_TAG in tags else []) + rest)


def read(tag: str, directory: Path | None = None) -> dict:
    """One catalogue off disk, parsed and not yet checked against anything.

    Separate from `load` so that `validate` has something to be handed. A
    caller outside this module wants `load`, which is this plus the checks;
    this exists so the checks can be run over a file that is *about* to be
    installed rather than only over one that already is.
    """
    known = paths(directory)
    if tag not in known:
        raise InvalidLocale(f"there is no catalogue for {tag!r}; this server "
                            f"has {', '.join(available(directory)) or 'none'}")
    try:
        data = json.loads(known[tag].read_text(encoding="utf-8"))
    except (OSError, ValueError) as problem:
        raise InvalidLocale(f"{tag}.json could not be read: {problem}") from None
    if not isinstance(data, dict):
        raise InvalidLocale(f"{tag}.json is a {type(data).__name__}, not an object")
    return data


def validate(tag: str, data: dict, reference: dict | None = None) -> None:
    """Raise `InvalidLocale` if `data` cannot be served as the catalogue for `tag`.

    `reference` is the reference language's `strings` map, and is the only
    thing that can answer the two questions that matter -- is a string missing,
    and is a string left over. Passed in rather than read here so that
    validating the reference against itself is the same code path as validating
    a translation against it, which is what keeps the reference honest: a
    malformed `en.json` would otherwise be the one file nothing checks.
    """
    for field in REQUIRED_FIELDS:
        if field not in data:
            raise InvalidLocale(f"{tag}.json has no {field!r}")
    if data["tag"] != tag:
        raise InvalidLocale(f"{tag}.json calls itself {data['tag']!r}; the "
                            f"filename is the tag a URL is matched against, so "
                            f"the two cannot differ")
    if not isinstance(data["label"], str) or not data["label"].strip():
        raise InvalidLocale(f"{tag}.json has no label to put in the picker")
    strings = data["strings"]
    if not isinstance(strings, dict) or not strings:
        raise InvalidLocale(f"{tag}.json carries no strings")

    for key, value in sorted(strings.items()):
        if not isinstance(key, str) or not isinstance(value, str):
            raise InvalidLocale(f"{tag}.json maps {key!r} to a "
                                f"{type(value).__name__}; a catalogue is flat "
                                f"and every value is a string")
        found = [mark for mark in MARKUP if mark in value]
        if found:
            raise InvalidLocale(
                f"{tag}.json's {key!r} contains {found[0]!r}. Every string on "
                f"the page goes through one textContent assignment, so markup "
                f"here renders as literal text at best and invites an "
                f"innerHTML at worst")

    if reference is None:
        return
    missing = sorted(set(reference) - set(strings))
    if missing:
        raise InvalidLocale(
            f"{tag}.json is missing {len(missing)} string(s) the reference "
            f"has: {', '.join(missing[:8])}"
            + (" ..." if len(missing) > 8 else "")
            + ". A catalogue is served whole or not at all; there is no "
              "fallback to English for the ones it does have")
    orphans = sorted(set(strings) - set(reference))
    if orphans:
        raise InvalidLocale(
            f"{tag}.json carries {len(orphans)} string(s) the reference does "
            f"not: {', '.join(orphans[:8])}"
            + (" ..." if len(orphans) > 8 else "")
            + ". Nothing renders them, so they are work that will be done "
              "again the next time the key they were named after is edited")
    for key in sorted(reference):
        wanted = set(PLACEHOLDER.findall(reference[key]))
        got = set(PLACEHOLDER.findall(strings[key]))
        if wanted != got:
            raise InvalidLocale(
                f"{tag}.json's {key!r} substitutes {sorted(got)} where the "
                f"reference substitutes {sorted(wanted)}. A placeholder the "
                f"renderer does not recognise is rendered to the operator, "
                f"braces and all")


def reference_strings(directory: Path | None = None) -> dict[str, str]:
    """The reference language's strings, read and shape-checked but not compared.

    Its own validation pass runs with `reference=None`, which is the one call
    in this module that is allowed to skip the parity check -- there is nothing
    above it to be compared with. Everything else in this module goes through
    `load`.
    """
    data = read(DEFAULT_TAG, directory)
    validate(DEFAULT_TAG, data, None)
    return data["strings"]


def load(tag: str, directory: Path | None = None) -> dict:
    """One validated catalogue, ready to serve. Raises `InvalidLocale`.

    Read from disk on every call rather than cached, the same way
    `catalogue.load` is. A page load asks for one file of about 20 kB and the
    operator running this server is frequently the person editing that file;
    a cache would mean a translation fix needs a restart to be visible, and
    the failure that produces -- "I changed it and nothing happened" -- costs
    more than the read.
    """
    data = read(tag, directory)
    validate(tag, data, None if tag == DEFAULT_TAG
             else reference_strings(directory))
    return data


def describe(directory: Path | None = None) -> list[dict]:
    """What a picker needs to list the locales, without fetching any of them.

    Label only, never the strings: this goes into `/config`, which a page reads
    before it knows which language it wants, and serving every catalogue there
    would make a page load carry every translation this server has in order to
    render one of them.
    """
    listed = []
    for tag in available(directory):
        try:
            data = load(tag, directory)
        except InvalidLocale:
            # A file that does not validate is not offered. The picker is a
            # promise that the option works; an entry that 409s when chosen is
            # worse than an option that was never there, because the operator
            # cannot tell it from a network fault.
            continue
        listed.append({"tag": tag, "label": data["label"],
                       "default": tag == DEFAULT_TAG})
    return listed


def preferences(accept_language: str) -> list[str]:
    """`Accept-Language` as tags in the order the browser asked for them.

    Lowercased, `q=0` dropped -- which the RFC defines as "not acceptable", so
    an entry with it is a refusal and not a weak preference -- and a malformed
    `q` drops its entry rather than defaulting to 1.0. That last one is a
    choice: a header this function cannot parse is a header this function
    should not be ranking, and treating an unreadable weight as the strongest
    possible one would let a garbled header outrank a well-formed entry beside
    it.

    Sorted by weight only. Python's sort is stable, so entries of equal weight
    keep the order the browser wrote them in, which is the order the browser
    meant.
    """
    ranked: list[tuple[float, str]] = []
    for entry in accept_language.split(","):
        parts = [part.strip() for part in entry.split(";") if part.strip()]
        if not parts:
            continue
        tag = parts[0].lower()
        weight = 1.0
        broken = False
        for parameter in parts[1:]:
            name, _, value = parameter.partition("=")
            if name.strip().lower() != "q":
                continue
            try:
                weight = float(value)
            except ValueError:
                broken = True
        if broken or weight <= 0:
            continue
        ranked.append((weight, tag))
    order = sorted(range(len(ranked)), key=lambda i: -ranked[i][0])
    return [ranked[i][1] for i in order]


def negotiate(accept_language: str, directory: Path | None = None) -> str:
    """Which catalogue to serve a browser that has not been told otherwise.

    Two passes over the browser's list rather than one, and the order is the
    point. An exact match is taken wherever it appears in the list, then and
    only then is a primary-subtag match considered: a browser asking for
    `de-CH, en, de` prefers Swiss German to English, and a single pass that
    accepted `de` for `de-CH` on the first entry would hand it German before
    it had looked at `en` -- which is the same answer here, but would not be
    on a server that had a `de-CH` file.

    `*` is not honoured as a match. It means "anything", and the answer to
    "anything" is already the default this function returns when nothing
    matched, so treating it as a hit would only change which file "anything"
    resolved to depending on where in the list it appeared.

    Never raises and never returns a tag this server cannot serve. This is
    called to pick a default for somebody who expressed no preference, and a
    failure to negotiate is not an error condition -- it is English.
    """
    wanted = preferences(accept_language or "")
    known = available(directory)
    lowered = {tag.lower(): tag for tag in known}
    for tag in wanted:
        if tag in lowered:
            return lowered[tag]
    for tag in wanted:
        primary = tag.split("-")[0]
        if primary in lowered:
            return lowered[primary]
    return DEFAULT_TAG if DEFAULT_TAG in known else (known[0] if known
                                                     else DEFAULT_TAG)
