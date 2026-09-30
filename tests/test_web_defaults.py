#!/usr/bin/env python3
"""Saved defaults: a person's run settings, kept on the server.

`GET`, `PUT` and `DELETE /api/v1/defaults`, driven over real sockets the way
`tests/test_web_accounts.py` drives the account routes, and read back out of
real response bodies and real files. Every check that can be seeded is: the
break it is written against is put into the shipped code for the length of one
call, and the check has to go red over it. A detector that stays green over
its own defect is decoration.

What is held:

  - a saved set comes back exactly as it was saved, and a delete forgets it;
  - every field is checked against this server: an unknown key, a level it
    does not offer, a model nobody lists and an oversize body are refused;
  - one person never reads, overwrites or deletes another's;
  - a server with no account store keeps one set for its single user;
  - every verb needs a session, a same-origin request and a JSON body;
  - the file is `0600` in a `0700` directory, as the credentials file is, and
    a wider one is refused rather than trusted;
  - a saved model no longer offered is dropped and named, never replaced, and
    the file keeps it for the day it is offered again;
  - effort is kept only beside a command route that takes it;
  - a saved effort beside a single-level route (Haiku) is
    dropped too, but silently -- not named, because the field was never
    applicable rather than gone;
  - the page saves only after the server accepted the run, and the box
    starts unticked.

Run with `python3 tests/test_web_defaults.py`, or collect with pytest.
"""

from __future__ import annotations

import contextlib
import json
import os
import stat
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless.web import accounts, api, credentials, defaults, server  # noqa: E402

from test_web_accounts import (ALICE_PASSWORD, BOB_PASSWORD, MEMBER,  # noqa: E402
                               OPERATOR, P, Deployment, as_json, code_of,
                               environment, request)

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


PROVIDER = "self-hosted"
# An address nothing listens on: the listing below is written straight into
# the credentials file, so no request is ever made to it.
ADDRESS = "http://127.0.0.1:9"
LISTED = ("test-model", "other-model")

# A full set, in the shape the page sends.
FULL = {
    "model": {"kind": "listed", "id": "other-model", "endpoint": PROVIDER},
    "window": 32768,
    "fidelity": "mid",
    "verify_depth": "coverage",
    "loss_budget": 0.05,
    "title_policy": "keep-base",
}
# A second one, different in every field, for the isolation checks.
OTHER = {
    "model": {"kind": "catalogue", "id": "qwen3-8b"},
    "check_model": {"kind": "catalogue", "id": "qwen3.8-27b-fp8"},
    "fidelity": "high",
    "verify_depth": "full",
    "loss_budget": 0.0,
    "title_policy": "choose-best",
}


@contextlib.contextmanager
def patched(owner, name: str, value):
    """`owner.name` replaced for the body only: one seeded break at a time."""
    before = getattr(owner, name)
    setattr(owner, name, value)
    try:
        yield
    finally:
        setattr(owner, name, before)


def listing_environ() -> dict:
    """The environment a server needs to count the self-hosted endpoint as set."""
    return {credentials.url_env(PROVIDER): ADDRESS}


@contextlib.contextmanager
def deployment():
    """A tenanted server, the operator and a member signed in, one endpoint listed."""
    with environment(), Deployment(environ=listing_environ()) as live:
        live.keys.set_endpoint(PROVIDER, ADDRESS, models=LISTED)
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        yield live, alice, bob


def put(live, who, payload, **headers):
    sent = {**who, **headers}
    return request(live.url(f"{P}/defaults"), method="PUT", payload=payload,
                   headers=sent)


def get(live, who) -> dict:
    status, _, body = request(live.url(f"{P}/defaults"), headers=who)
    payload = as_json(body)
    return payload if status == 200 and isinstance(payload, dict) else {"status": status}


def delete(live, who):
    return request(live.url(f"{P}/defaults"), method="DELETE", headers=who)


def record_of(live, username: str):
    return live.accounts.get(username)


# --------------------------------------------------------------------------
# the round trip
# --------------------------------------------------------------------------


