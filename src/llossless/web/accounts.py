"""Who is asking. Accounts on disk, passwords hashed, sessions in memory.

`credentials.py` holds *what* a run may spend; this holds *whose* it is. Until
now the two questions had one answer: everyone who could reach the server
shared one set of keys, because a process has one environment and a key was
read out of it at send time. `config.keys_for_this_run` removed that
constraint without touching the rule it was mistaken for, and this module
is what fills the seam it opened -- an identity per request, so that a job can
be run with the submitter's credentials rather than with the machine's.

**The rule this module is held to is the one `credentials.py` is held to, one
field along: this module knows a password for the length of one call, and
nothing it hands to another layer does.** A `Record` carries a hash and a salt
and has a written `repr` that prints neither. A `Session` carries an account id
and never the session id that indexes it. Nothing here takes a password as a
field, returns one, or puts one in a message -- `api.ApiError` puts an
exception's message into a response body, and a module that formatted a
rejected password into a refusal would be a module that serves passwords to
whoever guesses wrong.

**Hashing is `hashlib` and nothing else.** This project has no third-party
dependency and is not about to acquire one for a login page, so the choice is
between the two key-derivation functions the standard library ships.
`hashlib.scrypt` is preferred and is memory-hard, which is the property that
makes a stolen file expensive to attack on a GPU; `hashlib.pbkdf2_hmac` is the
fallback, because `scrypt` is only present when Python was linked against an
OpenSSL that offers it and a server must not fail to start over a build option.
Which one produced a record is written *into* the record, beside its cost, so
the two can coexist in one file and so a cost raised next year does not
invalidate the accounts already in it: `verify` reads the parameters off the
record it is checking rather than off this module's constants.

**An unknown user and a wrong password are one answer and one duration.** The
answer is easy -- both are `None` and the route above turns both into the same
refusal. The duration is the part that takes work: returning early on an
unknown name makes the two distinguishable with a stopwatch, and a stopwatch is
all it takes to turn "guess a password" into "enumerate the users first". So
`verify` derives a hash either way, against a decoy record with this module's
own parameters when the name is not there. It is not constant time in the
cryptographic sense -- nothing written in Python is -- and the docstring says
so rather than claiming otherwise.

**A username never becomes a path.** Every account gets an opaque id from
`secrets.token_hex`, and it is the id that names the directory holding that
account's credentials file. `check_account_id` refuses anything that is not 32
hexadecimal characters, for the same reason `api.check_job_id` refuses anything
that is not a uuid4: a shape check is right about `../../etc` for what it is
rather than for where it would have pointed. The username itself is checked by
an allowlist too, but the allowlist is not what keeps it off the filesystem --
it never reaches the filesystem at all.

**The session id is held server-side and compared with `hmac.compare_digest`.**
A signed cookie carrying its own claims was considered and refused: it cannot
be revoked, so an operator deleting an account would delete the row and leave
the cookie working until it expired. A server-side table costs one dict and
makes `DELETE /session` mean what it says. The ids come from
`secrets.token_urlsafe`, never from `random`, and the comparison is
`compare_digest` on bytes for the reason `credentials.token_matches` gives: a
comparison that is correct on every input and wrong about how long it takes is
still wrong.

**Sessions die with the process, and that is deliberate.** `JobStore`'s index
does too, for the reason its docstring gives -- the alternative is a database
of who did what and when, which outlives every window retention promises. A
restart logs everybody out, which on a self-hosted tool is an inconvenience
rather than an outage, and it is the same trade the job queue already makes.

**The first account is the operator's, and there is no default password.** A
server with no accounts prints a URL carrying a `secrets` token and answers
nothing else; that URL creates the first account and nothing else can. It works
on loopback and on a network bind alike, which a "log in as admin/admin and
change it" arrangement does not: the password that has not been changed yet is
the one the scanner finds.
"""

from __future__ import annotations

import contextlib
import hmac
import json
import os
import re
import secrets
import stat
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from .. import config
from . import credentials

# What the file says it is. A version rather than a bare mapping, for the
# reason `credentials.SCHEMA_VERSION` exists: a later shape is recognised and
# refused with a sentence instead of a `KeyError` three layers down.
SCHEMA_VERSION = 1

FILE_NAME = "accounts.json"

# Where the file lives, and the variable that moves it. Read here rather than
# in `config.py` for the reason `credentials.PATH_ENV` is: `config.from_env`
# builds what a *run* resolves against, and nothing a run does should be able
# to name the file the accounts are in.
PATH_ENV = "LLOSSLESS_ACCOUNTS"

# The directory each account's own credentials file lives under, below the
# accounts file's own directory. One level, named by an opaque id.
USERS_DIR = "users"

# Owner, and nobody else. Both are checked on read and set on write, and the
# directory's mode matters as much as the file's: a directory another account
# can write is a directory in which the file can be replaced.
FILE_MODE = 0o600
DIR_MODE = 0o700

# What a username may be. Lowercase, because two accounts differing only in
# case are two accounts one of their owners will mistake for one; and bounded,
# because the name is rendered into a page and into this file.
#
# It is an allowlist, but the allowlist is not what keeps a name off the
# filesystem -- `Record.id` does, and a name is never joined to a path
# anywhere in this package.
USERNAME = re.compile(r"\A[a-z0-9][a-z0-9._-]{1,31}\Z")

# An account id: 32 hexadecimal characters from `secrets.token_hex(16)`. The
# same shape and the same reasoning as `api.JOB_ID`, and `\A`/`\Z` rather than
# `^`/`$` for the same reason -- `$` also matches before a trailing newline,
# which is the standard way this exact validation is defeated.
ACCOUNT_ID = re.compile(r"\A[0-9a-f]{32}\Z")

# A password shorter than this is not one. Ten rather than eight because this
# is a credential that guards other credentials, and longer than a vendor's own
# minimum because the failure it guards is a password reused from somewhere
# that had a shorter rule.
MIN_PASSWORD = 10

