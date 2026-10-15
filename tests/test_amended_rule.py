#!/usr/bin/env python3
"""The amended rule for "reworded or gone", seeded both ways. Offline, no model.

`reconcile.locate` decides whether a source segment the merge does not carry
word for word is reworded or absent, and it has two rules for that line: the
registered one (a similarity ratio against one merge segment) and the amended
one of 2026-10-12, which adds two steps that look for the segment's own words
as one unbroken run of the merge. This module holds the amended rule to what
it is for and to what it must never do, in the two views that call it: the
tool's (`reconcile.reconcile`) and the benchmark scorer's
(`rank_matrix.located_of`, which reads the merge with its inline marks off).

The first principle is that a real loss stays a loss. So every case that must
be cleared (the content is there: a sentence joined to its neighbour, split
cleanly in two, turned into a list) stands beside siblings built from the same
line with one thing taken out, a clause, a number, a name, a link, which must
stay absent. A rule that cleared the first and not the second by accident of
length would pass a one-sided suite.

Four parts:

    synthetic   one pair of sources and a merge that carries every sentence;
                each case replaces exactly one line of that merge
    headings    an untaken heading is lost content only if its section is lost
                with it, or it carries a value the merge does not have
    controls    the nine pairs: reference merge, concatenation, mechanical
                union and base only, under both rules and in both views
    seeds       every real sentence of the nine pairs' sources, joined, split
                and cut, each in its own document; the three seeded losses the
                rule is known to clear are pinned by name, so a fourth is loud

Known limits are pinned as what they are and not as successes. `limit_kept`
is a false alarm the rule keeps (the content is there and the segment stays
absent); `limit_cleared` is a difference the rule clears (reworded, though a
reader would not call it the same statement).

Run with `python3 tests/test_amended_rule.py`, or collect with pytest.
"""

from __future__ import annotations

import dataclasses
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# No call is made here at all; the guard is the module's statement of it, in
# the shape `tests/test_socket_guard.py` asserts every test module uses.
socket_guard.install()

from llossless import config, reconcile, segment  # noqa: E402
from llossless.reconcile import (  # noqa: E402
    ABSENT,
    AMENDED,
    PRESENT,
    REGISTERED,
    REWORDED,
    STEP_CONTAINMENT,
    STEP_EXACT,
    STEP_NONE,
    STEP_PHRASE,
    STEP_RATIO,
)

import lineup_figures  # noqa: E402
import rank_matrix  # noqa: E402

PAIRS_ROOT = ROOT / "tests" / "pairs"
PAIRS = sorted(path.name for path in PAIRS_ROOT.iterdir() if path.is_dir())
BASE = "source_a.md"

failures: list[str] = []
counts = {"must_not_fire": 0, "must_fire": 0, "limit_kept": 0, "limit_cleared": 0}


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# --------------------------------------------------------------------------
# The two views
# --------------------------------------------------------------------------

def tool_view(documents: dict[str, str], merged: str, rule: str) -> list[reconcile.Located]:
    """Every source segment as the tool locates it."""
    result = reconcile.reconcile(documents, merged, rule=rule)
    return [item for coverage in result.coverages for item in coverage.located]


def scorer_view(documents: dict[str, str], merged: str, rule: str) -> list[reconcile.Located]:
    """Every source segment as the benchmark's scorer locates it."""
    return rank_matrix.located_of(documents, merged, rule=rule)[0]


VIEWS = {"tool": tool_view, "scorer": scorer_view}


def both_rules(documents: dict[str, str], merged: str) -> dict[str, tuple[list, list]]:
    """view name -> (amended, registered), and the additive property asserted."""
    out = {}
    for name, view in VIEWS.items():
        amended, registered = view(documents, merged, AMENDED), view(documents, merged, REGISTERED)
        additive(amended, registered, name)
        out[name] = (amended, registered)
    return out


def additive(amended: list, registered: list, where: str) -> None:
    """The amended rule only ever moves a segment from absent to reworded."""
    check([i.segment.id for i in amended] == [i.segment.id for i in registered],
          f"{where}: the two rules located different segments")
    for new, old in zip(amended, registered):
        if old.verdict == ABSENT:
            check(new.verdict in (ABSENT, REWORDED),
                  f"{where}: {new.segment.id} was absent and is now {new.verdict}")
        else:
            check(new.verdict == old.verdict,
                  f"{where}: {new.segment.id} was {old.verdict} and is now {new.verdict}; "
                  f"the amended rule may only clear an absence")
        check((new.ratio, new.nearest, new.nearest_text)
              == (old.ratio, old.nearest, old.nearest_text),
              f"{where}: {new.segment.id}: the similarity reading must not move with the rule")
        check(old.step == {PRESENT: STEP_EXACT, REWORDED: STEP_RATIO, ABSENT: STEP_NONE}[old.verdict],
              f"{where}: {old.segment.id}: registered step {old.step!r} for {old.verdict}")
        check(not (old.window or old.section or old.protected_missing),
              f"{where}: {old.segment.id}: the registered rule records what only the "
              f"amended rule computes")


def find(view: list, text: str) -> reconcile.Located:
    wanted = reconcile.flatten(text)
    hits = [item for item in view if reconcile.flatten(item.segment.text) == wanted]
    assert len(hits) == 1, f"{len(hits)} source segments read {text!r}"
    return hits[0]


def ids(items) -> list[str]:
    return [item.segment.id for item in items]


def silent(view: list, declared=frozenset()) -> list[str]:
    """Lost content no record explains, under the amended rule."""
    by_id = {item.segment.id: item for item in view}
    return [item.segment.id for item in view
            if reconcile.is_silent_loss(item, by_id, declared)]


def untaken(view: list, declared=frozenset()) -> list[str]:
    """Untaken headings with no record that are not lost content."""
    by_id = {item.segment.id: item for item in view}
    return [item.segment.id for item in view
            if reconcile.is_untaken_heading(item, by_id, declared)]


def silent_registered(view: list, declared=frozenset()) -> list[str]:
    """Silent loss as the registered scoring counts it: absent, not a title, no record."""
    return [item.segment.id for item in view
            if item.verdict == ABSENT and item.segment.kind != segment.TITLE
            and item.segment.id not in declared]


# --------------------------------------------------------------------------
# Synthetic families
# --------------------------------------------------------------------------

SOURCE_A = """# Relay Handbook

The relay listens on port 8443 and accepts TLS 1.2 or later.
Operators restart the relay from the console after every certificate change.
Operators record the restart in the change log within one hour.
The duty engineer confirms every restart by phone.
The duty engineer files the restart report with the site office by noon.
The connect timeout is 30 seconds.
The cutoff was 15:00 on the 20th.
After two failed attempts, call the workshop and log the fault code.
The handover needs the badge, the console key and the restart log.
"""

SOURCE_B = """# Relay Notes

## Night shift

The night shift lead signs the restart log before 06:00.
If the console is unreachable, phone the duty engineer on 555-0142 and wait for a callback before touching the relay.
Do not restart the relay while a transfer is running.
See [the transfer guide](https://docs.example.test/relay/transfers) for the list of transfer states.
The support desk escalates to the workshop after three failed attempts.
Security collects the badge at the exit.
Call security.
It is the same as it was.

```
relayctl restart --grace 30
```

- None.
"""

SOURCES = {"source_a.md": SOURCE_A, "source_b.md": SOURCE_B}

# Every body line of both sources, word for word, under A's title and B's heading.
BASE_MERGE = SOURCE_A + "\n" + SOURCE_B.split("\n", 2)[2]

# The lines a case may replace, by a short name.
LINE = {
    "listens": "The relay listens on port 8443 and accepts TLS 1.2 or later.",
    "restart": "Operators restart the relay from the console after every certificate change.",
    "record": "Operators record the restart in the change log within one hour.",
    "confirms": "The duty engineer confirms every restart by phone.",
    "files": "The duty engineer files the restart report with the site office by noon.",
    "timeout": "The connect timeout is 30 seconds.",
    "cutoff": "The cutoff was 15:00 on the 20th.",
    "attempts": "After two failed attempts, call the workshop and log the fault code.",
    "handover": "The handover needs the badge, the console key and the restart log.",
    "signs": "The night shift lead signs the restart log before 06:00.",
    "phone": ("If the console is unreachable, phone the duty engineer on 555-0142 and wait "
              "for a callback before touching the relay."),
    "donot": "Do not restart the relay while a transfer is running.",
    "guide": ("See [the transfer guide](https://docs.example.test/relay/transfers) for the "
              "list of transfer states."),
    "desk": "The support desk escalates to the workshop after three failed attempts.",
    "badge": "Security collects the badge at the exit.",
    "call": "Call security.",
    "same": "It is the same as it was.",
    "none": "- None.",
    "heading": "## Night shift",
    "block": "```\nrelayctl restart --grace 30\n```",
}
for _name, _line in LINE.items():
    assert BASE_MERGE.count(_line) == 1, f"{_name}: the base merge must hold this line once"

URL = "https://docs.example.test/relay/transfers"

# The two halves of the `phone` sentence as a merge might write them: cut at
# "and", which is dropped; a clause added in front of the first half and one
# after the second, so that neither half reaches the similarity threshold
# against the whole. The seam itself is clean: a full stop and nothing else.
SPLIT_FIRST = ("Whatever the hour and whoever holds the pager that week, if the console is "
               "unreachable, phone the duty engineer on 555-0142.")
SPLIT_SECOND = ("Wait for a callback before touching the relay, however long the console "
                "stays dark and whatever the status page says.")

RUN_TOGETHER = ("The duty engineer confirms every restart by phone within ten minutes of the "
                "page from the console and files the restart report with the site office")