def round_trip_problems(live, who) -> list[str]:
    found = []
    status, _, body = put(live, who, FULL)
    if status != 200:
        found.append(f"a full set was refused: {status} {body[:200]!r}")
    got = get(live, who)
    if got.get("defaults") != FULL or got.get("saved") is not True or got.get("dropped"):
        found.append(f"the set did not come back as saved: {got}")
    if delete(live, who)[0] != 204:
        found.append("the delete did not answer 204")
    after = get(live, who)
    if after.get("saved") is not False or after.get("defaults"):
        found.append(f"the set survived its delete: {after}")
    return found


def test_a_saved_set_comes_back_as_it_was_saved() -> None:
    """Must not fire as shipped; must fire when the write does nothing."""
    with deployment() as (live, alice, bob):
        for who, name in ((alice, "the operator"), (bob, "a member")):
            problems = round_trip_problems(live, who)
            check(not problems, f"round trip for {name}: {problems}")
        with patched(defaults.Store, "write", lambda self, clean: None):
            check(bool(round_trip_problems(live, bob)),
                  "must fire: the round trip passed over a write that stores nothing")


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------

BAD = {
    "an unknown key": {**FULL, "colour": "blue"},
    "an unknown key inside the model": {**FULL, "model": {**FULL["model"], "url": "x"}},
    "a fidelity level this server does not offer": {**FULL, "fidelity": "verbose"},
    "a depth this server does not offer": {**FULL, "verify_depth": "deep"},
    "a title policy this server does not offer": {**FULL, "title_policy": "invent"},
    "a ceiling above 1": {**FULL, "loss_budget": 1.5},
    "a ceiling as a string": {**FULL, "loss_budget": "0.1"},
    "a ceiling as a boolean": {**FULL, "loss_budget": True},
    "a catalogue id nobody has": {"model": {"kind": "catalogue", "id": "gpt-9-imaginary"}},
    "a catalogue row on an endpoint nobody set": {"model": {"kind": "catalogue", "id": "claude-sonnet-5"}},
    "a name the endpoint does not list": {"model": {"kind": "listed", "id": "gone", "endpoint": PROVIDER}},
    "a typed id with a space": {"model": {"kind": "typed", "id": "a model", "endpoint": ""}},
    "a typed id sent to a provider with no endpoint": {"model": {"kind": "typed", "id": "m", "endpoint": "openai"}},
    "a model kind that does not exist": {"model": {"kind": "url", "id": "x"}},
    "effort beside a model that is not a route": {**FULL, "effort": "high"},
    "a window with no model": {"window": 32768},
    "a window below the bound": {**FULL, "window": 12},
    "a command route nobody configured": {"model": {"kind": "route", "id": "claude-opus"}},
    "a check model beside a typed id": {"model": {"kind": "typed", "id": "m", "endpoint": ""},
                                        "check_model": {"kind": "catalogue", "id": "qwen3-8b"}},
    "not an object": ["fidelity", "mid"],
}


def validation_problems(live, who) -> list[str]:
    found = []
    for label, payload in BAD.items():
        status, _, body = put(live, who, payload)
        if status != 400:
            found.append(f"{label} was answered {status} {body[:160]!r}")
    big = {"model": {"kind": "typed", "id": "m" * 5000, "endpoint": ""}}
    status, _, body = put(live, who, big)
    if status != 413:
        found.append(f"an oversize body was answered {status}")
    return found


def test_every_field_is_checked_against_this_server() -> None:
    """Must fire on every bad body; must not fire on a good one; seeded."""
    with deployment() as (live, _alice, bob):
        problems = validation_problems(live, bob)
        check(not problems, f"refusals missing: {problems}")
        # Must not fire: every good shape is accepted.
        for good in (FULL, OTHER, {"fidelity": "off"}, {},
                     {"model": {"kind": "typed", "id": "Qwen/Qwen3.8-27B-FP8",
                                "endpoint": PROVIDER}, "window": 4096}):
            status, _, body = put(live, bob, good)
            check(status == 200, f"a good set was refused: {good} {status} {body[:200]!r}")
        # Refused, and the code is the one the page branches on.
        status, _, body = put(live, bob, BAD["an unknown key"])
        check(code_of(body) == "bad_defaults", f"the refusal's code is {code_of(body)!r}")
        # Seeded: a check that accepts anything.
        with patched(defaults, "check", lambda payload, offer: dict(payload)):
            check(len(validation_problems(live, bob)) >= len(BAD) - 1,
                  "must fire: the validation checks passed over a server that "
                  "accepts every field")


