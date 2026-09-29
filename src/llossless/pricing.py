"""Dollars per million tokens, and where each figure came from.

Moved here from `tests/spend.py` (488), which is where it was built and the
wrong place for it to live: a table the *product* needs to answer "what did
this merge cost" cannot sit in the test tree, and `src/` may not import from
there. `spend.py` imports it back, so the vendor-arm harness, the probes and
their tests read the same rows they always did.

Stdlib only, like every other module here.

**The three-state rule this exists to keep.** A run's cost is one of: a
figure, *unpriced* because nothing here knows the rate, or *unmeasured*
because the calls reported no tokens. None of those is `$0.00`. A zero would
read as "measured, and free", which is the inversion `DECISIONS.md` entry 480
already had to fix once in `counts`.

So `price_for` raises on an unknown SKU rather than returning a free row, and
`estimate` reports what it could not price instead of leaving it out of the
total silently.
"""

from __future__ import annotations

from dataclasses import dataclass


class UnknownPrice(RuntimeError):
    """A SKU with no entry in the table. Aborts rather than assuming free."""



@dataclass(frozen=True)
class Price:
    """Dollars per million tokens, and where the figure came from.

    `read_on` and `source` are not documentation. A price with no date is not
    checkable, and the run that used it cannot be re-costed later; the paper
    cites this table, so every row has to carry its own provenance the way a
    bibliography entry does.

    `max_input` exists because a rate is not a property of a SKU alone. OpenAI
    bills the same model at two rates depending on how long the prompt is, in a
    second column headed "Long context" that sits beside the one everybody
    reads. A table with one input rate per SKU silently under-costs every call
    above the threshold, and under-costing is the direction a cap cannot
    survive. So a row states the input length its rate is good for, and `cost`
    refuses rather than guessing above it.
    """
    input: float
    output: float
    source: str
    read_on: str
    cached_input: float | None = None
    max_input: int | None = None


# Read 2026-08-31. Each figure was read twice, in two separate passes over a
# freshly fetched page, and the UNIT was re-confirmed on the second pass rather
# than carried over from the first - a transcription error cannot catch itself,
# and the failure `_unit_error` names is exactly a per-1K figure entered against
# a per-1M table. Units, verbatim from the pages: OpenAI "Prices per 1M
# tokens."; Anthropic "/ MTok" with "All prices are in USD"; Google "per 1M
# tokens in USD". `cost` divides by 1_000_000, so per-million is the table's
# unit by construction and a per-1K entry would read 1000x low.
#
# Two traps on OpenAI's page, both of which produce a plausible wrong number:
#   - four price blocks per SKU (Standard / Batch / Flex / Fast mode). For
#     gpt-5.6-sol they are $4/$20, $2/$10, $2/$10, $8/$40. Standard is the one
#     billed for an ordinary synchronous call and the one entered here.
#   - two columns per block, Short context and Long context, roughly 2x apart.
#     The short-context rate is entered, because that is what these calls will
#     actually be billed, and `max_input` stops a call that would leave it.
#
# Promotional pricing carries end dates and these rows will go stale: OpenAI
# states gpt-5.6-sol's promotional pricing holds "at least through November 21,
# 2026", and Google's $0.75 rate becomes $1.50 on January 1, 2027. Re-read
# before any run dated after those.
_OPENAI = "https://platform.openai.com/docs/pricing"   # openai.com/api/pricing/ 403s
_ANTHROPIC = "https://docs.claude.com/en/docs/about-claude/pricing"
_GOOGLE = "https://ai.google.dev/gemini-api/docs/pricing"

# max_input is a deliberate under-estimate. The Long context column's threshold
# was not extracted cleanly from the page, so rather than enter a boundary from
# recollection this sets one comfortably below any plausible value. Aborting a
# call that would in fact have been billed at the short rate is the harmless
# direction; the other direction under-costs by 2x. Confirm and raise it before
# any arm sends a long prompt. Probe inputs are ~2K tokens, far below this.
_OPENAI_SHORT_CONTEXT = 100_000

