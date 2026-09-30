#!/usr/bin/env python3
"""catalogue.json loads, validates, and refuses the shapes it must refuse.

`src/llossless/web/catalogue.py` is the only code that reads
`catalogue.json` before a UI does; a defect in its validation is invisible
until a bad row reaches a picker, and until this file existed nothing ran
that validation at all -- `"measured": null` in particular had never been
exercised, which is exactly the state every check in this project has been
caught in at least once.

Two of the checks below are regressions for defects a release-guard run
against the shipped file actually found, not hypothetical ones: a compute
provider named three times (twice in a self-hosted entry's `notes`, once in
`catalogue.py`'s own docstring, before both were rewritten), caught by
the release guard's provider scan; and six absolute paths
into the operator's home directory, one `source` field per model, caught by
its home-path scan (such a path is rewritten, never
exempted). Both scans run over `git ls-files`, so neither catches an
untracked file -- this module is the one that runs whether or not the
catalogue happens to be staged.

This file must not itself name a compute provider. The check below follows
`scripts/build_arm_bundle.py`'s own pattern: import `internal/tests/providers.py`
at runtime rather than repeat the literal, and report one fewer check rather
than fail when that module -- withheld from publication -- is not present in
this checkout. The home-path half of that pair is deliberately not duplicated here: it is owned by a check elsewhere, seeded both ways, and run over the whole published set, which includes this file.

Run with `python3 tests/test_catalogue.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "internal" / "tests"))

import socket_guard  # noqa: E402

# This module makes no call at all: it reads one JSON file shipped in the
# package, plus synthetic dicts built in memory for the cases the shipped
# file does not itself exercise. "It does not use the network" is a claim,
# and tests/test_socket_guard checks that every test module states it the
# same way.
socket_guard.install()

from llossless.web import catalogue  # noqa: E402
from llossless.structured import PROFILES  # noqa: E402

CATALOGUE_PATH = ROOT / "src" / "llossless" / "web" / "catalogue.json"

# There is deliberately no home-path detector here. That rule is owned
# elsewhere, seeded both ways, and scanned over the whole published set -- which
# includes this file and `catalogue.json` -- so a second copy here would be a
# weaker duplicate of a stronger check. It would also have to carry a probe
# string of the shape it detects, in a published file, which is the thing the
# release guard exists to refuse.

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def provider_detector():
    """`internal/tests/providers.py`, or None when it is not in the tree.

    A published clone does not carry it, so absence here
    means one fewer check runs, reported as such, rather than the whole
    module failing or -- worse -- quietly reporting a clean scan it did not
    perform. Mirrors `scripts/build_arm_bundle.py`'s `provider_detector()`.
    """
    try:
        import providers
        return providers
    except ImportError:
        return None


def minimal_entry(**overrides) -> dict:
    """One valid model entry, so a test only has to state what it breaks."""
    entry = {
        "id": "test-model",
        "api_model": "test-model-on-the-wire",
        "display_name": "Test Model",
        "provider": "test",
        "profile": "openai-compatible",
        "context_window": 8192,
        "measured": {
            "usd_per_merge": 0.01,
            "seconds_per_merge": 1.0,
            "silent_loss": 0,
            "silent_loss_per_pair": 0.0,
            "deviations": 0,
            "deviations_per_pair": 0.0,
            "pairs": 1,
            "fidelity": "high",
            "run": "test-run",
            "artefacts": ["results.json"],
            "derived_by": "test fixture",
            "measured_on": "2026-01-01",
            "claimcheck_commit": "0" * 12,
        },
    }
    entry.update(overrides)
    return entry


def minimal_catalogue(*entries: dict) -> dict:
    return {"schema_version": 1, "models": list(entries)}


def must_raise(data: dict, message: str) -> None:
    try:
        catalogue.validate(data)
        check(False, message)
    except catalogue.InvalidCatalogue:
        pass


def test_the_shipped_catalogue_loads_and_validates() -> None:
    data = catalogue.load()
    check(isinstance(data.get("models"), list) and len(data["models"]) > 0,
          "the shipped catalogue.json has no models")


def test_every_used_profile_is_registered_and_an_unknown_one_is_rejected() -> None:
    for entry in catalogue.models():
        check(entry.get("profile") in PROFILES,
              f"{entry.get('id')}: profile {entry.get('profile')!r} is not "
              f"in structured.PROFILES ({sorted(PROFILES)})")
    must_raise(minimal_catalogue(minimal_entry(profile="not-a-real-profile")),
               "an unregistered profile must raise InvalidCatalogue")


def test_every_entry_carries_a_wire_name_and_no_two_share_one() -> None:
    """`api_model` is required, and it is required to be unique. Must fire both.

    `id` is a display key and `api_model` is the string that goes on the wire;
    they are two fields because they are two strings. Falling back to the id is
    what sent `claude-haiku-4-5` to a vendor that only answers to
    `claude-haiku-4-5-20251001`, and `qwen3-8b` to an endpoint whose model is
    `qwen/qwen3-8b` -- both failing two steps into a run, after the documents
    had been uploaded, with a message naming a model nobody had typed.

    Uniqueness matters because the reverse lookup is what decides where a
    request goes: `for_api_model` maps the submitted name back to a provider,
    and two rows claiming one name would make that pick one arbitrarily.

    Must not fire: the shipped catalogue satisfies both, and at least one of
    its rows has a wire name that genuinely differs from its id -- without that
    last check the whole field could be a copy of `id` and nothing here would
    notice.
    """
    for absent in ({}, {"api_model": ""}, {"api_model": None}, {"api_model": 7}):
        entry = minimal_entry()
        if absent:
            entry.update(absent)
        else:
            entry.pop("api_model")
        must_raise(minimal_catalogue(entry),
                   f"an entry with api_model={absent.get('api_model', '<absent>')!r} "
                   f"must raise InvalidCatalogue")

    must_raise(minimal_catalogue(minimal_entry(api_model=" test-model ")),
               "a wire name with surrounding whitespace must raise: it is "
               "matched byte for byte and a stray space is a model the "
               "endpoint does not have")
    must_raise(minimal_catalogue(minimal_entry(api_model="a\nb")),
               "a wire name carrying a newline must raise")
    must_raise(minimal_catalogue(minimal_entry(id="one", api_model="same"),
                                 minimal_entry(id="two", api_model="same")),
               "two entries claiming one wire name must raise: for_api_model "
               "would pick one of them arbitrarily and route a request by it")

    shipped = catalogue.models()
    wire = [entry.get("api_model") for entry in shipped]
    check(all(isinstance(name, str) and name.strip() for name in wire),
          f"a shipped row has no usable wire name: {wire}")
    check(len(set(wire)) == len(wire),
          f"two shipped rows share a wire name: {wire}")
    check(any(entry["api_model"] != entry["id"] for entry in shipped),
          "no shipped row has a wire name that differs from its id, so the "
          "field could be a copy of id and every check above would still pass")


def test_the_shipped_wire_names_are_the_ones_the_recorded_runs_sent() -> None:
    """Which rows differ from their id, pinned against the runs they came from.

    Every `api_model` in the shipped catalogue was read off a recorded run's
    own `provenance.models` -- the string `Settings.model_for` handed the
    transport -- and not retyped from a vendor's documentation. Four of the six
    differ from their display id, and this pins which four.

    Without it the field can be silently "corrected" back to the id one row at
    a time and every other check in this module still passes: the uniqueness
    rule holds, the type rule holds, and the "at least one row differs" rule
    holds as long as one of the other three is untouched. That is exactly how
    this defect arrives -- somebody tidies one row.

    The pairs are the claim, so they are written out here rather than derived
    from the file: a check that read the file to decide what the file should
    say would agree with any file at all. `run` names where each came from;
    every run is published under `arms/` now, and this stays a pin
    rather than a re-derivation for the reason just given.
    """
    sent = {entry["id"]: entry["api_model"] for entry in catalogue.models()}
    expected = {
        # 2026-09-18-matrix (arms/2026-09-18/matrix), */report.json, provenance.models
        # claude-opus-5's row was removed from the card entirely (the
        # operator's ruling that Opus 5 is not Opus 5.5 and is no longer
        # credible here); it is no longer one of catalogue.models()'s rows.
        "claude-sonnet-5": "claude-sonnet-5",
        "claude-haiku-4-5": "claude-haiku-4-5-20251001",
        "gpt-5.6-terra": "gpt-5.6-terra",
        # 2026-09-25-vendor (arms/2026-09-25/vendor), */report.json, provenance.models
        "gpt-6-sol": "gpt-6-sol",
        "gpt-6-luna": "gpt-6-luna",
        "claude-opus-5-5": "claude-opus-5-5",
        # 2026-09-25-google (arms/2026-09-25/google), */report.json, provenance.models
        "gemini-3.8-flash": "gemini-3.8-flash",
        "gemini-3.5-flash-lite": "gemini-3.5-flash-lite",
        # 2026-09-16-phase4 (arms/2026-09-16/phase4), */report.json, provenance.models
        "qwen3-8b": "qwen/qwen3-8b",
        "qwen3.8-27b-fp8": "Qwen/Qwen3.8-27B-FP8",
    }
    check(sent == expected,
          f"the shipped wire names are not the ones the recorded runs sent. "
          f"Got {sent}; the runs sent {expected}. A row corrected back to its "
          f"display id is a request the endpoint will refuse two steps into a "
          f"merge")


def test_a_wire_name_resolves_back_to_exactly_one_entry() -> None:
    """`for_api_model` is the lookup that decides where a request is sent.

    Must fire on a name nothing claims -- which has to be None, because that
    is what makes a hand-typed model id work rather than being refused -- and
    must not fire on every shipped row, each of which has to resolve to itself.
    """
    for entry in catalogue.models():
        found = catalogue.for_api_model(entry["api_model"])
        check(found is not None and found["id"] == entry["id"],
              f"{entry['api_model']!r} does not resolve back to {entry['id']!r}")
    check(catalogue.for_api_model("a-model-nobody-has-measured") is None,
          "a name the catalogue has never heard of must resolve to None, or a "
          "typed model id becomes a refusal instead of a request")
    check(catalogue.for_id(catalogue.models()[0]["id"]) is not None,
          "for_id stopped working, so the two lookups are not both live")


def test_the_minimal_entry_itself_validates() -> None:
    """The fixture every refusal test builds on has to be valid to begin with.

    Without this, a rule added to `validate` that the fixture does not satisfy
    makes every `must_raise` test in this module pass for the wrong reason: the
    catalogue raises before the check reaches the defect it was written to
    probe, and a suite of green refusals proves nothing about any of them.

    That happened. `RATE_FIELDS` was added with the fixture carrying
    `silent_loss` and `deviations` but neither rate, so the fixture raised on
    the missing rate and six refusal tests went vacuous while staying green.
    """
    catalogue.validate(minimal_catalogue(minimal_entry()))


def test_a_rate_that_disagrees_with_its_own_count_is_rejected() -> None:
    """`deviations_per_pair` was published and read for a day with nothing
    checking it against `deviations / pairs`. The suite asserted only that the
    renderer *reads* the rate, which is a different claim: a wrong rate would
    have ranked models against each other and been believed.
    """
    for rate_field, count_field in catalogue.RATE_FIELDS:
        entry = minimal_entry()
        entry["measured"][count_field] = 9
        entry["measured"]["pairs"] = 3          # so the rate must be 3.0
        entry["measured"][rate_field] = 0.5
        must_raise(minimal_catalogue(entry),
                   f"{rate_field} disagreeing with {count_field} over pairs "
                   f"must raise InvalidCatalogue")

        # Must-not-fire: the same entry with the rate that the count implies.
        entry["measured"][rate_field] = 3.0
        catalogue.validate(minimal_catalogue(entry))

        # And rounding to two decimals must not be read as disagreement: 35
        # over 3 is 11.666..., published as 11.67, and an exact test would
        # refuse the shipped catalogue.
        entry["measured"][count_field] = 35
        entry["measured"][rate_field] = 11.67
        catalogue.validate(minimal_catalogue(entry))


def test_a_count_with_no_rate_is_rejected() -> None:
    """A count that ships without its rate gets ranked raw by whoever reads it,
    and the rows in this catalogue were measured over different numbers of
    pairs -- 19 over 9 ranks below 10 over 3 unless something divides.
    """
    for rate_field, _ in catalogue.RATE_FIELDS:
        entry = minimal_entry()
        del entry["measured"][rate_field]
        must_raise(minimal_catalogue(entry),
                   f"a measured block with no {rate_field} must raise")


def test_a_duplicate_id_is_rejected() -> None:
    must_raise(minimal_catalogue(minimal_entry(), minimal_entry()),
               "two entries sharing one id must raise InvalidCatalogue")


def test_a_measured_block_missing_a_required_field_is_rejected() -> None:
    for field in catalogue.REQUIRED_MEASURED_FIELDS:
        entry = minimal_entry()
        del entry["measured"][field]
        must_raise(minimal_catalogue(entry),
                   f"a measured block missing {field!r} must raise InvalidCatalogue")


def test_an_unknown_schema_version_is_rejected() -> None:
    bad = minimal_catalogue(minimal_entry())
    bad["schema_version"] = 999
    must_raise(bad, "an unrecognised schema_version must raise InvalidCatalogue")


def test_measured_null_is_accepted() -> None:
    """The one path the shipped catalogue never exercises -- all six entries
    there are measured -- so this is the must-fire probe for it rather than
    a read of the real file. Two qwen rows come closest (usd_per_merge is
    null) but their `measured` block as a whole is still present."""
    good = minimal_catalogue(minimal_entry(measured=None))
    try:
        catalogue.validate(good)
    except catalogue.InvalidCatalogue as exc:
        check(False, f"'measured': null must be accepted; it raised {exc}")


def test_no_entry_names_a_compute_provider() -> None:
    """Regression for the defect the release guard caught: a provider named
    three times before the fix, twice in this file's `notes`."""
    provider = provider_detector()
    if provider is None:
        print("  SKIP no-provider-name check: internal/tests/providers.py "
              "is withheld and absent from this checkout")
        return
    text = CATALOGUE_PATH.read_text(encoding="utf-8")
    found = provider.named(text)
    check(not found, f"catalogue.json names a compute provider: {found}")
    # The detector itself has to fire, or a quiet scan above proves nothing.
    with tempfile.TemporaryDirectory() as tmp:
        seeded = Path(tmp) / "seeded.json"
        seeded.write_text(provider.FIRE[0], encoding="utf-8")
        check(provider.named(seeded.read_text(encoding="utf-8")),
              "the provider detector did not fire on a seeded name -- a "
              "quiet catalogue.json scan above would prove nothing")


