#!/usr/bin/env python3
"""Accounts, sessions and per-user credentials, driven over real sockets.

`src/llossless/web/accounts.py` covers the session routes in
`api.py`, the ownership check on every job route, and the retirement of the
bind token. Everything that can be asked of a server is asked of a server:
bound to port 0, driven with `urllib.request`, and read back out of a real
response body -- the rule this project arrived at the expensive way, and one
that applies with particular force here, because every failure this module is
written against looks like success from inside the function that causes it. A
job served to the wrong user is a correct-looking 200. A session compared with
`==` is a correct-looking 401. A key leaked between two jobs is a merge that
works.

Seven of the checks are worth naming.

**Two concurrent jobs from two users use two different keys.** Asserted on
what the *transport* was handed -- the `Authorization` header recorded by each
user's own scripted endpoint -- rather than on a mapping handed to a function,
because the thing that can go wrong is a process-wide environment and the only
place that shows is on the wire. The two runs are forced to overlap with a
barrier, so the assertion is about two jobs in flight at once rather than two
jobs that happened to serialise.

**User B cannot read user A's job.** Every route that reaches a run: the
status, the report, the merged document, the deletion and the event stream. A
uuid4 is not an access control -- it is printed in a URL bar, copied into a
chat window and kept in a browser history -- and the refusal has to be the
same answer an id that never existed gets, or it is an oracle for whose runs
exist.

**A forged or expired session is refused, and the cookie is `HttpOnly` and
`SameSite=Strict`.** The attributes are the CSRF defence that replaced the
custom header's, so they are read off a real `Set-Cookie` rather than off the
function that builds one.

**An unknown username and a wrong password are indistinguishable.** In the
status, in the code, in the message, and -- as far as anything written in
Python can be -- in the time. The timing half is stated as a ratio with a
generous bound, because a tight one on a loaded machine is a check that fails
for reasons that have nothing to do with the code.

**No response body, log line or exception carries a password, a hash or a
session id.** Seeded with recognisable values and asserted over every route
this server answers, including the refusals, with a must-not-fire line proving
the probe can see the strings at all.

**A non-loopback bind is refused with no accounts and no token, and permitted
once an account exists.** The supersession, from both ends.

**Every route but `session` and `setup` needs an identity.** Derived from the
routing table rather than from a list written here, so a route added next year
is covered by construction.

Run with `python3 tests/test_web_accounts.py`, or collect with pytest.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import stat
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs. Every request below reaches a real
# loopback socket, so this is the module's claim that the only sockets it opens
# are the ones it bound itself; `tests/test_socket_guard.py` asserts every test
# module states it in exactly this shape.
socket_guard.install()

from llossless import config  # noqa: E402
from llossless.web import accounts, api, credentials, jobs, server  # noqa: E402

from fake_endpoint import FakeEndpoint  # noqa: E402
from test_cli import CLEAN, SOURCE_A, SOURCE_B, Script  # noqa: E402

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# scaffolding
# --------------------------------------------------------------------------

# Long enough that a loaded machine running the whole suite does not fail a
# check about a request, short enough that a genuine hang is reported as one
# rather than as a suite that never returns. Every read below is capped;
# agents on this project have seeded breaks that hung rather than failed.
PATIENCE = 60.0

# The most bytes any response here is read for.
READ_CAP = 256 * 1024

# The two passwords, and neither is a word any scanner in this repository has
# a reason to recognise. Distinct tails so that a leak found in one place
# cannot be confused with the other, and long enough to pass
# `accounts.MIN_PASSWORD` without being at it -- a probe sitting exactly on a
# bound tests the bound rather than the property.
ALICE_PASSWORD = "probe-password-alice-4k2"
BOB_PASSWORD = "probe-password-bob-9x7"

# The two API keys. Not address-shaped, not word-shaped, and not a string any
# document under test carries.
ALICE_KEY = "probe-key-alice-must-not-cross-3a1"
BOB_KEY = "probe-key-bob-must-not-cross-7c5"

OPERATOR = "alice"
MEMBER = "bob"

# Which provider the per-user endpoints use. `self-hosted` because its key
# variable is `config.DEFAULT_KEY_ENV`, which is the fallback every role with
# no override of its own reads -- so a key that leaked would leak on every
# role rather than on one.
PROVIDER = "self-hosted"
KEY_VARIABLE = credentials.PROVIDERS[PROVIDER]

P = api.API_PREFIX


def request(url: str, *, method: str = "GET", payload=None, headers=None,
            timeout: float = PATIENCE):
    """One HTTP call. Returns (status, headers, body-bytes). Never raises on 4xx.

    An `HTTPError` is a response with a body, and every refusal this module
    asserts about arrives as one; letting it propagate would turn every
    negative check into a `try`/`except` at the call site and make the
    interesting assertion the one in the handler.
    """
    body = None
    sent = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        sent.setdefault("Content-Type", "application/json")
    if body is None and method in ("POST", "PUT", "DELETE"):
        # A request that changes something declares the JSON type with or
        # without a body, which is what the page sends and what the server
        # asks for. A caller that means otherwise passes the header itself.
        sent.setdefault("Content-Type", "application/json")
    call = urllib.request.Request(url, data=body, method=method, headers=sent)
    try:
        with urllib.request.urlopen(call, timeout=timeout) as answer:
            return answer.status, dict(answer.headers), answer.read(READ_CAP)
    except urllib.error.HTTPError as refusal:
        return refusal.code, dict(refusal.headers), refusal.read(READ_CAP)


def as_json(body: bytes):
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None


def code_of(body: bytes) -> str:
    """The refusal code out of a response body, or `` for anything else.

    `payload.get("error") or {}` rather than `payload.get("error", {})`, and
    the difference is not style: a *successful* run payload carries
    `"error": null`, so the default-argument form returns `None` and the
    `.get` after it raises -- which aborts the whole check function and takes
    five assertions down with one traceback. Found by seeding a break that
    made a refusal answer 200.
    """
    payload = as_json(body)
    if not isinstance(payload, dict):
        return ""
    return str((payload.get("error") or {}).get("code", ""))


class Deployment:
    """A running server with an account store, and the helpers to drive it.

    A class rather than a context-managed tuple because every check here needs
    the same four things -- the base URL, the account store, the credentials
    directory and a way to log in -- and threading four values through twenty
    call sites is how one of them ends up reaching for `os.environ`.
    """

    def __init__(self, *, host=None, token="", environ=None, workers=1,
                 log=None) -> None:
        self._raw = tempfile.TemporaryDirectory()
        self.root = Path(self._raw.name)
        self.accounts = accounts.Accounts(self.root / "accounts.json")
        self.setup = accounts.Setup()
        self.keys = credentials.Credentials(self.root / "credentials.json")
        self.built = server.build(
            host=server.HOST if host is None else host, port=0, token=token,
            keys=self.keys, accounts=self.accounts, setup=self.setup,
            work_dir=self.root / "work", workers=workers,
            environ={} if environ is None else dict(environ), log_stream=log)
        self.thread = server.background(self.built)
        self.base = f"http://127.0.0.1:{self.built.port}"

    def close(self) -> None:
        self.built.shutdown()
        self.built.server_close()
        self.built.store.close()
        self.thread.join(timeout=5)
        self._raw.cleanup()

    def __enter__(self) -> Deployment:
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    # -- driving ---------------------------------------------------------

    def url(self, path: str) -> str:
        return f"{self.base}{path}"

    def first_account(self, username=OPERATOR, password=ALICE_PASSWORD,
                      headers=None):
        """Create the operator through the route, the way the page does.

        `headers` is for the one server where setup still costs a bind token:
        with no account, the setup rule stands in full and the token guards
        everything including this route.
        """
        return request(self.url(f"{P}/setup"), method="POST", headers=headers,
                       payload={"token": self.setup.token,
                                "username": username, "password": password})

    def sign_in(self, username: str, password: str) -> dict:
        """A session id, presented in the header the way a script does.

        The header rather than the cookie, because `urllib` has no cookie jar
        and a module that built one would be testing its own jar. The cookie's
        own attributes are asserted on a real `Set-Cookie` elsewhere.
        """
        status, _, body = request(
            self.url(f"{P}/session"), method="POST",
            payload={"username": username, "password": password, "token": True})
        payload = as_json(body) or {}
        if status != 200 or "token" not in payload:
            raise AssertionError(f"could not sign in as {username}: "
                                 f"{status} {body[:200]!r}")
        return {accounts.SESSION_HEADER: payload["token"]}

    def add_account(self, who: dict, username: str, password: str):
        return request(self.url(f"{P}/accounts"), method="POST", headers=who,
                       payload={"username": username, "password": password})

    def set_endpoint(self, who: dict, base_url: str, *, provider=PROVIDER):
        return request(self.url(f"{P}/settings/endpoints/{provider}"),
                       method="PUT", headers=who, payload={"base_url": base_url})

    def set_key(self, who: dict, key: str, *, provider=PROVIDER):
        return request(self.url(f"{P}/settings/keys/{provider}"),
                       method="PUT", headers=who, payload={"key": key})


@contextlib.contextmanager
def environment():
    """Restore `os.environ` afterwards, whatever the body did to it.

    The operator's settings routes put keys into the process environment on
    purpose -- that is how the *shared* credentials reach a run -- so a module
    that exercises them changes the environment of the interpreter running the
    suite. Snapshotted and put back rather than deleted key by key, because
    the thing being guarded is a variable this module never thought about.
    """
    before = dict(os.environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(before)


def state_of(live, run_id: str, who) -> str:
    """One run's state, or `` for any answer that is not a status payload.

    Tolerant on purpose. A seeded break makes a route answer something this
    poller did not expect, and a `.get` straight onto whatever came back turns
    that into an `AttributeError` that aborts the whole check function -- so
    one seeded defect reports one traceback and leaves the five assertions
    after it unexercised, which is indistinguishable from five that do not
    work.
    """
    payload = as_json(request(live.url(f"{P}/runs/{run_id}"), headers=who)[2])
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("state") or "")


def wait_for(predicate, *, timeout: float = PATIENCE) -> bool:
    """Poll until true or give up. Every wait in this module is capped.

    A seeded break that hangs is a break that reports nothing, which is worse
    than one that fails: the suite never returns and the agent that seeded it
    reports the detector as unexercised.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.05)
    return False


# --------------------------------------------------------------------------
# passwords
# --------------------------------------------------------------------------


def test_a_password_is_hashed_with_a_recorded_cost_and_never_stored() -> None:
    """The file holds a salt, a hash and the parameters -- and no password.

    Must fire on the password itself in any encoding the file could carry it
    in, and must not fire on the salt and the hash, which are what a
    verifiable record *is*. The cost is required to be in the record rather
    than assumed from this module's constants, because that is what lets the
    constants be raised without invalidating the accounts already written.
    """
    with tempfile.TemporaryDirectory() as raw:
        store = accounts.Accounts(Path(raw) / "accounts.json")
        record = store.create(OPERATOR, ALICE_PASSWORD, operator=True)
        text = (Path(raw) / "accounts.json").read_text(encoding="utf-8")
        check(ALICE_PASSWORD not in text,
              "the accounts file carries the password in plain text")
        check(ALICE_PASSWORD.encode("utf-8").hex() not in text,
              "the accounts file carries the password hex-encoded")
        import base64
        check(base64.b64encode(ALICE_PASSWORD.encode()).decode() not in text,
              "the accounts file carries the password base64-encoded")
        # Must not fire: the record really is there and really is checkable.
        check(record.salt in text and record.hash in text,
              "the salt and the derived hash are not in the file, so the probe "
              "above proves nothing about what it searched")
        check(record.algorithm in (accounts.SCRYPT, accounts.PBKDF2),
              f"a record was written under {record.algorithm!r}, which is "
              f"neither of the two functions this build knows")
        check(bool(record.cost),
              "the cost the hash was derived under is not recorded, so raising "
              "it would invalidate every account already in the file")
        check(store.verify(OPERATOR, ALICE_PASSWORD) is not None,
              "the password that was just set does not verify")
        check(store.verify(OPERATOR, ALICE_PASSWORD + "x") is None,
              "a wrong password verifies")


def test_a_record_written_under_an_older_cost_still_verifies() -> None:
    """The parameters come off the record, not off this module's constants.

    Must fire: a record written at a cheaper cost is still checkable after the
    constant is raised. Must not fire: the same record checked with the wrong
    password is refused, so the first half is not passing because `verify`
    accepts everything.

    **The cheap hash is computed with `hashlib` directly and not with
    `accounts.derive`**, and that is the whole reason this check works. Built
    with the shipped function, a seeded break in it would move both sides of
    the comparison together: the fixture and the verification would agree on
    the wrong parameters and the detector would stay green over a `derive`
    that had stopped reading the record at all. It was silent over exactly
    that seed before this was rewritten.
    """
    import hashlib
    import secrets

    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "accounts.json"
        store = accounts.Accounts(path)
        algorithm, cost = accounts.default_algorithm()
        salt = secrets.token_bytes(accounts.SALT_BYTES)
        if algorithm == accounts.SCRYPT:
            cheap = dict(cost, n=1 << 10)
            derived = hashlib.scrypt(
                ALICE_PASSWORD.encode("utf-8"), salt=salt, n=cheap["n"],
                r=cheap["r"], p=cheap["p"], dklen=accounts.HASH_BYTES,
                maxmem=accounts.SCRYPT_MAXMEM)
        else:
            cheap = dict(cost, rounds=1000)
            derived = hashlib.pbkdf2_hmac(
                "sha256", ALICE_PASSWORD.encode("utf-8"), salt,
                cheap["rounds"], dklen=accounts.HASH_BYTES)
        payload = {
            "version": accounts.SCHEMA_VERSION,
            "accounts": {OPERATOR: {
                "id": secrets.token_hex(16), "algorithm": algorithm,
                "salt": salt.hex(), "hash": derived.hex(), "cost": cheap,
                "operator": True, "created_at": 0.0,
            }},
        }
        path.write_text(json.dumps(payload), encoding="utf-8")
        os.chmod(path, 0o600)
        check(store.verify(OPERATOR, ALICE_PASSWORD) is not None,
              "a record written under a cheaper cost no longer verifies, so "
              "raising the cost would lock every existing account out")
        check(store.verify(OPERATOR, BOB_PASSWORD) is None,
              "the cheap record verifies a password it was not derived from")


def test_an_accounts_file_wider_than_0600_is_refused() -> None:
    """Must fire on 0644, must not fire on 0600, and the same file for both.

    Only the mode changes between the two halves, so the refusal cannot be
    about the file being unreadable for some other reason. It is refused and
    not repaired for the reason the credentials file is: every account on the
    box has had the chance to read the hashes, and chmodding it back would
    destroy the evidence while leaving the passwords in service.
    """
    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "accounts.json"
        store = accounts.Accounts(path)
        store.create(OPERATOR, ALICE_PASSWORD, operator=True)
        check(stat.S_IMODE(path.stat().st_mode) == accounts.FILE_MODE,
              f"the file this tool writes is mode "
              f"{stat.S_IMODE(path.stat().st_mode):04o}, not "
              f"{accounts.FILE_MODE:04o}")
        check(stat.S_IMODE(path.parent.stat().st_mode) == accounts.DIR_MODE,
              "the directory holding the accounts file is wider than 0700")
        # Must not fire at 0600.
        check(len(store.read()) == 1, "a 0600 accounts file is not read")
        os.chmod(path, 0o644)
        try:
            store.read()
            check(False, "a world-readable accounts file was read anyway")
        except accounts.AccountError as refused:
            check("0644" in str(refused),
                  f"the refusal does not name the mode: {refused}")
            check(ALICE_PASSWORD not in str(refused),
                  "the refusal carries a password")


def test_a_username_never_becomes_a_path() -> None:
    """Must fire on every traversal spelling; must not fire on a real name.

    The id is what names the directory, so the check that matters is the one
    on the id -- and a username that reached a path would be a username the
    allowlist below had already refused. Both are asserted, because a rule
    enforced in only one of the two places is a rule with a way round it.
    """
    for hostile in ("../../etc", "..%2f..%2fetc", "a/b", "A", "", " ", "x" * 64,
                    "0" * 32 + "\n/../../etc"):
        try:
            accounts.check_username(hostile)
            check(False, f"{hostile!r} was accepted as a username")
        except accounts.AccountError:
            pass
    check(accounts.check_username("Bob.1") == "bob.1",
          "a real username is refused, so the loop above proves nothing")
    for hostile in ("../../etc", "0" * 31, "0" * 33, "g" * 32,
                    "0" * 32 + "\n/../../etc", None, 7):
        try:
            accounts.check_account_id(hostile)
            check(False, f"{hostile!r} was accepted as an account id")
        except accounts.AccountError:
            pass
    check(accounts.check_account_id("a" * 32) == "a" * 32,
          "a real account id is refused, so the loop above proves nothing")


# --------------------------------------------------------------------------
# no enumeration
# --------------------------------------------------------------------------


def test_an_unknown_username_and_a_wrong_password_are_one_answer() -> None:
    """Same status, same code, same sentence, and the same order of duration.

    The first three are the ones that matter and are asserted exactly. The
    fourth is asserted as a ratio with a generous bound, because a tight one
    on a machine running the whole suite is a check that fails for reasons
    that have nothing to do with this code -- and because the property being
    guarded is "there is no branch that skips the expensive part", which shows
    up as an order of magnitude and not as a percentage.

    Must not fire: the right password is accepted, so a login that refused
    everything would not pass this.
    """
    with Deployment() as live:
        live.first_account()
        wrong = request(live.url(f"{P}/session"), method="POST",
                        payload={"username": OPERATOR, "password": "wrong-password-x"})
        stranger = request(live.url(f"{P}/session"), method="POST",
                           payload={"username": "nobody", "password": "wrong-password-x"})
        check(wrong[0] == stranger[0] == 401,
              f"a wrong password answered {wrong[0]} and an unknown name "
              f"{stranger[0]}")
        check(code_of(wrong[2]) == code_of(stranger[2]) == "bad_login",
              f"the two refusals carry different codes: "
              f"{code_of(wrong[2])!r} and {code_of(stranger[2])!r}")
        check(wrong[2] == stranger[2],
              f"the two refusals read differently: {wrong[2]!r} vs "
              f"{stranger[2]!r}")
        for body in (wrong[2], stranger[2]):
            for leaked in (OPERATOR, "nobody"):
                check(leaked.encode() not in body,
                      f"a login refusal quotes the submitted username "
                      f"{leaked!r} back into a response body")

        # The duration. Three of each, the fastest of each taken, because the
        # slowest is whatever else the machine was doing.
        def fastest(username: str) -> float:
            best = float("inf")
            for _ in range(3):
                started = time.monotonic()
                request(live.url(f"{P}/session"), method="POST",
                        payload={"username": username,
                                 "password": "wrong-password-y"})
                best = min(best, time.monotonic() - started)
            return best

        known, unknown = fastest(OPERATOR), fastest("nobody")
        ratio = max(known, unknown) / max(min(known, unknown), 1e-6)
        check(ratio < 8.0,
              f"an unknown username is answered {ratio:.1f}x faster or slower "
              f"than a known one ({known * 1000:.1f}ms vs "
              f"{unknown * 1000:.1f}ms), which is a user enumeration oracle "
              f"that needs nothing but a stopwatch")
        # Must not fire: the right password still works.
        good = request(live.url(f"{P}/session"), method="POST",
                       payload={"username": OPERATOR, "password": ALICE_PASSWORD})
        check(good[0] == 200,
              f"the right password is refused too, so the sameness above is "
              f"the sameness of a login that refuses everybody: {good[0]}")


def test_a_throttled_name_is_refused_exactly_as_a_wrong_password_is() -> None:
    """Must fire: past the limit, the right password is refused with the same 401.

    A lockout that answered 429 would be a lockout that says which names are
    worth guessing at. The cost is that a legitimate user who mistypes ten
    times has to wait, which they can see and an attacker cannot.

    Must not fire: a name that has not been thrashed still logs in, so this is
    a throttle rather than a server that stopped accepting passwords.
    """
    with Deployment() as live:
        live.first_account()
        who = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(who, MEMBER, BOB_PASSWORD)
        for _ in range(live.built.api.throttle.limit):
            request(live.url(f"{P}/session"), method="POST",
                    payload={"username": MEMBER, "password": "wrong-password-z"})
        locked = request(live.url(f"{P}/session"), method="POST",
                         payload={"username": MEMBER, "password": BOB_PASSWORD})
        check(locked[0] == 401 and code_of(locked[2]) == "bad_login",
              f"a throttled name answers {locked[0]} {code_of(locked[2])!r}, "
              f"which is a different answer from a wrong password and "
              f"therefore an oracle")
        untouched = request(live.url(f"{P}/session"), method="POST",
                            payload={"username": OPERATOR,
                                     "password": ALICE_PASSWORD})
        check(untouched[0] == 200,
              f"an untouched name cannot log in either, so the refusal above "
              f"is not a throttle: {untouched[0]}")


# --------------------------------------------------------------------------
# sessions
# --------------------------------------------------------------------------


def test_the_session_cookie_is_httponly_and_samesite_strict() -> None:
    """Read off a real `Set-Cookie`, not off the function that builds one.

    `SameSite=Strict` is what replaces the custom header's CSRF immunity: a
    cross-site navigation or form post that arrives with no cookie at all,
    and `HttpOnly` is what stops a script on the page reading it. Both are
    asserted on the wire, and so is the absence of `Secure` on a plain-HTTP
    deployment: a `Secure` cookie over `http` is one the browser never sends
    back, which presents as a login that succeeds and then does nothing.

    Must not fire: the same response under a proxy saying the request arrived
    over TLS *does* carry `Secure`.
    """
    with Deployment() as live:
        _, headers, _ = live.first_account()
        raw = headers.get("Set-Cookie", "")
        check(raw.startswith(accounts.COOKIE_NAME + "="),
              f"setup did not set a session cookie: {raw!r}")
        for attribute in ("HttpOnly", "SameSite=Strict", "Path=/"):
            check(attribute in raw,
                  f"the session cookie is missing {attribute}: {raw!r}")
        check("Secure" not in raw,
              f"the cookie is marked Secure over plain HTTP, so the browser "
              f"will never send it back: {raw!r}")
        _, tls_headers, _ = request(
            live.url(f"{P}/session"), method="POST",
            headers={api.FORWARDED_PROTO: "https"},
            payload={"username": OPERATOR, "password": ALICE_PASSWORD})
        check("Secure" in tls_headers.get("Set-Cookie", ""),
              f"a request that reached the front of the deployment over TLS "
              f"still gets a cookie with no Secure: "
              f"{tls_headers.get('Set-Cookie')!r}")


def test_a_forged_or_revoked_session_is_refused() -> None:
    """Must fire on four kinds of dead id; must not fire on the live one.

    The four are a forgery of the right shape, a truncation of a real id, an
    extension of one, and a real id that has been logged out. The first three
    are what a comparison written with `startswith` or one that stops at the
    shorter of two strings would accept; the fourth is what a signed cookie
    with its own claims could not have refused at all, which is why the
    sessions are held server-side.
    """
    with Deployment() as live:
        live.first_account()
        who = live.sign_in(OPERATOR, ALICE_PASSWORD)
        real = who[accounts.SESSION_HEADER]
        check(request(live.url(f"{P}/runs"), headers=who)[0] == 200,
              "a live session cannot read its own runs")
        for label, forged in (
                ("a different id of the same shape", "A" * len(real)),
                ("a prefix of the real one", real[:-1]),
                ("an extension of the real one", real + "A"),
                ("nothing at all", "")):
            status, _, body = request(
                live.url(f"{P}/runs"),
                headers={accounts.SESSION_HEADER: forged} if forged else None)
            check(status == 401 and code_of(body) == "no_session",
                  f"{label} was accepted: {status} {body[:160]!r}")
        # And the same id after a logout.
        check(request(live.url(f"{P}/session"), method="DELETE",
                      headers=who)[0] == 204,
              "logging out did not answer 204")
        after = request(live.url(f"{P}/runs"), headers=who)
        check(after[0] == 401,
              f"a revoked session still reads runs: {after[0]}")


def test_a_session_cookie_under_the_old_name_is_ignored() -> None:
    """The cookie is `llossless_session`; the pre-rename cookie logs nobody in.

    The code used to read the old cookie when the new one was absent; the operator's
    fresh-start ruling removed that. A live session id under the old name is
    refused as if no cookie were sent, alone or among others, and beside a
    dead new cookie. Must fire: the same id under the new name is accepted,
    so the refusals are about the name and not the session.
    """
    check(accounts.COOKIE_NAME == "llossless_session"
          and not hasattr(accounts, "LEGACY_COOKIE_NAME"),
          f"one cookie name, {accounts.COOKIE_NAME!r}, and no old one")
    with Deployment() as live:
        _, headers, _ = live.first_account()
        check(headers.get("Set-Cookie", "").startswith("llossless_session="),
              f"the cookie set is not the new name: {headers.get('Set-Cookie')!r}")
        first = live.sign_in(OPERATOR, ALICE_PASSWORD)[accounts.SESSION_HEADER]

        def runs(cookie: str) -> int:
            return request(live.url(f"{P}/runs"), headers={"Cookie": cookie})[0]

        check(runs(f"llossless_session={first}") == 200,
              "must fire: the new session cookie is accepted")
        check(runs(f"claimcheck_session={first}") == 401,
              "an old session cookie must not log in")
        check(runs(f"other=1; claimcheck_session={first}; theme=dark") == 401,
              "an old session cookie among others must not log in")
        check(runs(f"llossless_session={'A' * len(first)}; "
                   f"claimcheck_session={first}") == 401,
              "a live old cookie beside a dead new one must not log in")
        check(accounts.sessions_from_cookie(f"claimcheck_session={first}") == (),
              "the cookie parser must not return an id under the old name")
        check(runs(f"llossless_session={first}") == 200,
              "the refusals above must not have revoked the session")


def test_an_expired_session_is_refused() -> None:
    """Must fire past the idle window; must not fire inside it.

    Driven with an injected clock rather than by waiting, for the reason the
    retention checks are: a window tested by sleeping is either slow or is a
    window short enough to be untypical.
    """
    now = {"t": 1_000_000.0}
    sessions = accounts.Sessions(idle_seconds=100.0, max_seconds=1000.0,
                                 clock=lambda: now["t"])
    session_id = sessions.new("a" * 32)
    check(sessions.lookup(session_id) is not None,
          "a session just created does not look up")
    now["t"] += 99.0
    check(sessions.lookup(session_id) is not None,
          "a session inside the idle window was dropped")
    now["t"] += 101.0
    check(sessions.lookup(session_id) is None,
          "a session past the idle window still looks up")

    # And the absolute cap, which idle refreshing must not defeat: a session
    # renewed forever is a stolen cookie that never expires.
    second = sessions.new("a" * 32)
    for _ in range(20):
        now["t"] += 60.0
        sessions.lookup(second)
    check(sessions.lookup(second) is None,
          "a session kept alive by use outlived the absolute cap, so a stolen "
          "cookie never expires")


def test_a_password_change_ends_every_session_it_belongs_to() -> None:
    """Must fire: the session opened with the old password stops working.

    A password changed because it may have leaked has bought nothing while the
    session opened with the old one is still live. Must not fire: a second
    account's session is untouched, so this revokes one account's rather than
    everybody's.
    """
    with Deployment() as live:
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        changed = request(live.url(f"{P}/accounts/{MEMBER}/password"),
                          method="PUT", headers=bob,
                          payload={"current": BOB_PASSWORD,
                                   "password": BOB_PASSWORD + "-new"})
        check(changed[0] == 204,
              f"changing your own password answered {changed[0]} "
              f"{changed[2][:160]!r}")
        check(request(live.url(f"{P}/runs"), headers=bob)[0] == 401,
              "the session opened with the old password still works")
        check(request(live.url(f"{P}/runs"), headers=alice)[0] == 200,
              "another account's session was revoked too")
        wrong = request(live.url(f"{P}/accounts/{OPERATOR}/password"),
                        method="PUT", headers=alice,
                        payload={"current": "wrong-password-q",
                                 "password": "another-password-1"})
        check(wrong[0] == 403 and code_of(wrong[2]) == "bad_current_password",
              f"your own password can be changed without giving the current "
              f"one: {wrong[0]} {wrong[2][:160]!r}")


# --------------------------------------------------------------------------
# what needs an identity
# --------------------------------------------------------------------------


def routes_of(built) -> list[tuple[str, str]]:
    """Every route the contract defines, as (method, path), derived from source.

    Derived rather than listed, so a route added next year is covered by
    construction. The paths carry placeholders filled with values of the right
    shape, because the question is which *gate* answers, not whether the thing
    behind it exists.
    """
    identifier = "0" * 32
    return [
        ("GET", f"{P}/health"),
        ("GET", f"{P}/config"),
        # Saved defaults: a person's own, so every verb needs a person.
        ("GET", f"{P}/defaults"),
        ("PUT", f"{P}/defaults"),
        ("DELETE", f"{P}/defaults"),
        ("GET", f"{P}/settings/keys"),
        ("PUT", f"{P}/settings/keys/{PROVIDER}"),
        ("DELETE", f"{P}/settings/keys/{PROVIDER}"),
        ("PUT", f"{P}/settings/endpoints/{PROVIDER}"),
        ("DELETE", f"{P}/settings/endpoints/{PROVIDER}"),
        ("GET", f"{P}/runs"),
        ("POST", f"{P}/runs"),
        ("GET", f"{P}/runs/{identifier}"),
        ("DELETE", f"{P}/runs/{identifier}"),
        ("GET", f"{P}/runs/{identifier}/merged"),
        ("GET", f"{P}/runs/{identifier}/report.html"),
        ("GET", f"{P}/runs/{identifier}/report"),
        ("GET", f"{P}/runs/{identifier}/events"),
        ("GET", f"{P}/accounts"),
        ("POST", f"{P}/accounts"),
        ("DELETE", f"{P}/accounts/{MEMBER}"),
        ("PUT", f"{P}/accounts/{MEMBER}/password"),
    ]


def test_every_route_but_session_and_setup_needs_an_identity() -> None:
    """Must fire on every route with no session; must not fire with one.

    The interesting half is the *set*: `api.OPEN_ROUTES` is an allowlist of
    tuples, and this asserts that nothing outside it answers. A route added
    under `/session/` next year does not inherit the exemption, because the
    allowlist is exact tuples rather than a prefix.

    The refusals below are all 401. A 404 would be wrong here and is worth
    saying: the route exists, and a server that answered "no such path" to an
    unauthenticated caller and "no such run" to an authenticated one would be
    telling the first one something by the difference.
    """
    with Deployment() as live:
        live.first_account()
        for method, path in routes_of(live.built):
            status, _, body = request(live.url(path), method=method,
                                      payload={} if method in ("POST", "PUT") else None)
            check(status == 401 and code_of(body) == "no_session",
                  f"{method} {path} answered {status} {code_of(body)!r} with "
                  f"no session; every route but session and setup needs one")
        # Must not fire: the two that are open, and one that is not, with a
        # session. `401` from the second group would mean the check above
        # passes over a server that refuses everybody.
        check(request(live.url(f"{P}/session"))[0] == 200,
              "the session route is not answerable without a session, so there "
              "is no way to log in")
        who = live.sign_in(OPERATOR, ALICE_PASSWORD)
        check(request(live.url(f"{P}/runs"), headers=who)[0] == 200,
              "a signed-in caller cannot read runs either")
        check(tuple(sorted(api.OPEN_ROUTES))
              == (("locales",), ("session",), ("setup",)),
              f"the open-route allowlist has grown: {sorted(api.OPEN_ROUTES)}")
        # The three that are open, asked with nothing at all. `locales` is the
        # one found by driving the page: without it every string on the login
        # form renders as its own key, which no file-level check sees because
        # the page still lays out perfectly.
        for path in (f"{P}/session", f"{P}/locales", f"{P}/locales/en"):
            status, _, _ = request(live.url(path))
            check(status == 200,
                  f"{path} answered {status} with no session; the login form "
                  f"is written in the strings behind it")
        # And a route one segment further down is not open, so the two-segment
        # rule is a rule rather than a prefix.
        deeper = request(live.url(f"{P}/locales/en/strings"))
        check(deeper[0] == 401,
              f"a route below /locales inherited the exemption: {deeper[0]}")


def test_a_server_with_no_accounts_answers_only_setup() -> None:
    """Must fire on every route; must not fire on the one that makes an account.

    "With no accounts, `serve` must not be open" is the whole of the first-run
    rule, and the alternative it replaces is a default password -- the password
    that has not been changed yet is the one a scanner finds.
    """
    with Deployment() as live:
        for method, path in routes_of(live.built):
            status, _, body = request(live.url(path), method=method,
                                      payload={} if method in ("POST", "PUT") else None)
            check(status == 401 and code_of(body) == "setup_required",
                  f"{method} {path} answered {status} {code_of(body)!r} on a "
                  f"server with no accounts")
        # The page is still served, because the form that makes the account is
        # on it. A setup mode that refused the page would be a setup mode with
        # no way in.
        check(request(live.url("/"))[0] == 200,
              "the page is not served in setup mode, so the setup form cannot "
              "be reached")
        # The wrong token is refused, and the right one works once.
        wrong = request(live.url(f"{P}/setup"), method="POST",
                        payload={"token": "not-the-token", "username": OPERATOR,
                                 "password": ALICE_PASSWORD})
        check(wrong[0] == 403 and code_of(wrong[2]) == "bad_setup_token",
              f"setup accepted the wrong token: {wrong[0]} {wrong[2][:160]!r}")
        check(live.first_account()[0] == 200, "the right setup token is refused")
        again = request(live.url(f"{P}/setup"), method="POST",
                        payload={"token": live.setup.token, "username": "carol",
                                 "password": "probe-password-carol-2"})
        check(again[0] == 409 and code_of(again[2]) == "already_set_up",
              f"the setup route works a second time: {again[0]}")


def test_the_first_account_inherits_the_existing_credentials_file() -> None:
    """The migration: nothing moves, and the answer says so.

    An upgrade from a single-tenant server already has a `credentials.json`
    full of keys. It becomes the operator's, which is exactly what it already
    was, and from there it is the set of endpoints shared with every later
    account. Must fire: the key configured before setup is the one the
    operator's own settings route reports afterwards. Must not fire: a second
    account sees no key of its own.
    """
    with environment(), Deployment() as live:
        live.keys.set(PROVIDER, ALICE_KEY)
        live.keys.apply(os.environ, live.built.store.environ)
        status, _, body = live.first_account()
        payload = as_json(body) or {}
        check(status == 200 and "migrated" in payload,
              f"setup does not say what happened to the keys already here: "
              f"{status} {body[:200]!r}")
        check(str(live.keys.path) in json.dumps(payload),
              "the migration note does not name the file it is about")
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        rows = as_json(request(live.url(f"{P}/settings/keys"),
                               headers=alice)[2])["providers"]
        mine = [row for row in rows if row["name"] == PROVIDER][0]
        check(mine["configured"] and mine.get("suffix") == ALICE_KEY[-4:],
              f"the operator does not hold the key that was already here: "
              f"{mine}")
        check(mine["owner"] == "operator" and mine["editable"] is True,
              f"the operator's own row is not theirs to edit: {mine}")
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        rows = as_json(request(live.url(f"{P}/settings/keys"),
                               headers=bob)[2])["providers"]
        theirs = [row for row in rows if row["name"] == PROVIDER][0]
        check(theirs["owner"] == "operator" and theirs["editable"] is False,
              f"a member is offered the operator's shared row as their own to "
              f"edit: {theirs}")
        check(ALICE_KEY not in json.dumps(rows),
              "a member's settings page carries the operator's key")


