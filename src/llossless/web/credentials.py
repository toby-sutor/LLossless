"""The operator's keys and endpoints, and who is allowed to set them. One rule.

`llossless serve` shipped able to bind loopback and nothing else, and the
reason was written into `server.py`'s docstring rather than left implied: the
server spends the operator's API credit on every submitted document, and until
something authenticated the submitter there must not exist a version of this
package where one flag makes a key-spending endpoint reachable from the
network. This module is the something. It holds the two credentials that
arrangement needs -- the API key the settings page writes, and the bind token
that lets a request be attributed to the operator -- and it holds them under
one rule: this module knows a value, and nothing it hands to another layer
does.

**The key never becomes a field on anything.** `config.Settings.api_key()`
stores the *name* of an environment variable and reads the value out of
`os.environ` at send time, deliberately, so that no `repr`, no
`dataclasses.asdict` and no JSON dump of a run's configuration can carry a key.
That property is worth more than the convenience of a `Settings` that owns its
credential, so this module does not extend `Settings`, does not pass it a
value, and does not cause `config.py` to be edited at all. It writes the value
into the process environment under the variable `Settings` already reads, and
stops. There is still exactly one place in this tool where a key is read, and
it is still read at send time.

**A file wider than `0600` is refused rather than repaired.** A credentials
file that went world-readable is a finding: every other account on the box has
already had the chance to read it, and quietly chmodding it back would destroy
the one piece of evidence that it happened while leaving the key -- now known
to somebody else -- in service. So the refusal names the file and the mode and
tells the operator to rotate, and the server starts without that key rather
than with a key it cannot vouch for.

**The file is `0600` from the instant it exists.** Written through a temporary
file in the same directory, opened `O_EXCL`, `fchmod`ed on its own descriptor
before a byte of content is written, then `os.replace`d over the target. Write-
then-chmod would leave a window in which a whole key sits on disk at whatever
the umask allowed, and "briefly" is not a property a credential has: a window
is a window to anything already polling the directory. `os.replace` is atomic
within a filesystem, so a crash mid-write leaves either the old file or the new
one and never half of either.

**A provider name never becomes a path.** `PROVIDERS` is an allowlist and the
name is looked up in it; nothing here joins a submitted name onto a directory.
The endpoints in `api.py` take `{name}` straight off the URL, which is the
shape that turns into a traversal the moment anybody builds a filename out of
it, and an allowlist is right about that for the same reason
`api.check_job_id` is: it refuses `../../etc/passwd` for what it is rather than
for where it would have pointed.

**Nothing in here echoes a value.** Not into a log line, not into an exception
message, not into a `repr`. The one place that rule is not obvious is the
unknown-provider case on read: the likeliest way a stranger's name reaches that
branch is an operator who swapped a name and a value while editing the file by
hand, so the key would *be* the name -- and `api.ApiError` puts an exception's
message in a response body. The count is reported and the names are not.

**The bind token replaces the loopback assumption rather than adding to it.**
`api.check_host` refuses any `Host` that is not loopback, and it is not a
formality: binding `127.0.0.1` stops a packet from another machine and does
nothing about a page in the operator's own browser resolving an attacker's name
to `127.0.0.1` and posting to it. That check is a *substitute* for
authentication -- it is what a server with no way to tell one requester from
another can do instead. Once a token is configured the real thing is available
and the substitute is in the way: a deployment reached over the network is
reached by some name, every such name fails the loopback test, and the rebinding
attack the check exists for is already answered because the attacker's page
cannot read the token. So `Api.check_access` runs one or the other, never both.

**A provider's endpoint lives here too, beside the key it is paired with.**
The model picker sets a model *name*; the address that name is sent to has to
come from somewhere, and `jobs.REQUEST_SETTABLE` refuses `LLOSSLESS_BASE_URL`
because a request is not a place an address belongs. So the address is stored
here instead, in this same `0600` file, one row per provider, freely editable
through the settings page -- the command line switches endpoint and model with
two flags and the page has to be no less free, or the exploration it exists to
invite does not happen. The consequence worth stating is that a catalogue model
whose provider has no endpoint here is a model this server cannot reach, and it
is refused at submit rather than offered and failed two steps into a run.

**The key is bound to the endpoint, and the accident it prevents is an
ordinary one.** Changing a provider's address does not carry its key across.
Not because the next person to type an address is assumed hostile -- they are
not -- but because moving an endpoint and not noticing that the previous
provider's key is still attached to it is a mistake anybody makes on an
ordinary afternoon, and the result is a real credential sent to a host that was
typed in thirty seconds ago. `Endpoint.moved_to` makes it unrepresentable
rather than merely discouraged: it is the only call that changes an address,
and it returns a pair with no key in it.

**An endpoint is checked with `config`'s own two guards, not with a check of
this module's own.** `config.check_base_url` refuses a scheme that is not
http(s), because `urllib.request.build_opener` installs `FileHandler` and
`FTPHandler` from its defaults and a `file://` base URL has a local file's
bytes parsed as a model answer. `config.check_cleartext_key` refuses putting a
bearer token on the wire unencrypted to a host that is not this machine. A
second implementation here would be a second set of rules to keep in step with
the first, and the one that drifted would be this one -- the settings page is
not where anybody looks when they change a rule about transport.

**A URL carrying userinfo is refused rather than stripped.** `https://user:tok@host/v1`
is a credential written into an address, and an address is not held to the
rules a key is held to here: it is reported back to the page and it reaches
`banner_endpoint` in a job's event log. Refusing says what to do instead -- the
key goes in the key field, one field along.
"""

from __future__ import annotations

import contextlib
import hmac
import ipaddress
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from .. import config