def test_a_provider_shape_is_the_one_its_rows_share_or_none() -> None:
    """The shape a model the catalogue does not know goes out in.

    Read off the rows, so it is whatever the measured rows of that provider
    were sent with; None where the provider has no row or its rows disagree,
    which leaves the server's own setting in charge as before.
    """
    for provider, want in (("openai", "openai-reasoning"), ("anthropic", "anthropic"),
                           ("self-hosted", "openai-compatible"), ("google", "google")):
        got = catalogue.provider_profile(provider)
        check(got == want, f"provider_profile({provider!r}) is {got!r}, want {want!r}")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "catalogue.json"
        path.write_text(json.dumps(minimal_catalogue(
            minimal_entry(id="a", api_model="a", provider="openai", profile="openai-reasoning"),
            minimal_entry(id="b", api_model="b", provider="openai",
                          profile="openai-compatible"))), encoding="utf-8")
        check(catalogue.provider_profile("openai", path) is None,
              "two rows of one provider that disagree must vouch for no shape")


def test_the_six_model_scope_is_recorded_as_deliberate() -> None:
    """Not a defect -- the six-model scope was accepted, not flagged -- but
    a future reader who notices a seventh vendor's model missing needs to be
    told that is a gap in what has been run, not in what this file allows,
    so this checks the note exists rather than just its content."""
    data = catalogue.load()
    check(isinstance(data.get("notes"), str) and len(data["notes"]) > 0,
          "catalogue.json has no top-level note recording that its model "
          "list is a deliberate, non-exhaustive scope")


