"""Prompts are files, never inline strings.

Every prompt is loaded from prompts/*.md and hashed. The hash goes in the
report, so a run can be reproduced and a prompt tweak is visible rather than
silent. It is also what makes the verdict cache correct: change the prompt,
change the hash, recompute.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, replace
from importlib import resources
from pathlib import Path

# Where the prompt files are, in the two situations there are.
#
# Installed: `pyproject.toml` force-includes the repository's `prompts/` into
# the wheel as `llossless/_prompts`, and `importlib.resources` finds it beside
# this module wherever site-packages happens to be. This used to be
# `parents[2] / "prompts"` alone, which in a wheel resolves to the directory
# above site-packages and does not exist -- every command that loads a prompt
# refused, and gate 3 did not notice because `--help` loads none of them,
# a pre-release review finding.
#
# A checkout: `_prompts` is a build-time copy and is not in the source tree, so
# the repository's own `prompts/` answers, unchanged. That ordering is
# deliberate -- an installed package must not read a directory it did not ship
# -- and it is why a developer editing `prompts/merge.md` still sees the edit.
#
# `resources.files` is used as a path, not as a Traversable: the prompts are
# read by name, hashed, and their paths are printed in the provenance table, so
# a zipped install would need a different mechanism anyway. pip unpacks wheels,
# and `load` refuses by name rather than guessing if that ever stops being true.
PACKAGED_PROMPTS = Path(str(resources.files("llossless"))) / "_prompts"
CHECKOUT_PROMPTS = Path(__file__).resolve().parents[2] / "prompts"
PROMPT_CANDIDATES = (PACKAGED_PROMPTS, CHECKOUT_PROMPTS)
PROMPTS_DIR = next((d for d in PROMPT_CANDIDATES if d.is_dir()), PACKAGED_PROMPTS)


@dataclass(frozen=True)
class Prompt:
    """A prompt file, its text, and the hash that identifies this version of it."""

    name: str
    path: Path
    text: str
    sha256: str

    def render(self, **fields: str) -> str:
        """Substitute {placeholders}. Missing placeholders are a bug, not a default.

        One pass, and that is the injection guard rather than a tidy-up. Every
        value substituted here is untrusted — a source document, a merged
        document a model wrote from source documents, the claims decomposed out
        of them — and substituting field by field rescans what the previous
        field just inserted. A document containing the literal `{claims}` was
        therefore handed the claim list *inside the reference text*, where the
        verifier reads it as part of the document it is grading.

        Substituting all fields in one scan means a value is never re-read as
        template. Order stops mattering, which is the point: the call sites no
        longer have to be ordered defensively, and a new field cannot reopen
        this by being added in the wrong place.

        This changes nothing for any input that does not contain a placeholder
        token, so no cassette key moves.
        """
        tokens = {"{" + key + "}": value for key, value in fields.items()}
        for token in tokens:
            if token not in self.text:
                raise KeyError(f"{self.name} has no placeholder {token}")
        if not tokens:
            return self.text
        pattern = re.compile("|".join(re.escape(token) for token in tokens))
        return pattern.sub(lambda found: tokens[found.group(0)], self.text)


def compose(base: Prompt, *fragments: Prompt) -> Prompt:
    """The same prompt, hashed with the fragments that get substituted into it.

    `Prompt.sha256` hashes the *unrendered* file, and `client.py` passes exactly
    that as `prompt_sha256`. So substituting a fidelity fragment into
    `{fidelity_rules}` changes what the model is shown and changes nothing about
    the digest — a report would name `merge.md` and be unable to say which
    level produced the run.

    This composes the digest and only the digest. `text` is left alone, so
    `render` still works and the placeholder is still substituted at call time;
    what moves is the one value the report identifies a prompt version by.

    **This is not a cassette key component and must not become one.** The key
    already separates the levels through `messages`, because the rendered
    fragment is in the message the model was sent. Adding a field to
    `cassette.key_for` would change the hash for *every* role and orphan all
    790 committed cassettes, decompose's 256 included; composing an existing
    value changes it only for the roles being re-recorded anyway. Those two
    figures read 423 and 357 when this was written; they are recounted rather
    than carried forward, because the argument is about the size of the blast
    radius and a stale count understates it.

    Order is significant and is the caller's, not sorted here: the digest
    identifies one arrangement of fragments, and two prompts that substitute the
    same fragments into different placeholders are different prompts.

    Composing no fragments is the identity, which is deliberate: wiring this
    into a call site that has nothing to substitute yet cannot move a key, so
    the orphaning happens when a fragment actually arrives and not before.
    """
    digest = hashlib.sha256(
        "".join([base.text, *(fragment.text for fragment in fragments)]).encode("utf-8")
    ).hexdigest()
    return replace(base, sha256=digest)


def load(name: str, directory: Path | None = None) -> Prompt:
    """Load prompts/<name>.md. A missing prompt is fatal, never substituted."""
    base = directory or PROMPTS_DIR
    path = base / f"{name}.md"
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        # Two different failures, and an operator can only act on one of them.
        # A missing file under a directory that exists is a prompt name that is
        # wrong. No directory at all is an install that shipped no prompts, and
        # the message has to name every place that was looked in: an earlier
        # review finding was a refusal naming one path that told nobody why it was that
        # path.
        if base.is_dir():
            why = ""
        elif directory is not None:
            why = f"; no such directory: {base}"
        else:
            why = ("; no prompt directory exists. Looked in "
                   + " and ".join(str(d) for d in PROMPT_CANDIDATES)
                   + ". An installed LLossless carries its own prompts; if "
                   "this one does not, the wheel was built without them.")
        raise FileNotFoundError(f"prompt not found: {path}{why}") from None
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return Prompt(name=name, path=path, text=text, sha256=digest)