# Which environment variable holds which provider's key. An allowlist, and the
# whole of what a `{name}` in a URL is permitted to mean.
#
# The names are the `provider` values `catalogue.json` already uses, so the
# settings page and the model picker call the same vendor the same thing --
# `tests/test_web_credentials.py` asserts that rather than leaving it to
# whoever edits the catalogue next. `google` has had catalogue rows since
# the free-tier run of 2026-09-25; it was here before them, because a
# key can be configured before a model from it has ever been measured.
#
# `self-hosted` maps to `config.DEFAULT_KEY_ENV`, read from `config` rather
# than restated, because that variable is not only the self-hosted bearer
# token: it is the fallback `Settings.api_key_env_for` returns for every role
# that has no `LLOSSLESS_API_KEY_ENV_<ROLE>` of its own. A row for it is
# therefore the row an operator with one endpoint actually wants, and naming it
# after the catalogue's word for that endpoint is the least surprising label
# available.
PROVIDERS: dict[str, str] = {
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_AI_API_KEY",
    "openai": "OPEN_AI_API_KEY",
    "self-hosted": config.DEFAULT_KEY_ENV,
}

# Asserted rather than commented. Two providers sharing one variable would make
# `DELETE` on either clear the key of both, and the operator would find out by
# watching a run fail on a credential they never touched.
assert len(set(PROVIDERS.values())) == len(PROVIDERS)

# The well-known OpenAI-compatible address of each vendor provider, so
# the Credentials sheet can offer it and a person only pastes a key. The
# operator: "We should pre set the default, well-known endpoints into the UI
# for Anthropic, OpenAI and Google."
#
# **Only an offer to the page, never a value anything resolves.** Nothing on
# the server reads this table to decide where a request or a key goes: a
# provider with no stored address still has none, is not configured, and its
# models stay unreachable. The page shows the address, and saving stores it
# as an explicit value through `Credentials.set_endpoint` -- the same call a
# typed address takes, through `clean_base_url` and both of `config`'s guards
# -- so a later change to this table cannot move a stored endpoint, and so a
# key is only ever bound to an address that was on screen when it was saved.
#
# Each is the address this repository's own vendor runs used, not
# a guess:
#   anthropic  `arms/2026-09-25/vendor/run_api.py` (Opus 5.5 over the
#              OpenAI-compatible `/v1/chat/completions`)
#   openai     the same file (GPT-6 Sol and Luna)
#   google     `arms/2026-09-25/google/run_api.py` and its `REGISTRATION.md`
#              (the Gemini free-tier run)
# Each already carries its path, so `config.with_api_path` appends nothing.
PRESET_URLS: dict[str, str] = {
    "anthropic": "https://api.anthropic.com/v1",
    "google": "https://generativelanguage.googleapis.com/v1beta/openai",
    "openai": "https://api.openai.com/v1",
}

# What the self-hosted address field shows as an example, and only as a
# placeholder: the address `config` defaults to, a local ollama. Never
# stored, never pre-filled -- a self-hosted endpoint is wherever the
# operator's own box is, and there is no well-known one to offer.
EXAMPLE_URLS: dict[str, str] = {
    "self-hosted": config.DEFAULT_BASE_URL,
}

# A preset for a provider this module does not know would be an address the
# page offers for a row that does not exist.
assert set(PRESET_URLS) | set(EXAMPLE_URLS) <= set(PROVIDERS)
assert not set(PRESET_URLS) & set(EXAMPLE_URLS)
assert all(url.startswith("https://") and not url.endswith("/")
           for url in PRESET_URLS.values())

# Where a provider's endpoint lives in the server's own environment.
#
# An environment variable rather than an object passed from here into the job
# store, for the same reason the key is one: `Credentials.apply` is already how
# a value configured through the page reaches a run, the job store already
# copies the environment it resolves against, and a second channel would be a
# second thing to keep in step. It is also what lets an operator who never
# opens the settings page configure the same thing in the unit file that starts
# the server.
#
# The prefix is deliberately not `LLOSSLESS_BASE_URL`-shaped. `config.from_env`
# reads `LLOSSLESS_BASE_URL` and `LLOSSLESS_BASE_URL_<ROLE>`, and a variable
# that looked like either would be read by a *run* -- which is exactly backwards:
# these are the operator's map from a provider to an address, and the job layer
# translates the entries it needs into the per-role variables `config` reads,
# once it knows which provider each role's model belongs to.
PROVIDER_URL_PREFIX = "LLOSSLESS_PROVIDER_URL_"

# And what that endpoint said it serves, beside it, one name per line.
#
# The job layer needs this and cannot read the file: a model discovered by
# probing an endpoint is not in the catalogue, so "which provider serves this
# name" has no other answer, and without one a discovered model would be sent
# to whichever endpoint the server was started with -- which is the exact
# defect this milestone exists to remove, reintroduced one layer down. Found
# by driving the page in a browser; no file-level check saw it.
#
# Newline-separated rather than JSON because a model name cannot contain one:
# `discover` strips and length-caps every name it takes, and `read` refuses a
# listing that is not a list of strings.
PROVIDER_MODELS_PREFIX = "LLOSSLESS_PROVIDER_MODELS_"

# Longer than this is not an address. A settings form is a place where a whole
# file gets pasted into a text box by accident, and the refusal belongs at the
# door.
MAX_URL_LENGTH = 2048


def url_env(name: str) -> str:
    """Which environment variable holds this provider's endpoint.

    `self-hosted` becomes `LLOSSLESS_PROVIDER_URL_SELF_HOSTED`: the hyphen has
    to go, because a variable name carrying one cannot be exported by a POSIX
    shell and an operator setting this outside the settings page is setting it
    in a shell or a unit file.
    """
    return PROVIDER_URL_PREFIX + check_provider(name).upper().replace("-", "_")