PRICES: dict[str, Price] = {
    "probe/canary-1m": Price(input=1.0, output=1.0,
                             source="not a real model; the self-test's own row",
                             read_on="n/a"),

    # OpenAI, Standard tier, Short context column. Prices per 1M tokens.
    "openai/gpt-5.6-luna": Price(input=0.20,          # per 1M, confirmed twice
                                 cached_input=0.02,   # per 1M
                                 output=1.20,         # per 1M
                                 max_input=_OPENAI_SHORT_CONTEXT,
                                 source=_OPENAI, read_on="2026-08-31"),
    "openai/gpt-5.6-terra": Price(input=2.00,         # per 1M, confirmed twice
                                  cached_input=0.20,  # per 1M
                                  output=12.00,       # per 1M
                                  max_input=_OPENAI_SHORT_CONTEXT,
                                  source=_OPENAI, read_on="2026-08-31"),

    # Added 2026-09-25 for the vendor re-run. Both ids are listed by this
    # account's `GET /v1/models` and named on their model pages
    # (platform.openai.com/docs/models/gpt-6-sol, .../gpt-6-luna). Read twice
    # from two fetches of the pricing page, the HTML and its `.md` rendering,
    # the unit re-confirmed on the second ("Prices per 1M tokens."): Standard
    # tier, Short context column. No promotional end date is stated for either;
    # the page's "at least through November 21, 2026" line names GPT-5.6 Sol.
    # The model pages put the long-context boundary at "more than 272K input
    # tokens", so `_OPENAI_SHORT_CONTEXT` stays a safe under-estimate of it.
    "openai/gpt-6-sol": Price(input=2.00,             # per 1M, confirmed twice
                              cached_input=0.20,      # per 1M
                              output=10.00,           # per 1M
                              max_input=_OPENAI_SHORT_CONTEXT,
                              source=_OPENAI, read_on="2026-09-25"),
    "openai/gpt-6-luna": Price(input=0.10,            # per 1M, confirmed twice
                               cached_input=0.01,     # per 1M
                               output=0.50,           # per 1M
                               max_input=_OPENAI_SHORT_CONTEXT,
                               source=_OPENAI, read_on="2026-09-25"),

    # Anthropic. Quoted "/ MTok", i.e. per 1M tokens. No context-length split.
    "anthropic/claude-haiku-4-5-20251001": Price(
        input=1.00,          # per MTok, confirmed twice
        cached_input=0.10,   # per MTok (cache read)
        output=5.00,         # per MTok
        source=_ANTHROPIC, read_on="2026-08-31"),
    "anthropic/claude-sonnet-5": Price(
        input=2.00,          # per MTok, confirmed twice
        cached_input=0.20,   # per MTok (cache read)
        output=10.00,        # per MTok
        source=_ANTHROPIC, read_on="2026-08-31"),

    # Added 2026-09-17 after the capability sweep confirmed both models drive
    # all three roles end to end. The pricing table lists Opus 5, 4.8, 4.7,
    # 4.6 and 4.5 at identical figures; cache read is its "Cache hits and
    # refreshes" column, the documented 0.1x of base input.
    "anthropic/claude-opus-5": Price(
        input=5.00,          # per MTok, confirmed twice
        cached_input=0.50,   # per MTok (cache read)
        output=25.00,        # per MTok
        source=_ANTHROPIC, read_on="2026-09-17"),
    "anthropic/claude-opus-4-8": Price(
        input=5.00,          # per MTok, confirmed twice
        cached_input=0.50,   # per MTok (cache read)
        output=25.00,        # per MTok
        source=_ANTHROPIC, read_on="2026-09-17"),
    # Added 2026-09-25; listed by this account's `GET /v1/models`. Read twice
    # from two fetches of the pricing page ("/ MTok", "All prices are in USD");
    # its cache hits are 0.05x base input, not the 0.1x of the rows above. The
    # same reads found Opus 5 unchanged at $5 / $25.
    "anthropic/claude-opus-5-5": Price(
        input=4.00,          # per MTok, confirmed twice
        cached_input=0.20,   # per MTok (cache read, 0.05x)
        output=20.00,        # per MTok
        source=_ANTHROPIC, read_on="2026-09-25"),

    # Google, added 2026-09-25 for the free-tier run (DECISIONS 624). These are
    # the PAID tier's rates, and no call of that run was billed at them: the
    # key has no credit loaded and every call went to the free tier ("Free of
    # charge" for input and output on both models). They are here so a report
    # can say what the same calls would cost on the paid tier, and so that a
    # Google call priced by this table is priced above zero -- which the
    # $0.00 Google cap in `tests/spend.py` refuses before the call is sent.
    # The harness that ran the free tier charged its calls to a separate,
    # run-local zero row, never to these.
    #
    # Read twice, 2026-09-25, from two fetches of the pricing page (its `.md`
    # rendering and the HTML), the unit re-confirmed on the second ("Paid
    # Tier, per 1M tokens in USD"): the Standard block, text input. Output is
    # "including thinking tokens". No context-length split on either model.
    # 3.8 Flash's rates are promotional: "$0.75 through December 31, 2026.
    # $1.50 starting January 1, 2027", output $3.75 then $7.50, cached input
    # $0.075 then $0.15. Re-read before any run dated 2027 or later.
    # Both ids are listed by this key's `GET /v1beta/models`.
    "google/gemini-3.8-flash": Price(
        input=0.75,          # per 1M, confirmed twice; $1.50 from 2027-01-01
        cached_input=0.075,  # per 1M (context caching)
        output=3.75,         # per 1M, confirmed twice; $7.50 from 2027-01-01
        source=_GOOGLE, read_on="2026-09-25"),
    "google/gemini-3.5-flash-lite": Price(
        input=0.30,          # per 1M, confirmed twice (text / image / video / audio)
        cached_input=0.03,   # per 1M (context caching)
        output=2.50,         # per 1M, confirmed twice
        source=_GOOGLE, read_on="2026-09-25"),
}