# --------------------------------------------------------------------------
# the verify_depth block (W2)
# --------------------------------------------------------------------------


def shipped_with_block() -> dict:
    """The shipped catalogue, deep-copied, so a test can break its block."""
    import copy
    data = copy.deepcopy(catalogue.load())
    check(isinstance(data.get("verify_depth"), dict),
          "the shipped catalogue carries no verify_depth block; every probe "
          "below would break a block that is not there and pass vacuously")
    return data


def depth_entry(data: dict, value: str) -> dict:
    return next(e for e in data["verify_depth"]["depths"] if e["value"] == value)


def test_the_verify_depth_block_is_what_its_records_say() -> None:
    """The command `derived_by` names, run as a command, over the committed run.

    It re-grades the 26 committed reports, requires the committed regraded
    records back, forms every figure from them and requires the shipped block
    to equal it. A figure typed into catalogue.json by hand, or a `grade()`
    change that would move one, fails here.
    """
    import subprocess
    block = catalogue.load().get("verify_depth") or {}
    check("tests/depth_figures.py --check" in str(block.get("derived_by")),
          "verify_depth.derived_by does not name the command this test runs")
    run = subprocess.run([sys.executable, str(ROOT / "tests" / "depth_figures.py"),
                          "--check"], cwd=ROOT, capture_output=True, text=True)
    check(run.returncode == 0,
          f"tests/depth_figures.py --check exited {run.returncode}: "
          f"{(run.stdout + run.stderr).strip()[-600:]}")


def test_the_verify_depth_check_fires_on_a_changed_figure() -> None:
    """Seeded, both layers: a figure the records do not give, and a record the
    reports do not give, must each be reported."""
    import depth_figures
    data = shipped_with_block()
    depth_entry(data, "coverage")["source_to_merged"]["plants_detected"] = 2
    check(bool(depth_figures.block_problems(data["verify_depth"])),
          "a published plants_detected the records do not give was not reported")
    data = shipped_with_block()
    del depth_entry(data, "coverage")["speedup"]
    check(bool(depth_figures.block_problems(data["verify_depth"])),
          "a published block missing a derived figure was not reported")

    real = depth_figures.committed

    def tampered(arm: str) -> dict:
        blob = real(arm)
        blob["records"][0]["guard_wrong"] = ["seeded"]
        return blob

    depth_figures.committed = tampered
    try:
        check(bool(depth_figures.regrade_problems()),
              "a committed regraded record the reports do not give was not "
              "reported")
    finally:
        depth_figures.committed = real


def test_a_verify_depth_block_missing_a_required_field_raises() -> None:
    for field in catalogue.REQUIRED_MEASURED_FIELDS:
        data = shipped_with_block()
        del data["verify_depth"][field]
        must_raise(data, f"a verify_depth block missing {field!r} must raise")


def test_an_absent_verify_depth_block_is_the_unmeasured_state() -> None:
    """Absent or null validates: the page says "unmeasured" for it."""
    for absent in ("missing", None):
        data = shipped_with_block()
        if absent == "missing":
            del data["verify_depth"]
        else:
            data["verify_depth"] = None
        try:
            catalogue.validate(data)
        except catalogue.InvalidCatalogue as exc:
            check(False, f"a catalogue with verify_depth {absent} must validate; "
                         f"it raised {exc}")


def test_a_verify_depth_rate_is_checked_against_its_own_count() -> None:
    data = shipped_with_block()
    depth_entry(data, "full")["source_to_merged"]["plants_detected_rate"] = 0.5
    must_raise(data, "a plants_detected_rate that disagrees with plants_detected "
                     "over plants must raise")
    data = shipped_with_block()
    del depth_entry(data, "full")["merged_to_sources"]["guards_wrong_rate"]
    must_raise(data, "a guards_wrong count with no rate beside it must raise")


def test_a_rate_over_nothing_is_null_not_zero() -> None:
    """`coverage` grades no merged-side guard probe; 0.0 there reads as measured."""
    data = shipped_with_block()
    gap = depth_entry(data, "coverage")["merged_to_sources"]
    check(gap["guards_graded"] == 0 and gap["guards_wrong_rate"] is None,
          f"the probe's anchor has moved: {gap}")
    gap["guards_wrong_rate"] = 0.0
    must_raise(data, "a rate of 0.0 over a zero denominator must raise")


def test_a_figure_over_both_directions_is_refused() -> None:
    """Never blended: a rate at the depth level is over both directions."""
    data = shipped_with_block()
    depth_entry(data, "coverage")["plants_detected_rate"] = 0.86
    must_raise(data, "a depth-level plants_detected_rate must raise; it blends "
                     "the two directions")
    data = shipped_with_block()
    del depth_entry(data, "coverage")["merged_to_sources"]
    must_raise(data, "a depth entry missing one direction must raise")


def test_what_a_depth_cannot_reach_is_named_not_lowered() -> None:
    """The structural miss is a class outside the rate, and it adds back up."""
    data = shipped_with_block()
    gaps = depth_entry(data, "coverage")["cannot_detect"]
    check([g["class"] for g in gaps] == ["hallucination"],
          f"coverage's structural miss is not named as the invention class: {gaps}")
    gaps[0]["detected"] = 1
    must_raise(data, "a class a depth cannot reach, recorded as detected, must raise")
    data = shipped_with_block()
    depth_entry(data, "coverage")["cannot_detect"] = []
    must_raise(data, "dropping the unreachable plant leaves the depth accounting "
                     "for fewer plants than the test set holds, and must raise")


def test_the_depths_and_the_speedup_are_checked() -> None:
    data = shipped_with_block()
    depth_entry(data, "coverage")["value"] = "shallow"
    must_raise(data, "a depth this build does not have must raise")
    data = shipped_with_block()
    data["verify_depth"]["comparator"] = "coverage-plus"
    must_raise(data, "a comparator that is not a measured depth must raise")
    data = shipped_with_block()
    depth_entry(data, "coverage")["speedup"] = 3.0
    must_raise(data, "a speedup that disagrees with the two depths' seconds must raise")


# --------------------------------------------------------------------------
# the command_routes block
# --------------------------------------------------------------------------


def shipped_routes() -> dict:
    """The shipped catalogue, deep-copied, so a test can break its routes."""
    import copy
    data = copy.deepcopy(catalogue.load())
    check(isinstance(data.get("command_routes"), list) and data["command_routes"],
          "the shipped catalogue carries no command_routes block; every probe "
          "below would break a block that is not there and pass vacuously")
    return data


def measured_route(data: dict) -> dict:
    return next(entry for entry in data["command_routes"] if entry.get("measured"))


# `claude-haiku` and `claude-sonnet` were checked here against
# `tests/subscription_figures.py`'s re-derivation of the 2026-09-24 run until
# the release benchmark superseded both directly (2026-09-28); `claude-opus`
# followed later, once its own resolved_model caught up with its alias
# (matching `opus-5.5-sub`, measured directly by the same run). All three are
# now checked by `test_the_lineup_rows_are_what_their_records_say` and
# `test_the_lineup_check_fires_on_a_changed_figure` below; nothing here still
# checks `claude-opus` against `subscription_figures.py`'s 2026-09-24 run.