# (family, case, kind, {line name: replacement}, target line name, expected
#  verdict, expected step, expected registered verdict or None)
#
# kind:  clear          must not fire: the content is there, must not be absent
#        loss           must fire: a real loss, must be absent
#        limit_kept     a false alarm the rule is known to keep (absent)
#        limit_cleared  a difference the rule is known to clear (reworded)
#
# A value given as a dict differs between the two views.
CASES = [
    # --- Joined with a semicolon -------------------------------------------
    ("joined-semicolon", "kept and joined", "clear",
     {"signs": "The night shift lead signs the restart log before 06:00; the day shift "
               "lead countersigns it after the morning handover and files it with the site office."},
     "signs", REWORDED, STEP_PHRASE, ABSENT),
    ("joined-semicolon", "a clause removed", "loss",
     {"signs": "The night shift lead signs the restart log; the day shift "
               "lead countersigns it after the morning handover and files it with the site office."},
     "signs", ABSENT, STEP_NONE, ABSENT),
    ("joined-semicolon", "the time changed", "loss",
     {"signs": "The night shift lead signs the restart log before 07:00; the day shift "
               "lead countersigns it after the morning handover and files it with the site office."},
     "signs", ABSENT, STEP_NONE, ABSENT),
    ("joined-semicolon", "the name removed", "loss",
     {"signs": "The lead signs the restart log before 06:00; the day shift "
               "lead countersigns it after the morning handover and files it with the site office."},
     "signs", ABSENT, STEP_NONE, ABSENT),
    ("joined-semicolon", "an unrelated sentence of the same vocabulary", "loss",
     {"signs": "The day shift lead reads the restart log after 06:00; the night shift "
               "lead is told at the morning handover and nothing is filed with the site office."},
     "signs", ABSENT, STEP_NONE, ABSENT),

    # --- Joined with a comma and "and", capital lost ------------------------
    ("joined-comma", "kept and joined", "clear",
     {"timeout": "Timeouts are fixed, and the connect timeout is 30 seconds, which the console "
                 "shows on the status page of every relay in the region."},
     "timeout", REWORDED, STEP_PHRASE, ABSENT),
    ("joined-comma", "30 became 3", "loss",
     {"timeout": "Timeouts are fixed, and the connect timeout is 3 seconds, which the console "
                 "shows on the status page of every relay in the region."},
     "timeout", ABSENT, STEP_NONE, ABSENT),
    ("joined-comma", "30 became 300 (a prefix match must not count)", "loss",
     {"timeout": "Timeouts are fixed, and the connect timeout is 300 seconds, which the console "
                 "shows on the status page of every relay in the region."},
     "timeout", ABSENT, STEP_NONE, ABSENT),
    ("joined-comma", "30 became 30.5 (a prefix match must not count)", "loss",
     {"timeout": "Timeouts are fixed, and the connect timeout is 30.5 seconds, which the console "
                 "shows on the status page of every relay in the region."},
     "timeout", ABSENT, STEP_NONE, ABSENT),
    ("joined-comma", "a negation written in front of the kept words", "limit_cleared",
     {"timeout": "It is not the case that the connect timeout is 30 seconds, whatever the status "
                 "page of an older relay in the region may still show."},
     "timeout", REWORDED, STEP_PHRASE, ABSENT),
    ("joined-comma", "another timeout in its place", "loss",
     {"timeout": "Timeouts are fixed, and the read timeout is 30 seconds, which the console "
                 "shows on the status page of every relay in the region."},
     "timeout", ABSENT, STEP_NONE, ABSENT),

    # --- Joined after a colon ----------------------------------------------
    ("joined-colon", "kept and joined", "clear",
     {"donot": "One rule stands above the others: do not restart the relay while a transfer is "
               "running, because a half-written transfer cannot be resumed and has to be sent again."},
     "donot", REWORDED, STEP_PHRASE, ABSENT),
    ("joined-colon", "the negation removed", "loss",
     {"donot": "One rule stands above the others: restart the relay while a transfer is "
               "running, because a half-written transfer cannot be resumed and has to be sent again."},
     "donot", ABSENT, STEP_NONE, ABSENT),
    ("joined-colon", "the condition removed", "loss",
     {"donot": "One rule stands above the others: do not restart the relay, "
               "because a half-written transfer cannot be resumed and has to be sent again."},
     "donot", ABSENT, STEP_NONE, ABSENT),

    # --- One sentence spread over two --------------------------------------
    ("split", "cut in two at 'and', a clean seam, a clause before and one after", "clear",
     {"phone": SPLIT_FIRST + " " + SPLIT_SECOND},
     "phone", REWORDED, STEP_CONTAINMENT, ABSENT),
    ("split", "the second half gone", "loss",
     {"phone": SPLIT_FIRST + " Note the time in the shift log, however long the console "
               "stays dark and whatever the status page says."},
     "phone", ABSENT, STEP_NONE, ABSENT),
    ("split", "the number changed", "loss",
     {"phone": SPLIT_FIRST.replace("555-0142", "555-0199") + " " + SPLIT_SECOND},
     "phone", ABSENT, STEP_NONE, ABSENT),
    ("split", "the condition gone", "loss",
     {"phone": SPLIT_FIRST.replace("if the console is unreachable, phone", "phone")
               + " " + SPLIT_SECOND},
     "phone", ABSENT, STEP_NONE, ABSENT),
    ("split", "the second half replaced by another instruction of the same vocabulary", "loss",
     {"phone": SPLIT_FIRST + " Touch nothing on the relay before the callback, however long "
               "the console stays dark and whatever the status page says."},
     "phone", ABSENT, STEP_NONE, ABSENT),
    ("split", "a negation written at the seam", "loss",
     {"phone": SPLIT_FIRST + " " + SPLIT_SECOND.replace("Wait for", "Do not wait for")},
     "phone", ABSENT, STEP_NONE, ABSENT),
    ("split", "a word written at the seam ('Then')", "limit_kept",
     {"phone": SPLIT_FIRST + " " + SPLIT_SECOND.replace("Wait for", "Then wait for")},
     "phone", ABSENT, STEP_NONE, ABSENT),
    ("split", "the two halves a whole sentence apart", "limit_kept",
     {"phone": SPLIT_FIRST + " The number is on the console lid. " + SPLIT_SECOND},
     "phone", ABSENT, STEP_NONE, ABSENT),

    # --- One sentence turned into a line and a list ------------------------
    ("listed", "every word kept, in order", "clear",
     {"handover": "The handover needs:\n\n- the badge\n- the console key\n"
                  "- and the restart log, signed by the night shift lead\n"},
     "handover", REWORDED, STEP_PHRASE, ABSENT),
    ("listed", "one item gone", "loss",
     {"handover": "The handover needs:\n\n- the badge\n"
                  "- and the restart log, signed by the night shift lead\n"},
     "handover", ABSENT, STEP_NONE, ABSENT),
    ("listed", "the opening made into a heading", "limit_kept",
     {"attempts": "## After two failed attempts\n\nCall the workshop and log the fault code, "
                  "unless the station is one of the four on the harbour loop.\n\n## Handover\n"},
     "attempts", ABSENT, STEP_NONE, ABSENT),

    # --- Cut short: what the similarity ratio already clears ----------------
    # Not the amended rule's doing and not undone by it, because it is
    # additive. Pinned so the inherited weakness is on the record: a sentence
    # that lost its second half reads as reworded under both rules, because
    # the half that is left is more than `NEAR_MATCH` like the whole.
    ("cut-short", "second half gone, nothing added (inherited from the ratio)",
     "limit_cleared",
     {"phone": "If the console is unreachable, phone the duty engineer on 555-0142."},
     "phone", REWORDED, STEP_RATIO, REWORDED),
    ("cut-short", "the deadline gone, nothing added (inherited from the ratio)",
     "limit_cleared",
     {"signs": "The night shift lead signs the restart log."},
     "signs", REWORDED, STEP_RATIO, REWORDED),

    # --- Two sentences run into one, the second one's subject dropped ------
    ("run-together", "first sentence, kept and joined", "clear",
     {"confirms": "", "files": RUN_TOGETHER + " by noon."},
     "confirms", REWORDED, STEP_PHRASE, ABSENT),
    ("run-together", "second sentence, its two-word subject taken from the first", "limit_kept",
     {"confirms": "", "files": RUN_TOGETHER + " by noon."},
     "files", ABSENT, STEP_NONE, ABSENT),
    ("run-together", "second sentence, the deadline gone", "loss",
     {"confirms": "", "files": RUN_TOGETHER + "."},
     "files", ABSENT, STEP_NONE, ABSENT),
    ("run-together", "second sentence, the recipient changed", "loss",
     {"confirms": "", "files": RUN_TOGETHER.replace("the site office", "the night shift lead")
                               + " by noon."},
     "files", ABSENT, STEP_NONE, ABSENT),
    ("run-together", "second sentence gone, first kept long", "loss",
     {"confirms": "", "files": "The duty engineer confirms every restart by phone within ten "
                               "minutes of the page from the console and tells the site office."},
     "files", ABSENT, STEP_NONE, ABSENT),
    ("run-together", "second sentence, its one-word subject taken from the first", "limit_kept",
     {"restart": "", "record": "Operators restart the relay from the console after every "
                               "certificate change and record the restart in the change log "
                               "within one hour."},
     "record", ABSENT, STEP_NONE, ABSENT),

    # --- Words inserted in the middle --------------------------------------
    ("inserted", "connecting words inserted, a clause added after", "clear",
     {"listens": "The relay listens on the port 8443, and it accepts TLS 1.2 or later; the "
                 "firewall opens that port for the two site networks and for nothing else at all."},
     "listens", REWORDED, STEP_CONTAINMENT, ABSENT),
    ("inserted", "connecting words inserted, the version changed", "loss",
     {"listens": "The relay listens on the port 8443, and it accepts TLS 1.3 or later; the "
                 "firewall opens that port for the two site networks and for nothing else at all."},
     "listens", ABSENT, STEP_NONE, ABSENT),
    ("inserted", "a 'not' inserted among the connecting words", "loss",
     {"listens": "The relay listens on the port 8443, and it is not one that accepts TLS 1.2 or "
                 "later; the firewall opens that port for the two site networks and nothing else."},
     "listens", ABSENT, STEP_NONE, ABSENT),
    ("inserted", "one clause inserted", "limit_kept",
     {"listens": "The relay listens on port 8443, which the firewall opens for the two site "
                 "networks and for nothing else, and accepts TLS 1.2 or later."},
     "listens", ABSENT, STEP_NONE, ABSENT),
    ("inserted", "one clause inserted, the version changed", "loss",
     {"listens": "The relay listens on port 8443, which the firewall opens for the two site "
                 "networks and for nothing else, and accepts TLS 1.3 or later."},
     "listens", ABSENT, STEP_NONE, ABSENT),
    ("inserted", "one clause inserted, 'or later' gone", "loss",
     {"listens": "The relay listens on port 8443, which the firewall opens for the two site "
                 "networks and for nothing else, and accepts TLS 1.2."},
     "listens", ABSENT, STEP_NONE, ABSENT),
    ("inserted", "one clause inserted, the port gone", "loss",
     {"listens": "The relay listens on a port which the firewall opens for the two site "
                 "networks and for nothing else, and accepts TLS 1.2 or later."},
     "listens", ABSENT, STEP_NONE, ABSENT),
    ("inserted", "clauses inserted in two places", "limit_kept",
     {"listens": "The relay, deployed once per region, listens on port 8443, which the firewall "
                 "opens for the two site networks and for nothing else, and accepts TLS 1.2 or later."},
     "listens", ABSENT, STEP_NONE, ABSENT),

    # --- A link ------------------------------------------------------------
    ("link", "kept and joined", "clear",
     {"guide": f"Transfers have states of their own; see [the transfer guide]({URL}) for the "
               "list of transfer states, which the console shows as coloured dots beside each transfer."},
     "guide", REWORDED, STEP_PHRASE, ABSENT),
    ("link", "the link gone, its text kept", "loss",
     {"guide": "Transfers have states of their own; see the transfer guide for the "
               "list of transfer states, which the console shows as coloured dots beside each transfer."},
     "guide", ABSENT, STEP_NONE, ABSENT),
    ("link", "the address changed", "loss",
     {"guide": "Transfers have states of their own; see [the transfer guide]"
               "(https://docs.example.test/relay/states) for the "
               "list of transfer states, which the console shows as coloured dots beside each transfer."},
     "guide", ABSENT, STEP_NONE, ABSENT),

    # --- Short segments ----------------------------------------------------
    ("short", "two words, kept and joined", "clear",
     {"call": "Call security; they hold the spare key to the console and the list of duty engineers."},
     "call", REWORDED, STEP_PHRASE, ABSENT),
    ("short", "its two words in two neighbouring sentences", "loss",
     {"call": "Call the front desk. Security holds the spare key to the console."},
     "call", ABSENT, STEP_NONE, ABSENT),
    ("short", "one word, found somewhere", "loss",
     {"none": "- If none of that applies, ask the duty engineer."},
     "none", ABSENT, STEP_NONE, None),
    ("short", "a sentence of connecting words among connecting words", "loss",
     {"same": "It is what it is, and that is the way it was and is to be."},
     "same", ABSENT, STEP_NONE, None),

    # --- A subject from one place, the rest from another -------------------
    ("actor", "kept and joined", "clear",
     {"badge": "Security collects the badge at the exit before the visitor leaves the building "
               "through the staff turnstile on the ground floor."},
     "badge", REWORDED, STEP_PHRASE, ABSENT),
    ("actor", "another actor does it, the one-word subject stands nearby", "loss",
     {"call": "", "badge": "Call security. Reception collects the badge at the exit before the "
                           "visitor leaves the building through the staff turnstile on the ground floor."},
     "badge", ABSENT, STEP_NONE, ABSENT),
    ("actor", "another actor does it, the two-word subject stands nearby", "loss",
     {"desk": "The fault code goes to the support desk. The field crew escalates to the workshop "
              "after three failed attempts, and only once the station has been power-cycled."},
     "desk", ABSENT, STEP_NONE, ABSENT),
    ("actor", "the subject ends one sentence and the rest begins the next", "limit_cleared",
     {"desk": "Whatever the code, the fault goes first to the support desk. Escalates to the "
              "workshop after three failed attempts is what the field crew's own guide says."},
     "desk", REWORDED, STEP_PHRASE, ABSENT),
    ("actor", "another actor does it, and after another number of attempts", "loss",
     {"desk": "The fault code goes to the support desk. The field crew escalates to the workshop "
              "after two failed attempts, and only once the station has been power-cycled."},
     "desk", ABSENT, STEP_NONE, ABSENT),

    # --- Rewordings the rule does not follow -------------------------------
    ("reworded", "clauses in another order", "limit_kept",
     {"attempts": "Call the workshop and log the fault code after two failed attempts, unless the "
                  "station is one of the four on the harbour loop, which the depot handles itself."},
     "attempts", ABSENT, STEP_NONE, ABSENT),
    ("reworded", "an inflection changed, and joined", "limit_kept",
     {"restart": "The operator restarts the relay from the console after every certificate change, "
                 "and the console keeps the last twenty restarts in its history for the auditors."},
     "restart", ABSENT, STEP_NONE, ABSENT),
    ("reworded", "only a connecting word differs (tense)", "limit_cleared",
     {"cutoff": "Under the schedule now in force the cutoff is 15:00 on the 20th, and the "
                "weekend rule moves it to the Friday before."},
     "cutoff", REWORDED, STEP_CONTAINMENT, ABSENT),
    ("reworded", "the time differs as well", "loss",
     {"cutoff": "Under the schedule now in force the cutoff is 12:00 on the 18th, and the "
                "weekend rule moves it to the Friday before."},
     "cutoff", ABSENT, STEP_NONE, ABSENT),

    # --- A fenced block is not words ---------------------------------------
    # The scorer takes backticks off both sides, so to it the block's line is
    # in the merge word for word and is carried, under both rules. The tool
    # keeps the fence and calls it absent, under both rules. Neither changes.
    ("code", "the block's words in a sentence, the block gone", "loss",
     {"block": "Run relayctl restart --grace 30 from the console and wait for the prompt to return."},
     "block", {"tool": ABSENT, "scorer": PRESENT}, {"tool": STEP_NONE, "scorer": STEP_EXACT},
     {"tool": ABSENT, "scorer": PRESENT}),
]