# And a ceiling, because the hash functions below do work proportional to the
# input and a request is a place where a whole file gets pasted by accident. A
# megabyte password is a denial of service against the box, presented as a
# login.
MAX_PASSWORD = 1024

# `scrypt`'s cost, and it is written into every record it produces so that
# raising it here does not invalidate the accounts already on disk.
#
# N = 2**14 with r = 8 asks for 16 MiB per derivation, which is the number that
# makes this expensive on a GPU and unremarkable on the box running the server.
# `maxmem` is passed explicitly: OpenSSL's own default is 32 MiB and the
# request for exactly 32 MiB is refused by it, so a parameter set chosen one
# step higher would fail at the boundary rather than at the limit.
SCRYPT_N = 1 << 14
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_MAXMEM = 1 << 26

# The fallback's cost. Higher than `scrypt`'s equivalent-feeling number on
# purpose: PBKDF2 is not memory-hard, so iterations are the only dial there is.
PBKDF2_ROUNDS = 600_000

# Bytes of salt, per account, from `secrets`. Sixteen is the length below which
# two accounts on two machines start being worth precomputing against together.
SALT_BYTES = 16

# How long a derived hash is. Both functions take a length; 32 is the digest
# size of the hash PBKDF2 is asked for here and is the size `scrypt` is
# ordinarily used at.
HASH_BYTES = 32

SCRYPT = "scrypt"
PBKDF2 = "pbkdf2-sha256"

# The cookie a browser carries, and the three attributes that make it safe to
# carry. `HttpOnly` so that a script on this page cannot read it -- the page
# never needs to, because the browser attaches it to every same-site request by
# itself. `SameSite=Strict` because it is what replaces the custom header's
# CSRF immunity: a cross-site navigation or form post arrives with no cookie at
# all, so there is nothing for a hostile page to ride. `Path=/` because the
# static page and the API are one origin and a cookie scoped narrower would be
# absent from one of them.
COOKIE_NAME = "llossless_session"

# Where a script presents the same secret. A header rather than a cookie,
# because a script is not a browser and has no cookie jar it did not build
# itself -- and because this is the header a token-protected deployment has
# always used, so a client that had one keeps its shape.
SESSION_HEADER = credentials.TOKEN_HEADER

# Bytes behind a session id. `secrets.token_urlsafe(32)` is 256 bits of
# urlsafe base64, which is not guessable and is short enough for a cookie.
SESSION_BYTES = 32

# How long a session lives without being used, and how long it may live at all.
# The first is the one that logs an abandoned browser out; the second is the
# one that says a session cannot be renewed forever, which is what makes a
# stolen cookie a bounded problem rather than a permanent one.
SESSION_IDLE_SECONDS = 12 * 3600.0
SESSION_MAX_SECONDS = 7 * 86400.0

# The token that creates the first account, and how long it is. Printed once,
# never stored on disk, and gone the moment an account exists.
SETUP_BYTES = 32


class AccountError(Exception):
    """The account store cannot do that, and the reason is safe to repeat.

    Every message raised as one of these names a rule, a file or a shape and
    never a value. `api.ApiError` puts an exception's message into a response
    body, so the discipline holds where the string is built rather than where
    it is served -- and the value most likely to be in scope here is a
    password.
    """


class UnknownAccount(AccountError):
    """A username that is not in the file. Refused, never used to build a path."""


def _scrypt_available() -> bool:
    """Does this build's `hashlib` actually do `scrypt`? Asked once, by trying.

    `hasattr` is not the check. `hashlib.scrypt` exists as a name whenever
    Python was built with any OpenSSL, and raises at call time when that
    OpenSSL does not offer the primitive -- so a server that trusted the
    attribute would start, accept an account, and fail on the first login.
    """
    import hashlib

    try:
        hashlib.scrypt(b"probe", salt=b"probe", n=2, r=1, p=1, dklen=16,
                       maxmem=SCRYPT_MAXMEM)
    except Exception:  # noqa: BLE001 - any failure means "use the fallback"
        return False
    return True


HAVE_SCRYPT = _scrypt_available()


def derive(password: str, salt: bytes, *, algorithm: str, cost: dict) -> bytes:
    """One password and one salt into `HASH_BYTES`, by the named algorithm.

    `algorithm` and `cost` come off the record being checked rather than off
    this module's constants, which is what lets the constants be raised without
    invalidating the accounts already written under the old ones. An algorithm
    this build cannot run raises rather than falling back to a weaker one: a
    silent downgrade is how a file written on one machine ends up verified more
    cheaply on another.
    """
    import hashlib

    encoded = password.encode("utf-8")
    if algorithm == SCRYPT:
        return hashlib.scrypt(
            encoded, salt=salt,
            n=int(cost.get("n", SCRYPT_N)), r=int(cost.get("r", SCRYPT_R)),
            p=int(cost.get("p", SCRYPT_P)), dklen=HASH_BYTES,
            maxmem=SCRYPT_MAXMEM)
    if algorithm == PBKDF2:
        return hashlib.pbkdf2_hmac(
            "sha256", encoded, salt,
            int(cost.get("rounds", PBKDF2_ROUNDS)), dklen=HASH_BYTES)
    raise AccountError(
        f"this build cannot check a password stored with {algorithm!r}. The "
        f"algorithms it knows are {SCRYPT} and {PBKDF2}.")


def default_algorithm() -> tuple[str, dict]:
    """Which function a new password is stored with here, and at what cost."""
    if HAVE_SCRYPT:
        return SCRYPT, {"n": SCRYPT_N, "r": SCRYPT_R, "p": SCRYPT_P}
    return PBKDF2, {"rounds": PBKDF2_ROUNDS}


def check_username(name) -> str:
    """The username, or `AccountError`. Returned rather than merely validated.

    Returned so that a call site cannot use the checked name and the raw one in
    the same breath, which is how a check ends up running beside a value
    instead of in front of it -- the same reason `credentials.check_provider`
    returns.
    """
    if not isinstance(name, str):
        raise AccountError(f"a username is a string; got a {type(name).__name__}.")
    cleaned = name.strip().lower()
    if not USERNAME.match(cleaned):
        raise AccountError(
            "a username is 2 to 32 characters of lowercase letters, digits, "
            "dot, dash or underscore, starting with a letter or a digit. It is "
            "matched against that list and is never used to build a path.")
    return cleaned


