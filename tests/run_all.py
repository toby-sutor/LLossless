#!/usr/bin/env python3
"""Run every check this repository has, in one command, and fail if one is missing.

The defect this exists for: there was no run-everything entry point. The suite
only ran by invoking each file by hand, `unittest discover` fails on `tests/`
because it is not an importable package, and the withheld tools -- the docs
audit, the leak scan, the publication rehearsal -- were not in anybody's habit
at all. `audit_docs.py` went red for four stale citations without that being
noticed, because nothing ran it. A check that does not run passes.

So the tool list is written down rather than discovered, and a named tool that
is not on disk is a hard failure, never a skip. Discovery is additive only: a
new `tests/test_*.py` is picked up automatically and reported as unnamed, so
adding a test cannot leave it unrun, and deleting one cannot leave the runner
quietly greener than the repository.

Two tools need a working directory. They get a fresh temporary one per run
rather than a path in the repository, because both write a copy of the tree and
a stale copy is exactly the artefact the leak scans exist to catch.

Usage:
    python3 tests/run_all.py              # everything
    python3 tests/run_all.py --fast       # skip the slow publication rehearsal
    python3 tests/run_all.py --list       # print the tool list and exit

A failing tool keeps everything it printed. The summary line is the last
line only, which is right for a tool that passed and useless for one that
did not, so a failure also writes the whole capture to a file and prints
both ends of it with the command to rerun that tool alone. Set
`LLOSSLESS_RUN_LOG` to choose where those files go; the default is a fresh
temporary directory, named in the summary. Not the repository, because
`rehearse_publication.py` asserts the tree is unchanged and a log written
there would turn one failure into two.

A finished run also writes `.suite-stamp.json` at the repository root, which
the repository's pre-commit hook reads to refuse a commit landing on a tree this
suite has not passed. `LLOSSLESS_SUITE_STAMP` moves it, which is what
the rehearsal does when it runs this file inside the copy it is about to scan.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"

# What this run proved, for the pre-commit hook to read. Gitignored: it
# is a fact about one working copy at one moment and it would be stale in
# anybody else's. Written on every finished run, green or red, because "the
# suite was red" and "the suite never ran" are different refusals and the hook
# has to be able to tell a person which one they are looking at.
#
# Redirectable, like `LLOSSLESS_RUN_LOG` and the cache, and for the same
# reason: `rehearse_publication.py` runs this suite inside the copy it is about
# to scan, and the copy is a real git repository -- it is `git init`ed and
# committed so the wheel can be built -- so nothing about the tree tells this
# file it is somewhere it should not write. The rehearsal says where instead.
STAMP = Path(os.environ.get("LLOSSLESS_SUITE_STAMP")
             or ROOT / ".suite-stamp.json")

# What a tool prints to say it did not check what it names -- whether it
# exited 0 because there was never anything to check here, or exited
# `UNMEASURED_EXIT` because there could have been and was not this run.
# `fixture_semantics.UNMEASURED` upper-cased, with the colon that makes it
# a marker rather than a word: see the note at the call site.
UNMEASURED_MARKER = "UNMEASURED:"

# The convention `audit_docs.py` and the other declining tools use for
# "this could have been checked and was not" -- as opposed to exit 0, which
# they also use for "there was never anything here to check." A caller that
# only reads the exit code (a CI gate) must not read either as a pass; this
# runner reads the marker to tell the two non-zero cases apart.
UNMEASURED_EXIT = 3


def marker_lines(out: str) -> list[str]:
    """Every line of `out` beginning `UNMEASURED_MARKER`, stripped."""
    return [line.strip() for line in out.splitlines()
            if line.strip().startswith(UNMEASURED_MARKER)]


def is_declined(code: int, out: str) -> bool:
    """`UNMEASURED_EXIT` beside at least one marker line: declined, not failed.

    Neither half is enough alone. `UNMEASURED_EXIT` for an unrelated reason
    is a crash, and a marker printed at any other code is the exit-0 case
    the loop below already handles without this function.
    """
    return code == UNMEASURED_EXIT and bool(marker_lines(out))


# The tools that reach the network, and what for. One, and it is named rather
# than described: a claim about the whole suite that is false for one member is
# the shape of claim this list exists to keep honest.
NEEDS_NETWORK = {"internal/tests/rehearse_publication.py"}

# Named, not globbed. The glob below adds; it never subtracts. `{work}` is
# substituted with a fresh temporary directory. `slow` tools copy the tree.
NAMED: list[tuple[str, list[str], bool]] = [
    ("tests/test_attribution.py", [], False),
    ("tests/test_catalogue.py", [], False),
    ("tests/test_client.py", [], False),
    ("tests/test_cli.py", [], False),
    ("tests/test_console.py", [], False),
    ("tests/test_decompose.py", [], False),
    ("internal/tests/test_docs.py", [], False),
    ("tests/test_fixtures.py", [], False),
    ("tests/test_html_report.py", [], False),
    ("tests/test_merge.py", [], False),
    ("tests/test_pairs.py", [], False),
    # The eight pre-freeze src fixes: I6 (backend error
    # classification), I7 (the dirty commit stamp), B3 (529/524 retryable),
    # I8 (the child's explicit environment), B7 (models_answered), refusal
    # naming, refuse-on-length-without-a-sent-ceiling, and four
    # report-accounting details.
    ("tests/test_prefreeze_fixes.py", [], False),
    # The answering-attempt accounting: per-call attempts,
    # waits and the answering attempt's own time, discarded calls, and the
    # split between what a cell is charged with and what is excluded.
    ("tests/test_answering_accounting.py", [], False),
    ("tests/test_handwritten.py", [], False),
    # The merge-measuring scripts read every source a pair has and refuse
    # a gap; three-source pairs arrived in `tests/handwritten/` later.
    ("tests/test_measure_merges.py", [], False),
    ("tests/test_coverage.py", [], False),
    # Nothing else here holds two implementations against each other: the
    # modules above test one function apiece and were all green over both
    # defects this one exists for -- a verify rule applied on one code path and
    # not the other, and one run described four different ways. A parity
    # failure is invisible to a test of either side.
    ("tests/test_contract_parity.py", [], False),
    # Public text names no commit: the general form of a rule first
    # applied to the README and docs/benchmark.md alone, here
    # over every docs/*.md page and the web interface's
    # own strings, git-verified rather than a denylist of one hash.
    ("tests/test_no_commit_ids.py", [], False),
    # The general form of that rule and of the rename check together, over
    # the whole published set rather than docs/*.md or one surface at a
    # time: no old name, no commit id, anywhere text leaves. A named,
    # one-line-reasoned exception list, checked against published_files()
    # itself so a stale entry is caught rather than just unused.
    ("tests/test_published_names.py", [], False),
    ("tests/test_reconcile.py", [], False),
    # The number format: each document's decimal convention, decided from
    # its own numerals and then its language, and a merged value that changed.
    ("tests/test_numerals.py", [], False),
    # A replay reads an answer no more strictly than its recording run
    # did. Named because the only corpus that needs it is the 27B re-record,
    # which is not committed yet, so nothing else in this list can see the
    # rule break until the day the import lands and every replay misses.
    ("tests/test_replay.py", [], False),
    # `run_detect.grade` accounts a second report of a detected plant
    # rather than calling it invented, and `--regrade` re-scores saved reports.
    ("tests/test_run_detect.py", [], False),
    # The pairs scorer (no model a judge, formatting moves nothing) and
    # the headline rules every figure script forms rows by: common pairs,
    # draws apart, exact money, one seconds source. Each seeded both ways.
    ("tests/test_figure_rules.py", [], False),
    # The fair-lineup runner and its figures, end to end against a fake
    # model and a fake `claude`, from a throwaway pinned clone: the pin and the
    # clean tree, the registration, the child environment, the model that
    # answered, the failure classes and the retry pass, resume, the spend
    # cap, pre-warm, the 27B thinking pilot, and `lineup_figures`' common-pairs
    # rule and `--check`; the positive-evidence classifier, refusals, limits,
    # the GPU cap, the torn journal, the address redaction, the floors and the
    # rule that a row's own failure never shrinks another's pairs; the
    # reference check, the outage pause, the reuse of a cell's own earlier
    # answers, the refusal and unruled flags, the harness timeout and Haiku's
    # one level. Each seeded both ways; no model call.
    ("tests/test_run_lineup.py", [], False),
    ("tests/test_run_arm.py", [], False),
    ("tests/test_segment.py", [], False),
    ("tests/test_socket_guard.py", [], False),
    ("tests/test_spend.py", [], False),
    ("tests/test_verify.py", [], False),
    # The job layer and the progress events, which nothing else reaches:
    # `test_cli.py` proves the engine never imports `llossless.web`, so by
    # construction no other module in this list can exercise a line of it.
    ("tests/test_web_jobs.py", [], False),
    # The CLI-equivalent block ("Web UI: show the equivalent CLI command for a
    # run"). Named for the same reason as its neighbour: `test_cli.py` proves
    # the engine never imports `llossless.web`, so no other tool here reaches
    # `web/cli_render.py`. Its own reason is the round trip -- the rendered
    # command is fed back through the CLI's own parser and `config.resolve`
    # and asserted equal to the settings the job ran with, on every route kind
    # and every fidelity level and depth, seeded by dropping a flag -- and the
    # must-not-fire half: no stored key, suffix, or command-route program ever
    # appears in the rendered payload.
    ("tests/test_web_cli_render.py", [], False),
    # The HTTP server and the `/api/v1` contract, driven over a real
    # loopback socket. Named here for the same reason its neighbour above is:
    # `test_cli.py` proves the engine never imports `llossless.web`, so no
    # other tool in this list can reach a line of it. It also holds the
    # equivalence check -- one merge through the web path and one through
    # `cli.main` against the same scripted endpoint, reports required to agree
    # -- which is the only thing standing between the two paths drifting.
    ("tests/test_web_server.py", [], False),
    # The credentials file, the settings routes and the bind token, driven
    # against real servers the same way. Named for the same reason as its two
    # neighbours, and for one of its own: the checks in it are the only place
    # anything asserts that a non-loopback bind with no token refuses to
    # start, and a suite that did not run them would be a suite in which that
    # refusal could be deleted without a single red line.
    ("tests/test_web_credentials.py", [], False),
    # Accounts, sessions, per-user credentials and job ownership. Named
    # here for the same reason as the three above it -- `test_cli.py` proves
    # the engine never imports `llossless.web`, so no other tool in this list
    # can reach a line of it -- and for one of its own: it is the only place
    # anything asserts that two concurrent jobs are handed two different keys,
    # that one user cannot read another's run by id, and that a non-loopback
    # bind is permitted once an account exists. Every one of those is silent
    # when it breaks: a job served to the wrong user is a correct-looking 200
    # and a key crossing between two runs is a merge that works.
    ("tests/test_web_accounts.py", [], False),
    # Saved defaults: a person's run settings on the server, beside their
    # credentials. Named here for its neighbours' reason -- nothing else in
    # this list reaches `llossless.web` -- and because both properties it
    # holds are silent when they break: one user's defaults served to
    # another is a correct-looking 200, and a model no longer offered that
    # is quietly replaced is a run on a route nobody chose.
    ("tests/test_web_defaults.py", [], False),
    # The shipped interface: what `static/` references, what it says,
    # and what it escapes. Named here because nothing else in this list
    # reads those three files -- they are data to every other tool -- and
    # because both properties it holds are silent when they break: a page
    # that fetches a font from a third party still renders, and a `data-t`
    # key with no string behind it still lays out.
    # The command-route allowlist, and the two seeded probes that post
    # a command string and an unknown id straight at the API. Named here for
    # the same reason as its four neighbours above -- `test_cli.py` proves the
    # engine never imports `llossless.web`, so no other tool in this list can
    # reach a line of it -- and for one of its own: it holds the only check
    # anywhere that a request cannot make this server run a program, and the
    # only control run proving that the program *can* be started, without which
    # the first check is a statement about a backend that was never wired.
    ("tests/test_web_commands.py", [], False),
    ("tests/test_web_static.py", [], False),
    # The theme toggle (storage key, three modes, applied before
    # first paint) and WCAG AA over every token pair in both themes; silent
    # when it breaks, because a page in the wrong colours still renders.
    ("tests/test_web_theme.py", [], False),
    # A command route named after the model its alias answers as now,
    # its figures marked when they were measured on another model and ranked
    # after every current figure; silent when it breaks, because a route
    # named after a retired model still renders.
    ("tests/test_route_label.py", [], False),
    # The two-pane workbench: the step, output and finding
    # tablists follow the WAI-ARIA pattern, and a blocked run leads to the
    # step that holds it back; silent when it breaks, because a tab that
    # hides the reason still renders.
    ("tests/test_web_layout.py", [], False),
    # The models table's width, as far as a suite with no browser can
    # hold it: that no string rendered into a cell that cannot wrap is a
    # sentence, that the marker under a model name wraps where the meta line
    # above it does not, and that both caveats a subscription row owes its
    # reader are still said under the table. Named here because all three are
    # silent when they break -- a table that scrolls sideways still renders,
    # and a caveat shortened to nothing still lays out -- and because the
    # widths themselves were measured in a browser, which this suite cannot do
    # and which therefore cannot be what stops the regression coming back.
    ("tests/test_web_table.py", [], False),
    # The two string catalogues, the route that serves them and the
    # `Accept-Language` negotiation behind it. Named here because every
    # property it holds is silent when it breaks: a catalogue missing half its
    # keys renders a page that looks translated, a renamed placeholder puts a
    # brace in the middle of one sentence, and a record that came back in a
    # different language because the reader's browser was configured
    # differently still parses. It also carries the only seeded probe in the
    # suite for `tsc` itself -- its neighbour asserts the type check passes,
    # and nothing else asserts that a real type error would be reported.
    ("tests/test_web_i18n.py", [], False),
    # Withheld from publication, and the reason they were never run: they are
    # not named `test_*` and no habit covered them.
    ("internal/tests/audit_docs.py", [], False),
    # The voyager scorer's key is derived by diff from the operator's pair, and
    # it holds both controls: the reference scores every planted error fixed,
    # the unmerged sources score none. The typed key it replaced had neither.
    ("tests/test_score_voyager.py", [], False),
    ("tests/scan_artefacts.py", ["--self-test"], False),
    ("tests/source_guard.py", ["--self-test"], False),
    ("tests/probe_vendors.py", ["--self-test"], False),
    ("tests/probe_shapes.py", ["--self-test"], False),
    # The must-fire schema probe, offline against its two loopback models.
    ("tests/schema_carriage.py", ["--self-test"], False),
    ("tests/run_vendor_arm.py", ["--self-test"], False),
    ("tests/smoke_vendor.py", ["--self-test"], False),
    ("tests/regrade_check2.py", ["--self-test"], False),
    ("tests/regrade_detect.py", ["--self-test"], False),
    # A guard fixture's probes were never graded at all
    # (`planted()` keeps only `expected_finding != "none"`, which is every
    # probe on a guard fixture, by construction). `--reports-dir` needs the
    # 2026-09-03 re-run's saved model reports and is exercised outside the
    # suite; the self-test alone proves the grading, seeded both ways.
    ("tests/regrade_guard_probes.py", ["--self-test"], False),
    ("tests/regrade_inventions.py", ["--self-test"], False),
    # `--check` only. Generating is a deliberate act; this asserts the
    # committed pages still match a fresh generation from the records,
    # which is the same staleness class as a prose figure that stopped
    # agreeing with the number behind it.
    ("tests/annotate_merges.py", ["--check"], False),
    # The benchmark matrix: every measured run group, its settings, its
    # figures and whether its raw output is committed, regenerated from the
    # records. `--check` fires its own tamper probes before it compares.
    ("tests/benchmark_matrix.py", ["--check"], False),
    # Same discipline one level down: `annotated/` shows what a merge
    # got wrong, this shows the chain behind every call. `--check` only, and it
    # asserts its own coverage against a count derived from the sources, so a
    # trail that quietly stopped covering part of the corpus fails here rather
    # than reading as complete.
    ("internal/tests/build_full_audit.py", ["--check"], False),
    # The generalised gate. `run_bench.py -> docs/bench-spec.md`
    # (since fixed) was one instance of a class -- a published file depending
    # at runtime on a file the manifest withholds. This derives every such
    # dependency from source rather than listing them, seeded with that known
    # instance and self-tested against read/write/name-only shapes so it does
    # not fire on a path merely mentioned.
    # The full scan, not just its self-test. It ran with `--self-test` alone
    # from the day it was added, so the check it exists for -- no published file
    # reads a withheld one -- had never gated anything, and was green over
    # `annotate_merges.py` reading a then-withheld `paper/records/` file for as long
    # as it existed. No-args runs the self-test *and* the scan.
    ("internal/tests/scan_dependencies.py", [], False),
    # The pre-commit gate on `paper/records/`. The records are published, so
    # the release scan reads them too, but only after the commit; this is the
    # detector that runs before it, and git history is permanent.
    ("internal/tests/gate_records.py", [], False),
    # `gate_records.py` decides whether a record may be committed;
    # this decides whether the inputs behind it were. An earlier check tested that a
    # pointer resolves, which is a weaker question than whether the thing it
    # points at is in the repository -- and the second is the one that costs a
    # paid re-run when the answer is no.
    ("internal/tests/gate_inputs.py", [], False),
    # `structured.ThinkingIgnored` writes the fact of a
    # collapsed reasoning contrast to every report it happens on; nothing read
    # it back across an arm until this. Regression-checked against the one
    # real case on record -- B1-70b-default's contrast with B2-70b-think never
    # held -- rather than against a stub, because a synthetic report would not
    # have caught that `decoding.thinking` looks like a measurement and is not
    # one.
    ("internal/tests/check_reasoning_honesty.py", [], False),
    # The re-run's numbers are also stated in prose,
    # and nothing else in the suite reads a number out of a doc. A
    # sentence about a result is a claim with a truth value.
    ("tests/grade_rerun.py", ["--self-test"], False),
    # The benchmark runner held seven refusals and was reachable only from a
    # bench session: not named here, no self-test, and `main` needs a card and
    # a paid endpoint. So the gate `95-availability.tex` claims -- a registered
    # property with no implementation aborts before a score is written -- had
    # run twice ever, on the two trees whose authors already believed them
    # clean. `--self-test` needs neither endpoint nor GPU: it compares the
    # `docs/bench-spec.md` registry against the implemented property set on
    # every commit, and seeds each of the refusals to fire.
    ("tests/run_bench.py", ["--self-test"], False),
    # This runner itself. `--self-test` exits before any tool runs, so this
    # is a probe of the withheld-tool split and not a recursion.
    ("tests/run_all.py", ["--self-test"], False),
    # Order is load-bearing: the rehearsal builds the tree that would be
    # published, and the scan runs over that tree rather than over a set
    # derived a second way. Same `{work}` for both, so they cannot drift apart.
    ("internal/tests/rehearse_publication.py", [".", "{work}"], True),
    ("internal/tests/scan_release.py", [".", "{work}/fresh"], True),
    # The paper gates, outside every habit. The first is withheld; the second is not.
    ("internal/paper/check_numbers.py", [], False),
    ("paper/check_refs.py", [], False),
]

# Every runnable tool under `tests/` is either named above or excused here, by
# name and with a reason. This list is the gate, not the documentation.
#
# `rehearse_publication.py` already proves behaviourally what the manifest says
# nothing proves -- that a published file can run without a withheld one -- by
# building the copy and running the whole suite inside it. But it proves it only
# for the tools this file names. `run_bench.py` was not named, so it was never
# proven, and it could not run in the copy at all: it read its registration
# from `docs/bench-spec.md`, and `docs` was then withheld. The gate existed; it did
# not run where the defect was. So coverage of this list is now itself checked,
# because an entry point that silently omits a tool makes every gate downstream
# of it optional.
#
# `unnamed()` below has long globbed `test_*.py` and printed a note.
# A note is not a gate, and it could not have seen `run_bench.py` in any case.
NOT_RUN: dict[str, str] = {
    # Covered in-process by a named test, so running the tool again would be a
    # second measurement of the same thing.
    "tests/spend.py":
        "its `--self-test` is called in-process at tests/test_spend.py:31",
    "tests/run_arm.py":
        "its three guards are proved by tests/test_run_arm.py",
    "tests/run_decompose.py":
        "driven offline by tests/test_decompose.py and tests/test_fixtures.py",
    "tests/run_detect.py":
        "driven offline by tests/test_fixtures.py",
    "tests/score_planted.py":
        "driven offline by tests/test_score_voyager.py, which calls its command "
        "form too",
    "tests/score_voyager.py":
        "a thin shim over score_planted.py with the pair fixed to voyager; "
        "driven the same way",
    "tests/run_merge.py":
        "driven offline by tests/test_merge.py and tests/test_cli.py",
    "tests/run_verify.py":
        "driven offline by tests/test_verify.py",
    "tests/depth_figures.py":
        "its `--check` is run as a command by tests/test_catalogue.py, which "
        "is the command catalogue.json's verify_depth.derived_by names",
    "tests/subscription_figures.py":
        "its `--check` is run as a command by tests/test_catalogue.py, which "
        "is the command catalogue.json's command_routes derived_by names",
    "tests/effort_figures.py":
        "its `--check` is run as a command by tests/test_catalogue.py, which "
        "is the command catalogue.json's measured_by_effort derived_by names",
    "tests/opus55_effort_figures.py":
        "its `--check` is run as a command by tests/test_catalogue.py, which "
        "is the command catalogue.json's pinned_by_effort derived_by names",
    "tests/mahjongg_figures.py":
        "its check runs inside tests/effort_figures.py --check and "
        "tests/opus55_effort_figures.py --check, and tests/test_catalogue.py "
        "probes it; those two are its arms' derived_by commands",
    "tests/rank_scale_floor.py":
        "its `--check` is run as a command by tests/test_web_static.py, which "
        "holds the page's deviations band to the union floor",
    "tests/vendor_figures.py":
        "its `--check` is run as a command by tests/test_catalogue.py, which "
        "is the command the GPT-6 and Opus 5.5 rows' derived_by names",
    "tests/google_figures.py":
        "its `--check` is run as a command by tests/test_catalogue.py, which "
        "is the command the Gemini rows' derived_by names",
    "tests/matrix_figures.py":
        "its `--check` is run as a command by tests/test_catalogue.py, which "
        "is the command the 2026-09-18 API rows' derived_by names",
    "tests/phase4_figures.py":
        "its `--check` is run as a command by tests/test_catalogue.py, which "
        "is the command the Qwen rows' derived_by names",
    # Needs a card, a paid endpoint or a live host, and asserts nothing that
    # can be asserted without one. Each is a measuring instrument rather than
    # a gate: no refusal in it decides whether a result is publishable.
    "tests/calibrate_endpoint.py":
        "measures a live endpoint's latency; no endpoint, nothing to measure",
    "tests/vendor_arm_tee.py":
        "tees the request bodies of a paid vendor call",
    "tests/analyse_merges.py":
        "post-hoc exploratory analysis over merges already on disk; no refusals",
    "tests/measure_merges.py":
        "the coverage instrument over merges already on disk; no refusals",
    "tests/league_table.py":
        "post-hoc league table over the published arms; its figures are "
        "re-derived and compared with tests/league_table.json by "
        "tests/benchmark_matrix.py, which run_all runs",
    "tests/merge_title_guard.py":
        "the semantic half of the title check, stubbed and offline; it is run "
        "by name from test_reconcile.py rather than as its own tool",
    "tests/rank_matrix.py":
        "post-hoc ranking of the repo-pair matrix against each pair's ideal.md; "
        "no refusals, no model call; tests/matrix_figures.py checks the same "
        "cells by the same code",
    "tests/rank_arms.py":
        "post-hoc ranking of recorded arms against the operator's expected "
        "merges; no refusals; its scoring is re-run by tests/phase4_figures.py "
        "and tests/benchmark_matrix.py",
    # The fair-lineup runner, its figures and its fakes. Run by hand, never
    # here: the runner makes model calls, and a run needs a registration and a
    # pinned clone. All three are driven in-process and as commands by
    # tests/test_run_lineup.py, against a fake model and a fake `claude`.
    "tests/run_lineup.py":
        "the benchmark runner (model calls); driven against fakes by "
        "tests/test_run_lineup.py",
    "tests/lineup_figures.py":
        "needs a lineup run directory; its --write and --check are driven on a "
        "fake run, clean and tampered, by tests/test_run_lineup.py",
    "tests/lineup_fakes.py":
        "a fake model and a fake `claude` for tests/test_run_lineup.py; its "
        "dry-run command runs the whole lineup against them (minutes)",
    # Done, and kept for the record rather than for the run.
    "tests/migrate_endpoint_id.py":
        "a one-pass migration already applied to the committed cassettes",
    "internal/tests/known_failures.py":
        "its register is empty (`ENTRIES = ()`), and `modules()` re-runs every "
        "test_*.py as a subprocess to harvest failures -- running it here "
        "would double the suite's cost to assert nothing",
}

RUNNABLE = 'if __name__ == "__main__"'


# Where a runnable tool may live. Two roots: the publication-hygiene
# tools moved to `internal/tests/` and discovery globbed `tests/` alone, so ten
# of them would have left the suite by being moved and nothing would have said
# so. A tool that silently stops running is a known failure pattern, and a migration
# meant to improve leak safety must not manufacture one.
TOOL_ROOTS = ("tests", "internal/tests")

# The floor the discovery probe holds. Not a total to keep current -- a count
# that may only grow. It is pinned rather than derived because the failure being
# guarded against is discovery finding *fewer* tools than it did, and a derived
# figure would move with the defect.
DISCOVERED_FLOOR = 47


def tool_files(root: Path = None) -> list[Path]:
    """Every `.py` under either tool root, in one list."""
    root = root or ROOT
    out: list[Path] = []
    for where in TOOL_ROOTS:
        out.extend(sorted((root / where).glob("*.py")))
    return out


def discovered(root: Path = None) -> list[str]:
    """Every runnable tool either root holds, repo-relative."""
    root = root or ROOT
    return sorted(str(p.relative_to(root).as_posix()) for p in tool_files(root)
                  if RUNNABLE in p.read_text(encoding="utf-8", errors="replace"))


def uncovered(root: Path = None) -> list[str]:
    """Runnable tools under `tests/` that are in neither NAMED nor NOT_RUN.

    Runnable means it has a `__main__` block: something a person can invoke and
    therefore something that either runs here or is excused by name. Read from
    the source rather than from a list, because a hand-kept list of what to
    check is the thing that forgot `run_bench.py`.
    """
    root = root or ROOT
    named = {name for name, _, _ in NAMED}
    out = []
    for path in tool_files(root):
        rel = path.relative_to(root).as_posix()
        if rel in named or rel in NOT_RUN:
            continue
        if RUNNABLE in path.read_text(encoding="utf-8", errors="replace"):
            out.append(rel)
    return out


TIMEOUT = 1800


def withheld(root: Path = None) -> set[str]:
    """Tool names `publication-manifest.txt` keeps back, as path prefixes.

    Read rather than listed again here. A published copy of this repository is
    missing five of the tools below on purpose, and the alternative to deriving
    that from the manifest is a second hand-kept list that can disagree with the
    first. Absent because the manifest withholds it is a different fact from
    absent because someone deleted it, and only one of them is a defect.
    """
    manifest = (root or ROOT) / "publication-manifest.txt"
    if not manifest.is_file():
        return set()
    return {line.split(None, 1)[1].strip().rstrip("/")
            for line in manifest.read_text(encoding="utf-8").splitlines()
            if line.startswith("NOT-PUBLISHED ")}


def absent_by_kind(root: Path = None,
                   named: list = None) -> tuple[list[str], list[str]]:
    """Named tools not on disk, split into (deleted, withheld-by-manifest)."""
    root = root or ROOT
    keep = withheld(root)
    gone = [name for name, _, _ in (named or NAMED) if not (root / name).is_file()]
    known = [n for n in gone
             if any(n == k or n.startswith(k + "/") for k in keep)]
    return [n for n in gone if n not in known], known


def discovery_probe(root: Path = None) -> list[str]:
    """Refuse a tool count that has fallen. Must-fire probe below.

    The failure this exists for has no symptom: a tool moved out of the globbed
    root stops being discovered, stops running, and the summary line gets
    shorter. Nothing reports it, because nothing was looking at the number.
    """
    root = root or ROOT
    # Only where `internal/` exists. The publication copy has none by design, so
    # seven withheld tools are legitimately absent there and a floor written for
    # the source tree would fail every rehearsal. The floor is about a tool
    # disappearing from the tree that owns it.
    if not (root / "internal").is_dir():
        return []
    found = discovered(root)
    if len(found) < DISCOVERED_FLOOR:
        return [f"discovery found {len(found)} runnable tool(s), below the "
                f"pinned floor of {DISCOVERED_FLOOR}. A tool that stops being "
                f"discovered stops running and says nothing. Roots searched: "
                f"{', '.join(TOOL_ROOTS)}."]
    return []


def self_test() -> int:
    """Probe the split both ways, because only one side of it is ever exercised.

    In this repository nothing named is absent, so the branch that lets a
    published copy run at all never executes here and a regression in it would
    be invisible until somebody unpacked the copy. The must-fire probe is the
    one that matters: a tool that is simply gone must still stop the run.
    """
    fake = [("tests/kept_back.py", [], False), ("tests/deleted.py", [], False)]
    bad = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "tests").mkdir()
        (root / "publication-manifest.txt").write_text(
            "src\ntests\n\nNOT-PUBLISHED tests/kept_back.py\n", encoding="utf-8")

        gone, kept = absent_by_kind(root, fake)
        if gone != ["tests/deleted.py"]:
            bad.append(f"a deleted tool must be fatal, got {gone}")
        if kept != ["tests/kept_back.py"]:
            bad.append(f"a withheld tool must be excused, got {kept}")

        (root / "tests" / "deleted.py").touch()
        gone, kept = absent_by_kind(root, fake)
        if gone:
            bad.append(f"nothing is deleted now, got {gone}")

        # And the over-skip direction: withheld but present is a tool to run,
        # not a tool to excuse. This repository is that case for all five.
        (root / "tests" / "kept_back.py").touch()
        gone, kept = absent_by_kind(root, fake)
        if gone or kept:
            bad.append(f"present tools must not be excused, got {gone} {kept}")

    for line in bad:
        print(f"FAIL  {line}")
    print(f"{'FAIL' if bad else 'PASS'}  absence is split against the manifest "
          f"(4 probes, both directions)")

    # And the coverage of this file's own tool list, probed the same way. The
    # must-fire probe is a new runnable tool in neither list; the must-not-fire
    # probes are a tool that is named, a tool that is excused, and a module
    # with no `__main__` block, which is not a tool at all.
    worse = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "tests").mkdir()
        body = 'if __name__ == "__main__":\n    raise SystemExit(0)\n'
        (root / "tests" / "brand_new_tool.py").write_text(body, encoding="utf-8")
        got = uncovered(root)
        if got != ["tests/brand_new_tool.py"]:
            worse.append(f"a runnable tool in neither list must be reported, "
                         f"got {got}")

        (root / "tests" / "run_all.py").write_text(body, encoding="utf-8")
        (root / "tests" / "spend.py").write_text(body, encoding="utf-8")
        (root / "tests" / "a_library.py").write_text(
            "def helper():\n    return 1\n", encoding="utf-8")
        got = uncovered(root)
        if got != ["tests/brand_new_tool.py"]:
            worse.append(f"named, excused and non-runnable files must not be "
                         f"reported, got {got}")

        (root / "tests" / "brand_new_tool.py").write_text(
            "def helper():\n    return 1\n", encoding="utf-8")
        got = uncovered(root)
        if got:
            worse.append(f"nothing is uncovered now, got {got}")

    for line in worse:
        print(f"FAIL  {line}")
    print(f"{'FAIL' if worse else 'PASS'}  every runnable tool is named or "
          f"excused by name (3 probes, both directions)")

    # `tally_line`, must-fire and must-not-fire. One failure inlines its own
    # message beside the count nobody scrolls past; two failures do not,
    # because inlining both would be the clutter a bare count is there to
    # avoid on the run that is read in full anyway.
    wrong = []
    one = [("tests/a.py", 0, 1.0, ""), ("tests/b.py", 1, 2.0, "b's own reason")]
    line = tally_line(one, [one[1]], [])
    if "b's own reason" not in line:
        wrong.append(f"a single failure must carry its own message in the "
                     f"tally, got {line!r}")

    two = [("tests/a.py", 1, 1.0, "a's own reason"),
           ("tests/b.py", 1, 2.0, "b's own reason")]
    line = tally_line(two, two, [])
    if "a's own reason" in line or "b's own reason" in line or " -- " in line:
        wrong.append(f"two failures must not inline either message, got "
                     f"{line!r}")

    for line in wrong:
        print(f"FAIL  {line}")
    print(f"{'FAIL' if wrong else 'PASS'}  the tally inlines one failure's "
          f"message and not two's (2 probes, both directions)")

    # The third outcome, must-fire and must-not-fire. The half that
    # matters is the second: a tool that did not run must not be able to read
    # as a pass, and a green tally with a silent skip in it is what let a leak
    # live in the tree for two suite runs.
    missing = []
    ran = [("tests/a.py", 0, 1.0, ""), ("tests/b.py", 0, 2.0, "")]
    line = tally_line(ran, [], [], [("tests/c.py", "its input was not built")])
    if "DID NOT RUN" not in line or "1 tool(s)" not in line:
        missing.append(f"an unrun tool must be counted in the tally under a "
                       f"name of its own, got {line!r}")
    if "2 tool(s) run, 0 failing" not in line:
        missing.append(f"and must be counted in neither of the other two: "
                       f"{line!r}")
    line = tally_line(ran, [], [])
    if "DID NOT RUN" in line:
        missing.append(f"a run with nothing skipped must not mention the "
                       f"category at all, got {line!r}")

    for line in missing:
        print(f"FAIL  {line}")
    print(f"{'FAIL' if missing else 'PASS'}  a tool that did not run is its "
          f"own count, in neither the passes nor the failures (3 probes, both "
          f"directions)")

    # `is_declined`, must-fire and must-not-fire. Either half missing -- the
    # code without the marker, or the marker at some other code -- is a crash
    # or an ordinary exit-0 pass, and neither may read as a decline.
    confused = []
    if not is_declined(UNMEASURED_EXIT, "UNMEASURED: cannot check this here"):
        confused.append("UNMEASURED_EXIT with a marker line must be a decline")
    if is_declined(UNMEASURED_EXIT, "a crash unrelated to any figure"):
        confused.append("UNMEASURED_EXIT with no marker line must not be a decline")
    if is_declined(1, "UNMEASURED: cannot check this here"):
        confused.append("a marker line at an exit code other than "
                        "UNMEASURED_EXIT must not be a decline")
    if is_declined(0, "UNMEASURED: cannot check this here"):
        confused.append("a marker line at exit 0 is the existing pass-with-a-"
                        "marker case, not a decline")
    for line in confused:
        print(f"FAIL  {line}")
    print(f"{'FAIL' if confused else 'PASS'}  UNMEASURED_EXIT is a decline "
          f"only beside its own marker (4 probes, both directions)")

    bad += worse + wrong + missing + confused
    return 1 if bad else 0


def unnamed() -> list[str]:
    named = {name for name, _, _ in NAMED}
    return sorted(p.relative_to(ROOT).as_posix() for p in tool_files()
                  if p.name.startswith("test_")
                  and p.relative_to(ROOT).as_posix() not in named)


def run(name: str, args: list[str], work: Path) -> tuple[str, int, float, str, str]:
    """One tool. Returns the summary line *and* everything it printed.

    The whole output comes back, not just the last line. A passing tool is
    still reported by its last line -- that is the right summary and this file
    does not turn a green run into a wall of text -- but a failing one has its
    output kept by `main`, because that output is the only evidence the failure
    will ever produce. It was once discarded here, and a
    `test_html_report` failure that has not recurred since is unidentifiable
    because of it: the summary line named a count and not the group.
    """
    argv = [sys.executable, str(ROOT / name)]
    argv += [a.replace("{work}", str(work)) for a in args]
    start = time.monotonic()
    try:
        done = subprocess.run(argv, cwd=ROOT, timeout=TIMEOUT,
                              capture_output=True, text=True)
        code, out = done.returncode, (done.stdout + done.stderr)
    except subprocess.TimeoutExpired:
        code, out = 124, f"timed out after {TIMEOUT}s"
    tail = [line for line in out.strip().splitlines() if line.strip()]
    return name, code, time.monotonic() - start, (tail[-1] if tail else ""), out


def tally_line(results: list[tuple], failed: list[tuple],
                unmeasured: list[tuple], unrun: list[tuple] = ()) -> str:
    """The one line most likely to be the only one read.

    A single failure inlines its own message here, beside the count: the
    count is what gets read first, and on a truncating read -- a piped
    `tail -N`, a scrollback that has already lost the top -- it is read
    alone. The message was never missing; it prints two lines below this one
    in `main`'s own output. But a bare count with no text next to it is
    exactly what starts the mistake this function exists to stop: read "1
    failing", assume the worst, act on the count instead of the reason.

    Left bare above one failure on purpose. A multi-failure run is read in
    full regardless of how this line looks, and inlining several messages
    here would be the clutter a one-line summary is supposed to avoid for the
    case that actually needs the help.

    **`did not run` is a count of its own**. A tool whose input was
    never built used to be filed as a failure, which is honest about the exit
    code and wrong about what happened: the reader sees a number, attributes
    it to the tool that really failed, and moves on -- and a leak sat in the
    tree for two full suite runs behind exactly that reading, with the scanner
    that would have caught it never executing. "Did not run" is not
    "ran and passed" and it is not "ran and failed", and the only way a reader
    can act on the difference is to be shown it. The run is still red; three
    outcomes, two of them non-zero.
    """
    ran = len(results)
    tally = (f"{ran} tool(s) run, {len(failed)} failing, "
             f"{sum(r[2] for r in results):.0f}s total")
    if len(failed) == 1:
        tally += f" -- {failed[0][3]}"
    if unrun:
        tally += (f"; {len(unrun)} tool(s) DID NOT RUN -- their input was "
                  f"never built, so they have neither passed nor failed")
    if unmeasured:
        tally += (f"; {len(unmeasured)} check(s) UNMEASURED -- declined rather "
                  f"than checking what they name, not counted as failing")
    return tally


# Where a failing tool's output is kept. Not in the repository: writing there
# would dirty the tree, and `rehearse_publication.py` asserts the tree is
# unchanged, so a failure would cause a second, misleading failure. Not the
# `work` directory either -- that is removed in `finally`, which is exactly
# when the evidence is wanted. `$LLOSSLESS_RUN_LOG` overrides, so a session
# can point it at a scratchpad that is already being mirrored.
def log_dir() -> Path:
    named = os.environ.get("LLOSSLESS_RUN_LOG", "").strip()
    if named:
        path = Path(named).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        return path
    return Path(tempfile.mkdtemp(prefix="llossless-failures-"))


# Enough of a failing tool to identify it on the terminal, with the whole of it
# on disk. Both ends rather than the head: a runner prints its summary last and
# its first failure first, and a middle elided between them loses neither.
TERMINAL_LINES = 40


def excerpt(out: str) -> list[str]:
    lines = [line for line in out.rstrip().splitlines()]
    if len(lines) <= TERMINAL_LINES:
        return lines
    half = TERMINAL_LINES // 2
    return (lines[:half]
            + [f"       ... {len(lines) - TERMINAL_LINES} line(s) elided, "
               f"the whole output is in the log file below ..."]
            + lines[-half:])


def rerun(name: str, args: list[str], work: Path) -> str:
    """A command the reader can paste. `{work}` is expanded to a real path."""
    filled = [a.replace("{work}", str(work)) for a in args]
    return " ".join(["python3", name, *filled]).rstrip()


def stamp(results, failed, unmeasured, fast: bool, unrun=()) -> dict:
    """Write down what this run proved, and about which tree.

    The tree is `HEAD^{tree}`, not the index and not the working copy, and the
    dirty count is recorded beside it. That pairing is the whole content: a
    green run is only possible on a clean tree in the first place, because
    `rehearse_publication.py` asserts `git status --porcelain` is empty, so a
    stamp that names a tree and admits to dirt is a stamp from a run that could
    not have been a release gate.

    What the hook does with it is therefore "was the tree you are committing
    *on top of* proved", never "is this commit good". That is the sequence it guards against
    exactly: three commits landed before anyone learned the tree was red.
    """
    def git(*args: str) -> str:
        done = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True)
        return done.stdout.strip() if done.returncode == 0 else ""

    record = {
        "when": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "head": git("rev-parse", "HEAD"),
        "tree": git("rev-parse", "HEAD^{tree}"),
        "dirty": len(git("status", "--porcelain").splitlines()),
        "tools": len(results),
        "failing": len(failed),
        # Recorded beside `failing` rather than added to it, so the hook can
        # refuse for the right reason and say which it was. A stamp
        # written before this key existed has no `unrun` and reads as zero,
        # which is what it was: the count was inside `failing`.
        "unrun": len(unrun),
        "unmeasured": len(unmeasured),
        "fast": fast,
    }
    # A stamp is a claim about a git tree, so where there is no tree there is
    # no claim to make: an extracted tarball gets no file rather than one whose
    # every field is empty. This does not cover the publication copy, which is
    # `git init`ed and committed so the wheel can build -- that one is handled
    # by the redirect at `STAMP`, and it was the copy that found this at all.
    #
    # A dirty tree is the same case. The run happened over files that are in no
    # tree, so it proves nothing about `HEAD`, and writing it would *overwrite*
    # the green stamp that does -- which is how a run made while the next item
    # was already in the working copy came to refuse the commit of the item
    # before it. The last stamp that means something survives instead, and the
    # hook's tree comparison is what keeps it honest if it is stale.
    if (record["dirty"] or not record["tree"]
            or git("rev-parse", "--show-toplevel") != str(ROOT)):
        return record
    try:
        STAMP.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    except OSError as problem:                    # a read-only tree is not a
        print(f"note: no stamp written ({problem})")   # reason to fail a run
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fast", action="store_true",
                        help="skip the tools that copy the whole tree")
    parser.add_argument("--list", action="store_true",
                        help="print the tool list and exit")
    parser.add_argument("--self-test", action="store_true",
                        help="probe the withheld-tool split and exit")
    options = parser.parse_args()

    if options.self_test:
        return self_test()

    if options.list:
        for name, args, slow in NAMED:
            print(f"{'slow' if slow else '    '}  {name} {' '.join(args)}".rstrip())
        return 0

    # Before anything runs, not after. A missing tool is the whole defect.
    deleted, kept_back = absent_by_kind()
    if deleted:
        print("REFUSING TO RUN. Named tools are not on disk:", file=sys.stderr)
        for name in deleted:
            print(f"  - {name}", file=sys.stderr)
        print("Either restore them or remove them from NAMED, on purpose.",
              file=sys.stderr)
        return 2

    # Refused before anything runs, and refused rather than noted: a runnable
    # tool this file has never heard of is a tool whose refusals have never
    # fired, and every gate the rehearsal applies to the published copy is
    # applied only to what this list names.
    fallen = discovery_probe()
    if fallen:
        print("REFUSED: " + fallen[0], file=sys.stderr)
        return 2

    orphans = uncovered()
    if orphans:
        print(f"REFUSED: {len(orphans)} runnable tool(s) under tests/ are in "
              f"neither NAMED nor NOT_RUN: {', '.join(orphans)}", file=sys.stderr)
        print("Add each to NAMED so it runs, or to NOT_RUN with the reason it "
              "does not. A tool nobody runs is a check that passes.",
              file=sys.stderr)
        return 2
    if kept_back:
        print(f"note: {len(kept_back)} tool(s) withheld by "
              f"publication-manifest.txt are not in this copy and will not "
              f"run: {', '.join(kept_back)}.\n")


    # The rehearsal asserts the source tree is untouched, so it cannot pass on
    # a dirty tree. Said here, before the run, because "the source repository is
    # unchanged by the rehearsal" reads like a defect when it is just uncommitted
    # work. It still runs and it still fails: a warning is not a skip.
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    rehearsing = any(n == "internal/tests/rehearse_publication.py" for n, _, _ in NAMED
                     if (ROOT / n).is_file())
    if dirty and not options.fast and rehearsing:
        print(f"note: working tree has {len(dirty.splitlines())} uncommitted "
              "change(s). internal/tests/rehearse_publication.py asserts the source tree "
              "is unchanged and will fail until they are committed or stashed.\n")

    extra = unnamed()
    plan = [(n, a, s) for n, a, s in NAMED
            if not (options.fast and s) and n not in kept_back]
    plan += [(n, [], False) for n in extra]

    # Said here, beside the withheld line, because "the test suite makes no
    # network call" was in the README and in the paper and was not true: this
    # one builds a virtual environment and fetches the build backend into it.
    # Every other tool is offline and `socket_guard` refuses anything else.
    #
    # Derived from the tool list rather than written out, so a second tool that
    # needs the network cannot join the suite without appearing on this line
    # -- and so a reader who sees only one name knows it is one.
    online = [name for name, _, _ in plan if name in NEEDS_NETWORK]
    if online:
        print(f"note: {len(online)} tool(s) make a network call: "
              f"{', '.join(online)}, once each, to fetch the build backend. "
              f"Every other tool here is offline.\n")

    work = Path(tempfile.mkdtemp(prefix="llossless-run-all-"))
    results, skip, kept, unmeasured, declined = [], set(), [], [], set()
    # Its own list, and deliberately not in `results`. A tool that never
    # started did not take 0.0s to pass and did not take 0.0s to fail; putting
    # it among the results made `N tool(s) run` count a tool that did not run
    # and made `F failing` a number the reader attributes to whatever really
    # broke. That reading has already cost something: a leak sat in the tree
    # through two full suite runs while the scanner that sees it never
    # executed, and the line that would have said so said "failing" instead.
    unrun: list[tuple[str, str]] = []
    logs: Path | None = None
    try:
        for name, args, _ in plan:
            if name in skip:
                # Not passed over quietly, and not filed as a pass or as a
                # failure either. An unrun check that prints nothing is the
                # defect this file exists for; an unrun check filed as a
                # failure is the same defect one reading later.
                unrun.append((name, "its input was not built"))
                print(f"NOTRUN   0.0s  {name}", flush=True)
                print("       its input was not built, so this check has "
                      "neither passed nor failed", flush=True)
                continue
            name, code, secs, last, out = run(name, args, work)
            results.append((name, code, secs, last))
            marked = marker_lines(out)
            # `UNMEASURED_EXIT` beside a marker line is the same outcome as
            # exit 0 beside one: a tool that correctly declined to check
            # something it cannot check here, not one that broke. The code
            # stays non-zero so a caller that only reads the exit code -- a
            # CI gate -- does not read this run as having checked the thing;
            # this runner reads the marker instead, the same way it already
            # does for the exit-0 case below.
            if is_declined(code, out):
                declined.add(name)
            mark = "ok  " if code == 0 else ("UNM " if name in declined else "FAIL")
            print(f"{mark} {secs:7.1f}s  {name}", flush=True)
            # UNMEASURED is a third outcome beside pass and fail, and a tool
            # that reports it has *not* checked the thing it names even though
            # it exited 0 (or `UNMEASURED_EXIT`, above). Surfaced rather than
            # folded into "ok": the whole point of the outcome is that a
            # reader can tell it from a check that ran and found nothing, and
            # summarising it away would undo that.
            #
            # `UNMEASURED:` with the colon, not the bare word. The loose match
            # was written first and fired on `regrade_inventions.py`, whose
            # self-test prose says "the unmeasured skip" -- one firing, and it
            # was the wrong one. A marker a tool emits on purpose is a claim; a
            # word in a sentence is not.
            if code == 0 or name in declined:
                # At the start of the line, not anywhere in it. A tool that
                # *quotes* another tool's output -- which is exactly what
                # `rehearse_publication.py` does, asserting that the copy's
                # suite said this -- would otherwise be reported as
                # unmeasured itself. Second time this scan has been too
                # loose; the first matched the bare word and caught a
                # sentence, this one matched a marker and caught a
                # quotation of it.
                for line in marked:
                    print(f"     {line}", flush=True)
                    unmeasured.append((name, line))
            if code != 0 and name not in declined:
                # The whole output, not the summary line. Written before it is
                # printed, so a runner killed part-way through still leaves the
                # evidence behind.
                if logs is None:
                    logs = log_dir()
                stem = name.replace("/", "-").removesuffix(".py")
                where = logs / f"{stem}.txt"
                command = rerun(name, args, work)
                where.write_text(
                    f"# {name} exited {code} after {secs:.1f}s\n"
                    f"# rerun: {command}\n"
                    f"# note: {{work}} was {work}, which is removed when this "
                    f"run ends; a tool that needs it wants a fresh directory\n\n"
                    + out, encoding="utf-8")
                kept.append((name, code, where, command))
                for line in excerpt(out):
                    print(f"       {line}", flush=True)
                print(f"       -> {where}", flush=True)
                if name.endswith("rehearse_publication.py"):
                    skip.add("internal/tests/scan_release.py")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    failed = [r for r in results if r[1] != 0 and r[0] not in declined]
    print()
    if extra:
        print(f"note: {len(extra)} test file(s) found by glob and not named in "
              f"NAMED: {', '.join(extra)}")
        print("      add them to NAMED so their deletion becomes a failure.")
    skipped = len(NAMED) - len([p for p in plan if p[0] not in extra])
    if skipped:
        print(f"note: --fast skipped {skipped} tool(s) that copy the tree; "
              f"this run is not a release gate.")
    print(tally_line(results, failed, unmeasured, unrun))
    for name, line in unmeasured:
        print(f"  ? {name}: {line}")
    # Above the failures, not below them. The failures are what a reader came
    # for; these are the checks whose answer this run does not have at all, and
    # a red suite therefore hides more than the failure it names. The
    # marker is `!` rather than `-`: a reader scanning for the difference
    # between the two lists has to be able to see it without reading either.
    for name, why in unrun:
        print(f"  ! {name}: DID NOT RUN -- {why}; nothing it checks was "
              f"checked on this tree")
    for name, code, _, last in failed:
        print(f"  - {name} exit {code}: {last}")
    if kept:
        # Repeated at the end because the per-tool output above has scrolled
        # by the time a long run finishes, and this is the part to act on.
        print()
        print(f"full output of {len(kept)} failing tool(s) kept in {logs}:")
        for name, code, where, command in kept:
            print(f"  {where.name}  (exit {code})")
            print(f"    rerun: {command}")
    stamp(results, failed, unmeasured, options.fast, unrun)
    # A tool that did not run keeps the run red. Splitting the category out of
    # `failed` was about what the reader is told, never about what the exit
    # code says: a suite that could not run one of its gates has not proved the
    # tree, and `0` here is the sentence "it did".
    return 1 if failed or unrun else 0


if __name__ == "__main__":
    sys.exit(main())