# How many cases of each kind the table above holds. A count, so that a case
# cannot be dropped from the table and leave the suite green and thinner.
CASE_COUNTS = {"clear": 10, "loss": 34, "limit_kept": 9, "limit_cleared": 5}


def merged_with(replacements: dict[str, str]) -> str:
    text = BASE_MERGE
    for name, new in replacements.items():
        old = LINE[name]
        text = text.replace(old + "\n", (new + "\n") if new else "", 1)
    return text


def test_the_base_merge_carries_everything_but_the_second_title() -> None:
    """The floor every synthetic case stands on: one line replaced, nothing else moved."""
    for name, (amended, registered) in both_rules(SOURCES, BASE_MERGE).items():
        for view, rule in ((amended, AMENDED), (registered, REGISTERED)):
            gone = [item.segment.id for item in view if item.verdict != PRESENT]
            check(gone == ["b1"],
                  f"base merge, {name} view, {rule}: only B's title may be missing, got {gone}")


def test_the_synthetic_families_each_case_with_its_siblings() -> None:
    """A join, a split, a list, a link, a short item: cleared, and its losses kept."""
    seen = {kind: 0 for kind in CASE_COUNTS}
    for family, case, kind, replacements, target, verdicts, steps, olds in CASES:
        merged = merged_with(replacements)
        label = f"{family}: {case}"
        for name, (amended, registered) in both_rules(SOURCES, merged).items():
            verdict, step, old = (value[name] if isinstance(value, dict) else value
                                  for value in (verdicts, steps, olds))
            item = find(amended, LINE[target].removeprefix("- "))
            check(item.verdict == verdict,
                  f"{label} [{kind}, {name} view]: expected {verdict}, got {item.verdict} "
                  f"by {item.step} (ratio {item.ratio:.2f}, window {item.window})")
            check(item.step == step,
                  f"{label} [{name} view]: expected step {step}, got {item.step}")
            before = find(registered, LINE[target].removeprefix("- "))
            if old is not None:
                check(before.verdict == old,
                      f"{label} [{name} view]: the case is built to be {old} under the "
                      f"registered rule and is {before.verdict} at ratio {before.ratio:.2f}")
            if kind == "clear":
                check(item.verdict != ABSENT, f"{label} [{name} view]: MUST NOT FIRE")
            if kind == "loss" and verdict == ABSENT:
                check(item.verdict == ABSENT, f"{label} [{name} view]: MUST FIRE")
            # A segment a run step cleared says where its words were found.
            if item.step in reconcile.RUN_STEPS:
                check(bool(item.window) and bool(item.window_text),
                      f"{label} [{name} view]: cleared with no merge text to show")
                normalise = ((lambda t: rank_matrix.inline_plain(reconcile.flatten(t)))
                             if name == "scorer" else reconcile.flatten)
                wanted = reconcile.words(normalise(item.segment.text))
                if item.step == STEP_CONTAINMENT:
                    wanted = reconcile.content_words(wanted)
                    there = reconcile.content_words(reconcile.words(item.window_text))
                else:
                    there = reconcile.words(item.window_text)
                check(reconcile._run_at(wanted, there) >= 0,
                      f"{label} [{name} view]: the words are not one run of the merge text "
                      f"the verdict names: {item.window_text!r}")
            else:
                check(not item.window and not item.window_text,
                      f"{label} [{name} view]: a window is recorded for step {item.step}")
            # Only the replaced lines may differ from the base merge.
            touched = {reconcile.flatten(LINE[n].removeprefix("- ")) for n in replacements}
            strays = [other.segment.id for other in amended
                      if other.verdict != PRESENT and other.segment.id != "b1"
                      and reconcile.flatten(other.segment.text) not in touched]
            check(not strays, f"{label} [{name} view]: segments outside the replaced line(s) "
                              f"changed: {strays}")
        seen[kind] += 1
        counts[{"clear": "must_not_fire", "loss": "must_fire"}.get(kind, kind)] += 1
    check(seen == CASE_COUNTS,
          f"the table holds {seen}; {CASE_COUNTS} are registered. A case that left the table "
          f"must be taken out of the count by hand, with its reason")


