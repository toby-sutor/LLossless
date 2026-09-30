# `tests/eval/` — exploratory cassettes, not the record

This directory holds recorded responses from a one-off cross-model sweep run on
2026-08-07. **It is not the project's cassette corpus and nothing replays from
it.** The corpus that offline runs depend on is `tests/responses/`, which holds
local `qwen3:8b` cassettes only.

The cassettes themselves are gitignored; this README is the only tracked file
here. Two reasons they are not committed:

1. They were recorded from a dirty working tree — every one of them carries
   `meta.claimcheck_source` stamped `-dirty`, so no commit reproduces the
   inputs that produced them. A cassette whose provenance says "dirty" is
   evidence of a conversation, not of a build.
2. They were recorded against a prompt version that no longer exists in the
   tree, so their keys cannot be hit by any current run in any case.

They were not deleted because the sweep's cross-model figures were computed from
them, and those figures should stay checkable for as long as the files survive
on the machine that produced them.

## What is in them

Six models, one sample each, 8 fixtures: `gpt-5-1`, `claude-sonnet-4-5`,
`claude-opus-5`, `kimi-k2`, `kimi-k3`, and `qwen3:8b` recorded through the same
path for comparison. `kimi-k3`'s decompose run and `qwen-3-5-397b` entirely are
missing because the endpoint returned HTTP 504; those are non-measurements, not
results.

The five hosted models were reached through one OpenAI-compatible endpoint
configured in `.env`. Which endpoint that was is not recorded anywhere in the
repo and does not matter: any provider serving the same model ids would produce
a comparable sweep, and the finding is about the models, not about who was
hosting them.

No cassette in this directory or in `tests/responses/` contains an API key or an
`Authorization` header — checked by scanning every JSON file under `tests/` for
the key, the header name, and the full endpoint URL. The only trace of the
hosted endpoint is `meta.endpoint_id`, a truncated `sha256` of the hostname,
which answers whether two recordings share a machine without naming one.
