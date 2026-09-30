"""No test may open a socket the operator did not configure.

A past session self-reported a constraint breach: while gathering evidence for the timeout
split, one `post_json` call was made to `10.255.255.1:9`, a non-configured
address, to observe a real connect timeout. The call was harmless. The detection
was not: the only mechanism that caught it was the person who made it choosing
to write it down, in a repository whose first design principle is LOCAL-FIRST
and whose non-goals include "no telemetry, ever".

This module is that mechanism. `socket.socket.connect` and `connect_ex` raise
`SocketGuardError` unless the destination is one of two things:

* **the configured endpoint** -- `Settings.host` and `Settings.port`, either as
  written or as an address the configured host resolved to. Resolutions are
  observed rather than performed: `socket.getaddrinfo` is wrapped and records
  what came back, and only for the configured name. Nothing here looks anything
  up, so the guard itself makes no network call.
* **a loopback address this process bound.** `socket.socket.bind` is wrapped and
  records loopback binds, so `tests/fake_endpoint.py:276` binding `127.0.0.1` on
  an ephemeral port entitles the suite to connect to that port and to no other.
  The allow-list is a predicate over what the process did, not a constant.

Three limits, stated because a guard that is trusted past its scope is worse
than none.

**It is per-process.** A test that spawns a subprocess -- `test_client.py:2170`
does, to prove replay never imports `urllib.request` -- is not covered inside
that child. The two checks are complementary: this one watches where a socket
goes, that one watches whether the socket layer is reached at all.

**It judges AF_INET and AF_INET6 only.** A unix-domain connect cannot leave the
machine, and passing those through avoids failing the suite for something that
is not a network call. Anything with an address shape this module does not
recognise is allowed and counted, and `unjudged()` reports the count, so
"nothing was blocked" can be told apart from "nothing was examined".

**It is test-time.** It is never installed by `src/llossless/`. Patching
`socket` in the shipped tool to enforce a policy the production code is already
responsible for would be a second implementation of the same rule, and the one
that fired would be the wrong one to debug.
"""

from __future__ import annotations

import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from llossless import config  # noqa: E402

# Wildcard binds. A server bound to one of these is reachable on loopback, and
# the connect that follows names the loopback address rather than the wildcard.
WILDCARD = {"0.0.0.0", "::", ""}
LOOPBACK = {"127.0.0.1", "::1"}


class SocketGuardError(AssertionError):
    """A socket was pointed at an address the operator did not configure.

    An `AssertionError` rather than a `RuntimeError`: this is a test failing,
    not an operation going wrong, and the harnesses that catch broad exceptions
    around a call should not be able to swallow it into an errored unit.
    """


# Facts about this process, not about the current installation. A test that
# swaps the allow-list must not be able to erase what the guard already saw --
# the record of a refusal is evidence, and evidence that a reinstall clears is
# a counter that reads zero for two different reasons.
_bound: set[tuple[str, int]] = set()
_blocked: list[tuple[str, int]] = []
_unjudged = 0


class _Guard:
    """The installed state. One per process, or none."""

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.resolved: set[str] = set()
        self.originals: dict[str, object] = {}

    # -- the predicate -----------------------------------------------------

    def target(self, family, address) -> tuple[str, int] | None:
        """The `(host, port)` this connect is for, or None if it is not judged."""
        if family not in (socket.AF_INET, socket.AF_INET6):
            return None
        if not isinstance(address, tuple) or len(address) < 2:
            return None
        host, port = address[0], address[1]
        if not isinstance(host, str) or not isinstance(port, int):
            return None
        return host, port

    def permits(self, host: str, port: int) -> bool:
        if (host, port) in _bound:
            return True
        if port != self.port:
            return False
        return host == self.host or host in self.resolved


_guard: _Guard | None = None


def install(settings: config.Settings | None = None) -> None:
    """Patch the socket layer for this process. Idempotent.

    The allow-list is read from the environment the tests actually run under,
    so a suite run against a non-default `LLOSSLESS_BASE_URL` guards that
    endpoint rather than the default one. Idempotent because every test module
    installs it and modules import each other: `test_client.py` imports
    `run_decompose`, and wrapping a wrapper would make the second call's error
    message name the first wrapper's frame.
    """
    global _guard
    if _guard is not None:
        return
    resolved = settings or config.from_env()
    guard = _Guard(resolved.host, resolved.port)

    real_connect = socket.socket.connect
    real_connect_ex = socket.socket.connect_ex
    real_bind = socket.socket.bind
    real_getaddrinfo = socket.getaddrinfo

    def judge(sock, address, what: str) -> None:
        global _unjudged
        target = guard.target(sock.family, address)
        if target is None:
            _unjudged += 1
            return
        if guard.permits(*target):
            return
        _blocked.append(target)
        raise SocketGuardError(
            f"{what} to {target[0]}:{target[1]}, which is neither the configured "
            f"endpoint {guard.host}:{guard.port} nor a loopback port this process "
            f"bound. The brief permits no network call other than to the "
            f"configured LLM endpoint."
        )

    def connect(sock, address):
        judge(sock, address, "connect")
        return real_connect(sock, address)

    def connect_ex(sock, address):
        judge(sock, address, "connect_ex")
        return real_connect_ex(sock, address)

    def bind(sock, address):
        result = real_bind(sock, address)
        target = guard.target(sock.family, sock.getsockname())
        if target is not None:
            host, port = target
            if host in LOOPBACK:
                _bound.add((host, port))
            elif host in WILDCARD:
                _bound.update((loopback, port) for loopback in LOOPBACK)
        return result

    def getaddrinfo(host, port, *args, **kwargs):
        infos = real_getaddrinfo(host, port, *args, **kwargs)
        # Only the configured name. Recording every lookup would let a mistake
        # resolve an address and then be permitted to connect to it, which is
        # the whole failure this guard exists for.
        if host == guard.host:
            for info in infos:
                address = info[4]
                if isinstance(address, tuple) and address:
                    guard.resolved.add(address[0])
        return infos

    guard.originals = {
        "connect": real_connect,
        "connect_ex": real_connect_ex,
        "bind": real_bind,
        "getaddrinfo": real_getaddrinfo,
    }
    socket.socket.connect = connect
    socket.socket.connect_ex = connect_ex
    socket.socket.bind = bind
    socket.getaddrinfo = getaddrinfo
    _guard = guard


def uninstall() -> None:
    """Put the socket layer back. For the guard's own tests, not for tests."""
    global _guard
    if _guard is None:
        return
    socket.socket.connect = _guard.originals["connect"]
    socket.socket.connect_ex = _guard.originals["connect_ex"]
    socket.socket.bind = _guard.originals["bind"]
    socket.getaddrinfo = _guard.originals["getaddrinfo"]
    _guard = None


def installed() -> bool:
    return _guard is not None


def blocked() -> list[tuple[str, int]]:
    """Every destination refused in this process. A guard reports what it did."""
    return list(_blocked)


def unjudged() -> int:
    """Connects allowed because their address shape is not judged.

    REPORT THE DENOMINATOR: a guard that examined nothing raises nothing, and
    from the outside that is the same silence as a guard that examined every
    call and approved them all.
    """
    return _unjudged
