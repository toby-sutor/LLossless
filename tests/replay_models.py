"""The model ids a recorded corpus was made with, read from the corpus. One definition.

An offline replay has to name the model its cassettes were recorded against:
the model is in the cassette key, so any other id misses every recording.
These runs used to name no model, so they took whichever one
`models.local.json` or `LLOSSLESS_MODEL` happened to supply. On a fresh clone
of the published set that is neither: `models.local.json` is untracked and the
ship-gate rehearsal runs with no environment, so a run exited on "no model
configured". On the author's machine the same runs quietly used a private model
id, and after a re-record that id is the wrong one. Both are the same fault --
the model a replay needs is a property of the recording, and the recording is in
the repository, so it is read from there.

Not a default inside the harness. A live run must still be told what to call;
only a replay has the answer already, and only the tests and audits that replay
the committed corpus are entitled to assume one.

Copies of this lived in `test_decompose.py`, `test_verify.py` and
`test_reconcile.py`, and `audit_docs.py` needed another. This is the one they
share.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESPONSES = ROOT / "tests" / "responses"

# Which flag names the model for which role. `--model` sets verify and
# decompose (and merge, unless `--merge-model` follows it), so decompose and
# verify must agree for one argv to replay both.
FLAG = {"decompose": "--model", "verify": "--model", "merge": "--merge-model"}


def recorded_models(directory: Path, role: str) -> set[str]:
    """Every model id the `role` cassettes in `directory` name, overlay included.

    `local/` is read too, because a replay reads it (`client._replay_store`):
    an overlay recorded against another model is a corpus one `--model`
    cannot replay, and that has to be an error here rather than a miss later.
    """
    found: set[str] = set()
    for where in (directory, directory / "local"):
        for path in sorted(where.glob(f"{role}-*.json")):
            model = json.loads(path.read_text(encoding="utf-8")).get("request", {}).get("model")
            if model:
                found.add(model)
    return found


def replay_argv(directory: Path = RESPONSES, roles: tuple[str, ...] = ("verify",)) -> list[str]:
    """`--model` and, when merge is among `roles`, `--merge-model`, for a replay of `directory`.

    Raises AssertionError unless each flag has exactly one answer: a corpus
    recorded with two models for one flag cannot be replayed by one argv, and
    picking one would be a replay that misses half of it.
    """
    argv: list[str] = []
    for flag in ("--model", "--merge-model"):
        wanted = [role for role in roles if FLAG[role] == flag]
        if not wanted:
            continue
        models: set[str] = set()
        for role in wanted:
            models |= recorded_models(directory, role)
        if len(models) != 1:
            raise AssertionError(
                f"the {'/'.join(wanted)} cassettes in {directory} were recorded with "
                f"{sorted(models)}; an offline run cannot be pinned to one model id "
                f"for {flag} until that is one entry")
        argv += [flag, models.pop()]
    return argv