def check_password(value) -> str:
    """A password, checked for length only, with the value never in the message.

    Length only, and deliberately no composition rule. A rule demanding a digit
    and a symbol is a rule people satisfy by appending `1!` to a word, and the
    thing it would buy is already bought by the floor being ten rather than
    eight. The ceiling is not a style opinion at all: `derive` does work
    proportional to its input.
    """
    if not isinstance(value, str):
        raise AccountError(f"a password is a string; got a {type(value).__name__}.")
    if len(value) < MIN_PASSWORD:
        raise AccountError(
            f"a password is at least {MIN_PASSWORD} characters. This one is "
            f"shorter; its value is not repeated here.")
    if len(value) > MAX_PASSWORD:
        raise AccountError(
            f"a password is at most {MAX_PASSWORD} characters, which is past "
            f"what this accepts. A whole file was probably pasted into the box.")
    return value


def check_account_id(value) -> str:
    """The id, or `AccountError`. Nothing builds a path from an unchecked one.

    By shape, not by lookup. A check that asked whether the directory resolved
    inside the users directory would be a check whose correctness depended on
    symlinks and on the platform's separator; 32 hexadecimal characters depends
    on neither and refuses `../../etc` for what it is.
    """
    if not isinstance(value, str) or not ACCOUNT_ID.match(value):
        raise AccountError(
            "an account id is 32 hexadecimal characters. Nothing else is "
            "looked up, and no path is built from an id that is not one.")
    return value


@dataclass(frozen=True)
class Record:
    """One account as it is stored: an id, a name, a role, and a derived hash.

    **`repr` is written rather than generated**, for the reason
    `credentials.Endpoint`'s is: a frozen dataclass's default prints every
    field, this one holds a salt and a password hash, and a `repr` reaches a
    log line, a debugger and an exception's own rendering without anybody
    deciding that it should. A hash is not a password, but it is the input to
    the only offline attack there is, and a file this careful about a key has
    no business being casual about the material that guards it.

    `operator` is not a permission list. There is exactly one distinction in
    this tool -- whoever set the server up owns the endpoints everybody shares,
    and everyone else owns their own -- so it is one boolean rather than a role
    system nobody asked for. `Directory` is where that boolean turns into which
    file a write lands in.
    """

    id: str
    username: str
    algorithm: str
    salt: str          # hex
    hash: str          # hex
    cost: dict
    operator: bool = False
    created_at: float = 0.0

    def __repr__(self) -> str:
        return (f"Record(id={self.id!r}, username={self.username!r}, "
                f"operator={self.operator!r}, algorithm={self.algorithm!r}, "
                f"salt=<{len(self.salt) // 2} bytes>, hash=<derived>)")

    def describe(self) -> dict:
        """What a client may be told about an account. No salt, no hash, ever.

        The id is included: it is not a secret -- it names a directory this
        server owns and nothing else -- and without it a page listing accounts
        has nothing stable to key a row on when two names differ by a rename.
        """
        return {
            "id": self.id,
            "username": self.username,
            "operator": self.operator,
            "created_at": self.created_at,
        }


# The decoy an unknown username is checked against. Built once, with this
# module's own parameters, so that `verify` does the same work whether or not
# the name exists -- see the module docstring. The password it was built from
# is a throwaway from `secrets` that nothing keeps.
_DECOY = Record(
    id="0" * 32, username="", algorithm=default_algorithm()[0],
    salt=secrets.token_bytes(SALT_BYTES).hex(), hash="", cost=default_algorithm()[1],
)


def default_path(environ=None) -> Path:
    """`$XDG_CONFIG_HOME/llossless/accounts.json`, or the spec's fallback.

    Beside the credentials file, deliberately: the two are the same operator's
    configuration of the same server, and an arrangement where one moves and
    the other does not is an arrangement where a backup carries half of it.
    """
    source = os.environ if environ is None else environ
    named = (source.get(PATH_ENV) or "").strip()
    if named:
        return Path(named).expanduser()
    # Beside a credentials file named by its variable, as it always was.
    if (source.get(credentials.PATH_ENV) or "").strip():
        return credentials.default_path(environ).parent / FILE_NAME
    return config.config_file(FILE_NAME, source)


