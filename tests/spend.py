#!/usr/bin/env python3
"""Spend and rate caps for paid endpoints. Enforced, not remembered.

The harness that runs the API arms is about to spend the user's money against
two loaded keys and a third that must never be billed at all. Care is not a
control: a retry loop that goes wrong at three in the morning does not care,
and the failure is only visible on an invoice.

Where the money is decided, and why it is here and not in `src/llossless/`:
a token count is a measurement and belongs in the tool; a price is a dated fact
about a vendor's web page and belongs beside the date it was read.
So `llossless` records tokens and knows nothing about dollars, and this
file - harness-side, never published as part of the tool - holds the table.

**The table starts empty until the SKUs are pinned, and that is the safe state.**
`price_for` raises on a SKU it does not know. An unpriced model therefore
aborts the run rather than costing nothing, which is the only direction this
can fail in safely: a table that defaulted to zero would let an unrecognised
SKU spend without limit and report `$0.00` while doing it. Prices are entered
from the vendor's own pricing page, with the URL and the date read, and never
from recollection - the rule this project holds citations to, applied to the
other kind of claim that looks fine until somebody checks it.

Four caps, and each one is checked before the call as well as after it. A cap
that only reconciles afterwards has already spent the money it was there to
refuse:

  spend     per vendor, in dollars. The pre-call estimate is deliberately
            pessimistic - the whole output allowance at the output rate - so
            the cap trips early rather than exactly.
  calls     per run, across all vendors.
  tokens    per run, across all vendors.
  interval  per vendor, in seconds. A free-tier rate limit should produce
            pacing, not a cascade of retries that each cost a call.

Serial only. `Ledger.call` is a context manager that refuses to be entered
twice, so two arms running concurrently against hosted endpoints is a crash and
not a race. Parallelism here would break the pacing and the cap in the same
move, since both are read-modify-write over one counter.

Usage:
    python3 tests/spend.py --self-test
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# The price table moved to `src/llossless/pricing.py`: the product needs
# it to answer "what did this merge cost", and `src/` may not import from the
# test tree. Re-exported here so this module's callers -- the vendor arms, the
# probes and their tests -- read the same rows under the same names they
# always did, and so that there is exactly one table to keep dated.
from llossless.pricing import (  # noqa: F401  (re-exported)
    PRICES,
    Price,
    UnknownPrice,
    cost,
    price_for,
)

import source_guard
from source_guard import NO_DOCUMENT, UnapprovedSource  # noqa: F401  (re-exported)


class BudgetExceeded(RuntimeError):
    """A cap would be crossed. The run stops here, before the call."""



class ConcurrentCall(RuntimeError):
    """Two calls in flight at once against hosted endpoints. Never allowed."""




@dataclass
class Caps:
    """The limits for one run. Deliberately low by default.

    A default high enough to be convenient is a default that never fires, and
    the harness that needs this is the one nobody has run yet.
    """
    spend: dict[str, float] = field(default_factory=dict)  # vendor -> dollars
    calls: int = 60
    tokens: int = 500_000
    interval: dict[str, float] = field(default_factory=dict)  # vendor -> seconds


# The user's ruling for the first pass, recorded here so the harness reads it
# from one place rather than from a command line somebody has to remember.
# Google is $0.00 and that is not a formality: the key has no credit loaded, the
# arm is free-tier only, and any call the table prices above zero aborts the run
# instead of quietly becoming the first billable one.
#
# The call and token ceilings are per run and across all vendors. They are set
# where a retry loop cannot run away rather than where the planned work fits
# comfortably: 2x2 arms at K=3 over 23 corpus items is the shape of the sweep,
# and if that needs more than this, raising it is a decision somebody makes with
# the numbers in front of them.
# Pacing. Derived, not recalled - and derived from the *account's* limits read
# off each console on 2026-08-31, not from a published tier table, because the
# published tables state spend tiers and the enforced numbers are per-account.
#
# Requests per minute is never the binding constraint here. Calls are serial
# (`Ledger.call` refuses re-entry), so the ceiling is one call per round trip;
# at 500-1000 RPM the request limit cannot be reached by a serial caller. The
# token-per-minute limit is what binds, and the interval is the time one call's
# tokens take to clear it:  interval = 60 * tokens_per_call / TPM.
#
# Sized against the largest planned call: ~2,000 input tokens and a 10,000
# output allowance.
#
#   openai      gpt-5.6-luna is the tighter of the two SKUs at 200,000 TPM
#               (terra is 500,000); 500 RPM. TPM is combined here, so
#               60 * 12,000 / 200,000 = 3.6s. Rounded up.
#   anthropic   input and output are limited separately: 500,000 input TPM,
#               80,000 output TPM, 1,000 RPM, the same for haiku-4.5 and
#               sonnet-5. Output binds: 60 * 10,000 / 80,000 = 7.5s. Input
#               would want 0.24s. Rounded up.
#   google      no console figure has been read for this account. Rather than
#               enter a free-tier limit from recollection - the same rule the
#               prices are held to - this is a stated policy floor of two
#               requests per minute, chosen to sit below any published free
#               tier rather than to match one. It is not a vendor figure and
#               must not be cited as one. Replace it with the console's number.
FIRST_PASS = Caps(
    # Raised from $6.00/$6.00 ($12.00 total) to $7.50/$7.50 ($15.00 total),
    # the author's approval, split evenly on the same terms the original pair
    # were set on -- neither vendor argued for more room than the other.
    # Applied here, not only recorded as approved.
    spend={"openai": 7.50, "anthropic": 7.50, "google": 0.00},
    calls=400,
    tokens=4_000_000,
    interval={"openai": 4.0, "anthropic": 8.0, "google": 30.0},
)


@dataclass
class Spent:
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    dollars: dict[str, float] = field(default_factory=dict)

    @property
    def tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class Ledger:
    """One run's running total, and the thing that says no.

    `announce` is the console's detail channel: the running spend goes out
    after every call at `-vv`, because a total nobody sees until the end is a
    total nobody can stop.
    """

    def __init__(self, caps: Caps, *, announce=None, clock=time.monotonic,
                 sleep=time.sleep, now=None) -> None:
        self.caps = caps
        self.spent = Spent()
        self.announce = announce or (lambda _line: None)
        self._clock = clock
        self._sleep = sleep
        self._last: dict[str, float] = {}
        self._in_flight = False
        # The tracked paths the last approved call was allowed to send. Kept for
        # reconciliation: an invoice line and a document list, side by side.
        self.approved: list[str] = []
        # Wall clock, separate from `_clock`. Pacing runs on a monotonic clock
        # that the probes fake; a dashboard is queried over a wall-clock window
        # and the two must not be the same dial.
        self._now = now or (lambda: datetime.now(timezone.utc)
                            .isoformat(timespec="seconds").replace("+00:00", "Z"))
        self.rows: list[dict] = []

    # -- the checks ---------------------------------------------------------

    def _refuse(self, vendor: str, sku: str, dollars: float, tokens: int) -> str | None:
        cap = self.caps.spend.get(vendor)
        if cap is None:
            return (f"no spend cap registered for vendor {vendor!r}. Every vendor "
                    f"gets one, including the ones that are meant to be free.")
        after = self.spent.dollars.get(vendor, 0.0) + dollars
        if after > cap + 1e-9:
            return (f"{vendor}: this call would take spend to ${after:.4f}, over "
                    f"the ${cap:.2f} cap ({sku})")
        if self.spent.calls + 1 > self.caps.calls:
            return f"call ceiling {self.caps.calls} reached ({sku})"
        if self.spent.tokens + tokens > self.caps.tokens:
            return (f"token ceiling {self.caps.tokens} would be crossed at "
                    f"{self.spent.tokens + tokens} ({sku})")
        return None

    def _pace(self, vendor: str) -> float:
        wanted = self.caps.interval.get(vendor, 0.0)
        if wanted <= 0 or vendor not in self._last:
            return 0.0
        waited = max(0.0, wanted - (self._clock() - self._last[vendor]))
        if waited:
            self._sleep(waited)
        return waited

    @contextmanager
    def call(self, vendor: str, sku: str, *, input_estimate: int, output_allowance: int,
             documents):
        """Guard one call: approve, pace, refuse, run, charge, announce.

        The estimate is pessimistic on purpose - the whole output allowance at
        the output rate - so the cap trips before the call rather than after
        it. The body yields a function the caller hands the real usage to, and
        the real numbers replace the estimate on the way out.

        `documents` has no default, deliberately. It is the material about to
        leave the machine, and every document in it must sha256-match a blob
        tracked under `tests/` at HEAD or the call never happens
        (`source_guard`). A call that carries no document at all - a SKU or tier
        probe - passes `source_guard.NO_DOCUMENT` and says so. The two are kept
        apart because an empty list is what a filter returns when it has gone
        wrong, and that must not read as permission.

        It sits here rather than in a pre-flight script for one reason: a
        pre-flight runs once and then stops being run, and nobody notices. The
        caps are enforced on this line; so is this. There is no code path that
        issues a paid call and skips it, because there is no other code path.
        """
        self.approved = source_guard.approve(documents)
        if self._in_flight:
            raise ConcurrentCall(
                "a second call started while one was in flight. Hosted arms run "
                "serially: the cap and the pacing are both read-modify-write over "
                "one counter, and concurrency breaks them together."
            )
        estimate = cost(sku, input_tokens=input_estimate, output_tokens=output_allowance)
        refusal = self._refuse(vendor, sku, estimate, input_estimate + output_allowance)
        if refusal:
            raise BudgetExceeded(refusal)
        self._pace(vendor)
        self._in_flight = True
        charged: dict = {}

        def charge(*, input_tokens: int | None, output_tokens: int | None,
                   cached_tokens: int = 0) -> float:
            """What the call actually cost. `None` means the vendor said nothing.

            An unmeasured call is charged the estimate, not zero. The whole
            point of the tally in `llossless.usage` is that unknown and zero
            are different, and here the difference has a direction: a call
            nobody measured must not deplete the cap by nothing.
            """
            if input_tokens is None or output_tokens is None:
                charged["dollars"] = estimate
                charged["input"] = input_estimate
                charged["output"] = output_allowance
                charged["measured"] = False
            else:
                charged["dollars"] = cost(sku, input_tokens=input_tokens,
                                          output_tokens=output_tokens,
                                          cached_tokens=cached_tokens)
                charged["input"] = input_tokens
                charged["output"] = output_tokens
                charged["measured"] = True
            return charged["dollars"]

        try:
            yield charge
        finally:
            self._in_flight = False
            self._last[vendor] = self._clock()
            if not charged:
                # The call raised before it reported anything. Charge the
                # estimate: a failed request is still a request, and a retry
                # loop that failed for free would be the runaway this file
                # exists to stop.
                charge(input_tokens=None, output_tokens=None)
            self.spent.calls += 1
            self.spent.input_tokens += charged["input"]
            self.spent.output_tokens += charged["output"]
            self.spent.dollars[vendor] = (self.spent.dollars.get(vendor, 0.0)
                                          + charged["dollars"])
            self.rows.append({
                "at": self._now(),
                "vendor": vendor,
                "sku": sku,
                "input_tokens": charged["input"],
                "output_tokens": charged["output"],
                "dollars": charged["dollars"],
                "measured": charged["measured"],
                "documents": list(self.approved),
            })
            self.announce(self.summary(vendor, measured=charged["measured"]))

    def summary(self, vendor: str | None = None, *, measured: bool = True) -> str:
        totals = ", ".join(f"{name} ${value:.4f}"
                           for name, value in sorted(self.spent.dollars.items()))
        line = (f"spend: {totals or 'nothing'} | {self.spent.calls}/{self.caps.calls} "
                f"calls | {self.spent.tokens:,}/{self.caps.tokens:,} tokens")
        if not measured:
            line += f" | {vendor}: last call reported no usage, charged the estimate"
        return line

    def snapshot(self) -> dict:
        """What this run believes it spent, in a form a dashboard can be held to.

        The window is the point of it. "The ledger says $1.87" is not a claim
        anybody can check; "the ledger says $1.87 between these two instants" is,
        and the vendor consoles all filter by time. Per-call rows travel with it
        because a total that disagrees is only diagnosable at the call that
        caused the disagreement.
        """
        return {
            "window": {"from": self.rows[0]["at"] if self.rows else None,
                       "to": self.rows[-1]["at"] if self.rows else None},
            "calls": self.spent.calls,
            "input_tokens": self.spent.input_tokens,
            "output_tokens": self.spent.output_tokens,
            "dollars": dict(self.spent.dollars),
            # A vendor capped at zero is not "cheap", it is one that must never
            # appear on a bill at all, and reconciliation has to know which.
            "must_not_be_billed": sorted(v for v, cap in self.caps.spend.items()
                                         if cap == 0.0),
            "prices": {sku: {"input": p.input, "output": p.output,
                             "cached_input": p.cached_input,
                             "source": p.source, "read_on": p.read_on}
                       for sku, p in sorted(PRICES.items())},
            "rows": list(self.rows),
        }



# -- reconciliation ------------------------------------------------------------
#
# `price_for` demands a URL and a date, which is the right bar for
# entering a price. It is not a check that the price is right. The failure it
# cannot see is a unit error - a rate quoted per 1K tokens entered into a table
# that divides by 1M - and that error is 1000x in the dangerous direction: the
# ledger under-reports, the cap never trips, and everything looks fine until the
# invoice. Nothing in the tool can catch it, because the tool has only the
# table. The only external witness is the vendor's own dashboard.

# What a vendor console will show. Every one of them rounds to the cent, so a
# figure below this is not a small number - it is an unreadable one.
DASHBOARD_RESOLUTION = 0.01

# Fractional slack above the resolution floor, for the vendors that compute a
# bill in a slightly different order than `cost` does.
TOLERANCE = 0.01

AGREES = "AGREES"
DISAGREES = "DISAGREES"
UNANSWERABLE = "UNANSWERABLE"
MUST_NOT_BE_BILLED = "MUST-NOT-BE-BILLED"


@dataclass(frozen=True)
class Line:
    """One vendor's ledger range against one vendor's dashboard figure.

    `ledger` is the upper bound and the figure to quote: every charge, including
    the estimate booked for a call that failed before reporting usage. `lower`
    is the measured-only subtotal. The two differ by exactly the estimates for
    unmeasured calls, and the gap between them is the part of the ledger whose
    billing status this repository does not know.
    """
    vendor: str
    ledger: float
    charged: float
    verdict: str
    note: str
    lower: float | None = None

    @property
    def upper(self) -> float:
        return self.ledger

    @property
    def width(self) -> float:
        return self.ledger - (self.ledger if self.lower is None else self.lower)

    @property
    def ok(self) -> bool:
        return self.verdict == AGREES


def _unit_error(ledger: float, charged: float) -> str:
    """Name the shape of the discrepancy when it looks like a decimal slip."""
    if ledger <= 0 or charged <= 0:
        return ""
    ratio = charged / ledger
    for power, label in ((1000.0, "1000x"), (0.001, "1/1000x"),
                         (100.0, "100x"), (0.01, "1/100x")):
        if abs(ratio / power - 1.0) < 0.05:
            direction = "under" if ratio > 1 else "over"
            return (f" The ratio is {label}, which is what a per-1K rate entered "
                    f"into a per-1M table looks like: the ledger {direction}-reports "
                    f"by three orders of magnitude and the cap never fires.")
    return f" The ratio is {ratio:.4g}x."


# A range that is wide compared with what it contains will absorb a real error,
# so the note has to say so rather than reporting a bare AGREES. The threshold
# is where the unmeasured part is as large as the measured part: at that width
# the console could be double the measured spend and still land inside.
WIDE = 1.0


def _agreement_note(low: float, high: float, band: float, resolution: float) -> str:
    if high - low <= resolution:
        return f"within ${band:.4f}."
    note = (f"inside the ledger range ${low:.4f}..${high:.4f} (band ${band:.4f}). "
            f"The range is ${high - low:.4f} wide because that much was charged as "
            f"an estimate for calls the vendor may not bill.")
    if low > 0 and (high - low) / low >= WIDE:
        note += (f" At this width the pass certifies only that the console is not "
                 f"outside the range - it does NOT exclude an error up to "
                 f"${high - low:.4f}, which is {(high - low) / low:.1f}x the "
                 f"measured spend. Reduce the unmeasured share before trusting it.")
    return note


def bounds(snapshot: dict) -> dict[str, tuple[float, float]]:
    """Per vendor, the (measured-only, everything) pair the console can fall in.

    A call that raised before reporting usage is charged its estimate, because
    a call nobody measured must not deplete the cap by nothing. But
    a vendor does not necessarily bill it - OpenAI does not bill a 400 - so the
    ledger's total is an upper bound on the invoice, not a prediction of it.

    Rather than pick an end and hope, both are reported and the console is
    allowed to sit anywhere between. This is honest about what is actually
    unknown: not the arithmetic, but each vendor's billing policy per status
    code. Where every call was measured the two coincide and the range collapses
    to the point comparison it was before.
    """
    out: dict[str, tuple[float, float]] = {}
    for vendor, total in snapshot.get("dollars", {}).items():
        measured = sum(r["dollars"] for r in snapshot.get("rows", ())
                       if r["vendor"] == vendor and r.get("measured"))
        out[vendor] = (min(measured, float(total)), float(total))
    return out


def reconcile(snapshot: dict, charged: dict[str, float], *,
              resolution: float = DASHBOARD_RESOLUTION,
              tolerance: float = TOLERANCE) -> list[Line]:
    """The ledger's figure against the dashboard's, per vendor. Fail closed.

    Four verdicts, and only one of them permits an arm to run:

      AGREES              within one display unit, or within `tolerance` of the
                          larger figure, whichever is more generous.
      DISAGREES           outside that. The ratio is reported, and a ratio near
                          a power of a thousand is named as a probable unit
                          error rather than left for the reader to spot.
      UNANSWERABLE        both figures are below what a dashboard can display.
                          This is NOT agreement. Two numbers that both round to
                          $0.00 agree on nothing, and a 1000x under-count is
                          exactly what hides there. The probe has to be made big
                          enough to clear the resolution, or the check is
                          theatre.
      MUST-NOT-BE-BILLED  a vendor capped at $0.00 appears on a bill. There is
                          no tolerance on this one; the cap is not a budget, it
                          is a statement that the key has no credit and the arm
                          is free-tier only.

    Every vendor in either the snapshot or the dashboard figures gets a line. A
    vendor the dashboard was not asked about is not silently absent: an
    unqueried vendor is unreconciled, which is unanswerable, not clean.
    """
    ledger = snapshot.get("dollars", {})
    span = bounds(snapshot)
    never = set(snapshot.get("must_not_be_billed", ()))
    lines = []
    for vendor in sorted(set(ledger) | set(charged) | never):
        mine = float(ledger.get(vendor, 0.0))
        if vendor not in charged:
            lines.append(Line(vendor, mine, float("nan"), UNANSWERABLE,
                              "no dashboard figure was supplied for this vendor, so "
                              "nothing was reconciled. Unqueried is not clean."))
            continue
        theirs = float(charged[vendor])
        if vendor in never and theirs > 0:
            lines.append(Line(vendor, mine, theirs, MUST_NOT_BE_BILLED,
                              f"capped at $0.00 and billed ${theirs:.4f}. The key "
                              f"carries no credit and the arm is free-tier only; "
                              f"this is a stop, not a variance."))
            continue
        low, high = span.get(vendor, (mine, mine))
        band = max(resolution, tolerance * max(abs(low), abs(high), abs(theirs)))
        nearest = low if theirs < low else (high if theirs > high else theirs)
        gap = abs(theirs - nearest)
        width = high - low
        if gap <= band:
            if max(high, theirs) < resolution and vendor not in never:
                lines.append(Line(vendor, mine, theirs, UNANSWERABLE,
                                  f"both figures are under the ${resolution:.2f} a "
                                  f"dashboard can show, so their agreement proves "
                                  f"nothing. Size the probe to spend at least "
                                  f"${resolution:.2f} and reconcile again.", low))
            else:
                lines.append(Line(vendor, mine, theirs, AGREES,
                                  _agreement_note(low, high, band, resolution), low))
            continue
        lines.append(Line(vendor, mine, theirs, DISAGREES,
                          f"outside ${low:.4f}..${high:.4f} by ${gap:.4f}, more than "
                          f"the ${band:.4f} band.{_unit_error(nearest, theirs)}", low))
    return lines


def render(snapshot: dict, lines: list[Line]) -> str:
    """The reconciliation as figures, never as 'checked'."""
    window = snapshot.get("window", {})
    out = [f"reconciliation over {window.get('from')} .. {window.get('to')} "
           f"({snapshot.get('calls', 0)} call(s), "
           f"{snapshot.get('input_tokens', 0):,} in / "
           f"{snapshot.get('output_tokens', 0):,} out)",
           f"  {'vendor':<12} {'ledger':>12} {'dashboard':>12}  verdict"]
    for line in lines:
        shown = "not queried" if line.charged != line.charged else f"${line.charged:.4f}"
        out.append(f"  {line.vendor:<12} ${line.ledger:>11.4f} {shown:>12}  "
                   f"{line.verdict}")
        out.append(f"  {'':<12} {line.note}")
    blocked = [ln.vendor for ln in lines if not ln.ok]
    out.append(f"  verdict: {'PROCEED' if not blocked else 'STOP'} - "
               + ("every vendor reconciles" if not blocked
                  else f"unreconciled: {', '.join(blocked)}. No arm runs."))
    return "\n".join(out)


# -- probes ------------------------------------------------------------------
#
# A cap that has never fired is untested, and the brief asks for the abort to
# be asserted rather than trusted. One must-fire per cap, plus the two rules
# that are easy to get backwards: an unpriced SKU must abort rather than cost
# nothing, and an unmeasured call must be charged rather than waved through.

def self_test() -> int:
    failures = []

    def check(condition, message):
        if not condition:
            failures.append(message)

    probe = "probe/canary-1m"
    caps = Caps(spend={"probe": 1.00}, calls=10, tokens=10_000,
                interval={"probe": 0.0})

    # The happy path, so the failures below mean something.
    ledger = Ledger(caps)
    with ledger.call("probe", probe, input_estimate=1000, output_allowance=1000,
                     documents=NO_DOCUMENT) as charge:
        charge(input_tokens=1000, output_tokens=500)
    check(abs(ledger.spent.dollars["probe"] - 0.0015) < 1e-9,
          f"a priced call must cost what the table says, got {ledger.spent.dollars}")
    check(ledger.spent.calls == 1 and ledger.spent.tokens == 1500,
          f"and must be counted, got {ledger.spent}")

    # must-fire: the spend cap, pre-call.
    tight = Ledger(Caps(spend={"probe": 0.0001}, interval={"probe": 0.0}))
    try:
        with tight.call("probe", probe, input_estimate=1000, output_allowance=1000,
                        documents=NO_DOCUMENT):
            failures.append("the spend cap did not fire: a call ran over its cap")
    except BudgetExceeded as exc:
        check("over the $0.00 cap" in str(exc), f"the refusal must say so: {exc}")
    check(tight.spent.calls == 0, "and the refused call must not be counted as made")

    # must-fire: the zero-dollar vendor. Google is meant to cost nothing, and
    # `cap = 0` must refuse any call the table prices above zero.
    free = Ledger(Caps(spend={"google": 0.0}, interval={}))
    try:
        with free.call("google", probe, input_estimate=1, output_allowance=1,
                       documents=NO_DOCUMENT):
            failures.append("a $0.00 cap admitted a billable call")
    except BudgetExceeded:
        pass

    # must-not-fire: the same $0.00 cap over a SKU the table prices at zero.
    PRICES["probe/free"] = Price(input=0.0, output=0.0, source="the self-test", read_on="n/a")
    admitted = Ledger(Caps(spend={"google": 0.0}, interval={}))
    try:
        with admitted.call("google", "probe/free", input_estimate=100,
                           output_allowance=100, documents=NO_DOCUMENT) as charge:
            charge(input_tokens=100, output_tokens=100)
    except BudgetExceeded as exc:
        failures.append(f"a $0.00 cap refused a genuinely free call: {exc}")
    check(admitted.spent.calls == 1, "a free call still counts as a call")

    # must-fire: the call ceiling and the token ceiling, separately.
    counted = Ledger(Caps(spend={"probe": 100.0}, calls=1, interval={}))
    with counted.call("probe", probe, input_estimate=1, output_allowance=1,
                      documents=NO_DOCUMENT) as charge:
        charge(input_tokens=1, output_tokens=1)
    try:
        with counted.call("probe", probe, input_estimate=1, output_allowance=1,
                          documents=NO_DOCUMENT):
            failures.append("the call ceiling did not fire")
    except BudgetExceeded as exc:
        check("call ceiling" in str(exc), f"the refusal must name the ceiling: {exc}")

    windowed = Ledger(Caps(spend={"probe": 100.0}, tokens=100, interval={}))
    try:
        with windowed.call("probe", probe, input_estimate=60, output_allowance=60,
                           documents=NO_DOCUMENT):
            failures.append("the token ceiling did not fire")
    except BudgetExceeded as exc:
        check("token ceiling" in str(exc), f"the refusal must name the ceiling: {exc}")

    # must-fire: an unpriced SKU aborts rather than costing nothing.
    try:
        cost("openai/whatever-they-renamed-it-to", input_tokens=1, output_tokens=1)
        failures.append("an unpriced SKU was charged instead of refused")
    except UnknownPrice:
        pass

    # must-fire: a vendor with no registered cap is refused, so a vendor added
    # to the run and forgotten in the config cannot spend.
    unregistered = Ledger(Caps(spend={}, interval={}))
    try:
        with unregistered.call("newvendor", probe, input_estimate=1, output_allowance=1,
                               documents=NO_DOCUMENT):
            failures.append("a vendor with no cap was allowed to spend")
    except BudgetExceeded as exc:
        check("no spend cap registered" in str(exc), f"and must say why: {exc}")

    # An unmeasured call is charged the estimate, not zero.
    silent = Ledger(Caps(spend={"probe": 100.0}, interval={}))
    with silent.call("probe", probe, input_estimate=1000, output_allowance=2000,
                     documents=NO_DOCUMENT) as charge:
        charge(input_tokens=None, output_tokens=None)
    check(abs(silent.spent.dollars["probe"] - 0.003) < 1e-9,
          f"an unmeasured call must be charged the estimate: {silent.spent.dollars}")
    check("reported no usage" in silent.summary("probe", measured=False),
          "and must say so in the running total")

    # A call that raises is still a call. A retry loop that failed for free is
    # the runaway this file exists to stop.
    crashed = Ledger(Caps(spend={"probe": 100.0}, interval={}))
    try:
        with crashed.call("probe", probe, input_estimate=10, output_allowance=10,
                          documents=NO_DOCUMENT):
            raise TimeoutError("the endpoint went away")
    except TimeoutError:
        pass
    check(crashed.spent.calls == 1 and crashed.spent.dollars["probe"] > 0,
          f"a failed call must still be charged: {crashed.spent}")

    # Serial only.
    serial = Ledger(Caps(spend={"probe": 100.0}, interval={}))
    try:
        with serial.call("probe", probe, input_estimate=1, output_allowance=1,
                         documents=NO_DOCUMENT) as charge:
            charge(input_tokens=1, output_tokens=1)
            with serial.call("probe", probe, input_estimate=1, output_allowance=1,
                             documents=NO_DOCUMENT):
                failures.append("two hosted calls were allowed in flight at once")
    except ConcurrentCall:
        pass

    # Pacing, on a fake clock: a free-tier limit must produce a wait, not a
    # retry. Measured through the sleeps asked for, because a test that
    # actually waited would be a test nobody runs.
    now = [0.0]
    slept: list[float] = []
    paced = Ledger(Caps(spend={"probe": 100.0}, interval={"probe": 4.0}),
                   clock=lambda: now[0], sleep=slept.append)
    for _ in range(2):
        with paced.call("probe", probe, input_estimate=1, output_allowance=1,
                        documents=NO_DOCUMENT) as charge:
            charge(input_tokens=1, output_tokens=1)
    check(slept == [4.0], f"the second call must wait the interval, slept {slept}")

    # And the running total reaches the console after every call.
    said: list[str] = []
    loud = Ledger(Caps(spend={"probe": 100.0}, interval={}), announce=said.append)
    with loud.call("probe", probe, input_estimate=1, output_allowance=1,
                   documents=NO_DOCUMENT) as charge:
        charge(input_tokens=1, output_tokens=1)
    check(len(said) == 1 and "spend:" in said[0] and "calls" in said[0],
          f"the running total must be announced per call, got {said}")

    # must-fire: the vendor gate, ON the call path. Not `source_guard.approve`
    # called directly - that is the module's own self-test - but through
    # `Ledger.call`, which is the only way a paid call is ever issued. This is
    # the reach probe: it fails if the call site is removed, however well the
    # guard itself works.
    gated = Ledger(Caps(spend={"probe": 100.0}, interval={}))
    try:
        with gated.call("probe", probe, input_estimate=1, output_allowance=1,
                        documents=[b"material this repository never committed\n" * 30]):
            failures.append("an uncommitted document reached a paid call")
    except UnapprovedSource:
        pass
    check(gated.spent.calls == 0 and not gated._in_flight,
          f"a refused document must leave the ledger untouched and usable, "
          f"got {gated.spent}")

    # must-not-fire: a committed pair goes through, and the ledger records which
    # tracked paths it was allowed to send.
    pair = sorted((source_guard.REPO / "tests" / "pairs" / "index_429").glob("*.md"))
    check(bool(pair), "expected a committed pair to gate the must-not-fire probe on")
    if pair:
        body = pair[0].read_text(encoding="utf-8")
        try:
            with gated.call("probe", probe, input_estimate=1, output_allowance=1,
                            documents=[body]) as charge:
                charge(input_tokens=1, output_tokens=1)
            check(gated.approved == [str(pair[0].relative_to(source_guard.REPO))],
                  f"an approved call must name what it sent, got {gated.approved}")
        except UnapprovedSource as exc:
            failures.append(f"a committed pair was refused on the call path: {exc}")

    # must-fire: no default. A caller that forgets the argument cannot compile a
    # call, which is the property the whole gate rests on.
    try:
        with Ledger(caps).call("probe", probe, input_estimate=1, output_allowance=1):
            failures.append("a paid call was issued without declaring its documents")
    except TypeError:
        pass

    # -- reconciliation ----------------------------------------------------------
    #
    # Seeded both ways. The must-not-fire side is a real snapshot off a real
    # ledger, so the shape being reconciled is the shape the harness produces.
    PRICES["probe/big"] = Price(input=3.00, output=15.00, source="the self-test",
                                read_on="n/a")
    tick = iter([f"2026-09-0{n}T00:00:0{n}Z" for n in range(1, 9)])
    real = Ledger(Caps(spend={"openai": 100.0, "google": 0.0}, interval={}),
                  now=lambda: next(tick))
    with real.call("openai", "probe/big", input_estimate=100_000,
                   output_allowance=100_000, documents=NO_DOCUMENT) as charge:
        charge(input_tokens=100_000, output_tokens=100_000)
    snap = real.snapshot()
    check(abs(snap["dollars"]["openai"] - 1.80) < 1e-9,
          f"the snapshot must carry the ledger's own figure, got {snap['dollars']}")
    check(snap["window"]["from"] == "2026-09-01T00:00:01Z" and len(snap["rows"]) == 1,
          f"the snapshot must carry a window and its rows, got {snap['window']}")
    check(snap["must_not_be_billed"] == ["google"],
          f"a $0.00 cap must travel with the snapshot, got {snap['must_not_be_billed']}")
    check("probe/big" in snap["prices"] and snap["prices"]["probe/big"]["read_on"],
          "the snapshot must carry the table it costed against, dates included")
    check(json.loads(json.dumps(snap)) == snap, "the snapshot must be JSON-round-trippable")

    def verdicts(charged, **kw):
        return {ln.vendor: ln for ln in reconcile(snap, charged, **kw)}

    # must-not-fire: the dashboard agrees to the cent.
    ok = verdicts({"openai": 1.80, "google": 0.0})
    check(ok["openai"].verdict == AGREES and ok["google"].verdict == AGREES,
          f"an agreeing dashboard must reconcile, got {[v.verdict for v in ok.values()]}")
    # must-not-fire: a cent of rounding is rounding.
    check(verdicts({"openai": 1.81, "google": 0.0})["openai"].verdict == AGREES,
          "a cent of rounding must not stop the run")

    # must-fire: the 1000x unit error, which is the whole reason for this check.
    slipped = verdicts({"openai": 1800.00, "google": 0.0})["openai"]
    check(slipped.verdict == DISAGREES, f"a 1000x under-report must stop the run, "
                                        f"got {slipped.verdict}")
    check("1000x" in slipped.note and "per-1K" in slipped.note,
          f"a 1000x discrepancy must be named as a unit error, got {slipped.note!r}")

    # must-fire: two figures that both round to nothing agree on nothing.
    tiny = {"window": {}, "dollars": {"openai": 0.0001}, "must_not_be_billed": []}
    blind = reconcile(tiny, {"openai": 0.0})[0]
    check(blind.verdict == UNANSWERABLE,
          f"a probe below the dashboard's resolution must not read as agreement, "
          f"got {blind.verdict}")
    check("$0.01" in blind.note,
          f"and must say how big the probe has to be: {blind.note!r}")

    # must-fire: a vendor nobody asked the dashboard about is unreconciled. It
    # must get a line saying so - dropping it from the table is the same bug
    # wearing a tidier output.
    unasked = verdicts({"openai": 1.80}).get("google")
    check(unasked is not None and unasked.verdict == UNANSWERABLE,
          f"an unqueried vendor must get an UNANSWERABLE line, not be omitted: "
          f"{unasked}")

    # must-fire: the zero-cap vendor on a bill. No tolerance, no band.
    billed = verdicts({"openai": 1.80, "google": 0.02})["google"]
    check(billed.verdict == MUST_NOT_BE_BILLED,
          f"a $0.00-capped vendor appearing on a bill must stop the run, got {billed}")

    # The rendering is the deliverable: figures, not "checked".
    text = render(snap, list(verdicts({"openai": 1.80, "google": 0.0}).values()))
    check("1.8000" in text and "PROCEED" in text,
          f"the reconciliation must render as figures, got {text!r}")
    stopped = list(verdicts({"openai": 1800.0, "google": 0.0}).values())
    check("STOP" in render(snap, stopped), "a disagreement must render as STOP")

    # Reach, not only shape. The `Path` import this branch needs was missing and
    # every value probe above stayed green, because none of them went through
    # `main`. The CLI is what runs at the stop, so the CLI is what gets probed:
    # exit 0 on agreement, exit 1 on the unit error, over a real snapshot file.
    with tempfile.TemporaryDirectory() as tmp:
        written = Path(tmp) / "snapshot.json"
        written.write_text(json.dumps(snap), encoding="utf-8")
        cli = [sys.executable, str(Path(__file__).resolve()), "--reconcile", str(written)]
        agree = subprocess.run(cli + ["--charged", "openai=1.80", "--charged", "google=0"],
                               capture_output=True, text=True)
        check(agree.returncode == 0 and "PROCEED" in agree.stdout,
              f"the CLI must exit 0 on an agreeing dashboard, got {agree.returncode} "
              f"{agree.stdout.strip()[:120]!r} {agree.stderr.strip()[:200]!r}")
        stop = subprocess.run(cli + ["--charged", "openai=1800", "--charged", "google=0"],
                              capture_output=True, text=True)
        check(stop.returncode == 1 and "STOP" in stop.stdout,
              f"the CLI must exit 1 on a 1000x discrepancy, got {stop.returncode} "
              f"{stop.stdout.strip()[:120]!r} {stop.stderr.strip()[:200]!r}")
        check(not stop.stderr.strip(), "and must refuse cleanly rather than "
              f"traceback: {stop.stderr.strip()[:200]!r}")
    del PRICES["probe/big"]

    del PRICES["probe/free"]
    for line in failures:
        print(f"  FAIL {line}")
    if failures:
        return 1
    print("  spend: every cap fires - spend, zero-dollar vendor, call ceiling, "
          "token ceiling, unpriced SKU, unregistered vendor - and a free call, "
          "a failed call, pacing and serial execution behave; the vendor gate is "
          "on the call path, has no default, and refuses uncommitted material; "
          "reconciliation catches a 1000x unit error, a billed zero-cap vendor, "
          "an unqueried vendor and a probe too small to be answerable")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--reconcile", metavar="SNAPSHOT.json",
                    help="a snapshot written by Ledger.snapshot()")
    ap.add_argument("--charged", action="append", default=[], metavar="VENDOR=DOLLARS",
                    help="what the vendor's dashboard says was billed over the "
                         "snapshot's window. Repeat per vendor.")
    ap.add_argument("--resolution", type=float, default=DASHBOARD_RESOLUTION,
                    help="smallest figure the dashboard displays (default 0.01)")
    args = ap.parse_args()
    if not args.reconcile:
        return self_test()

    snapshot = json.loads(Path(args.reconcile).read_text(encoding="utf-8"))
    charged = {}
    for pair in args.charged:
        vendor, _, dollars = pair.partition("=")
        if not _ :
            print(f"  FAIL --charged wants VENDOR=DOLLARS, got {pair!r}")
            return 1
        charged[vendor.strip()] = float(dollars.replace("$", "").strip())
    lines = reconcile(snapshot, charged, resolution=args.resolution)
    print(render(snapshot, lines))
    # Exit code is the gate. A disagreement stops the run, and
    # it stops it here rather than in whoever remembers to read the table.
    return 0 if all(line.ok for line in lines) else 1


if __name__ == "__main__":
    raise SystemExit(main())
