# `tests/eval/`: trial recordings that are not kept

This directory is the place for trial recordings of model responses that should not become part of the repository, such as a first look at a new model or endpoint. Git ignores every subdirectory here (the `tests/eval/*/` line in `.gitignore`), so in a published copy this README is the only file. Nothing here is published, the test suite replays nothing from it, and no published figure is computed from it.

The recordings that are published, and that the test suite replays offline, are in `tests/responses/`. `tests/responses/README.md` describes them.

## Recording into this directory

Pass `--record tests/eval/NAME` to `tests/run_decompose.py`, `tests/run_merge.py` or `tests/run_verify.py` to write every model call to a directory, and `--replay tests/eval/NAME` to answer every call from it again. Recording needs a model endpoint; [the command reference](../../docs/reference.md) says how to configure one.

A recording is matched by a key computed from the whole request, and the request contains the prompt. When a prompt file changes, earlier recordings no longer match. That is why trial recordings are not kept: they stop being replayable at the next prompt edit, and nobody else could check a figure taken from them.

## What refers to this directory

Three published files refer to recordings in this directory, which a published copy does not have:

- `tests/calibrate_endpoint.py` measures an endpoint's latency with ten merge calls and writes its recordings to `tests/eval/m7-calibration/`.
- `tests/test_client.py` has one test that reads three recorded error responses from `tests/eval/m4-tier-latch/failures/` when that directory exists. When it does not, the module prints a line starting `unjudged: failure bodies: evidence not in this copy` and counts the step as unjudged, neither passed nor failed.
- `arms/BENCHMARK-MATRIX.md` lists seven early exploratory runs of 2026-08-07 and 2026-08-08 (rows X1 to X7) whose recordings were kept here. It marks them as having no published evidence, and their figures are not published.
