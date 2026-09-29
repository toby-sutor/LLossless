"""A person's saved run settings: what the page starts from next time (674).

The operator asked for it in their own words: *"we may offer them a button or
checkbox ... asking if we should save those settings as default: model, effort,
fidelity etc. So next time they log in, they can always use the same settings
for their merges instead of going through the whole process every time."*

**One small file per account, beside that account's credentials.** An account
with a store of its own keeps it at `users/<id>/defaults.json`, the directory
`accounts.Directory` already names by an opaque id; a server with no account
store keeps one file for its single user, beside `credentials.json`. The
operator's is under `users/<id>/` too, although their *credentials* are the
shared file: settings are a person's, and the shared file is the server's.

**Written the way the credentials file is written**: the directory created and
set to `0700` first, a temporary opened `O_EXCL` in that directory and
`fchmod`ed to `0600` before a byte is written, `fsync`ed, then `os.replace`d
over the target. There is no secret in this file -- nothing here is a key, an
address or a password -- but it decides which route the next run takes, and a
route can be a metered API, so a file another account could have written is
not trusted: a file wider than `0600` is refused on read. A save replaces it.

**Nothing is trusted because this server wrote it.** Every value is checked
against what this server offers *this caller* now: a model id against the
catalogue, the command routes and the models the caller's endpoints listed, a
level against `config`, a window against `jobs`' bounds. `check` refuses a
request whole and names the field; `sift` reads a stored file back and keeps
what is still offered, naming what it dropped, because a model that has gone
from an endpoint since it was saved is ordinary rather than an error -- and
never silently replaced, because the page says what was dropped.

Unknown keys are refused rather than ignored, for `api.SUBMIT_FIELDS`' reason:
a misspelt field that is ignored saves nothing and says nothing about it.
"""

from __future__ import annotations

import contextlib
import json
import math
import os
import re
import stat
import threading
from dataclasses import dataclass, field
from pathlib import Path

from . import credentials

# What the file says it is, so a later shape is refused with a sentence.
SCHEMA_VERSION = 1

FILE_NAME = "defaults.json"

# The credentials file's modes, by reference: "the same permissions" is a
# property of the two files, and two constants would be two numbers that can
# drift apart.
FILE_MODE = credentials.FILE_MODE
DIR_MODE = credentials.DIR_MODE

# The most a request body or a stored file may be. A full set is under 600
# bytes; this leaves room for a long typed model id and nothing much else.
MAX_BYTES = 4096

# The fields, in the order the page shows them. Nothing else is accepted.
FIELDS = ("model", "check_model", "window", "effort", "fidelity",
          "verify_depth", "loss_budget", "title_policy")

# How a model was chosen, which is also what its id is checked against:
#   route      one of the operator's command routes, by id
#   catalogue  a catalogue row, by its id
#   listed     a name an endpoint listed, with that endpoint's provider name
#   typed      an id typed into "Use a model id not in the table", with the
#              endpoint "Send it to" named ("" is this server's own)
MODEL_KINDS = ("route", "catalogue", "listed", "typed")
MODEL_KEYS = {"route": ("kind", "id"), "catalogue": ("kind", "id"),
              "listed": ("kind", "id", "endpoint"),
              "typed": ("kind", "id", "endpoint")}
# The checks' own model is a row of the table and never a route or a typed id:
# a route runs every role, and a typed id is used for both roles.
CHECK_KINDS = ("catalogue", "listed")

# What a typed model id may look like. Model names in the wild are letters,
# digits and `. _ : / @ + -` (`Qwen/Qwen3.8-27B-FP8`, `qwen3:8b`,
# `hf.co/org/model:Q4_K_M`); nothing here needs a space, a quote or a control
# character, and all of them would reach a page.
TYPED_ID = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,199}\Z")

# Every id is bounded, whatever it is checked against afterwards.
ID_MAX = 200


class DefaultsError(Exception):
    """The file on disk is unusable. The message names the file, never a value."""


class Refused(Exception):
    """A value this server does not offer. `field` names which."""

    def __init__(self, field_name: str, reason: str) -> None:
        super().__init__(reason)
        self.field = field_name


@dataclass(frozen=True)
class Offer:
    """What this server offers one caller right now. Built by `api.Api.offer`.

    `routes` maps a command route's id to the effort levels it takes (empty
    for a route that takes none). `single_level_routes` names the routes
    among them whose empty tuple means "one level, not a scale" rather than
    "no effort concept at all" (688, ruling 11) -- `sift`'s one way to tell a
    Haiku route's stored level apart from a route that never took one, so it
    can drop the first silently and the second as a named `dropped` entry.
    `catalogue` is the catalogue rows this caller can run: not retired, and on
    a provider with an endpoint, or on none. `listed` maps each configured
    provider to the names it listed. `providers` is the configured providers,
    which a typed id may name.
    """

    routes: dict = field(default_factory=dict)
    single_level_routes: frozenset = frozenset()
    catalogue: frozenset = frozenset()
    listed: dict = field(default_factory=dict)
    providers: frozenset = frozenset()
    fidelity: tuple = ()
    depths: tuple = ()
    titles: tuple = ()
    window_min: int = 1
    window_max: int = 10_000_000