def test_the_tokeniser_never_makes_a_word_less_specific() -> None:
    """`5` is not in `5.5`, `30` is not in `300`, and a link is its text then its address."""
    cut = reconcile.words
    check(cut("The limit is 5.") == ["the", "limit", "is", "5"], f"{cut('The limit is 5.')}")
    check(cut("5.5, 30-33; -70 (2,000,000)") == ["5.5", "30-33", "-70", "2,000,000"],
          f"values must stay whole: {cut('5.5, 30-33; -70 (2,000,000)')}")
    check(cut("`wide_text` and channel.id, the visitor's") ==
          ["wide_text", "and", "channel.id", "the", "visitor's"],
          f"identifiers must stay whole: {cut('`wide_text` and channel.id')}")
    check(cut(f"see [the guide]({URL}).") == ["see", "the", "guide", URL],
          f"a link is its text followed by its address: {cut(f'see [the guide]({URL}).')}")
    check(cut("--- ... !") == [], "a piece with no letter and no digit is not a word")
    for short, long in (("The limit is 5.", "The limit is 50 seconds."),
                        ("The limit is 5.", "The limit is 5.5 seconds.")):
        check(reconcile._run_at(cut(short), cut(long)) < 0,
              f"{short!r} must not be found in {long!r}")
    check(reconcile.content_words(cut("It is the same as it was.")) == ["same", "as"],
          "the connecting words are the listed ones and no others")
    # The list is closed, and what is not in it is the point of it.
    for word in ("not", "no", "never", "only", "if", "unless", "or", "but", "so", "then",
                 "also", "before", "after", "must", "may", "can", "of", "in", "two"):
        check(word not in reconcile.FREE_WORDS,
              f"{word!r} can carry a negation, a condition, an obligation, a place or a "
              f"quantity and must not be a free word")
    check(len(reconcile.FREE_WORDS) == 21, f"21 free words, got {len(reconcile.FREE_WORDS)}")
    check((reconcile.PHRASE_MIN_WORDS, reconcile.CONTAINMENT_MIN_CONTENT_WORDS,
           reconcile.WINDOW) == (2, 4, 2),
          "a constant of the amended rule moved; every one of them was fixed before the rule "
          "was run on a benchmark cell, and moving one is a new rule")


def test_one_step_either_side_of_the_two_floors_and_the_window() -> None:
    """The constants as behaviour: what each one refuses, beside what it admits.

    The pin on their values above says a constant moved. These say what moving
    it would have done, each as a pair that varies one thing.
    """
    filler = ", for the whole of last year and on every site the team runs today."

    def verdict_of(source_line: str, merge_line: str) -> dict[str, tuple[str, str]]:
        documents = {"source_a.md": f"# Env\n\n{source_line}\n",
                     "source_b.md": "# Env\n\nNothing else is recorded here.\n"}
        merged = f"# Env\n\n{merge_line}\nNothing else is recorded here.\n"
        out = {}
        for name, (amended, registered) in both_rules(documents, merged).items():
            item = find(amended, source_line)
            check(find(registered, source_line).verdict == ABSENT,
                  f"{source_line!r}, {name}: built to be absent under the registered rule")
            out[name] = (item.verdict, item.step)
        return out

    # The containment step does not run below four content words. Three:
    # `platform`, `nimbrel`, `cloud`, with a connecting word changed and one
    # added, stays absent. Four, the same line with one more content word, is
    # found. Below four a segment is cleared only whole, by the phrase step.
    three = verdict_of("The platform is Nimbrel Cloud.",
                       "Our platform was the Nimbrel Cloud" + filler)
    four = verdict_of("The build platform is Nimbrel Cloud.",
                      "Our build platform was the Nimbrel Cloud" + filler)
    for name in VIEWS:
        check(three[name] == (ABSENT, STEP_NONE),
              f"three content words, {name}: MUST FIRE, the containment step must not "
              f"run, got {three[name]}")
        check(four[name] == (REWORDED, STEP_CONTAINMENT),
              f"four content words, {name}: found by containment, got {four[name]}")
    counts["must_fire"] += 1
    counts["limit_cleared"] += 1    # tense is the one free word that can carry a fact

    # The window is two merge segments. A sentence cut once is found across
    # the cut; the same sentence cut twice, into three merge sentences with
    # clean seams, is not: its run would have to pass through a whole segment.
    whole = ("If the console is unreachable, phone the duty engineer on 555-0142 and wait "
             "for a callback before touching the relay.")
    once = verdict_of(whole, SPLIT_FIRST + " " + SPLIT_SECOND)
    twice = verdict_of(whole, SPLIT_FIRST.replace("unreachable, phone", "unreachable. Phone")
                       + " " + SPLIT_SECOND)
    for name in VIEWS:
        check(once[name] == (REWORDED, STEP_CONTAINMENT),
              f"cut once, {name}: found across the cut, got {once[name]}")
        check(twice[name] == (ABSENT, STEP_NONE),
              f"cut twice, {name}: a known false alarm the window keeps, got {twice[name]}")
    counts["must_not_fire"] += 1
    counts["limit_kept"] += 1


def test_a_run_that_fits_one_merge_segment_names_that_segment_alone() -> None:
    """Where the words were found is the smallest place they were found in.

    The containment step reads windows of one and of two merge segments, and a
    run that lies wholly in one segment is also a run of that segment together
    with the one before it. A reader shown both would be shown an unrelated
    sentence as part of the evidence. So the one-segment windows are asked
    first. The verdict does not depend on the order; the text shown does.
    The sibling is the sentence that really is spread over two: it names two.
    """
    tense = ("Under the schedule now in force the cutoff is 15:00 on the 20th, and the "
             "weekend rule moves it to the Friday before.")
    for name, (amended, _) in both_rules(SOURCES, merged_with({"cutoff": tense})).items():
        item = find(amended, LINE["cutoff"])
        check(item.step == STEP_CONTAINMENT and len(item.window) == 1
              and item.window_text == tense,
              f"one segment, {name}: the window is the one sentence the words stand in, "
              f"got {item.window}: {item.window_text!r}")
    split = merged_with({"phone": SPLIT_FIRST + " " + SPLIT_SECOND})
    for name, (amended, _) in both_rules(SOURCES, split).items():
        item = find(amended, LINE["phone"])
        check(item.step == STEP_CONTAINMENT and len(item.window) == 2
              and item.window_text == SPLIT_FIRST + " " + SPLIT_SECOND,
              f"two segments, {name}: a sentence cut once names both halves, got "
              f"{item.window}: {item.window_text!r}")


def test_a_rule_must_be_named_and_known() -> None:
    """`locate` has no default rule, and an unknown one is refused, not guessed."""
    document = segment.segment_document(SOURCE_A, "a", "source_a.md")
    merged = segment.segment_document(BASE_MERGE, reconcile.MERGE_LETTER).segments
    flat = reconcile.flatten(BASE_MERGE)
    try:
        reconcile.locate(document, flat, merged)
        check(False, "locate() without a rule must be a TypeError")
    except TypeError:
        pass
    for call in (lambda: reconcile.locate(document, flat, merged, rule="strict"),
                 lambda: reconcile.reconcile(SOURCES, BASE_MERGE, rule="strict")):
        try:
            call()
            check(False, "an unknown rule must be refused")
        except ValueError:
            pass
    check(reconcile.reconcile(SOURCES, BASE_MERGE).rule == AMENDED,
          "the tool's own rule is the amended one")
    check(reconcile.RULES == (REGISTERED, AMENDED), f"two rules, got {reconcile.RULES}")


# --------------------------------------------------------------------------
# Headings
# --------------------------------------------------------------------------

SECTION = [name for name in LINE if LINE[name] in SOURCE_B and name != "heading"]


def test_an_untaken_heading_over_a_section_that_survived_is_not_lost_content() -> None:
    """MUST NOT FIRE as a loss: the label was not taken, everything under it was."""
    merged = merged_with({"heading": ""})
    for name, (amended, registered) in both_rules(SOURCES, merged).items():
        item = find(amended, "Night shift")
        check(item.verdict == ABSENT and item.step == STEP_NONE,
              f"untaken heading, {name}: the verdict itself does not change, got "
              f"{item.verdict}/{item.step}")
        check(len(item.section) == len(SECTION),
              f"untaken heading, {name}: its section is every B segment under it, got "
              f"{item.section}")
        check(silent_registered(registered) == [item.segment.id],
              f"untaken heading, {name}: the registered scoring counts it as silent loss")
        check(silent(amended) == [], f"untaken heading, {name}: the amended scoring must not")
        check(untaken(amended) == [item.segment.id],
              f"untaken heading, {name}: it is still reported, as an untaken heading")
        title = find(amended, "Relay Notes")
        check(title.verdict == ABSENT and title.segment.id not in silent(amended)
              and title.segment.id not in untaken(amended),
              f"title, {name}: a title is left to the title checks under both rules")
    counts["must_not_fire"] += 1


def test_a_heading_whose_whole_section_is_gone_stays_lost_content() -> None:
    """MUST FIRE: the sibling. The section went with the heading, so both are lost."""
    merged = merged_with({name: "" for name in SECTION + ["heading"]})
    for name, (amended, registered) in both_rules(SOURCES, merged).items():
        item = find(amended, "Night shift")
        new = silent(amended)
        check(item.segment.id in new,
              f"heading with its section gone, {name}: must stay a loss, got {new}")
        check(sorted(new) == sorted(silent_registered(registered)),
              f"heading with its section gone, {name}: the amended count is the registered one")
        check(untaken(amended) == [],
              f"heading with its section gone, {name}: nothing is refiled")
    counts["must_fire"] += 1