def test_the_subscription_check_only_fires_on_routes_it_still_owns() -> None:
    """subscription_figures.py forms every route in ROUTES for the
    history, but checks against catalogue.json only the ones catalogue.json's
    own `measured.derived_by` still names to it: `opus` alone for a time,
    until its own resolved_model caught up with its alias and its
    `measured` block moved to the release benchmark too, leaving none of
    ROUTES still attributed here. Must not fire: the shipped catalogue's
    `claude-haiku` row, now `tests/lineup_figures.py`'s and read differently
    from what this run's own cells give it. Must fire: `claude-haiku`
    reattributed to this script, still carrying the lineup's figures."""
    import copy
    import subscription_figures
    check(not subscription_figures.row_problems(catalogue.load()["command_routes"]),
          "subscription_figures.py flags a route tests/lineup_figures.py now owns")
    data = copy.deepcopy(catalogue.load())
    entry = next(e for e in data["command_routes"] if e["route"] == "claude-haiku")
    entry["measured"]["derived_by"] = str(entry["measured"]["derived_by"]).replace(
        "tests/lineup_figures.py", "tests/subscription_figures.py")
    check(bool(subscription_figures.row_problems(data["command_routes"])),
          "a route reattributed to subscription_figures.py with a figure the cells do "
          "not give was not reported")


def test_a_command_route_row_is_held_to_the_model_rows_rules() -> None:
    """Shape rules, each must-fire: a price, an id no route can carry, a
    duplicate, a rate off its count, and a figure with no attribution."""
    def broken(change) -> dict:
        data = shipped_routes()
        change(data)
        return data

    def priced(data):
        measured_route(data)["measured"]["usd_per_merge"] = 0.0
    must_raise(broken(priced), "a command route priced per call must raise, zero above all")

    def bad_id(data):
        data["command_routes"][0]["route"] = "Claude Haiku"
    must_raise(broken(bad_id), "a route id no route can carry must raise")

    def twice(data):
        data["command_routes"].append(dict(data["command_routes"][0]))
    must_raise(broken(twice), "a route listed twice must raise")

    def off_rate(data):
        measured_route(data)["measured"]["deviations_per_pair"] += 1
    must_raise(broken(off_rate), "a rate off its own count must raise")

    for field in catalogue.REQUIRED_MEASURED_FIELDS:
        def unattributed(data, field=field):
            del measured_route(data)["measured"][field]
        must_raise(broken(unattributed), f"a route's figures without {field!r} must raise")

    # And the page's reverse lookup is never handed a route alias as a wire
    # name: a route's model routes nowhere, which is the typed-id case.
    for entry in catalogue.load()["command_routes"]:
        check(catalogue.for_api_model(entry["model"]) is None,
              f"{entry['model']!r} resolves to a model row, so a typed alias "
              f"would be routed by a route's figures")


def test_a_retired_row_keeps_its_figures_and_a_malformed_retirement_raises() -> None:
    """`validate_retired`'s rules once retired API Opus 5 this way: the row
    stayed, dated, and was not offered. Opus 5 was later removed from the
    card entirely rather than kept retired, the operator's ruling that Opus
    5 is not Opus 5.5 and is no longer credible, so no shipped row exercises
    this mechanism any more, and it is held to synthetically instead of
    against the real card.

    A retired row that lost its measured block would be offered again and
    fail every run, and one that lost its figures would delete measured
    history; the mechanism itself keeps both, pinned on a fabricated row here.
    Then must-fire probes for `validate_retired`'s shape, and for a successor
    that is missing, retired itself, or self-named.
    """
    check(not [e["id"] for e in catalogue.load()["models"] if e.get("retired")],
          "no shipped row should be retired now that Opus 5 was removed from the "
          "card, not kept retired")

    successor = minimal_entry(id="test-successor", api_model="test-successor-wire")
    retired_block = {"on": "2026-09-25", "decision": 618, "replacement": "Test Successor",
                     "replaced_by": "test-successor", "refused": 617}
    retired = minimal_entry(id="test-retired", api_model="test-retired-wire",
                            retired=retired_block)
    catalogue.validate(minimal_catalogue(successor, retired))
    check(isinstance(retired.get("measured"), dict),
          "a retired row must keep its measured block; a picked row must never lose "
          "measured history")

    for bad in ({"on": "25.09.2026", "decision": 618, "replacement": "x"},
                {"on": "2026-09-25", "decision": "618", "replacement": "x"},
                {"on": "2026-09-25", "decision": 618, "replacement": ""},
                {"on": "2026-09-25", "decision": 618},
                {"on": "2026-09-25", "decision": 618, "replacement": "x", "refused": 0},
                {"on": "2026-09-25", "decision": 618, "replacement": "x", "since": "abc1234"},
                {"on": "2026-09-25", "decision": 618, "replacement": "x",
                 "replaced_by": "no-such-row"},
                {"on": "2026-09-25", "decision": 618, "replacement": "x",
                 "replaced_by": "test-retired"},
                "retired"):
        broken = minimal_entry(id="test-retired", api_model="test-retired-wire", retired=bad)
        must_raise(minimal_catalogue(successor, broken),
                   f"a malformed retired block {bad!r} must raise")

    # A successor that is itself retired must also raise: the page's "use
    # this instead" must never point at a dead end.
    retired_successor = minimal_entry(id="test-successor", api_model="test-successor-wire",
                                      retired={"on": "2026-09-25", "decision": 618,
                                               "replacement": "y"})
    must_raise(minimal_catalogue(retired_successor,
                                 minimal_entry(id="test-retired", api_model="test-retired-wire",
                                              retired=retired_block)),
               "a successor that is itself retired must raise")


# `claude-opus-5-5`, `gpt-6-sol` and `gpt-6-luna` were checked here against
# the 2026-09-25 vendor run until the release benchmark superseded all three
# (2026-09-28): see `test_the_lineup_rows_are_what_their_records_say`
# and `test_the_lineup_check_fires_on_a_changed_figure` below. `vendor_figures.ROWS`
# still forms all three, for the history `tests/benchmark_matrix.py` and
# `tests/test_figure_rules.py` read; its catalogue check now finds
# none of them still attributed to it, seeded below.


def test_the_vendor_check_only_fires_on_rows_it_still_owns() -> None:
    """vendor_figures.py forms every row in ROWS for the history, but
    checks against catalogue.json only the ones catalogue.json's own
    `measured.derived_by` still names to it. Must not fire: the shipped
    catalogue's three rows, all now `tests/lineup_figures.py`'s and read
    differently from what this run's own cells give them. Must fire: one of
    them reattributed to this script, still carrying the lineup's figures."""
    import copy
    import vendor_figures
    check(not vendor_figures.row_problems(catalogue.load()["models"]),
          "vendor_figures.py flags a row tests/lineup_figures.py now owns")
    data = copy.deepcopy(catalogue.load())
    entry = next(e for e in data["models"] if e["id"] == "gpt-6-sol")
    entry["measured"]["derived_by"] = str(entry["measured"]["derived_by"]).replace(
        "tests/lineup_figures.py", "tests/vendor_figures.py")
    check(bool(vendor_figures.row_problems(data["models"])),
          "a row reattributed to vendor_figures.py with a figure the cells do not give "
          "was not reported")


def effort_route(data: dict, route: str = "claude-opus") -> dict:
    return next(entry for entry in data["command_routes"] if entry["route"] == route)