class Accounts:
    """The accounts file: read it, write it, check a password against it.

    Holds no password in a field and no hash beyond the life of one call.
    `read()` returns records to its caller and the callers use them within one
    statement; nothing on this object survives a call holding either.

    The lock is this object's own and guards the read-modify-write in every
    mutator. Two HTTP threads creating two accounts at once would otherwise
    each read the file, add their row, and write the whole of it back -- and
    the second write would silently drop the first account. The file is
    replaced atomically, so the failure is not a corrupt file; it is a user who
    was told they exist and does not.
    """

    def __init__(self, path=None, *, environ=None) -> None:
        self.path = Path(path) if path is not None else default_path(environ)
        self._lock = threading.Lock()

    def __repr__(self) -> str:
        """The file, and nothing about who is in it."""
        return f"Accounts(path={str(self.path)!r})"

    # -- reading ---------------------------------------------------------

    def read(self) -> dict[str, Record]:
        """Every account, keyed by username, or `{}`. Raises if the file is unusable.

        An absent file is the ordinary first-boot state and is not an error:
        `serve` is expected to start on a machine that has never had an
        account and to say so.

        A file wider than `0600` is refused rather than repaired, on the same
        reasoning `credentials.Credentials.read` gives about a key: every
        account on the box has already had the chance to read the hashes, and
        chmodding it back would destroy the evidence while leaving the
        passwords -- now open to an offline attack -- in service. The refusal
        says to change them.
        """
        try:
            info = self.path.stat()
        except FileNotFoundError:
            return {}
        except OSError as exc:
            raise AccountError(
                f"{self.path} cannot be read: {exc.strerror or exc}") from None

        mode = stat.S_IMODE(info.st_mode)
        if mode & ~FILE_MODE:
            raise AccountError(
                f"refusing to read {self.path}: it is mode {mode:04o} and an "
                f"accounts file must be no wider than {FILE_MODE:04o}. Every "
                f"account on this machine has had the chance to read the "
                f"password hashes in it, so change those passwords first; "
                f"`chmod {FILE_MODE:04o}` on its own puts them back into "
                f"service.")

        try:
            raw = self.path.read_text(encoding="utf-8")
        except OSError as exc:
            raise AccountError(
                f"{self.path} cannot be read: {exc.strerror or exc}") from None
        except UnicodeDecodeError:
            raise AccountError(
                f"{self.path} is not UTF-8, so it was not written by this "
                f"tool.") from None

        try:
            payload = json.loads(raw)
        except ValueError:
            raise AccountError(
                f"{self.path} is not readable as JSON. No account in it was "
                f"loaded.") from None
        if not isinstance(payload, dict):
            raise AccountError(
                f"{self.path} holds a {type(payload).__name__} where this "
                f"expects an object.")
        if payload.get("version") != SCHEMA_VERSION:
            raise AccountError(
                f"{self.path} declares schema version "
                f"{payload.get('version')!r}; this build reads "
                f"{SCHEMA_VERSION}.")
        rows = payload.get("accounts")
        if not isinstance(rows, dict):
            raise AccountError(f"{self.path} has no `accounts` object in it.")

        out: dict[str, Record] = {}
        for name, value in rows.items():
            out[check_username(name)] = self._row(name, value)
        return out

    def _row(self, name: str, value) -> Record:
        """One entry as a `Record`, or a refusal naming the field and not the value."""
        if not isinstance(value, dict):
            raise AccountError(
                f"{self.path}'s entry for {name} is a {type(value).__name__} "
                f"where this expects an object.")
        wanted = ("id", "algorithm", "salt", "hash")
        missing = [field for field in wanted
                   if not isinstance(value.get(field), str) or not value[field]]
        if missing:
            raise AccountError(
                f"{self.path}'s entry for {name} has no "
                f"{', '.join(missing)}. Nothing in it was loaded.")
        cost = value.get("cost")
        if not isinstance(cost, dict):
            raise AccountError(
                f"{self.path}'s entry for {name} has no cost object, so the "
                f"parameters its hash was derived under are not recorded and "
                f"it cannot be checked.")
        return Record(
            id=check_account_id(value["id"]),
            username=check_username(name),
            algorithm=value["algorithm"],
            salt=value["salt"],
            hash=value["hash"],
            cost=dict(cost),
            operator=bool(value.get("operator")),
            created_at=float(value.get("created_at") or 0.0),
        )

    def count(self) -> int:
        """How many accounts there are. The whole of what "is this set up" means."""
        return len(self.read())

    def names(self) -> list[str]:
        return sorted(self.read())

    def get(self, username) -> Record | None:
        """One account by name, or None. Never raises on an unknown name."""
        try:
            wanted = check_username(username)
        except AccountError:
            return None
        return self.read().get(wanted)

    def by_id(self, account_id) -> Record | None:
        """One account by its opaque id, or None."""
        try:
            wanted = check_account_id(account_id)
        except AccountError:
            return None
        for record in self.read().values():
            if record.id == wanted:
                return record
        return None

    # -- checking --------------------------------------------------------

    def verify(self, username, password) -> Record | None:
        """The account this password belongs to, or None. One duration either way.

        **An unknown username and a wrong password are indistinguishable from
        here**, which is the whole of what this function adds over a dict
        lookup and a comparison. A version that returned early on a name it did
        not find would answer in microseconds for a stranger and in tens of
        milliseconds for a real user, and that difference is a user enumeration
        oracle that needs nothing but a stopwatch -- after which guessing a
        password is a search over the accounts that exist rather than over
        every string somebody might have chosen as a name.

        So the derivation runs either way, against `_DECOY` when the name is
        not there, with this module's own parameters. It is **not** constant
        time in the cryptographic sense: `derive` is `hashlib`'s, the
        comparison after it is `compare_digest`, and everything around it is
        interpreted Python whose timing depends on the garbage collector. What
        it is, is a function with no branch that skips the expensive part, and
        that is the branch an attacker can actually see.

        A malformed username is checked against the decoy too, for the same
        reason: refusing `Bob!` instantly while taking 20ms over `bob` says
        which spellings are real.
        """
        try:
            wanted = check_username(username)
        except AccountError:
            wanted = ""
        if not isinstance(password, str):
            password = ""
        # Bounded before it reaches `derive`, which does work proportional to
        # its input. The body cap upstream is four megabytes, and a login is a
        # route anybody can reach before authenticating -- so a submitted
        # password longer than one can be is cut here rather than refused,
        # because refusing early would answer a long guess faster than a short
        # one and put a second timing signal beside the one this function
        # exists to remove.
        password = password[:MAX_PASSWORD]
        record = self.read().get(wanted) if wanted else None
        checked = _DECOY if record is None else record
        try:
            derived = derive(password, bytes.fromhex(checked.salt),
                             algorithm=checked.algorithm, cost=checked.cost)
        except (AccountError, ValueError):
            # A record this build cannot check, or a salt that is not hex.
            # Answered as a failed login rather than as a 500: the operator
            # sees the file's own refusal on the next read, and whoever is
            # typing a password gets the one answer this function has.
            return None
        expected = bytes.fromhex(checked.hash) if checked.hash else b"\x00" * HASH_BYTES
        if not hmac.compare_digest(derived, expected):
            return None
        return record

    # -- writing ---------------------------------------------------------

    def create(self, username, password, *, operator: bool = False,
               now: float | None = None) -> Record:
        """Add one account. Refuses a name that is already there.

        The id comes from `secrets.token_hex` rather than from the username,
        and that is what keeps a rename from moving a directory and a username
        from ever being a path segment.
        """
        name = check_username(username)
        check_password(password)
        algorithm, cost = default_algorithm()
        salt = secrets.token_bytes(SALT_BYTES)
        derived = derive(password, salt, algorithm=algorithm, cost=cost)
        with self._lock:
            rows = self.read()
            if name in rows:
                raise AccountError(
                    f"there is already an account called {name}. Names are how "
                    f"one is picked out, so two cannot share one.")
            record = Record(
                id=secrets.token_hex(16), username=name, algorithm=algorithm,
                salt=salt.hex(), hash=derived.hex(), cost=cost,
                operator=bool(operator),
                created_at=time.time() if now is None else now,
            )
            rows[name] = record
            self._write(rows)
        return record

    def set_password(self, username, password) -> Record:
        """Change one account's password, re-deriving under today's parameters.

        Re-derived rather than re-salted alone, so that a change of password is
        also the way an account written under an older, cheaper cost is moved
        onto the current one. `verify` reads the parameters off the record, so
        the two can coexist in the file for as long as it takes everybody to
        change theirs.
        """
        name = check_username(username)
        check_password(password)
        algorithm, cost = default_algorithm()
        salt = secrets.token_bytes(SALT_BYTES)
        derived = derive(password, salt, algorithm=algorithm, cost=cost)
        with self._lock:
            rows = self.read()
            current = rows.get(name)
            if current is None:
                raise UnknownAccount(f"there is no account called {name}.")
            rows[name] = Record(
                id=current.id, username=name, algorithm=algorithm,
                salt=salt.hex(), hash=derived.hex(), cost=cost,
                operator=current.operator, created_at=current.created_at,
            )
            self._write(rows)
        return rows[name]

    def remove(self, username) -> Record | None:
        """Drop one account. Returns the record that went, or None if there was none.

        **Refuses to remove the last operator.** An account store whose only
        operator has been deleted is a server nobody can configure the shared
        endpoints on again, and the only repair is editing the file by hand --
        which is exactly the state a tool should not be able to put its
        operator in with one click.
        """
        name = check_username(username)
        with self._lock:
            rows = self.read()
            current = rows.get(name)
            if current is None:
                return None
            if current.operator and sum(
                    1 for row in rows.values() if row.operator) == 1:
                raise AccountError(
                    "that is the only operator account on this server. "
                    "Removing it would leave nobody able to configure the "
                    "shared endpoints, and the only way back would be editing "
                    "the accounts file by hand. Make another account an "
                    "operator first.")
            del rows[name]
            self._write(rows)
        return current

    def _write(self, rows: dict[str, Record]) -> None:
        """The whole file, atomically, never wider than `0600` for an instant.

        The same four steps in the same order as `credentials.Credentials._write`,
        and for the same reasons: the directory is created and chmodded first,
        because a `0755` directory holding a `0600` file is a directory in
        which another account can rename the file out of the way and leave one
        of its own; the temporary is opened `O_EXCL` in that same directory,
        because `os.replace` is atomic only within a filesystem; it is
        `fchmod`ed on its own descriptor before a byte is written, rather than
        after, because a window is a window; and it is `fsync`ed before the
        replace so a machine that loses power comes back holding the old file
        rather than an empty new one.

        It is written out here rather than shared with that function because
        the two files have different contents, different schemas and different
        readers, and a shared writer would be one function with two callers
        that have to agree about a payload -- which is how one of them ends up
        writing the other's shape.
        """
        parent = self.path.parent
        parent.mkdir(parents=True, exist_ok=True)
        os.chmod(parent, DIR_MODE)
        stored = {
            name: {
                "id": row.id,
                "algorithm": row.algorithm,
                "salt": row.salt,
                "hash": row.hash,
                "cost": row.cost,
                "operator": row.operator,
                "created_at": row.created_at,
            }
            for name, row in sorted(rows.items())
        }
        payload = json.dumps({"version": SCHEMA_VERSION, "accounts": stored},
                             indent=2, sort_keys=True) + "\n"
        temporary = parent / f".{self.path.name}.{os.getpid()}.tmp"
        try:
            handle = os.open(temporary,
                             os.O_WRONLY | os.O_CREAT | os.O_EXCL, FILE_MODE)
            with os.fdopen(handle, "w", encoding="utf-8") as out:
                os.fchmod(out.fileno(), FILE_MODE)
                out.write(payload)
                out.flush()
                os.fsync(out.fileno())
            os.replace(temporary, self.path)
        except BaseException:
            with contextlib.suppress(OSError):
                temporary.unlink()
            raise


