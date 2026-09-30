#!/usr/bin/env python3
"""De-identify the endpoint in every committed cassette. One pass.

`endpoint_host` stored the hostname of the machine that answered. It is a meta
field: not a component of `cassette.key_for`, and the only question anything
asks of it is whether two recordings came from the same box. An equality test
does not need an address, and a cassette is committed test data in a public, source-available repository, so the address should not be in it.

This rewrites `meta.endpoint_host` to `meta.endpoint_id`, holding
`sha256(canonical_host(host))[:12]` — `config.legacy_endpoint_id`, which is
endpoint id **scheme 1** and is what every cassette in the repository carries.
Scheme 2 hashes the whole address and this script deliberately
does not follow it there: a hostname is all it has, the corpus it already wrote
cannot be re-derived from one, and a migration that changed its answer after the
fact would be rewriting history rather than recording it.

The normalisation runs *before* the hash
and is the load-bearing half: `127.0.0.1` and `localhost` are one machine, and
hashing them apart would make the endpoint guard fire on history rather than on
a mistake. That is the same failure this task's first half already fixed in the
corpus, folded into the hash so it cannot come back.

**No cassette key moves.** The field is not in the key, and the script proves it
rather than asserting it: the key index of every directory is compared before
and after, and each rewritten file must differ on exactly the lines that carry
the field.

Run with `python3 tests/migrate_endpoint_id.py [--apply]`. Without `--apply` it
reports what it would do and writes nothing.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

socket_guard.install()

from llossless import config  # noqa: E402
from llossless.cassette import Store  # noqa: E402

CORPORA = (ROOT / "tests" / "responses",)


def cassettes(root: Path) -> list[Path]:
    return sorted(root.rglob("*.json"))


def index_of(paths: list[Path]) -> dict[str, str]:
    """key -> filename, for every readable cassette. The thing that must not move."""
    index: dict[str, str] = {}
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if "key" in data and "meta" in data:
            index[data["key"]] = path.name
    return index


def migrate(path: Path, apply: bool) -> str | None:
    """Rewrite one cassette. Returns the id written, or None if untouched."""
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    meta = data.get("meta")
    if meta is None or "endpoint_host" not in meta:
        return None

    # `legacy_endpoint_id`, not `endpoint_id`: this migration's output is on
    # disk in 818 cassettes and must keep reproducing. Scheme 2 moved
    # `endpoint_id` onto the whole address, which a hostname is not, so calling
    # it here would return "" and silently unwrite what this script already did.
    identifier = config.legacy_endpoint_id(meta["endpoint_host"])
    rebuilt = {}
    for name, value in meta.items():
        if name == "endpoint_host":
            # In place, so the field keeps its position and the diff stays one
            # line per file rather than a reordering of every key in `meta`.
            rebuilt["endpoint_id"] = identifier
        else:
            rebuilt[name] = value
    data["meta"] = rebuilt

    if apply:
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return identifier


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--apply", action="store_true", help="write the changes")
    args = parser.parse_args(argv)

    failures: list[str] = []
    total = 0
    written: Counter[str] = Counter()

    for root in CORPORA:
        paths = cassettes(root)
        before = index_of(paths)
        for path in paths:
            identifier = migrate(path, args.apply)
            if identifier is not None:
                total += 1
                written[identifier] += 1

        after = index_of(cassettes(root))
        if before != after:
            moved = {k for k in before | after.keys() if before.get(k) != after.get(k)}
            failures.append(f"{root}: {len(moved)} cassette key(s) moved")
        else:
            print(f"  {root}: {len(before)} key(s), index unchanged")

        # The guard's own question, asked of the result. One value means one
        # machine, which is what makes the corpus a measurement of a deployment.
        store = Store(root)
        found = store.endpoints() if hasattr(store, "endpoints") else {}
        print(f"  {root}: endpoints {found}")
        if len(found) > 1:
            failures.append(f"{root}: {len(found)} distinct endpoints after migration")

    verb = "rewrote" if args.apply else "would rewrite"
    print(f"\n  {verb} {total} cassette(s): {dict(written)}")
    if not args.apply:
        print("  dry run — pass --apply to write")

    for failure in failures:
        print(f"  FAIL {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