def test_the_per_effort_blocks_are_what_the_grid_says() -> None:
    """The command `derived_by` names, run as a command, over the committed grid.

    It checks every scored record against its own outcomes, forms every level
    from the records, requires the cells `score_grid.py` rendered into
    `tables.md` back, and requires the shipped blocks to equal the levels.
    """
    import subprocess
    for entry in shipped_routes()["command_routes"]:
        block = entry.get("measured_by_effort")
        if block:
            check("tests/effort_figures.py --check" in str(block.get("derived_by")),
                  f"{entry['route']}: derived_by does not name the command this test runs")
    run = subprocess.run([sys.executable, str(ROOT / "tests" / "effort_figures.py"),
                          "--check"], cwd=ROOT, capture_output=True, text=True)
    check(run.returncode == 0,
          f"tests/effort_figures.py --check exited {run.returncode}: "
          f"{(run.stdout + run.stderr).strip()[-600:]}")
    # The page's two unmeasured states, as the catalogue carries them: Haiku
    # has figures at medium alone, and Fable at none.
    data = shipped_routes()
    check(list(effort_route(data, "claude-haiku")["measured_by_effort"]["levels"]) == ["medium"],
          "Haiku was run at medium only, and its block must say so by absence")
    check(effort_route(data, "claude-fable").get("measured_by_effort", "absent") is None,
          "Fable was never run, so its block is null")
    # `max` is `config.EFFORT_LEVELS`' fifth level, on the slider since
    # `commands.EFFORT_CHOICES` but not in the registered benchmark grid: no route's
    # own block may claim it, and `catalogue.load()` above already validated
    # the file with it absent everywhere, which is how an unmeasured level
    # reads. The one measurement of `max` is Opus 5.5's, in
    # `pinned_by_effort`, not here.
    check(all("max" not in (entry.get("measured_by_effort") or {}).get("levels", {})
              for entry in data["command_routes"]),
          "max was never run by the grid, so no route's block may claim a level for it")


def test_the_per_effort_check_fires_on_a_changed_figure() -> None:
    """Seeded, all three layers: a published figure the records do not give, a
    level the grid never ran, figures on the route it never ran, a record whose
    count disagrees with its outcomes, and a record the table does not give."""
    import effort_figures
    data = shipped_routes()
    # claude-opus lost its own measured_by_effort grid once its
    # resolved_model caught up with its alias; claude-sonnet still carries a
    # real grid (low-xhigh) and stands in for it here.
    effort_route(data, "claude-sonnet")["measured_by_effort"]["levels"]["high"]["pairs"]["voyager"]["fixed"]["median"] += 1
    check(bool(effort_figures.catalogue_problems(data["command_routes"])),
          "a published median the records do not give was not reported")
    data = shipped_routes()
    haiku = effort_route(data, "claude-haiku")["measured_by_effort"]["levels"]
    haiku["low"] = dict(haiku["medium"])
    check(bool(effort_figures.catalogue_problems(data["command_routes"])),
          "figures at a level the grid never ran were not reported")
    data = shipped_routes()
    effort_route(data, "claude-fable")["measured_by_effort"] = dict(
        effort_route(data, "claude-sonnet")["measured_by_effort"])
    check(bool(effort_figures.catalogue_problems(data["command_routes"])),
          "figures on the route the grid never ran were not reported")

    scored = effort_figures.load(effort_figures.SCORED)
    record = next(r for r in scored if r["pair"] == "voyager")
    record["fixed"] += 1
    check(bool(effort_figures.record_problems(scored)),
          "a scored record whose fixed disagrees with its own outcomes was not reported")
    scored = effort_figures.load(effort_figures.SCORED)
    record = next(r for r in scored if r["pair"] == "bip39" and r["model"] == "opus")
    record["fixed"] -= 1
    record["outcomes"][next(k for k, v in record["outcomes"].items() if v == "fixed")] = "kept"
    record["kept"] = (record.get("kept") or 0) + 1
    check(not effort_figures.record_problems(scored),
          "the seeded record must be self-consistent, so only the table can catch it")
    formed = effort_figures.blocks(scored, effort_figures.load(effort_figures.RESULTS))
    check(bool(effort_figures.table_problems(formed)),
          "a record the published table does not give was not reported")

    scored = effort_figures.load(effort_figures.SCORED)
    results = effort_figures.load(effort_figures.RESULTS)
    check(not effort_figures.effort_problems(scored, results),
          "every committed draw's calls ran at the level its record names")
    run = next(r for r in results if r["effort"] == "high" and r["pair"] == "voyager")
    next(c for c in run["calls"] if c["role"] == "merge")["effort"] = "medium"
    check(bool(effort_figures.effort_problems(scored, results)),
          "a draw filed under high whose merge ran at medium was not reported")


def test_a_per_effort_block_is_held_to_its_own_arithmetic() -> None:
    """Shape rules, each must-fire: a level this build has not got, an
    unmeasured level written as zeros or null, a rate off its count, a range
    out of order, more fixed than planted, runs off the pairs' draws, and a
    block with no attribution. And the command_routes block's rows name a real level."""
    def broken(change) -> dict:
        data = shipped_routes()
        # claude-opus's own measured_by_effort grid is gone; claude-sonnet
        # still carries one and stands in for it here.
        change(effort_route(data, "claude-sonnet")["measured_by_effort"])
        return data

    def level(block):
        return block["levels"]["high"]

    must_raise(broken(lambda b: b["levels"].update(extreme=level(b))),
               "a level this build does not have must raise")
    must_raise(broken(lambda b: b["levels"].update(max=None)),
               "an unmeasured level written as null must raise; it is left out")
    must_raise(broken(lambda b: level(b).update(searched_rate=0.5)),
               "a searched rate off its count must raise")
    must_raise(broken(lambda b: level(b)["pairs"]["bip39"].update(licence_fixed_rate=0.0)),
               "a licence rate off its count must raise")
    must_raise(broken(lambda b: level(b)["pairs"]["voyager"]["fixed"].update(min=40)),
               "a range out of order must raise")
    must_raise(broken(lambda b: level(b)["pairs"]["voyager"]["fixed"].update(max=45)),
               "more fixed than were planted must raise")
    must_raise(broken(lambda b: level(b).update(runs=7)),
               "runs that are not the pairs' draws must raise")
    must_raise(broken(lambda b: level(b).update(searched=7, runs=6)),
               "more runs searched than ran must raise")
    for field in catalogue.REQUIRED_MEASURED_FIELDS:
        must_raise(broken(lambda b, field=field: b.pop(field)),
                   f"a per-effort block without {field!r} must raise")
    must_raise(broken(lambda b: b.pop("safe_mode")),
               "a per-effort block that does not say whether it ran in safe mode must raise")

    data = shipped_routes()
    effort_route(data)["measured"]["merge_effort"] = "turbo"
    must_raise(data, "a merge_effort that is not a level must raise")


def test_the_route_rows_name_the_level_they_were_measured_at() -> None:
    """The command_routes block's rows carry `merge_effort`, derived from each run's own decoding.

    Seeded: a published `merge_effort` the runs do not give is reported. Every
    route's `measured` block traces to the release benchmark now, so
    the seeded probe runs through `lineup_figures.catalogue_problems`.
    """
    import lineup_figures
    for entry in shipped_routes()["command_routes"]:
        if entry.get("measured"):
            check(entry["measured"].get("merge_effort") == "medium",
                  f"{entry['route']}: these figures were measured at merge "
                  f"medium and must say so: {entry['measured'].get('merge_effort')!r}")
    figures = lineup_figures.load(lineup_figures.EVIDENCE / "figures.json")
    data = shipped_routes()
    measured_route(data)["measured"]["merge_effort"] = "high"
    check(bool(lineup_figures.catalogue_problems(data, figures)),
          "a merge_effort the release benchmark does not give was not reported")


def test_catalogue_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def test_a_free_tier_row_carries_no_dollar_figure() -> None:
    """`measured.billed: free-tier` with a dollar figure is refused;
    without one it validates, and an unknown `billed` value is refused."""
    base = minimal_entry()
    base["measured"]["billed"] = "free-tier"
    must_raise(minimal_catalogue(base), "a free-tier row with usd_per_merge must raise")
    base["measured"]["usd_per_merge"] = None
    try:
        catalogue.validate(minimal_catalogue(base))
    except catalogue.InvalidCatalogue as exc:
        check(False, f"a free-tier row with a null dollar figure must validate: {exc}")
    base["measured"]["billed"] = "gratis"
    must_raise(minimal_catalogue(base), "an unknown billed value must raise")