# --------------------------------------------------------------------------
# sessions
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Session:
    """One logged-in browser or script. **Carries no session id.**

    The id is the key of the dict this is stored in, and it is not also a field
    here, deliberately: a `repr` of a session is a thing that reaches a log
    line, and a session id in a log line is a credential in a log line. What is
    on the object is an account id, two timestamps and nothing else, so the
    default `repr` a frozen dataclass generates is safe -- which is why this
    one is not written out by hand the way `Record`'s is.
    """

    account: str
    created_at: float
    last_used_at: float


class Sessions:
    """Live sessions, in memory, keyed by an id nothing else ever sees.

    In memory for the reason `JobStore`'s index is: the alternative is a table
    of who was logged in when, which outlives every window this tool promises
    anything about. A restart logs everybody out, and on a self-hosted tool
    that is an inconvenience rather than an outage.

    `lookup` is where expiry happens, rather than in a reaper thread. There is
    no cost to an expired row sitting in a dict nobody reads, the dict is
    bounded by how many people work here, and a thread that has to be started
    and stopped is a thread whose failure mode is a server that will not shut
    down.
    """

    def __init__(self, *, idle_seconds: float = SESSION_IDLE_SECONDS,
                 max_seconds: float = SESSION_MAX_SECONDS,
                 clock=time.time) -> None:
        self.idle_seconds = idle_seconds
        self.max_seconds = max_seconds
        self.clock = clock
        self._lock = threading.Lock()
        self._live: dict[str, Session] = {}

    def __repr__(self) -> str:
        """The count. Never an id, and never whose."""
        return f"Sessions(live={len(self._live)})"

    def __len__(self) -> int:
        return len(self._live)

    def new(self, account: str) -> str:
        """Start a session for this account and return its id. Printed nowhere.

        `secrets.token_urlsafe` and never `random`: `random` is a Mersenne
        twister whose whole state is recoverable from its output, so a handful
        of observed session ids would predict every later one.
        """
        now = self.clock()
        session_id = secrets.token_urlsafe(SESSION_BYTES)
        with self._lock:
            self._prune(now)
            self._live[session_id] = Session(account=account, created_at=now,
                                             last_used_at=now)
        return session_id

    def lookup(self, presented) -> Session | None:
        """The session this id names, or None. Refreshes its idle clock.

        **Compared with `hmac.compare_digest` rather than looked up directly**,
        and this is the one place in this module where that is not obviously
        necessary. A dict lookup on a 256-bit id is not a realistic timing
        oracle -- the hash is computed over the whole string -- but the
        argument for `==` here is "this particular comparison is probably fine",
        and the rule this project keeps is that a credential is compared one
        way. `credentials.token_matches` states the reasoning in full.

        Returns None for an unknown, expired or malformed id, all three as one
        answer: a client with a dead session is told to log in, and which kind
        of dead it was is worth nothing to it and something to whoever is
        probing.
        """
        if not isinstance(presented, str) or not presented:
            return None
        given = presented.strip().encode("utf-8")
        now = self.clock()
        with self._lock:
            self._prune(now)
            for session_id, session in self._live.items():
                if hmac.compare_digest(session_id.encode("utf-8"), given):
                    refreshed = Session(account=session.account,
                                        created_at=session.created_at,
                                        last_used_at=now)
                    self._live[session_id] = refreshed
                    return refreshed
        return None

    def revoke(self, presented) -> bool:
        """End one session. True if there was one to end."""
        if not isinstance(presented, str) or not presented:
            return False
        given = presented.strip()
        with self._lock:
            return self._live.pop(given, None) is not None

    def revoke_account(self, account: str) -> int:
        """End every session belonging to one account. Returns how many.

        Called when an account is deleted and when its password changes. A
        password changed because it may have leaked has bought nothing if the
        session opened with the old one is still live, which is the failure
        every "log out everywhere" button exists for.
        """
        with self._lock:
            doomed = [key for key, row in self._live.items()
                      if row.account == account]
            for key in doomed:
                del self._live[key]
        return len(doomed)

    def _prune(self, now: float) -> None:
        """Drop everything past either window. Called under the lock."""
        for key, row in list(self._live.items()):
            if (now - row.last_used_at > self.idle_seconds
                    or now - row.created_at > self.max_seconds):
                del self._live[key]