def test_a_dropped_model_takes_what_depends_on_it() -> None:
    """`sift` names the model, and the window and effort that belonged to it."""
    offer = defaults.Offer(routes={"claude-opus": ("low", "high")},
                           fidelity=("mid",), depths=("full",), titles=("keep-base",))
    kept, dropped = defaults.sift(
        {"model": {"kind": "route", "id": "claude-opus"}, "effort": "high",
         "fidelity": "mid"}, offer)
    check(kept == {"model": {"kind": "route", "id": "claude-opus"},
                   "effort": "high", "fidelity": "mid"} and dropped == [],
          f"must not fire: an offered route and its effort were dropped: {kept} {dropped}")
    gone = defaults.Offer(routes={}, fidelity=("mid",), depths=("full",),
                          titles=("keep-base",))
    kept, dropped = defaults.sift(
        {"model": {"kind": "route", "id": "claude-opus"}, "effort": "high",
         "fidelity": "mid"}, gone)
    check(kept == {"fidelity": "mid"}
          and [d["field"] for d in dropped] == ["model", "effort"],
          f"must fire: a route no longer offered kept its effort: {kept} {dropped}")
    # An effort level the route no longer takes is dropped on its own.
    fewer = defaults.Offer(routes={"claude-opus": ("low",)})
    kept, dropped = defaults.sift({"model": {"kind": "route", "id": "claude-opus"},
                                   "effort": "high"}, fewer)
    check("model" in kept and dropped == [{"field": "effort", "value": "high"}],
          f"a level the route stopped taking was not named: {kept} {dropped}")


def test_effort_beside_a_single_level_route_is_dropped_silently() -> None:
    """A stored effort beside Haiku is not applicable, not gone.

    Must fire (silent): `single_level_routes` names the route, its stored
    `effort` is refused by `_one` exactly as `fewer`'s is above, and `sift`
    keeps the model but neither keeps the level nor names it in `dropped`.
    Must not fire: an ordinary route whose levels merely narrowed (not in
    `single_level_routes`) still gets the named, visible drop `fewer` above
    holds -- the exemption is keyed by the flag, not by an empty tuple alone.
    """
    single = defaults.Offer(routes={"claude-haiku": ()},
                            single_level_routes=frozenset({"claude-haiku"}))
    kept, dropped = defaults.sift(
        {"model": {"kind": "route", "id": "claude-haiku"}, "effort": "high"}, single)
    check(kept == {"model": {"kind": "route", "id": "claude-haiku"}} and dropped == [],
          f"must fire: a single-level route's stored effort was named as dropped: "
          f"{kept} {dropped}")
    not_flagged = defaults.Offer(routes={"claude-haiku": ()})
    kept, dropped = defaults.sift(
        {"model": {"kind": "route", "id": "claude-haiku"}, "effort": "high"}, not_flagged)
    check("model" in kept and dropped == [{"field": "effort", "value": "high"}],
          f"must not fire: a route with no levels and no single_level flag "
          f"still names its dropped effort: {kept} {dropped}")


# --------------------------------------------------------------------------
# isolation
# --------------------------------------------------------------------------


def isolation_problems(live, alice, bob) -> list[str]:
    found = []
    for who in (alice, bob):
        delete(live, who)
    put(live, alice, FULL)
    if get(live, bob).get("saved"):
        found.append("a member read the operator's defaults")
    put(live, bob, OTHER)
    if get(live, alice).get("defaults") != FULL:
        found.append("a member's save overwrote the operator's")
    if get(live, bob).get("defaults") != OTHER:
        found.append("the member's own save did not come back")
    delete(live, bob)
    if get(live, alice).get("defaults") != FULL:
        found.append("a member's delete removed the operator's")
    return found