GOOGLE_ROWS = ("gemini-3.8-flash", "gemini-3.5-flash-lite")


def google_rows(data: dict) -> list[dict]:
    """The 2026-09-25 free-tier rows that carry figures."""
    return [e for e in data["models"] if e["id"] in GOOGLE_ROWS and e.get("measured")]


def test_the_gemini_rows_are_what_their_records_say() -> None:
    """The command `derived_by` names, run as a command, over the committed run.

    `tests/google_figures.py --check` re-scores the published cells of
    `arms/2026-09-25/google/`, requires the committed scored cells back, forms
    the rows and requires the shipped rows, and the figures their notes state,
    to equal them.
    """
    import subprocess
    rows = google_rows(catalogue.load())
    check(bool(rows), "no Gemini row carries figures; the probes below would pass vacuously")
    for entry in rows:
        check("tests/google_figures.py --check" in str(entry["measured"].get("derived_by")),
              f"{entry['id']}: derived_by does not name the command this test runs")
        check(entry["measured"].get("usd_per_merge") is None,
              f"{entry['id']}: a free-tier row carries a dollar figure; nothing was billed")
    run = subprocess.run([sys.executable, str(ROOT / "tests" / "google_figures.py"),
                          "--check"], cwd=ROOT, capture_output=True, text=True)
    check(run.returncode == 0,
          f"tests/google_figures.py --check exited {run.returncode}: "
          f"{(run.stdout + run.stderr).strip()[-600:]}")


def test_the_gemini_check_fires_on_a_changed_figure() -> None:
    """Seeded: a changed count, a $0.00 where the run was not billed, a notes
    line that drops the paid-tier figure, and a scored cell the raw runs do
    not give."""
    import copy
    import google_figures
    data = copy.deepcopy(catalogue.load())
    rows = google_rows(data)
    if not rows:
        check(False, "no Gemini row to seed")
        return
    rows[0]["measured"]["deviations"] += 1
    check(bool(google_figures.row_problems(data["models"])),
          "a published deviations count the cells do not give was not reported")
    data = copy.deepcopy(catalogue.load())
    google_rows(data)[0]["measured"]["usd_per_merge"] = 0.0
    check(bool(google_figures.row_problems(data["models"])),
          "a $0.00 on a free-tier row was not reported")
    data = copy.deepcopy(catalogue.load())
    row = google_rows(data)[0]
    row["notes"] = row["notes"].replace("per merge", "each")
    check(bool(google_figures.row_problems(data["models"])),
          "notes that no longer state the paid-tier figure were not reported")
    real = google_figures.load

    def tampered(path):
        blob = real(path)
        if path == google_figures.SCORED:
            counted = next(c for c in blob if not c["excluded"])
            counted["silent"] = counted.get("silent", 0) + 1
        return blob

    google_figures.load = tampered
    try:
        found, _said = google_figures.score_problems()
        check(bool(found), "a scored cell the raw runs do not give was not reported")
    finally:
        google_figures.load = real


def opus55_block(data: dict) -> dict:
    return next(block for block in effort_route(data).get("pinned_by_effort") or []
                if block.get("requested_model") == "claude-opus-5-5")


def test_the_opus55_block_is_what_its_run_says() -> None:
    """The command `derived_by` names, run as a command, over the committed run."""
    import subprocess
    block = opus55_block(shipped_routes())
    check("tests/opus55_effort_figures.py --check" in str(block.get("derived_by")),
          "the Opus 5.5 block's derived_by does not name the command this test runs")
    check(sorted(block["levels"]) == ["max", "xhigh"],
          "Opus 5.5 was run at xhigh and max only, and its block must say so by absence")
    run = subprocess.run([sys.executable, str(ROOT / "tests" / "opus55_effort_figures.py"),
                          "--check"], cwd=ROOT, capture_output=True, text=True)
    check(run.returncode == 0,
          f"tests/opus55_effort_figures.py --check exited {run.returncode}: "
          f"{(run.stdout + run.stderr).strip()[-600:]}")


def test_the_opus55_check_fires_on_a_changed_figure() -> None:
    """Seeded, all three layers: a published figure or usage the records do not
    give, the block on another route, a record off its own outcomes, a call at
    the wrong level, model or mode, and a record the table does not give."""
    import opus55_effort_figures as o55
    data = shipped_routes()
    opus55_block(data)["levels"]["max"]["pairs"]["voyager"]["fixed"]["median"] += 1
    check(bool(o55.catalogue_problems(data["command_routes"])),
          "a published median the records do not give was not reported")
    data = shipped_routes()
    opus55_block(data)["levels"]["max"]["api_equivalent_usd"]["median"] = 1.0
    check(bool(o55.catalogue_problems(data["command_routes"])),
          "a usage figure the records do not give was not reported")
    data = shipped_routes()
    opus55_block(data)["levels"]["high"] = opus55_block(data)["levels"]["xhigh"]
    check(bool(o55.catalogue_problems(data["command_routes"])),
          "figures at a level the run never ran were not reported")
    data = shipped_routes()
    effort_route(data, "claude-sonnet")["pinned_by_effort"] = [opus55_block(data)]
    check(bool(o55.catalogue_problems(data["command_routes"])),
          "the block filed under a route it was not run through was not reported")
    data = shipped_routes()
    effort_route(data)["pinned_by_effort"] = []
    check(bool(o55.catalogue_problems(data["command_routes"])),
          "a missing block was not reported")

    scored = o55.load(o55.SCORED)
    next(r for r in scored if r["pair"] == "voyager")["fixed"] += 1
    check(bool(o55.record_problems(scored)),
          "a scored record whose fixed disagrees with its own outcomes was not reported")
    scored, results = o55.load(o55.SCORED), o55.load(o55.RESULTS)
    check(not o55.run_problems(scored, results), "every committed call is as registered")
    for field, value in (("effort", "high"), ("model_flag", "opus"), ("safe_mode", False)):
        results = o55.load(o55.RESULTS)
        run = next(r for r in results if r["pair"] == "voyager" and r["effort"] == "max")
        next(c for c in run["calls"] if c["role"] == "merge")[field] = value
        check(bool(o55.run_problems(scored, results)),
              f"a merge call with {field} {value!r} was not reported")
    scored = o55.load(o55.SCORED)
    record = next(r for r in scored if r["pair"] == "voyager" and r["effort"] == "max")
    record["fixed"] -= 1
    record["outcomes"][next(k for k, v in record["outcomes"].items() if v == "fixed")] = "kept"
    record["kept"] += 1
    check(not o55.record_problems(scored),
          "the seeded record must be self-consistent, so only the table can catch it")
    check(bool(o55.table_problems(o55.block(scored, o55.load(o55.RESULTS)))),
          "a record the published table does not give was not reported")


