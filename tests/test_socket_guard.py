"""Offline checks for the socket guard. No network, no model.

The guard is the only thing in this repository that can fail a test for where a
socket went, so it is the one module whose own failure mode is a suite that
looks clean. Two halves here. The first exercises the predicate against real
sockets -- a loopback listener this process bound, and an address nobody
configured. The second is the part that makes the guard mean anything at all: a
scan asserting that every test module installs it, because a guard installed by
five modules out of seven is indistinguishable, from a passing run, from a guard
installed by all of them. Test modules are found by what they define rather than
by what they are called, so `audit_docs.py` is one of them.

The blocked address is `10.255.255.1:9`, the same one an earlier run reported reaching. It
is TEST-NET-2 discard: unroutable by RFC 5737 and dropped by RFC 863 if it were
not. Reusing it means the check names the breach it exists because of, and the
guard has to refuse before anything can find out whether the address answers.
"""

from __future__ import annotations

import re
import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402
from llossless import config  # noqa: E402
from fake_endpoint import FakeEndpoint, envelope  # noqa: E402

socket_guard.install()

BREACH = ("10.255.255.1", 9)

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def raises(function, *args) -> socket_guard.SocketGuardError | None:
    try:
        function(*args)
    except socket_guard.SocketGuardError as error:
        return error
    return None


def with_guard(settings: config.Settings):
    """Reinstall the guard against one endpoint, for one check.

    The module-level install is the real one and stays installed for everything
    else; these swap it for a known allow-list and put it back. `uninstall` is
    exposed for exactly this and is not used by any other test module.
    """
    socket_guard.uninstall()
    socket_guard.install(settings)


def restore() -> None:
    socket_guard.uninstall()
    socket_guard.install()


# --------------------------------------------------------------------------
# The predicate, against real sockets
# --------------------------------------------------------------------------


def test_a_non_configured_address_is_refused() -> None:
    """The breach reported earlier, refused before it reaches the network."""
    sock = socket.socket()
    sock.settimeout(0.1)
    error = raises(sock.connect, BREACH)
    check(error is not None, f"connect to {BREACH[0]}:{BREACH[1]} was permitted")
    if error is not None:
        check("10.255.255.1:9" in str(error),
              f"the refusal does not name the destination: {error}")
        check("configured" in str(error),
              f"the refusal does not say why it refused: {error}")
    check(raises(sock.connect_ex, BREACH) is not None,
          "connect_ex is not guarded; only connect is")
    sock.close()
    check(BREACH in socket_guard.blocked(),
          f"the guard refused {BREACH} and does not report having done so")


def test_a_loopback_port_this_process_bound_is_allowed() -> None:
    """The fake endpoint's whole shape: bind ephemeral, then connect to it.

    Bound before the connect and refused after it closes -- the entitlement is
    to the port this process actually holds, not to loopback in general.
    """
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    port = listener.getsockname()[1]

    client = socket.socket()
    client.settimeout(1)
    check(raises(client.connect, ("127.0.0.1", port)) is None,
          f"a loopback port this process bound was refused: 127.0.0.1:{port}")
    client.close()
    listener.close()

    other = socket.socket()
    other.settimeout(0.1)
    check(raises(other.connect, ("127.0.0.1", port + 1)) is not None,
          "a loopback port nobody bound was permitted; the guard allows loopback wholesale")
    other.close()


def test_the_fake_endpoint_still_works_under_the_guard() -> None:
    """The end the suite depends on. If this fails, everything else does too."""
    from llossless import transport  # noqa: PLC0415 - the module that opens sockets

    with FakeEndpoint(lambda _b, _n: (200, envelope('{"ok": true}'))) as base_url:
        host = base_url.split("//", 1)[1].split("/", 1)[0]
        response = transport.post_json(
            f"{base_url}/chat/completions", {"model": "m"},
            api_key=None, timeout=5, ca_bundle=None, host=host, model="m",
        )
    check(response.status == 200, f"the fake endpoint answered {response.status} under the guard")
    check(host.startswith("127.0.0.1:"), f"the fake endpoint moved off loopback: {host}")