def test_one_surviving_sentence_makes_the_heading_a_record_matter() -> None:
    """MUST NOT FIRE on the heading; every sentence that is gone is still a loss."""
    merged = merged_with({name: "" for name in SECTION + ["heading"] if name != "donot"})
    for name, (amended, registered) in both_rules(SOURCES, merged).items():
        item = find(amended, "Night shift")
        new, old = silent(amended), silent_registered(registered)
        check(item.segment.id not in new and sorted(new + [item.segment.id]) == sorted(old),
              f"heading with one sentence left, {name}: only the heading leaves the count, "
              f"registered {old}, amended {new}")
        check(untaken(amended) == [item.segment.id],
              f"heading with one sentence left, {name}: the heading is the record matter")
    counts["must_not_fire"] += 1


def test_a_section_accounted_for_by_records_makes_the_heading_a_record_matter() -> None:
    """The section is gone as text and every line of it has a record."""
    merged = merged_with({name: "" for name in SECTION + ["heading"]})
    for name, (amended, _) in both_rules(SOURCES, merged).items():
        item = find(amended, "Night shift")
        declared = set(item.section)
        check(silent(amended, declared) == [],
              f"heading over a declared section, {name}: nothing is silent, got "
              f"{silent(amended, declared)}")
        check(untaken(amended, declared) == [item.segment.id],
              f"heading over a declared section, {name}: the heading is the record matter")
        own = declared | {item.segment.id}
        check(silent(amended, own) == [] and untaken(amended, own) == [],
              f"heading over a declared section, {name}: with its own record it is nothing")
        # The sibling that must fire: one line of the section left without a
        # record is one silent loss, and the heading is still not one.
        one_short = declared - {item.section[0]}
        check(silent(amended, one_short) == [item.section[0]],
              f"heading over a section declared but for one line, {name}: that line is "
              f"the loss, got {silent(amended, one_short)}")
    counts["must_not_fire"] += 1
    counts["must_fire"] += 1


def test_a_heading_that_carries_a_value_the_merge_lost_stays_lost_content() -> None:
    """`## From release 4.6 onward`: a record matter while the merge says 4.6, a loss when it does not."""
    a = "# Ledger Guide\n\nBatches are refused when the queue is full.\n"
    b = ("# Ledger Notes\n\n## From release 4.6 onward\n\n"
         "A batch that would exhaust the node is refused on its own account.\n")
    kept_elsewhere = ("# Ledger Guide\n\nBatches are refused when the queue is full.\n\n"
                      "A batch that would exhaust the node is refused on its own account. "
                      "This applies from release 4.6.\n")
    lost = ("# Ledger Guide\n\nBatches are refused when the queue is full.\n\n"
            "A batch that would exhaust the node is refused on its own account.\n")
    documents = {"source_a.md": a, "source_b.md": b}
    for name, (amended, _) in both_rules(documents, kept_elsewhere).items():
        item = find(amended, "From release 4.6 onward")
        check(item.verdict == ABSENT and item.protected_missing == ()
              and silent(amended) == [] and untaken(amended) == [item.segment.id],
              f"heading with a value the merge still states, {name}: a heading matter, got "
              f"{item.verdict}, missing {item.protected_missing}, silent {silent(amended)}")
    counts["must_not_fire"] += 1
    for name, (amended, _) in both_rules(documents, lost).items():
        item = find(amended, "From release 4.6 onward")
        check(item.verdict == ABSENT and silent(amended) == [item.segment.id]
              and untaken(amended) == [],
              f"heading whose value the merge lost, {name}: must stay a loss, got "
              f"silent {silent(amended)}")
        check(item.protected_missing == ("4.6",),
              f"heading whose value the merge lost, {name}: the reason must name 4.6, got "
              f"{item.protected_missing}")
    counts["must_fire"] += 1


def test_a_near_twin_under_a_lost_heading_files_it_as_a_record_matter() -> None:
    """A known limit, inherited from the ratio and pinned so it cannot grow unseen.

    Source B's one section is `## Timeouts` over a single sentence, and the
    merge has neither. But the merge has source A's `The connect timeout is 30
    seconds.`, which is 0.80 like B's `The read timeout is 45 seconds.`, so
    the ratio calls B's sentence reworded when it is gone (the registered
    near twin). The section therefore does not read as lost as a whole, and
    the heading is filed as an untaken heading although nothing under it
    survived. Nothing is hidden by it: the sentence is still reported as
    reworded and undeclared, a document finding, and check 5 reports the 45
    that did not survive. What it costs is the heading's own filing.

    The sibling: with A's twin out of the merge too, the sentence is absent,
    the section is lost as a whole and the heading is lost content again.
    """
    a = "# Relay Handbook\n\nThe relay listens on port 8443.\nThe connect timeout is 30 seconds.\n"
    b = "# Relay Handbook\n\n## Timeouts\n\nThe read timeout is 45 seconds.\n"
    documents = {"source_a.md": a, "source_b.md": b}
    for name, (amended, _) in both_rules(documents, a).items():
        sentence = find(amended, "The read timeout is 45 seconds.")
        check((sentence.verdict, sentence.step) == (REWORDED, STEP_RATIO),
              f"near twin under a heading, {name}: the ratio misfiles the sentence, got "
              f"{sentence.verdict}/{sentence.step}")
        check(untaken(amended) == ["b2"] and silent(amended) == [],
              f"near twin under a heading, {name}: the heading is filed as untaken, got "
              f"untaken {untaken(amended)}, silent {silent(amended)}")
    got = found_in(documents, a)
    check(sorted(kinds_of(got)) == sorted([
              (reconcile.UNDECLARED_REWORDING, "b3"), (reconcile.HEADING_NOT_DECLARED, "b2"),
              (reconcile.VERBATIM_VIOLATION, "b3")]),
          f"near twin under a heading: the tool still reports the sentence and the value, "
          f"got {kinds_of(got)}")
    counts["limit_cleared"] += 1

    without_twin = a.replace("The connect timeout is 30 seconds.\n", "")
    for name, (amended, _) in both_rules(documents, without_twin).items():
        check(sorted(silent(amended)) == ["a3", "b2", "b3"] and untaken(amended) == [],
              f"no twin, {name}: the heading is lost with its section, got silent "
              f"{silent(amended)}, untaken {untaken(amended)}")
    counts["must_fire"] += 1


def test_a_headings_words_in_a_sentence_are_still_not_the_heading() -> None:
    """MUST FIRE: the run steps are for content, and a heading names a place."""
    a = "# Runbook\n\nThe relay listens on port 8443.\n"
    b = "# Runbook\n\n## Peak window limits apply\n\nConcurrency is capped during peak windows.\n"
    merged = ("# Runbook\n\nThe relay listens on port 8443.\n\n"
              "Note that peak window limits apply here, and concurrency is capped during peak "
              "windows; nothing else changes.\n")
    for name, (amended, _) in both_rules({"source_a.md": a, "source_b.md": b}, merged).items():
        item = find(amended, "Peak window limits apply")
        check(item.verdict == ABSENT and item.step == STEP_NONE,
              f"heading words in a sentence, {name}: a heading does not go through the "
              f"phrase step, got {item.verdict}/{item.step}")
    counts["must_fire"] += 1


def test_a_section_runs_to_the_next_heading_of_its_level_or_above() -> None:
    """And holds what stands under its sub-headings, but not the sub-headings."""
    nested = ("# T\n\n## One\n\nFirst body line here.\n\n### One A\n\nSecond body line here.\n\n"
              "## Two\n\nThird body line here.\n")
    document = segment.segment_document(nested, "a", "source_a.md")
    merged = segment.segment_document("# T\n", reconcile.MERGE_LETTER).segments
    view = reconcile.locate(document, reconcile.flatten("# T\n"), merged, rule=AMENDED).located
    sections = {item.segment.text: item.section for item in view
                if item.segment.kind == segment.HEADING}
    check(sections == {"One": ("a3", "a5"), "One A": ("a5",), "Two": ("a7",)},
          f"sections: got {sections}")
    registered = reconcile.locate(document, reconcile.flatten("# T\n"), merged,
                                  rule=REGISTERED).located
    check(all(item.section == () for item in registered),
          "the registered rule knows no sections")


# --------------------------------------------------------------------------
# The repository's own small cases, unchanged in outcome
# --------------------------------------------------------------------------