def models_env(name: str) -> str:
    """Which environment variable holds what this provider's endpoint listed."""
    return PROVIDER_MODELS_PREFIX + check_provider(name).upper().replace("-", "_")


def provider_serving(model: str, environ) -> str | None:
    """Which configured endpoint listed this model, or None.

    The lookup for a model the catalogue has never heard of. A discovered model
    belongs to the endpoint that named it, and nothing else knows that: it has
    no catalogue row to read a provider off, so without this it would go to
    whichever endpoint the server was started with.

    None for a name nothing listed, which is the hand-typed case and is not an
    error -- the request says where that goes, or it goes to the server's own
    endpoint, which is what a typed model id has always done.

    Ordered by provider name so that two endpoints listing one model resolve
    the same way twice. That is a tie nobody can break correctly from here --
    the model really is on both -- so it is broken predictably instead.
    """
    for name in sorted(PROVIDERS):
        listed = (environ.get(models_env(name)) or "").split("\n")
        if model in [entry.strip() for entry in listed if entry.strip()]:
            return name
    return None


# The same assertion as the one above, for the same failure one field along:
# two providers whose names differed only by a hyphen would share one variable,
# and clearing either endpoint would clear both.
assert len({PROVIDER_URL_PREFIX + n.upper().replace("-", "_")
            for n in PROVIDERS}) == len(PROVIDERS)

# What the file says it is. A version rather than a bare mapping so that a
# later shape can be recognised instead of guessed at, and refused with a
# sentence instead of a `KeyError` three layers down.
#
# 2 is the pair. Version 1 held `{"keys": {provider: key}}`, an address
# nowhere, and every run went to whichever single endpoint the server had been
# started with. A version 1 file is still *read* -- see `read()` -- because
# refusing it would silently start a server with no credentials at all and tell
# nobody, and because a key with no address recorded against it is exactly a
# pair whose address has not been set yet.
SCHEMA_VERSION = 2
READABLE_SCHEMA_VERSIONS = (1, 2)

# Owner, and nobody else. The file mode is checked on read and set on write;
# the directory's matters as much, because a directory another account can
# write is a directory in which the file can be replaced.
FILE_MODE = 0o600
DIR_MODE = 0o700

FILE_NAME = "credentials.json"

# Where the file lives, and the variable that moves it. Named `LLOSSLESS_`
# like everything else the operator sets, but read here rather than in
# `config.py`: `config.from_env` builds the settings a *run* resolves against,
# and nothing a run does should be able to see, let alone name, the file the
# keys came out of.
PATH_ENV = "LLOSSLESS_CREDENTIALS"

# A key shorter than this is a paste that lost most of itself. The number is
# not about strength -- this module does not get to have an opinion about a
# vendor's key format -- it is about the two failures a length check can
# actually catch: an empty paste, and a fragment. Eight also keeps `suffix()`
# honest, since the last four characters of a six-character key are most of the
# credential rather than a hint about which one it is.
MIN_KEY_LENGTH = 8

# Above this it is not a key. A settings form is a place where a whole file
# gets pasted into a text box by accident, and the refusal should happen at the
# door rather than after it has been written to disk.
MAX_KEY_LENGTH = 8192

# How many characters of a configured key may be reported back. Four, which is
# enough for an operator to tell which of two keys is loaded and not enough to
# be a fragment of one. Nothing else about a value ever leaves this module.
SUFFIX_LENGTH = 4

# The token, and where it comes from. An environment variable and never a
# tracked file: the address a pod answers on is already handled that way in
# this project, and a token in a file is a token in somebody's shell history
# the first time they `cat` it.
TOKEN_ENV = "LLOSSLESS_WEB_TOKEN"

# The header every request carries once a token is configured. A header of this
# project's own rather than `Authorization`, for the reason
# `api.check_content_type` gives about JSON: a cross-origin page cannot set a
# custom header without a preflight, and this server answers no preflight at
# all. So the same header that authenticates a request is also the part of the
# CSRF defence that does not depend on anything the attacker controls.
TOKEN_HEADER = "X-LLossless-Token"

# Below this a token is a password, and a password on a network port is
# guessable at whatever rate the box will answer. The refusal is the same
# refusal as no token, because the server is being asked to do the same thing.
MIN_TOKEN_LENGTH = 16

# Names that mean this machine without being addresses. Only the one: a name
# that happens to resolve to `127.0.0.1` today is a DNS answer and not a
# property of the bind, and treating it as loopback would let a resolver
# decide whether this server needs authentication.
LOOPBACK_NAMES = frozenset({"localhost"})


class CredentialsError(Exception):
    """The credentials file cannot be used, and the reason is safe to repeat.

    Every message raised as one of these names the file, the mode or the shape
    and never a value -- `api.ApiError` puts an exception's message into a
    response body, so the discipline has to hold at the point the string is
    built rather than at the point it is served.
    """


class UnknownProvider(CredentialsError):
    """A provider name that is not in `PROVIDERS`. Refused, never looked up."""


class BindRefused(Exception):
    """This server may not start on this address with this token.

    A separate class from `CredentialsError` because it is answered somewhere
    else entirely: `CredentialsError` becomes a response, and this becomes a
    line on stderr and an exit code, before any socket exists.
    """


