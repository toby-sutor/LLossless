"""catalogue.json: what the web UI's model picker is allowed to say about a model.

A picker choosing between models for the operator needs to answer three
questions before the operator commits a document to one: what will this cost,
how long will it take, and how much silent loss did it produce the last time
anyone actually ran it. Those are exactly the numbers this project already
computes for every recorded run -- `tests/rank_matrix.py` and its siblings
compute them from `reconcile.reconcile()` over a reference merge -- so this
module does not compute anything new. It reads a small JSON file that someone
copied those numbers into by hand, checks the file's own internal consistency,
and hands the result to whatever renders the picker.

**Every number in `measured` traces to a named run, not a path on someone's
disk.** The `run`, `artefacts` and `derived_by` fields are not decoration:
they are how a reader six months from now tells a measurement from a guess
that has been sitting in a JSON file long enough to look authoritative.
`run` names the recorded run the figures came from (a directory name, not a
filesystem path -- this file ships outside the machine that produced the
numbers, and a `/home/...` path in it would be unopenable by any reader who
is not that same machine); `artefacts` lists which files in that run were
read; `derived_by` names the script that did the reading, or -- when no
script in this repository covers that row's schema -- says so plainly and
describes what was run by hand instead. This project has a name for the
failure this prevents -- a figure that reads as derived and was actually
typed in, or averaged across two runs that used different corpora without
saying so, or a self-hosted model quietly reported as free because nobody
priced its GPU time. `validate()` below only catches the shape of that
mistake (a measured block with no `run`/`artefacts`/`derived_by`), not the
content of it (a run that does not actually contain the number); nothing
short of re-running `derived_by` against `run`/`artefacts` and checking does
that, and the loader cannot do it at import time without turning every page
load into a filesystem audit that would not even resolve, since `run` is
deliberately not a path. That check belongs to whoever adds a row, once,
before it lands here.

**Unmeasured models are `"measured": null`, never an estimate.** A model
nobody has run through this tool has no basis for a cost or a deviation
count, and interpolating one from a vendor's price sheet or from a
similarly-sized model that was actually measured would dress up a guess as a
figure with the same shape as the real ones. The picker has to render the
null case anyway -- there is no world where every model a user might want is
already benchmarked -- so it is a first-class state here rather than a gap
papered over with a plausible-looking number.

**Self-hosted models never get a real `usd_per_merge`.** A metered
serverless GPU endpoint bills per minute of wall-clock GPU time, not
per token, so there is no per-merge dollar figure to attribute without
assuming a utilisation rate this module has no way to know. The field is
`null` and `notes` says why, rather than the field being silently omitted or
filled with 0 -- 0 reads as "measured and free", which is the exact inversion
a cost comparison must not make against the models that do carry a real
figure.

**`id` is a display key and `api_model` is the wire name, and they are two
fields because they are two different strings.** `id` is what this catalogue
calls a row, what a URL fragment or a saved preference can hold, and what a
reader recognises; `api_model` is the exact string that goes into
`LLOSSLESS_MODEL` and out onto the wire, and an endpoint matches it byte for
byte. They were one field until a picker sent `claude-haiku-4-5` to a vendor
that only answers to `claude-haiku-4-5-20251001`, and `qwen3-8b` to an endpoint
whose model is `qwen/qwen3-8b`. Both failed two steps into a run, after the
documents had been uploaded and a worker had started, with a message about a
model nobody had typed. `validate()` requires `api_model` on every entry and
requires it unique, because the reverse lookup -- which provider serves the
model this request named -- is what decides where the request is sent, and two
rows claiming one wire name would make that lookup pick one arbitrarily.

Every `api_model` here is read off a recorded run's own `provenance.models`,
which is the string `Settings.model_for` handed the transport, not a string
anybody retyped from a vendor's documentation.

**`profile` is checked against `structured.PROFILES`, not a copy of it.**
`structured.py` already carries the registered request-shape names and the
reasons each one exists; a second list of valid profiles maintained here
would be exactly the kind of table that goes stale the first time the real
one gains a row. Importing it is the whole of the check.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# The one import this module makes from its own package, for the same reason
# `config.py` imports `structured.PROFILES` rather than restating it: the
# profile names are registered in exactly one place, and a catalogue entry
# claiming a profile that table does not recognise is a data-entry mistake
# this loader can catch for free by asking the table itself.
from ..structured import PROFILES

# The second, for the same reason: the depth names are registered once, in
# `config.VERIFY_DEPTHS`, and a `verify_depth` block measuring a depth this
# build does not have is a block written against a different tool.
from ..config import VERIFY_DEPTHS

# And the levels a merge can be asked for (`config.EFFORT_LEVELS`, read off the
# installed CLI's own help), so a per-effort block cannot publish figures for a
# level no route can be asked to run at.
from ..config import EFFORT_LEVELS

# And the third: a command route id is spelled the way `commands.ROUTE_ID`
# allows, since a figure for an id no route can carry is a figure for nothing.
from .commands import ROUTE_ID

# The catalogue ships beside this module as package data, not in the
# operator's working directory: it is data about the
# tool, distributed with it, the same way `tests/pairs/*/ideal.json` travels
# with the tests that read it. A caller that wants a different file --
# a fork's own measurements, or a file assembled for a one-off comparison --
# passes `path` explicitly; nothing here goes looking anywhere else.
DEFAULT_PATH = Path(__file__).resolve().parent / "catalogue.json"

# Schema versions this loader understands. A tuple rather than a single int so
# that a future, backward-compatible addition (a new optional field, say) can
# be recognised without every existing catalogue.json needing to be rewritten
# to claim a version its shape hasn't actually earned yet.
SUPPORTED_SCHEMA_VERSIONS = (1,)

# The fields a `measured` block cannot be without. Everything else in the
# block is a number; these are what make the numbers checkable by anyone
# other than whoever typed them in. `run` is a name, not a path -- see the
# module docstring for why `source` (a single absolute filesystem path) was
# replaced with `run`/`artefacts`/`derived_by`.
REQUIRED_MEASURED_FIELDS = ("run", "artefacts", "derived_by", "measured_on")
BILLED_VALUES = ("free-tier",)

# The two figures that are a rate rather than a count, each with the raw count
# and the denominator it is formed from. Rows in this catalogue were measured
# over different numbers of pairs -- nine for the vendor models, two and three
# for the self-hosted ones -- so the raw counts do not compare and the rates
# are what any ranking must read.
#
# Nothing checked this arithmetic until 2026-09-19. `deviations_per_pair` had
# been published and consumed for a day with no rule that it equal
# `deviations / pairs`; the suite asserted only that the *renderer* reads the
# rate, which is a different claim entirely. A wrong rate here would have
# ranked models against each other and been believed.
RATE_FIELDS = (("deviations_per_pair", "deviations"),
               ("silent_loss_per_pair", "silent_loss"))

# The published rates are rounded to two decimals, so exact equality is the
# wrong test and would fail on 35/3. Half of the last retained place, with room
# for binary float representation.
RATE_TOLERANCE = 0.006

# --- the `verify_depth` block ------------------------------------------------
#
# What the cheaper verification depth costs in detection, measured over the
# seeded-defect fixtures. It is not a model row, so it sits beside
# `models` rather than in it, and it has rules of its own.
#
# **The two probe directions are never blended.** A `source_to_merged` probe
# asks whether a source's content survived; a `merged_to_sources` probe asks
# whether the merge says something its sources do not. The two have different
# denominators, and at a depth with no reverse pass the second is a different
# question entirely. So every figure lives under one direction, and a depth
# entry may carry nothing else numeric beside them but its cost.
VERIFY_DEPTH_DIRECTIONS = ("source_to_merged", "merged_to_sources")

# What a depth entry may hold. A key outside this set is refused rather than
# ignored: a rate at the depth level is a blend of the two directions, which
# is the one figure this block exists not to publish.
VERIFY_DEPTH_ENTRY_FIELDS = ("value", *VERIFY_DEPTH_DIRECTIONS, "cannot_detect",
                             "model_calls", "seconds", "speedup")

# Each rate with its count and its denominator, the `RATE_FIELDS` rule
# applied per direction. A denominator of zero is a rate over nothing, which is
# null and never 0.0: `coverage` grades no merged-side guard probe at all, and
# a 0.0 there would read as "never wrong" about probes it never reached.
VERIFY_DEPTH_RATE_FIELDS = (("plants_detected_rate", "plants_detected", "plants"),
                            ("guards_wrong_rate", "guards_wrong", "guards_graded"))
VERIFY_DEPTH_DIRECTION_FIELDS = ("plants", "plants_detected", "plants_detected_rate",
                                 "plants_detected_mechanically", "guards",
                                 "guards_graded", "guards_wrong", "guards_wrong_rate")

# --- a command route's `measured_by_effort` block ---------------------------
#
# What the merge did at each merge effort level, from one registered grid:
# per level, per pair, the planted errors fixed as a median and range
# over the draws, the whole run's seconds the same way, the licence on the pair
# that carries one, and how many runs searched. The page's effort slider reads
# one level at a time.
#
# **A level nobody ran is absent from `levels`, never zero and never null.**
# Haiku ran at `medium` only; a `low` entry of zeros would read as "measured,
# and fixed nothing", which is the inversion the page's "not measured at this
# level" exists to prevent.
EFFORT_LEVEL_FIELDS = ("pairs", "runs", "searched", "searched_rate", "api_equivalent_usd",
                       "uncached_list_usd")
# Optional on a level: the CLI envelope's own `total_cost_usd` per run,
# summed over the run's calls, as a median and range. **Not a price.** A
# subscription bills no call, which is why a command route's `usd_per_merge`
# stays null; this is what the same tokens would have cost through the API, the
# one usage figure the envelope reports. The page never shows it as money, only
# as a ratio between two levels of one block ("about 2x the usage").
EFFORT_USAGE_FIELD = "api_equivalent_usd"
# Beside it, never alone: the same tokens at the API's
# uncached list price. The envelope's figure bills the CLI's own cache writes
# at 1.25x or 2x the input rate, which an API row never pays, so it is not the
# same unit as an API row's list price; this one is. Also not a price.
EFFORT_UNCACHED_FIELD = "uncached_list_usd"
# A route's figures for a model its program was pinned to by full id rather
# than by the route's own alias: `pinned_by_effort`, a list of blocks
# held to `validate_effort_block`, each naming the id it asked for.
PINNED_FIELDS = ("requested_model", "resolved_model")
# What a route's alias answers as now, when that is no longer the model its
# figures were measured on: `{model, checked_on, cli_version}`. The page
# then labels the route's own figures as history and shows the pinned block
# for that model first. A check, dated, of one call -- not a measurement.
ALIAS_NOW_FIELDS = ("model", "checked_on", "cli_version")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_SEMVER = re.compile(r"\d+\.\d+\.\d+")
EFFORT_PAIR_FIELDS = ("planted", "draws", "fixed", "seconds",
                      "licence_fixed", "licence_fixed_rate")
EFFORT_SPREAD_FIELDS = ("median", "min", "max")


class InvalidCatalogue(ValueError):
    """catalogue.json failed validation and nothing here trusted any of it.

    Raised rather than logged, and the whole file is rejected rather than the
    one bad entry skipped: a picker that silently drops one row on a load
    error just shows a shorter list, and an operator comparing a shortened
    list to what they remember seeing has no way to tell "this model was
    removed" from "this model's entry broke and nobody said so." A raise
    stops the page from rendering a plausible-looking but incomplete picker
    and instead surfaces the one line that says what to go fix.
    """


def validate(data: dict) -> None:
    """Raise `InvalidCatalogue` if `data` cannot be trusted as a catalogue.

    Checks exactly four things, each because a wrong answer to it would let a
    number through that nobody could stand behind:

      unknown `schema_version`  a file this loader has never seen the shape
                                 of. Refusing it beats guessing at fields a
                                 newer or older schema might not have.
      duplicate `id`            two entries for one model id means `for_id`
                                 would have to pick one arbitrarily, silently
                                 discarding whichever measurement it did not
                                 pick.
      unregistered `profile`    a request shape this build of the tool does
                                 not know how to send, which means the entry
                                 was written against a different version of
                                 `structured.py`, or against a typo.
      missing/duplicate
      `api_model`               the string that goes on the wire. Absent, the
                                 renderer would have to fall back to `id`,
                                 which is a display key and is not what any
                                 endpoint answers to; duplicated, the reverse
                                 lookup that decides which provider's endpoint
                                 a request is sent to has two answers and
                                 would take one of them silently.
      an incomplete `measured`  a measured block missing `run`, `artefacts`,
                                 `derived_by` or `measured_on` is a number
                                 with no way to check it, which this project
                                 treats as indistinguishable from a number
                                 nobody measured.

    Also checks that `artefacts`, when present, is a non-empty list -- a
    string typed where a list was meant would otherwise pass the truthy
    check above silently -- and, when the file carries a `verify_depth` or a
    `command_routes` block, everything `validate_verify_depth` or
    `validate_command_routes` checks.

    Deliberately does **not** check that `run`/`artefacts` exist on disk or
    that they contain the attributed figure. Both of those are true facts
    about the world outside this file that would make `load()` do
    filesystem-shaped work on every call, for a guarantee a caller loading
    the catalogue to render a picker does not need at that moment -- and
    `run` is a name, not a path, so there is no location to even check
    without a caller supplying one. That check belongs to whoever adds or
    edits a row, run once against the artefact they are citing, not to
    every page load thereafter.
    """
    if not isinstance(data, dict):
        raise InvalidCatalogue(
            f"catalogue must be a JSON object at the top level, got {type(data).__name__}"
        )

    version = data.get("schema_version")
    if version not in SUPPORTED_SCHEMA_VERSIONS:
        raise InvalidCatalogue(
            f"unknown catalogue schema_version {version!r}; this loader "
            f"understands {', '.join(str(v) for v in SUPPORTED_SCHEMA_VERSIONS)}"
        )

    entries = data.get("models")
    if not isinstance(entries, list):
        raise InvalidCatalogue("catalogue has no 'models' list")

    seen_ids: set[str] = set()
    seen_wire: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise InvalidCatalogue(f"a model entry is not an object: {entry!r}")

        model_id = entry.get("id")
        if not model_id:
            raise InvalidCatalogue(f"a model entry has no 'id': {entry!r}")
        if model_id in seen_ids:
            raise InvalidCatalogue(
                f"duplicate model id {model_id!r} in catalogue.json -- "
                f"for_id() cannot serve two measurements from one id"
            )
        seen_ids.add(model_id)

        wire = entry.get("api_model")
        if not isinstance(wire, str) or not wire.strip():
            raise InvalidCatalogue(
                f"{model_id}: no 'api_model'. That is the string the endpoint "
                f"is asked for, and it is required separately from 'id' "
                f"because the two are not always the same string -- an id is "
                f"what this catalogue calls a row, and a wire name is what a "
                f"vendor answers to. Falling back to the id is what sent "
                f"'claude-haiku-4-5' to an endpoint that only knows "
                f"'claude-haiku-4-5-20251001'"
            )
        if wire != wire.strip() or any(c in wire for c in "\r\n\t"):
            raise InvalidCatalogue(
                f"{model_id}: api_model {wire!r} carries surrounding "
                f"whitespace or a control character. It is sent verbatim and "
                f"matched byte for byte, so a stray space is a model the "
                f"endpoint does not have"
            )
        if wire in seen_wire:
            raise InvalidCatalogue(
                f"{model_id}: api_model {wire!r} is claimed by another entry "
                f"as well. The wire name is how a submitted request is traced "
                f"back to the provider whose endpoint it must be sent to, and "
                f"two rows claiming one name make that lookup arbitrary"
            )
        seen_wire.add(wire)

        profile = entry.get("profile")
        if profile not in PROFILES:
            raise InvalidCatalogue(
                f"{model_id}: unknown profile {profile!r}; the registered "
                f"profiles are {', '.join(sorted(PROFILES))} (see "
                f"structured.PROFILES)"
            )

        validate_measured(model_id, entry.get("measured"))
        validate_retired(model_id, entry.get("retired"))

    # A retired row's successor, when it names one, must be a row here that is
    # not retired itself: the page tells a reader to use it instead.
    for entry in entries:
        successor = (entry.get("retired") or {}).get("replaced_by")
        if successor is None:
            continue
        target = next((e for e in entries if e.get("id") == successor), None)
        if target is None or target is entry or target.get("retired"):
            raise InvalidCatalogue(
                f"{entry['id']}.retired.replaced_by is {successor!r}, which is not a "
                f"live row in this catalogue")

    # Absent, or null, is the unmeasured state and is not an error: the page
    # says "unmeasured" for it. Present, it is checked as hard as a model row.
    if data.get("verify_depth") is not None:
        validate_verify_depth(data["verify_depth"])
    if data.get("command_routes") is not None:
        validate_command_routes(data["command_routes"])


def validate_measured(where: str, measured) -> None:
    """One `measured` block, for a model row or a command route: null, or checked.

    Attribution first -- `run`, `artefacts`, `derived_by`, `measured_on` -- and
    then every rate against its own count over `pairs`.
    """
    if measured is None:
        return
    if not isinstance(measured, dict):
        raise InvalidCatalogue(
            f"{where}: 'measured' must be an object or null, got "
            f"{type(measured).__name__}"
        )
    missing = [field for field in REQUIRED_MEASURED_FIELDS if not measured.get(field)]
    if missing:
        raise InvalidCatalogue(
            f"{where}: measured block is missing {', '.join(missing)}; "
            f"a figure with no run, artefacts and derived_by to check it "
            f"against is not a measurement here, it is an unattributed claim"
        )
    artefacts = measured.get("artefacts")
    if artefacts is not None and not isinstance(artefacts, list):
        raise InvalidCatalogue(
            f"{where}: measured.artefacts must be a list of filenames, "
            f"got {type(artefacts).__name__}"
        )

    # `billed` says how the run's calls were paid for, when that is not "at
    # the price on record". One value exists: `free-tier`, a vendor's free
    # tier, billed $0.00. Its dollar figure must be null -- a zero would
    # read as "measured, and free", which is the inversion `pricing.py`
    # refuses -- and the page shows a word for it instead of "unmeasured".
    billed = measured.get("billed")
    if billed is not None:
        if billed not in BILLED_VALUES:
            raise InvalidCatalogue(f"{where}: measured.billed is {billed!r}; the values are "
                                   f"{', '.join(BILLED_VALUES)}")
        if measured.get("usd_per_merge") is not None:
            raise InvalidCatalogue(f"{where}: measured.billed is {billed!r} and "
                                   f"usd_per_merge is {measured['usd_per_merge']!r}; a run "
                                   f"nobody was billed for carries no dollar figure")

    pairs = measured.get("pairs")
    for rate_field, count_field in RATE_FIELDS:
        rate, count = measured.get(rate_field), measured.get(count_field)
        if rate is None and count is None:
            continue
        if rate is None or count is None or not pairs:
            raise InvalidCatalogue(
                f"{where}: {rate_field} and {count_field} travel together "
                f"with pairs, and one of the three is missing "
                f"({rate_field}={rate!r}, {count_field}={count!r}, "
                f"pairs={pairs!r}); a rate with no denominator on record "
                f"cannot be checked and a count with no rate gets ranked raw"
            )
        expected = count / pairs
        if abs(rate - expected) > RATE_TOLERANCE:
            raise InvalidCatalogue(
                f"{where}: {rate_field} is {rate}, but {count_field} "
                f"{count} over {pairs} pair(s) is {expected:.4f}. A rate that "
                f"disagrees with its own numerator is worse than no rate: it "
                f"is what a ranking reads"
            )


RETIRED_FIELDS = ("on", "decision", "replacement", "replaced_by", "refused")
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_retired(where: str, retired) -> None:
    """A retired row: absent, or checked.

    A model the operator no longer offers keeps its row, because its figures were
    measured and history is never deleted; the page shows the row, dated, and does
    not let it be picked. The block says when (`on`), which entry in the project's
    own record retired it (`decision`), what to use instead (`replacement`, as the
    page words it, and optionally `replaced_by`, that row's id), and, when the
    vendor refuses this build's requests, the entry recording that (`refused`).
    """
    if retired is None:
        return
    if not isinstance(retired, dict):
        raise InvalidCatalogue(f"{where}.retired must be an object, got "
                               f"{type(retired).__name__}")
    stray = [key for key in retired if key not in RETIRED_FIELDS]
    if stray:
        raise InvalidCatalogue(f"{where}.retired carries unknown field(s) {', '.join(stray)}")
    if not isinstance(retired.get("on"), str) or not _ISO_DATE.match(retired["on"]):
        raise InvalidCatalogue(f"{where}.retired.on must be a YYYY-MM-DD date, got "
                               f"{retired.get('on')!r}")
    for field in ("decision", "refused"):
        if field == "refused" and field not in retired:
            continue
        value = retired.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise InvalidCatalogue(f"{where}.retired.{field} must be a positive whole "
                                   f"number, an entry in the project's record, got {value!r}")
    for field in ("replacement", "replaced_by"):
        if field == "replaced_by" and field not in retired:
            continue
        if not isinstance(retired.get(field), str) or not retired[field].strip():
            raise InvalidCatalogue(f"{where}.retired.{field} must be a non-empty string, "
                                   f"got {retired.get(field)!r}")


def validate_command_routes(block) -> None:
    """Raise `InvalidCatalogue` if the `command_routes` block cannot be trusted.

    Figures for command routes -- a subscription CLI at one model alias -- sit
    beside `models` rather than in it, because a route is not a wire name: a
    row in `models` is looked up by `for_api_model` to decide where a request
    is sent, and a route's alias (`haiku`) must never be routed that way.

    Each entry names a route id the way `commands.ROUTE_ID` spells one, the
    model alias and profile the route runs, and a `measured` block held to the
    model rows' rules. One rule of its own: **`usd_per_merge` is null.** The
    calls are included in the subscription and not priced per call, and a
    number there -- zero above all -- would be a price nobody was charged.
    """
    if not isinstance(block, list):
        raise InvalidCatalogue(f"command_routes must be a list or null, got "
                               f"{type(block).__name__}")
    seen: set[str] = set()
    for entry in block:
        if not isinstance(entry, dict):
            raise InvalidCatalogue(f"a command_routes entry is not an object: {entry!r}")
        route = entry.get("route")
        if not isinstance(route, str) or not ROUTE_ID.match(route):
            raise InvalidCatalogue(f"command_routes: {route!r} is not a route id")
        if route in seen:
            raise InvalidCatalogue(f"command_routes: route {route!r} appears twice")
        seen.add(route)
        where = f"command_routes.{route}"
        if not isinstance(entry.get("model"), str) or not entry["model"].strip():
            raise InvalidCatalogue(f"{where} names no model; a route's figures are "
                                   f"figures about the model it pins")
        if entry.get("profile") not in PROFILES:
            raise InvalidCatalogue(f"{where}: unknown profile {entry.get('profile')!r}")
        measured = entry.get("measured")
        validate_measured(where, measured)
        if isinstance(measured, dict) and measured.get("usd_per_merge") is not None:
            raise InvalidCatalogue(
                f"{where}.usd_per_merge is {measured['usd_per_merge']!r}; a command "
                f"route's calls are included in the subscription and not priced "
                f"per call, so the field is null")
        # The level the row's figures were measured at, when it says. The
        # page shows it beside them, because the effort slider shows figures
        # from other levels and a row that named none would read as all of them.
        if isinstance(measured, dict) and "merge_effort" in measured \
                and measured["merge_effort"] not in EFFORT_LEVELS:
            raise InvalidCatalogue(
                f"{where}.merge_effort is {measured['merge_effort']!r}, not one of "
                f"{', '.join(EFFORT_LEVELS)}")
        validate_effort_block(f"{where}.measured_by_effort",
                              entry.get("measured_by_effort"))
        validate_pinned_blocks(f"{where}.pinned_by_effort", entry)
        validate_alias_now(f"{where}.alias_now", entry)


def validate_alias_now(where: str, entry: dict) -> None:
    """Raise `InvalidCatalogue` if a route's `alias_now` cannot be trusted.

    Absent is the ordinary case: the alias still answers as `resolved_model`.
    Present, it is exactly `model`, `checked_on` and `cli_version`, dated and
    versioned because an alias moves with the CLI, and `model` differs from
    the `resolved_model` the route's figures name -- the same model would
    make every figure current and the label "history" false.
    """
    if "alias_now" not in entry:
        return
    now = entry["alias_now"]
    if not isinstance(now, dict) or set(now) != set(ALIAS_NOW_FIELDS):
        raise InvalidCatalogue(f"{where} must be exactly {', '.join(ALIAS_NOW_FIELDS)}, "
                               f"got {now!r}")
    if not isinstance(now["model"], str) or not now["model"].strip():
        raise InvalidCatalogue(f"{where}.model must name a model id")
    if now["model"] == entry.get("resolved_model"):
        raise InvalidCatalogue(f"{where}.model is the resolved_model the figures were "
                               f"measured on; leave alias_now out")
    if not isinstance(entry.get("resolved_model"), str):
        raise InvalidCatalogue(f"{where} needs the route's resolved_model to differ from")
    if not isinstance(now["checked_on"], str) or not _DATE.fullmatch(now["checked_on"]):
        raise InvalidCatalogue(f"{where}.checked_on must be a YYYY-MM-DD date")
    if not isinstance(now["cli_version"], str) or not _SEMVER.fullmatch(now["cli_version"]):
        raise InvalidCatalogue(f"{where}.cli_version must be a version like 2.1.283")


def validate_pinned_blocks(where: str, entry: dict) -> None:
    """Raise `InvalidCatalogue` if a route's `pinned_by_effort` cannot be trusted.

    Absent or an empty list is a route with no such figures. Otherwise a list
    of effort blocks, each held to `validate_effort_block`, and each naming
    the model id the grid asked for (`requested_model`) and the id that
    answered (`resolved_model`). The id asked for must differ from the route's
    own model: figures measured through the route's alias belong in
    `measured_by_effort`, and a pinned block that repeated the alias would be
    two blocks about one model with nothing on the page to tell them apart.
    Two blocks for one id would make the page choose one arbitrarily.
    """
    blocks = entry.get("pinned_by_effort", [])
    if not isinstance(blocks, list):
        raise InvalidCatalogue(f"{where} must be a list, got {type(blocks).__name__}")
    seen: set[str] = set()
    for i, block in enumerate(blocks):
        here = f"{where}[{i}]"
        if not isinstance(block, dict):
            raise InvalidCatalogue(f"{here} must be an object; a route with no pinned "
                                   f"figures leaves the list empty")
        for field in PINNED_FIELDS:
            if not isinstance(block.get(field), str) or not block[field].strip():
                raise InvalidCatalogue(f"{here}.{field} must name a model id, got "
                                       f"{block.get(field)!r}")
        asked = block["requested_model"]
        if asked == entry.get("model"):
            raise InvalidCatalogue(
                f"{here}.requested_model is the route's own model {asked!r}; figures "
                f"measured through the route's alias belong in measured_by_effort")
        if asked in seen:
            raise InvalidCatalogue(f"{here}: a second block for {asked!r}")
        seen.add(asked)
        validate_effort_block(here, block)


def _spread(where: str, figure, ceiling=None) -> None:
    """A median and range: three numbers, in order, under `ceiling` when given."""
    if not isinstance(figure, dict) or set(figure) != set(EFFORT_SPREAD_FIELDS):
        raise InvalidCatalogue(f"{where} must be exactly {', '.join(EFFORT_SPREAD_FIELDS)}, "
                               f"got {figure!r}")
    for name in EFFORT_SPREAD_FIELDS:
        value = figure[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise InvalidCatalogue(f"{where}.{name} must be a number, got {value!r}")
    if not figure["min"] <= figure["median"] <= figure["max"]:
        raise InvalidCatalogue(f"{where}: min {figure['min']}, median "
                               f"{figure['median']} and max {figure['max']} are not "
                               f"in order")
    if ceiling is not None and figure["max"] > ceiling:
        raise InvalidCatalogue(f"{where}.max is {figure['max']}, more than the "
                               f"{ceiling} there are")


def _rate_of(where: str, rate, count: int, over: int) -> None:
    if not isinstance(rate, (int, float)) or isinstance(rate, bool) \
            or abs(rate - count / over) > RATE_TOLERANCE:
        raise InvalidCatalogue(f"{where} is {rate!r}, but {count} over {over} is "
                               f"{count / over:.4f}")


def validate_effort_block(where: str, block) -> None:
    """Raise `InvalidCatalogue` if a route's `measured_by_effort` cannot be trusted.

    Null is the unmeasured route. Otherwise the four attribution fields, a
    positive `draws`, and a `levels` object keyed by level names this build
    has, each level held to its own arithmetic: every rate equal to its count
    over its denominator, `runs` the sum of the pairs' draws, nothing counted
    past what there was. It does not re-derive the figures from the records;
    `derived_by` names the program that does, and `tests/test_catalogue.py`
    runs it.
    """
    if block is None:
        return
    if not isinstance(block, dict):
        raise InvalidCatalogue(f"{where} must be an object or null, got "
                               f"{type(block).__name__}")
    missing = [field for field in REQUIRED_MEASURED_FIELDS if not block.get(field)]
    if missing:
        raise InvalidCatalogue(
            f"{where} is missing {', '.join(missing)}; a figure with no run, "
            f"artefacts and derived_by to check it against is not a measurement "
            f"here, it is an unattributed claim")
    if not isinstance(block["artefacts"], list):
        raise InvalidCatalogue(f"{where}.artefacts must be a list")
    draws = block.get("draws")
    if not _count(draws) or not draws:
        raise InvalidCatalogue(f"{where}.draws must be a positive count, got {draws!r}")
    # Whether the CLI ran in safe mode. Required, because the page says
    # "before safe mode" off it, and a block that did not say would have the
    # page say one thing or the other about a run it knows nothing of.
    if not isinstance(block.get("safe_mode"), bool):
        raise InvalidCatalogue(f"{where}.safe_mode must be true or false, got "
                               f"{block.get('safe_mode')!r}")
    levels = block.get("levels")
    if not isinstance(levels, dict) or not levels:
        raise InvalidCatalogue(f"{where} has no 'levels'; a route with nothing "
                               f"measured carries null instead")
    for level, figures in levels.items():
        here = f"{where}.levels.{level}"
        if level not in EFFORT_LEVELS:
            raise InvalidCatalogue(f"{here}: {level!r} is not an effort level "
                                   f"({', '.join(EFFORT_LEVELS)})")
        if not isinstance(figures, dict):
            raise InvalidCatalogue(
                f"{here} is {figures!r}; a level nobody ran is left out of "
                f"levels, never written as null or zero")
        stray = [key for key in figures if key not in EFFORT_LEVEL_FIELDS]
        if stray:
            raise InvalidCatalogue(f"{here} carries unknown field(s) {', '.join(stray)}")
        pairs = figures.get("pairs")
        if not isinstance(pairs, dict) or not pairs:
            raise InvalidCatalogue(f"{here} has no pairs")
        runs = 0
        for pair, cell in pairs.items():
            at = f"{here}.pairs.{pair}"
            if not isinstance(cell, dict):
                raise InvalidCatalogue(f"{at} must be an object")
            stray = [key for key in cell if key not in EFFORT_PAIR_FIELDS]
            if stray:
                raise InvalidCatalogue(f"{at} carries unknown field(s) {', '.join(stray)}")
            planted, ran = cell.get("planted"), cell.get("draws")
            if not _count(planted) or not planted:
                raise InvalidCatalogue(f"{at}.planted must be a positive count")
            if not _count(ran) or not 0 < ran <= draws:
                raise InvalidCatalogue(f"{at}.draws is {ran!r}; the grid ran {draws} "
                                       f"per level")
            _spread(f"{at}.fixed", cell.get("fixed"), ceiling=planted)
            _spread(f"{at}.seconds", cell.get("seconds"))
            if ("licence_fixed" in cell) != ("licence_fixed_rate" in cell):
                raise InvalidCatalogue(f"{at}: licence_fixed and licence_fixed_rate "
                                       f"travel together")
            if "licence_fixed" in cell:
                if not _count(cell["licence_fixed"]) or cell["licence_fixed"] > ran:
                    raise InvalidCatalogue(f"{at}.licence_fixed must be a count of at "
                                           f"most {ran} draws")
                _rate_of(f"{at}.licence_fixed_rate", cell["licence_fixed_rate"],
                         cell["licence_fixed"], ran)
            runs += ran
        if figures.get("runs") != runs:
            raise InvalidCatalogue(f"{here}.runs is {figures.get('runs')!r}, and its "
                                   f"pairs ran {runs}")
        searched = figures.get("searched")
        if not _count(searched) or searched > runs:
            raise InvalidCatalogue(f"{here}.searched must be a count of at most "
                                   f"{runs} runs, got {searched!r}")
        _rate_of(f"{here}.searched_rate", figures.get("searched_rate"), searched, runs)
        if EFFORT_USAGE_FIELD in figures:
            _spread(f"{here}.{EFFORT_USAGE_FIELD}", figures[EFFORT_USAGE_FIELD])
        if (EFFORT_UNCACHED_FIELD in figures) != (EFFORT_USAGE_FIELD in figures):
            raise InvalidCatalogue(f"{here}: {EFFORT_UNCACHED_FIELD} and "
                                   f"{EFFORT_USAGE_FIELD} travel together")
        if EFFORT_UNCACHED_FIELD in figures:
            _spread(f"{here}.{EFFORT_UNCACHED_FIELD}", figures[EFFORT_UNCACHED_FIELD])
    # On every level or on none: the page forms a ratio between two levels of
    # one block, and a block with usage at one of them has nothing to divide.
    with_usage = [level for level, figures in levels.items()
                  if EFFORT_USAGE_FIELD in figures]
    if with_usage and len(with_usage) != len(levels):
        raise InvalidCatalogue(f"{where}: {EFFORT_USAGE_FIELD} is on "
                               f"{', '.join(with_usage)} and not on every level")


def _count(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def validate_verify_depth(block) -> None:
    """Raise `InvalidCatalogue` if the `verify_depth` block cannot be trusted.

    The same four attribution fields as a model row, then the shape rules that
    keep the figure honest:

      every rate beside its count and denominator, and equal to their ratio;
      a zero denominator gives a null rate, never 0.0
      nothing numeric on a depth entry outside the two directions but its cost
      `cannot_detect` for a defect class the depth has no step to reach: it is
      named, it is left out of the rate rather than lowering it, and it must
      have gone undetected -- a class a depth cannot reach that it reached is
      a contradiction, not a figure
      every depth's plants, reachable and not, add up to the block's `plants`
      `speedup` equal to the comparator's seconds over this depth's

    It does not re-derive the figures from the records; `derived_by` names the
    program that does, and `tests/test_catalogue.py` runs it.
    """
    where = "verify_depth"
    if not isinstance(block, dict):
        raise InvalidCatalogue(f"{where} must be an object or null, got "
                               f"{type(block).__name__}")
    missing = [field for field in REQUIRED_MEASURED_FIELDS if not block.get(field)]
    if missing:
        raise InvalidCatalogue(
            f"{where} is missing {', '.join(missing)}; a figure with no run, "
            f"artefacts and derived_by to check it against is not a measurement "
            f"here, it is an unattributed claim")
    if not isinstance(block["artefacts"], list):
        raise InvalidCatalogue(f"{where}.artefacts must be a list, got "
                               f"{type(block['artefacts']).__name__}")
    if not isinstance(block.get("model"), str) or not block["model"].strip():
        raise InvalidCatalogue(f"{where} names no model; a detection figure "
                               f"is a figure about one model")
    for field in ("draws", "fixtures", "plants"):
        if not _count(block.get(field)) or not block[field]:
            raise InvalidCatalogue(f"{where}.{field} must be a positive count, "
                                   f"got {block.get(field)!r}")

    entries = block.get("depths")
    if not isinstance(entries, list) or not entries:
        raise InvalidCatalogue(f"{where} has no 'depths' list")
    seen: dict[str, dict] = {}
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("value") not in VERIFY_DEPTHS:
            raise InvalidCatalogue(
                f"{where}: a depth entry names no depth this build has "
                f"({', '.join(VERIFY_DEPTHS)}): {entry!r}"[:400])
        value = entry["value"]
        if value in seen:
            raise InvalidCatalogue(f"{where}: depth {value!r} is measured twice")
        seen[value] = entry
        stray = [key for key in entry if key not in VERIFY_DEPTH_ENTRY_FIELDS]
        if stray:
            raise InvalidCatalogue(
                f"{where}.{value} carries {', '.join(stray)} outside the two "
                f"directions; a figure over both directions at once is a blend, "
                f"and the directions have different denominators")
        for direction in VERIFY_DEPTH_DIRECTIONS:
            _validate_direction(f"{where}.{value}.{direction}", entry.get(direction))

        unreachable = entry.get("cannot_detect", [])
        if not isinstance(unreachable, list):
            raise InvalidCatalogue(f"{where}.{value}.cannot_detect must be a list")
        for gap in unreachable:
            if (not isinstance(gap, dict) or not isinstance(gap.get("class"), str)
                    or not gap["class"] or gap.get("direction") not in VERIFY_DEPTH_DIRECTIONS
                    or not _count(gap.get("plants")) or not gap["plants"]):
                raise InvalidCatalogue(
                    f"{where}.{value}.cannot_detect: every entry names a class, "
                    f"a direction and how many plants of it the test set holds: "
                    f"{gap!r}")
            if gap.get("detected") != 0:
                raise InvalidCatalogue(
                    f"{where}.{value}.cannot_detect names {gap['class']!r} as a "
                    f"class this depth cannot reach, and records "
                    f"{gap.get('detected')!r} detected; either it is reachable "
                    f"and belongs in the rate, or it was not detected")
        total = (sum(entry[d]["plants"] for d in VERIFY_DEPTH_DIRECTIONS)
                 + sum(gap["plants"] for gap in unreachable))
        if total != block["plants"]:
            raise InvalidCatalogue(
                f"{where}.{value} accounts for {total} plant(s), reachable and "
                f"not, and the test set holds {block['plants']}; a plant left "
                f"out of both is a miss nobody can see")
        if not _count(entry.get("model_calls")):
            raise InvalidCatalogue(f"{where}.{value}.model_calls must be a count")
        seconds = entry.get("seconds")
        if not isinstance(seconds, (int, float)) or isinstance(seconds, bool) \
                or seconds <= 0:
            raise InvalidCatalogue(f"{where}.{value}.seconds must be a positive "
                                   f"number, got {seconds!r}")

    comparator = block.get("comparator")
    if comparator not in seen:
        raise InvalidCatalogue(
            f"{where}.comparator is {comparator!r}, which is not one of the "
            f"depths measured here ({', '.join(seen)})")
    for value, entry in seen.items():
        speedup = entry.get("speedup")
        if value == comparator:
            if speedup is not None:
                raise InvalidCatalogue(f"{where}.{value} is the comparator and "
                                       f"carries a speedup against itself")
            continue
        if speedup is None:
            continue
        expected = seen[comparator]["seconds"] / entry["seconds"]
        if not isinstance(speedup, (int, float)) or abs(speedup - expected) > RATE_TOLERANCE:
            raise InvalidCatalogue(
                f"{where}.{value}.speedup is {speedup!r}, but {comparator}'s "
                f"{seen[comparator]['seconds']}s over this depth's "
                f"{entry['seconds']}s is {expected:.4f}")


def _validate_direction(where: str, figures) -> None:
    """One direction's figures: counts, rates, and the order between them."""
    if not isinstance(figures, dict):
        raise InvalidCatalogue(f"{where} is missing; both directions are "
                               f"reported for every depth, never one for both")
    stray = [key for key in figures if key not in VERIFY_DEPTH_DIRECTION_FIELDS]
    if stray:
        raise InvalidCatalogue(f"{where} carries unknown field(s) {', '.join(stray)}")
    counts = [name for name in VERIFY_DEPTH_DIRECTION_FIELDS if not name.endswith("_rate")]
    for name in counts:
        if not _count(figures.get(name)):
            raise InvalidCatalogue(f"{where}.{name} must be a count, got "
                                   f"{figures.get(name)!r}")
    for smaller, larger in (("plants_detected", "plants"),
                            ("plants_detected_mechanically", "plants_detected"),
                            ("guards_graded", "guards"),
                            ("guards_wrong", "guards_graded")):
        if figures[smaller] > figures[larger]:
            raise InvalidCatalogue(f"{where}.{smaller} is {figures[smaller]}, "
                                   f"more than {larger} {figures[larger]}")
    for rate_field, count_field, denominator_field in VERIFY_DEPTH_RATE_FIELDS:
        if rate_field not in figures:
            raise InvalidCatalogue(
                f"{where} has {count_field} and no {rate_field}; a count with no "
                f"rate gets compared raw across denominators that differ")
        rate, count = figures[rate_field], figures[count_field]
        denominator = figures[denominator_field]
        if denominator == 0:
            if rate is not None:
                raise InvalidCatalogue(
                    f"{where}.{rate_field} is {rate!r} over {denominator_field} "
                    f"0; a rate over nothing is null, and a 0.0 here reads as "
                    f"measured")
            continue
        if not isinstance(rate, (int, float)) or isinstance(rate, bool):
            raise InvalidCatalogue(f"{where}.{rate_field} must be a number over "
                                   f"{denominator_field} {denominator}, got {rate!r}")
        expected = count / denominator
        if abs(rate - expected) > RATE_TOLERANCE:
            raise InvalidCatalogue(
                f"{where}.{rate_field} is {rate}, but {count_field} {count} over "
                f"{denominator_field} {denominator} is {expected:.4f}")


def load(path: str | Path | None = None) -> dict:
    """Read, validate, and return the catalogue as a plain dict.

    `path` defaults to the file shipped beside this module. Passed explicitly
    it can be anything readable as JSON with this shape -- a fork's own
    measurements, or a file assembled for a one-off comparison -- and it is
    validated exactly the same way, because a caller that reaches for a
    non-default path is usually doing something unusual with the data and is
    the reader least able to notice a malformed row by eye.

    Returns the parsed dict verbatim, not a copy filtered down to some
    subset of fields: `models()` and `for_id()` below exist for the common
    case of wanting the model list, but a caller that wants
    `data["schema_version"]` or a future top-level field this loader does not
    yet know to special-case still gets it.
    """
    target = Path(path) if path is not None else DEFAULT_PATH
    data = json.loads(target.read_text(encoding="utf-8"))
    validate(data)
    return data


def models(path: str | Path | None = None) -> list[dict]:
    """Every model entry in the catalogue, measured or not, in file order.

    File order rather than sorted, so that whoever maintains catalogue.json
    controls the picker's default ordering (hosted first, then self-hosted,
    say) by the order they wrote the rows in, instead of that being an
    accident of whatever sort key a renderer picked.
    """
    return load(path)["models"]


def for_id(model_id: str, path: str | Path | None = None) -> dict | None:
    """The catalogue entry for `model_id`, or None if there is no such entry.

    None rather than raising: "the picker was asked about a model the
    catalogue has never heard of" is an ordinary event for a UI backed by a
    hand-maintained file -- a new model landed in `models.local.json` before
    anyone measured it, say -- and the caller deciding how to render that
    (grey it out, fall back to an unmeasured-looking row, refuse the
    request) is a UI decision this module has no business making for it.
    """
    for entry in models(path):
        if entry.get("id") == model_id:
            return entry
    return None


def provider_profile(provider: str, path: str | Path | None = None) -> str | None:
    """The request shape this provider's measured rows share, or None.

    The shape a model this catalogue does not know is sent with, once the
    request has named its provider. A model is sent to the
    endpoint stored for its provider, and the body that endpoint accepts is a
    fact about the endpoint as much as about the model: `max_tokens` and
    `temperature: 0.0` are refused by OpenAI's reasoning models whatever they
    are called. Without this, an id typed for the `openai` provider went out in
    the default `openai-compatible` shape and was refused on its first call.

    Read off the rows rather than kept in a second table, for `PROFILES`'
    reason. None when the provider has no row, or when its rows disagree:
    there is then no shape the rows vouch for, and the server's own setting or
    the default applies as it always did.
    """
    shapes = {entry.get("profile") for entry in models(path)
              if entry.get("provider") == provider and entry.get("profile")}
    return shapes.pop() if len(shapes) == 1 else None


def for_api_model(wire_name: str, path: str | Path | None = None) -> dict | None:
    """The catalogue entry whose wire name is `wire_name`, or None.

    The lookup the request path uses, and the reason `api_model` is required
    and unique. A submitted request carries a model *name*, not a catalogue id
    -- that is the whole point of sending the wire name -- and the server has
    to get from that name back to a provider before it knows which endpoint is
    allowed to serve it.

    None is the ordinary answer rather than an error, and it is the answer that
    makes a typed-in model id work: a name this catalogue has never heard of is
    a model the operator named themselves, and it goes to the endpoint the
    server was started with, which is exactly where a hand-typed name is meant
    to go. A catalogue row is the case that gets routed; everything else is the
    case that is left alone.
    """
    for entry in models(path):
        if entry.get("api_model") == wire_name:
            return entry
    return None