class Throttle:
    """How many wrong passwords a name may collect before it stops answering.

    `derive` is the only rate limit a login endpoint gets for free -- one
    attempt costs tens of milliseconds -- and on a LAN that is still a few
    thousand guesses a minute. This adds a ceiling.

    **A locked name answers exactly as a wrong password does**, and that is the
    part that takes care. The obvious implementation returns 429 while locked,
    which tells a caller that the name they are guessing is one somebody is
    guessing at -- and, worse, which of two names is real, because an unknown
    name would not be worth locking. So the counter is kept for *whatever was
    submitted*, real or not, and a locked name is refused with the same status
    and the same sentence as a wrong password. The only way to tell is to have
    the right password and be refused anyway, which is a thing the legitimate
    user notices and an attacker does not.

    The window slides forward from the last failure rather than from the first,
    so an attacker cannot wait out a fixed window and resume at full rate.
    """

    def __init__(self, *, limit: int = 10, window: float = 300.0,
                 clock=time.time) -> None:
        self.limit = limit
        self.window = window
        self.clock = clock
        self._lock = threading.Lock()
        self._failures: dict[str, tuple[int, float]] = {}

    def __repr__(self) -> str:
        """The count of names being counted. Never one of them."""
        return f"Throttle(watching={len(self._failures)})"

    def locked(self, name: str) -> bool:
        now = self.clock()
        with self._lock:
            self._prune(now)
            count, last = self._failures.get(name, (0, 0.0))
            return count >= self.limit and now - last < self.window

    def failed(self, name: str) -> None:
        now = self.clock()
        with self._lock:
            self._prune(now)
            count, _ = self._failures.get(name, (0, 0.0))
            self._failures[name] = (count + 1, now)

    def succeeded(self, name: str) -> None:
        with self._lock:
            self._failures.pop(name, None)

    def _prune(self, now: float) -> None:
        """Drop names whose last failure is older than the window. Under the lock."""
        for key, (_, last) in list(self._failures.items()):
            if now - last >= self.window:
                del self._failures[key]


def cookie(session_id: str, *, secure: bool, max_age: float) -> str:
    """The `Set-Cookie` value for a session, with every attribute that matters.

    `HttpOnly`, so no script on this page can read it -- the page has no reason
    to, because the browser attaches it by itself. `SameSite=Strict`, which is
    what replaces the custom header's CSRF immunity: a cross-site
    navigation or form post arrives with no cookie at all, so there is nothing
    for a hostile page to ride, and the `Origin` check on mutating requests
    stays in place as the second layer rather than the only one. `Path=/`,
    because the page and the API are one origin. `Secure` when the request
    arrived over TLS, and only then: setting it on a plain-HTTP deployment
    would produce a cookie the browser refuses to send back, which presents as
    a login that appears to succeed and then does nothing.
    """
    parts = [f"{COOKIE_NAME}={session_id}", "Path=/", "HttpOnly",
             "SameSite=Strict", f"Max-Age={int(max_age)}"]
    if secure:
        parts.append("Secure")
    return "; ".join(parts)