def price_for(sku: str) -> Price:
    if sku not in PRICES:
        raise UnknownPrice(
            f"no price on record for {sku!r}. Add it to src/llossless/pricing.py "
            f"(this module's own PRICES table, since 488 -- tests/spend.py only "
            f"re-exports it) from the vendor's pricing page, with the URL and "
            f"the date you read it. An unpriced model aborts the run rather "
            f"than being charged at zero."
        )
    return PRICES[sku]


def cost(sku: str, *, input_tokens: int, output_tokens: int,
         cached_tokens: int = 0) -> float:
    """Dollars for one call. Cached input is billed at its own rate when known.

    When a vendor reports cached input and the table has no cached rate for the
    SKU, the cached tokens are charged at the full input rate. Over-charging is
    the safe direction for a cap: it can only make the run stop sooner.

    Above `max_input` the row's rate is not the rate the vendor will bill, so
    this raises instead of returning a number that looks fine. `UnknownPrice`
    is the right class: the price for a prompt that long genuinely is not on
    record here.
    """
    price = price_for(sku)
    if price.max_input is not None and input_tokens > price.max_input:
        raise UnknownPrice(
            f"{sku!r} is priced here for inputs up to {price.max_input:,} tokens "
            f"and this call is {input_tokens:,}. The vendor bills a second, "
            f"higher rate above its long-context threshold, so the rate on "
            f"record would under-cost this call. Read the long-context column "
            f"from {price.source} and add a row for it before running this."
        )
    billed_input = input_tokens - cached_tokens
    total = (billed_input * price.input + output_tokens * price.output) / 1_000_000
    rate = price.input if price.cached_input is None else price.cached_input
    return total + cached_tokens * rate / 1_000_000


# The self-test's own row is never a price for a real run. A model that
# happened to be called `canary-1m` would otherwise be costed at $1/$1 per
# million by a table row that exists only so `test_spend.py` can prove the cap
# fires. Excluded by prefix rather than by name, so a second probe row added
# later is excluded too.
_NOT_A_VENDOR = ("probe/",)


def sku_for(model: str) -> str | None:
    """The table key for a model id, or `None` when nothing here prices it.

    Matched on the part after the provider prefix, exactly. A run knows the
    model it asked for and does not always know which vendor served it -- a
    custom endpoint is the ordinary case -- so requiring the caller to supply
    a provider would make the common path unpriceable for no gain.

    Ambiguity is `None`, not a guess. Two vendors serving a model of the same
    name at different rates is exactly the case where picking one silently is
    worse than saying nothing: the figure would be wrong and would look
    authoritative. `None` reaches the reader as *unpriced*, which is true.
    """
    wanted = (model or "").strip()
    if not wanted:
        return None
    hits = [sku for sku in PRICES
            if not sku.startswith(_NOT_A_VENDOR)
            and sku.split("/", 1)[-1] == wanted]
    return hits[0] if len(hits) == 1 else None