def test_one_person_never_reads_or_overwrites_anothers() -> None:
    """Must not fire as shipped; must fire when the file ignores whose it is."""
    with deployment() as (live, alice, bob):
        problems = isolation_problems(live, alice, bob)
        check(not problems, f"isolation: {problems}")
        # Each file under its own account's directory, and never the shared root.
        put(live, bob, OTHER)
        for username in (OPERATOR, MEMBER):
            record = record_of(live, username)
            path = live.root / accounts.USERS_DIR / record.id / defaults.FILE_NAME
            check(path.is_file(), f"{username}'s defaults are not at {path}")
        check(not (live.root / defaults.FILE_NAME).exists(),
              "a tenanted server wrote a defaults file at the shared root")
        # A request cannot name a file: there is no path segment to name one.
        status, _, _ = request(live.url(f"{P}/defaults/{record_of(live, OPERATOR).id}"),
                               headers=bob)
        check(status == 404, f"a defaults path with an id in it answered {status}")

        def shared(self, record, file_name):
            return self.root / file_name
        with patched(accounts.Directory, "defaults_path", shared):
            check(bool(isolation_problems(live, alice, bob)),
                  "must fire: isolation passed over one file for everybody")


# --------------------------------------------------------------------------
# a server with no accounts
# --------------------------------------------------------------------------


def test_a_server_with_no_accounts_keeps_one_set() -> None:
    with environment(), tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        keys = credentials.Credentials(root / "credentials.json")
        keys.set_endpoint(PROVIDER, ADDRESS, models=LISTED)
        built = server.build(port=0, keys=keys, work_dir=root / "work",
                             environ=listing_environ())
        thread = server.background(built)
        base = f"http://127.0.0.1:{built.port}{P}/defaults"
        try:
            status, _, body = request(base, method="PUT", payload=FULL)
            check(status == 200, f"no-accounts save: {status} {body[:200]!r}")
            got = as_json(request(base)[2]) or {}
            check(got.get("defaults") == FULL, f"no-accounts round trip: {got}")
            path = root / defaults.FILE_NAME
            check(path.is_file(), "a server with no accounts did not keep its set "
                                  "beside the credentials file")
            check(not (root / accounts.USERS_DIR).exists(),
                  "a server with no accounts made a users directory")
            check(request(base, method="DELETE")[0] == 204 and not path.exists(),
                  "the no-accounts delete left the file")
        finally:
            built.shutdown()
            built.server_close()
            built.store.close()
            thread.join(timeout=5)


# --------------------------------------------------------------------------
# authentication and the CSRF defence
# --------------------------------------------------------------------------


def gate_problems(live, bob) -> list[str]:
    found = []
    for method in ("GET", "PUT", "DELETE"):
        status, _, body = request(live.url(f"{P}/defaults"), method=method,
                                  payload=FULL if method == "PUT" else None)
        if status != 401:
            found.append(f"{method} with no session answered {status}")
    evil = {"Origin": "http://evil.example"}
    status, _, _ = put(live, bob, FULL, **evil)
    if status != 403:
        found.append(f"a cross-origin PUT answered {status}")
    status, _, _ = request(live.url(f"{P}/defaults"), method="DELETE",
                           headers={**bob, **evil})
    if status != 403:
        found.append(f"a cross-origin DELETE answered {status}")
    status, _, _ = request(live.url(f"{P}/defaults"), method="PUT",
                           payload=FULL, headers={**bob, "Content-Type": "text/plain"})
    if status != 415:
        found.append(f"a PUT that is not JSON answered {status}")
    return found


def test_every_verb_needs_a_session_and_a_same_origin_json_body() -> None:
    """Must fire with no session, a foreign origin or a form body; seeded twice."""
    with deployment() as (live, _alice, bob):
        problems = gate_problems(live, bob)
        check(not problems, f"the gate: {problems}")
        own = {"Origin": live.base}
        check(put(live, bob, FULL, **own)[0] == 200,
              "must not fire: a same-origin JSON save with a session was refused")
        with patched(api, "check_origin", lambda headers: None):
            check(any("cross-origin" in p for p in gate_problems(live, bob)),
                  "must fire: the gate passed with the origin check removed")
        with patched(api, "check_content_type", lambda headers: None):
            check(any("not JSON" in p for p in gate_problems(live, bob)),
                  "must fire: the gate passed with the content-type check removed")


# --------------------------------------------------------------------------
# the file
# --------------------------------------------------------------------------