def expired_cookie(*, secure: bool) -> str:
    """The `Set-Cookie` that removes one. Same attributes, no value, no age.

    The attributes have to match the ones it was set with or the browser treats
    it as a different cookie and leaves the live one in place -- a logout that
    reports success and leaves the session in the jar.
    """
    parts = [f"{COOKIE_NAME}=", "Path=/", "HttpOnly", "SameSite=Strict",
             "Max-Age=0"]
    if secure:
        parts.append("Secure")
    return "; ".join(parts)


def session_from_cookie(raw) -> str:
    """The session id out of a `Cookie:` header, or ``.

    Parsed by hand rather than with `http.cookies`, which is the standard
    library's parser and is the wrong tool here: `SimpleCookie.load` silently
    drops the rest of the header when it meets a value it cannot parse, so one
    malformed cookie set by something else on the same host would log the
    operator out with no error anywhere. This looks for one name and ignores
    everything it does not understand.
    """
    presented = sessions_from_cookie(raw)
    return presented[0] if presented else ""


def sessions_from_cookie(raw) -> tuple[str, ...]:
    """Every session id a `Cookie:` header carries under `COOKIE_NAME`.

    One at most: a repeated name keeps its first value. The pre-rename
    cookie name was read here until the rename completed and is ignored now.
    """
    if not isinstance(raw, str) or not raw:
        return ()
    found: dict[str, str] = {}
    for part in raw.split(";"):
        name, _, value = part.strip().partition("=")
        name = name.strip()
        if name == COOKIE_NAME and name not in found:
            found[name] = value.strip().strip('"')
    return (found[COOKIE_NAME],) if found.get(COOKIE_NAME) else ()


# --------------------------------------------------------------------------
# first run
# --------------------------------------------------------------------------


class Setup:
    """The one-time token that creates the first account, and nothing else.

    A server with no accounts is not a server anybody may use, so it answers
    one route and prints one URL. The token is `secrets`, lives in this
    object, is never written to disk, and stops being accepted the moment an
    account exists -- so a URL left in a terminal's scrollback is a URL that
    does nothing.

    **A token rather than a default password**, because the password that has
    not been changed yet is the one the scanner finds, and **a token rather
    than "loopback may create the first account"**, because the first boot of a
    deployment is frequently not on loopback and an arrangement that only works
    there is an arrangement whose network case is undefined.

    It rides in the URL's **fragment**, not its query. A fragment is not sent
    to any server, so the token does not reach this server's own access log,
    an intermediary's, or a `Referer` on the way out -- and the page can still
    read it and post it in a body.
    """

    def __init__(self, *, token: str = "") -> None:
        self.token = token or secrets.token_urlsafe(SETUP_BYTES)

    def __repr__(self) -> str:
        """Never the token. This object's whole content is a credential."""
        return "Setup(<token>)"

    def matches(self, presented) -> bool:
        """Constant-time comparison, failing closed on an empty expectation.

        The empty case is unreachable -- `__init__` always has a token -- which
        is exactly why it is written: `hmac.compare_digest(b"", b"")` is True,
        so the version of this that grew a way to have no token would become a
        version that admitted everybody.
        """
        if not self.token:
            return False
        given = presented if isinstance(presented, str) else ""
        return hmac.compare_digest(given.strip().encode("utf-8"),
                                   self.token.encode("utf-8"))

    def url(self, base: str) -> str:
        """The address to paste, with the token in the fragment. See the class."""
        return f"{base.rstrip('/')}/#setup={self.token}"


# --------------------------------------------------------------------------
# whose credentials
# --------------------------------------------------------------------------


