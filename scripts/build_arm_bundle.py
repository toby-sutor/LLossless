#!/usr/bin/env python3
"""Build the published arm bundle from a run directory, and gate it.

The three model-study arms ran on a rented pod; their raw
outputs lived only in the scratchpad, so the paper's model study was
recomputable from the per-arm records but not readable at the level of what a
model actually wrote. This copies those outputs into the repository.

Copying is the easy half. The gate is the point:

* **The pod address is in the run captures.** The CLI names the endpoint it is
  calling in its first line of stderr, which is right for an operator at a
  terminal and wrong in a published file, and the window probe repeats it. 22
  of 267 files in the first build carried it. Every file is put through
  `scripts/stream_redact.scrub`, which is the repository's one
  definition of what a secret looks like - not a second pattern
  written here.
* **The provider is in the run scripts, by name rather than by shape.** Both
  runners export an endpoint label built from the name of the company the pod
  was rented from. No address pattern can see that, the first build shipped it,
  and the release scan caught it three commits later. The
  detector is `internal/tests/providers.py`, withheld because the literal cannot live in
  a published file, and imported here by name.
* **A scan that has not fired on this input proves nothing.**
  `--self-test` plants every leak class into a copy and requires the gate to
  refuse it, so a build that reports clean has been shown to be capable of
  reporting dirty.

The source directory is not published and is never modified: it is the
operator's own record of the run, and this reads it.

    scripts/build_arm_bundle.py SOURCE DEST      build, scrub and gate
    scripts/build_arm_bundle.py --check DEST     re-gate a built bundle
    scripts/build_arm_bundle.py --self-test      prove the gate can fire
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "internal" / "tests"))

import stream_redact  # noqa: E402
import test_client  # noqa: E402

# Never copied. A `.pyc` is a build artefact of the scratchpad, not evidence,
# and it is the one thing here that is not text.
SKIP_PARTS = {"__pycache__"}
SKIP_SUFFIXES = {".pyc"}


def patterns() -> dict:
    """Every detector `test_client` defines, not just the address ones.

    The address is what this bundle was known to carry. A key would be the
    worse leak and the same one line of code catches it, so the gate reads
    both rather than the class that happened to be found first.

    The provider name is a third class and is not here, because it is matched
    by name rather than by shape and this file is published. `internal/tests/providers.py`
    holds it, is withheld, and is imported below by name.
    """
    return test_client.secret_patterns()


def provider_detector():
    """`internal/tests/providers.py`, or None when it is not in the tree.

    A published clone does not carry it, and `--check` is a command this
    repository's `arms/README.md` invites a reader to run. Absence therefore
    reports one fewer detector rather than refusing, and it says which one is
    missing: a scan that quietly runs short is the failure mode this whole file
    exists to avoid.
    """
    try:
        import providers
    except ImportError:
        return None
    return providers


def leaks(root: Path) -> dict[str, dict[str, int]]:
    """Every file under `root` that any detector fires on, with counts."""
    detectors = dict(patterns())
    provider = provider_detector()
    if provider is not None:
        detectors["compute provider named"] = provider.PROVIDERS
    found: dict[str, dict[str, int]] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = {name: len(p.findall(text))
                for name, p in detectors.items() if p.search(text)}
        if hits:
            found[str(path.relative_to(root))] = hits
    return found


def build(source: Path, dest: Path) -> tuple[int, int]:
    """Copy, scrubbing every file on the way in. Returns (files, scrubbed)."""
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    forms, pats = stream_redact.literal_forms(), stream_redact.patterns()
    # The runner scripts export an endpoint label built from the provider's
    # name, which no address pattern can see. Scrubbed on the way in rather
    # than found later: `<redacted>-2026-08-30` still reads as a label.
    provider = provider_detector()
    if provider is not None:
        pats = list(pats) + [provider.PROVIDERS]
    files = scrubbed = 0
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        if SKIP_PARTS & set(path.parts) or path.suffix in SKIP_SUFFIXES:
            continue
        target = dest / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        text = path.read_text(encoding="utf-8", errors="replace")
        clean = stream_redact.scrub(text, forms, pats)
        target.write_text(clean, encoding="utf-8")
        files += 1
        scrubbed += clean != text
    return files, scrubbed


def check(dest: Path) -> int:
    found = leaks(dest)
    total = sum(1 for p in dest.rglob("*") if p.is_file())
    provider = provider_detector()
    count = len(patterns()) + (provider is not None)
    if found:
        print(f"REFUSED: {len(found)} of {total} file(s) carry a secret shape.")
        for name, hits in sorted(found.items())[:20]:
            print(f"  {name}: {', '.join(f'{n} x {s}' for s, n in sorted(hits.items()))}")
        print("  The values are not repeated here. Fix the copy, never the pattern.")
        return 1
    print(f"clean: {total} file(s), 0 hits from {count} detector(s)"
          + ("" if provider is not None else
             "; the provider detector is withheld and absent from this tree, so "
             "it did not run"))
    return 0


def self_test() -> int:
    """Plant one of each leak class and require the gate to refuse.

    Assembled from fragments. A sample address written out is a sample address
    in a tracked file, and this file is inside the scan's own corpus.
    """
    host = ".".join(("pod-x", "provider-net", "io"))
    seeds = {
        "seeded-address.log": f"llossless merge model at https://{host}/v1",
        "seeded-key.log": "Authorization: Bearer " + "s" + "k-" + "A" * 24,
    }
    # The third seed is read from the withheld detector's own must-fire list
    # rather than written here, for the reason `patterns()` gives: this file is
    # published and the seed is the name itself.
    provider = provider_detector()
    if provider is None:
        print("-- the provider detector is not in this tree; 2 classes seeded, not 3")
    else:
        seeds["seeded-provider.log"] = provider.FIRE[0]
    with tempfile.TemporaryDirectory(prefix="arm-bundle-selftest-") as tmp:
        plot = Path(tmp)
        (plot / "clean.md").write_text("# a merge\n\nnothing here\n", encoding="utf-8")
        if check(plot) != 0:
            print("SELF-TEST FAILED: the gate refused a clean directory")
            return 1
        for name, body in seeds.items():
            (plot / name).write_text(body, encoding="utf-8")
        print(f"-- with {len(seeds)} classes planted, the gate must refuse:")
        if check(plot) == 0:
            print("SELF-TEST FAILED: the gate passed a directory holding "
                  f"{len(seeds)} planted leak(s). It cannot fire, so a clean "
                  "report from it means nothing.")
            return 1
        for name in seeds:
            (plot / name).unlink()
        if check(plot) != 0:
            print("SELF-TEST FAILED: the gate stayed red after the seeds were removed")
            return 1
    print(f"self-test passes: the gate fires on all {len(seeds)} classes "
          "and clears when they go")
    return 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["--self-test"]:
        return self_test()
    if argv[:1] == ["--check"] and len(argv) == 2:
        return check(Path(argv[1]).resolve())
    if len(argv) != 2:
        print(__doc__)
        return 2
    source, dest = Path(argv[0]).resolve(), Path(argv[1]).resolve()
    if not source.is_dir():
        print(f"no such source directory: {source}")
        return 2
    if self_test() != 0:
        return 1
    files, scrubbed = build(source, dest)
    print(f"copied {files} file(s) from {source.name}, {scrubbed} scrubbed")
    return check(dest)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