def mode_of(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


def test_the_file_is_as_private_as_the_credentials_file() -> None:
    """0600 in 0700, like `credentials.json`; a wider file is refused, seeded."""
    with deployment() as (live, _alice, bob):
        put(live, bob, FULL)
        record = record_of(live, MEMBER)
        path = live.root / accounts.USERS_DIR / record.id / defaults.FILE_NAME
        # The member's own credentials file, written by the credentials code,
        # in the same directory: the two must agree, measured, not assumed.
        live.built.api.directory.own(record.id).set_endpoint(
            PROVIDER, ADDRESS, models=LISTED)
        keys_path = live.built.api.directory.path_for(record.id)
        check(mode_of(path) == mode_of(keys_path) == 0o600,
              f"defaults {mode_of(path):04o}, credentials {mode_of(keys_path):04o}; "
              f"both must be 0600")
        check(mode_of(path.parent) == credentials.DIR_MODE == 0o700,
              f"the directory is {mode_of(path.parent):04o}")
        check(get(live, bob).get("saved") is True, "must not fire: a 0600 file was refused")
        os.chmod(path, 0o644)
        status, _, body = request(live.url(f"{P}/defaults"), headers=bob)
        check(status == 409 and code_of(body) == "bad_defaults",
              f"must fire: a 0644 defaults file was read: {status} {body[:160]!r}")
        # A save replaces it at 0600.
        check(put(live, bob, FULL)[0] == 200 and mode_of(path) == 0o600,
              f"a save did not put the file back at 0600: {mode_of(path):04o}")
        # Seeded: a writer that leaves the file wider than the credentials file.
        with patched(defaults, "FILE_MODE", 0o644):
            put(live, bob, OTHER)
            check(mode_of(path) != mode_of(keys_path),
                  "must fire: the mode probe could not see a wider file")


# --------------------------------------------------------------------------
# a model that is gone
# --------------------------------------------------------------------------


def test_a_saved_model_no_longer_offered_is_dropped_and_named() -> None:
    with deployment() as (live, _alice, bob):
        put(live, bob, FULL)
        before = get(live, bob)
        check(before.get("dropped") == [] and before["defaults"].get("model"),
              f"must not fire: an offered model was dropped: {before}")
        live.keys.set_models(PROVIDER, ("test-model",))
        after = get(live, bob)
        named = [entry["field"] for entry in after.get("dropped", [])]
        check(named == ["model", "window"]
              and after["dropped"][0]["value"] == "other-model",
              f"must fire: the model gone from the endpoint was not named: {after}")
        check("model" not in after.get("defaults", {})
              and after["defaults"].get("fidelity") == "mid",
              f"the dropped model was kept, or took the rest with it: {after}")
        # The file is not rewritten: offered again, it is used again.
        live.keys.set_models(PROVIDER, LISTED)
        again = get(live, bob)
        check(again.get("dropped") == [] and again["defaults"] == FULL,
              f"a model listed again was not restored: {again}")


# --------------------------------------------------------------------------
# effort, beside a command route
# --------------------------------------------------------------------------


def test_effort_is_kept_only_beside_a_route_that_takes_it() -> None:
    from test_web_server import claude_routes
    # `claude_routes` builds with no credentials object, so `Api` makes one at
    # the default path: pointed into a temporary directory here, or this test
    # would write the defaults file of whoever runs the suite.
    with environment(), tempfile.TemporaryDirectory() as raw:
        os.environ["XDG_CONFIG_HOME"] = raw
        os.environ[credentials.PATH_ENV] = str(Path(raw) / "credentials.json")
        with claude_routes() as (built, _calls):
            where = built.api.defaults_store(None).path
            check(where.is_relative_to(raw), f"the route test would write {where}")
            if where.is_relative_to(raw):
                effort_round_trip(built.url + P)


def effort_round_trip(base: str) -> None:
    """A route and its level round trip; a level or a check model beside it do not."""
    routes = (as_json(request(f"{base}/config")[2]) or {})["commands"]["routes"]
    taking = [r for r in routes if (r.get("effort") or {}).get("levels")]
    plain = [r for r in routes if not (r.get("effort") or {}).get("levels")]
    check(bool(taking), "the fake routes offer no route that takes effort")
    if taking:
        route = taking[0]
        level = route["effort"]["levels"][-1]
        body = {"model": {"kind": "route", "id": route["id"]}, "effort": level}
        status, _, raw = request(f"{base}/defaults", method="PUT", payload=body)
        check(status == 200, f"a route and its level were refused: {status} {raw[:200]!r}")
        got = as_json(request(f"{base}/defaults")[2]) or {}
        check(got.get("defaults") == body, f"route round trip: {got}")
        bad = dict(body, effort="ludicrous")
        check(request(f"{base}/defaults", method="PUT", payload=bad)[0] == 400,
              "a level the route does not take was saved")
        split = dict(body, check_model={"kind": "catalogue", "id": "qwen3-8b"})
        check(request(f"{base}/defaults", method="PUT", payload=split)[0] == 400,
              "a check model beside a command route was saved")
    if plain:
        body = {"model": {"kind": "route", "id": plain[0]["id"]}, "effort": "high"}
        check(request(f"{base}/defaults", method="PUT", payload=body)[0] == 400,
              "effort beside a route that takes none was saved")


# --------------------------------------------------------------------------
# the page
# --------------------------------------------------------------------------

APP_JS = ROOT / "src" / "llossless" / "web" / "static" / "app.js"
INDEX = ROOT / "src" / "llossless" / "web" / "static" / "index.html"


def function_body(js: str, name: str) -> str:
    start = js.index(f"function {name}(")
    end = js.index("\n}\n", start)
    return js[start:end]


def save_order_problems(js: str) -> list[str]:
    """The save must come after the accepted POST, inside the `try`."""
    body = function_body(js, "submit")
    found = []
    post = body.find('await sendJson("POST", ROUTES.runs')
    save = body.find("saveDefaults(keep)")
    catch = body.find("} catch (error) {")
    if post < 0 or save < 0 or catch < 0:
        return ["submit no longer posts, saves or catches where this looks"]
    if not post < save < catch:
        found.append("the defaults are saved before the server accepted the run")
    if "currentDefaults()" not in body[:post]:
        found.append("the settings are not read at the click, before the POST")
    return found


def test_the_page_saves_only_after_the_run_is_accepted() -> None:
    js = APP_JS.read_text(encoding="utf-8")
    check(not save_order_problems(js), f"the save: {save_order_problems(js)}")
    seeded = js.replace("    if (keep) void saveDefaults(keep);\n", "", 1).replace(
        "  setRunning(true);\n  say(\"busy\", t(\"word.sending\")",
        "  if (keep) void saveDefaults(keep);\n  setRunning(true);\n  say(\"busy\", t(\"word.sending\")", 1)
    check(seeded != js and bool(save_order_problems(seeded)),
          "must fire: a save before the POST passed")
    html = INDEX.read_text(encoding="utf-8")
    box = html[html.index('data-cc="save-defaults"') - 40:html.index('data-cc="save-defaults"') + 40]
    check("checked" not in box, f"the save-defaults box is ticked by default: {box!r}")
    # Ticked still once a save worked (operator, 2026-09-28): the
    # box says the current settings are the saved defaults, and it unticks only
    # when a setting moves away from them (`syncSaveDefaultsChecked`).
    untick = 'input("save-defaults").checked = false'
    check(untick not in function_body(js, "saveDefaults"),
          "a successful save unticks the box, although the settings are now the defaults")
    check("function syncSaveDefaultsChecked" in js,
          "nothing re-derives the box from the saved defaults")
    body = function_body(js, "saveDefaults")
    seeded = js.replace(body, body.replace("{", "{\n  " + untick + ";", 1), 1)
    check(seeded != js and untick in function_body(seeded, "saveDefaults"),
          "must fire: a save that unticks the box passed")


# --------------------------------------------------------------------------


def test_web_defaults_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_defaults_offline" \
                and callable(function):
            try:
                function()
            except Exception as raised:  # noqa: BLE001 - one failure, not all
                failures.append(f"{name} raised {type(raised).__name__}: {raised}")
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web defaults: {checks} checks pass over the saved-defaults routes, "
          f"their file, their isolation and the page's save")
    return 0


if __name__ == "__main__":
    sys.exit(main())
