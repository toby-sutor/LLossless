#!/usr/bin/env python3
"""Run one llossless command and keep every request body it actually sent.

Temperature `== 0.0` needs asserting in the recorded body per
draw, not inferred. Three things that look like the record are not:

  - `cassette.write` stores `temperature=TEMPERATURE`, the module constant. It
    is the same value whatever the request carried, so asserting on it asserts
    that a constant equals itself.
  - the `--json` report has no request block at all.
  - rebuilding the body here with `build_body` would prove the rebuild, which
    is the failure this project has already had twice.

So this captures the literal bytes handed to `urllib.request.Request`, one JSON
object per line, and nothing in `src/` changes to make that possible. It is an
observation of the wire, not a reconstruction of it. If the body ever stops
passing through `urllib`, the capture goes empty rather than silently wrong -
the driver treats an empty capture as a failed draw, because a draw whose
bodies nobody saw is exactly the draw this file exists to rule out.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


def main() -> int:
    out = Path(sys.argv[1])
    argv = sys.argv[2:]
    real = urllib.request.Request

    def teeing(url, data=None, headers=None, *args, **kwargs):
        # Every request, not only the ones with a body. A bodyless GET is still
        # a request to a third party, and the run this file was written for
        # died on one: `merge` probes `/api/ps` for the served window before it
        # generates, and skipping bodyless requests here made the run look as
        # though it had reached nothing at all.
        if True:
            try:
                body = json.loads(data.decode("utf-8")) if data else None
            except (ValueError, UnicodeDecodeError):
                body = {"_unparsed_bytes": len(data)}
            # The URL is kept because "which endpoint" is half of every
            # finding here. Headers are NOT kept: the Authorization header is
            # built one line below this and carries the key.
            with out.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({"url": url, "body": body}) + "\n")
        return real(url, data=data, headers=headers or {}, *args, **kwargs)

    urllib.request.Request = teeing
    from llossless import cli
    return cli.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