def test_the_mahjongg_rescore_is_rederived_and_fires_when_seeded() -> None:
    """Ruled 2026-09-28: the control's figures are the corrected
    scorer's over the draw each record names, the first-published count is
    re-derived beside them, and the catalogue note states both. Must-not-fire
    on the committed files; must-fire on each seeded defect, including the old
    counting rule put back into the scorer the check calls."""
    import mahjongg_figures as mf
    import opus55_effort_figures as o55
    for arm in mf.ARMS:
        check(not mf.problems(arm), f"{arm.path}: the committed mahjongg figures must "
              f"be the rescore's: {mf.problems(arm)[:2]}")
    arm = mf.SUBSCRIPTION
    scored = mf.load(arm.root / "scored.json")
    record = next(r for r in scored if r.get("pair") == "mahjongg" and r["model"] == "opus")
    record["false_corrections"] = record["rescored"]["first_scored"]["false_corrections"]
    check(bool(mf.problems(arm, scored)),
          "a record carrying the first-published count as its figure was not reported")
    scored = mf.load(arm.root / "scored.json")
    record = next(r for r in scored if r.get("pair") == "mahjongg" and r["model"] == "opus")
    record["rescored"]["first_scored"]["false_corrections"] += 1
    check(bool(mf.problems(arm, scored)),
          "a first-published count the first scoring's rule does not give was not reported")
    scored = mf.load(arm.root / "scored.json")
    record = next(r for r in scored if r.get("pair") == "mahjongg" and r["model"] == "opus")
    record["attempt"] = 9
    check(any("runner rows" in p for p in mf.problems(arm, scored)),
          "a record naming a draw the runner never ran was not reported")
    text = (arm.root / "tables.md").read_text(encoding="utf-8")
    seeded = text.replace("|  | 2 (1-2) |", "|  | 3 (2-3) |", 1)
    check(seeded != text and bool(mf.problems(arm, None, seeded)),
          "a tables.md cell still at the first-published count was not reported")
    real = mf.score_planted.false_corrections

    def first_rule(path, pair="mahjongg"):
        got = real(path, pair)
        return {**got, "false_corrections": got["false_corrections_changed"]
                + got["false_corrections_declared"]}
    mf.score_planted.false_corrections = first_rule
    try:
        check(bool(mf.problems(mf.OPUS_MAX)),
              "the scorer's old double count, put back, was not reported")
    finally:
        mf.score_planted.false_corrections = real
    data = shipped_routes()
    block = opus55_block(data)
    block["notes"] = block["notes"].replace("max: 4 mechanical", "max: 7 mechanical", 1)
    check(bool(o55.catalogue_problems(data["command_routes"])),
          "a catalogue note stating the first-published mahjongg count was not reported")
    check(not o55.catalogue_problems(shipped_routes()["command_routes"]),
          "the shipped Opus 5.5 block, notes included, must be what its run says")


def test_a_pinned_block_is_held_to_its_own_rules() -> None:
    """Each must-fire: the route's own alias as the pinned id, no id, one id
    twice, not a list, a level this build has not got, usage on one level only,
    usage out of order, and a usage field under another name."""
    def broken(change) -> dict:
        data = shipped_routes()
        change(effort_route(data), opus55_block(data))
        return data

    catalogue.validate(broken(lambda entry, block: None))
    must_raise(broken(lambda entry, block: block.update(requested_model=entry["model"])),
               "a pinned block for the route's own alias must raise")
    must_raise(broken(lambda entry, block: block.pop("resolved_model")),
               "a pinned block naming no answering model must raise")
    must_raise(broken(lambda entry, block: entry["pinned_by_effort"].append(dict(block))),
               "two pinned blocks for one id must raise")
    must_raise(broken(lambda entry, block: entry.update(pinned_by_effort=block)),
               "pinned_by_effort that is not a list must raise")
    must_raise(broken(lambda entry, block: block["levels"].update(
        extreme=block["levels"]["max"])), "a level this build does not have must raise")
    must_raise(broken(lambda entry, block: block["levels"]["xhigh"].pop("api_equivalent_usd")),
               "usage on one level and not the other must raise")
    must_raise(broken(lambda entry, block: block["levels"]["max"]["api_equivalent_usd"].update(
        min=9.0)), "a usage range out of order must raise")
    must_raise(broken(lambda entry, block: block["levels"]["max"].update(
        usd=block["levels"]["max"]["api_equivalent_usd"])),
               "a usage figure under a name the validator does not know must raise")


def test_alias_now_is_dated_and_names_another_model() -> None:
    """`alias_now` records that a route's alias answers as a model its
    own figures were not measured on, dated and versioned.

    Previously, the Opus route's alias answered as claude-opus-5-5 since
    2026-09-26 while its own figures (and `resolved_model`) still named
    claude-opus-5, and this test held that literal state. The operator's
    ruling that Opus 5 is not Opus 5.5 and is no longer credible retired that
    state rather than the mechanism: the route's own `measured` moved to the
    release benchmark's `opus-5.5-sub` figures, `resolved_model` became
    claude-opus-5-5 to match, and `alias_now` came out with it (the schema
    forbids `alias_now.model` equalling `resolved_model`, and the two now
    agree). No shipped route carries `alias_now` any more, so the mechanism
    is held to synthetically here instead; each rule must-fire: the model its
    figures already name, no date, a version that is not one, a stray field.
    """
    check(not [e["route"] for e in catalogue.load()["command_routes"] if "alias_now" in e],
          "no shipped route should carry alias_now now that opus's own resolved_model "
          "has caught up with its alias")

    def route_with(alias_now) -> dict:
        entry = {"route": "claude-sonnet", "model": "sonnet", "profile": "subscription",
                 "resolved_model": "claude-sonnet-5"}
        if alias_now is not None:
            entry["alias_now"] = alias_now
        return {"schema_version": 1, "models": [], "command_routes": [entry]}

    catalogue.validate(route_with(None))  # absent is the ordinary case
    ok = {"model": "claude-sonnet-5-5", "checked_on": "2026-09-26", "cli_version": "2.1.283"}
    catalogue.validate(route_with(dict(ok)))  # a well-formed alias_now must not raise

    def broken(change) -> dict:
        data = route_with(dict(ok))
        change(data["command_routes"][0]["alias_now"])
        return data

    must_raise(broken(lambda now: now.update(model="claude-sonnet-5")),
               "alias_now naming the model the figures were measured on must raise")
    must_raise(broken(lambda now: now.pop("checked_on")), "an undated alias_now must raise")
    must_raise(broken(lambda now: now.update(cli_version="latest")),
               "an alias_now whose version is not one must raise")
    must_raise(broken(lambda now: now.update(note="x")),
               "a field alias_now does not have must raise")


# Two earlier published runs, each row's figures
# re-derived from its committed cells. `claude-sonnet-5` and `claude-haiku-4-5`
# dropped from matrix_figures: the release benchmark superseded both,
# and their rows are checked by `test_the_lineup_rows_are_what_their_records_say`
# instead.
EARLY_ROWS = {"matrix_figures": ("claude-opus-5", "gpt-5.6-terra"),
              "phase4_figures": ("qwen3-8b", "qwen3.8-27b-fp8")}


def test_the_early_rows_are_what_their_records_say() -> None:
    """The command each row's `derived_by` names, run as a command.

    A row in `matrix_figures.REMOVED_FROM_CARD` (claude-opus-5) is
    missing from the card by ruling, not by a broken attribution, and is
    skipped here the same way `matrix_figures.row_problems()` skips it.
    """
    import subprocess
    import matrix_figures
    removed = {"matrix_figures": matrix_figures.REMOVED_FROM_CARD}
    data = catalogue.load()
    for program, ids in EARLY_ROWS.items():
        for row_id in ids:
            if row_id in removed.get(program, {}):
                continue
            entry = next((e for e in data["models"] if e["id"] == row_id), None)
            check(entry is not None and f"tests/{program}.py --check" in
                  str((entry.get("measured") or {}).get("derived_by")),
                  f"{row_id}: derived_by does not name tests/{program}.py --check")
        run = subprocess.run([sys.executable, str(ROOT / "tests" / f"{program}.py"),
                              "--check"], cwd=ROOT, capture_output=True, text=True)
        check(run.returncode == 0,
              f"tests/{program}.py --check exited {run.returncode}: "
              f"{(run.stdout + run.stderr).strip()[-600:]}")