# --------------------------------------------------------------------------
# checking
# --------------------------------------------------------------------------


def _string(field_name: str, value, *, limit: int = ID_MAX) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise Refused(field_name, f"{field_name} is a non-empty string of at "
                                  f"most {limit} characters.")
    return value.strip()


def _model(field_name: str, value, offer: Offer, kinds) -> dict:
    """One model choice, checked against the offer. Returns its clean form."""
    if not isinstance(value, dict):
        raise Refused(field_name, f"{field_name} is an object with a `kind`.")
    kind = value.get("kind")
    if kind not in kinds:
        raise Refused(field_name, f"{field_name}.kind is one of "
                                  f"{', '.join(kinds)}.")
    allowed = MODEL_KEYS[kind]
    unknown = sorted(set(value) - set(allowed))
    if unknown:
        raise Refused(field_name, f"{field_name} carries {', '.join(unknown)}, "
                                  f"which a {kind} model does not have.")
    ident = _string(field_name, value.get("id"))
    if kind == "route":
        if ident not in offer.routes:
            raise Refused(field_name, f"{field_name}: no command route with "
                                      f"that id is offered here.")
        return {"kind": kind, "id": ident}
    if kind == "catalogue":
        if ident not in offer.catalogue:
            raise Refused(field_name, f"{field_name}: that catalogue model is "
                                      f"not offered here.")
        return {"kind": kind, "id": ident}
    endpoint = value.get("endpoint")
    if kind == "listed":
        endpoint = _string(field_name, endpoint)
        if ident not in offer.listed.get(endpoint, ()):
            raise Refused(field_name, f"{field_name}: that endpoint does not "
                                      f"list that model.")
        return {"kind": kind, "id": ident, "endpoint": endpoint}
    # typed
    if not TYPED_ID.match(ident):
        raise Refused(field_name, f"{field_name}: a typed model id is letters, "
                                  f"digits and . _ : / @ + - only.")
    if not isinstance(endpoint, str) or (endpoint and endpoint not in offer.providers):
        raise Refused(field_name, f"{field_name}.endpoint is \"\" for this "
                                  f"server's own, or a configured provider.")
    return {"kind": kind, "id": ident, "endpoint": endpoint}


def _choice(field_name: str, value, choices) -> str:
    text = _string(field_name, value)
    if text not in choices:
        raise Refused(field_name, f"{field_name} is one of {', '.join(choices)}.")
    return text


def _one(name: str, value, offer: Offer, clean: dict):
    """One field, checked. `clean` is what was accepted so far (for effort)."""
    if name == "model":
        return _model(name, value, offer, MODEL_KINDS)
    if name == "check_model":
        model = clean.get("model")
        if model is None or model["kind"] in ("route", "typed"):
            raise Refused(name, "check_model is only saved beside a model from "
                                "the table that is not a command route.")
        return _model(name, value, offer, CHECK_KINDS)
    if name == "window":
        model = clean.get("model")
        if model is None or model["kind"] == "route":
            raise Refused(name, "window is only saved beside the model it was "
                                "stated for, and a command route states its own.")
        if isinstance(value, bool) or not isinstance(value, int) \
                or not offer.window_min <= value <= offer.window_max:
            raise Refused(name, f"window is a whole number of tokens from "
                                f"{offer.window_min} to {offer.window_max}.")
        return value
    if name == "effort":
        model = clean.get("model")
        levels = (offer.routes.get(model["id"], ())
                  if model is not None and model["kind"] == "route" else ())
        if not levels:
            raise Refused(name, "effort is only saved beside a command route "
                                "that takes an effort level.")
        return _choice(name, value, levels)
    if name == "fidelity":
        return _choice(name, value, offer.fidelity)
    if name == "verify_depth":
        return _choice(name, value, offer.depths)
    if name == "title_policy":
        return _choice(name, value, offer.titles)
    if name == "loss_budget":
        if isinstance(value, bool) or not isinstance(value, (int, float)) \
                or not math.isfinite(value) or not 0.0 <= value <= 1.0:
            raise Refused(name, "loss_budget is a fraction from 0 to 1.")
        return float(value)
    raise Refused(name, f"{name} is not a setting that can be saved.")


def _object(payload) -> dict:
    if not isinstance(payload, dict):
        raise Refused("", "the defaults are a JSON object.")
    unknown = sorted(str(key) for key in set(payload) - set(FIELDS))
    if unknown:
        raise Refused(unknown[0], f"these defaults carry {', '.join(unknown)}; "
                                  f"the fields are {', '.join(FIELDS)}. An "
                                  f"unknown field is refused, not ignored.")
    return payload