def test_the_small_cases_of_the_reconciler_suite_keep_their_outcome() -> None:
    """Two absences, a small rewording, the near twin, a folded list, the fan-in six."""
    a = "# Relay Handbook\n\nThe relay listens on port 8443.\nThe connect timeout is 30 seconds.\n"
    b = "# Relay Notes\n\nThe relay listens on port 8443.\nThe read timeout is 45 seconds.\n"
    pair = {"source_a.md": a, "source_b.md": b}
    clean = ("# Relay Handbook\n\nThe relay listens on port 8443.\n"
             "The connect timeout is 30 seconds.\nThe read timeout is 45 seconds.\n")

    neither = clean.replace("The connect timeout is 30 seconds.\n", "").replace(
        "The read timeout is 45 seconds.\n", "")
    for name, (amended, _) in both_rules(pair, neither).items():
        check(sorted(silent(amended)) == ["a3", "b3"],
              f"both timeouts removed, {name}: got {sorted(silent(amended))}")
    counts["must_fire"] += 1

    reworded = clean.replace("The connect timeout is 30 seconds.",
                             "The connect timeout is set to 30 seconds.")
    for name, (amended, registered) in both_rules(pair, reworded).items():
        item = find(amended, "The connect timeout is 30 seconds.")
        check((item.verdict, item.step) == (REWORDED, STEP_RATIO)
              and find(registered, "The connect timeout is 30 seconds.").verdict == REWORDED,
              f"small rewording, {name}: got {item.verdict}/{item.step}")
    counts["must_not_fire"] += 1

    # The registered near twin: reworded under both rules, by the ratio. The
    # amended rule is additive, so it inherits this misfiling and says which
    # step made it.
    one_gone = clean.replace("The connect timeout is 30 seconds.\n", "")
    for name, (amended, _) in both_rules(pair, one_gone).items():
        item = find(amended, "The connect timeout is 30 seconds.")
        check((item.verdict, item.step) == (REWORDED, STEP_RATIO),
              f"near twin, {name}: the amended rule is additive, got {item.verdict}/{item.step}")
    counts["limit_cleared"] += 1

    a = "# Env\n\nSomething else entirely.\n"
    b = "# Env\n\n- Product: Ledger\n- Version: 4.4\n- Platform: Cloud\n"
    merged = "# Env\n\nSomething else entirely.\n\nProduct: Ledger, Version: 4.4, Platform: Cloud\n"
    for name, (amended, _) in both_rules({"source_a.md": a, "source_b.md": b}, merged).items():
        check(all(item.verdict == PRESENT for item in amended),
              f"folded list, {name}: {[(i.segment.id, i.verdict) for i in amended]}")
    counts["must_not_fire"] += 1

    a = ("# Release notes\n\nThe scheduler now retries failed jobs before giving up.\n"
         "Operators may pause a queue without draining it.\n"
         "Audit entries record who approved each override.\n")
    b = ("# Release notes\n\nSupport for read-only replicas has been withdrawn.\n"
         "The archive tier no longer accepts new writes.\n"
         "Nightly compaction runs during the maintenance window.\n")
    merged = ("# Release notes\n\nThis release changes scheduling, queues, auditing, "
              "replicas, archiving and compaction.\n")
    for name, (amended, _) in both_rules({"source_a.md": a, "source_b.md": b}, merged).items():
        check(sorted(silent(amended)) == ["a2", "a3", "a4", "b2", "b3", "b4"],
              f"six segments against one summary sentence, {name}: got {sorted(silent(amended))}")
    counts["must_fire"] += 1


# --------------------------------------------------------------------------
# What a user sees: checks 2, 3 and 6a under the amended rule
# --------------------------------------------------------------------------

def found_in(documents: dict[str, str], merged: str, records: tuple[dict, ...] = (), *,
             rule: str = AMENDED, fidelity: str = "high") -> reconcile.Reconciled:
    return reconcile.findings(
        reconcile.reconcile(documents, merged, rule=rule), records, fidelity=fidelity,
        title_policy="keep-base", base="source_a.md",
        budget=config.DEFAULT_DECLARED_LOSS_BUDGET)


def kinds_of(result: reconcile.Reconciled) -> list[tuple[str, str]]:
    return [(item.kind, item.segment) for item in result.findings]


TITLE_RECORD = ({"segment": "b1", "disposition": "superseded",
                 "replacement": "Relay Handbook", "reason": "A's title was kept"},)


def test_check_2_says_how_a_joined_sentence_was_found_and_not_a_ratio() -> None:
    """A segment a run step cleared is "reworded and undeclared", explained by where it stands.

    Its similarity is below the threshold by construction, so a sentence that
    printed the ratio as the reason would contradict the verdict. The sibling
    is the same line with its time changed: absent, and explained as before.
    """
    joined = merged_with({"signs": "The night shift lead signs the restart log before 06:00; "
                                   "the day shift lead countersigns it after the morning "
                                   "handover and files it with the site office."})
    got = found_in(SOURCES, joined, TITLE_RECORD)
    target = find(tool_view(SOURCES, joined, AMENDED), LINE["signs"])
    check(kinds_of(got) == [(reconcile.UNDECLARED_REWORDING, target.segment.id)],
          f"a joined sentence with no record is reworded and undeclared, got {kinds_of(got)}")
    finding = got.findings[0]
    check("reworded in the merge" in finding.detail and "not in the merge" not in finding.detail,
          f"the detail must say the text is there: {finding.detail!r}")
    check("one unbroken run" in finding.detail and " at 0." not in finding.detail
          and "nearest merge segment" not in finding.detail,
          f"a segment found as a run must not be explained by a similarity score: "
          f"{finding.detail!r}")
    check(all(identifier in finding.detail for identifier in target.window),
          f"the detail names the merge segment(s) the run stands in: {finding.detail!r}")
    check(finding.merge_text == target.window_text
          and "signs the restart log before 06:00; the day shift" in finding.merge_text,
          f"the merge text shown is the text the run was found in: {finding.merge_text!r}")
    check(finding.source_text == LINE["signs"], "and the source text is the segment's own")
    check(reconcile.DOCUMENT_FINDINGS >= {finding.kind}, "it is still a document finding")

    # Under the registered rule the same merge reads as a loss, with the ratio.
    before = found_in(SOURCES, joined, TITLE_RECORD, rule=REGISTERED)
    check(kinds_of(before) == [(reconcile.UNDECLARED_ABSENCE, target.segment.id)]
          and "nearest merge segment" in before.findings[0].detail,
          f"the registered rule calls the joined sentence absent, got {kinds_of(before)}")

    # The sibling that must stay a loss, worded as a loss always was. Check 5
    # reports the time that did not survive beside it, as it would have before.
    changed = found_in(SOURCES, joined.replace("before 06:00;", "before 07:00;"), TITLE_RECORD)
    check(kinds_of(changed) == [(reconcile.UNDECLARED_ABSENCE, target.segment.id),
                                (reconcile.VERBATIM_VIOLATION, target.segment.id)]
          and "not in the merge" in changed.findings[0].detail
          and "nearest merge segment" in changed.findings[0].detail
          and changed.findings[0].merge_text == "",
          f"the same line with its time changed is absent: {kinds_of(changed)}")

    # A sentence split cleanly in two: the containment step, both segments named.
    split = found_in(SOURCES, merged_with({"phone": SPLIT_FIRST + " " + SPLIT_SECOND}),
                     TITLE_RECORD)
    check([kind for kind, _ in kinds_of(split)] == [reconcile.UNDECLARED_REWORDING],
          f"a cleanly split sentence is reworded and undeclared, got {kinds_of(split)}")
    detail = split.findings[0].detail
    check("connecting words aside" in detail and " at 0." not in detail,
          f"the containment step says what it allowed: {detail!r}")
    check(split.findings[0].merge_text == SPLIT_FIRST + " " + SPLIT_SECOND,
          f"both merge sentences are shown: {split.findings[0].merge_text!r}")

    # A rewording the ratio found keeps its sentence, score included.
    small = found_in(SOURCES, merged_with({"timeout": "The connect timeout is set to 30 seconds."}),
                     TITLE_RECORD)
    check("nearest merge segment" in small.findings[0].detail
          and "one unbroken run" not in small.findings[0].detail,
          f"a rewording found by similarity is explained by it: {small.findings[0].detail!r}")


CHECK3_A = ("# Gate Notes\n\nThe gate opens at 06:00 for deliveries.\n"
            "Drivers sign in at the lodge before unloading.\n")
CHECK3_B = "# Gate Notes\n\nThe yard closes at 18:00 on weekdays.\n"
CHECK3_JOINED = ("# Gate Notes\n\nThe gate opens at 06:00 for deliveries; nothing is accepted "
                 "before that hour, whoever is on the lodge and whatever the carrier says.\n"
                 "Drivers sign in at the lodge before unloading.\n"
                 "The yard closes at 18:00 on weekdays.\n")
CHECK3_SOURCES = {"source_a.md": CHECK3_A, "source_b.md": CHECK3_B}


def test_check_3_a_blank_replacement_over_a_segment_the_merge_still_has() -> None:
    """A record with no replacement over a joined sentence is no longer a loss.

    Check 3 treats a `reworded` record that names no replacement as an
    undeclared drop when the segment is absent. Under the registered rule a
    joined sentence is absent, so this merge draws "Absent and undeclared" and
    exits 1. Under the amended rule the sentence is found, nothing is lost,
    and the merge is clean. The sibling, with the hour changed, is absent
    under both and keeps the finding.
    """
    record = ({"segment": "a2", "disposition": "reworded", "replacement": "",
               "reason": "joined to the sentence after it"},)
    registered = found_in(CHECK3_SOURCES, CHECK3_JOINED, record, rule=REGISTERED)
    check(kinds_of(registered) == [(reconcile.UNDECLARED_ABSENCE, "a2")],
          f"registered: a blank replacement over an absent segment is a drop, got "
          f"{kinds_of(registered)}")
    amended = found_in(CHECK3_SOURCES, CHECK3_JOINED, record)
    check(kinds_of(amended) == [],
          f"amended: the sentence is in the merge, so nothing is lost and nothing is "
          f"reported, got {kinds_of(amended)}")
    lost = found_in(CHECK3_SOURCES, CHECK3_JOINED.replace("06:00", "07:00"), record)
    check((reconcile.UNDECLARED_ABSENCE, "a2") in kinds_of(lost),
          f"MUST FIRE: the same record over a sentence whose hour changed, got {kinds_of(lost)}")


FAN_A = ("# Depot Rules\n\n"
         "Forklifts are checked before the first shift.\n"
         "Pallets are wrapped before they leave the bay.\n"
         "Spills are reported to the shift lead at once.\n"
         "Visitors wear a vest on the yard floor.\n")
FAN_B = "# Depot Rules\n\nThe depot follows the rules below without exception.\n"
FAN_SUMMARY = "The depot follows the rules below without exception."
# All four of A's rules gone but for the summary sentence.
FAN_GONE = "# Depot Rules\n\n" + FAN_SUMMARY + "\n"
# The same, with the fourth rule kept and joined to a long clause.
FAN_ONE_KEPT = ("# Depot Rules\n\n" + FAN_SUMMARY + "\n"
                "Visitors wear a vest on the yard floor; the lodge hands them out and takes "
                "them back at the gate, and nobody walks past the barrier without one.\n")
