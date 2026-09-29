"""Ask an endpoint what it serves, so nobody has to guess a model name again.

The failure this exists for is small, common and expensive. An operator's local
ollama holds `qwen3:8b`; the catalogue calls the same family `qwen3-8b`; the
picker sent the catalogue's spelling, the endpoint had never heard of it, and
the run died two steps in -- after the documents had been uploaded, after a
worker had started, with a message naming a model the operator had not typed.
Every part of that is avoidable by asking the endpoint, once, at the moment it
is configured, instead of deriving a name and hoping.

**Two shapes, tried in order, because there are two conventions and no way to
tell them apart from the address.** `GET <base>/models` is the OpenAI-compatible
listing that vLLM and the hosted vendors answer; `GET <root>/api/tags` is
ollama's own, one path segment above the `/v1` the same server also serves. An
endpoint that answers neither is not an error -- see below -- so both are tried
and the first that parses wins.

**A probe that fails is not a failure.** An endpoint can be perfectly usable and
refuse to list: Anthropic's listing wants its own header shape rather than a
bearer token, a proxy may expose only the completion route, a self-hosted box
may have listings switched off. So this returns what it found and a sentence
about what happened, never an exception the caller has to decide how to
tolerate, and the settings route stores the endpoint either way. The operator
gets "could not list models here", the free-text field, and the catalogue rows,
which is exactly where they were before the probe existed.

**It is bounded, because the page is waiting on it.** One short timeout, no
backoff between attempts, and a cap on how many names are taken. A discovery
convenience that can hang a settings form for the length of three default
timeouts is a worse product than no discovery at all.

**Nothing discovered here is a measurement.** A probed model gets
`"measured": null` in the picker, which is the catalogue's own word for a model
nobody has run through this tool: no cost, no seconds, no silent-loss figure,
nothing interpolated from a similarly-named row that was measured. That path
had never been exercised by anything before this -- every row in the shipped
catalogue carries figures -- so this is also the first caller that proves the
unmeasured case renders at all.
"""

from __future__ import annotations

import ipaddress
import json
from urllib.parse import urlsplit, urlunsplit

from .. import transport

# One attempt's ceiling. Short, because the settings form is blocked on this
# and an endpoint that cannot answer a listing in three seconds is one the
# operator is better off being told about than waited on.
PROBE_TIMEOUT = 3.0

# How many names are taken from an answer. A listing endpoint in front of a
# model garden can answer with hundreds, and a picker with hundreds of rows in
# it is not a picker. The cap is reported rather than applied silently.
MAX_MODELS = 60

# Past this a "model name" is something else -- a description, an error, a page
# of HTML that happened to parse. Names are rendered through `textContent` so
# there is nothing to escape; this is about the row staying readable.
MAX_NAME = 120


# The three answers `kind_of` gives, and the three words the page reads them
# back as. Spelled here rather than in `app.js` because the page holds no
# vocabulary of its own -- the rule `verify_depths` and `commands.described`
# already follow -- and because the question "is this address on this network"
# is one the server can answer and a browser cannot.
KIND_SELFHOSTED = "selfhosted"
KIND_METERED = "metered"
KIND_UNKNOWN = "unknown"


def kind_of(base_url) -> str:
    """Is this address on this network, out on the internet, or unstated?

    **The third answer is the one this exists for.** The submit button names
    the route the click is about to take, and until now a run that could not be
    classified was labelled `metered API` -- a sentence about where the money
    goes, asserted from an absence. The operator's rule is that naming *every*
    case is what makes the naming trustworthy: a label that appears for two
    routes out of three teaches a reader that its absence means nothing in
    particular. So an address that is not there, or that does not parse, or
    whose host this cannot place, is `unknown` and says so on the button.

    Loopback, private and link-local addresses are the machine's own network
    and bill nothing per token -- a GPU there is paid for by the minute, which
    is the distinction `costCell` already draws for the self-hosted rows. So is
    `localhost` and the `.local`/`.localhost` names, which are reserved for
    exactly this by RFC 6761 and cannot resolve anywhere else.

    Everything else is treated as metered. That direction is chosen rather than
    left to `unknown` on purpose: the expensive mistake is believing a metered
    API is free, so an address this cannot place as local reads as the one that
    costs money per token.
    """
    if not isinstance(base_url, str) or not base_url.strip():
        return KIND_UNKNOWN
    try:
        host = (urlsplit(base_url.strip()).hostname or "").strip().lower()
    except ValueError:
        # A URL `urlsplit` refuses -- a bracketed host that is not an address,
        # most often. Unclassifiable is the honest answer and the button says
        # so; it is not this function's job to decide whether the run will
        # start.
        return KIND_UNKNOWN
    if not host:
        return KIND_UNKNOWN
    if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
        return KIND_SELFHOSTED
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        # A name rather than a literal. Resolving it would be a DNS call from
        # a settings render, which is a network round trip this page does not
        # make and a way to probe internal names besides.
        return KIND_METERED
    if address.is_loopback or address.is_private or address.is_link_local:
        return KIND_SELFHOSTED
    return KIND_METERED