def check(payload, offer: Offer) -> dict:
    """A request's defaults, all of them valid here, or `Refused` naming a field.

    A field that is absent or null is not saved, and the page then uses the
    server's default for it. In `FIELDS` order, because `effort`, `window` and
    `check_model` are checked against the model accepted before them.
    """
    payload = _object(payload)
    clean: dict = {}
    for name in FIELDS:
        value = payload.get(name)
        if value is None:
            continue
        clean[name] = _one(name, value, offer, clean)
    return clean


def sift(stored: dict, offer: Offer) -> tuple[dict, list[dict]]:
    """What a stored set still offers here, and what it had to drop.

    Each dropped entry is `{"field": ..., "value": ...}`, the value being what
    a person would recognise: a model's id, a level's name. A field that
    depends on a dropped model is dropped with it and named too, rather than
    left to be checked against whatever model the page falls back to.

    One exception (688, ruling 11): a stored `effort` beside a route
    `offer.single_level_routes` names is not offered here either, and `_one`
    refuses it exactly as it would a route that never took a level -- but it
    is not *gone*, the way a retired model or a removed route is. It is a
    field this model was never able to carry, and saying so as a dropped
    setting would read as this server having taken something away. Dropped
    silently instead: not in `kept`, and not named in `dropped`.
    """
    kept: dict = {}
    dropped: list[dict] = []
    for name in FIELDS:
        value = stored.get(name)
        if value is None:
            continue
        try:
            kept[name] = _one(name, value, offer, kept)
        except Refused:
            model = kept.get("model") or stored.get("model")
            if (name == "effort" and isinstance(model, dict)
                    and model.get("kind") == "route"
                    and model.get("id") in offer.single_level_routes):
                continue
            dropped.append({"field": name, "value": _shown(value)})
    for name in sorted(set(stored) - set(FIELDS)):
        dropped.append({"field": str(name), "value": ""})
    return kept, dropped


def _shown(value) -> str:
    """A stored value as a short string for the page's notice. Never long."""
    if isinstance(value, dict):
        value = value.get("id", "")
    if isinstance(value, float):
        return f"{value * 100:.1f}%"
    return str(value)[:ID_MAX]


# --------------------------------------------------------------------------
# the file
# --------------------------------------------------------------------------

# One lock for every defaults file in this process. Saves are rare and small,
# and a lock per path would need a table of locks that outlives the requests.
_LOCK = threading.Lock()


class Store:
    """One person's defaults file: read it, replace it, remove it."""

    def __init__(self, path) -> None:
        self.path = Path(path)

    def __repr__(self) -> str:
        return f"Store(path={str(self.path)!r})"

    def read(self) -> dict | None:
        """The stored set, or None when there is none. Raises if it is unusable."""
        try:
            info = self.path.stat()
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise DefaultsError(
                f"{self.path.name} cannot be read: {exc.strerror or exc}") from None
        mode = stat.S_IMODE(info.st_mode)
        if mode & ~FILE_MODE:
            raise DefaultsError(
                f"refusing to read your saved defaults: the file is mode "
                f"{mode:04o} and must be no wider than {FILE_MODE:04o}, because "
                f"it decides where your runs go. Saving your settings again "
                f"replaces it.")
        if info.st_size > MAX_BYTES:
            raise DefaultsError(
                f"your saved defaults are {info.st_size} bytes and the limit is "
                f"{MAX_BYTES}, so they were not written by this tool.")
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            raise DefaultsError("your saved defaults are not readable as JSON."
                                ) from None
        if not isinstance(payload, dict) or payload.get("version") != SCHEMA_VERSION:
            raise DefaultsError(
                f"your saved defaults are not schema version {SCHEMA_VERSION}.")
        rows = payload.get("defaults")
        if not isinstance(rows, dict):
            raise DefaultsError("your saved defaults carry no `defaults` object.")
        return rows

    def write(self, clean: dict) -> None:
        """Replace the file with `clean`. Never wider than `0600`, and atomic.

        The four steps of `credentials.Credentials._write`, in its order and
        for its reasons.
        """
        payload = json.dumps({"version": SCHEMA_VERSION, "defaults": clean},
                             indent=2, sort_keys=True) + "\n"
        if len(payload.encode("utf-8")) > MAX_BYTES:
            raise Refused("", f"these defaults would be more than {MAX_BYTES} "
                              f"bytes on disk.")
        parent = self.path.parent
        with _LOCK:
            parent.mkdir(parents=True, exist_ok=True)
            os.chmod(parent, DIR_MODE)
            temporary = parent / (f".{self.path.name}.{os.getpid()}."
                                  f"{threading.get_ident()}.tmp")
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

    def remove(self) -> bool:
        """Forget the saved set. True if there was one."""
        with _LOCK:
            try:
                self.path.unlink()
            except FileNotFoundError:
                return False
        return True