def test_the_configured_endpoint_is_allowed_by_name_and_by_resolution() -> None:
    """A hosted endpoint is connected to by address, and named in the allow-list.

    `create_connection` resolves the name and then connects to the result, so a
    guard comparing hostnames would refuse the endpoint it is supposed to
    permit. The resolution is observed rather than performed -- getaddrinfo is
    wrapped, and only lookups of the configured name are recorded.
    """
    settings = config.Settings(base_url="http://localhost:11434/v1")
    with_guard(settings)
    try:
        check(socket_guard._guard.permits("localhost", 11434),
              "the configured host is refused by name")
        check(not socket_guard._guard.permits("localhost", 11435),
              "the guard ignores the port; any port on the configured host is allowed")
        socket.getaddrinfo("localhost", 11434, socket.AF_INET)
        check(socket_guard._guard.permits("127.0.0.1", 11434),
              "an address the configured host resolved to is refused")
        # Deliberately on the configured *port*. Resolving a non-configured
        # host and then asking about the port the endpoint uses is the only
        # question the port check does not answer on its own -- ask it on port
        # 9 and the answer is False whether or not the lookup was recorded.
        socket.getaddrinfo("127.0.0.2", 11434, socket.AF_INET)
        check(not socket_guard._guard.permits("127.0.0.2", 11434),
              "resolving any name entitles a connect to it; only the configured name should")
    finally:
        restore()


def test_installing_twice_does_not_wrap_twice() -> None:
    """Every test module installs, and test modules import each other."""
    before = socket.socket.connect
    socket_guard.install()
    check(socket.socket.connect is before,
          "a second install wrapped the wrapper")
    check(socket_guard.installed(), "the guard reports itself uninstalled while installed")


def test_uninstall_restores_the_real_socket_layer() -> None:
    """A guard that cannot be removed cannot be shown to have been doing anything."""
    socket_guard.uninstall()
    try:
        check(not socket_guard.installed(), "uninstall left the guard installed")
        sock = socket.socket()
        sock.settimeout(0.05)
        try:
            sock.connect(BREACH)
        except (OSError, socket_guard.SocketGuardError) as error:
            check(not isinstance(error, socket_guard.SocketGuardError),
                  "the guard still refuses connects after uninstall")
        sock.close()
    finally:
        restore()


def test_an_unjudged_address_shape_is_counted_rather_than_hidden() -> None:
    """REPORT THE DENOMINATOR, applied to the guard's own coverage."""
    before = socket_guard.unjudged()
    sock = socket.socket(socket.AF_UNIX)
    try:
        # The path does not exist, so the real connect fails -- which is the
        # point: the guard let it through to the OS instead of ruling on it.
        sock.connect("/nonexistent/llossless.sock")
    except socket_guard.SocketGuardError:
        check(False, "a unix-domain connect was judged as a network call")
    except OSError:
        pass
    sock.close()
    check(socket_guard.unjudged() == before + 1,
          f"an unjudged connect was not counted: {before} -> {socket_guard.unjudged()}")


# --------------------------------------------------------------------------
# The half that makes the guard mean anything: everyone installs it
# --------------------------------------------------------------------------


def test_every_test_module_installs_the_guard() -> None:
    """Discovered, not listed. A new test module is unguarded until this fails.

    Both lines are required and the import alone is not enough: importing the
    module patches nothing, and a module that imports the guard without calling
    `install()` reads, at a glance, exactly like one that does.
    """
    modules = [(path, path.read_text(encoding="utf-8"))
               for path in sorted((ROOT / "tests").glob("*.py"))]
    # By content, not by filename. `audit_docs.py` is a test module that does
    # not start with `test_`, and a rule keyed on the name would have excused
    # it -- discovery by what a file defines is the same rule test_fixtures.py
    # uses to find fixtures, and for the same reason.
    modules = [(path, text) for path, text in modules
               if re.search(r"^def test_", text, re.M)]
    check(len(modules) >= 7,
          f"only {len(modules)} test modules found; the discovery rule has drifted")
    for path, text in modules:
        name = path.relative_to(ROOT).as_posix()
        check("import socket_guard" in text, f"{name} does not import the socket guard")
        check(re.search(r"^socket_guard\.install\(\)$", text, re.M) is not None,
              f"{name} imports the socket guard and never installs it")


def test_the_shipped_package_never_installs_it() -> None:
    """A test-time guard in production would be a second copy of the rule."""
    for path in sorted((ROOT / "src" / "llossless").glob("*.py")):
        check("socket_guard" not in path.read_text(encoding="utf-8"),
              f"{path.relative_to(ROOT).as_posix()} references the test-time socket guard")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_socket_guard" and callable(function):
            function()
    if failures:
        print(f"socket guard: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"socket guard: {checks} checks pass, "
          f"{len(socket_guard.blocked())} destination(s) refused, "
          f"{socket_guard.unjudged()} unjudged")
    return 0


def test_socket_guard() -> None:
    """pytest entry point."""
    assert main() == 0, "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
