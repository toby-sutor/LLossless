"""Record and replay model responses, so the pipeline is testable without a model.

The reason this exists: the decompose and verify passes are the whole value of
this tool, and neither can be developed if every iteration needs a GPU, an API
key, and thirty seconds of patience. With cassettes, one recording session
against one model produces test data that anyone can clone and run offline, and
that stays fixed while the parsing and alignment logic underneath it changes.

Two design choices worth their justification:

*The recorded body is raw.* It is stored exactly as the endpoint returned it,
before any of PART C touches it. That is the whole point — a cassette recorded
today must still exercise the parser after the parser is rewritten, and a
cassette of already-parsed output would only ever test itself.

*The key covers everything that could change the answer* — role, model, tier,
prompt file hash, rendered messages, schema, temperature, seed, max_tokens.
Edit a prompt and the key changes, so the old recording is not silently served
against the new prompt. A cache that answers a question you did not ask is
worse than no cache.

*And `sample`, which changes nothing about the request.* It is the one key
component that is not a property of the question asked. Temperature 0 and a
fixed seed are supposed to make a model deterministic and do not: the same
request to the same local model returns different text run to run. So the same
request is asked several times, `sample` distinguishes the recordings, and the
measurement reports the modal answer and flags what varied. Without it the
second identical call would be served the first one's cassette and the run would
look perfectly stable by construction.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

# For one constant: the name of the request profile whose body is what every
# recording on disk was made with. `structured` imports nothing from this
# package, so this is a leaf dependency and not a cycle.
from . import structured

# One way only: `config` imports nothing from this package, so a cassette can
# ask it how an endpoint is identified without the two modules pointing at
# each other.
from . import config

SCHEMA_VERSION = 2
_UNSAFE = re.compile(r"[^a-z0-9_-]")

# What a cassette with no `meta.field_order` is read as: the strictest order,
# so that under `config.replay_field_order` the replaying run's own setting
# decides, which is exactly what every replay did before the field existed.
# Not a claim that the recording was strict. Unstamped recordings made under
# `--field-order any` exist (the deepseek-r1 arms), and they keep replaying
# the way they always have: with the flag.
UNSTAMPED_FIELD_ORDER = config.FIELD_ORDERS[0]


class MissingCassette(RuntimeError):
    """Replay was asked for a call that was never recorded.

    A hard error on purpose. Falling through to a live call would make an
    "offline" run silently reach the network, and would make a replayed result
    depend on whether the machine happened to have an endpoint configured.
    """

    def __init__(self, key: str, role: str, directory: Path) -> None:
        super().__init__(
            f"no recorded response for role {role!r}, key {key}\n"
            f"  looked in: {directory}\n"
            f"  expected:  {filename(role, key)}\n"
            f"  Record it with --record {directory}, or check whether a prompt "
            f"file changed since the cassettes were made."
        )
        self.key = key
        self.role = role
        # Where it looked, so a consumer can ask whether that corpus is stale
        # by ruling (`tests/stale_corpus.py`) rather than broken.
        self.directory = directory


class MixedSources(RuntimeError):
    """A recording sweep would deepen a corpus that another revision produced.

    Refused rather than warned about, because the damage is invisible after the
    fact: the cassettes are individually valid and the directory is
    indistinguishable from one revision's work unless someone reads the meta of
    every file. The report header has one line for the commit, and it would be
    a lie.

    Pass --mixed-sources to proceed anyway. That is the honest option when the
    edit provably cannot reach the model — a rename, a docstring — and it is
    stated as a decision rather than taken by default.
    """

    def __init__(self, directory: Path, current: str, found: dict[str, int]) -> None:
        mixture = ", ".join(f"{source} ({n})" for source, n in sorted(found.items()))
        super().__init__(
            f"{directory} holds cassettes recorded by another revision\n"
            f"  recording as: {current}\n"
            f"  already here: {mixture}\n"
            f"  Re-record the directory from empty, commit the working tree, or "
            f"pass --mixed-sources to accept a corpus with two provenances."
        )


class ConflictingCassettes(RuntimeError):
    """One key resolves to two different recordings in the directory being read.

    The key is meant to cover everything that could change the answer, so two
    files carrying the same key are two answers to one question. Which of them
    a run gets is decided by `sorted()` over filenames — an ordering that is not
    a fact about either recording, and that nothing downstream reports.

    Refused rather than resolved by precedence, and the choice is the same one
    `MixedSources` makes one rung out. A precedence rule would keep working: it
    would pick a file, the run would finish, every figure would be reproducible,
    and the second recording would be invisible for as long as nobody looked.
    Replay determinism is this project's central claim, so the failure mode that
    matters is not "the wrong answer" but "an answer nobody knew was a choice".

    Neither recording is wrong. Both are true records of what the model said on
    their day, and the non-determinism between them is measured; an earlier study puts
    it at 14 of 240 multi-sample units. The fix is in resolution, not in the
    data: put the two recordings in two directories, because a directory is a
    corpus and a corpus is one measurement.

    Scope, stated because a guard's limits are what its user needs. This fires
    on the files one `Store` indexes, which is one directory, non-recursively.
    Two *corpora* holding different bodies under one key is not this error and
    must not be: `tests/responses/`, `tests/responses/m4/` and
    `tests/responses/m7/` are three separate recording sessions and three
    separate Stores, and no single run reads more than one of them — `_fetch`
    returns from the replay store before the cache is consulted. That the first
    of those three is also the *parent* of the other two is the reason a file
    can move between them by copy and land somewhere it collides; the
    cross-corpus inventory is pinned in `tests/test_client.py` instead, where a
    fourth such key trips a check rather than a run.
    """

    def __init__(self, directory: Path, key: str, paths: list[Path], differ: str) -> None:
        listing = "\n".join(f"    {path.name}" for path in paths)
        super().__init__(
            f"{directory} holds {len(paths)} recordings under one key, and their "
            f"{differ} differ\n"
            f"  key: {key}\n"
            f"{listing}\n"
            f"  Which one a run gets is filename sort order. Move all but one out "
            f"of this directory:\n"
            f"  a corpus is one measurement, and two answers to one question are "
            f"two corpora. Do not\n"
            f"  delete either recording — both are records of what the model said."
        )
        self.key = key
        self.paths = list(paths)


def guard_sources(store: Store, current: str | None) -> None:
    """Refuse to record into a directory another revision wrote.

    A dirty tree counts as its own revision and so trips this on the second
    sweep, which is the intended pressure: commit, then measure.

    `current` of None waives this entirely — that is exactly what
    --mixed-sources buys, and nothing more.

    No endpoint check here any more. A corpus keyed on content
    (`key_for` — role, model, tier, prompt, messages, schema, temperature,
    seed, max_tokens, thinking, sample) answers "what did this model say to
    this prompt", and that question has one answer regardless of which box
    asked it. Refusing a second machine's answer protected a claim this
    project no longer makes — "a corpus is a measurement of one deployment" —
    and cost real recordings for it: a local card that cannot hold the model
    and a rented pod that changes address on every restart are the two
    endpoints this tool actually has, and the guard blocked moving between
    them. `endpoint_id` is still recorded on every cassette (`Cassette.endpoint_id`)
    and still tallied by `Store.endpoints()`, so a human can ask which machines
    answered; nothing here reads that tally to refuse a write. What still
    matters and is not yet a guard: the model plus its quantization, which
    changes the answer and is in neither this key nor any check today. Adding
    it is a schema bump against the committed corpus and is deliberately not
    done here.
    """
    if current is None:
        return
    found = {source: n for source, n in store.sources().items() if source != current}
    if found:
        raise MixedSources(store.directory, current, found)


DIR_MODE = 0o700
FILE_MODE = 0o600


def secure_dir(path: Path) -> Path:
    """Make `path` and any missing ancestor, owner-only, and tighten an existing one.

    These files are the rendered prompt and the raw response -- the documents
    and the merge. `.gitignore` withholds `/assets/` because it "carries the
    source documents' content"; this is a second copy of that content and was
    held to a weaker rule: `mkdir` with no mode let the umask decide, which on
    the development machine meant 0755 directories and 0644 files.

    Three things this does that a bare `mkdir(mode=...)` does not:

    * **It tightens a directory that already exists.** `mkdir`'s mode argument
      is ignored when the directory is there, so a cache created before this
      change would have kept 0755 for ever -- and every existing cache is
      exactly the case this was written for.
    * **It tightens the ancestors it creates.** `parents=True` makes
      intermediates at the default mode, so `~/.cache/llossless/responses`
      left `~/.cache/llossless` world-readable while its child was not, and
      the dumps and the capability record live in that parent.
    * **It only ever narrows.** An owner who has deliberately widened something
      above the cache is not overruled: nothing outside the tree being created
      is touched, and a mode already at or below `DIR_MODE` is left alone.
    """
    missing = []
    probe = path
    while not probe.exists() and probe != probe.parent:
        missing.append(probe)
        probe = probe.parent
    path.mkdir(parents=True, exist_ok=True)
    for made in missing + [path]:
        try:
            current = made.stat().st_mode & 0o777
            if current & ~DIR_MODE:
                made.chmod(current & DIR_MODE)
        except OSError:
            pass          # a read-only or foreign-owned tree is not ours to fix
    return path


def secure_write(path: Path, text: str) -> Path:
    """Write owner-only. The mode is set before the bytes, never after.

    `chmod` after `write_text` leaves a window in which the file exists at the
    umask's mode with the documents already in it. Small window, avoidable
    window.
    """
    handle = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, FILE_MODE)
    with os.fdopen(handle, "w", encoding="utf-8") as out:
        out.write(text)
    try:
        path.chmod(FILE_MODE)      # an existing file keeps its old mode otherwise
    except OSError:
        pass
    return path


def canonical(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def key_for(
    *,
    role: str,
    model: str,
    tier: str,
    prompt_sha256: str,
    messages: list[dict],
    schema: dict | None,
    temperature: float,
    seed: int | None,
    max_tokens: int | None,
    thinking: bool = False,
    sample: int = 0,
    profile: str = structured.DEFAULT_PROFILE,
    command: str = "",
) -> str:
    """The cassette key: sha256 over everything that determines the response.

    `thinking` is not in the addendum's list of key components, and is here
    anyway: a reasoning block changes the answer as surely as temperature does,
    and the merge pass is going to be run both ways specifically to compare
    them. Two runs that differ only in whether the model was allowed to think
    must not share a recording.

    `sample` is here for the opposite reason. It determines nothing — it is the
    repeat index of an identical request, and it is in the key precisely so that
    identical requests do not collide. See the module docstring.

    `profile` is the one component that is **omitted from the hash at its
    default**, and that is a deliberate exception to how every other one works.
    The reason it has to be in the key at all: a profile decides which of
    `temperature`, `seed` and the budget field reach the endpoint, so two runs
    with the same temperature in this signature and different profiles did not
    send the same bytes, and must not read each other's recordings. The reason
    it is omitted at the default: the default profile *is*, by construction,
    the body every one of the 697 recordings on disk was made with, so
    including it would rename all of them to say something that was already
    true of them. A component that is absent when it carries no information is
    not a hole in the key — it is the difference between adding an axis and
    re-keying a corpus, and `test_cassette_key_derivation_is_pinned` holds both
    halves: the fourteen golden digests are unchanged, and a non-default
    profile moves the key.

    `command` is in the key on exactly the terms `profile` is, and absent at
    its default for the same reason: every recording on disk was made over
    HTTP, and a component that carries no information is not a hole. It has to
    be here because a subprocess and an endpoint answering the same request
    are two different things that would otherwise share a recording -- and
    because the profile alone does not separate them. Nothing stops a command
    backend running under `openai-compatible`, and nothing should: an
    operator's wrapper may genuinely constrain output, and a keyspace that
    depends on their choosing the right profile is a keyspace that collides
    the first time they do not.

    Hashed, never carried whole. A command is a local path as often as not,
    and cassettes are committed test data in a public repository -- the same
    argument `endpoint_id` makes about an address, reaching the same answer.
    """
    components = {
        "role": role,
        "model": model,
        "tier": tier,
        "prompt_sha256": prompt_sha256,
        "messages": messages,
        "schema": schema,
        "temperature": temperature,
        "seed": seed,
        "max_tokens": max_tokens,
        "thinking": thinking,
        "sample": sample,
    }
    if profile != structured.DEFAULT_PROFILE:
        components["profile"] = profile
    if command:
        components["backend"] = hashlib.sha256(
            command.encode("utf-8")).hexdigest()[:16]
    return hashlib.sha256(canonical(components)).hexdigest()


def filename(role: str, key: str) -> str:
    return f"{_UNSAFE.sub('-', role.lower())}-{key[:16]}.json"


@dataclass(frozen=True)
class Cassette:
    key: str
    role: str
    raw: str
    http_status: int
    tier: str
    latency_ms: int
    # The code that produced this recording, as provenance.source_state names
    # it. Empty for cassettes written before the field existed; the Store
    # treats that as one more distinct provenance rather than as a wildcard.
    source: str = ""
    # The machine that answered, as an opaque id — see config.endpoint_id. Not
    # an address: a cassette is committed test data in a public repository, and
    # every question anyone asks of this field is an equality test.
    # Same wildcard rule as `source`: empty is its own value, not "any endpoint".
    endpoint_id: str = ""
    # Which rule made that id -- `config.ENDPOINT_ID_SCHEME`. An id is a digest
    # and says nothing about how it was derived, so two schemes' ids sit side by
    # side in one tally looking like two machines. This is stamped when written,
    # and absent means scheme 1, because the scheme that had no marker is the
    # only one a file without a marker can have been written under. This is the
    # field the next such change migrates *from*: 818 cassettes were left
    # unmigratable by this one, and the reason is that nothing on disk said
    # which rule they were made under.
    endpoint_id_scheme: int = config.ENDPOINT_ID_SCHEME_HOSTNAME
    # The field order the recording run read this answer under -- the setting
    # of the run that wrote it, `--field-order`. Not in the key: it does not
    # change what was asked, only how the answer was read, and a replay needs
    # it to read the answer the same way (`config.replay_field_order`).
    # Absent means `UNSTAMPED_FIELD_ORDER`, which defers to the replaying run.
    field_order: str = UNSTAMPED_FIELD_ORDER

    @classmethod
    def from_file(cls, path: Path) -> Cassette:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(
                f"{path.name}: schema_version {data.get('schema_version')!r}, "
                f"this build reads {SCHEMA_VERSION}"
            )
        meta = data.get("meta", {})
        field_order = meta.get("field_order", UNSTAMPED_FIELD_ORDER)
        if field_order not in config.FIELD_ORDERS:
            # Refused rather than defaulted: a value this build does not know
            # is a recording made under a rule it cannot apply.
            raise ValueError(
                f"{path.name}: meta.field_order {field_order!r} is not one of "
                f"{', '.join(config.FIELD_ORDERS)}"
            )
        # `endpoint_host` is what cassettes carried before the field was
        # de-identified. Hashing it on read rather than bumping the schema keeps
        # a local cache written by an older build usable — it
        # resolves to the same id the migration wrote into the corpus, so the
        # guard cannot fire on the difference between the two spellings.
        endpoint = meta.get("endpoint_id")
        if endpoint is None:
            # A hostname is a scheme 1 id and can be nothing else, so it is
            # hashed under scheme 1 rather than through `config.endpoint_id`,
            # which now wants a URL and would return "" for a bare host.
            endpoint = config.legacy_endpoint_id(meta.get("endpoint_host", ""))
        return cls(
            key=data["key"],
            role=data["request"].get("role", ""),
            raw=data["response"]["raw"],
            http_status=data["response"].get("http_status", 200),
            tier=data["request"].get("tier", ""),
            latency_ms=meta.get("latency_ms", 0),
            source=meta.get("llossless_source") or meta.get("claimcheck_source", ""),
            endpoint_id=endpoint,
            endpoint_id_scheme=meta.get("endpoint_id_scheme",
                                        config.ENDPOINT_ID_SCHEME_HOSTNAME),
            field_order=field_order,
        )


class Store:
    """A directory of cassettes, indexed by key on first use.

    Serves both jobs the addendum asks for: the committed test corpus under
    tests/responses/, and the on-disk response cache under .llossless-cache/.
    They are the same thing with different lifetimes, and one implementation
    means the cache cannot drift from the format the tests read.
    """

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self._index: dict[str, Path] | None = None

    def _load_index(self) -> dict[str, Path]:
        if self._index is None:
            index: dict[str, Path] = {}
            if self.directory.is_dir():
                for path in sorted(self.directory.glob("*.json")):
                    try:
                        key = Cassette.from_file(path).key
                    except (ValueError, KeyError, json.JSONDecodeError):
                        continue  # not a cassette, or written by another version
                    if key in index:
                        # `index[key] = path` used to stand here alone, and the
                        # second file won by sort order without saying so. The
                        # keys are content-addressed but the filenames are not
                        # the index: a cassette copied under any other name is
                        # indexed by the key inside it and lands on top.
                        self._refuse_conflict(key, index[key], path)
                    index[key] = path
            self._index = index
        return self._index

    @staticmethod
    def _resolution(path: Path) -> tuple[str, str, str]:
        """What a run would actually get from this file: the request, the answer, and how it is read.

        Compared as canonical JSON rather than as file bytes, so the fields a
        cassette carries *about* a recording — when it was made, how long it
        took, which revision was checked out — do not count as a disagreement.
        Two recordings of one request that returned the same body are one
        answer stored twice, and that is a tidiness problem, not this one.

        `meta.field_order` is the one meta field that does count, because a
        replay reads the answer under it (`config.replay_field_order`): one
        body stamped `any` and `schema` is two outcomes, picked by sort order.
        Absent and `UNSTAMPED_FIELD_ORDER` are one value, as they are on read.
        """
        data = json.loads(path.read_text(encoding="utf-8"))
        return (
            canonical(data.get("request", {})).decode("utf-8"),
            canonical(data.get("response", {})).decode("utf-8"),
            (data.get("meta") or {}).get("field_order", UNSTAMPED_FIELD_ORDER),
        )

    def _refuse_conflict(self, key: str, first: Path, second: Path) -> None:
        request_a, response_a, order_a = self._resolution(first)
        request_b, response_b, order_b = self._resolution(second)
        if request_a != request_b:
            # Worse than two answers: two *questions* filed under one key. The
            # key is a digest of the request, so this is either a derivation
            # bug or a collision, and neither may be resolved by picking one.
            raise ConflictingCassettes(self.directory, key, [first, second], "requests")
        if response_a != response_b:
            raise ConflictingCassettes(self.directory, key, [first, second], "responses")
        if order_a != order_b:
            raise ConflictingCassettes(self.directory, key, [first, second], "field orders")

    def conflicts(self) -> dict[str, list[Path]]:
        """Keys in this directory that resolve to more than one recording.

        Empty whenever `_load_index` succeeds, by construction — indexing
        raises on the first conflict it meets. It exists so a caller that wants
        the whole census rather than the first offender can take it without
        catching an exception per file, which is what the corpus inventory in
        the test suite does across sibling directories.
        """
        found: dict[str, list[Path]] = {}
        by_key: dict[str, list[Path]] = {}
        if self.directory.is_dir():
            for path in sorted(self.directory.glob("*.json")):
                try:
                    by_key.setdefault(Cassette.from_file(path).key, []).append(path)
                except (ValueError, KeyError, json.JSONDecodeError):
                    continue
        for key, paths in by_key.items():
            if len({self._resolution(path) for path in paths}) > 1:
                found[key] = paths
        return found

    def has(self, key: str) -> bool:
        return key in self._load_index()

    def _tally(self, attribute: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for path in self._load_index().values():
            try:
                value = getattr(Cassette.from_file(path), attribute)
            except (ValueError, KeyError, json.JSONDecodeError):
                continue
            counts[value or "unrecorded"] = counts.get(value or "unrecorded", 0) + 1
        return counts

    def sources(self) -> dict[str, int]:
        """Which revisions produced the cassettes already here, and how many each.

        A corpus is only a corpus if one revision made all of it. A sweep that
        resumes after an edit produces a directory whose recordings answer
        slightly different questions, and no report header can describe that
        honestly — it has one line for the commit. So the runners read this
        before recording and refuse a mixture rather than quietly deepening one.
        """
        return self._tally("source")

    def endpoints(self) -> dict[str, int]:
        """Which endpoints produced the cassettes already here, and how many each.

        The same question as `sources`, asked of the machine rather than the
        code, and it needs asking separately: `endpoint_id` is not part of
        `key_for`, so recordings from two boxes interleave without ever
        colliding and nothing downstream can tell them apart.

        The ids are opaque, which costs this method nothing: it counts equal
        values, and it never needed to know what they stood for.
        """
        return self._tally("endpoint_id")

    def get(self, key: str) -> Cassette | None:
        path = self._load_index().get(key)
        return Cassette.from_file(path) if path else None

    def require(self, key: str, role: str) -> Cassette:
        cassette = self.get(key)
        if cassette is None:
            raise MissingCassette(key, role, self.directory)
        return cassette

    def write(
        self,
        *,
        key: str,
        role: str,
        model: str,
        tier: str,
        messages: list[dict],
        schema: dict | None,
        temperature: float,
        raw: str,
        http_status: int,
        endpoint: str,
        latency_ms: int,
        attempt: int,
        source: str = "",
        force: bool = False,
        field_order: str | None = None,
    ) -> Path | None:
        """Write one cassette. Returns None when an existing one was kept.

        `field_order` is the order the writing run read the answer under, and
        `client` always passes it. `None` writes no field, which a reader takes
        as `UNSTAMPED_FIELD_ORDER` -- the reading every cassette written
        before the field existed gets -- rather than a value nobody stated.

        `endpoint` is an id from `config.endpoint_id` and nothing else. Not a
        URL, not a hostname, not a port, no headers, no key: a cassette is
        committed test data in a public repository, and the only thing about the
        endpoint anything downstream asks is whether two recordings came from
        the same machine. An opaque label answers that question exactly and
        publishes no address to answer it with.

        `meta.endpoint_id_scheme` says which rule made that id. It is a number,
        not a second identity: it is the same for every cassette this build
        writes, it distinguishes nothing within a corpus, and its whole job is
        to be there when the rule changes again. It was not there when the rule
        changed the first time, and 818 recorded ids are stuck under the old one
        as a result: they are readable, and they cannot be converted, because
        nothing beside them says what they were made from.
        """
        path = self.directory / filename(role, key)
        if path.exists() and not force:
            return None
        if field_order is not None and field_order not in config.FIELD_ORDERS:
            raise ValueError(f"field_order {field_order!r} is not one of "
                             f"{', '.join(config.FIELD_ORDERS)}")

        secure_dir(self.directory)
        secure_write(path,
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "key": key,
                    "request": {
                        "role": role,
                        "model": model,
                        "tier": tier,
                        "messages": messages,
                        "schema": schema,
                        "temperature": temperature,
                    },
                    "response": {"raw": raw, "http_status": http_status},
                    "meta": {
                        "endpoint_id": endpoint,
                        "endpoint_id_scheme": config.ENDPOINT_ID_SCHEME,
                        "claimcheck_source": source,
                        "latency_ms": latency_ms,
                        "attempt": attempt,
                        **({"field_order": field_order} if field_order is not None else {}),
                    },
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n")
        if self._index is not None:
            self._index[key] = path
        return path


class ChainedStore:
    """A primary `Store`, plus a read-only `local/` overlay checked on miss.

    This existed because `guard_sources` refused to deepen one
    directory with cassettes from two endpoints, so a corpus recorded against
    a hosted endpoint could only be *extended* by a cassette recorded honestly
    against a different one, never mixed into the same directory. That refusal
    is gone, but the overlay is still worth having: it keeps
    what was recorded against the local card physically separate from what was
    recorded against a rented pod, which is a fact a human may still want to
    read off the directory layout even though nothing enforces it any more.

    `primary` is authoritative. A key present in both resolves to `primary`'s
    answer, silently -- there is no scenario where a later local cassette is
    meant to shadow an existing hosted one, so this never needs to choose.
    """

    def __init__(self, primary: Store, overlay: Store | None) -> None:
        self.primary = primary
        self.overlay = overlay
        self.directory = primary.directory

    def has(self, key: str) -> bool:
        return self.primary.has(key) or (self.overlay is not None and self.overlay.has(key))

    def get(self, key: str) -> Cassette | None:
        found = self.primary.get(key)
        if found is not None:
            return found
        return self.overlay.get(key) if self.overlay is not None else None

    def require(self, key: str, role: str) -> Cassette:
        cassette = self.get(key)
        if cassette is None:
            raise MissingCassette(key, role, self.primary.directory)
        return cassette
