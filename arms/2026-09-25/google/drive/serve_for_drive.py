#!/usr/bin/env python3
"""Start a real claimcheck web server, with four command routes through a fake
`claude`, for a real browser to drive against. Reuses
tests/test_web_server.py's claude_routes() fixture verbatim, so the routes are
exactly what test_web_server.py and test_web_static.py already exercise -- no
accounts (server.build's single-tenant mode), so no login gate to script.

Prints "URL <address>" once bound, then sleeps until killed.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve()
REPO = Path("<home>/Documents/Dev/vibe-coding/claimcheck")
sys.path.insert(0, str(REPO / "tests"))
sys.path.insert(0, str(REPO / "src"))

from test_web_server import claude_routes  # noqa: E402

import os
extra = {}
if os.environ.get('DRIVE_PROVIDERS'):
    extra = {'CLAIMCHECK_PROVIDER_URL_ANTHROPIC': 'https://anthropic.invalid/v1',
             'CLAIMCHECK_PROVIDER_URL_OPENAI': 'https://openai.invalid/v1',
             'CLAIMCHECK_PROVIDER_URL_GOOGLE': 'https://google.invalid/v1beta/openai'}
with claude_routes(extra) as (built, calls):
    print(f"URL {built.url}", flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass
