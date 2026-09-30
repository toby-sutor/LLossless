#!/usr/bin/env python3
"""The voyager pair's scorer: `score_planted.py --pair voyager`. Offline; no call.

Kept because the voyager answer-key review names this file.
Everything it did now lives in `score_planted.py`, which scores any pair with
planted errors (`voyager`, `bip39`) and the `mahjongg` false-correction
control; the functions below are that module's, with the pair fixed to
voyager. A later ruling changed the counting rule to one error per changed
unit, so the key is 44 errors, not the 47 it originally was.

Usage:
    python3 tests/score_voyager.py FILE...     # score merges
    python3 tests/score_voyager.py --key       # print the derived key
    python3 tests/score_voyager.py -v FILE...  # and every error's outcome
    python3 tests/score_voyager.py --json FILE...
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import score_planted as _planted  # noqa: E402
from score_planted import (DATE, QUANTITY, Error, Key, Merge, Piece, Word,  # noqa: E402,F401
                           load, words)

PAIR = _planted.PAIRS / "voyager"


def planted(pair: Path = PAIR) -> Key:
    return _planted.planted(pair)


def planted_text(pair: Path = PAIR) -> str:
    return _planted.planted_text(pair)


def score_text(text: str, key: Key | None = None) -> list[dict]:
    return _planted.score_text(text, key or planted())


def declared(records: list[dict] | None, key: Key | None = None) -> set[int] | None:
    return _planted.declared(records, key or planted())


def score(path: str | Path, key: Key | None = None) -> dict:
    return _planted.score(path, key or planted())


def main(argv: list[str] | None = None) -> int:
    return _planted.main(["--pair", "voyager", *(sys.argv[1:] if argv is None else argv)])


if __name__ == "__main__":
    sys.exit(main())