def test_the_early_checks_fire_on_a_changed_figure() -> None:
    """Each must-fire: a figure the cells do not give, a missing row, and
    a scored cell the raw runs do not give, on both programs.

    `matrix_figures.REMOVED_FROM_CARD`'s `claude-opus-5` is already
    missing from the real card, by ruling; the missing-row must-fire probe
    below uses an id that is not in that set, and a separate must-not-fire
    confirms the removed one stays quiet.
    """
    import copy
    import importlib
    import matrix_figures
    removed = {"matrix_figures": matrix_figures.REMOVED_FROM_CARD}
    for program, ids in EARLY_ROWS.items():
        module = importlib.import_module(program)
        for key, delta in (("silent_loss", 1), ("deviations", 1), ("seconds_per_merge", 1)):
            data = copy.deepcopy(catalogue.load())
            entry = next(e for e in data["models"] if e["id"] == ids[-1])
            entry["measured"][key] += delta
            check(bool(module.row_problems(data["models"])),
                  f"{program}: a {key} the cells do not give was not reported")
        missing_id = next(i for i in ids if i not in removed.get(program, {}))
        data = copy.deepcopy(catalogue.load())
        data["models"] = [e for e in data["models"] if e["id"] != missing_id]
        check(bool(module.row_problems(data["models"])),
              f"{program}: a missing {missing_id} row was not reported")
        check(not module.row_problems(catalogue.load()["models"]),
              f"{program}: the shipped rows are reported as differing")
        real = module.load

        def tampered(path, real=real, module=module):
            blob = real(path)
            if path == module.SCORED:
                counted = next(c for c in blob if not c["excluded"])
                counted["lost"] = counted.get("lost", 0) + 1
            return blob

        module.load = tampered
        try:
            found, _said = module.score_problems()
            check(bool(found), f"{program}: a scored cell the raw runs do not give "
                               f"was not reported")
        finally:
            module.load = real
    check(not matrix_figures.row_problems(catalogue.load()["models"]),
          "matrix_figures: claude-opus-5 missing from the card by ruling must not fire "
          "(REMOVED_FROM_CARD)")


def test_the_matrix_check_only_fires_on_rows_it_still_owns() -> None:
    """matrix_figures.py forms every row in ROWS for the history
    (including `claude-sonnet-5` and `claude-haiku-4-5`, dropped from
    `EARLY_ROWS` above), but checks against catalogue.json only the
    ones catalogue.json's own `measured.derived_by` still names to it. Must
    not fire: the shipped catalogue's `claude-sonnet-5` row, now
    `tests/lineup_figures.py`'s and read differently from what this run's own
    cells give it, and `claude-opus-5`, removed from the card entirely
    by ruling rather than reattributed (`REMOVED_FROM_CARD`). Must fire:
    `claude-sonnet-5` reattributed to this script, still carrying the
    lineup's figures, and `gpt-5.6-terra`, still attributed here and not in
    `REMOVED_FROM_CARD`, missing from the card."""
    import copy
    import matrix_figures
    check(not matrix_figures.row_problems(catalogue.load()["models"]),
          "matrix_figures.py flags a row tests/lineup_figures.py now owns, or wrongly "
          "flags claude-opus-5 missing")
    data = copy.deepcopy(catalogue.load())
    entry = next(e for e in data["models"] if e["id"] == "claude-sonnet-5")
    entry["measured"]["derived_by"] = str(entry["measured"]["derived_by"]).replace(
        "tests/lineup_figures.py", "tests/matrix_figures.py")
    check(bool(matrix_figures.row_problems(data["models"])),
          "a row reattributed to matrix_figures.py with a figure the cells do not give "
          "was not reported")
    data = copy.deepcopy(catalogue.load())
    data["models"] = [e for e in data["models"] if e["id"] != "gpt-5.6-terra"]
    check(bool(matrix_figures.row_problems(data["models"])),
          "a row this script still owns, missing from the card and not in "
          "REMOVED_FROM_CARD, was not reported")


# The release benchmark's rows: five model rows and all four
# command routes, `derived_by tests/lineup_figures.py`. fable-sub is not a
# headline row: its figures are the side comparison against
# opus-5.5-sub, checked the same way through `lineup_figures.catalogue_problems`.
# claude-opus joined later: until then its route stayed pinned to the
# 2026-09-24 run (see subscription_figures.py's module docstring for what
# superseded it and why).
LINEUP_MODELS = ("claude-opus-5-5", "claude-sonnet-5", "claude-haiku-4-5",
                 "gpt-6-sol", "gpt-6-luna")
LINEUP_ROUTES = ("claude-sonnet", "claude-haiku", "claude-opus", "claude-fable")


def test_the_lineup_rows_are_what_their_records_say() -> None:
    """The command `derived_by` names, run as a command, over the
    committed release benchmark (arms/2026-09-27/lineup/)."""
    import subprocess
    data = catalogue.load()
    for row_id in LINEUP_MODELS:
        entry = next((e for e in data["models"] if e["id"] == row_id), None)
        check(entry is not None and "tests/lineup_figures.py --check" in
              str((entry.get("measured") or {}).get("derived_by")),
              f"{row_id}: derived_by does not name the command this test runs")
    for route_id in LINEUP_ROUTES:
        entry = next((e for e in data["command_routes"] if e["route"] == route_id), None)
        check(entry is not None and "tests/lineup_figures.py --check" in
              str((entry.get("measured") or {}).get("derived_by")),
              f"{route_id}: derived_by does not name the command this test runs")
    run = subprocess.run([sys.executable, str(ROOT / "tests" / "lineup_figures.py"),
                          "--check"], cwd=ROOT, capture_output=True, text=True)
    check(run.returncode == 0,
          f"tests/lineup_figures.py --check exited {run.returncode}: "
          f"{(run.stdout + run.stderr).strip()[-600:]}")


def test_the_lineup_check_fires_on_a_changed_figure() -> None:
    """Must-fire: a published figure the release benchmark does not
    give, on a model row and on a route, and a row or route missing entirely."""
    import copy
    import lineup_figures
    figures = lineup_figures.load(lineup_figures.EVIDENCE / "figures.json")
    check(not lineup_figures.catalogue_problems(catalogue.load(), figures),
          "the shipped lineup rows are reported as differing")
    data = copy.deepcopy(catalogue.load())
    entry = next(e for e in data["models"] if e["id"] == "claude-opus-5-5")
    entry["measured"]["silent_loss"] += 1
    check(bool(lineup_figures.catalogue_problems(data, figures)),
          "a published model silent_loss the release benchmark does not give was not "
          "reported")
    data = copy.deepcopy(catalogue.load())
    route = next(e for e in data["command_routes"] if e["route"] == "claude-sonnet")
    route["measured"]["deviations"] += 1
    check(bool(lineup_figures.catalogue_problems(data, figures)),
          "a published route deviations the release benchmark does not give was not "
          "reported")
    data = copy.deepcopy(catalogue.load())
    # claude-opus joined the checked routes once its own resolved_model
    # caught up with its alias.
    opus = next(e for e in data["command_routes"] if e["route"] == "claude-opus")
    opus["measured"]["silent_loss"] += 1
    check(bool(lineup_figures.catalogue_problems(data, figures)),
          "a published claude-opus silent_loss the release benchmark does not give "
          "was not reported")
    data = copy.deepcopy(catalogue.load())
    fable = next(e for e in data["command_routes"] if e["route"] == "claude-fable")
    fable["measured"]["usd_per_merge"] = 0.0
    check(bool(lineup_figures.catalogue_problems(data, figures)),
          "a command route priced per call was not reported")
    data = copy.deepcopy(catalogue.load())
    data["models"] = [e for e in data["models"] if e["id"] != "gpt-6-luna"]
    check(bool(lineup_figures.catalogue_problems(data, figures)),
          "a missing gpt-6-luna row was not reported")


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_catalogue_offline" \
                and callable(function):
            function()
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    n = len(catalogue.models())
    print(f"catalogue: {checks} checks pass over {n} shipped model(s), "
          f"schema_version {catalogue.load()['schema_version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
