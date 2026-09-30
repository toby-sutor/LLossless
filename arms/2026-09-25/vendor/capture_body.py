#!/usr/bin/env python3
"""Run claimcheck's CLI with the transport replaced by a recorder: no request leaves.

    capture_body.py OUT.json -- merge ...
The first chat request body is written to OUT.json and the run is ended.
"""
import json, os, sys
from pathlib import Path
TREE = Path(os.environ["BENCH_TREE"]).resolve()
sys.path.insert(0, str(TREE / "src"))
import claimcheck
assert claimcheck.__file__.startswith(str(TREE / "src") + os.sep), claimcheck.__file__
from claimcheck import cli, transport
out = Path(sys.argv[1]); argv = sys.argv[3:]
def record(url, payload, **kwargs):
    out.write_text(json.dumps({"url": url, "body": payload}, indent=1))
    raise SystemExit(f"captured {url}")
transport.post_json = record
sys.exit(cli.main(argv))