@dataclass(frozen=True)
class Endpoint:
    """One provider's address, the key that may be sent to it, and what it serves.

    **The address and the key are one object because they are one decision.**
    The rule this whole arrangement rests on is that no key is ever sent to an
    endpoint it was not stored against: the original danger was a submitter
    aiming this server, holding the operator's key, at a host of their
    choosing, and binding the pair severs it -- change the address and the
    operator's key does not travel with you, so whoever moved the endpoint has
    to bring their own.

    That is a property of the *shape* here rather than a rule somebody has to
    remember. There is no setter for an address that keeps a key: `moved_to`
    returns a whole new pair with no key in it, and it is the only way an
    address changes. Two independent fields with two independent mutators would
    desynchronise the first time an edit touched one of them, and the failure
    would be silent and would be the exact failure the pairing exists to
    prevent.

    `models` is what the endpoint answered when it was asked what it serves.
    It rides with the address, not with the key, and `moved_to` drops it for
    the same reason it drops the key: a list of models is a fact about one
    host, and carrying it to another would offer the operator models the new
    address has never heard of. It is not a secret and it is served to the
    page; it is here rather than in a cache because it has exactly the lifetime
    of the address it was read from.

    `repr` is written rather than generated. A frozen dataclass's default
    `repr` prints every field, this one holds a key, and a `repr` reaches a log
    line, a debugger and an exception's own rendering without anybody deciding
    that it should.
    """

    base_url: str = ""
    key: str = ""
    models: tuple[str, ...] = ()

    def __repr__(self) -> str:
        return (f"Endpoint(base_url={self.base_url!r}, "
                f"key={'<set>' if self.key else '<unset>'}, "
                f"models={len(self.models)})")

    def moved_to(self, base_url: str) -> Endpoint:
        """The same provider at a new address, with no key and no model list.

        The only way an address changes anywhere in this module. See the class
        docstring: this is the pairing, expressed as the absence of any other
        route.
        """
        return Endpoint(base_url=base_url)

    def with_key(self, key: str) -> Endpoint:
        """The same address, with a key stored against it.

        The models survive: they are a fact about the address, and the address
        has not moved.
        """
        return Endpoint(base_url=self.base_url, key=key, models=self.models)

    def listing(self, models) -> Endpoint:
        """The same pair, with what the endpoint said it serves."""
        return Endpoint(base_url=self.base_url, key=self.key,
                        models=tuple(models))

    @property
    def empty(self) -> bool:
        """Nothing set. Written out of the file rather than stored as a blank row."""
        return not self.base_url and not self.key and not self.models


# --------------------------------------------------------------------------
# where the file is
# --------------------------------------------------------------------------


def default_path(environ=None) -> Path:
    """`$XDG_CONFIG_HOME/llossless/credentials.json`, or the spec's fallback.

    `config.config_file` does the lookup rather than `config._xdg`, for one
    reason that matters here: `_xdg` reads `os.environ` directly, and every
    check in `tests/test_web_credentials.py` that has an opinion about where
    this file goes has to be able to say so without editing the environment of
    the process running the suite.
    """
    source = os.environ if environ is None else environ
    named = (source.get(PATH_ENV) or "").strip()
    if named:
        return Path(named).expanduser()
    return config.config_file(FILE_NAME, source)


def check_provider(name) -> str:
    """The provider name, or `UnknownProvider`. The only thing `{name}` may be.

    Returned rather than merely validated so that a call site cannot use the
    checked name and the raw one in the same breath, which is how the check
    ends up running beside the value instead of in front of it.
    """
    if not isinstance(name, str) or name not in PROVIDERS:
        raise UnknownProvider(
            f"there is no provider by that name. The providers are "
            f"{', '.join(sorted(PROVIDERS))}. A name is looked up in that list "
            f"and is never used to build a path.")
    return name


def clean_key(value) -> str:
    """A pasted key, stripped, or `CredentialsError` saying which way it is wrong.

    The message says what was wrong with the value and never what the value
    was, including in the too-long case, where quoting even a prefix would be
    quoting a key.
    """
    if not isinstance(value, str):
        raise CredentialsError(
            f"a key is a string; got a {type(value).__name__}.")
    key = value.strip()
    if not key:
        raise CredentialsError("the key is empty. Delete the provider's entry "
                               "instead of setting it to nothing.")
    if len(key) < MIN_KEY_LENGTH:
        raise CredentialsError(
            f"that key is {len(key)} characters and the shortest a provider "
            f"issues is longer than {MIN_KEY_LENGTH}; it is almost certainly a "
            f"paste that lost most of itself.")
    if len(key) > MAX_KEY_LENGTH:
        raise CredentialsError(
            f"that key is {len(key)} characters, which is past the "
            f"{MAX_KEY_LENGTH} this accepts. A whole file was probably pasted "
            f"into the box.")
    if any(character in key for character in "\r\n\t") or not key.isprintable():
        raise CredentialsError(
            "that key carries a line break or a control character. It was "
            "pasted out of something that added one, and sending it as a "
            "header value is not a thing this tool will do.")
    return key


def suffix(value: str) -> str:
    """The last four characters of a key. The only part of one that is ever served."""
    return value[-SUFFIX_LENGTH:]