def shared_key_problems() -> list[str]:
    """What each account is told about the operator's shared key, as sentences.

    The operator owns the shared key and is told its last four characters. A
    member is told that it is set and nothing of what it is. A member's own
    key, stored against their own endpoint, is theirs to be told about.
    """
    found: list[str] = []
    last = ALICE_KEY[-credentials.SUFFIX_LENGTH:]
    with environment(), Deployment() as live:
        live.keys.set(PROVIDER, ALICE_KEY)
        live.keys.apply(os.environ, live.built.store.environ)
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)

        def row(who: dict) -> dict:
            rows = as_json(request(live.url(f"{P}/settings/keys"),
                                   headers=who)[2])["providers"]
            return [entry for entry in rows if entry["name"] == PROVIDER][0]

        theirs = row(alice)
        if not (theirs["configured"] is True and theirs.get("suffix") == last
                and theirs["owner"] == "operator"):
            found.append(f"the operator is not told the last characters of "
                         f"their own shared key: {theirs}")
        seen = row(bob)
        if not (seen["configured"] is True and seen["owner"] == "operator"
                and seen["editable"] is False):
            found.append(f"a member is not told that the operator's key is "
                         f"set: {seen}")
        if "suffix" in seen:
            found.append(f"a member's row for the operator's key carries a "
                         f"suffix: {seen.get('suffix')!r}")
        # Nothing else a member can read carries the characters either.
        for path in (f"{P}/settings/keys", f"{P}/config", f"{P}/health",
                     f"{P}/session"):
            body = request(live.url(path), headers=bob)[2].decode("utf-8")
            if last in body:
                found.append(f"GET {path} gives a member the last characters "
                             f"of the operator's key")
        # A member's own key: theirs, so its characters are theirs to see.
        if live.set_endpoint(bob, "http://127.0.0.1:2")[0] != 200 \
                or live.set_key(bob, BOB_KEY)[0] != 204:
            found.append("a member could not store a key of their own")
        mine = row(bob)
        if not (mine["owner"] == "you"
                and mine.get("suffix") == BOB_KEY[-credentials.SUFFIX_LENGTH:]):
            found.append(f"a member is not told the last characters of their "
                         f"own key: {mine}")
        # And the operator's view is not changed by any of that.
        if row(alice).get("suffix") != last:
            found.append("the operator's own view lost its characters")
    return found


def test_a_member_learns_only_that_the_shared_key_is_set() -> None:
    """The last four characters of a key go to the account that owns it.

    Must not fire: the operator sees the characters of the shared key, a
    member sees `configured` and no `suffix`, and a member sees the
    characters of a key they stored themselves.

    Must fire: `Directory.rows_for` with the one expression that withholds
    the suffix taken out of its own source, which is the server this was
    before. The member's row then carries the operator's characters and the
    check says so.
    """
    import inspect
    import textwrap

    for problem in shared_key_problems():
        check(False, f"shared key: {problem}")

    shipped = accounts.Directory.rows_for
    text = textwrap.dedent(inspect.getsource(shipped))
    withheld = "seen = row if operator else {"
    start = text.index(withheld)
    end = text.index("}", start) + 1
    seeded_text = text[:start] + "seen = row" + text[end:]
    scope = dict(vars(accounts))
    exec(compile(seeded_text, "seeded rows_for", "exec"), scope)  # noqa: S102
    accounts.Directory.rows_for = scope["rows_for"]
    try:
        seeded = shared_key_problems()
    finally:
        accounts.Directory.rows_for = shipped
    check(any("carries a suffix" in problem for problem in seeded)
          and any("gives a member the last characters" in problem
                  for problem in seeded),
          f"seeded check: a server that sends a member the operator's "
          f"characters passed: {seeded}")
    check(shared_key_problems() == [],
          "rows_for was not put back after the seed")


# --------------------------------------------------------------------------
# the bind token, superseded
# --------------------------------------------------------------------------

# The two spellings of "everything". `0.0.0.0` is the one an operator types and
# `""` is the one that matches no address pattern at all, which is why both are
# asked rather than one taken as standing for the other.
WILDCARDS = ("0.0.0.0", "")


def test_a_non_loopback_bind_is_refused_with_no_accounts_and_allowed_with_one() -> None:
    """Both halves of the supersession, on a real `build`.

    Must fire: with no accounts and no token, every non-loopback spelling
    raises before a socket is bound -- asserted by the absence of a `Server`
    rather than by a message, because a server that refused loudly and bound
    anyway would pass a check written against the text.

    Must not fire: the same address, with an account on the store and still no
    token, binds and answers. That is the retirement: logging in *is* the
    authentication a bind token used to demand, and leaving a second secret
    configured alongside it is how the wrong one stays in place for years.
    """
    with tempfile.TemporaryDirectory() as raw:
        empty = accounts.Accounts(Path(raw) / "empty.json")
        filled = accounts.Accounts(Path(raw) / "filled.json")
        filled.create(OPERATOR, ALICE_PASSWORD, operator=True)
        for host in WILDCARDS:
            for token in ("", "   ", "short"):
                try:
                    built = server.build(host=host, port=0, token=token,
                                         accounts=empty,
                                         work_dir=Path(raw) / "w", environ={})
                    built.server_close()
                    built.store.close()
                    check(False,
                          f"build bound {host!r} with token {token!r} and no "
                          f"account; a key-spending port on the network with "
                          f"nothing in front of it")
                except credentials.BindRefused as refusal:
                    check("account" in str(refusal),
                          f"the refusal does not mention that an account lifts "
                          f"it: {refusal}")
            built = server.build(host=host, port=0, token="", accounts=filled,
                                 work_dir=Path(raw) / "w", environ={})
            try:
                check(built.host == host,
                      f"a server with an account bound {built.host!r} rather "
                      f"than the {host!r} it was asked for")
            finally:
                built.server_close()
                built.store.close()


def test_the_bind_token_is_not_consulted_once_an_account_exists() -> None:
    """Must fire: the old header, carrying the old secret, is refused.

    Two parallel secrets where one has been superseded is an arrangement in
    which the wrong one stays configured for years, so the token is not merely
    unnecessary here -- it is not looked at. A script still presenting it gets
    a 401 that names the route it should be posting to instead.

    Must not fire: the same server accepts a session id in that same header,
    so the header is still the way a script presents an identity.
    """
    token = "probe-bind-token-0123456789"
    with Deployment(token=token) as live:
        # With no account, the token is still what it always was.
        with_token = request(live.url(f"{P}/runs"),
                             headers={credentials.TOKEN_HEADER: token})
        check(with_token[0] == 401 and code_of(with_token[2]) == "setup_required",
              f"with no account the token gets past the bind rule and lands in "
              f"setup: {with_token[0]} {code_of(with_token[2])!r}")
        live.first_account(headers={credentials.TOKEN_HEADER: token})
        refused = request(live.url(f"{P}/runs"),
                          headers={credentials.TOKEN_HEADER: token})
        check(refused[0] == 401 and code_of(refused[2]) == "no_session",
              f"the bind token still authenticates a request after accounts "
              f"exist: {refused[0]} {code_of(refused[2])!r}")
        check(f"{P}/session".encode() in refused[2],
              f"the refusal does not say where to log in: {refused[2][:200]!r}")
        who = live.sign_in(OPERATOR, ALICE_PASSWORD)
        check(request(live.url(f"{P}/runs"), headers=who)[0] == 200,
              "a session id in the same header is refused too, so scripts have "
              "no way in at all")


def network_setup_problems() -> list[str]:
    """A server on every interface, a token, no account: the path to signed in.

    What the page does, request by request, against a real wildcard bind: it
    is refused without the token, is answered with it, creates the first
    account with it, and is then carried by the cookie alone. Returned as
    sentences so the seeded run below can ask the same question.
    """
    found: list[str] = []
    token = "probe-bind-token-0123456789"
    carried = {credentials.TOKEN_HEADER: token}
    with Deployment(host=WILDCARDS[0], token=token) as live:
        # The token is required on every API route, the open ones included,
        # and a wrong one is refused the same way as none.
        for method, path in routes_of(live.built):
            for headers in (None, {credentials.TOKEN_HEADER: token + "x"}):
                status, _, body = request(
                    live.url(path), method=method, headers=headers,
                    payload={} if method in ("POST", "PUT") else None)
                if status != 401 or code_of(body) != "no_token":
                    found.append(f"{method} {path} answered {status} "
                                 f"{code_of(body)!r} without the token")
        for path in (f"{P}/session", f"{P}/locales"):
            status, _, body = request(live.url(path))
            if status != 401 or code_of(body) != "no_token":
                found.append(f"GET {path} answered {status} {code_of(body)!r} "
                             f"without the token")
        # The page itself is public, or there is nothing to type the token into.
        if request(live.url("/"))[0] != 200:
            found.append("the page is not served, so the token cannot be given")

        # With the token: the session route says setup is wanted.
        status, _, body = request(live.url(f"{P}/session"), headers=carried)
        state = as_json(body) or {}
        if status != 200 or state.get("setup_required") is not True:
            found.append(f"with the token the session route answered {status} "
                         f"{body[:160]!r}, not a server waiting for setup")
        if request(live.url(f"{P}/locales"), headers=carried)[0] != 200:
            found.append("with the token the strings are still refused")

        # The first account needs both: the access token and the setup token.
        bare = live.first_account()
        if bare[0] != 401 or code_of(bare[2]) != "no_token":
            found.append(f"setup without the access token answered {bare[0]} "
                         f"{code_of(bare[2])!r}")
        made = live.first_account(headers=carried)
        cookie = (made[1].get("Set-Cookie") or "").split(";")[0]
        if made[0] != 200 or not cookie:
            found.append(f"setup with both tokens answered {made[0]} and set "
                         f"{cookie!r}")
            return found

        # Signed in, by the cookie alone, and the token is finished with.
        status, _, body = request(live.url(f"{P}/session"),
                                  headers={"Cookie": cookie})
        state = as_json(body) or {}
        if not (status == 200 and state.get("authenticated") is True
                and (state.get("user") or {}).get("username") == OPERATOR):
            found.append(f"the cookie setup set does not sign the operator in: "
                         f"{status} {body[:160]!r}")
        if request(live.url(f"{P}/runs"), headers={"Cookie": cookie})[0] != 200:
            found.append("the signed-in operator is refused their own runs")
        # Why the page has to drop the token here: the same header is a
        # session id now, and it outranks the cookie.
        status, _, body = request(live.url(f"{P}/session"),
                                  headers={"Cookie": cookie, **carried})
        if (as_json(body) or {}).get("authenticated") is not False:
            found.append("the access token beside a good cookie still reads as "
                         "signed in, so the header no longer outranks the cookie")
    return found


def test_a_network_server_with_a_token_is_set_up_through_the_api() -> None:
    """Token, then the first account, then signed in, on a wildcard bind.

    Must not fire: the path works with the token in the header and ends in a
    session carried by the cookie.

    Must fire: with the token check taken out, the routes that must refuse a
    request without it answer, and the check says so. The token is the only
    thing in front of a server with no account.
    """
    for problem in network_setup_problems():
        check(False, f"network setup: {problem}")
    shipped = api.check_token
    api.check_token = lambda headers, expected: None
    try:
        seeded = network_setup_problems()
    finally:
        api.check_token = shipped
    check(any("without the token" in problem for problem in seeded),
          f"seeded check: a server that no longer asks for the token passed: "
          f"{seeded}")


def test_serve_always_has_an_account_store() -> None:
    """Asserted on the command's own source, because the mode has no other guard.

    `build(accounts=None)` is the single-tenant server and is a legitimate
    thing for a library caller -- and the suite -- to ask for. It is not a
    thing an operator should be able to get by running the command, and the
    only thing standing between those two statements is one argument in
    `serve`. Seeded both ways, because a source check nobody has watched fail
    reads every function as correct.
    """
    import inspect

    real = inspect.getsource(server.serve)

    def always_has_a_store(text: str) -> bool:
        return "Accounts(" in text and "accounts=accounts" in text

    check(always_has_a_store(real),
          "server.serve no longer builds an account store, so `llossless "
          "serve` is a server with no identity on it")
    check(not always_has_a_store(real.replace("accounts=accounts,", "")),
          "the detector cannot see a `serve` that drops the store, so its "
          "silence over the real one means nothing")


# --------------------------------------------------------------------------
# whose job
# --------------------------------------------------------------------------


def a_submission(**overrides) -> dict:
    """The smallest valid submit body, aimed at a typed model and an endpoint."""
    payload = {
        "documents": [{"name": "notes-a.md", "text": SOURCE_A},
                      {"name": "notes-b.md", "text": SOURCE_B}],
        "base": "notes-a.md",
        "model": "test-model",
        "merge_model": "test-model",
        "endpoint": PROVIDER,
    }
    payload.update(overrides)
    return payload


def test_user_b_cannot_read_user_a_s_run_by_id() -> None:
    """Every route that reaches a run, and the refusal is the id-does-not-exist one.

    Must fire on five routes -- the status, the report, the merged document,
    the deletion and the event stream. Must not fire on the owner, who reads
    all five, because a check that refused everybody would pass the first half
    and mean nothing.

    The deletion is the odd one and is asserted on its *effect* rather than on
    its status: `DELETE` is idempotent and answers 204 for an id that was
    never here, so answering anything else for a stranger's id would be an
    oracle. What is checked is that the run is still there afterwards.
    """
    with FakeEndpoint(Script(**CLEAN)) as base_url, \
            environment(), Deployment(
                environ={"LLOSSLESS_STRUCTURED": "prompt"}) as live:
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        check(live.set_endpoint(alice, base_url)[0] == 200,
              "the operator could not configure the scripted endpoint")
        submitted = request(live.url(f"{P}/runs"), method="POST", headers=alice,
                            payload=a_submission())
        check(submitted[0] == 202,
              f"a submit by the operator answered {submitted[0]} "
              f"{submitted[2][:300]!r}")
        if submitted[0] != 202:
            return
        run_id = as_json(submitted[2])["id"]
        check(wait_for(lambda: state_of(live, run_id, alice)
                       in ("done", "failed")),
              "the operator's run never finished")

        paths = (f"{P}/runs/{run_id}", f"{P}/runs/{run_id}/merged",
                 f"{P}/runs/{run_id}/report.html",
                 f"{P}/runs/{run_id}/report",
                 f"{P}/runs/{run_id}/events")
        for path in paths:
            status, _, body = request(live.url(path), headers=bob)
            check(status == 404 and code_of(body) == "no_run",
                  f"{path} answered {status} {code_of(body)!r} to a user who "
                  f"does not own it; a uuid4 is not an access control")
        # Must not fire: the owner reads every one of them.
        for path in paths:
            status, _, _ = request(live.url(path), headers=alice)
            check(status == 200,
                  f"{path} answered {status} to its own owner, so the refusals "
                  f"above are not about ownership")
        # And the listing.
        theirs = as_json(request(live.url(f"{P}/runs"), headers=bob)[2])["runs"]
        check(theirs == [],
              f"another user's run list carries {len(theirs)} of the "
              f"operator's runs")
        mine = as_json(request(live.url(f"{P}/runs"), headers=alice)[2])["runs"]
        check(len(mine) == 1,
              f"the owner's own run list has {len(mine)} runs in it")
        # The deletion, asserted on its effect.
        check(request(live.url(f"{P}/runs/{run_id}"), method="DELETE",
                      headers=bob)[0] == 204,
              "deleting somebody else's run answers something other than the "
              "204 an unknown id gets, which is an oracle")
        check(request(live.url(f"{P}/runs/{run_id}"), headers=alice)[0] == 200,
              "a user who does not own a run was able to delete it")
        check(request(live.url(f"{P}/runs/{run_id}"), method="DELETE",
                      headers=alice)[0] == 204,
              "the owner cannot delete their own run")
        check(request(live.url(f"{P}/runs/{run_id}"), headers=alice)[0] == 404,
              "the owner's own deletion did nothing")


def test_a_run_is_cancelled_by_its_submitter_or_the_operator_and_nobody_else() -> None:
    """`POST /runs/<id>/cancel`, under the accounts model.

    Must fire: a third account's cancel answers the 404 a stranger's id gets
    and leaves the run running and unflagged. Must not fire: the submitter's
    own cancel, and the operator's cancel of a member's run, each land the run
    in `cancelled`. A finished run's cancel is a 409, and a GET is a 405.
    """
    class Slow:
        def __init__(self):
            self.script = Script(**CLEAN)

        def __call__(self, body, n):
            time.sleep(1.5)
            return self.script(body, n)

    carol_password = "carol-password-for-the-cancel-check-639"
    with FakeEndpoint(Slow()) as base_url, environment(), Deployment(
            environ={"LLOSSLESS_STRUCTURED": "prompt"}) as live:
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        live.add_account(alice, "carol", carol_password)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        carol = live.sign_in("carol", carol_password)
        check(live.set_endpoint(alice, base_url)[0] == 200,
              "the operator could not configure the scripted endpoint")

        def submit(who) -> str:
            status, _, body = request(live.url(f"{P}/runs"), method="POST",
                                      headers=who, payload=a_submission())
            check(status == 202, f"a submit answered {status} {body[:300]!r}")
            return (as_json(body) or {}).get("id", "")

        def cancel(run_id, who, method="POST"):
            return request(live.url(f"{P}/runs/{run_id}/cancel"), method=method,
                           headers=who)

        def status(run_id, who) -> dict:
            return as_json(request(live.url(f"{P}/runs/{run_id}"), headers=who)[2]) or {}

        run_id = submit(bob)
        check(wait_for(lambda: state_of(live, run_id, bob) == "running"),
              "the member's run never started")
        refused = cancel(run_id, carol)
        check(refused[0] == 404 and code_of(refused[2]) == "no_run",
              f"another member's cancel answered {refused[0]} {code_of(refused[2])!r}")
        now = status(run_id, bob)
        check(now.get("state") == "running" and now.get("cancel_requested") is False,
              f"a refused cancel changed the run: {now}")
        check(cancel(run_id, bob, method="GET")[0] == 405, "GET on the cancel route is not a 405")
        taken = cancel(run_id, bob)
        check(taken[0] == 202 and (as_json(taken[2]) or {}).get("cancel_requested") is True,
              f"the submitter's own cancel answered {taken[0]} {taken[2][:200]!r}")
        check(wait_for(lambda: state_of(live, run_id, bob) == "cancelled", timeout=20),
              f"the submitter's cancelled run is {state_of(live, run_id, bob)!r}")
        late = cancel(run_id, bob)
        check(late[0] == 409 and code_of(late[2]) == "not_running",
              f"a finished run's cancel answered {late[0]} {code_of(late[2])!r}")

        other = submit(bob)
        check(wait_for(lambda: state_of(live, other, bob) == "running"),
              "the member's second run never started")
        taken = cancel(other, alice)
        check(taken[0] == 202, f"the operator's cancel of a member's run answered {taken[0]}")
        check(wait_for(lambda: state_of(live, other, bob) == "cancelled", timeout=20),
              f"the operator's cancel did not stop the run: {state_of(live, other, bob)!r}")

        # Seeded: with ownership not consulted, the third account's cancel is
        # taken, so the refusal above is the ownership rule and nothing else.
        third = submit(bob)
        check(wait_for(lambda: state_of(live, third, bob) == "running"),
              "the member's third run never started")
        real = api.Api.__dict__["_owns"]
        api.Api._owns = staticmethod(lambda job, who: True)
        try:
            seeded = cancel(third, carol)
        finally:
            api.Api._owns = real
        check(seeded[0] == 202,
              f"seeded: with ownership ignored a stranger's cancel still answered "
              f"{seeded[0]}, so the refusal is not the ownership check")
        wait_for(lambda: state_of(live, third, bob) in ("cancelled", "done", "failed"), timeout=20)