FAN_SOURCES = {"source_a.md": FAN_A, "source_b.md": FAN_B}
FAN_RECORDS = tuple({"segment": identifier, "disposition": "subsumed",
                     "replacement": FAN_SUMMARY, "reason": "covered by the summary"}
                    for identifier in ("a2", "a3", "a4", "a5"))


def test_check_6a_the_fan_in_counts_only_what_is_really_gone() -> None:
    """Four absent segments behind one replacement are over the ceiling of three; three are not.

    MUST FIRE under both rules: all four rules gone. Then the fourth is kept
    and joined to its neighbour. The registered rule still calls it absent and
    still counts four; the amended rule finds it, counts three, and the
    over-budget finding is gone. It was this merge's only finding, so the run
    that exited 1 exits 0: the `subsumed` record over the kept sentence is a
    record over a segment that is reworded, which no check objects to.
    """
    for rule in (REGISTERED, AMENDED):
        gone = found_in(FAN_SOURCES, FAN_GONE, FAN_RECORDS, rule=rule)
        check([kind for kind, _ in kinds_of(gone)] == [reconcile.DECLARED_LOSS_OVER_BUDGET],
              f"{rule}: MUST FIRE, four absent segments behind one replacement, got "
              f"{kinds_of(gone)}")
    registered = found_in(FAN_SOURCES, FAN_ONE_KEPT, FAN_RECORDS, rule=REGISTERED)
    check([kind for kind, _ in kinds_of(registered)] == [reconcile.DECLARED_LOSS_OVER_BUDGET],
          f"registered: the joined rule still reads as absent and the count stays four, got "
          f"{kinds_of(registered)}")
    amended = found_in(FAN_SOURCES, FAN_ONE_KEPT, FAN_RECORDS)
    check(kinds_of(amended) == [],
          f"amended: the fourth rule is in the merge, three absent segments are at the "
          f"ceiling and not over it, got {kinds_of(amended)}")


def test_an_untaken_heading_is_its_own_finding_in_the_record_family() -> None:
    """"Heading dropped in silence": exit 3 where the same merge exited 1.

    The merge took every sentence of source B and not its heading, and wrote
    no record for the heading. Under the registered rule that is "Absent and
    undeclared" (a document finding). Under the amended rule it is a record
    finding of its own. The siblings: with the section gone too it is lost
    content again, and with a record of any kind it is no finding at all.
    """
    merged = merged_with({"heading": ""})
    heading = find(tool_view(SOURCES, merged, AMENDED), "Night shift").segment.id
    amended = found_in(SOURCES, merged, TITLE_RECORD)
    check(kinds_of(amended) == [(reconcile.HEADING_NOT_DECLARED, heading)],
          f"an untaken, undeclared heading over a kept section, got {kinds_of(amended)}")
    finding = amended.findings[0]
    check(finding.kind in reconcile.RECORD_FINDINGS
          and finding.kind not in reconcile.DOCUMENT_FINDINGS,
          "the heading finding is a record finding")
    check("Night shift" in finding.detail and "no disposition record" in finding.detail,
          f"the detail names the heading and the missing record: {finding.detail!r}")
    check(finding.source_text == "Night shift" and finding.merge_text == ""
          and finding.document == "source_b.md",
          f"the row carries the heading and no merge side: {finding}")
    registered = found_in(SOURCES, merged, TITLE_RECORD, rule=REGISTERED)
    check(kinds_of(registered) == [(reconcile.UNDECLARED_ABSENCE, heading)],
          f"the registered rule files it as lost content, got {kinds_of(registered)}")

    # MUST FIRE as lost content: the section is gone with the heading.
    section_gone = merged_with({name: "" for name in SECTION + ["heading"]})
    lost = found_in(SOURCES, section_gone, TITLE_RECORD)
    check((reconcile.UNDECLARED_ABSENCE, heading) in kinds_of(lost)
          and not any(kind == reconcile.HEADING_NOT_DECLARED for kind, _ in kinds_of(lost)),
          f"a heading whose whole section is gone is lost content, got {kinds_of(lost)}")

    # MUST NOT FIRE at all: any record on the heading silences check 2.
    owned = found_in(SOURCES, merged, TITLE_RECORD + (
        {"segment": heading, "disposition": "subsumed", "replacement": LINE["signs"],
         "reason": "the merge has one flat section"},))
    check(kinds_of(owned) == [], f"a declared heading is no finding, got {kinds_of(owned)}")

    # A title is not a heading: an untaken, undeclared title is reported as it
    # always was, by check 2 and by the title check, under both rules.
    for rule in (REGISTERED, AMENDED):
        untitled = found_in(SOURCES, BASE_MERGE, (), rule=rule)
        check(sorted(kinds_of(untitled)) == sorted([
                  (reconcile.UNDECLARED_ABSENCE, "b1"),
                  (reconcile.TITLE_NOT_SUPERSEDED, "b1")]),
              f"{rule}: an untaken title keeps both of its findings, got {kinds_of(untitled)}")


# --------------------------------------------------------------------------
# Controls on the nine pairs
# --------------------------------------------------------------------------

def pair_merges(pair: str, reference: str = rank_matrix.CURRENT) -> dict[str, str]:
    """reference, concatenation, union and base_only for one pair.

    `reference` names which reference merge (`rank_matrix.reference_file`).
    """
    out = {"reference": rank_matrix.reference_file(pair, ".md", reference).read_text(
        encoding="utf-8")}
    out.update(lineup_figures.baseline_texts(pair, BASE))
    return out


def declared_in_reference(pair: str, reference: str = rank_matrix.CURRENT) -> set[str]:
    data = json.loads(rank_matrix.reference_file(pair, ".json", reference).read_text(
        encoding="utf-8"))
    return {record["segment"] for record in data["dispositions"]}


# The headings of source B that base only does not have and that leave the
# count of silent loss under the amended rule, because at least one segment
# of their section is in source A. Named, so that a ninth is loud. The other
# source B headings base only lacks stay silent losses: their whole section
# is gone with them.
BASE_ONLY_UNTAKEN = {
    "bike_docks": ["Escalating E4"],
    "loading_dock": ["Requesting a slot", "When to request", "On the day", "Late finishes"],
    "rate_limits": ["What the client does", "Other kinds of refusal"],
    "trace_names": ["Resolution"],
}


def test_the_reference_merges_stay_clean_under_both_rules() -> None:
    """MUST NOT FIRE: nine reference merges, no silent loss, no untaken heading, both views."""
    moved = {rank_matrix.AS_REGISTERED: [], rank_matrix.CURRENT: []}
    for reference, found in moved.items():
        for pair in PAIRS:
            documents = rank_matrix.pair_docs(pair)
            declared = declared_in_reference(pair, reference)
            merged = pair_merges(pair, reference)["reference"]
            for name, (amended, registered) in both_rules(documents, merged).items():
                check(silent(amended, declared) == [] and untaken(amended, declared) == [],
                      f"{pair}/reference ({reference})/{name}: amended silent "
                      f"{silent(amended, declared)}, untaken {untaken(amended, declared)}")
                check([i for i in silent_registered(registered, declared)] == [],
                      f"{pair}/reference ({reference})/{name}: registered silent "
                      f"{silent_registered(registered, declared)}")
                found += [(pair, name, new.segment.id, new.step)
                          for new, old in zip(amended, registered)
                          if new.verdict != old.verdict]
    # In the references as registered one declared segment changes side, and it
    # is the whole of what the rule does to them: a final comma that the
    # reference writes as a full stop. Pinned, because this one segment is why
    # the mechanical union's deviations differ by one between the two scorings
    # of the 2026-09-27 benchmark. It was bike_docks' support desk count of 3,
    # which the corrected reference (2026-10-15) no longer carries, so there
    # nothing moves.
    check(moved[rank_matrix.AS_REGISTERED] == [("bike_docks", "tool", "b10", STEP_PHRASE),
                                                ("bike_docks", "scorer", "b10", STEP_PHRASE)],
          f"the references as registered move exactly one segment between the rules, "
          f"got {moved[rank_matrix.AS_REGISTERED]}")
    check(moved[rank_matrix.CURRENT] == [],
          f"the corrected references move no segment between the rules, "
          f"got {moved[rank_matrix.CURRENT]}")
    counts["must_not_fire"] += 1


def test_concatenation_and_the_union_lose_nothing_under_either_rule() -> None:
    """MUST NOT FIRE: nothing is absent from a concatenation, and the union is not silent."""
    for pair in PAIRS:
        documents = rank_matrix.pair_docs(pair)
        merges = pair_merges(pair)
        for name, (amended, registered) in both_rules(documents, merges["concatenation"]).items():
            for view, rule in ((amended, AMENDED), (registered, REGISTERED)):
                gone = [i.segment.id for i in view if i.verdict == ABSENT]
                check(not gone, f"{pair}/concatenation/{name}/{rule}: absent {gone}")
        amended, registered = both_rules(documents, merges["union"])["scorer"]
        check(silent(amended) == [] and silent_registered(registered) == [],
              f"{pair}/union: silent loss amended {silent(amended)}, registered "
              f"{silent_registered(registered)}")
    counts["must_not_fire"] += 1


def test_base_only_keeps_its_losses() -> None:
    """MUST FIRE: source A alone against both sources, 129 silent losses registered, 121 amended.

    No sentence, list item or table row of source B is cleared against source
    A alone. The eight that leave the count are headings of source B with at
    least one segment of their section in source A, named in
    `BASE_ONLY_UNTAKEN`.
    """
    registered_total = amended_total = 0
    refiled: dict[str, list[str]] = {}
    for pair in PAIRS:
        documents = rank_matrix.pair_docs(pair)
        amended, registered = both_rules(documents, pair_merges(pair)["base_only"])["scorer"]
        old, new, headings = silent_registered(registered), silent(amended), untaken(amended)
        registered_total += len(old)
        amended_total += len(new)
        check(sorted(new + headings) == sorted(old) and not set(new) & set(headings),
              f"{pair}/base_only: the amended count and the untaken headings must be the "
              f"registered count, split")
        cleared = [(new_item.segment.id, new_item.step)
                   for new_item, old_item in zip(amended, registered)
                   if new_item.verdict != old_item.verdict]
        check(not cleared,
              f"{pair}/base_only: no body segment of source B may be cleared against "
              f"source A alone, got {cleared}")
        by_id = {item.segment.id: item for item in amended}
        if headings:
            refiled[pair] = [by_id[identifier].segment.text for identifier in headings]
        for identifier in headings:
            alive = [member for member in by_id[identifier].section
                     if by_id[member].verdict != ABSENT]
            check(bool(alive), f"{pair}/base_only: {identifier} left the count with nothing "
                               f"of its section in the merge")
    check((registered_total, amended_total) == (129, 121),
          f"base only over the nine pairs: registered {registered_total}, amended "
          f"{amended_total}; 129 and 121 are registered")
    check(refiled == BASE_ONLY_UNTAKEN,
          f"the headings that leave the count: {refiled}; registered: {BASE_ONLY_UNTAKEN}")
    counts["must_fire"] += 1


# --------------------------------------------------------------------------
# Seeded changes to real sentences
# --------------------------------------------------------------------------
#
# Every sentence, list item and table row of at least six words in the
# eighteen source documents of the nine pairs, one at a time. The "merge" is
# the sentence's own document with that one sentence changed and nothing
# else, and the only source is that document, so what is found can only be
# what the change left behind. Each change is a seed: some must be cleared
# (the sentence is all there), some must stay absent (part of it was taken
# out).

FILLER = ("; the control added this clause, which says nothing that either document says, "
          "so that no line of the merge is close to the sentence in length.")
_END = ".!?:;,"

# seed name -> must the amended rule call it reworded ("clear"), absent
# ("stay"), or is it only counted ("measure")?
SEEDS = {
    "joined to a long clause": "clear",
    "split at a comma or at 'and', clean seam": "clear",
    "joined, last two words cut": "stay",
    "joined, last three words cut": "stay",
    "joined, last four words cut": "stay",
    "joined, first two words cut": "stay",
    "joined, first three words cut": "stay",
    "joined, first four words cut": "stay",
    "joined, a word cut from the middle": "stay",
    "joined, a digit changed": "stay",
    "second half cut, a long clause in its place": "stay",
    "deleted": "stay",
    "split, a long clause written in at the seam": "measure",
    "last two words cut, nothing added": "measure",
    "second half cut, nothing added": "measure",
}

# Seeded losses the amended rule clears: its known limit, by name. Listed by
# hand after reading each one, so that a fourth fails the run instead of
# joining a count.
#
# All three are one thing. The sentence before ends with the very words that
# were cut from the front of this one ("...is a guess. [That guess] is not
# worth having."), so the run passes across the full stop. It needs the merge
# to hold a sentence without its opening, directly after a sentence that ends
# on those words.
KNOWN_SEEDED_CLEARS = {
    ("joined, first two words cut", "rate_limits", "source_b.md",
     "That guess is not worth having."),
    ("joined, first three words cut", "rate_limits", "source_a.md",
     "A loop that waits and retries against a suspended credential spends its whole budget "
     "without ever reaching the service \u2014 and the log afterwards shows nothing at all "
     "except a long run of refusals."),
    ("joined, first three words cut", "trace_names", "source_b.md",
     "The Nimbrel Probe stream name is what seperates one instrumented process from the next."),
}


def seeds_of(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    bare = text.rstrip(_END)
    tail = text[len(bare):] or "."
    pieces = bare.split(" ")
    content = lambda part: reconcile.content_words(reconcile.words(part))  # noqa: E731
    out["joined to a long clause"] = bare + FILLER
    for count, word in ((2, "two"), (3, "three"), (4, "four")):
        if len(pieces) < count + 4:
            continue
        if content(" ".join(pieces[-count:])):
            out[f"joined, last {word} words cut"] = " ".join(pieces[:-count]) + FILLER
            if count == 2:
                out["last two words cut, nothing added"] = " ".join(pieces[:-2]) + tail
        if content(" ".join(pieces[:count])):
            out[f"joined, first {word} words cut"] = " ".join(pieces[count:]) + FILLER
    middle = len(pieces) // 2
    if content(pieces[middle]):
        out["joined, a word cut from the middle"] = (
            " ".join(pieces[:middle] + pieces[middle + 1:]) + FILLER)
    digit = re.search(r"\d", bare)
    if digit:
        changed = str((int(digit.group()) + 1) % 10)
        out["joined, a digit changed"] = (bare[:digit.start()] + changed
                                          + bare[digit.end():] + FILLER)
    best = None
    for match in re.finditer(r", | and ", bare):
        left, right = bare[:match.start()], bare[match.end():]
        if len(left.split()) >= 3 and len(right.split()) >= 3:
            balance = abs(len(left) - len(right))
            if best is None or balance < best[0]:
                best = (balance, left, right)
    if best:
        _, left, right = best
        capital = right[:1].upper() + right[1:]
        clause = FILLER.replace("; the control", ", as the control").rstrip(".")
        out["split at a comma or at 'and', clean seam"] = left + ". " + capital + tail
        out["split, a long clause written in at the seam"] = (
            left + clause + ". " + capital + clause + ".")
        out["second half cut, a long clause in its place"] = left + FILLER
        out["second half cut, nothing added"] = left + "."
    out["deleted"] = ""
    return out


def test_seeded_cuts_of_real_sentences_stay_losses_but_for_three_named_ones() -> None:
    """Join and split every real sentence (cleared), then cut it (stays absent).

    MUST FIRE: a sentence that lost two, three or four words from either end,
    a word from the middle, a digit or its second half, joined to a long
    clause so the ratio cannot reach it, stays absent. MUST NOT FIRE: the same
    sentence whole, joined or split at a clean seam, is reworded. The three
    seeded losses the rule does clear are the known limit, by name.
    """
    cleared_losses, kept_alarms = [], []
    used = seeded = cleared = 0
    for pair in PAIRS:
        for name, text in rank_matrix.pair_docs(pair).items():
            document = segment.segment_document(text, "a", "source_a.md")
            flat = reconcile.flatten(text)
            for item in document.segments:
                if (item.kind not in reconcile.BODY_KINDS
                        or len(reconcile.words(item.text)) < 6):
                    continue
                if text.count(item.text) != 1 or flat.count(reconcile.flatten(item.text)) != 1:
                    continue    # hard-wrapped, or stated twice in its own document
                used += 1
                alone = dataclasses.replace(document, segments=(item,))
                for seed, new in seeds_of(item.text).items():
                    merged = text.replace(item.text, new, 1)
                    merged_segments = segment.segment_document(
                        merged, reconcile.MERGE_LETTER).segments
                    merged_flat = reconcile.flatten(merged)
                    result = reconcile.locate(alone, merged_flat, merged_segments,
                                              rule=AMENDED).located[0]
                    seeded += 1
                    # A seed counts only where the registered rule calls the
                    # sentence absent, which the step says: nothing found it,
                    # or only a run step did. Where a run step cleared it the
                    # registered rule is asked as well, so that the claim
                    # "absent before, reworded now" is observed and not derived.
                    if result.step not in (STEP_NONE, *reconcile.RUN_STEPS):
                        continue
                    if result.step in reconcile.RUN_STEPS:
                        old = reconcile.locate(alone, merged_flat, merged_segments,
                                               rule=REGISTERED).located[0]
                        additive([result], [old], f"seed {seed!r} on {pair}/{name}/{item.id}")
                        check(old.verdict == ABSENT,
                              f"seed {seed!r} on {pair}/{name}/{item.id}: cleared by "
                              f"{result.step} and {old.verdict} under the registered rule")
                        cleared += 1
                    if SEEDS[seed] == "stay" and result.verdict != ABSENT:
                        cleared_losses.append((seed, pair, name, item.text))
                    if SEEDS[seed] == "clear" and result.verdict == ABSENT:
                        kept_alarms.append((seed, pair, name, item.text))
    # Exact, because the nine pairs are a frozen corpus: a different count means
    # the sources, the segmenter or the tokeniser moved under this control.
    check((used, seeded, cleared) == (181, 2109, 164),
          f"the seeds ran over {used} sentences and {seeded} changes and a run step "
          f"cleared {cleared}; 181, 2109 and 164 are registered")
    check(set(cleared_losses) == KNOWN_SEEDED_CLEARS and len(cleared_losses) == 3,
          f"seeded losses cleared: expected exactly the three known ones, got "
          f"{sorted(set(cleared_losses) ^ KNOWN_SEEDED_CLEARS)} different")
    check(not kept_alarms,
          f"{len(kept_alarms)} whole sentences, joined or cleanly split, are still absent: "
          f"{kept_alarms[:3]}")
    counts["must_fire"] += 1
    counts["must_not_fire"] += 1
    counts["limit_cleared"] += len(KNOWN_SEEDED_CLEARS)


def test_amended_rule_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def main() -> int:
    for kind in counts:
        counts[kind] = 0
    checks = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_amended_rule_offline" and callable(function):
            try:
                function()
            except Exception as exc:  # noqa: BLE001 - a crashing check is a failing check
                failures.append(f"{name} raised {type(exc).__name__}: {exc}")
            checks += 1
    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures[:60]:
            print(f"  - {failure}")
        return 1
    print(f"amended rule: {checks} checks pass in both views: {counts['must_not_fire']} "
          f"must-not-fire, {counts['must_fire']} must-fire, {counts['limit_kept']} known "
          f"false alarms kept, {counts['limit_cleared']} known differences cleared")
    return 0


if __name__ == "__main__":
    sys.exit(main())