def clean_base_url(name, value) -> str:
    """One provider's endpoint, checked the way a run's own endpoint is checked.

    The shape checks here are this module's -- a string, not empty, not a
    pasted file, no control character, no userinfo -- and then the two that
    decide whether the address is safe to talk to are `config`'s own, run on a
    throwaway `Settings` built with this provider's key variable:

      `config.check_base_url`        refuses anything that is not http(s).
                                     `urllib.request.build_opener` installs
                                     `FileHandler` and `FTPHandler` from its
                                     defaults, so a `file://` endpoint has a
                                     local file's bytes parsed as a model
                                     answer, and the suite's socket guard
                                     cannot see it because no socket is opened.

      `config.check_cleartext_key`   refuses `http://` to a host that is not
                                     this machine while a key for this provider
                                     is in the environment. The key would go on
                                     the wire unencrypted once per call.

    The second reads the *live* environment, deliberately, because the question
    it answers is about the credential the next call would actually spend, and
    that is whatever `Settings.api_key` finds at send time. So the order in
    which an operator fills the two fields matters and is the honest way round:
    saving a key for a provider whose endpoint is cleartext, or a cleartext
    endpoint for a provider whose key is already set, is refused at whichever
    of the two arrives second.

    Returned rather than merely validated, and returned stripped of a trailing
    slash and nothing else. The `/v1` that an OpenAI-compatible endpoint needs
    is supplied by `config.with_api_path` when a run resolves, not here: two
    places normalising one address is how the file and the run end up
    disagreeing about what the operator typed.
    """
    name = check_provider(name)
    if not isinstance(value, str):
        raise CredentialsError(
            f"an endpoint is a URL, so a string; got a {type(value).__name__}.")
    url = value.strip()
    if not url:
        raise CredentialsError(
            "the endpoint is empty. Delete the provider's endpoint instead of "
            "setting it to nothing.")
    if len(url) > MAX_URL_LENGTH:
        raise CredentialsError(
            f"that endpoint is {len(url)} characters, which is past the "
            f"{MAX_URL_LENGTH} this accepts. A whole file was probably pasted "
            f"into the box.")
    if any(character in url for character in "\r\n\t ") or not url.isprintable():
        raise CredentialsError(
            "that endpoint carries a space, a line break or a control "
            "character. An address has none of those, so this is a paste that "
            "brought something with it.")
    url = url.rstrip("/")
    if "@" in urlsplit(url).netloc:
        raise CredentialsError(
            "that endpoint carries a username or a password in the address. "
            "An endpoint is reported back to the page and printed in a run's "
            "event log, and a credential written into an address would travel "
            "with it. Put the key in the key field for this provider and give "
            "the address on its own.")
    probe = config.Settings(base_url=url, api_key_env=PROVIDERS[name])
    try:
        config.check_base_url(probe)
        config.check_cleartext_key(probe)
    except config.ConfigError as refusal:
        raise CredentialsError(str(refusal)) from None
    return url


# --------------------------------------------------------------------------
# the token
# --------------------------------------------------------------------------


def is_loopback(host) -> bool:
    """Does this bind address mean "this machine only"? Fails closed.

    The empty string is the answer worth spelling out: `("", port)` is a
    wildcard bind, it reaches every interface, and it matches no address
    pattern at all -- `tests/test_web_server.py` keeps a detector for exactly
    that spelling because the address-shaped one cannot see it. It is not
    loopback here either.

    A name that is not `localhost` and does not parse as an address is not
    loopback, even if this machine's resolver would send it here. Whether a
    deployment needs authentication is not a question a DNS answer gets to
    decide.
    """
    value = (host or "").strip().lower()
    if not value:
        return False
    if value in LOOPBACK_NAMES:
        return True
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    try:
        return ipaddress.ip_address(value).is_loopback
    except ValueError:
        return False


def require_token(host, token, *, accounts: int = 0) -> str:
    """The token this bind needs, or `BindRefused` saying why there is no server.

    This is the check the token requirement was built around, so it refuses before a socket exists
    rather than after: a server that binds first and discovers its
    configuration second is a server that was, for however long that took, a
    key-spending endpoint on the network with nothing in front of it.

    A short token is refused as hard as a missing one. The operator is asking
    for the same thing in both cases -- a port answering to anybody who can
    reach it -- and a four-character token on a network port is a password
    guessable at whatever rate the box will answer.

    **`accounts` is what retires this.** 461 demanded a token for a
    non-loopback bind because opening to a network and authenticating the
    caller are one decision and there was nothing else that could make it. With
    accounts there is: logging in *is* that authentication, per request and per
    person, which is strictly more than a shared secret was ever going to be.
    So a server with at least one account may bind any address with no token at
    all, and `api.Api.check_access` stops consulting one -- because two
    parallel secrets where one has been superseded is an arrangement in which
    the wrong one stays configured for years.

    With **no** accounts the old rule stands in full, and that is not a
    leftover: a server nobody has an account on is a server in setup, its one
    reachable route creates the first account, and a networked bind still has
    to be something more than a URL somebody found.
    """
    given = (token or "").strip()
    if is_loopback(host):
        return given
    if accounts > 0:
        return given
    if not given:
        raise BindRefused(
            f"refusing to bind {host or 'every interface'}: an address that is "
            f"not loopback needs a token, and {TOKEN_ENV} is not set. This "
            f"server spends the credential its own environment holds on every "
            f"document submitted to it, so reaching it from the network and "
            f"authenticating the submitter are one decision and not two. Set "
            f"{TOKEN_ENV} to a secret of at least {MIN_TOKEN_LENGTH} "
            f"characters, or leave the address at the loopback default. Once "
            f"this server has an account on it, logging in is that "
            f"authentication and no token is wanted here at all.")
    if len(given) < MIN_TOKEN_LENGTH:
        raise BindRefused(
            f"refusing to bind {host or 'every interface'}: {TOKEN_ENV} is "
            f"{len(given)} characters and a token guarding a network port must "
            f"be at least {MIN_TOKEN_LENGTH}. A short one is refused as hard as "
            f"a missing one, because the port answers a guess just as fast. "
            f"Once this server has an account on it, logging in is that "
            f"authentication and no token is wanted here at all.")
    return given


def token_from(environ=None) -> str:
    """The configured token, or ``. Read at start, never stored on disk."""
    source = os.environ if environ is None else environ
    return (source.get(TOKEN_ENV) or "").strip()


