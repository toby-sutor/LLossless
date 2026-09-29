"""Redact secrets from a runner's stdout and stderr, before the first line.

DECISIONS 91: a bespoke runner put an endpoint address into a transcript
through an HTTP error's *traceback*, which no print site can redact after the
fact. So the streams are wrapped at import, not at each call.

DECISIONS 92: the credential classes are covered too. `.env` holds real paid-API
credentials and an exception carrying one is the same path the 404 took.

Two sources, deliberately:

* **Values from the environment**, matched literally. This is what catches a
  host or key that no pattern anticipates, and it is why the address forms are
  expanded to netloc, bare host and leading label rather than trusted to a URL
  regex - a URL regex is precisely what missed the portless shape twice.
* **The scanner's own patterns**, imported from `tests/test_client.py` so there
  is exactly one definition of what a secret looks like in this repo. No
  pattern is written here and no example is embedded, because this file is
  tracked and acceptance 7 scans it.
"""
from __future__ import annotations

import os
import re
import sys
from urllib.parse import urlsplit

MARK = "<redacted>"
HOME_MARK = "<home>"

# `/home/<user>/` -> `<home>/`, generic rather than one literal username. An
# operator's home directory is not a secret in the way a key is, but it names
# a person and a machine layout, and 124 files under the published `arms/`
# carried one. Written as a rule and not as a literal because the next person
# to run an arm will have a different username and the same problem.
#
# `/home/` alone is left: it is the mount point and says nothing about anyone.
HOME_PATH = re.compile(r"/home/[^/\s\"\'`:;,)\]}]+/")

# Environment variables whose *values* are secrets. Names only: a name is not a
# secret and this file is published.
SECRET_VARS = ("HOSTED_OLLAMA_URL", "AI_API_KEY", "AI_API_BASE_URL",
               "LLOSSLESS_API_KEY", "CLAIMCHECK_API_KEY", "OPENAI_API_KEY")


def literal_forms(env=None) -> list[str]:
    """Every literal worth replacing, longest first so netloc beats bare host."""
    env = os.environ if env is None else env
    forms: set[str] = set()
    for var in SECRET_VARS:
        raw = (env.get(var) or "").strip().rstrip("/")
        if not raw:
            continue
        forms.add(raw)
        if "://" in raw:
            parts = urlsplit(raw)
            forms.update(f for f in (raw.split("://", 1)[-1], parts.netloc,
                                     parts.hostname) if f)
            if parts.hostname:
                forms.add(parts.hostname.split(".")[0])
    # A one- or two-character "secret" would redact ordinary prose to noise.
    return sorted((f for f in forms if len(f) > 3), key=len, reverse=True)


def patterns():
    """The scanner's detectors, or none if the test tree is not importable."""
    here = os.path.dirname(os.path.abspath(__file__))
    tests = os.path.join(os.path.dirname(here), "tests")
    if tests not in sys.path:
        sys.path.insert(0, tests)
    try:
        import test_client
    except Exception:
        return []
    return list(test_client.secret_patterns().values())


def scrub(text: str, forms=None, pats=None) -> str:
    """Literals first, then patterns, then home paths. Idempotent."""
    for form in (literal_forms() if forms is None else forms):
        text = text.replace(form, MARK)
    for pat in (patterns() if pats is None else pats):
        text = pat.sub(MARK, text)
    return HOME_PATH.sub(HOME_MARK + "/", text)


class _Stream:
    def __init__(self, stream, forms, pats):
        self._s, self._f, self._p = stream, forms, pats

    def write(self, text):
        return self._s.write(scrub(text, self._f, self._p))

    def __getattr__(self, name):
        return getattr(self._s, name)


def install() -> None:
    """Wrap stdout and stderr. Call before the first line of output."""
    forms, pats = literal_forms(), patterns()
    sys.stdout = _Stream(sys.stdout, forms, pats)
    sys.stderr = _Stream(sys.stderr, forms, pats)