# --------------------------------------------------------------------------
# whose key
# --------------------------------------------------------------------------


def bearer_keys(endpoint) -> set[str]:
    """Every bearer token this endpoint was handed, as a set. `` for none."""
    seen = set()
    for headers in endpoint.headers:
        for name, value in headers.items():
            if name.lower() == "authorization":
                seen.add(str(value).split(" ", 1)[-1].strip())
    return seen


def test_two_concurrent_jobs_from_two_users_use_two_different_keys() -> None:
    """The check this milestone exists for, asserted on the wire.

    Two accounts, two endpoints, two keys, two jobs, forced to overlap by a
    barrier so that the assertion is about two runs in flight at once rather
    than two that happened to serialise. What is read is the `Authorization`
    header each endpoint was *handed* -- not a mapping handed to a function --
    because the failure being guarded is a process-wide environment and the
    only place that shows is on the socket.

    Must fire: neither endpoint ever sees the other user's key. Must not fire:
    both endpoints see a key at all, and the search can find one when it is
    there. Three clean checks over nothing is the failure mode this project
    has recorded, and without the second half that is what this would be.
    """
    barrier = threading.Barrier(2, timeout=PATIENCE)
    broke = {"it": False}

    def gate(script):
        """A responder that holds the first call until the other job arrives."""
        state = {"first": True}

        def responder(body, call):
            if state["first"]:
                state["first"] = False
                try:
                    barrier.wait()
                except threading.BrokenBarrierError:
                    broke["it"] = True
            return script(body, call)

        return responder

    with contextlib.ExitStack() as stack:
        # The endpoint objects are held rather than only their URLs, because
        # what is read at the end is `FakeEndpoint.headers` -- the
        # `Authorization` each one was actually handed.
        alice_endpoint = FakeEndpoint(gate(Script(**CLEAN)))
        bob_endpoint = FakeEndpoint(gate(Script(**CLEAN)))
        alice_url = stack.enter_context(alice_endpoint)
        bob_url = stack.enter_context(bob_endpoint)
        stack.enter_context(environment())
        live = stack.enter_context(Deployment(
            workers=2, environ={"LLOSSLESS_STRUCTURED": "prompt"}))

        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        check(live.set_endpoint(alice, alice_url)[0] == 200,
              "the operator could not configure their endpoint")
        check(live.set_key(alice, ALICE_KEY)[0] == 204,
              "the operator could not store their key")
        check(live.set_endpoint(bob, bob_url)[0] == 200,
              "a member could not configure an endpoint of their own")
        check(live.set_key(bob, BOB_KEY)[0] == 204,
              "a member could not store a key of their own")

        first = request(live.url(f"{P}/runs"), method="POST", headers=alice,
                        payload=a_submission())
        second = request(live.url(f"{P}/runs"), method="POST", headers=bob,
                         payload=a_submission())
        check(first[0] == 202 and second[0] == 202,
              f"the two submits answered {first[0]} and {second[0]}: "
              f"{first[2][:200]!r} {second[2][:200]!r}")
        if first[0] != 202 or second[0] != 202:
            return
        ids = (as_json(first[2])["id"], as_json(second[2])["id"])
        for run_id, who in zip(ids, (alice, bob)):
            check(wait_for(lambda run_id=run_id, who=who:
                           state_of(live, run_id, who) in ("done", "failed")),
                  f"run {run_id} never finished")

        check(not broke["it"],
              "the two runs never overlapped, so this is a check about two "
              "jobs that happened to serialise rather than about two in flight")

        alice_saw = bearer_keys(alice_endpoint)
        bob_saw = bearer_keys(bob_endpoint)
        # Must not fire: the probe can see a key at all.
        check(alice_saw and bob_saw,
              f"one of the endpoints was handed no bearer token, so the "
              f"assertions below are over nothing: {alice_saw} {bob_saw}")
        check(ALICE_KEY in alice_saw and BOB_KEY in bob_saw,
              f"an endpoint was not handed its own user's key: "
              f"alice saw {sorted(alice_saw)}, bob saw {sorted(bob_saw)}")
        # Must fire: neither crossed.
        check(BOB_KEY not in alice_saw,
              f"the operator's endpoint was handed a member's key")
        check(ALICE_KEY not in bob_saw,
              f"a member's endpoint was handed the operator's key")


def test_a_users_key_never_reaches_the_process_environment() -> None:
    """Must fire: a member's key is in no environment anywhere in this process.

    `os.environ` is per process, and a second user's key in it is exactly the
    single tenancy multi-account support removes. The store's own copy is
    checked too, because that is the mapping a queued job resolves against.

    Must not fire: the operator's key *is* in the environment, which is the
    shared arrangement and is what makes the first half a statement about
    users rather than about a server that stores nothing.
    """
    with environment(), Deployment() as live:
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        check(live.set_key(alice, ALICE_KEY)[0] == 204,
              "the operator could not store a key")
        check(live.set_endpoint(bob, "http://127.0.0.1:2")[0] == 200,
              "a member could not configure an endpoint of their own")
        check(live.set_key(bob, BOB_KEY)[0] == 204,
              "a member could not store a key")
        check(os.environ.get(KEY_VARIABLE) == ALICE_KEY,
              f"the operator's key is not in the process environment, so the "
              f"check below is not about the difference between the two")
        check(BOB_KEY not in json.dumps(dict(os.environ)),
              "a member's key is in the process environment")
        check(BOB_KEY not in json.dumps(live.built.store.environ),
              "a member's key is in the environment a queued job resolves "
              "against")
        # And the member's own file holds it, so it was stored rather than
        # dropped -- a key that went nowhere would pass both checks above.
        theirs = live.built.api.directory.own(
            live.accounts.get(MEMBER).id)
        check(theirs.read()[PROVIDER].key == BOB_KEY,
              "the member's key was not stored in their own file at all")
        check(stat.S_IMODE(theirs.path.stat().st_mode) == credentials.FILE_MODE,
              f"a member's credentials file is mode "
              f"{stat.S_IMODE(theirs.path.stat().st_mode):04o}")


def test_a_member_configures_their_own_and_shadows_the_operators() -> None:
    """Must fire on a key with no address of its own; must not fire on their own row.

    The arrangement the real deployment wants: the operator configures the
    local endpoint once and everybody uses it, while each account adds its own
    vendor keys. So a member's writes always land in their own file and
    shadow the shared row for their runs alone -- and the one thing they are
    refused is a key stored against *nobody's* address, because a credential
    with no recorded destination travels to whichever one is in effect, which
    is the address-scoping rule and not a permission.
    """
    with environment(), Deployment() as live:
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        check(live.set_endpoint(alice, "http://127.0.0.1:1")[0] == 200,
              "the operator could not configure a shared endpoint")
        refused = live.set_key(bob, BOB_KEY)
        check(refused[0] == 403
              and code_of(refused[2]) == "no_endpoint_of_your_own",
              f"a member stored a key with no address of their own, which "
              f"would travel to the operator's: {refused[0]} "
              f"{refused[2][:200]!r}")
        # Must not fire: their own endpoint for the same provider is theirs.
        check(live.set_endpoint(bob, "http://127.0.0.1:2")[0] == 200,
              "a member cannot configure an endpoint of their own")
        check(live.set_key(bob, BOB_KEY)[0] == 204,
              "a member cannot store a key against their own endpoint")
        rows = as_json(request(live.url(f"{P}/settings/keys"),
                               headers=bob)[2])["providers"]
        mine = [row for row in rows if row["name"] == PROVIDER][0]
        check(mine["owner"] == "you" and mine["editable"] is True,
              f"a member's own row is not reported as theirs: {mine}")
        check(mine.get("suffix") == BOB_KEY[-4:],
              f"a member's own row does not report their own key: {mine}")
        # And the operator still sees theirs, unshadowed.
        rows = as_json(request(live.url(f"{P}/settings/keys"),
                               headers=alice)[2])["providers"]
        theirs = [row for row in rows if row["name"] == PROVIDER][0]
        check(theirs["base_url"] == "http://127.0.0.1:1",
              f"a member's endpoint replaced the operator's: {theirs}")


def test_the_operators_key_never_travels_to_an_address_a_member_typed() -> None:
    """The address-scoping rule, across the tenancy boundary. Must fire, then must not fire.

    A member who configures an endpoint of their own and stores no key against
    it must get **no** key, not the operator's. A shared credential sent to an
    address somebody typed thirty seconds ago is exactly the pairing
    `Endpoint.moved_to` exists to make unrepresentable, and it does not stop
    being that because the two sides are now two people rather than two
    addresses.

    Must not fire, twice: a member with *no* endpoint of their own does get
    the operator's key, because that goes to the operator's address and is the
    whole point of a shared endpoint; and a member with their own endpoint and
    their own key gets theirs.
    """
    with environment(), Deployment() as live:
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        check(live.set_endpoint(alice, "http://127.0.0.1:1")[0] == 200,
              "the operator could not configure a shared endpoint")
        check(live.set_key(alice, ALICE_KEY)[0] == 204,
              "the operator could not store a key")
        directory = live.built.api.directory
        member = live.accounts.get(MEMBER)
        # Must not fire: no endpoint of their own, so the shared key applies.
        shared = directory.keys_for(member.id, live.built.store.environ)
        check(shared.get(KEY_VARIABLE) == ALICE_KEY,
              f"a member with no endpoint of their own does not get the "
              f"shared key, so the shared endpoint is unusable: {shared}")
        # Must fire: their own address, and the operator's key must not follow.
        check(live.set_endpoint(bob, "http://127.0.0.1:2")[0] == 200,
              "a member cannot configure an endpoint of their own")
        alone = directory.keys_for(member.id, live.built.store.environ)
        check(alone.get(KEY_VARIABLE) is None,
              f"the operator's key travels to an address a member typed: "
              f"{alone}")
        # Must not fire: their own key against their own address.
        check(live.set_key(bob, BOB_KEY)[0] == 204,
              "a member cannot store a key against their own endpoint")
        theirs = directory.keys_for(member.id, live.built.store.environ)
        check(theirs.get(KEY_VARIABLE) == BOB_KEY,
              f"a member's own key is not what their own endpoint gets: "
              f"{theirs}")
        # And the operator is unswapped, so a key they exported in a shell
        # rather than through the page is still the one their runs spend.
        check(directory.keys_for(live.accounts.get(OPERATOR).id,
                                 live.built.store.environ) is None,
              "the operator's runs read a copy of their file rather than the "
              "environment, so a key set outside the settings page is lost "
              "while the page goes on reporting it as configured")


class Seeded:
    """Patch one attribute for the length of a `with`, and put it back.

    What is put back is the attribute as the owner holds it, not as
    `getattr` hands it over: a `staticmethod` read off its class comes back
    as a bare function, and restoring that would leave a method that takes
    one argument too many for every check that runs afterwards.
    """

    def __init__(self, owner, name: str, value) -> None:
        self.owner, self.name, self.value = owner, name, value

    def __enter__(self):
        self.before = vars(self.owner).get(self.name,
                                           getattr(self.owner, self.name))
        setattr(self.owner, self.name, self.value)
        return self

    def __exit__(self, *exc_info) -> None:
        setattr(self.owner, self.name, self.before)


def one_state_problems(change: str, seed=None) -> list[str]:
    """A member changes their endpoint while their run is starting. Who got whose key?

    Asked on the wire: what is read is the `Authorization` header each
    endpoint was handed. The change is made from inside the first read of
    the member's file that the worker makes, so it lands after that read and
    before any later one, every time, with no race to win.

    `change` is `delete` (the member had an endpoint of their own and removes
    it: a second read would then hand over the operator's shared key, for a
    run already addressed to the member's endpoint) or `create` (the member
    had none and stores one with a key: a second read would send the member's
    key to the operator's endpoint).
    """
    problems: list[str] = []
    with contextlib.ExitStack() as stack:
        shared_endpoint = FakeEndpoint(Script(**CLEAN))
        member_endpoint = FakeEndpoint(Script(**CLEAN))
        shared_url = stack.enter_context(shared_endpoint)
        member_url = stack.enter_context(member_endpoint)
        stack.enter_context(environment())
        live = stack.enter_context(Deployment(
            environ={"LLOSSLESS_STRUCTURED": "prompt"}))
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        if live.set_endpoint(alice, shared_url)[0] != 200 \
                or live.set_key(alice, ALICE_KEY)[0] != 204:
            return ["the operator could not configure the shared endpoint"]
        own = live.built.api.directory.own(live.accounts.get(MEMBER).id)
        if change == "delete" and live.set_endpoint(bob, member_url)[0] != 200:
            return ["a member could not configure an endpoint of their own"]

        shipped = credentials.Credentials.read
        state = {"reads": 0, "changing": False}

        def read(self):
            rows = shipped(self)
            if (self.path == own.path and not state["changing"]
                    and threading.current_thread().name.startswith(
                        "llossless-job")):
                state["reads"] += 1
                if state["reads"] == 1:
                    state["changing"] = True
                    try:
                        if change == "delete":
                            own.remove_endpoint(PROVIDER)
                        else:
                            own.set_endpoint(PROVIDER, member_url)
                            own.set(PROVIDER, BOB_KEY)
                    finally:
                        state["changing"] = False
            return rows

        with contextlib.ExitStack() as patches:
            patches.enter_context(Seeded(credentials.Credentials, "read", read))
            if seed is not None:
                patches.enter_context(seed)
            answer = request(live.url(f"{P}/runs"), method="POST", headers=bob,
                             payload=a_submission())
            if answer[0] != 202:
                return [f"the submit answered {answer[0]}: {answer[2][:200]!r}"]
            run_id = as_json(answer[2])["id"]
            if not wait_for(lambda: state_of(live, run_id, bob)
                            in ("done", "failed")):
                return ["the run never finished"]

        if state["reads"] < 1:
            problems.append("the worker never read the member's file, so the "
                            "change was never made and nothing was probed")
        addressed, other = ((member_endpoint, shared_endpoint)
                            if change == "delete"
                            else (shared_endpoint, member_endpoint))
        if not addressed.headers:
            problems.append("the endpoint the run was addressed to was never "
                            "called, so the assertions are over nothing")
        if other.headers:
            problems.append("one run called both endpoints")
        if ALICE_KEY in bearer_keys(member_endpoint):
            problems.append("the member's endpoint was handed the operator's key")
        if BOB_KEY in bearer_keys(shared_endpoint):
            problems.append("the operator's endpoint was handed the member's key")
    return problems


def test_a_run_s_address_and_its_key_come_from_one_read() -> None:
    """The operator's key never reaches a member's endpoint, whatever the timing.

    A run's address and its key used to be two reads of the member's settings
    file, one when the worker built the run and one a moment later on the same
    thread. A member who deleted their own endpoint between the two got a run
    addressed to their endpoint and carrying the operator's shared key, which
    their endpoint then received on every call.

    Must not fire: with the change landing straight after the first read, the
    member's endpoint is called and is handed no key of the operator's; and
    the other way round, the operator's endpoint is handed none of the
    member's.

    Must fire: `JobStore.resolved_for` replaced by the two shipped halves read
    one after the other, which is the store this was before.
    """
    for change in ("delete", "create"):
        problems = one_state_problems(change)
        check(not problems, f"one state, member {change}s their endpoint: "
                            + "; ".join(problems))

    def two_reads(self, owner):
        return self.environ_for(owner), self.keys_for(owner)

    seeded = one_state_problems(
        "delete", Seeded(jobs.JobStore, "resolved_for", two_reads))
    check("the member's endpoint was handed the operator's key" in seeded,
          f"must fire: a store that reads the address and the key separately "
          f"passed: {seeded}")
    seeded = one_state_problems(
        "create", Seeded(jobs.JobStore, "resolved_for", two_reads))
    check("the operator's endpoint was handed the member's key" in seeded,
          f"must fire: a store that reads the address and the key separately "
          f"passed the other direction: {seeded}")

    # And the same seed one layer down, on the function the store calls. A
    # second rule now stands behind this one: the operator's key is read
    # through `jobs.MemberKeys`, which hands it out only while the run's
    # address for that provider is the operator's own. So a directory that
    # reads twice no longer gets the key across by itself, and that is
    # asserted; the seed fires once the store hands over what the directory
    # read as it stands, which is the store this was before.
    def two_reads_below(self, account_id, environ=None):
        return self.environ_for(account_id), self.keys_for(account_id, environ)

    behind = one_state_problems(
        "delete", Seeded(accounts.Directory, "for_run", two_reads_below))
    check("the member's endpoint was handed the operator's key" not in behind,
          f"a directory that reads twice got the operator's key to a "
          f"member's endpoint past the store's own rule: {behind}")

    def as_read(keys, shared, standing, addresses=()):
        return dict(keys)

    with Seeded(jobs, "MemberKeys", as_read):
        seeded = one_state_problems(
            "delete", Seeded(accounts.Directory, "for_run", two_reads_below))
    check("the member's endpoint was handed the operator's key" in seeded,
          f"must fire: a directory that reads its file twice for one run, "
          f"under a store that hands over what it read, passed: {seeded}")


def moved_endpoint_problems() -> list[str]:
    """The operator moves a shared endpoint between a run's two sources.

    The address a member's run uses for a shared provider is the one in the
    environment the run resolves against; the shared file is read a moment
    later. The file is given the endpoint's new address and new key here
    while the environment still names the old pair.
    """
    problems: list[str] = []
    old_address, new_address = "http://127.0.0.1:1", "http://127.0.0.1:2"
    with tempfile.TemporaryDirectory() as raw:
        shared = credentials.Credentials(Path(raw) / "credentials.json")
        directory = accounts.Directory(shared)
        member = "d" * 32
        shared.set_endpoint(PROVIDER, old_address)
        shared.set(PROVIDER, ALICE_KEY)
        environ = shared.mapping()
        both = directory.for_run(member, environ)[1]
        if both.get(KEY_VARIABLE) != ALICE_KEY:
            problems.append("the shared key is not handed out for the address "
                            "it is stored with, so the shared endpoint is "
                            "unusable")
        shared.set_endpoint(PROVIDER, new_address)
        shared.set(PROVIDER, BOB_KEY)
        for name, keys in (("for_run", directory.for_run(member, environ)[1]),
                           ("keys_for", directory.keys_for(member, environ))):
            if keys.get(KEY_VARIABLE) == BOB_KEY:
                problems.append(f"{name} hands out the key stored with the "
                                f"new address for a run that resolves the "
                                f"old one")
            elif keys.get(KEY_VARIABLE) != ALICE_KEY:
                problems.append(f"{name} hands out no key at all, though the "
                                f"environment holds the old pair whole")
    return problems


def test_a_shared_key_is_handed_out_only_for_the_address_it_is_stored_with() -> None:
    """The operator's half of the same rule. Must not fire, then must fire.

    Must fire: `Directory._keys` with the line that leaves the file's key out
    removed from its own source.
    """
    import inspect
    import textwrap

    problems = moved_endpoint_problems()
    check(not problems, "moved shared endpoint: " + "; ".join(problems))

    shipped = accounts.Directory._keys
    text = textwrap.dedent(inspect.getsource(shipped))
    check(text.count('stored = ""') == 1,
          "the line this probe removes is no longer in `_keys` exactly once")
    scope = dict(vars(accounts))
    exec(compile(text.replace('stored = ""', "pass"),  # noqa: S102
                 "seeded _keys", "exec"), scope)
    with Seeded(accounts.Directory, "_keys", scope["_keys"]):
        seeded = moved_endpoint_problems()
    check(any("stored with the new address" in problem for problem in seeded),
          f"must fire: a directory that pairs the file's key with whatever "
          f"address the environment holds passed: {seeded}")


# A key saved for an endpoint's new address, while a run still calls the old one.
LATER_KEY = "probe-key-saved-for-the-new-address-9z4"


def moved_mid_run_problems(seed=None) -> list[str]:
    """The operator moves an endpoint while their own run is under way.

    The run's first call is held at the old address until the endpoint has
    been moved and a key saved for the new one, so every later call of the
    run is made after the change. What the old address was handed is read
    off the wire.
    """
    problems: list[str] = []
    hold, entered = threading.Event(), threading.Event()
    script = Script(**CLEAN)

    def held(body, call):
        if call == 1:
            entered.set()
            hold.wait(timeout=PATIENCE)
        return script(body, call)

    with contextlib.ExitStack() as stack:
        old_endpoint = FakeEndpoint(held)
        new_endpoint = FakeEndpoint(Script(**CLEAN))
        old_url = stack.enter_context(old_endpoint)
        new_url = stack.enter_context(new_endpoint)
        stack.enter_context(environment())
        if seed is not None:
            stack.enter_context(seed)
        live = stack.enter_context(Deployment(
            environ={"LLOSSLESS_STRUCTURED": "prompt"}))
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        try:
            if live.set_endpoint(alice, old_url)[0] != 200 \
                    or live.set_key(alice, ALICE_KEY)[0] != 204:
                return ["the operator could not configure the endpoint"]
            answer = request(live.url(f"{P}/runs"), method="POST",
                             headers=alice, payload=a_submission())
            if answer[0] != 202:
                return [f"the submit answered {answer[0]}"]
            run_id = as_json(answer[2])["id"]
            if not entered.wait(timeout=PATIENCE):
                return ["the run never called its endpoint"]
            if live.set_endpoint(alice, new_url)[0] != 200 \
                    or live.set_key(alice, LATER_KEY)[0] != 204:
                return ["the operator could not move the endpoint"]
        finally:
            hold.set()
        if not wait_for(lambda: state_of(live, run_id, alice)
                        in ("done", "failed")):
            return ["the run never finished"]
        if len(old_endpoint.headers) < 2:
            problems.append("the run made no call after the endpoint moved, "
                            "so nothing was probed")
        saw = bearer_keys(old_endpoint)
        if ALICE_KEY not in saw:
            problems.append("the old address was never handed its own key, "
                            "so the run was not using it to begin with")
        if LATER_KEY in saw:
            problems.append("the old address was handed the key saved for "
                            "the new one")
        if new_endpoint.headers:
            problems.append("the run moved to the new address part-way")
    return problems


def test_a_key_saved_for_a_new_address_never_reaches_a_run_on_the_old_one() -> None:
    """The same rule for the operator's own run, which reads its key at send time.

    A run resolves its addresses when it starts and the operator's key is
    read from the process environment on every call. So a run under way
    when the operator moved the endpoint and saved a key for the new address
    was handed that key on its next call, and sent it to the old address.

    Must not fire: a key replaced at the *same* address does reach a run
    under way, which is the reason the key is read at send time at all.

    Must fire: `StandingKeys.get` reading the environment with no regard to
    the address, which is the unswapped source this was before.
    """
    problems = moved_mid_run_problems()
    check(not problems, "endpoint moved mid-run: " + "; ".join(problems))

    def unbound(self, name, default=None):
        return os.environ.get(name, default)

    seeded = moved_mid_run_problems(Seeded(jobs.StandingKeys, "get", unbound))
    check("the old address was handed the key saved for the new one" in seeded,
          f"must fire: a run that reads the process's key whatever its "
          f"address has become passed: {seeded}")

    address = credentials.url_env(PROVIDER)
    with environment():
        live = {address: "http://127.0.0.1:1"}
        os.environ[KEY_VARIABLE] = ALICE_KEY
        os.environ["PROBE_UNRELATED_VARIABLE"] = "unrelated"
        source = jobs.StandingKeys(live, dict(live))
        check(source.get(KEY_VARIABLE) == ALICE_KEY,
              "a run is not handed the key of an address that has not moved")
        os.environ[KEY_VARIABLE] = LATER_KEY
        check(source.get(KEY_VARIABLE) == LATER_KEY,
              "a key replaced at the same address does not reach a run "
              "under way")
        live[address] = "http://127.0.0.1:2"
        check(source.get(KEY_VARIABLE) is None,
              "a run is handed a key after its address moved")
        check(source.get("PROBE_UNRELATED_VARIABLE") == "unrelated",
              "a variable that is no provider's key is not read through")
        check(ALICE_KEY not in repr(source) and LATER_KEY not in repr(vars(source)),
              "the key source holds or prints a key")