def token_matches(presented, expected: str) -> bool:
    """Constant-time comparison of the presented token against the configured one.

    `hmac.compare_digest` and never `==`. A `==` on strings returns at the
    first differing byte, so the time it takes to refuse is a measurement of
    how many leading characters were right -- which turns guessing a token from
    a search of the whole space into a search of one character at a time. A
    check that is correct on every input and wrong about how long it takes is
    still wrong.

    Encoded to bytes first, because `compare_digest` on two `str` raises if
    either holds a character outside ASCII, and a token pasted from a password
    manager is not guaranteed to be ASCII. A refusal must not be able to become
    a 500.

    No configured token matches nothing, including the empty string. The
    callers only ask when a token is configured, so this branch is unreachable
    by design -- which is exactly why it fails closed. `compare_digest(b"",
    b"")` is `True`, so the obvious no-op version of this guard would turn a
    server that had lost its token into a server that admitted everybody.
    """
    if not expected:
        return False
    given = presented if isinstance(presented, str) else ""
    return hmac.compare_digest(given.strip().encode("utf-8"),
                               expected.encode("utf-8"))


# --------------------------------------------------------------------------
# the file
# --------------------------------------------------------------------------


class Credentials:
    """The credentials file: read it, write it, put it in the environment.

    Holds no key in a field. `read()` returns a mapping to its caller and the
    only callers are `apply()` and the two mutators, each of which uses it
    within one statement and drops it; nothing on this object survives a call
    holding a value, so there is nothing for a `repr` or a traceback to find.

    `_applied` is the exception and is not a value: it is the set of variable
    *names* this object put into an environment, kept so that deleting a
    provider can unset its variable without this object being able to unset a
    variable the operator's own shell exported. A credentials manager that
    cleared a variable it never set would silently disarm a working deployment
    the first time somebody pressed delete on an unrelated row.
    """

    def __init__(self, path=None, *, environ=None) -> None:
        self.path = Path(path) if path is not None else default_path(environ)
        self._applied: set[str] = set()

    def __repr__(self) -> str:
        """The file and the count. Never a name, never a value.

        A `repr` reaches a log line, a debugger and an exception's own
        rendering without anybody deciding that it should, which is why the
        rule about what may be in one is enforced here rather than at the call
        sites.
        """
        return f"Credentials(path={str(self.path)!r})"

    # -- reading ---------------------------------------------------------

    def read(self) -> dict[str, Endpoint]:
        """Every pair in the file, or `{}` if there is none. Raises if it is unusable.

        Returns `Endpoint`s and not keys, because the pairing is the invariant:
        a caller that could ask for the keys alone is a caller that can send
        one to an address it did not come with.

        A version 1 file is read as pairs with no address. That shape predates
        per-provider endpoints -- there was one endpoint, the server's own --
        and it is exactly a key whose address has not been set yet, so it is
        migrated rather than refused. Refusing it would start a server with no
        credentials at all over a file that is perfectly intelligible, and the
        operator would find out by watching a run fail on a key they can see in
        the file. The next write puts the file at version 2.

        An absent file is the ordinary state and is not an error: a server that
        has never had a key configured through the page has no file, and
        `llossless serve` is expected to start on such a machine and say
        nothing about it.

        A file whose mode is wider than `0600` is the case this function
        exists for. It is refused and not repaired: the exposure has already
        happened, chmodding it back would delete the evidence, and a key that
        another account on this box has had the opportunity to read is a key to
        rotate rather than a key to keep using more carefully.

        The JSON parser's own message is deliberately not repeated. It carries
        a position rather than content, so quoting it would not leak anything
        today -- but the string it would be quoting is a line number inside a
        file whose other lines are keys, and the habit is the thing worth
        keeping.
        """
        try:
            info = self.path.stat()
        except FileNotFoundError:
            return {}
        except OSError as exc:
            raise CredentialsError(
                f"{self.path} cannot be read: {exc.strerror or exc}") from None

        mode = stat.S_IMODE(info.st_mode)
        if mode & ~FILE_MODE:
            raise CredentialsError(
                f"refusing to read {self.path}: it is mode {mode:04o} and a "
                f"credentials file must be no wider than {FILE_MODE:04o}. "
                f"Every account on this machine has already had the chance to "
                f"read it, so rotate the keys it holds first; `chmod "
                f"{FILE_MODE:04o}` on its own puts an exposed key back into "
                f"service.")

        try:
            raw = self.path.read_text(encoding="utf-8")
        except OSError as exc:
            raise CredentialsError(
                f"{self.path} cannot be read: {exc.strerror or exc}") from None
        except UnicodeDecodeError:
            raise CredentialsError(
                f"{self.path} is not UTF-8, so it was not written by this "
                f"tool.") from None

        try:
            payload = json.loads(raw)
        except ValueError:
            raise CredentialsError(
                f"{self.path} is not readable as JSON. Nothing in it was "
                f"loaded.") from None
        if not isinstance(payload, dict):
            raise CredentialsError(
                f"{self.path} holds a {type(payload).__name__} where this "
                f"expects an object.")
        version = payload.get("version")
        if version not in READABLE_SCHEMA_VERSIONS:
            raise CredentialsError(
                f"{self.path} declares schema version "
                f"{version!r}; this build writes {SCHEMA_VERSION} and reads "
                f"{', '.join(str(v) for v in READABLE_SCHEMA_VERSIONS)}.")
        field = "keys" if version == 1 else "endpoints"
        rows = payload.get(field)
        if not isinstance(rows, dict):
            raise CredentialsError(
                f"{self.path} has no `{field}` object in it.")

        out: dict[str, Endpoint] = {}
        unknown = 0
        for name, value in rows.items():
            if not isinstance(name, str) or name not in PROVIDERS:
                # Counted, not named. See the module docstring: the likeliest
                # route to this branch is a hand edit that swapped a name and a
                # value, in which case the name *is* a key, and this message
                # can reach a response body.
                unknown += 1
                continue
            out[name] = self._row(name, value, version)
        if unknown:
            raise CredentialsError(
                f"{self.path} carries {unknown} entr"
                f"{'y' if unknown == 1 else 'ies'} under a name this build "
                f"does not recognise. The providers are "
                f"{', '.join(sorted(PROVIDERS))}. The names are not repeated "
                f"here: the usual way one gets in is a key and a name written "
                f"the wrong way round.")
        return out

    def _row(self, name: str, value, version: int) -> Endpoint:
        """One entry, whichever schema wrote it, as an `Endpoint`.

        Nothing read back off disk is re-run through `clean_base_url`, and that
        is deliberate rather than an omission: that function resolves a host
        name and judges the answer against how *this* server is deployed, and a
        read happens on every settings request and at every start. A file whose
        address was written by an older deployment is the operator's own file,
        and refusing to start over it would make a stored address able to lock
        the operator out of their own settings page. The shape is checked; the
        policy is checked where a value is set.
        """
        if version == 1:
            if not isinstance(value, str) or not value.strip():
                raise CredentialsError(
                    f"{self.path}'s entry for {name} is empty or is not a "
                    f"string. Remove the entry rather than blanking it.")
            return Endpoint(key=value.strip())
        if not isinstance(value, dict):
            raise CredentialsError(
                f"{self.path}'s entry for {name} is a "
                f"{type(value).__name__} where this expects an object with a "
                f"base_url and a key.")
        base_url = value.get("base_url") or ""
        key = value.get("key") or ""
        models = value.get("models") or []
        if not isinstance(base_url, str) or not isinstance(key, str):
            raise CredentialsError(
                f"{self.path}'s entry for {name} has a base_url or a key that "
                f"is not a string.")
        if not isinstance(models, list) or any(
                not isinstance(model, str) for model in models):
            raise CredentialsError(
                f"{self.path}'s entry for {name} has a models field that is "
                f"not a list of names.")
        # A key with no address is not a broken pair, it is the pair whose
        # address is this server's own `LLOSSLESS_BASE_URL`. That is the
        # shape every version 1 file has and the shape a single-endpoint
        # deployment still wants, and it satisfies the rule rather than
        # dodging it: the destination is the one the operator started the
        # server with, which is operator configuration by definition. What the
        # rule forbids is a key *surviving an address change*, and there is no
        # path here that does that -- `moved_to` is the only way an address
        # moves and it returns a pair with no key.
        return Endpoint(base_url=base_url.strip(), key=key.strip(),
                        models=tuple(models))

    def names(self) -> list[str]:
        """Which providers the file holds anything for, in a stable order."""
        return sorted(self.read())

    # -- writing ---------------------------------------------------------

    def set(self, name, key) -> None:
        """Store one provider's key against whatever endpoint it has.

        An endpoint of its own if one is recorded, and this server's own
        `LLOSSLESS_BASE_URL` if none is -- which is the single-endpoint
        deployment this tool shipped with and is still the ordinary one. Either
        way the key is stored against an address the operator chose, which is
        the rule; what the rule forbids is a key outliving a change of address,
        and `set_endpoint` is where that is enforced.
        """
        name = check_provider(name)
        rows = self.read()
        rows[name] = rows.get(name, Endpoint()).with_key(clean_key(key))
        self._write(rows)

    def remove(self, name) -> bool:
        """Drop one provider's key, keeping its endpoint. True if there was one.

        The False case writes nothing and is not an error, so that `DELETE` can
        be idempotent the way `Api.delete` already is: the operator asked for
        the key to be gone and it is gone, and a client retrying after a
        dropped connection should not be told its first attempt failed.
        """
        name = check_provider(name)
        rows = self.read()
        current = rows.get(name)
        if current is None or not current.key:
            return False
        rows[name] = current.with_key("")
        self._write(rows)
        return True

    def set_endpoint(self, name, base_url, *, models=None) -> Endpoint:
        """Point one provider at an address. **The key it had does not survive.**

        `Endpoint.moved_to` is what does it, and it is the only way an address
        changes here, so "the key is cleared" is not a step this method could
        forget to take -- there is no version of this call that keeps one.
        Whoever moves an endpoint brings their own credential, which is the
        whole of why a submitter naming an endpoint is not a submitter spending
        the operator's key.

        Re-storing the *same* address clears the key too. That looks
        over-eager and is not: this method cannot tell a no-op from a
        correction, the operator typing an address they believe is already
        there is exactly the case where a stale key would be silently reused,
        and re-entering a key is cheap next to sending one somewhere it was
        never meant to go.

        Returns the stored pair so that a caller which has just probed the
        endpoint can attach what it found without reading the file again.
        """
        name = check_provider(name)
        url = clean_base_url(name, base_url)
        rows = self.read()
        moved = rows.get(name, Endpoint()).moved_to(url)
        if models is not None:
            moved = moved.listing(models)
        rows[name] = moved
        self._write(rows)
        return moved

    def remove_endpoint(self, name) -> bool:
        """Forget one provider's endpoint, and with it the key and the listing.

        The whole row goes. Keeping the key would leave a credential with no
        recorded destination, which `_row` refuses to read back anyway -- the
        two halves of the same rule, on the write side and the read side.
        """
        name = check_provider(name)
        rows = self.read()
        if name not in rows:
            return False
        del rows[name]
        self._write(rows)
        return True

    def set_models(self, name, models) -> None:
        """Record what an endpoint said it serves. Nothing else about it moves."""
        name = check_provider(name)
        rows = self.read()
        current = rows.get(name)
        if current is None or not current.base_url:
            return
        rows[name] = current.listing(models)
        self._write(rows)

    def _write(self, rows: dict[str, Endpoint]) -> None:
        """The whole file, atomically, never wider than `0600` for an instant.

        Four things in order, and the order is the point.

        The directory is created and chmodded first, because a `0755` directory
        holding a `0600` file is a directory in which another account can
        rename the file out of the way and leave one of its own.

        The temporary file is opened `O_EXCL` in the same directory -- the same
        directory because `os.replace` is only atomic within a filesystem, and
        a temporary under `/tmp` would degrade the replace into a copy on any
        machine where they differ.

        It is `fchmod`ed on its own descriptor before a byte is written. Not
        `chmod` by path, which is a second lookup and a race; not after the
        write, which would leave a whole key on disk at whatever the umask
        allowed for as long as the flush took.

        And it is `fsync`ed before the replace, so that a machine that loses
        power between the two comes back holding the old file rather than an
        empty new one.
        """
        parent = self.path.parent
        parent.mkdir(parents=True, exist_ok=True)
        os.chmod(parent, DIR_MODE)
        # An empty pair is dropped rather than written as a row of blanks: a
        # provider nobody has configured and a provider whose configuration was
        # deleted are the same state, and two spellings of one state is how a
        # reader of the file ends up believing there is a difference.
        stored = {name: {"base_url": row.base_url, "key": row.key,
                         "models": list(row.models)}
                  for name, row in sorted(rows.items()) if not row.empty}
        payload = json.dumps({"version": SCHEMA_VERSION, "endpoints": stored},
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

    # -- the environment -------------------------------------------------

    def apply(self, *environs) -> tuple[str, ...]:
        """Load the file into one or more environments. Returns the variables set.

        This is the whole of how a key configured through the page reaches a
        run. `Settings.api_key()` reads `os.environ` at send time, so a key put
        there is a key the next model call uses -- including a call in a merge
        that is already running, which is correct: the operator changed their
        credential, and the alternative is a queued job spending a key its
        owner has just revoked.

        Called at start and after every change. Calling it after a change is
        what makes the settings page a setting rather than a note to self: the
        file alone is read once, and a server that only read it at boot would
        tell the operator their key was saved and then go on spending the old
        one until a restart.

        The address goes in beside the key, under `url_env`, and the two are
        written in one pass over one mapping so that an environment can never
        hold half a pair. A variable this object did not set is never removed,
        which is what lets an operator configure a provider entirely in the
        unit file that starts the server and have the page leave it alone.
        """
        targets = environs or (os.environ,)
        wanted = self.mapping()
        for variable in sorted(self._applied - set(wanted)):
            for target in targets:
                target.pop(variable, None)
        self._applied = set(wanted)
        for variable, value in sorted(wanted.items()):
            for target in targets:
                target[variable] = value
        return tuple(sorted(wanted))

    def describe(self, environ=None) -> list[dict]:
        """Every provider: its endpoint, whether a key is in effect, and four characters.

        The answer comes out of the environment rather than out of the file,
        and that is deliberate: what an operator needs to know is which
        credential the next run will *spend* and which address it will spend it
        at, and that is whatever is in `os.environ` under the two variables --
        put there by this file, by their shell, or by the unit that started the
        server. A page that reported only what this file holds would show
        `configured: false` beside a key that works, which is the sort of
        answer that gets a working deployment taken apart.

        The file is still read, and the read is the point rather than a
        leftover: a file that went world-readable is a finding, and an endpoint
        that answered out of the already-loaded environment would report a
        healthy row over a file the next start is going to refuse.

        `suffix` is absent rather than empty when nothing is configured, so a
        client cannot render four blank characters as though they were a key's
        last four. **The address is reported in full and the key never is**:
        an address is operator configuration that the page has to be able to
        show, it already reaches a submitter through a run's own banner event,
        and `clean_base_url` refuses one carrying userinfo precisely so that
        this row cannot become a way to read a credential.
        """
        stored = self.read()
        source = os.environ if environ is None else environ
        rows = []
        for name in sorted(PROVIDERS):
            variable = PROVIDERS[name]
            value = (source.get(variable) or "").strip()
            address = (source.get(url_env(name)) or "").strip()
            row = {
                "name": name,
                "variable": variable,
                "configured": bool(value),
                "url_variable": url_env(name),
                "base_url": address,
                "endpoint_configured": bool(address),
                "models": list(stored[name].models) if name in stored else [],
            }
            if value:
                row["suffix"] = suffix(value)
            rows.append(row)
        return rows

    def describe_file(self) -> list[dict]:
        """The same rows, answered out of this file alone and never a process's.

        `describe` reads the environment because the operator's question is
        "which credential will the next run spend", and for the server's own
        file the honest answer includes whatever their shell exported.

        **A per-account file is not in that position.** Its keys never reach
        `os.environ` -- that is the whole point of `config.keys_for_this_run`,
        and a second user's key in the process environment is the single-tenancy
        this milestone removes -- so the file is the only place an answer can
        come from, and asking the environment would report the *operator's*
        credential beside a user's provider name.
        """
        stored = self.read()
        rows = []
        for name in sorted(PROVIDERS):
            row = stored.get(name, Endpoint())
            described = {
                "name": name,
                "variable": PROVIDERS[name],
                "configured": bool(row.key),
                "url_variable": url_env(name),
                "base_url": row.base_url,
                "endpoint_configured": bool(row.base_url),
                "models": list(row.models),
            }
            if row.key:
                described["suffix"] = suffix(row.key)
            rows.append(described)
        return rows

    def mapping(self) -> dict[str, str]:
        """What `apply` would put in an environment, without putting it anywhere.

        Split out so that a caller which must *not* write to a process
        environment -- a per-account store, whose keys go through
        `config.keys_for_this_run` instead -- computes the same thing from the
        same pass over the same file. Two functions deriving one mapping is how
        the shared path and the per-account path end up disagreeing about what
        a row means.
        """
        wanted: dict[str, str] = {}
        for name, row in self.read().items():
            if row.key:
                wanted[PROVIDERS[name]] = row.key
            if row.base_url:
                wanted[url_env(name)] = row.base_url
            if row.models:
                wanted[models_env(name)] = "\n".join(row.models)
        return wanted