@dataclass(frozen=True)
class Estimate:
    """What a run cost, or why there is no figure.

    Three states and no fourth, because a cost display has exactly one way to
    mislead: showing `$0.00` for a run nobody could price. `dollars` is `None`
    whenever no call was both measured and priced, and the two counts beside
    it say which of the two reasons applied -- they are different facts and a
    reader can act on them differently. An unpriced model needs a table row;
    an unmeasured call needs a vendor that reports usage, and no table will
    fix it.

    `partial` is the case that would otherwise be read as a total: some calls
    priced and others not. The figure is real and it is a floor, and a report
    that showed it without saying so would understate the run.
    """

    dollars: float | None
    priced_calls: int = 0
    unpriced_calls: int = 0
    unmeasured_calls: int = 0
    unpriced_models: tuple[str, ...] = ()
    # Which table rows this run's own priced calls actually billed against
    # (680, report-details item). Not every SKU the table has ever priced --
    # `provenance._cost_block` used to read `rates_read_on` off the whole
    # table and report the *oldest* date anywhere in it, which named a rate
    # this run never touched the moment any other SKU had an older reading.
    # Sorted and de-duplicated, in call order otherwise.
    priced_skus: tuple[str, ...] = ()

    @property
    def partial(self) -> bool:
        """A figure that is a floor rather than a total."""
        return self.dollars is not None and bool(
            self.unpriced_calls or self.unmeasured_calls)

    @property
    def calls(self) -> int:
        return self.priced_calls + self.unpriced_calls + self.unmeasured_calls

    @property
    def state(self) -> str:
        """`none`, `priced`, `partial`, `unpriced` or `unmeasured`. Never `free`.

        `none` is a run that made no call at all -- a dry run, or a `verify`
        that answered from nothing. It is separated from `unpriced` because
        "nothing was called" and "what was called cannot be priced" are
        different answers, and only the second is a gap in this table.
        """
        if not self.calls:
            return "none"
        if self.dollars is None:
            return "unmeasured" if self.unmeasured_calls and not self.unpriced_calls \
                else "unpriced"
        return "partial" if self.partial else "priced"


def estimate(ledger: list[dict]) -> Estimate:
    """Cost a run from its own ledger rows, one call at a time.

    Per call rather than from the run's totals, because a run can put three
    roles on three models at three rates, and a single total divided by one
    rate is a number with no referent. The ledger already carries the model on
    every row for exactly this kind of question.

    A row missing *either* `prompt_tokens` or `completion_tokens` is
    unmeasured -- `client._record_usage` writes each token key only when the
    vendor reported it (480), so either one's absence is the vendor's silence
    rather than a zero. Before 680 this checked for both keys absent, so a row
    that reported prompt tokens and nothing else was priced at
    `output_tokens=0`: a real answer costing nothing and an endpoint that
    never said what it produced are different facts, and only the table row
    that actually knows both halves may be priced from them (report-details
    item, entry 138's rule applied here).

    `UnknownPrice` from `cost` is caught and counted, not raised. It is raised
    in the harness because a run about to be billed must stop; here the caller
    is a report describing a run that already happened, and refusing to render
    it would be the wrong answer to "I cannot price this".
    """
    dollars = 0.0
    priced = unpriced = unmeasured = 0
    models: list[str] = []
    skus: list[str] = []
    for row in ledger:
        if "prompt_tokens" not in row or "completion_tokens" not in row:
            unmeasured += 1
            continue
        model = str(row.get("model", ""))
        sku = sku_for(model)
        if sku is None:
            unpriced += 1
            if model and model not in models:
                models.append(model)
            continue
        # A row whose total exceeds input plus output carries output the
        # vendor did not count as output: Google's thinking tokens (624).
        # Billed as output, so costed as output; never below the count given.
        output = int(row.get("completion_tokens", 0))
        if "total_tokens" in row:
            output = max(output, int(row["total_tokens"]) - int(row.get("prompt_tokens", 0)))
        try:
            dollars += cost(
                sku,
                input_tokens=int(row.get("prompt_tokens", 0)),
                output_tokens=output,
                cached_tokens=int(row.get("cached_tokens", 0)),
            )
        except UnknownPrice:
            unpriced += 1
            if model and model not in models:
                models.append(model)
            continue
        priced += 1
        if sku not in skus:
            skus.append(sku)
    return Estimate(
        dollars=dollars if priced else None,
        priced_calls=priced,
        unpriced_calls=unpriced,
        unmeasured_calls=unmeasured,
        unpriced_models=tuple(models),
        priced_skus=tuple(sorted(skus)),
    )