def _root(base_url: str) -> str:
    """The server root, from an OpenAI-compatible base URL.

    The same rebuild `window._root` does and for the same reason: ollama's own
    routes sit beside `/v1` rather than under it, and a deployment behind a
    path prefix has to keep the prefix and lose only the `/v1`. Rebuilt through
    `urlsplit` rather than by trimming the string, so a prefix that happens to
    end in the same three characters is not eaten.
    """
    parts = urlsplit(base_url)
    path = parts.path.rstrip("/")
    if path.endswith("/v1"):
        path = path[: -len("/v1")]
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def _names(payload, field: str, key: str) -> list[str]:
    """Model names out of one listing shape, or `[]` if this is not that shape.

    `[]` and never a raise: this is asked twice per probe, once per convention,
    and "the answer parsed as JSON but is not this listing" is the ordinary
    result of asking an ollama server for an OpenAI listing. A raise here would
    make the second attempt depend on catching the first one's exception, which
    is the same control flow with a worse name.
    """
    if not isinstance(payload, dict):
        return []
    rows = payload.get(field)
    if not isinstance(rows, list):
        return []
    found: list[str] = []
    for row in rows:
        name = row.get(key) if isinstance(row, dict) else None
        if isinstance(name, str) and name.strip() and len(name) <= MAX_NAME:
            found.append(name.strip())
    return found


def _get(url: str, *, api_key, ca_bundle, host: str) -> list | None:
    """One GET, parsed, or None if this route did not answer with JSON.

    `sleep` is replaced rather than left at `time.sleep`: `transport.get_json`
    retries three times with a one-, two- and four-second backoff, which is the
    right discipline for a model call in a forty-minute run and the wrong one
    for a form field. The attempts are kept -- a listing that fails on a cold
    connection and works on the second is worth the two extra packets -- and
    the waiting between them is not.

    Every transport failure lands here as None. The caller turns that into a
    sentence; nothing about a probe is worth raising, because nothing about it
    decides whether the endpoint can be used.
    """
    try:
        response = transport.get_json(
            url, api_key=api_key, timeout=PROBE_TIMEOUT, ca_bundle=ca_bundle,
            host=host, sleep=lambda _seconds: None)
    except Exception:  # noqa: BLE001 - every failure is the same answer here
        return None
    try:
        return json.loads(response.body)
    except ValueError:
        return None


def models(base_url: str, *, api_key: str | None = None,
           ca_bundle: str | None = None) -> tuple[list[str], str]:
    """What this endpoint says it serves, and a sentence about how that went.

    Returns `(names, note)`. `names` is empty when nothing could be listed, and
    `note` always says which of the three things happened -- listed, listed
    nothing, or could not list -- because "no models" and "no answer" are
    different facts about an endpoint and a picker that showed the same empty
    row for both would send the operator looking in the wrong place.

    Duplicates are dropped and order is preserved: two listings can name the
    same model (an ollama server answers both shapes), and the order an
    endpoint reports in is the order its own operator sees elsewhere.
    """
    host = urlsplit(base_url).hostname or base_url
    attempts = (
        (f"{base_url.rstrip('/')}/models", "data", "id"),
        (f"{_root(base_url)}/api/tags", "models", "name"),
    )
    for url, field, key in attempts:
        payload = _get(url, api_key=api_key, ca_bundle=ca_bundle, host=host)
        found = _names(payload, field, key)
        if not found:
            continue
        unique: list[str] = []
        for name in found:
            if name not in unique:
                unique.append(name)
        if len(unique) > MAX_MODELS:
            return (unique[:MAX_MODELS],
                    f"listed {len(unique)} models and kept the first "
                    f"{MAX_MODELS}")
        return unique, f"listed {len(unique)} model(s)"
    return [], ("could not list models here: this endpoint answered neither "
                "the OpenAI-compatible listing nor ollama's. It can still be "
                "used -- type the model name in the custom field")
