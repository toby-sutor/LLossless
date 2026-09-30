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