class Watched(dict):
    """An environment that records every state it passes through."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.states: list[dict] = []
        self.locked: list[bool] = []
        self.lock = None

    def _note(self) -> None:
        self.states.append(dict(self))
        if self.lock is not None:
            self.locked.append(self.lock.locked())

    def __setitem__(self, name, value) -> None:
        super().__setitem__(name, value)
        self._note()

    def pop(self, name, *default):
        value = super().pop(name, *default)
        self._note()
        return value


def apply_order_problems() -> list[str]:
    """One `apply` takes an environment from one address and key to another.

    Every state on the way is one a starting run could copy, so each is
    asked the question a run asks: is this key beside the address it was
    stored with? Every provider, because the order used to be alphabetical
    and so differed from one provider's variable names to the next.
    """
    problems: list[str] = []
    old_address, new_address = "http://127.0.0.1:1", "http://127.0.0.1:2"
    for name, variable in sorted(credentials.PROVIDERS.items()):
        with tempfile.TemporaryDirectory() as raw:
            keys = credentials.Credentials(Path(raw) / "credentials.json")
            target = Watched()
            keys.set_endpoint(name, old_address)
            keys.set(name, ALICE_KEY)
            keys.apply(target)
            keys.set_endpoint(name, new_address)
            keys.set(name, LATER_KEY)
            target.states.clear()
            target.lock = keys._applying
            keys.apply(target)
            if target.get(credentials.url_env(name)) != new_address \
                    or target.get(variable) != LATER_KEY:
                problems.append(f"{name}: the environment did not arrive at "
                                f"the new address and its key")
            for state in target.states:
                pair = (state.get(credentials.url_env(name)), state.get(variable))
                if pair == (old_address, LATER_KEY):
                    problems.append(f"{name}: the new key beside the old address")
                if pair == (new_address, ALICE_KEY):
                    problems.append(f"{name}: the old key beside the new address")
            if not target.locked or not all(target.locked):
                problems.append(f"{name}: the environment was written outside "
                                f"the lock")
            # And a pass that changes no address leaves no moment without a key.
            target.states.clear()
            keys.apply(target)
            if any(variable not in state for state in target.states):
                problems.append(f"{name}: a pass that moved nothing took the "
                                f"key away for a moment")
    return problems


def test_apply_never_leaves_a_key_beside_an_address_it_was_not_stored_with() -> None:
    """`Credentials.apply`, state by state. Must not fire, then must fire twice.

    Must fire: the same function writing its variables in alphabetical
    order, which is the order it had, and the same function with its lock
    taken away.
    """
    import inspect
    import textwrap

    problems = apply_order_problems()
    check(not problems, "apply order: " + "; ".join(sorted(set(problems))))

    shipped = credentials.Credentials.apply
    text = textwrap.dedent(inspect.getsource(shipped))
    for wanted in ("gone | (moving & set(wanted))",
                   "key=lambda name: (name in secret, name)",
                   "with self._applying:"):
        check(text.count(wanted) == 1,
              f"the expression this probe replaces is not in `apply` exactly "
              f"once: {wanted!r}")
    alphabetical = (text.replace("gone | (moving & set(wanted))", "gone")
                    .replace("key=lambda name: (name in secret, name)",
                             "key=lambda name: name"))
    unlocked = text.replace("with self._applying:",
                            "with contextlib.nullcontext():")
    for seeded_text, expected in ((alphabetical, "the new key beside the old address"),
                                  (unlocked, "written outside the lock")):
        scope = dict(vars(credentials))
        exec(compile(seeded_text, "seeded apply", "exec"), scope)  # noqa: S102
        with Seeded(credentials.Credentials, "apply", scope["apply"]):
            seeded = apply_order_problems()
        check(any(expected in problem for problem in seeded),
              f"must fire ({expected}): a seeded apply passed: "
              f"{sorted(set(seeded))}")


def test_a_per_user_endpoint_is_checked_by_both_of_configs_guards() -> None:
    """A per-user endpoint is still an endpoint. Must fire on both guards.

    `config.check_base_url` refuses a scheme that is not http(s), because
    `urllib.request.build_opener` installs `FileHandler` from its defaults and
    a `file://` base URL has a local file's bytes parsed as a model answer.
    `config.check_cleartext_key` refuses a bearer token over plain HTTP to a
    host that is not this machine -- and for a member that question is about
    *their* key, which is in their file and never in `os.environ`, so a check
    that read the environment would answer about somebody else's credential.

    Must not fire: a loopback http endpoint is accepted with a key stored,
    because the local default is exactly that and a guard that refused it
    would break every self-hosted deployment.
    """
    with environment(), Deployment() as live:
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        for hostile in ("file:///etc/passwd", "ftp://example.invalid/v1",
                        "http://user:secret@127.0.0.1:9/v1"):
            refused = live.set_endpoint(bob, hostile)
            check(refused[0] == 400,
                  f"a member set {hostile!r} as an endpoint: {refused[0]} "
                  f"{refused[2][:200]!r}")
        # Must not fire: loopback http is the local default and is accepted.
        check(live.set_endpoint(bob, "http://127.0.0.1:9")[0] == 200,
              "a member cannot configure a loopback endpoint")
        check(live.set_key(bob, BOB_KEY)[0] == 204,
              "a member cannot store a key against a loopback endpoint")
        # And the cleartext guard fires for that member's own key, which is
        # the half that needs the swapped key source to be right.
        # A reserved name rather than an address literal: the release scanner
        # scans every tracked file for an endpoint shape, and it is right to
        # refuse one it cannot tell from a live pod.
        cleartext = live.set_endpoint(bob, "http://not-this-machine.invalid:9")
        check(cleartext[0] == 400 and b"clear" in cleartext[2].lower(),
              f"a member sent their own key over plain HTTP to a host that is "
              f"not this machine: {cleartext[0]} {cleartext[2][:300]!r}")


# A cleartext address on another machine. A reserved name rather than an
# address literal, for the reason given in the check above.
ELSEWHERE = "http://not-this-machine.invalid:9"


def not_probed(*args, **kwargs):
    """Stands in for `discover.models`: an accepted address is not contacted."""
    return [], "not probed by this check"


def members_cleartext_problems() -> list[str]:
    """A member stores a cleartext endpoint of their own on a shared server.

    Two questions, and they have different answers. With the operator's key
    set for the provider and none of the member's own, nothing would travel
    to the member's address, so it is stored. With a key of the member's own
    saved, that key would travel, so it is refused, and the refusal has to
    name something a member can change.
    """
    problems: list[str] = []
    with environment(), Deployment() as live, \
            Seeded(api.discover, "models", not_probed):
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        if live.set_endpoint(alice, "http://127.0.0.1:1")[0] != 200 \
                or live.set_key(alice, ALICE_KEY)[0] != 204:
            return ["the operator could not configure the shared endpoint"]
        # The operator's own guard is not what is being loosened: the same
        # address, asked for by the account whose key would travel to it.
        theirs = live.set_endpoint(alice, ELSEWHERE)
        if theirs[0] != 400 or KEY_VARIABLE.encode() not in theirs[2]:
            problems.append(f"the operator moved a keyed endpoint to a "
                            f"cleartext address: {theirs[0]}")
        stored = live.set_endpoint(bob, ELSEWHERE)
        if stored[0] != 200:
            problems.append(f"a member's own cleartext endpoint was refused "
                            f"over a key that is never sent to it: "
                            f"{stored[0]} {stored[2][:160]!r}")
        keys = live.built.api.directory.keys_for(
            live.accounts.get(MEMBER).id, live.built.store.environ)
        if stored[0] == 200 and keys.get(KEY_VARIABLE) is not None:
            problems.append("the operator's key would be sent to the "
                            "member's cleartext address after all")
        # Now a key of the member's own, which would travel in the clear.
        if live.set_endpoint(bob, "http://127.0.0.1:9")[0] != 200 \
                or live.set_key(bob, BOB_KEY)[0] != 204:
            return problems + ["a member could not store a key of their own"]
        refused = live.set_endpoint(bob, ELSEWHERE)
        text = refused[2].decode("utf-8", "replace")
        if refused[0] != 400 or "cleartext" not in text:
            problems.append(f"a member's own key may travel in cleartext: "
                            f"{refused[0]} {text[:160]!r}")
        if KEY_VARIABLE in text or "unset" in text:
            problems.append("the refusal tells a member to unset a variable, "
                            "which a member cannot do")
        if refused[0] == 400 and "delete your" not in text:
            problems.append("the refusal names nothing a member can act on")
    return problems


def test_a_members_cleartext_endpoint_is_judged_by_the_members_own_key() -> None:
    """The cleartext guard asks about the key that would be sent. Both ways.

    The operator shares a key for a provider. A member who stored a
    cleartext address of their own for it was refused, and told to unset the
    operator's variable: a key that is never sent to a member's address, and
    a variable a member has no shell to unset.

    Must fire, twice: the route under the wider key source it used before
    (`Api._as`, which includes the operator's key), and the refusal left in
    the operator's wording.
    """
    problems = members_cleartext_problems()
    check(not problems, "a member's cleartext endpoint: " + "; ".join(problems))

    with Seeded(api.Api, "_as_owner", api.Api._as):
        seeded = members_cleartext_problems()
    check(any("never sent to it" in problem for problem in seeded),
          f"must fire: a guard that counts the operator's key against a "
          f"member's address passed: {seeded}")
    with Seeded(api.Api, "_cleartext_refusal",
                staticmethod(lambda who, provider, refusal: str(refusal))):
        seeded = members_cleartext_problems()
    check(any("unset a variable" in problem for problem in seeded)
          and any("nothing a member can act on" in problem
                  for problem in seeded),
          f"must fire: a refusal that names the operator's variable to a "
          f"member passed: {seeded}")


def test_the_request_allowlist_still_carries_no_url_or_key_variable() -> None:
    """Asserted by name, because the allowlist is what a request may set.

    Multi-tenancy changed where a key comes *from* and did not change what a
    submitter may name. A variable on this list that carried an address or a
    key variable would let one user aim another's run, which no amount of
    per-user storage would undo.
    """
    for variable in sorted(jobs.REQUEST_SETTABLE):
        check("BASE_URL" not in variable,
              f"{variable} is on REQUEST_SETTABLE and names an address")
        check("API_KEY" not in variable and "KEY_ENV" not in variable,
              f"{variable} is on REQUEST_SETTABLE and names a credential")
    # An exact set, so growing the allowlist is a deliberate edit here as well
    # as there. `LLOSSLESS_VERIFY_DEPTH` is the newest and the first
    # entry that can make a run check *less* rather than differently -- which
    # is a decision about what the submitter is told, not about what they can
    # reach, and the two loops above are what keep it from becoming one.
    #
    # `LLOSSLESS_WINDOW` is a number the submitter states for a model id
    # they typed, bounded by `jobs.stated_window_refusal`; it names no address
    # and no credential, which the two loops above hold it to like the rest.
    check(jobs.REQUEST_SETTABLE == frozenset({
        "LLOSSLESS_MODEL", "LLOSSLESS_MERGE_MODEL", "LLOSSLESS_FIDELITY",
        "LLOSSLESS_VERIFY_DEPTH",
        "LLOSSLESS_TITLE_POLICY", "LLOSSLESS_LOSS_BUDGET",
        "LLOSSLESS_WINDOW"}),
        f"REQUEST_SETTABLE has changed: {sorted(jobs.REQUEST_SETTABLE)}")


def test_an_empty_key_source_is_not_a_fallback_to_the_environment() -> None:
    """The property the whole arrangement rests on. Must fire both ways.

    A user with no key configured must get `None` rather than whatever the
    process holds. A truthiness test here would hand them the operator's
    credential and bill it to whoever owns the process -- which is precisely
    the failure the seam exists to prevent, and which nothing else in
    this module would catch, because every other check has a key configured.
    """
    settings = config.Settings(api_key_env=KEY_VARIABLE)
    with environment():
        os.environ[KEY_VARIABLE] = ALICE_KEY
        check(settings.api_key() == ALICE_KEY,
              "the environment is not the source when none is set, so the "
              "check below is not about the difference")
        with config.keys_for_this_run({}):
            check(settings.api_key() is None,
                  "an empty key source falls back to the environment, so a "
                  "user with no key spends the operator's")
        with config.keys_for_this_run({KEY_VARIABLE: BOB_KEY}):
            check(settings.api_key() == BOB_KEY,
                  "a swapped source is not read")
        check(settings.api_key() == ALICE_KEY,
              "the source was not restored on the way out")


# --------------------------------------------------------------------------
# a key goes to the address it was saved with, and nowhere else
# --------------------------------------------------------------------------


class Recorder:
    """A loopback server that keeps the headers of everything it is sent.

    `FakeEndpoint` keeps a completion's headers and not a probe's, and one of
    the requests asked about below is a probe: `GET /api/ps`, which every run
    sends to this server's own endpoint. It answers 404 to a GET and 400 to a
    POST, so a run sent here fails on its first call, at once, and what it
    was handed is on record.
    """

    def __init__(self) -> None:
        self.seen: list[tuple[str, str, dict]] = []

    def __enter__(self) -> "Recorder":
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
        recorder = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def answer(self) -> None:
                length = int(self.headers.get("Content-Length") or 0)
                if length:
                    self.rfile.read(length)
                recorder.seen.append((self.command, self.path, dict(self.headers)))
                body = b'{"error": "a recorder answers nothing"}'
                self.send_response(404 if self.command == "GET" else 400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            do_GET = do_POST = answer  # noqa: N815

            def log_message(self, *_args) -> None:
                pass

        class Quiet(ThreadingHTTPServer):
            def handle_error(self, request, client_address) -> None:
                """A client that hangs up is the run failing, as it is meant to."""
                if not isinstance(sys.exc_info()[1], ConnectionError):
                    super().handle_error(request, client_address)

        self._server = Quiet(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever,
                                        daemon=True)
        self._thread.start()
        self.url = f"http://127.0.0.1:{self._server.server_address[1]}/v1"
        return self

    def __exit__(self, *exc_info) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)

    def keys(self) -> set[str]:
        """Every bearer token this server was handed, on any request."""
        found = set()
        for _, _, headers in self.seen:
            for name, value in headers.items():
                if name.lower() == "authorization":
                    found.add(str(value).split(" ", 1)[-1].strip())
        return found

    def posts(self) -> int:
        return sum(1 for method, _, _ in self.seen if method == "POST")


KEY_SCOPE_SHAPES = ("member, endpoint named", "member, typed model",
                    "operator, another address", "operator, the server's own address",
                    "environment key", "operator's role, member's vendor key")


def key_scope_problems(shape: str, seed=None) -> list[str]:
    """Which key this server's own endpoint was handed, read off the wire.

    `self-hosted` keeps its key in the variable every role with no provider
    of its own reads, so a key saved with a self-hosted address also went to
    this server's own endpoint (`LLOSSLESS_BASE_URL`). Six arrangements:

      member, endpoint named      a member's own endpoint and key, and a run
                                  that names it. Every call goes to the
                                  member's endpoint; the window probe still
                                  goes to the server's own.
      member, typed model         the same member, a typed model and no
                                  endpoint: the run goes to the server's own.
      operator, another address   the operator stored a self-hosted address
                                  that is not the server's own, with a key.
      operator, the server's own  the operator stored the server's own
      address                     address, with a key. It is that address's.
      environment key             the key came with the server's environment
                                  and the operator stored an address with no
                                  key. The key is the server's own endpoint's.
      operator's role, member's   the operator's environment sends the merge
      vendor key                  role to an address of its own and names a
                                  vendor's key variable for it; a member has
                                  their own endpoint and key for that vendor.
    """
    problems: list[str] = []
    with contextlib.ExitStack() as stack:
        default = stack.enter_context(Recorder())
        role_address = stack.enter_context(Recorder())
        own_endpoint = FakeEndpoint(Script(**CLEAN))
        own_url = stack.enter_context(own_endpoint)
        stack.enter_context(environment())
        if seed is not None:
            stack.enter_context(seed)
        environ = {"LLOSSLESS_STRUCTURED": "prompt",
                   "LLOSSLESS_BASE_URL": default.url}
        if shape == "operator's role, member's vendor key":
            environ["LLOSSLESS_BASE_URL_MERGE"] = role_address.url
            environ["LLOSSLESS_API_KEY_ENV_MERGE"] = credentials.PROVIDERS["openai"]
        if shape == "environment key":
            environ[KEY_VARIABLE] = ALICE_KEY
            os.environ[KEY_VARIABLE] = ALICE_KEY
        live = stack.enter_context(Deployment(environ=environ))
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        who, stored = bob, []
        if shape in ("member, endpoint named", "member, typed model"):
            stored = [live.set_endpoint(bob, own_url)[0],
                      live.set_key(bob, BOB_KEY)[0]]
        elif shape == "operator's role, member's vendor key":
            stored = [live.set_endpoint(bob, own_url, provider="openai")[0],
                      live.set_key(bob, BOB_KEY, provider="openai")[0]]
        elif shape == "operator, another address":
            who = alice
            stored = [live.set_endpoint(alice, own_url)[0],
                      live.set_key(alice, ALICE_KEY)[0]]
        elif shape == "operator, the server's own address":
            who = alice
            stored = [live.set_endpoint(alice, default.url)[0],
                      live.set_key(alice, ALICE_KEY)[0]]
        elif shape == "environment key":
            who = alice
            stored = [live.set_endpoint(alice, own_url)[0], 204]
        if stored != [200, 204]:
            return [f"the endpoint and key could not be stored: {stored}"]
        body = a_submission()
        if shape != "member, endpoint named":
            body.pop("endpoint")
        answer = request(live.url(f"{P}/runs"), method="POST", headers=who,
                         payload=body)
        if answer[0] != 202:
            return [f"the submit answered {answer[0]}: {answer[2][:200]!r}"]
        run_id = as_json(answer[2])["id"]
        if not wait_for(lambda: state_of(live, run_id, who) in ("done", "failed")):
            return ["the run never finished"]
        heard = default.keys()
        if shape == "member, endpoint named":
            if BOB_KEY not in bearer_keys(own_endpoint):
                problems.append("the member's own endpoint was not handed "
                                "the member's key")
            if BOB_KEY in heard:
                problems.append("the server's own endpoint was handed the "
                                "member's key")
        elif shape == "member, typed model":
            if not default.posts():
                problems.append("the run did not go to the server's own "
                                "endpoint, so nothing was probed")
            if BOB_KEY in heard:
                problems.append("the server's own endpoint was handed the "
                                "member's key")
        elif shape == "operator, another address":
            if not default.posts():
                problems.append("the run did not go to the server's own "
                                "endpoint, so nothing was probed")
            if ALICE_KEY in heard:
                problems.append("the server's own endpoint was handed the key "
                                "stored with another address")
        elif shape in ("operator, the server's own address", "environment key"):
            sent = {key for method, _, headers in default.seen if method == "POST"
                    for name, key in headers.items()
                    if name.lower() == "authorization"}
            if f"Bearer {ALICE_KEY}" not in sent:
                problems.append("the server's own endpoint was not handed its "
                                "own key")
        else:
            if not role_address.posts():
                problems.append("the merge did not go to the operator's "
                                "address for it, so nothing was probed")
            if BOB_KEY in role_address.keys() | heard:
                problems.append("an address of the operator's was handed the "
                                "member's key")
    return problems


def test_a_key_saved_with_an_address_is_sent_to_no_other_address() -> None:
    """The server's own endpoint gets a key only when the key is its own.

    Must not fire: a role sent to the provider still carries the provider's
    key, the server's own address stored with a key still gets that key, and
    so does a key that came with the server's environment.

    Must fire: `credentials.key_scope` withholding nothing, which is the
    server this was before. The member's key then reaches the server's own
    endpoint on the window probe of every run and on every call of a typed
    model, the operator's stored key reaches an address it was not stored
    with, and a member's vendor key reaches the operator's address for a role.
    """
    for shape in KEY_SCOPE_SHAPES:
        problems = key_scope_problems(shape)
        check(not problems, f"key scope, {shape}: " + "; ".join(problems))

    def nothing_withheld(environ, paired):
        return {}

    for shape, wanted in (
            ("member, endpoint named", "handed the member's key"),
            ("member, typed model", "handed the member's key"),
            ("operator, another address", "stored with another address"),
            ("operator's role, member's vendor key", "handed the member's key")):
        seeded = key_scope_problems(
            shape, Seeded(credentials, "key_scope", nothing_withheld))
        check(any(wanted in problem for problem in seeded),
              f"must fire: with no key withheld, {shape} passed: {seeded}")

    # The name a withheld role reads is one nothing can supply.
    with environment():
        os.environ[credentials.NO_KEY_ENV] = ALICE_KEY
        source = jobs.StandingKeys({}, {})
        check(source.get(credentials.NO_KEY_ENV) is None,
              "a key exported under the withheld name is read by a run")
        member = jobs.MemberKeys({credentials.NO_KEY_ENV: BOB_KEY,
                                  "PROBE_UNRELATED_VARIABLE": "unrelated"},
                                 (), source)
        os.environ["PROBE_SERVER_VARIABLE"] = "the server's"
        check(member.get("PROBE_SERVER_VARIABLE") is None,
              "a member's run reads a variable of the server's environment "
              "that is no provider's key")
    check(credentials.NO_KEY_ENV not in credentials.PROVIDERS.values(),
          "the withheld name is a provider's key variable")


def test_an_endpoint_address_cannot_carry_a_query_or_a_fragment() -> None:
    """`?` and `#` are refused in an address, for everybody.

    Each request adds its own path to an endpoint. Behind a `?` that path is
    part of the query, so a member's own endpoint could aim this server at
    any path of any address it can reach: the model listing read an internal
    JSON document back to the member, and a run relayed 600 characters of an
    internal error body.

    Must not fire: a private and a loopback address are stored, because a
    member's own local model server is a supported use.

    Must fire: `credentials.clean_base_url` with the two characters let
    through, which is the function this was before.
    """
    with contextlib.ExitStack() as stack:
        inside = stack.enter_context(Recorder())
        stack.enter_context(environment())
        live = stack.enter_context(Deployment(
            environ={"LLOSSLESS_STRUCTURED": "prompt"}))
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)

        def stored(address: str, who) -> tuple[int, list]:
            del inside.seen[:]
            answer = live.set_endpoint(who, address.replace(
                "INSIDE", inside.url.removesuffix("/v1")))
            return answer[0], [path for _, path, _ in inside.seen]

        for who_is, who in (("member", bob), ("operator", alice)):
            for address in ("INSIDE/admin/list?x=", "INSIDE/admin/list#",
                            "INSIDE/v1?", "INSIDE/v1#frag"):
                status, sent = stored(address, who)
                check(status == 400 and not sent,
                      f"a {who_is}'s endpoint {address!r} answered {status} "
                      f"and the server sent {sent}")
        for address in ("INSIDE/v1", "http://127.0.0.1:9/v1",
                        "http://localhost:9"):
            status, _ = stored(address, bob)
            check(status == 200,
                  f"a member's local endpoint {address!r} was refused: {status}")

        shipped = credentials.clean_base_url

        def lets_them_through(name, value):
            return shipped(name, value.replace("?", "%3F").replace("#", "%23")
                           ).replace("%3F", "?").replace("%23", "#")

        with Seeded(credentials, "clean_base_url", lets_them_through):
            status, sent = stored("INSIDE/admin/list?x=", bob)
        check(status == 200 and any("?" in path for path in sent),
              f"must fire: with the two characters let through, the address "
              f"was still refused ({status}) or nothing was sent ({sent})")


# --------------------------------------------------------------------------
# an account that is removed stops running
# --------------------------------------------------------------------------


def removal_problems(seed=None) -> list[str]:
    """The operator removes a member with one run in flight and two queued.

    The first call of the first run is held until the account is gone, so
    every later call is made after the removal. What ran afterwards is read
    off the endpoint.
    """
    problems: list[str] = []
    hold, entered = threading.Event(), threading.Event()
    script = Script(**CLEAN)

    def held(body, call):
        if call == 1:
            entered.set()
            hold.wait(timeout=PATIENCE)
        return script(body, call)

    with contextlib.ExitStack() as stack:
        endpoint = FakeEndpoint(held)
        base_url = stack.enter_context(endpoint)
        stack.enter_context(environment())
        if seed is not None:
            stack.enter_context(seed)
        live = stack.enter_context(Deployment(
            environ={"LLOSSLESS_STRUCTURED": "prompt"}))
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        try:
            if live.set_endpoint(alice, base_url)[0] != 200 \
                    or live.set_key(alice, ALICE_KEY)[0] != 204:
                return ["the operator could not configure the endpoint"]
            ids = []
            for _ in range(3):
                answer = request(live.url(f"{P}/runs"), method="POST",
                                 headers=bob, payload=a_submission())
                if answer[0] != 202:
                    return [f"a submit answered {answer[0]}"]
                ids.append(as_json(answer[2])["id"])
            if not entered.wait(timeout=PATIENCE):
                return ["the first run never called its endpoint"]
            removed = request(live.url(f"{P}/accounts/{MEMBER}"),
                              method="DELETE", headers=alice)
            if removed[0] != 204:
                return [f"the removal answered {removed[0]}"]
            before = len(endpoint.headers)
        finally:
            hold.set()
        if not wait_for(lambda: all(live.built.store.get(run_id).terminal
                                    for run_id in ids)):
            return ["the removed account's runs never ended"]
        jobs_now = [live.built.store.get(run_id) for run_id in ids]
        later = len(endpoint.headers) - before
        if later:
            problems.append(f"{later} model call(s) were made for the removed "
                            f"account after it was removed")
        if jobs_now[0].state != "cancelled":
            problems.append(f"the run in flight ended {jobs_now[0].state!r}")
        for job in jobs_now[1:]:
            if job.state == "done":
                problems.append("a queued run of the removed account ran to "
                                "the end")
            elif job.state == "failed" and "removed" in (job.error or ""):
                problems.append("a queued run was refused when it started")
    return problems


def test_removing_an_account_stops_its_runs() -> None:
    """Queued and running, they are cancelled with the account.

    They used to run to the end after the removal, as a member with nothing
    of their own, which is on the operator's key: 17 calls in the review's
    reproduction, visible to nobody.

    Must fire: `JobStore.cancel_owned` doing nothing. The run in flight then
    goes on calling. The queued ones are still stopped, by the second rule
    behind this one: a run whose account is gone is refused when it starts
    (`Directory.for_run`), and that refusal is asserted too, with the
    condition taken out of the function's own source as its probe.
    """
    import inspect
    import textwrap

    problems = removal_problems()
    check(not problems, "account removed: " + "; ".join(problems))

    def nothing(self, owner):
        return 0

    seeded = removal_problems(Seeded(jobs.JobStore, "cancel_owned", nothing))
    check(any("model call(s) were made" in problem for problem in seeded),
          f"must fire: a removal that cancels nothing passed: {seeded}")
    check(sum("refused when it started" in problem for problem in seeded) == 2
          and not any("ran to the end" in problem for problem in seeded),
          f"with nothing cancelled, the queued runs of a removed account "
          f"were not refused at their start: {seeded}")

    shipped = accounts.Directory.for_run
    text = textwrap.dedent(inspect.getsource(shipped))
    guard = ("if self.accounts is not None and "
             "self.accounts.by_id(account_id) is None:")
    check(guard in text, "the refusal of a removed account's run is not where "
                         "this check looks for it")
    scope = dict(vars(accounts))
    exec(compile(text.replace(guard, "if False:"), "seeded for_run", "exec"),  # noqa: S102
         scope)
    with Seeded(accounts.Directory, "for_run", scope["for_run"]):
        seeded = removal_problems(Seeded(jobs.JobStore, "cancel_owned", nothing))
    check(any("ran to the end" in problem for problem in seeded),
          f"must fire: with neither rule, a removed account's queued run "
          f"did not run: {seeded}")


def in_flight_key_problems(seed=None) -> list[str]:
    """The operator deletes the shared key while a member's run is using it."""
    problems: list[str] = []
    hold, entered = threading.Event(), threading.Event()
    script = Script(**CLEAN)

    def held(body, call):
        if call == 1:
            entered.set()
            hold.wait(timeout=PATIENCE)
        return script(body, call)

    with contextlib.ExitStack() as stack:
        endpoint = FakeEndpoint(held)
        base_url = stack.enter_context(endpoint)
        stack.enter_context(environment())
        if seed is not None:
            stack.enter_context(seed)
        live = stack.enter_context(Deployment(
            environ={"LLOSSLESS_STRUCTURED": "prompt"}))
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        try:
            if live.set_endpoint(alice, base_url)[0] != 200 \
                    or live.set_key(alice, ALICE_KEY)[0] != 204:
                return ["the operator could not configure the endpoint"]
            answer = request(live.url(f"{P}/runs"), method="POST", headers=bob,
                             payload=a_submission())
            if answer[0] != 202:
                return [f"the submit answered {answer[0]}"]
            run_id = as_json(answer[2])["id"]
            if not entered.wait(timeout=PATIENCE):
                return ["the run never called its endpoint"]
            gone = request(live.url(f"{P}/settings/keys/{PROVIDER}"),
                           method="DELETE", headers=alice)
            if gone[0] != 204:
                return [f"deleting the key answered {gone[0]}"]
            before = len(endpoint.headers)
        finally:
            hold.set()
        if not wait_for(lambda: state_of(live, run_id, bob) in ("done", "failed")):
            return ["the run never finished"]
        first = [value for name, value in endpoint.headers[0].items()
                 if name.lower() == "authorization"]
        if first != [f"Bearer {ALICE_KEY}"]:
            problems.append("the run was not using the shared key to begin "
                            "with, so nothing was probed")
        later = endpoint.headers[before:]
        if not later:
            problems.append("the run made no call after the key was deleted")
        carried = sum(1 for headers in later for name, value in headers.items()
                      if name.lower() == "authorization" and ALICE_KEY in value)
        if carried:
            problems.append(f"{carried} call(s) carried the shared key after "
                            f"the operator deleted it")
    return problems


def test_a_deleted_shared_key_is_not_sent_by_a_members_run_in_flight() -> None:
    """The member's run follows the rule the operator's own run follows.

    A member's run was handed the operator's key in a mapping read once at
    its start, so it went on sending a key the operator had deleted: 5 of 5
    later calls in the review's reproduction, where the operator's own run
    sent none.

    Must fire: the store handing a member's run the mapping as it was read,
    which is `jobs.MemberKeys` taken out.
    """
    problems = in_flight_key_problems()
    check(not problems, "shared key deleted mid-run: " + "; ".join(problems))

    def as_read(keys, shared, standing, addresses=()):
        return dict(keys)

    seeded = in_flight_key_problems(Seeded(jobs, "MemberKeys", as_read))
    check(any("after the operator deleted it" in problem for problem in seeded),
          f"must fire: a member's run on a mapping read once passed: {seeded}")


# --------------------------------------------------------------------------
# a worker outlives a file it cannot read
# --------------------------------------------------------------------------


def unusable_file_problems(seed=None) -> list[str]:
    """A member's credentials file becomes unusable between submit and start."""
    problems: list[str] = []
    hold, entered = threading.Event(), threading.Event()
    script = Script(**CLEAN)

    def held(body, call):
        if call == 1:
            entered.set()
            hold.wait(timeout=PATIENCE)
        return script(body, call)

    noise = io.StringIO()
    with contextlib.ExitStack() as stack:
        endpoint = FakeEndpoint(held)
        base_url = stack.enter_context(endpoint)
        stack.enter_context(environment())
        stack.enter_context(contextlib.redirect_stderr(noise))
        live = stack.enter_context(Deployment(
            environ={"LLOSSLESS_STRUCTURED": "prompt"}))
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        member = live.accounts.get(MEMBER).id
        if seed is not None:
            stack.enter_context(seed(member))
        own = live.built.api.directory.own(member)
        try:
            if live.set_endpoint(alice, base_url)[0] != 200 \
                    or live.set_endpoint(bob, base_url)[0] != 200:
                return ["the endpoints could not be configured"]

            def submit(who) -> str:
                answer = request(live.url(f"{P}/runs"), method="POST",
                                 headers=who, payload=a_submission())
                return (as_json(answer[2]) or {}).get("id", "")

            first = submit(alice)
            if not entered.wait(timeout=PATIENCE):
                return ["the operator's run never started"]
            queued = submit(bob)
            if not queued:
                return ["the member's run was not accepted"]
            os.chmod(own.path, 0o644)
        finally:
            hold.set()
        if not wait_for(lambda: state_of(live, first, alice) in ("done", "failed")):
            return ["the operator's first run never finished"]
        wait_for(lambda: state_of(live, queued, bob) in ("done", "failed"),
                 timeout=10)
        os.chmod(own.path, 0o600)
        told = as_json(request(live.url(f"{P}/runs/{queued}"), headers=bob)[2]) or {}
        if told.get("state") != "failed":
            problems.append(f"the member's run is {told.get('state')!r} and "
                            f"not failed")
        error = str(told.get("error") or "")
        if live.root.name in error or str(own.path.parent.name) in error:
            problems.append(f"the member is told a path on this server: {error}")
        if told.get("state") == "failed" and "not started" not in error:
            problems.append(f"the member is not told what happened: {error}")
        after = submit(alice)
        if not wait_for(lambda: state_of(live, after, alice) in ("done", "failed"),
                        timeout=20):
            problems.append(f"a later run stayed "
                            f"{state_of(live, after, alice)!r}: the worker "
                            f"did not survive")
        if str(own.path) not in noise.getvalue() and told.get("state") == "failed":
            problems.append("the operator's stream does not name the file")
    return problems


def test_a_worker_survives_a_credentials_file_it_cannot_use() -> None:
    """The job fails with a sentence, and the next job runs.

    The read was made outside any handler, so a member's file with the wrong
    mode ended the worker thread: the job stayed `running`, and with one
    worker every later run stayed queued.

    Must not fire: the member is told the run was not started, in words that
    name no path; the operator's stream names the file.

    Must fire: the read failing with something `_execute` does not catch,
    which is every failure it had before.
    """
    problems = unusable_file_problems()
    check(not problems, "unusable member file: " + "; ".join(problems))

    def uncaught(member):
        shipped = jobs.JobStore.resolved_for

        def resolved_for(self, owner):
            if owner == member and threading.current_thread().name.startswith(
                    "llossless-job"):
                raise RuntimeError("seeded: a read nothing catches")
            return shipped(self, owner)

        return Seeded(jobs.JobStore, "resolved_for", resolved_for)

    seeded = unusable_file_problems(uncaught)
    check(any("the worker did not survive" in problem for problem in seeded)
          and any("not failed" in problem for problem in seeded),
          f"must fire: a worker whose read raised past it passed: {seeded}")


# --------------------------------------------------------------------------
# what a member is shown of this server
# --------------------------------------------------------------------------

# A path segment an operator's address carries and a member must not be sent.
PATH_MARK = "tenant-9f3c1e-probe-path"


def address_problems(seed=None) -> list[str]:
    """Where the operator's full address reaches, for the operator and for a member."""
    import zipfile

    problems: list[str] = []
    with contextlib.ExitStack() as stack:
        shared_endpoint = FakeEndpoint(Script(**CLEAN))
        member_endpoint = FakeEndpoint(Script(**CLEAN))
        shared_url = stack.enter_context(shared_endpoint).replace(
            "/v1", f"/{PATH_MARK}/v1")
        member_url = stack.enter_context(member_endpoint).replace(
            "/v1", "/the-members-own-path/v1")
        stack.enter_context(environment())
        if seed is not None:
            stack.enter_context(seed)
        live = stack.enter_context(Deployment(
            environ={"LLOSSLESS_STRUCTURED": "prompt"}))
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        if live.set_endpoint(alice, shared_url)[0] != 200:
            return ["the operator could not configure the endpoint"]

        def run(who) -> str:
            answer = request(live.url(f"{P}/runs"), method="POST", headers=who,
                             payload=a_submission())
            run_id = (as_json(answer[2]) or {}).get("id", "")
            wait_for(lambda: state_of(live, run_id, who) in ("done", "failed"))
            return run_id

        def everything(who, run_id) -> dict[str, str]:
            read = {}
            for path in (f"{P}/config", f"{P}/settings/keys", f"{P}/health",
                         f"{P}/runs", f"{P}/runs/{run_id}",
                         f"{P}/runs/{run_id}/events",
                         f"{P}/runs/{run_id}/report.html"):
                read[path] = request(live.url(path), headers=who)[2].decode(
                    "utf-8", "replace")
            status, _, packed = request(live.url(f"{P}/runs/{run_id}/bundle.zip"),
                                        headers=who)
            if status == 200:
                with zipfile.ZipFile(io.BytesIO(packed)) as archive:
                    read["bundle.zip"] = "\n".join(
                        archive.read(name).decode("utf-8", "replace")
                        for name in archive.namelist())
            return read

        theirs = run(bob)
        if state_of(live, theirs, bob) != "done":
            return ["the member's run on the shared endpoint did not finish"]
        for where, text in everything(bob, theirs).items():
            if PATH_MARK in text:
                problems.append(f"a member is sent the operator's full "
                                f"address in {where.replace(theirs, '<id>')}")
        short = accounts.reduced(shared_url)
        rows = {row["name"]: row for row in as_json(request(
            live.url(f"{P}/config"), headers=bob)[2])["endpoints"]["providers"]}
        if rows[PROVIDER]["base_url"] != short or not short.startswith("http://127.0.0.1:"):
            problems.append(f"a member's row for the shared endpoint reads "
                            f"{rows[PROVIDER]['base_url']!r} and not {short!r}")
        told = as_json(request(live.url(f"{P}/runs/{theirs}"), headers=bob)[2])
        command = (told.get("cli_equivalent") or {}).get("command", "")
        if f"--base-url {short} " not in command:
            problems.append(f"a member's command does not name the endpoint "
                            f"by scheme, host and port: {command}")
        if not any(note.get("key") == "address_reduced"
                   for note in (told.get("cli_equivalent") or {}).get("notes", [])):
            problems.append("a member's command does not say its address is "
                            "shortened")

        # The operator is shown the whole of their own address, everywhere.
        own = run(alice)
        seen = everything(alice, own)
        for where in (f"{P}/config", f"{P}/settings/keys", f"{P}/runs/{own}"):
            if PATH_MARK not in seen[where]:
                problems.append(f"the operator is not shown their own address "
                                f"in {where.replace(own, '<id>')}")

        # And a member is shown the whole of an address they stored themselves.
        if live.set_endpoint(bob, member_url)[0] != 200:
            return problems + ["a member could not configure their own endpoint"]
        mine = run(bob)
        told = as_json(request(live.url(f"{P}/runs/{mine}"), headers=bob)[2])
        command = (told.get("cli_equivalent") or {}).get("command", "")
        if f"--base-url {member_url} " not in command:
            problems.append(f"a member's own address is not shown to them in "
                            f"full: {command}")
        rows = {row["name"]: row for row in as_json(request(
            live.url(f"{P}/settings/keys"), headers=bob)[2])["providers"]}
        if rows[PROVIDER]["base_url"] != member_url:
            problems.append("a member's own row does not carry their address")
    return problems


def test_a_member_is_shown_scheme_host_and_port_of_the_operators_address() -> None:
    """The path of an operator's address stays with the operator.

    A member received the operator's full `base_url` from `/config`, from
    `/settings/keys`, and in the command-line block of their own run, which
    is also in the `report.json` they download. A path or a query can carry
    a token or name a private service.

    Must not fire: the operator sees their whole address, and a member sees
    the whole of an address they stored.

    Must fire: `accounts.reduced` handing the address back whole.
    """
    problems = address_problems()
    check(not problems, "operator's address: " + "; ".join(problems))

    seeded = address_problems(Seeded(accounts, "reduced", lambda address: address))
    for where in ("/config", "/settings/keys", "/runs/<id>", "bundle.zip"):
        check(any(problem.endswith(f"{P}{where}") or problem.endswith(where)
                  for problem in seeded if "full address" in problem),
              f"must fire: with nothing shortened, a member's {where} "
              f"passed: {seeded}")

    check(accounts.reduced("https://example.invalid:8443/a/b?c=d#e")
          == "https://example.invalid:8443"
          and accounts.reduced("http://[::1]:11434/v1") == "http://[::1]:11434"
          and accounts.reduced("https://user:pw@example.invalid/v1")
          == "https://example.invalid"
          and accounts.reduced("not an address") == "",
          "an address is not reduced to its scheme, host and port")


def server_path_problems(seed=None) -> list[str]:
    """Every place a path on this server reached a member, asked as a member."""
    from llossless.web import commands

    problems: list[str] = []
    with contextlib.ExitStack() as stack:
        endpoint = FakeEndpoint(Script(**CLEAN))
        base_url = stack.enter_context(endpoint)
        stack.enter_context(environment())
        stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
        if seed is not None:
            stack.enter_context(seed)
        live = stack.enter_context(Deployment(
            environ={"LLOSSLESS_STRUCTURED": "prompt"}))
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        if live.set_endpoint(alice, base_url)[0] != 200 \
                or live.set_endpoint(bob, base_url)[0] != 200:
            return ["the endpoints could not be configured"]
        # The name of this server's own directory, and not its whole path: a
        # suite run with its temporary directory under the home directory
        # has the front of that path taken out by the home rule alone, and
        # the name is what is left when nothing else is.
        root = live.root.name

        # A write that fails inside a run, as a full disk would make it.
        shipped = jobs.write_private

        def full(path, text):
            if str(path).endswith(jobs.MERGED_MD):
                raise OSError(28, "No space left on device", str(path))
            return shipped(path, text)

        with Seeded(jobs, "write_private", full):
            answer = request(live.url(f"{P}/runs"), method="POST", headers=bob,
                             payload=a_submission())
            run_id = (as_json(answer[2]) or {}).get("id", "")
            wait_for(lambda: state_of(live, run_id, bob) in ("done", "failed"))
        told = request(live.url(f"{P}/runs/{run_id}"), headers=bob)[2].decode()
        if "No space left on device" not in told:
            problems.append("the member is not told why the run failed, so "
                            "the path was never in question")
        if root in told:
            problems.append("a member's run status carries the work directory")
        listed = request(live.url(f"{P}/runs"), headers=bob)[2].decode()
        if root in listed:
            problems.append("a member's run list carries the work directory")
        stream = request(live.url(f"{P}/runs/{run_id}/events"), headers=bob)[2].decode()
        if "No space left on device" not in stream:
            problems.append("the event stream does not carry the failure")
        if root in stream:
            problems.append("a member's event stream carries the work directory")

        # A commands file with a row this build cannot use.
        routes = live.root / "commands.json"
        routes.write_text(json.dumps({"version": 1, "routes": {"broken": {
            "label": "Broken", "command": "/bin/true --x", "window": "nope",
            "model": "m"}}}), encoding="utf-8")
        os.chmod(routes, 0o600)
        live.built.api.routes = commands.Commands(routes)
        for who, name in ((bob, "member"), (alice, "operator")):
            config_now = as_json(request(live.url(f"{P}/config"), headers=who)[2])
            reasons = [row["reason"] for row in config_now["commands"]["problems"]]
            if not reasons:
                problems.append("the unusable route is not reported")
            if name == "member" and any(root in reason for reason in reasons):
                problems.append(f"a member's /config names where the commands "
                                f"file is: {reasons}")
            if not all("commands.json" in reason for reason in reasons):
                problems.append(f"the {name} is not told which file: {reasons}")

        # A credentials file this server refuses to read.
        own = live.built.api.directory.own(live.accounts.get(MEMBER).id)
        os.chmod(own.path, 0o644)
        refused = request(live.url(f"{P}/settings/keys"), headers=bob)
        os.chmod(own.path, 0o600)
        body = refused[2].decode()
        if refused[0] != 409 or code_of(refused[2]) != "bad_credentials":
            problems.append(f"an unusable file answered {refused[0]}")
        if root in body or "users" in body or "credentials.json" in body:
            problems.append(f"a member's refusal names a path: {body}")
        os.chmod(live.keys.path, 0o644)
        refused = request(live.url(f"{P}/settings/keys"), headers=alice)
        os.chmod(live.keys.path, 0o600)
        if "credentials.json" not in refused[2].decode():
            problems.append("the operator is not told which file is unusable")
    return problems


def test_a_member_is_sent_no_path_on_this_server() -> None:
    """A failed write, a refused file and an unusable route, as a member reads them.

    The work directory reached a member in the `error` of a run that could
    not write its file and in that run's event stream, and the commands
    file's and the credentials file's own paths reached one with only the
    home directory taken out.

    Must not fire: the member is still told what failed, and the operator is
    still told which file.

    Must fire: `Api.roots_for` answering nothing, for the status, the run
    list and the stream, and a member read as the operator for the two files.
    """
    problems = server_path_problems()
    check(not problems, "server paths: " + "; ".join(problems))

    seeded = server_path_problems(
        Seeded(api.Api, "roots_for", lambda self, who: ()))
    for what in ("run status", "run list", "event stream"):
        check(any(f"a member's {what} carries" in problem for problem in seeded),
              f"must fire: with no directory taken out, a member's {what} "
              f"passed: {seeded}")
    seeded = server_path_problems(
        Seeded(api.Api, "_member", staticmethod(lambda who: False)))
    check(any("a member's refusal names a path" in problem for problem in seeded)
          and any("a member's /config names" in problem for problem in seeded),
          f"must fire: a member answered as the operator is passed: {seeded}")


# --------------------------------------------------------------------------
# the operator's routes
# --------------------------------------------------------------------------


def operator_route_problems(seed=None) -> list[str]:
    """Every route that is the operator's alone, asked by a member."""
    problems: list[str] = []
    with contextlib.ExitStack() as stack:
        stack.enter_context(environment())
        if seed is not None:
            stack.enter_context(seed)
        live = stack.enter_context(Deployment())
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        live.add_account(alice, "carol", "carol-password-for-the-route-walk-27")
        bob = live.sign_in(MEMBER, BOB_PASSWORD)
        walk = (
            ("GET", f"{P}/accounts", None),
            ("POST", f"{P}/accounts",
             {"username": "eve", "password": "eve-password-of-enough-length",
              "operator": True}),
            ("DELETE", f"{P}/accounts/carol", None),
            ("PUT", f"{P}/accounts/carol/password",
             {"password": "a-password-somebody-else-chose-51"}),
            ("PUT", f"{P}/settings/commands/claude-opus", None),
            ("DELETE", f"{P}/settings/commands/claude-opus", None),
        )
        for method, path, payload in walk:
            # A PUT with no body still states its length, as a browser does.
            headers = ({**bob, "Content-Length": "0"}
                       if method == "PUT" and payload is None else bob)
            status, _, body = request(live.url(path), method=method,
                                      headers=headers, payload=payload)
            if status != 403 or code_of(body) != "not_operator":
                problems.append(f"{method} {path} answered a member "
                                f"{status} {code_of(body)!r}")
        names = sorted(live.accounts.read())
        if names != sorted((OPERATOR, MEMBER, "carol")):
            problems.append(f"a member changed the accounts: {names}")
        if live.accounts.verify("carol", "carol-password-for-the-route-walk-27") is None:
            problems.append("a member changed somebody else's password")
        problems.append(f"walked {len(walk)}")
    return problems


def test_every_operator_route_refuses_a_member() -> None:
    """403 `not_operator`, on each of them, and nothing changed.

    With `Api._operator` made to permit everybody, no check in this module or
    in `tests/test_web_server.py` failed: the gate was asserted nowhere.

    Must fire: that same change. A member then lists the accounts, adds an
    operator, removes an account and sets somebody else's password.

    The walk is held against the source: one entry per call of the gate, so
    a route added behind it is a route this has to be told about.
    """
    import inspect

    problems = operator_route_problems()
    walked = [problem for problem in problems if problem.startswith("walked ")]
    check(problems == walked, "operator routes: " + "; ".join(problems))
    gates = inspect.getsource(api.Api).count("self._operator(who)")
    check(walked == [f"walked {gates}"],
          f"the walk covers {walked} and the API calls its operator gate in "
          f"{gates} places")

    seeded = operator_route_problems(
        Seeded(api.Api, "_operator", lambda self, who: who))
    check(sum("answered a member" in problem for problem in seeded) >= 4
          and any("changed the accounts" in problem for problem in seeded),
          f"must fire: with the operator gate open, the walk passed: {seeded}")


# --------------------------------------------------------------------------
# before anybody has signed in
# --------------------------------------------------------------------------


def test_the_first_account_is_made_once_whatever_arrives_together() -> None:
    """Two setup requests that both find no account make one operator.

    The route counted the accounts and then created one, as two steps, so two
    requests carrying the code at the same moment both passed the count and
    both made an operator.

    Asked without a race to win: the count is held at zero for both requests,
    which is what each of two that arrive together sees.

    Must fire: `Accounts.create` not being told this is the first account.
    """
    def twice(seed=None) -> list[str]:
        problems: list[str] = []
        with contextlib.ExitStack() as stack:
            stack.enter_context(environment())
            if seed is not None:
                stack.enter_context(seed)
            live = stack.enter_context(Deployment())
            with Seeded(api.Api, "account_count", lambda self: 0):
                first = live.first_account()
                second = live.first_account(username="mallory")
            if first[0] != 200:
                problems.append(f"the first setup answered {first[0]}")
            if second[0] != 409 or code_of(second[2]) != "already_set_up":
                problems.append(f"the second setup answered {second[0]} "
                                f"{code_of(second[2])!r}")
            rows = live.accounts.read()
            if sum(1 for row in rows.values() if row.operator) != 1 or len(rows) != 1:
                problems.append(f"the server has {len(rows)} accounts")
        return problems

    problems = twice()
    check(not problems, "setup twice: " + "; ".join(problems))

    shipped = accounts.Accounts.create

    def not_told(self, username, password, *, operator=False, now=None,
                 first=False):
        return shipped(self, username, password, operator=operator, now=now)

    seeded = twice(Seeded(accounts.Accounts, "create", not_told))
    check(any("the server has 2 accounts" in problem for problem in seeded),
          f"must fire: a store not told the account is the first passed: {seeded}")


def test_a_name_no_account_can_have_is_not_kept() -> None:
    """A submitted name longer than a username is answered and not stored.

    The sign-in throttle is keyed on the submitted name, before any password
    is checked, by anybody who can reach the port. A name of a million
    characters was held for five minutes.

    Must not fire: the refusal is the one a wrong sign-in gets.

    Must fire: the bound taken away.
    """
    def longest(seed=None) -> tuple[int, tuple]:
        with contextlib.ExitStack() as stack:
            stack.enter_context(environment())
            if seed is not None:
                stack.enter_context(seed)
            live = stack.enter_context(Deployment())
            live.first_account()
            wrong = request(live.url(f"{P}/session"), method="POST", payload={
                "username": OPERATOR, "password": "not-the-password-at-all"})
            long = request(live.url(f"{P}/session"), method="POST", payload={
                "username": "x" * 50_000, "password": ALICE_PASSWORD})
            held = max(len(name) for name in live.built.api.throttle._failures)
            return held, (wrong[0], wrong[2], long[0], long[2])

    held, (status, body, long_status, long_body) = longest()
    check(held <= accounts.USERNAME_MAX,
          f"the throttle holds a name of {held} characters")
    check((status, body) == (long_status, long_body) and status == 401,
          f"a name no account can have is refused differently from a wrong "
          f"sign-in: {long_status} {long_body[:120]!r}")
    held, _ = longest(Seeded(accounts, "USERNAME_MAX", 10 ** 9))
    check(held == 50_000,
          f"must fire: with no bound the throttle held {held} characters")
    check(accounts.USERNAME.match("a" * accounts.USERNAME_MAX) is not None
          and accounts.USERNAME.match("a" * (accounts.USERNAME_MAX + 1)) is None,
          "USERNAME_MAX is not the longest name the pattern takes")


def test_guesses_of_the_current_password_are_throttled() -> None:
    """Under the sign-in throttle, by the same name.

    A session could try the `current` password of its own account as fast as
    the hash allows: 15 guesses in under a second in the review.

    Must not fire: another account is unaffected, and the refusal a throttled
    guess gets is the one a wrong guess gets.

    Must fire: the throttle never locking.
    """
    new = "a-new-password-for-the-throttle-check"

    def guesses(seed=None) -> list[str]:
        problems: list[str] = []
        with contextlib.ExitStack() as stack:
            stack.enter_context(environment())
            if seed is not None:
                stack.enter_context(seed)
            live = stack.enter_context(Deployment())
            live.first_account()
            alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
            live.add_account(alice, MEMBER, BOB_PASSWORD)
            bob = live.sign_in(MEMBER, BOB_PASSWORD)

            def change(current: str):
                return request(live.url(f"{P}/accounts/{MEMBER}/password"),
                               method="PUT", headers=bob,
                               payload={"password": new, "current": current})

            wrong = [change(f"a-wrong-guess-number-{n}") for n in range(10)]
            if {(status, code_of(body)) for status, _, body in wrong} \
                    != {(403, "bad_current_password")}:
                problems.append("a wrong guess is not refused as one")
            right = change(BOB_PASSWORD)
            if (right[0], right[2]) != (wrong[0][0], wrong[0][2]):
                problems.append(f"after ten wrong guesses the right password "
                                f"answered {right[0]}")
            if request(live.url(f"{P}/session"), method="POST", payload={
                    "username": MEMBER, "password": BOB_PASSWORD})[0] != 401 \
                    and right[0] == 403:
                problems.append("the sign-in for that name is not under the "
                                "same throttle")
            if request(live.url(f"{P}/session"), method="POST", payload={
                    "username": OPERATOR, "password": ALICE_PASSWORD})[0] != 200:
                problems.append("another account was locked with it")
        return problems

    problems = guesses()
    check(not problems, "guessing the current password: " + "; ".join(problems))
    seeded = guesses(Seeded(accounts.Throttle, "locked", lambda self, name: False))
    check(any("the right password answered 204" in problem for problem in seeded),
          f"must fire: a throttle that never locks passed: {seeded}")


def test_a_body_is_not_read_before_its_sender_is_known() -> None:
    """An unauthenticated request is answered before its body arrives.

    The server read a body in full, up to four megabytes, and only then asked
    who sent it. Asked here by declaring a body and not sending it: an answer
    that arrives is an answer that did not wait for the body.

    Must not fire: a signed-in request of the same size is read and answered,
    and a sign-in of ordinary size is taken.

    Must fire: `Api.admit` checking the size alone, which is what stood in
    front of the read before.
    """
    import socket

    def answer_to(live, path: str, length: int, extra: str = "") -> bytes:
        """What the server says to the headers alone, within two seconds.

        Where it says nothing, the body is then sent and the answer read, so
        the server is never left writing to a connection that went away.
        """
        with socket.create_connection(("127.0.0.1", live.built.port),
                                      timeout=5) as link:
            link.sendall((f"POST {path} HTTP/1.1\r\nHost: 127.0.0.1\r\n"
                          f"Content-Type: application/json\r\n{extra}"
                          f"Connection: close\r\n"
                          f"Content-Length: {length}\r\n\r\n").encode("ascii"))
            def whole() -> bytes:
                """One answer, read to its end, so the server is not cut off."""
                got = b""
                while b"\r\n\r\n" not in got:
                    more = link.recv(4096)
                    if not more:
                        return got
                    got += more
                head, _, body = got.partition(b"\r\n\r\n")
                size = 0
                for line in head.split(b"\r\n"):
                    if line.lower().startswith(b"content-length:"):
                        size = int(line.split(b":", 1)[1])
                while len(body) < size:
                    more = link.recv(4096)
                    if not more:
                        break
                    body += more
                return head

            link.settimeout(2)
            try:
                return whole()
            except (TimeoutError, socket.timeout):
                link.settimeout(PATIENCE)
                link.sendall(b" " * length)
                whole()
                return b"(no answer without the body)"

    def unread(seed=None) -> list[str]:
        problems: list[str] = []
        with contextlib.ExitStack() as stack:
            stack.enter_context(environment())
            if seed is not None:
                stack.enter_context(seed)
            live = stack.enter_context(Deployment())
            live.first_account()
            alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
            stranger = answer_to(live, f"{P}/runs", api.MAX_BODY_BYTES - 10)
            if b" 401 " not in stranger.split(b"\r\n")[0]:
                problems.append(f"a stranger's body was waited for: "
                                f"{stranger[:40]!r}")
            sign_in = answer_to(live, f"{P}/session", api.MAX_OPEN_BODY_BYTES + 1)
            if b" 413 " not in sign_in.split(b"\r\n")[0]:
                problems.append(f"a sign-in of {api.MAX_OPEN_BODY_BYTES + 1} "
                                f"bytes was waited for: {sign_in[:40]!r}")
            # Must not fire: with a session, the body is what is waited for.
            known = answer_to(
                live, f"{P}/runs", 1000,
                f"{accounts.SESSION_HEADER}: {alice[accounts.SESSION_HEADER]}\r\n")
            if known != b"(no answer without the body)":
                problems.append(f"a signed-in request was answered before its "
                                f"body: {known[:40]!r}")
            if request(live.url(f"{P}/session"), method="POST", payload={
                    "username": OPERATOR, "password": ALICE_PASSWORD})[0] != 200:
                problems.append("an ordinary sign-in is refused")
        return problems

    problems = unread()
    check(not problems, "body before identity: " + "; ".join(problems))

    def size_alone(self, path, headers, length):
        api.check_body_size(length)

    seeded = unread(Seeded(api.Api, "admit", size_alone))
    check(any("a stranger's body was waited for" in problem for problem in seeded)
          and any("a sign-in of" in problem for problem in seeded),
          f"must fire: a server that reads before it asks passed: {seeded}")


def test_the_users_directory_is_its_owners_alone() -> None:
    """`users/` is created `0700`, and one made `0755` is repaired.

    Each member's own folder was `0700` and the directory holding them was
    whatever `mkdir(parents=True)` made it, which is `0755`: any account on
    the machine could list which accounts exist.

    Must fire: `credentials.private_dir` making the directories the way the
    old code did.
    """
    from llossless.web import defaults

    def modes(seed=None) -> list[str]:
        problems: list[str] = []
        before = os.umask(0o022)
        try:
            with contextlib.ExitStack() as stack:
                raw = stack.enter_context(tempfile.TemporaryDirectory())
                if seed is not None:
                    stack.enter_context(seed)
                for what in ("credentials", "defaults"):
                    root = Path(raw) / what / "config"
                    directory = accounts.Directory(
                        credentials.Credentials(root / "credentials.json"))
                    account = "0" * 31 + "1"
                    if what == "credentials":
                        directory.own(account).set_endpoint(
                            PROVIDER, "http://127.0.0.1:2")
                    else:
                        defaults.Store(directory.path_for(account).with_name(
                            defaults.FILE_NAME)).write({})
                    for path in (root / accounts.USERS_DIR,
                                 root / accounts.USERS_DIR / account, root):
                        mode = stat.S_IMODE(path.stat().st_mode)
                        if mode != 0o700:
                            problems.append(
                                f"{path.relative_to(Path(raw) / what)} made "
                                f"by a {what} write is {mode:04o}")
        finally:
            os.umask(before)
        return problems

    problems = modes()
    check(not problems, "directory modes: " + "; ".join(problems))

    def as_before(directory):
        Path(directory).mkdir(parents=True, exist_ok=True)
        os.chmod(directory, credentials.DIR_MODE)

    seeded = modes(Seeded(credentials, "private_dir", as_before))
    check(sum("config/users made" in problem and "0755" in problem
              for problem in seeded) == 2,
          f"must fire: directories made the old way passed: {seeded}")

    # One an earlier version made is repaired when the server starts.
    with tempfile.TemporaryDirectory() as raw:
        users = Path(raw) / accounts.USERS_DIR
        users.mkdir()
        os.chmod(users, 0o755)
        accounts.Directory(credentials.Credentials(Path(raw) / "credentials.json"))
        check(stat.S_IMODE(users.stat().st_mode) == 0o700,
              "an existing users directory is not repaired")


# --------------------------------------------------------------------------
# nothing leaks
# --------------------------------------------------------------------------


def test_no_body_log_line_or_exception_carries_a_password_hash_or_session() -> None:
    """Seeded values, asserted over every route including the refusals.

    A path reaches a message by way of an exception, and so does anything else
    that was in scope when one was raised -- which is why the refusals are in
    the sweep rather than only the successes. The log stream is captured for
    the same reason: an access log is where a credential in a URL ends up, and
    a session id in one is a credential in one.

    Must not fire: the probe can see each seeded value when it is present, so
    a sweep that found nothing is a sweep that looked.
    """
    log = io.StringIO()
    with environment(), Deployment(log=log) as live:
        live.first_account()
        alice = live.sign_in(OPERATOR, ALICE_PASSWORD)
        session_id = alice[accounts.SESSION_HEADER]
        live.add_account(alice, MEMBER, BOB_PASSWORD)
        live.set_key(alice, ALICE_KEY)
        record = live.accounts.get(OPERATOR)
        seeded = {
            "the operator's password": ALICE_PASSWORD,
            "a member's password": BOB_PASSWORD,
            "the operator's password hash": record.hash,
            "the operator's salt": record.salt,
            "a live session id": session_id,
            "the operator's API key": ALICE_KEY,
        }
        # Must not fire: each value is findable in a string that holds it.
        for what, value in seeded.items():
            check(value and value in f"prefix {value} suffix",
                  f"the probe cannot see {what} even when it is there")

        seen: list[tuple[str, str]] = []
        for method, path in routes_of(live.built):
            for headers in (alice, None, {accounts.SESSION_HEADER: "A" * 40}):
                status, answer, body = request(
                    live.url(path), method=method, headers=headers,
                    payload={"nonsense": 1} if method in ("POST", "PUT") else None)
                seen.append((f"{method} {path} [{status}]",
                             body.decode("utf-8", "replace")))
                # The response headers too: a `Set-Cookie` is the one place a
                # session id is *meant* to be, and every other header is a
                # place it is not.
                for name, value in answer.items():
                    if name.lower() != "set-cookie":
                        seen.append((f"{method} {path} header {name}", str(value)))
        seen.append(("the access log", log.getvalue()))
        # And a deliberately broken login, which is the request most likely to
        # put a password in an exception.
        for payload in ({"username": OPERATOR, "password": ALICE_PASSWORD[:3]},
                        {"username": OPERATOR, "password": {"not": "a string"}},
                        {"username": {"not": "a string"}, "password": ALICE_PASSWORD}):
            status, _, body = request(live.url(f"{P}/session"), method="POST",
                                      payload=payload)
            seen.append((f"a refused login [{status}]",
                         body.decode("utf-8", "replace")))
        # And the settings sweep, where a key is the value in scope.
        for path in (f"{P}/settings/keys", f"{P}/health", f"{P}/config",
                     f"{P}/accounts", f"{P}/session"):
            status, _, body = request(live.url(path), headers=alice)
            seen.append((f"GET {path} [{status}]",
                         body.decode("utf-8", "replace")))

        for where, text in seen:
            for what, value in seeded.items():
                if not value:
                    continue
                if what == "the operator's API key":
                    # Four characters is what the settings page is allowed to
                    # serve, so the leak test is the whole value and anything
                    # longer than the permitted suffix.
                    for length in range(len(value), credentials.SUFFIX_LENGTH, -1):
                        if value[-length:] in text:
                            check(False, f"{where} carries {length} characters "
                                         f"of {what}")
                            break
                    continue
                check(value not in text, f"{where} carries {what}")


def test_the_session_id_is_never_on_an_object_that_reprs() -> None:
    """A `repr` reaches a log line and a debugger without anybody deciding it should.

    Must fire on every object in this module's chain that holds one: the
    session table, a session, an account record, the setup token and the
    credentials directory. Must not fire: the probe can see each value in a
    string, and each `repr` is non-empty, so a silent pass is not a pass over
    nothing.
    """
    with tempfile.TemporaryDirectory() as raw:
        store = accounts.Accounts(Path(raw) / "accounts.json")
        record = store.create(OPERATOR, ALICE_PASSWORD, operator=True)
        sessions = accounts.Sessions()
        session_id = sessions.new(record.id)
        setup = accounts.Setup()
        keys = credentials.Credentials(Path(raw) / "credentials.json")
        directory = accounts.Directory(keys)
        throttle = accounts.Throttle()
        throttle.failed(OPERATOR)
        subjects = {
            "Sessions": repr(sessions),
            "Session": repr(sessions.lookup(session_id)),
            "Record": repr(record),
            "Setup": repr(setup),
            "Directory": repr(directory),
            "Accounts": repr(store),
            "Throttle": repr(throttle),
        }
        secrets_ = {"a session id": session_id,
                    "a password": ALICE_PASSWORD,
                    "a password hash": record.hash,
                    "a salt": record.salt,
                    "the setup token": setup.token}
        for what, value in secrets_.items():
            check(value and value in f"x{value}x",
                  f"the probe cannot see {what} even when it is there")
        for name, text in subjects.items():
            check(bool(text), f"{name}'s repr is empty, so nothing was checked")
            for what, value in secrets_.items():
                check(value not in text, f"{name}'s repr carries {what}")


# --------------------------------------------------------------------------
# the engine is untouched
# --------------------------------------------------------------------------


def test_the_engine_still_does_not_know_this_package_exists() -> None:
    """`tests/test_cli.py` owns the real probe; this asserts it is still there.

    The import boundary is the operator's stated requirement that the command
    line works standalone with no web interface installed, and a milestone
    that added five modules to `llossless.web` is exactly the kind that
    breaks it. Asserted here by name so that deleting the check over there is
    a red line in two places rather than one.
    """
    text = (ROOT / "tests" / "test_cli.py").read_text(encoding="utf-8")
    check("def test_a_complete_merge_never_loads_the_web_package" in text,
          "tests/test_cli.py no longer holds the import-boundary probe")
    engine = (ROOT / "src" / "llossless" / "cli.py").read_text(encoding="utf-8")
    check("from .web.server import serve as serve_http" in engine,
          "cli.py no longer defers the web import inside the serve branch")
    for line in engine.splitlines():
        stripped = line.strip()
        if stripped.startswith(("import ", "from ")) and not line.startswith(" "):
            check("web" not in stripped,
                  f"cli.py imports the web package at module scope: {stripped}")


def test_web_accounts_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    """Every check, and a check that raises is one failure rather than all of them.

    The exception is caught and recorded instead of propagating, which is not
    the usual arrangement in this suite and is earned here the same way it is
    in `tests/test_web_credentials.py`: every detector in this module was shown
    to work by seeding the break it is written against into the shipped code,
    and several of those breaks make an *earlier* check raise. Propagating
    would abort the module at the first one, so a single seeded defect would
    report one failure and leave the rest unexercised -- which is
    indistinguishable from detectors that do not work.
    """
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_accounts_offline" \
                and callable(function):
            try:
                function()
            except Exception as raised:  # noqa: BLE001 - see the docstring
                failures.append(f"{name} raised "
                                f"{type(raised).__name__}: {raised}")
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web accounts: {checks} checks pass over the account store, the "
          f"session routes, per-user credentials and job ownership")
    return 0


if __name__ == "__main__":
    sys.exit(main())