class Directory:
    """Which credentials file belongs to whom, and what a run reads from it.

    This is the join between the two halves of the milestone. `credentials.py`
    knows how to store one provider's address and key; `Accounts` knows who is
    asking; this decides *whose file* a write lands in and *which keys* a job
    runs with.

    **Two owners, and the split is the one the deployment actually wants.** The
    operator's file is the one `serve` already loads into the server's
    environment, and it stays exactly that -- the shared endpoints everybody
    can reach, a local ollama configured once. Every other account gets a file
    of its own under `users/<id>/`, private, and it *shadows* the operator's
    per provider: configure your own `anthropic` and your runs go to your
    address with your key, leaving everyone else's alone.

    **A user with no key for a provider does not get the operator's** unless
    the operator configured that provider as a shared endpoint, which is the
    same statement as "the operator's endpoints are shared". That is the
    behaviour the seam was built to make possible: an empty key source
    yields `None` rather than falling back to the environment, so a user with
    nothing configured gets a run that fails on a missing credential rather
    than one billed to whoever owns the process.

    **`keys_for` returns `None` for an empty account**, and the difference
    matters. `None` means "do not swap the source at all", which is what a
    single-tenant server already does and is byte-identical to every CLI run
    and every recorded cassette. An empty dict would mean "this user has no
    keys", which is a different and much stronger statement.

    Nothing on this object is a key. The files are read at the moment they are
    needed and the mappings they produce are locals of the caller that asked.
    """

    def __init__(self, shared: credentials.Credentials, *, root=None,
                 accounts=None) -> None:
        self.shared = shared
        self.root = Path(root) if root is not None else shared.path.parent
        # The account store, so that `keys_for` can tell an operator from
        # everybody else. `None` on a server that has no accounts, where the
        # question never arises.
        self.accounts = accounts

    def __repr__(self) -> str:
        """The root. Never a key, never an account."""
        return f"Directory(root={str(self.root)!r})"

    def path_for(self, account_id: str) -> Path:
        """Where one account's own credentials file lives. Checked, then joined."""
        return (self.root / USERS_DIR / check_account_id(account_id)
                / credentials.FILE_NAME)

    def defaults_path(self, record: Record | None, file_name: str) -> Path:
        """Where one person's saved run settings live. Checked, then joined.

        Beside their own credentials file, for every account including the
        operator's: settings are a person's, where the operator's credentials
        are the server's shared file. A server with no account store has one
        user, and keeps one file beside the shared credentials. `forget`
        removes the directory, so an account's defaults go with it.
        """
        if record is None:
            return self.root / file_name
        return self.root / USERS_DIR / check_account_id(record.id) / file_name

    def own(self, account_id: str) -> credentials.Credentials:
        """One account's private credentials store."""
        return credentials.Credentials(self.path_for(account_id))

    def store_for(self, record: Record | None) -> credentials.Credentials:
        """Which file this account's settings writes land in.

        The operator's land in the shared file, everyone else's in their own.
        That is the whole of the ownership rule, and it is one expression
        rather than a flag on every route: a non-operator has no way to name
        the shared file, so there is no request shape in which one of them
        edits an endpoint everybody uses.
        """
        if record is None or record.operator:
            return self.shared
        return self.own(record.id)

    def forget(self, record: Record) -> None:
        """Delete one account's private credentials, file and directory.

        Called when the account goes. Leaving the file behind would leave a
        vendor key on disk belonging to somebody with no way to reach it, and
        the next account to be issued that id -- which cannot happen, ids are
        random -- is not the reason to delete it. The reason is that the person
        whose key it is asked to be gone.
        """
        import shutil

        if record.operator:
            return
        with contextlib.suppress(OSError, AccountError):
            shutil.rmtree(self.path_for(record.id).parent, ignore_errors=True)

    # -- what a run reads ------------------------------------------------

    def environ_for(self, account_id: str) -> dict[str, str]:
        """This account's **non-secret** settings, as environment variables.

        Addresses and model listings, and never a key. They are not secrets --
        an address is reported back to the page and printed in a run's own
        banner -- so they go into the environment a job resolves against, which
        is where `jobs.endpoint_plan` already looks for them.

        The keys go the other way, through `keys_for` and
        `config.keys_for_this_run`, and the split is the point: the environment
        a job resolves against is copied, merged and logged about, and a key
        must not be in anything that is.
        """
        if not account_id:
            return {}
        out: dict[str, str] = {}
        for name, row in self.own(account_id).read().items():
            if row.base_url:
                out[credentials.url_env(name)] = row.base_url
            if row.models:
                out[credentials.models_env(name)] = "\n".join(row.models)
        return out

    def keys_for(self, account_id: str, environ=None) -> dict[str, str] | None:
        """What `config.keys_for_this_run` is handed for this account's job.

        **`None` twice, for two different reasons, and both mean "do not swap
        the source".** An empty account is a server with no account store,
        which is the single-tenant arrangement and is byte-identical to every
        CLI run. An *operator* is the same answer for a different reason: the
        shared credentials file is theirs and `Credentials.apply` has already
        put it in the process environment, along with whatever their shell
        exported -- so swapping in a copy built from the file alone would
        quietly drop a key they set outside the settings page, and the page
        would go on reporting it as configured because `describe` reads the
        environment. `None` and `{}` are different statements, and so are
        `None` and "a faithful-looking copy".

        For everybody else the mapping is built per provider, and the rule
        takes each provider whole rather than a merge of two dictionaries:

          their own endpoint     their own key, and **never** the operator's.
                                 A shared key sent to an address a member
                                 typed is exactly the pairing `moved_to`
                                 exists to make unrepresentable, and it does
                                 not stop being that because the two are now
                                 two people rather than two addresses.

          no endpoint of their   the operator's key, which goes to the
          own                    operator's address. That is the arrangement
                                 the deployment wants: a local endpoint
                                 configured once and used by everybody.

        `environ` is where the operator's half is read from, rather than the
        shared file, because that is where the answer actually is -- the file,
        their shell and the unit that started the server all land there, and
        `Credentials.describe` reports from the same place. A caller with no
        environ to offer falls back to the file.
        """
        if not account_id:
            return None
        if self.accounts is not None:
            try:
                record = self.accounts.by_id(account_id)
            except AccountError:
                record = None
            if record is not None and record.operator:
                return None
        try:
            mine = self.own(account_id).read()
        except credentials.CredentialsError:
            # An unusable file is not a reason to hand this job somebody
            # else's credential. Their own rows are dropped, which leaves them
            # on the operator's shared endpoints -- and the settings page
            # reports the same refusal over the same file.
            mine = {}
        try:
            shared = self.shared.read()
        except credentials.CredentialsError:
            shared = {}
        out: dict[str, str] = {}
        for name, variable in credentials.PROVIDERS.items():
            row = mine.get(name)
            if row is not None and row.base_url:
                if row.key:
                    out[variable] = row.key
                continue
            operators = shared.get(name)
            value = (operators.key if operators is not None else "") or (
                (environ or {}).get(variable) or "")
            if value:
                out[variable] = value
        return out

    def rows_for(self, record: Record | None, *, environ) -> list[dict]:
        """Every provider, as the settings page sees it for this account.

        One row per provider, never two, because a user who has configured
        their own endpoint for a provider is not offered a choice between it
        and the operator's -- theirs shadows. `owner` says whose the row is and
        `editable` says whether this account may change it, so a page can grey
        a row out and say why rather than offering a button that 403s.

        The operator's rows are answered out of the environment, exactly as
        `Credentials.describe` always has: what an operator needs to know is
        which credential the next run will *spend*, whatever put it there --
        their file, their shell, or the unit that started the server. A user's
        rows are answered out of their file alone, because that is the only
        place theirs can come from.
        """
        operator = record is None or record.operator
        shared = {row["name"]: row for row in self.shared.describe(environ)}
        mine = ({row["name"]: row for row in self.own(record.id).describe_file()}
                if not operator else {})
        out = []
        for name in sorted(shared):
            own = mine.get(name)
            if own is not None and (own["endpoint_configured"] or own["configured"]):
                out.append(dict(own, owner="you", editable=True))
                continue
            row = shared[name]
            if row["endpoint_configured"] or row["configured"]:
                out.append(dict(row, owner="operator", editable=operator))
                continue
            # Nobody has configured this provider. It is offered to everyone,
            # and where the write lands is `store_for`'s answer rather than
            # this row's: an operator configures the shared endpoint, anyone
            # else configures one of their own.
            out.append(dict(own or row, owner=None, editable=True))
        return out
