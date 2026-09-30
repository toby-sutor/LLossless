#!/usr/bin/env python3
"""Offline checks for the merge pass and its harness. No network, no model.

Two halves. The first exercises `src/llossless/merge.py` against a real
loopback endpoint (tests/fake_endpoint.py), because the things worth checking
about this pass — that a truncated document errors instead of arriving as a
short one, that the document comes back byte for byte — are properties of the
whole path through the client and not of a function that was handed a dict.

The second half is `tests/run_merge.py`'s grading, which is where the merge
pass's honesty actually lives: the transfer rule, the uniform forward rule, the reduced
denominator, and the `identical` status. None of it needs inference, so none of
it is measured by the sweep — it is asserted here and the sweep inherits it.

Run with `python3 tests/test_merge.py`, or collect with pytest.
"""

from __future__ import annotations

import argparse
import contextlib
import inspect
import io
import itertools
import json
import re
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Installed before anything else runs, so a test that points a
# socket anywhere but the configured endpoint fails loudly instead of
# succeeding quietly. tests/test_socket_guard.py asserts every module does this.
socket_guard.install()

from llossless import (  # noqa: E402
    cassette, config, decompose, merge, parsing, prompts, reconcile, segment,
    structured, transport, window,
)
from llossless.cassette import MissingCassette  # noqa: E402
from llossless.client import (  # noqa: E402
    SEED, TEMPERATURE, Client, Completion, SCHEMA_ATTEMPTS, SchemaFailure,
)
from llossless.console import Console  # noqa: E402
from llossless.decompose import Claim  # noqa: E402
from llossless.provenance import Provenance  # noqa: E402
from llossless.verify import GROUNDED, NOT_GRADED, SOURCE_TO_MERGED, Verdict  # noqa: E402

import journal  # noqa: E402
import run_merge  # noqa: E402
from fake_endpoint import FakeEndpoint, envelope  # noqa: E402

failures: list[str] = []

SOURCE_A = "The relay listens on port 8443.\nThe connect timeout is 30 seconds.\n"
SOURCE_B = "The relay listens on port 8443.\nThe read timeout is 45 seconds.\n"
TWO = {"source_a.md": SOURCE_A, "source_b.md": SOURCE_B}
# Spelled out above and derived here, so the two agree by assertion rather than
# by having been typed the same way.
assert tuple(TWO) == merge.source_names(2)
FIRST = merge.source_names(2)[0]

# The level every budget below is taken at unless it is the level under test.
# `merge_documents` uses the policy's, and `MergePolicy` defaults to this one.
# The strict level, pinned rather than read from the default. The default
# moved to `high`; every assertion below that says LEVEL is about what `off`
# does -- the budget pair, the permitted dispositions, the fragment texts --
# and none of them was ever about whichever level a flagless run happens to
# take. `test_the_default_level_is_high` is where the default is asserted.
LEVEL = "off"


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def raises(exception, call, message: str):
    try:
        call()
    except exception as exc:
        return exc
    except Exception as exc:  # noqa: BLE001
        failures.append(f"{message} (raised {type(exc).__name__}: {exc})")
        return None
    failures.append(f"{message} (nothing raised)")
    return None


@contextlib.contextmanager
def endpoint(responder):
    """A live loopback endpoint and a Client wired to it, with the cache off."""
    with tempfile.TemporaryDirectory() as raw, FakeEndpoint(responder) as base_url:
        settings = config.Settings(
            base_url=base_url,
            models={"merge": "test-model", "decompose": "test-model", "verify": "test-model"},
            cache_dir=Path(raw) / "cache",
            use_cache=False,
        )
        yield Client(settings)


def merged(text: str, decisions: list | None = None, dispositions: list | None = None) -> str:
    """A well-formed v2 merge payload. All three fields, because all three are required.

    Both lists default to empty rather than absent, which is the honest default
    for these two sources: nothing was chosen between and nothing departed. An
    absent key would test a payload the schema forbids.
    """
    return json.dumps({
        "merged_document": text,
        "decisions": decisions or [],
        "dispositions": dispositions or [],
        # Required at every level, and empty is the honest answer
        # here for the same reason the two lists above are: these documents
        # are two versions of one thing, which is what the fixtures are.
        "mismatch": "",
    })


# --------------------------------------------------------------------------
# the pass
# --------------------------------------------------------------------------


def test_the_conflict_rule_fires_on_exclusive_values_and_not_on_compatible_ones() -> None:
    """The rule asked whether two values differ; it now asks
    whether they can both be true.

    The old wording fired on a real pair five times and not one firing was a
    disagreement: a date in one document and a time of day in the other, a
    gift named loosely and named precisely, two phrasings of one closing
    greeting, two registers of one name, and one restatement. Three of the
    five also restated a fact the merged document already carried, so the
    document asserted something and then said it could not decide it.

    Read off the file rather than asserted as a literal, for the reason
    `test_verify.py` gives about the label set: the point is that the file
    says it. The must-fire case is `conflict_surfaced`, whose two connect
    timeouts cannot both hold; the must-not-fire cases are the classes the
    carve-out has to name, or a model reading only the first sentence
    reproduces the old behaviour.
    """
    # Collapsed before matching, for `blindspots.py:274`'s reason: these are
    # sentences in a wrapped prose file, and an assertion pinned to where the
    # wrap falls today fails the next time someone reflows a paragraph without
    # changing a word of it.
    text = re.sub(r"\s+", " ", prompts.load("merge").text)
    check("cannot both be true" in text,
          "merge.md must trigger on mutual exclusivity, not on difference")
    check("Where documents give different values for the same attribute" not in text,
          "the old difference-based trigger must be gone, not merely supplemented")
    check("Ask whether a reader could believe both statements at once" in text,
          "merge.md must give the test a model can apply, not only the rule")
    for compatible in ("Two wordings of one fact", "two details that hold at once",
                       "a general statement narrowed by", "not disagreements"):
        check(compatible in text,
              f"the carve-out must name this class or the rule stays over-broad: "
              f"{compatible!r}")
    # A genuine conflict is still refused every way it could be softened, and
    # combining is named because `reconciled` exists: a reader must not take
    # that disposition as a licence to invent a middle value. The phrase is
    # qualified rather than absolute -- `open` may carry a value covering both
    # candidates -- and what stays refused at every level is a value of your
    # own, one that neither document wrote and no rule lets you declare.
    for refused in ("average them", "split the difference",
                    "combine them into a value of your own"):
        check(refused in text, f"a real disagreement must still refuse {refused!r}")
    # "Never pick a winner" used to be absolute. Picking is now the one thing
    # that is level-dependent: `high` chooses and the levels below keep both,
    # so the base rule defers it rather than forbidding it, and the absolute
    # refusals are the three numeric softenings above, which no level licenses.
    check("what the merge does about it is set" in text
          and "the lower levels keep both statements" in text,
          "the base rule must defer the choice to the level rather than forbid it")
    check("Never pick a winner" not in text,
          "picking is level-dependent now; an absolute refusal here would "
          "contradict high's own instruction")

    # The must-fire case, tied to the corpus rather than to this file's opinion.
    merged = (ROOT / "tests" / "fixtures" / "conflict_surfaced" / "merged.md").read_text()
    check("30 seconds" in merged and "60 seconds" in merged,
          "conflict_surfaced must still carry both connect timeouts")
    check("Unresolved" in merged,
          "conflict_surfaced must still surface its disagreement; if this fails the "
          "fixture moved and the must-fire case for the narrowed rule moved with it")


def test_the_inference_rule_is_level_conditional_and_absolute_against_invention() -> None:
    """The carve-out is in the base, not in a
    fragment overriding an invariant from below.

    `merge.md` states the rules that hold at every level, and a fragment that
    contradicted one of them would leave the model holding two instructions
    with no stated precedence. So the level-sensitivity is written into the
    invariant itself: what moves with the level is what *support* means, and
    what does not move is that something must support the sentence. A fact
    drawn from the model's own knowledge is refused at every level including
    high, which is the half of this rule that stage 2 must not erode.
    """
    text = re.sub(r"\s+", " ", prompts.load("merge").text)
    check("Rules that hold at every fidelity level:" in text,
          "the invariant block must still be called that")
    check("do not infer a fact from two others" in text,
          "the prohibition must survive for the levels that keep it")
    for level in ("off, low and mid", "at high and open"):
        check(level in text,
              f"the inference rule must name which levels it binds: {level!r}")
    # And a sixth level cannot arrive unnamed. The two phrases above are the
    # current partition; this is the property they spell out, so the test fails
    # on a level added without being placed on one side of the joint-support
    # line or the other -- which is the state `open` was briefly in, permitted
    # to combine by its own fragment and told otherwise by the block above it.
    for level in config.FIDELITY_LEVELS:
        check(level in text,
              f"merge.md's invariant block never says where {level!r} stands on "
              f"joint support, so a model at that level is not told")
    check("a single source statement on its own" in text,
          "off, low and mid must require support from one statement, not two")
    check("support a statement jointly" in text,
          "high must be the level where joint support is permitted")
    # The half that never moves. Stage 2 widens what `high` may combine; it
    # must not widen this, and a test that only checked the permission would
    # not notice if it did.
    check("alone or jointly" in text,
          "no level may permit a fact no document supports either way")
    check("is an invention at every level without exception" in text,
          "merge.md must carry the invariant the levels share: a fact no document "
          "supports and no rule lets you declare is an invention everywhere")
    # `merge.md` is rendered above *every* fidelity fragment, `open`'s
    # included, so a universal claim here is read in the same breath as the
    # fragment that contradicts it. Three sentences did exactly that. Each was
    # true when written and false the moment a level gained the licence to add,
    # and nothing failed -- the level shipped its fragment, the base prompt kept
    # its prohibition, and the model was told both. These are those sentences.
    # A new universal belongs on this list before it goes in the file.
    for banned in ("no level permits one drawn from your own knowledge",
                   "combine them into one value",
                   "including high:"):
        check(banned not in text,
              f"merge.md states as universal something a level now permits, and "
              f"the fragment below it will contradict this: {banned!r}")
    # Every level still renders, and none of them is handed the placeholder.
    for level in config.FIDELITY_LEVELS:
        fragment = prompts.load(f"fidelity/{level}.merge").text
        rendered = prompts.load("merge").render(
            fidelity_rules=fragment, title_rule="TITLE", base_filename=FIRST,
            sources=segment.render_sources(segment.segment_sources(TWO), FIRST))
        check("{fidelity_rules}" not in rendered,
              f"the {level} render must substitute its fragment")
        check("do not infer a fact from two others" in re.sub(r"\s+", " ", rendered),
              f"the {level} render must still carry the prohibition it qualifies")


def test_prompt_renders_its_four_placeholders_and_the_sources_by_name() -> None:
    """The prompt takes a rendered document list, not two slots.

    A two-slot prompt has nowhere to put a third document, and the disposition
    contract needs document ids to point at. The *gate* is still two sources --
    `check_sources` refuses anything else -- so the prompt can be ready for N
    before the fixture suite is.
    """
    prompt = prompts.load("merge")
    for placeholder in ("{fidelity_rules}", "{title_rule}", "{base_filename}", "{sources}"):
        check(placeholder in prompt.text, f"merge.md must carry a {placeholder} placeholder")
    for gone in ("{source_a}", "{source_b}", "{source_a_filename}", "{source_b_filename}"):
        check(gone not in prompt.text, f"merge.md must no longer carry {gone}")

    rendered = prompt.render(
        fidelity_rules="RULES",
        title_rule="TITLE",
        base_filename=FIRST,
        sources=segment.render_sources(segment.segment_sources(TWO), FIRST),
    )
    for sentence in ("The relay listens on port 8443.", "The read timeout is 45 seconds."):
        check(sentence in rendered, f"the sources' sentences must reach the prompt: {sentence!r}")
    for placeholder in ("{fidelity_rules}", "{title_rule}", "{base_filename}", "{sources}"):
        check(placeholder not in rendered, f"{placeholder} must be substituted, not left in")
    sources = segment.render_sources(segment.segment_sources(TWO), FIRST)
    check(sources.count('base="true"') == 1,
          f"exactly one document is shown as the base, not {sources.count('base=')}")
    # A base nobody was shown is worse than no base: the prompt names a filename
    # in `{base_filename}` and no document carries the attribute, so the model is
    # told to follow the structure of a document it cannot identify.
    raises(
        ValueError,
        lambda: segment.render_sources(segment.segment_sources(TWO), "merged.md"),
        "render_sources must refuse a base that is not one of the documents",
    )

    raises(
        KeyError,
        lambda: prompt.render(source_a="X"),
        "render must reject a placeholder merge.md does not have",
    )
    # `render` substitutes what it is given and rejects what it does not
    # recognise; it cannot know a caller forgot one. So an omitted placeholder
    # leaves its token in the text, and what actually stops that reaching a
    # model is merge_documents rendering all four -- checked over the wire below.
    check("{sources}" in prompt.render(base_filename="X"),
          "an omitted placeholder stays visible rather than becoming an empty document")


def test_schema_is_the_document_and_the_two_record_lists() -> None:
    """The merge now declares what it did, and the shape is closed.

    Three required fields, in this order. `decisions` and `dispositions` are
    required even though an empty list is a legitimate answer for either,
    because an absent key and an empty list read the same to a human and
    differently to a checker: with the key required, "no departures" is a claim
    the model made, and the reconciler can hold every segment to it. Optional,
    it would be indistinguishable from a model that ignored the instruction.

    Field order inside each record is emission order, and a grammar-constrained
    model fills them in the order the schema lists. Value before justification,
    the same discipline `verify.VERDICT_SCHEMA` enforces: with the reason first,
    the record is whatever the argument's last clause happened to be.
    """
    schema = merge.MERGE_SCHEMA
    check(list(schema["properties"]) == ["merged_document", "decisions",
                                         "dispositions", "mismatch"],
          f"three fields, document first: {list(schema['properties'])}")
    check(schema["properties"]["merged_document"]["type"] == "string",
          "the merged document is a string")
    check(schema["required"] == ["merged_document", "decisions",
                                 "dispositions", "mismatch"],
          f"all three must be required: {schema['required']}")
    check(schema["additionalProperties"] is False, "the schema must be closed")

    disposition = schema["properties"]["dispositions"]["items"]
    check(tuple(disposition["properties"]) == parsing.DISPOSITION_FIELDS,
          f"disposition field order is the contract: {tuple(disposition['properties'])}")
    check(disposition["properties"]["disposition"]["enum"] == list(parsing.DISPOSITIONS),
          f"the departure values are a closed enum: {disposition['properties']}")
    check("retained" not in parsing.DISPOSITIONS,
          "retained is never declared -- silence is the claim, and a string comparison checks it")
    # `reconciled` owes one like the rest: its replacement is the combined
    # statement, and a reconciliation with nothing to point at is exactly the
    # shape an invention would take if the declaration were allowed to be
    # empty. Only `dropped` points at nothing, because nothing is what it means.
    check(parsing.REPLACED == ("reworded", "superseded", "subsumed", "duplicate",
                               "reconciled"),
          f"every value but dropped owes a replacement: {parsing.REPLACED}")
    check(disposition["properties"]["replacement"]["type"] == "string",
          "replacement is a string and empty for dropped, not null; one type, one emptiness test")
    check(disposition["properties"]["replacement"]["maxLength"] == parsing.REPLACEMENT_MAX,
          f"the schema carries the replacement cap so a grammar-constrained model is "
          f"stopped at it: {disposition['properties']['replacement']}")
    check(disposition["properties"]["reason"]["maxLength"] == parsing.REASON_MAX,
          f"the schema carries the reason cap too: {disposition['properties']['reason']}")
    check(disposition["additionalProperties"] is False, "a disposition record is closed")

    decision = schema["properties"]["decisions"]["items"]
    check(tuple(decision["properties"]) == parsing.DECISION_FIELDS,
          f"decision field order is the contract: {tuple(decision['properties'])}")
    check(tuple(decision["properties"]["candidates"]["items"]["properties"])
          == parsing.CANDIDATE_FIELDS,
          "a candidate is its text and the document it came from, in that order")
    check(decision["properties"]["reason"]["maxLength"] == parsing.REASON_MAX,
          "both record types share one reason cap")
    check(decision["additionalProperties"] is False, "a decision record is closed")

    # The five values the schema offers are the five the prompt lists, checked
    # against the prompt file rather than against a second copy of the tuple. A
    # rule written twice is not checked twice; this is the check.
    text = prompts.load("merge").text
    for value in parsing.DISPOSITIONS:
        check(f"{value} " in text or f"{value}\n" in text,
              f"merge.md must name the {value} disposition it can be given")
    # Both record types carry a reason and `_check_reason` holds both to the same
    # cap, so the prompt has to state it twice. It used to state it once,
    # on the disposition record, and a decision reason was capped by a rule the
    # model was never shown -- enforced in two places and written in one, which is
    # the inverse of the usual failure and just as silent.
    check(text.count(f"maximum {parsing.REASON_MAX} characters") == 2,
          f"merge.md must state the {parsing.REASON_MAX}-character reason cap for both "
          f"record types, found {text.count(f'maximum {parsing.REASON_MAX} characters')}")

    # The verbatim rule used to read "numeric
    # values with their units", which left a bare count outside it, and the
    # reconciler's `verbatim` check has never consulted the unit, so an unaccompanied
    # number was checked against a rule the model was not given. That is a finding
    # the model was never warned about, which reads as a model failure and is not.
    check("whether or not they carry a unit" in text,
          "merge.md's verbatim rule must cover numeric values with no unit; "
          "reconcile.verbatim checks them either way")
    # The replacement cap, and the shape a longer span is given in. Both figures and
    # the marker, because a model told the cap and not the form answers a long
    # span by truncating it, and a truncated span still resolves -- silently
    # naming less of the merge than the record meant.
    check(str(parsing.REPLACEMENT_MAX) in text,
          f"merge.md must state the {parsing.REPLACEMENT_MAX}-character replacement cap")
    check(str(parsing.ANCHOR_HALF) in text and parsing.ELISION.strip() in text,
          f"merge.md must give the anchor form: {parsing.ANCHOR_HALF} each end, "
          f"joined by {parsing.ELISION.strip()!r}")


def test_the_merge_policy_defaults_to_off_and_refuses_a_level_that_does_not_exist() -> None:
    """The default is decided, not conservative-by-habit.

    A rewording the caller did not ask for is indistinguishable downstream from
    a fact quietly restated: the reverse pass sees generated wording and has to
    judge whether it is invention. At `off` it does not have to judge.

    The policy is its own object rather than `Settings` because the two things
    that consume it — the merge call, and the reconciler that decides which
    dispositions are permitted — consume nothing else from the runtime
    configuration, and a pure reconciler holding an API key variable name would
    be carrying what it can never use.
    """
    check(config.FIDELITY_LEVELS == ("off", "low", "mid", "high", "open", "sourced"),
          f"the six levels are fixed and ordered: {config.FIDELITY_LEVELS}")
    # `high` is the default, kept and pointed the other way rather than deleted: the
    # default decides what a flagless run is, and at `off` that is a diff with
    # a verifier attached rather than a merge tool. `off` remains the strict
    # mode five registrations hold constant, and every block passes --fidelity
    # explicitly, so this constant reaches no registered property.
    check(config.DEFAULT_FIDELITY == "high", "the default level is high")
    check(merge.MergePolicy().fidelity == "high",
          "an unspecified policy takes the default, which is high")

    for level in config.FIDELITY_LEVELS:
        check(merge.MergePolicy(fidelity=level).fidelity == level, f"{level} must round-trip")
    raises(
        config.ConfigError,
        lambda: merge.MergePolicy(fidelity="medium"),
        "a level that does not exist must be refused at construction, not at render time",
    )

    # Env and flag, both, and the flag wins. `LLOSSLESS_FIDELITY` is validated
    # in `from_env` rather than left to argparse, because nothing validates an
    # env var for you and an unknown level would otherwise reach the fragment
    # loader as a filename.
    settings = config.from_env({"LLOSSLESS_FIDELITY": "MID "}, model_map_path=Path("/nowhere"))
    check(settings.fidelity == "mid", f"the env var must be read and normalised: {settings!r}")
    check(merge.MergePolicy.from_settings(settings).fidelity == "mid",
          "the policy must be derivable from settings without re-reading the environment")
    raises(
        config.ConfigError,
        lambda: config.from_env({"LLOSSLESS_FIDELITY": "medium"},
                                model_map_path=Path("/nowhere")),
        "an unknown level in the environment must be refused",
    )
    check(config.from_env({}, model_map_path=Path("/nowhere")).fidelity
          == config.DEFAULT_FIDELITY,
          "an unset env var is the default, not an error")


def test_verbatim_is_the_published_name_for_off_and_off_still_works() -> None:
    """The rename, both directions. A person reads `verbatim`, the wire says `off`.

    `--fidelity off` reads as "turn fidelity checking off" when it means
    "rewriting off", and it is the strictest setting -- so the level is
    published as `verbatim`. The wire spelling did not move with it, because
    151 recorded cassettes, every graded run record (withheld with the paper) and the operator's own
    scripts are written in `off`, and the alias is not on a deprecation clock.
    """
    check(config.FIDELITY_LEVELS == ("off", "low", "mid", "high", "open", "sourced"),
          f"the wire names and their order are untouched: {config.FIDELITY_LEVELS}")
    check(config.FIDELITY_PUBLISHED == ("verbatim", "low", "mid", "high", "open", "sourced"),
          f"the published names, in the same order: {config.FIDELITY_PUBLISHED}")
    check(set(config.FIDELITY_CHOICES)
          == {"verbatim", "low", "mid", "high", "open", "sourced", "off"},
          f"both spellings are accepted: {config.FIDELITY_CHOICES}")

    for spelling, wire in (("verbatim", "off"), ("off", "off"), ("high", "high")):
        check(config.canonical_fidelity(spelling) == wire,
              f"{spelling!r} must resolve to the wire name {wire!r}")
    check(config.fidelity_name("off") == "verbatim" and config.fidelity_name("mid") == "mid",
          "the published name is the way back, and it is total on the levels")

    # Everything that takes a level takes either spelling and means one run.
    check(merge.MergePolicy(fidelity="verbatim").fidelity == "off",
          "a policy built on the alias resolves to the wire name, once, at construction")
    check(reconcile.PERMITTED["verbatim"] == reconcile.PERMITTED["off"],
          "PERMITTED must resolve for both spellings")
    # Against `FIDELITY_LEVELS`, not against a literal count. The point of the
    # check is that the alias resolves without joining the iteration -- one more
    # level must not need one more edit here, and a fifth already did.
    check(tuple(reconcile.PERMITTED) == config.FIDELITY_LEVELS
          and len(reconcile.PERMITTED) == len(config.FIDELITY_LEVELS),
          f"and must still iterate as the wire names alone: "
          f"{tuple(reconcile.PERMITTED)}")
    check(merge.composes("verbatim") == merge.composes("off"),
          "and so must everything that reads it")
    settings = config.from_env({"LLOSSLESS_FIDELITY": " VERBATIM "},
                               model_map_path=Path("/nowhere"))
    check(settings.fidelity == "off",
          f"the environment takes the alias too, and normalises it: {settings.fidelity!r}")


def test_an_aliased_run_keys_to_the_same_cassette_as_an_off_run() -> None:
    """The rename's stop-and-report condition. If this fails, every recording orphans.

    Fidelity is not a `key_for` argument: it reaches the key through the
    rendered prompt, the schema and `max_tokens`. So "the alias is the same
    run" is not a statement about `canonical_fidelity`, it is a statement about
    those three, and it is asserted on the key itself rather than on the
    resolution that is supposed to produce it.

    The second half is what makes the first mean anything: the levels must
    still key to *different* cassettes, one each. An assertion that only checked
    `off == verbatim` would pass just as well on a key that had stopped reading
    the level at all.
    """
    documents = {"source_a.md": "# Notes\n\nThe timeout is 30 seconds.\n"
                                "Operators may pause a queue.\n",
                 "source_b.md": "# Notes\n\nThe timeout is 60 seconds.\n"
                                "The archive tier is read-only.\n"}

    def key(spelling: str) -> str:
        policy = merge.MergePolicy(fidelity=spelling)
        prompt, rules, example, title_rule = merge.compose_prompt(policy, None)
        segmented = segment.segment_sources(documents)
        rendered = prompt.render(
            fidelity_rules=rules, fidelity_example=example, title_rule=title_rule,
            base_filename="source_a.md",
            sources=segment.render_sources(segmented, "source_a.md"))
        return cassette.key_for(
            role="merge", model="qwen/qwen3-8b", tier="native",
            prompt_sha256=prompt.sha256,
            messages=[{"role": "user", "content": rendered}],
            schema=merge.merge_schema(policy.fidelity),
            temperature=TEMPERATURE, seed=SEED,
            max_tokens=merge.budget_tokens(documents, policy.fidelity),
            thinking=False, sample=0, profile=structured.DEFAULT_PROFILE,
        )

    check(key("verbatim") == key("off"),
          f"an aliased run must key to the cassette an `off` run keys to, or "
          f"every recording orphans: {key('verbatim')} vs {key('off')}")
    keys = {level: key(level) for level in config.FIDELITY_LEVELS}
    check(len(set(keys.values())) == len(config.FIDELITY_LEVELS),
          f"and every level must still key to a cassette of its own: {keys}")


def test_the_title_policy_is_synthesise_by_default_and_travels_the_same_road() -> None:
    """Same mechanism as fidelity, and unordered where that is not.

    `keep-base` and `choose-best` are two policies rather than two rungs: there
    is no "more" of a title. That is why they live in their own tuple with their
    own default instead of being folded into the fidelity ladder, where a reader
    would reasonably assume the fourth entry permits everything the third does.

    The default was `keep-base` for the reason `off` is the fidelity default: a
    merge that picks its own heading produces a line neither source states
    verbatim, and something then has to decide whether a title is a factual
    claim. At `keep-base` nothing had to decide.

    That reason expired: the deciding procedure now has
    `merge.verify_title` grade a written title as a claim against both sources
    and report `CONTRADICTED` or `MISSING` as a finding, so the thing the
    default was avoiding is now the thing that is tested. `synthesise` is a
    superset rather than a looser rung: its own prompt says taking the base
    document's title unchanged "is always a correct answer at this level and is
    never penalised", so every `keep-base` answer remains correct under it.

    The change moves no published figure. `run_bench.py`, `run_arm.py` and
    `run_vendor_arm.py` all pass `--title-policy keep-base` explicitly, and
    `title_policy` is not a component of the cassette key, so nothing recorded
    is re-keyed and nothing reproducible moves. What it costs is one short model
    call per merge, and only when the model actually writes a title.
    """
    check(config.TITLE_POLICIES == ("keep-base", "choose-best", "synthesise"),
          f"the policies are fixed: {config.TITLE_POLICIES}. `synthesise` was "
          f"added last and is the only one permitting a written "
          f"title, and the only one whose titles `reconcile` does not decide: "
          f"adding a policy means deciding which half checks it")
    check(config.DEFAULT_TITLE_POLICY == "synthesise", "the default policy is synthesise")
    check(merge.MergePolicy().title_policy == "synthesise", "an unspecified policy is synthesise")

    for policy in config.TITLE_POLICIES:
        check(merge.MergePolicy(title_policy=policy).title_policy == policy,
              f"{policy} must round-trip")
        check(prompts.load(f"title/{policy}").text.strip() != "",
              f"prompts/title/{policy}.md must exist and be non-empty")
    raises(
        config.ConfigError,
        lambda: merge.MergePolicy(title_policy="keep-longest"),
        "a policy that does not exist must be refused at construction, not at render time",
    )
    check(prompts.load("title/keep-base").text != prompts.load("title/choose-best").text,
          "the two policies must be two different rules, not one file named twice")

    settings = config.from_env({"LLOSSLESS_TITLE_POLICY": "CHOOSE-BEST "},
                               model_map_path=Path("/nowhere"))
    check(settings.title_policy == "choose-best",
          f"the env var must be read and normalised: {settings!r}")
    raises(
        config.ConfigError,
        lambda: config.from_env({"LLOSSLESS_TITLE_POLICY": "keep-longest"},
                                model_map_path=Path("/nowhere")),
        "an unknown policy in the environment must be refused",
    )
    # Against the constant, not a literal. `test_the_title_policy_is_synthesise_
    # by_default_and_travels_the_same_road` is the one place the default's value
    # is pinned; a second literal here only means two edits every time it moves,
    # and this check is about the unset case rather than about which value it is.
    check(config.from_env({}, model_map_path=Path("/nowhere")).title_policy
          == config.DEFAULT_TITLE_POLICY,
          "an unset env var is the default, not an error")

    # Both halves of the policy come off `Settings` together. Carrying one and
    # defaulting the other is the failure that reports a level correctly while
    # merging under a title rule nobody chose.
    both = config.from_env(
        {"LLOSSLESS_FIDELITY": "high", "LLOSSLESS_TITLE_POLICY": "choose-best"},
        model_map_path=Path("/nowhere"),
    )
    check(merge.MergePolicy.from_settings(both) == merge.MergePolicy("high", "choose-best"),
          f"from_settings must carry both fields: {merge.MergePolicy.from_settings(both)!r}")


def test_the_title_rule_reaches_the_prompt_and_moves_the_key() -> None:
    """The fragment is substituted and hashed, exactly as fidelity is.

    Two assertions that look alike and are not. The first is about `messages` —
    the rule text has to reach the endpoint, or the policy is a report field
    describing nothing. The second is about `prompt_sha256` — the digest has to
    move, or a report names `merge.md` and cannot say which of two policies
    produced the run.

    The cassette keys separate on `messages` either way, which is why **no field
    goes on `key_for` for this** any more than for fidelity.
    """
    sent: dict[str, list[dict]] = {}

    def capture(request, _n):
        sent.setdefault("bodies", []).append(request)
        return 200, envelope(merged("ok"))

    contents: dict[str, str] = {}
    keys: dict[str, str] = {}
    for policy in config.TITLE_POLICIES:
        with endpoint(capture) as client:
            merge.merge_documents(client, TWO, policy=merge.MergePolicy(title_policy=policy))
            keys[policy] = client.last_key
        contents[policy] = sent["bodies"][-1]["messages"][-1]["content"]
        rule = prompts.load(f"title/{policy}").text
        check(rule.strip() in contents[policy],
              f"the {policy} rule text must reach the endpoint, not just the report")

    check(contents["keep-base"] != contents["choose-best"],
          "the two policies must send two different prompts")
    check(keys["keep-base"] != keys["choose-best"],
          f"the two policies must record under two cassette keys, got {keys}")

    digests = {policy: merge.compose_prompt(merge.MergePolicy(title_policy=policy))[0].sha256
               for policy in config.TITLE_POLICIES}
    check(len(set(digests.values())) == len(config.TITLE_POLICIES),
          f"every title fragment must reach the composed digest, one key "
          f"each: {digests}")
    check(prompts.load("merge").sha256 not in set(digests.values()),
          "a composed digest must differ from the bare prompt's under either policy")


def test_the_declared_loss_budget_does_not_reach_the_prompt_or_the_key() -> None:
    """The inverse of the test above, and the reason it exists.

    `title_policy` moves the cassette key because it changes the request. The
    declared-loss budget must not, because it is not part of the request at
    all: it is a grading threshold applied to the answer after it arrives.
    Keying on it would re-key all 264 m4 cassettes and orphan the corpus on a
    flag that cannot change what the model was asked.

    Three budgets over the same sources, and both halves are asserted because
    they fail separately. Equal bodies with different keys would mean the value
    reached `key_for` directly; equal keys with different bodies would mean it
    reached the prompt and the key was blind to it.
    """
    sent: list[dict] = []

    def capture(request, _n):
        sent.append(request)
        return 200, envelope(merged("ok"))

    keys, bodies = [], []
    for budget in (0.0, config.DEFAULT_DECLARED_LOSS_BUDGET, 0.5, 1.0):
        with endpoint(capture) as client:
            merge.merge_documents(
                client, TWO,
                policy=merge.MergePolicy(declared_loss_budget=budget),
            )
            keys.append(client.last_key)
        bodies.append(sent[-1])

    check(len(set(keys)) == 1,
          f"four budgets must record under one cassette key; got {sorted(set(keys))}")
    check(all(body == bodies[0] for body in bodies),
          "and must send one request; the budget is graded against the answer, "
          "not asked of the model")

    # Named rather than counted: a future field added to `key_for` should fail
    # here with the name it added, not with a number that has to be looked up.
    registered = ("role", "model", "tier", "prompt_sha256", "messages", "schema",
                  "temperature", "seed", "max_tokens", "thinking", "sample",
                  # The request envelope: which of the fields to its left
                  # actually go on the wire. Omitted from the hash at its
                  # default, so it named no recording that was already on disk
                  # -- `test_cassette_key_derivation_is_pinned` holds both
                  # halves of that.
                  "profile",
                  # And which mechanism answered. Absent from the hash at
                  # its default on exactly the same terms: every recording on
                  # disk was made over HTTP, so naming it would rename all of
                  # them to say something already true of them.
                  "command")
    actual = tuple(inspect.signature(cassette.key_for).parameters)
    check(actual == registered,
          f"the cassette key is these components and no others; got {actual}")


def test_each_level_names_its_own_fragment_and_they_are_four_different_texts() -> None:
    """The level is a file, not a branch in Python.

    Rules that tell a model what it may rewrite belong in the prompt directory
    with the other prompts, where a hash identifies them and a diff shows what
    changed. Four files also means the levels can say different things without
    a conditional anywhere in `merge.py`.
    """
    fragments = {level: merge.MergePolicy(fidelity=level).fragment()
                 for level in config.FIDELITY_LEVELS}

    for level, fragment in fragments.items():
        check(fragment.path.exists(), f"prompts/fidelity/{level}.merge.md must exist")
        check(fragment.text.strip() != "", f"the {level} fragment must not be empty")
        check(fragment.name == f"fidelity/{level}.merge",
              f"the fragment must be named for its level and role, got {fragment.name!r}")

    texts = [fragment.text for fragment in fragments.values()]
    check(len(set(texts)) == len(config.FIDELITY_LEVELS),
          f"every level must be a text of its own, got {len(set(texts))} distinct")
    digests = {fragment.sha256 for fragment in fragments.values()}
    check(len(digests) == len(config.FIDELITY_LEVELS),
          f"four texts must be four digests, got {len(digests)}")

    # The verbatim classes are level-invariant, which is the one property of
    # these four files a reader is entitled to rely on without reading them:
    # what a level buys is freedom over expression, never over a number. `off`
    # gets it for free by copying everything; the three above it have to say so,
    # and `high` says it by reference because the enumeration belongs in the
    # prompt rather than repeated four times. This is prose in a prompt and so
    # cannot be enforced, only checked: the mechanical guard is `reconcile`'s
    # `verbatim_violation` finding, which is an error and does not ask the model.
    check("character for character" in fragments["off"].text,
          "the off fragment must require character-for-character copying")
    for level in ("low", "mid", "high"):
        check("verbatim class" in fragments[level].text,
              f"the {level} fragment must name the verbatim classes as out of its licence")
    for level in ("low", "mid"):
        for kind in ("number", "unit", "URL", "file path", "version string", "command"):
            check(kind in fragments[level].text,
                  f"the {level} fragment must enumerate {kind!r} among the verbatim classes")

    # The role is part of the filename because one level has to be told to the
    # passes that grade the merge as well as to the one that writes it. Those
    # two are not yet wired up; what is asserted here is that the mapping exists and
    # that a role with no fragment fails loudly rather than falling back.
    raises(
        FileNotFoundError,
        lambda: merge.MergePolicy().fragment("decompose"),
        "a role with no fidelity fragment must be fatal, not silently unrestricted",
    )


def test_the_composed_digest_names_the_level_and_the_cassette_key_still_does_not() -> None:
    """The paragraph worth reading twice.

    `Prompt.sha256` hashes the **unrendered** file and `client.py:221` passes
    exactly that as `prompt_sha256`. Substituting a fragment therefore changes
    what the model is shown and changes nothing about the digest -- so a report
    would name `merge.md` and be unable to say which level produced the run. `compose` fixes the report and nothing else.

    What separates the levels in the corpus is `messages`, which already
    carries the rendered fragment. That is asserted below the composition, and
    asserted **with the base digest held constant**, so it is a claim about the
    message and not about the hash that happens to travel beside it.

    A field on `key_for` would do the same job and cost all 423 committed
    cassettes: the key is a sha over a fixed dict, so a new key changes the hash
    for every role, decompose's 357 included. The last check here is the guard
    on that -- it fails if anyone adds one.
    """
    base = prompts.load("merge")
    composed = {level: prompts.compose(base, merge.MergePolicy(fidelity=level).fragment())
                for level in config.FIDELITY_LEVELS}

    check(len({prompt.sha256 for prompt in composed.values()}) == len(config.FIDELITY_LEVELS),
          "each level must compose to its own digest")
    check(base.sha256 not in {prompt.sha256 for prompt in composed.values()},
          "a composed digest must differ from the bare prompt's, including at off")
    check(prompts.load("merge").sha256 == base.sha256,
          "compose must not mutate the prompt it was handed")
    for level, prompt in composed.items():
        check(prompt.text == base.text,
              f"compose changes the digest only; {level} must keep the prompt text")
        check(prompt.path == base.path and prompt.name == base.name,
              f"a composed prompt is still merge.md; {level} moved its identity")

    # Order is the caller's and is significant: two prompts that substitute the
    # same fragments into different placeholders are different prompts, so the
    # digest has to be able to tell them apart. What follows composes two fragments.
    off, high = (merge.MergePolicy(fidelity=level).fragment() for level in ("off", "high"))
    check(prompts.compose(base, off, high).sha256 != prompts.compose(base, high, off).sha256,
          "fragment order must reach the composed digest")
    # Composing nothing is the identity, and that is load-bearing rather than
    # incidental: a role that takes no fragment keeps the digest it has, so
    # wiring `compose` into a call site cannot orphan cassettes on its own. Only
    # actually having a fragment to substitute moves the key.
    check(prompts.compose(base).sha256 == base.sha256,
          "composing no fragments must leave the digest exactly where it was")

    # And the order `compose_prompt` actually uses, pinned rather than described.
    # It is fidelity then title, matching where the placeholders sit in
    # `merge.md`. Both orders are self-consistent, so nothing else in the suite
    # notices a swap -- it would simply re-key every merge cassette in silence.
    policy = merge.MergePolicy()
    composed_prompt, fidelity_rules, _example, title_rule = merge.compose_prompt(policy)
    check(composed_prompt.sha256 == prompts.compose(
              base, policy.fragment(), policy.fragment("example"),
              prompts.load(f"title/{policy.title_policy}")).sha256,
          "compose_prompt must hash merge.md, then the fidelity fragment, then "
          "that level's worked example, then the title one")
    check((fidelity_rules, _example, title_rule) == (
              policy.fragment().text, policy.fragment("example").text,
              prompts.load(f"title/{policy.title_policy}").text),
          "compose_prompt must return the same fragment texts it hashed")

    # End to end. Four calls that differ only in the substituted fragment, and
    # the base digest passed every time, so nothing but `messages` can separate
    # them -- and they must still land on four keys.
    keys: list[str] = []
    with endpoint(lambda body, n: (200, envelope(merged("m")))) as client:
        for level in config.FIDELITY_LEVELS:
            fragment = merge.MergePolicy(fidelity=level).fragment()
            client.complete(
                role="merge",
                prompt=base,
                messages=[{"role": "user", "content": f"rules:\n{fragment.text}"}],
                schema=merge.MERGE_SCHEMA,
                schema_name="emit_merge",
                max_tokens=64,
            )
            keys.append(client.last_key)
    check(len(set(keys)) == len(config.FIDELITY_LEVELS),
          f"every level must record under a cassette key of its own, got "
          f"{len(set(keys))} for {len(config.FIDELITY_LEVELS)} level(s): {keys}")

    check(set(inspect.signature(cassette.key_for).parameters) == {
        "role", "model", "tier", "prompt_sha256", "messages", "schema",
        "temperature", "seed", "max_tokens", "thinking", "sample", "profile",
        "command",
    }, f"key_for gained or lost a component: {sorted(inspect.signature(cassette.key_for).parameters)}")


def test_budget_is_sized_from_the_sources_and_never_zero() -> None:
    """The budget is the payload plus a flat reasoning allowance, in both conditions."""
    small = merge.budget_tokens({"source_a.md": "a\n", "source_b.md": "b\n"}, LEVEL)
    large = merge.budget_tokens({"source_a.md": "a" * 6000, "source_b.md": "b" * 6000}, LEVEL)
    check(small > merge.REASONING_ALLOWANCE,
          f"a two-character merge still gets room above the allowance, got {small}")
    check(large > small, "a longer pair of sources must get a larger budget")
    check(small % merge.BUDGET_STEP == 0 and large % merge.BUDGET_STEP == 0,
          "budgets are rounded to whole steps")

    # The escaping is what the model actually emits, so it is what is counted:
    # the same 800 characters cost twice as many once every one of them needs a
    # backslash.
    plain = merge.budget_tokens({"source_a.md": "x" * 800, "source_b.md": "y"}, LEVEL)
    escaped = merge.budget_tokens({"source_a.md": '"' * 800, "source_b.md": "y"}, LEVEL)
    check(escaped > plain, "a document full of escapes must cost more than one without")

    # Segment count is the other half, and it moves the budget on its own: the
    # same characters split into more segments buy more declared records.
    one = merge.budget_tokens({"source_a.md": "x " * 400, "source_b.md": "y"}, LEVEL)
    many = merge.budget_tokens({"source_a.md": "x\n" * 400, "source_b.md": "y"}, LEVEL)
    check(many > one,
          f"the same text in 400 segments must cost more than in one, got {many} and {one}")

    # `config.FIDELITY_LEVELS` promises the levels are ordered: everything
    # permitted at one is permitted at every level above it, so the budget they
    # size must be ordered too, and a level must never ask for less than the one
    # below. `low` and `mid` coming out equal is not a gap: `reconcile.PERMITTED`
    # gives them the same row, and a figure derived from it cannot separate them.
    pair = {"source_a.md": "x " * 400, "source_b.md": "y " * 400}
    ladder = [merge.budget_tokens(pair, level) for level in config.FIDELITY_LEVELS]
    check(ladder == sorted(ladder),
          f"the budget must not fall as fidelity rises: {dict(zip(config.FIDELITY_LEVELS, ladder))}")
    check(ladder[0] < ladder[-1],
          f"off forbids composed replacements and must be cheaper than high, got {ladder}")


def worst_case_payload(documents: dict[str, str], fidelity: str) -> str:
    """The largest response this schema plausibly permits for these sources
    at this level.

    Built from the sources, `parsing`'s contract and `reconcile.PERMITTED` alone
    -- it must not consult `merge.budget_tokens`, `merge.GENERATED` or any of the
    budget's constants, or the acceptance below would be the formula agreeing
    with itself. `PERMITTED` is shared with the budget on purpose and is the one
    thing both sides may read: it is the rule, and a worst case built from some
    other rule would be a worst case for some other tool.

    What makes it worst-case, field by field. The document is both sources whole
    (nothing dropped) plus half again, which is the merge restating a disputed
    value under two attributions. Every segment is declared -- the `high` case --
    with the longest disposition word its level allows and a reason at its cap.
    The replacement is where the level enters: a level that permits `reworded` or
    `subsumed` can answer with wording it composed, so the worst case is the
    segment restated at the same headroom; a level that permits neither can only
    point at wording that already exists, so the worst case is the segment
    itself. Either way it goes through `parsing.anchor`, which is the contract
    and not the budget: a longer answer is refused by `check_merge` and cannot be
    part of any worst case that parses. And every segment also carries a decision, each weighing that segment
    against one from every other document and quoting the winner in full, which is
    the pessimistic reading of a field the schema does not bound: a decision needs
    alternatives, so there cannot really be one per segment, but nothing in the
    schema says so. The candidate list is one entry per document rather than two,
    because that is what the schema permits at three sources and what a budget
    charging two would truncate.
    """
    names = tuple(documents)
    sources = segment.segment_sources(documents)
    segments = [item for source in sources for item in source.segments]

    def restated(text: str) -> str:
        return text + text[: len(text) // 2]

    # One cycle per document, so every decision draws a candidate from each: the
    # longest document sets the length of each column and the shorter ones repeat.
    columns = [itertools.cycle(source.segments) for source in sources]
    # `dropped` is declarable at every level: it is a review-queue
    # entry, not an illegal answer, so it belongs in every level's worst case
    # even though `PERMITTED` lists it nowhere. It is the cheap one, so the
    # `max` below never picks it; it is here so the set is the true one.
    declarable = reconcile.PERMITTED[fidelity] + ("dropped",)
    composed = bool({"reworded", "subsumed"} & set(declarable))
    return json.dumps({
        # The worst case is a *filled* mismatch, not an empty one: the model
        # may write its capped sentence on any response, and a worst case that
        # assumed silence would under-budget exactly the run that used it.
        "mismatch": "x" * parsing.REASON_MAX,
        "merged_document": restated("".join(documents.values())),
        "decisions": [
            {
                "slot": "x" * merge.SLOT_MAX,
                "candidates": [
                    {"text": text, "document": name}
                    for name, text in zip(names, row)
                ],
                "chosen": max(row, key=len),
                "reason": "x" * parsing.REASON_MAX,
            }
            for row in ([next(column).text for column in columns] for _ in segments)
        ],
        "dispositions": [
            {
                "segment": item.id,
                "disposition": max(declarable, key=len),
                "replacement": parsing.anchor(
                    restated(item.text) if composed else item.text),
                "reason": "x" * parsing.REASON_MAX,
            }
            for item in segments
        ],
    })


def test_an_unknown_fidelity_level_is_refused_rather_than_defaulted() -> None:
    """A typo must not silently buy the cheapest ceiling in the table."""
    try:
        merge.budget_tokens(TWO, "medium")
    except merge.MergeError as exc:
        check("medium" in str(exc), f"the rejection must name the level, got {exc}")
    else:
        check(False, "an unknown fidelity level must raise, not fall back to a default")

    check("fidelity" in inspect.signature(merge.budget_tokens).parameters,
          "budget_tokens takes the level")
    check(inspect.signature(merge.budget_tokens).parameters["fidelity"].default
          is inspect.Parameter.empty,
          "the level has no default: a caller that omits it would size for another level")


def test_paraphrase_states_the_same_values_at_two_granularities() -> None:
    """What `paraphrase` shows about the decision-record bound, corrected.

    Bounding the decision count by
    `min(len(s.segments) for s in sources)` was considered and rejected on a
    counterexample taken from this fixture: source B's bullet side was
    said to carry two segments holding two distinct values each, against four
    separate prose segments of source A, so one segment was a candidate in two
    decisions.

    Those two segments were the segmenter's, not the fixture's. A fix to
    `_take_block`, which had been folding each unpunctuated bullet into the one
    below it, means source B's five defaults are now five list items carrying one
    value each. The counterexample is gone and this test says so rather than
    being deleted, as a guard against the same fusion defect returning.

    What the fixture still shows is the granularity mismatch itself, which is
    the reason the tool exists: the same six values, stated as prose in one
    document and as a list in the other, over a different number of segments.
    """
    documents = run_merge.load_sources("paraphrase")
    sources = {source.filename: source for source in segment.segment_sources(documents)}
    a, b = sources["source_a.md"], sources["source_b.md"]

    def values(item) -> set:
        return {span.text for span in item.spans_of(segment.NUMERIC, segment.VERSION)}

    def multi(document) -> tuple:
        return tuple(item for item in document.segments if len(values(item)) >= 2)

    # The property the fix above rests on, asserted in the negative so that a
    # regression of the fusion defect fails here as well as in test_segment.
    check(not multi(b),
          f"no segment of paraphrase's bullet side may carry two invariant values; "
          f"two of them did while `_take_block` fused adjacent bullets, "
          f"found {len(multi(b))}")
    check(not multi(a),
          f"nor its prose side, which spends one segment per value: {len(multi(a))}")

    # The same values on both sides, one segment each. That is the slot
    # structure a merge decides over, and it is 1:1 in this pair.
    on_a = {value: item.id for item in a.segments for value in values(item)}
    on_b = {value: item.id for item in b.segments for value in values(item)}
    check(set(on_a) == set(on_b) and len(on_a) == 6,
          f"both documents must state the same six values: {sorted(on_a)} against "
          f"{sorted(on_b)}")
    for document in (a, b):
        for value in on_a:
            carriers = [item.id for item in document.segments if value in values(item)]
            check(len(carriers) == 1,
                  f"value {value!r} must be stated by exactly one segment of "
                  f"{document.filename}, found {carriers}")

    # And they take a different number of segments to do it, which is the
    # mismatch. Left as an inequality rather than two counts: the fixture is
    # allowed to grow a sentence without this test being about that.
    check(len(b.segments) < len(a.segments),
          f"the bullet side is the smaller document: {len(b.segments)} against "
          f"{len(a.segments)}")


def test_the_budget_covers_a_worst_case_payload_for_every_fixture() -> None:
    """Asserted against a constructed payload, not estimated.

    The v2 schema has four more fields that can hold copied text than the one
    the old budget was sized for, and measurement showed the old
    figure running out around half the declared fraction. Truncation is
    self-detecting -- an unterminated JSON string errors the unit rather than
    reporting a half-merge as dropped facts -- but a recording run that detects
    it at hour three is still a recording run spent.

    So every fixture pair is held to the payload above, over the whole corpus
    rather than the largest one: the shortest sources have the fewest characters
    per segment, so they are where the per-record scaffolding is largest as a
    fraction and where a document-shaped budget goes wrong first.
    """
    names = run_merge.fixture_names()
    # Unrelated to the 14 in `run_arm.py` and `test_pairs.py`, which pin `== 14`
    # for a benchmark denominator: 7 pairs x 2 levels, a fixed registration.
    # This one is a count of directories under `tests/fixtures/`. The two
    # coincided until `concatenated` landed and nothing ties them, so
    # moving one must not look like a reason to move the other; that they now
    # differ is the safer state for exactly that reason.
    check(len(names) == 16, f"the suite is sixteen fixture directories, found {len(names)}")

    for name in names:
        documents = run_merge.load_sources(name)
        for level in config.FIDELITY_LEVELS:
            payload = worst_case_payload(documents, level)
            budget = merge.budget_tokens(documents, level)
            # The reasoning allowance is for the `<think>` block, which is charged
            # against the same ceiling, so it is not room the payload may spend.
            room = (budget - merge.REASONING_ALLOWANCE) * merge.CHARS_PER_TOKEN
            check(room >= len(payload),
                  f"{name} at {level}: budget {budget} leaves {room} chars for the "
                  f"payload, and a worst-case one is {len(payload)} -- this pair "
                  f"truncates mid-string")

    # And the guard against the cheap way to pass it: a budget that is simply
    # enormous would satisfy every line above and tell a reader nothing. The
    # largest fixture must still be within one order of magnitude of its own
    # worst case.
    for level in config.FIDELITY_LEVELS:
        largest = max(names, key=lambda name: merge.budget_tokens(
            run_merge.load_sources(name), level))
        documents = run_merge.load_sources(largest)
        need = len(worst_case_payload(documents, level)) / merge.CHARS_PER_TOKEN
        budget = merge.budget_tokens(documents, level)
        check(budget < need * 10,
              f"{largest} at {level} budgets {budget} tokens against a {need:.0f}-token "
              f"worst case; a budget that loose is not sized from anything")


def test_the_off_budget_is_a_real_reduction_and_says_what_it_costs() -> None:
    """From the other side: what `off` stops paying for, and the risk.

    The acceptance above only asks that each level cover the worst case it
    permits, which a budget that never went down would also satisfy. This asks
    that the reduction be real -- that at `off` there is a pair whose *composed*
    worst case no longer fits.

    That is the cost of the reduction, stated rather than discovered: a model that
    disobeys the level and rewrites at `off` can run past the ceiling and
    truncate, and a truncated response errors the unit instead of reaching the
    reconciler, which would have called it `disposition_not_permitted`. On all
    thirteen fixtures the rounding leaves enough slack that it cannot happen; on
    a pair a few times larger it can.
    """
    # Every fixture has this margin again. Requiring `mismatch` briefly cost
    # `disjoint_sources` its last 81 characters, and `MISMATCH_ALLOWANCE` gave
    # them back by paying `PER_MISMATCH` after the rounding rather than inside
    # it: a fixed per-response cost rounded in gives one fixture a whole
    # 256-token step and its neighbour none, which is also what broke the
    # registered tie between the two disjoint controls. No exemption stands
    # here now, and reintroducing one should be the last resort rather than the first.
    suite = [(name, run_merge.load_sources(name)) for name in run_merge.fixture_names()]
    for name, documents in suite:
        room = ((merge.budget_tokens(documents, "off") - merge.REASONING_ALLOWANCE)
                * merge.CHARS_PER_TOKEN)
        short = len(worst_case_payload(documents, "high")) - room
        check(short <= 0,
              f"{name} is close enough to its ceiling for an off-level violation "
              f"to truncate, short by {short:.0f}; if this ever fails, say so in "
              f"the README rather than resizing")

    # Built by repetition rather than taken from a real document, and built from
    # long segments rather than many: the per-segment accounting does not move
    # with the level, so a pair of a thousand short lines hides the effect no
    # matter how big it is. What shows it is a document that is mostly prose.
    filler = " ".join(f"word{n}" for n in range(120))
    body = "".join(f"The relay at site {n} reports that {filler}.\n" for n in range(60))
    large = {"source_a.md": f"# Relay Handbook\n\n{body}",
             "source_b.md": f"# Relay Notes\n\n{body}"}
    for level in config.FIDELITY_LEVELS:
        room = ((merge.budget_tokens(large, level) - merge.REASONING_ALLOWANCE)
                * merge.CHARS_PER_TOKEN)
        check(room >= len(worst_case_payload(large, level)),
              f"the large pair must still fit its own worst case at {level}")

    # The worst case has to vary with the level or the loop above is one
    # assertion written four times. `off` may only point at wording that exists,
    # so its payload is strictly the smaller.
    sizes = {level: len(worst_case_payload(large, level)) for level in config.FIDELITY_LEVELS}
    check(sizes["off"] < sizes["high"],
          f"the constructed worst case must be smaller at off than at high, got {sizes}")
    check(sizes["low"] == sizes["mid"] == sizes["high"],
          f"reconcile.PERMITTED gives low, mid and high the same generating dispositions, "
          f"so their worst cases are one payload; got {sizes}")

    # And what the reduction is worth, measured rather than claimed. It is small,
    # and small in a way that is the answer to a real question: the per-segment
    # accounting is level-invariant and it is the larger half of the figure, so
    # bounding `replacement` in the schema would buy more than the slider does.
    gap = 1 - merge.budget_tokens(large, "off") / merge.budget_tokens(large, "high")
    check(0 < gap < 0.25,
          f"off saves {gap:.1%} against high on a prose-heavy pair; if that ever leaves "
          f"this range the README's account of where the budget goes is out of date")


def spread(count: int, per_document: int = 40) -> dict[str, str]:
    """`count` sources of similar size, under the canonical names, for N tests."""
    filler = " ".join(f"word{n}" for n in range(30))
    return {
        name: f"# Handbook {letter}\n\n" + "".join(
            f"Site {letter}{n} reports that {filler}.\n" for n in range(per_document)
        )
        for letter, name in enumerate(merge.source_names(count))
    }


def test_a_merge_takes_two_or_more_sources_under_canonical_names() -> None:
    """Two is the floor, the names are the tool's, and the order counts."""
    for count in (2, 3, 5, merge.MAX_SOURCES):
        names = merge.source_names(count)
        check(len(set(names)) == count, f"{count} sources must get {count} distinct names")
        check(merge.check_sources(spread(count)) == names,
              f"a {count}-source mapping must be accepted and its names handed back")

    # This used to ask `source_names(27)` for `source_aa.md`; that path is closed:
    # past `MAX_SOURCES` the letters reach the merge's own. The contract that
    # assertion was really about is `segment.document_id` not running out, and
    # it is asserted directly at `tests/test_segment.py:149-150`, which the cap
    # does not touch.
    check(merge.source_names(merge.MAX_SOURCES)[-1] == "source_l.md",
          f"the last nameable source is source_l.md, got "
          f"{merge.source_names(merge.MAX_SOURCES)[-1]!r}")

    raises(
        merge.MergeError,
        lambda: merge.check_sources({"source_a.md": SOURCE_A}),
        "one document is not a merge and must be refused",
    )


def test_the_source_letters_stop_before_they_reach_the_merges_own() -> None:
    """Thirteen sources would name one `source_m.md`, and `m` is the merge's."""
    check(segment.document_id(merge.MAX_SOURCES) == reconcile.MERGE_LETTER,
          "MAX_SOURCES must be the index of the first letter the merge already owns, "
          f"got document_id({merge.MAX_SOURCES})="
          f"{segment.document_id(merge.MAX_SOURCES)!r} against "
          f"{reconcile.MERGE_LETTER!r}")
    check(segment.document_id(merge.MAX_SOURCES).upper() == decompose.MERGED_LETTER,
          "the same index must be the claim-letter collision, so one cap covers both")

    raises(
        merge.MergeError,
        lambda: merge.source_names(merge.MAX_SOURCES + 1),
        "a merge past MAX_SOURCES must be refused rather than given ambiguous ids",
    )
    try:
        merge.source_names(merge.MAX_SOURCES + 1)
    except merge.MergeError as exc:
        text = str(exc)
    check("source_m.md" in text and str(merge.MAX_SOURCES) in text,
          f"the refusal must name the colliding filename and the cap, got {text!r}")
    raises(
        merge.MergeError,
        lambda: merge.check_sources({}),
        "an empty mapping must be refused",
    )
    raises(
        merge.MergeError,
        lambda: merge.check_sources({"source_a.md": SOURCE_A, "source_b.md": "   \n"}),
        "a whitespace-only source must be refused",
    )
    # The names are the tool's, not the operator's: a real filename in the
    # mapping would render a prompt no figure here was measured under, and would
    # key its own cassette.
    raises(
        merge.MergeError,
        lambda: merge.check_sources({"source_a.md": SOURCE_A, "notes-b.md": SOURCE_B}),
        "a source under a name this pass did not choose must be refused",
    )
    # Order is not incidental. `segment.segment_sources` letters by position, so
    # a mapping whose keys are the right names in the wrong order would give
    # `source_b.md` the letter `a` and every disposition record would point at
    # the wrong document.
    raises(
        merge.MergeError,
        lambda: merge.check_sources({"source_b.md": SOURCE_B, "source_a.md": SOURCE_A}),
        "the canonical names out of order must be refused, not silently re-sorted",
    )
    check(merge.check_sources(TWO) == merge.source_names(2), "the pair is still accepted")


def test_the_budget_covers_the_worst_case_at_three_and_five_documents() -> None:
    """The many-document half: the ceiling has to know how many documents there are.

    `decisions[].candidates` holds one entry per document, so the response grows
    with the source count in a place the old constant charged flat at two. This
    is the same constructed-payload acceptance as the fixture loop above, run at
    counts no fixture exercises -- and it is the assertion that fails if anyone
    reinstates a fixed copy count.
    """
    for count in (2, 3, 5):
        documents = spread(count)
        for level in config.FIDELITY_LEVELS:
            payload = worst_case_payload(documents, level)
            budget = merge.budget_tokens(documents, level)
            room = (budget - merge.REASONING_ALLOWANCE) * merge.CHARS_PER_TOKEN
            check(room >= len(payload),
                  f"{count} sources at {level}: budget {budget} leaves {room} chars and "
                  f"the worst case is {len(payload)} -- a merge of {count} truncates")

    # And that the growth is real rather than absorbed by rounding: five equal
    # documents must cost more than two of them, per document as well as in total.
    per_document = [
        merge.budget_tokens(spread(count), LEVEL) / count for count in (2, 3, 5)
    ]
    check(per_document[0] < per_document[-1],
          f"the per-document budget must rise with the count, got {per_document}")
    check(merge.document_copies("high", 5)[0] == merge.FIXED_COPIES + 5,
          "five documents means five candidate slots on top of the three fixed fields")


def test_document_comes_back_byte_for_byte() -> None:
    """Everything downstream grounds spans against this string. Nothing may touch it."""
    document = "  # Merged\n\nThe relay listens on port 8443.\r\nTimeout: 30 s (A).\n\n\n"

    decisions = [{"slot": "title", "candidates": [{"text": "A", "document": "source_a.md"},
                                                  {"text": "B", "document": "source_b.md"}],
                  "chosen": "A", "reason": "The base document's title."}]
    dispositions = [{"segment": "b2", "disposition": "duplicate",
                     "replacement": "The relay listens on port 8443.",
                     "reason": "a1 already states it."}]

    with endpoint(
        lambda body, n: (200, envelope(merged(document, decisions, dispositions)))
    ) as client:
        out = merge.merge_documents(client, TWO)

    check(out.document == document,
          "the merged document must be returned exactly as the model wrote it")
    # The declarations come back with the document rather than beside it: a
    # replacement is a span of *this* document, so a caller holding the string
    # alone could not check that the pointers point into what it was given.
    check(out.decisions == tuple(decisions), f"the decisions must survive the call: {out!r}")
    check(out.dispositions == tuple(dispositions),
          f"the dispositions must survive the call: {out!r}")
    check(out.declared() == {"b2"}, f"declared() is the departed segment ids: {out.declared()}")
    check(merge.MergeResult("x").declared() == set(),
          "a merge that declared nothing has declared nothing, not a crash")

    sent_bodies: list[dict] = []

    def capture(request, _n):
        sent_bodies.append(request)
        return 200, envelope(merged("ok"))

    with endpoint(capture) as client:
        merge.merge_documents(client, TWO)

    body = sent_bodies[-1]
    check(body["max_tokens"] == merge.budget_tokens(TWO, LEVEL),
          f"max_tokens must be the fixture's budget, got {body.get('max_tokens')}")
    sent = body["messages"][-1]["content"]
    # Segmented, not raw, and asserted as whole lines. `merge.md`'s own worked
    # example is a segmented document, so it contains `a1| ` and `base="true"`
    # on its own -- a bare substring check for either passes on a call site that
    # sends the sources raw. The id has to be tested attached to the sentence it
    # numbers, which is the thing the reconciler later looks up by set
    # membership and cannot do against a document quoted freehand.
    for line in ("a1| The relay listens on port 8443.",
                 "a2| The connect timeout is 30 seconds.",
                 "b1| The relay listens on port 8443.",
                 "b2| The read timeout is 45 seconds."):
        check(line in sent, f"every source segment must reach the endpoint as a line: {line!r}")
    check('<document id="a" filename="source_a.md" base="true">' in sent,
          "the base document must reach the endpoint marked as the base")

    # `render` rejects a field the prompt has no slot for and cannot
    # know a caller forgot one, so the guard against a half-rendered prompt is
    # here rather than in `prompts.py`: an omitted keyword leaves its token in
    # the text and ships `{base_filename}` to the model as literal characters.
    for placeholder in ("{fidelity_rules}", "{title_rule}", "{base_filename}", "{sources}"):
        check(placeholder not in sent,
              f"{placeholder} reached the endpoint unsubstituted; the call site is stale")


def test_truncation_errors_rather_than_returning_a_partial_document() -> None:
    """A document cut at max_tokens is an unterminated JSON string. That is the point.

    Returned as plain text it would arrive as a merge that simply stops, and
    every fact after the cut would be reported as dropped by the merge model
    rather than by the budget.
    """
    cut = '{"merged_document": "The relay listens on port 84'
    with endpoint(lambda body, n: (200, envelope(cut))) as client:
        raises(
            SchemaFailure,
            lambda: merge.merge_documents(client, TWO),
            "a truncated document must error the unit of work, not shorten it",
        )


def test_empty_document_is_rejected() -> None:
    check(parsing.check_merge({"merged_document": "the merge"}) == [],
          "a real document passes the semantic check")
    check(parsing.check_merge({"merged_document": "  \n "}),
          "a whitespace-only document must be reported, not returned")

    with endpoint(lambda body, n: (200, envelope(merged("   ")))) as client:
        raises(
            SchemaFailure,
            lambda: merge.merge_documents(client, TWO),
            "an empty merge must error rather than being scored as dropping every fact",
        )


def test_check_merge_repairs_shape_and_never_decides_a_finding() -> None:
    """Where the line falls, because everything here is fed back as a prompt.

    `check_merge`'s errors go to the model verbatim on retry. So it may say a
    record could not be read -- a missing field, a value outside the closed set,
    a reason that was cut off, a replacement on a `dropped` -- and it may not say
    the merge is wrong. A replacement that does not resolve in the document, a
    segment id nobody issued, a disposition the level does not permit: those are
    findings the reconciler decides, and asking the model to fix one would be the
    tool negotiating its own result away. The reconciler owns all three.

    The field-order checks are here rather than left to the schema because the
    schema only enforces order on a tier with grammar support, and the tier
    ladder is allowed to fall back.
    """
    def payload(**fields):
        return {"merged_document": "the merge", "decisions": [], "dispositions": [], **fields}

    good_disposition = {"segment": "b2", "disposition": "duplicate",
                        "replacement": "the merge", "reason": "a1 already states it."}
    good_decision = {"slot": "title",
                     "candidates": [{"text": "A", "document": "source_a.md"},
                                    {"text": "B", "document": "source_b.md"}],
                     "chosen": "A", "reason": "The base document's title."}

    check(parsing.check_merge(payload(dispositions=[good_disposition],
                                      decisions=[good_decision])) == [],
          "a well-formed pair of records must pass unremarked")
    check(parsing.check_merge(payload()) == [],
          "declaring nothing is a legitimate answer, not an error")

    def one(record, key="dispositions"):
        return parsing.check_merge(payload(**{key: [record]}))

    # Field order. Same value, different emission sequence.
    reordered = {"segment": "b2", "reason": "a1 already states it.",
                 "disposition": "duplicate", "replacement": "the merge"}
    check(any("in that order" in error for error in one(reordered)),
          f"a record emitted out of order must be repaired: {one(reordered)}")

    # The closed set, checked here as well as in the schema because a tier
    # without grammar support will not hold the enum.
    for bad in ("retained", "REWORDED", "merged", ""):
        broken = {**good_disposition, "disposition": bad}
        check(any(".disposition" in error for error in one(broken)),
              f"{bad!r} is not one of the five and must be reported: {one(broken)}")
    for value in parsing.DISPOSITIONS:
        record = {**good_disposition, "disposition": value,
                  "replacement": "" if value == "dropped" else "the merge"}
        check(one(record) == [], f"{value} in its own correct shape must pass: {one(record)}")

    # The dependency the schema cannot express, both ways round.
    dropped_with = {**good_disposition, "disposition": "dropped", "replacement": "the merge"}
    check(any("leave replacement empty" in error for error in one(dropped_with)),
          f"a dropped that names a replacement must be repaired: {one(dropped_with)}")
    for value in parsing.REPLACED:
        empty = {**good_disposition, "disposition": value, "replacement": "  "}
        check(any("names no replacement" in error for error in one(empty)),
              f"{value} owes a replacement: {one(empty)}")

    # The cap itself is no longer this function's business. Pass B
    # moved it to `parsing.parse`'s pre-pass, which
    # runs before `check_merge` ever sees the record and caps the field in
    # place -- so a `replacement` this function reads has already been
    # shortened if it needed to be, and there is nothing left here to repair.
    # See `test_pre_pass_caps_length_violations_instead_of_rejecting_them`.
    span = "The relay listens on port 8443, and the read timeout is 45 seconds. "
    anchored = {**good_disposition, "replacement": parsing.anchor(span * 8)}
    check(one(anchored) == [],
          f"the anchored form of a long span must pass: {one(anchored)}")
    check(len(parsing.anchor(span * 8)) <= parsing.REPLACEMENT_MAX,
          "the anchor a model is asked for must itself be under the cap")
    check(parsing.anchor(span) == span,
          "a span already under the cap is given whole, elision being the exception")

    # One record per departed segment. Two records for one segment is a payload
    # nobody can act on: the reconciler would have to pick which claim to check.
    twice = parsing.check_merge(payload(dispositions=[good_disposition, good_disposition]))
    check(any("repeats b2" in error for error in twice),
          f"a repeated segment must be reported: {twice}")

    # The reason, on both record types. Presence only -- length moved to the
    # pre-pass along with `replacement`'s, for the same reason.
    for key, good in (("dispositions", good_disposition), ("decisions", good_decision)):
        check(any(".reason is empty" in error for error in one({**good, "reason": " "}, key)),
              f"{key} must owe a reason")
        long = {**good, "reason": "x" * (parsing.REASON_MAX + 1) + "."}
        check(one(long, key) == [],
              f"{key} no longer holds the length cap itself: {one(long, key)}")
        # And below the cap it must not, whatever the prose looks like. These are
        # the three arm-1 reasons that cost a settled unit in an earlier run.
        for terse in ("the base title was kept and this one was not",
                      "a2 already states it",
                      "the base document's title was kept"):
            check(len(terse) < parsing.REASON_MAX and parsing.unfinished(terse),
                  f"the fixture must be a sub-cap reason the predicate reads as cut: {terse!r}")
            check(one({**good, "reason": terse}, key) == [],
                  f"{key} must accept a terse reason below the cap: "
                  f"{one({**good, 'reason': terse}, key)}")

    # A decision is a record of a choice, so one candidate is not a decision.
    # Shape, not judgement: nothing here says which candidate was right.
    alone = {**good_decision, "candidates": [{"text": "A", "document": "source_a.md"}]}
    check(any("records a" in error for error in one(alone, "decisions")),
          f"a decision needs something to have chosen between: {one(alone, 'decisions')}")
    hollow = {**good_decision,
              "candidates": [{"text": "A", "document": " "}, {"text": "B", "document": "b.md"}]}
    check(any("candidates[0].document is empty" in error
              for error in one(hollow, "decisions")),
          f"a candidate must name the document it came from: {one(hollow, 'decisions')}")
    for field in ("slot", "chosen"):
        check(any(f".{field} is empty" in error
                  for error in one({**good_decision, field: " "}, "decisions")),
              f"a decision must give its {field}")

    # And the line itself. None of these three is check_merge's to raise.
    unresolved = {**good_disposition, "replacement": "a span that is not in the merge at all"}
    check(one(unresolved) == [],
          f"an unresolved pointer is the reconciler's finding, not a repair request: "
          f"{one(unresolved)}")
    invented = {**good_disposition, "segment": "z99"}
    check(one(invented) == [],
          f"an invented segment id is the reconciler's finding, not a repair request: "
          f"{one(invented)}")
    at_off = {**good_disposition, "disposition": "subsumed"}
    check(one(at_off) == [],
          f"a disposition the level forbids is the reconciler's finding: {one(at_off)}")


def test_a_decision_is_charged_only_for_a_choice_the_sources_offered() -> None:
    """The check reads the documents before it charges.

    `check_merge` demands that a decision "list every candidate the documents
    offered", and until the resolver existed it had no way to read the
    documents, so it charged a decision naming one candidate even where one
    was all there was. That was the dominant attrition cause in an early
    test run: five decisions rejected across two arms, four of them on slots offering a
    single candidate, costing three settled units.

    Both directions are asserted here, because the whole risk of this fix is
    that it stops the check firing on the case it was written for. Arm 1's one
    rejection resolved to a slot with **two** distinct titles available, and it
    must still fail.
    """
    def decision(count: int, slot: str = "title") -> dict:
        candidates = [{"text": text, "document": name} for text, name in
                      (("A", "source_a.md"), ("B", "source_b.md"))][:count]
        return {"slot": slot, "candidates": candidates, "chosen": "A",
                "reason": "The base document's title."}

    def errors(record: dict, available=None) -> list[str]:
        found = parsing.check_merge(
            {"merged_document": "the merge", "decisions": [record], "dispositions": []},
            available,
        )
        return [error for error in found if ".candidates has" in error
                or ".candidates is empty" in error]

    def resolver(fixture: str):
        sources = {name: (run_merge.FIXTURES_DIR / fixture / name).read_text(encoding="utf-8")
                   for name in ("source_a.md", "source_b.md")}
        return merge.available_candidates(segment.segment_sources(sources))

    # The resolver reads the sources, and reads them the way the reconciler
    # does. `ordering_only` is the pair that shares one title; every other
    # fixture carries two distinct ones.
    one_title, two_titles = resolver("ordering_only"), resolver("dedup")
    check(one_title("title") == 1,
          f"ordering_only's two sources share one title, got {one_title('title')}")
    check(two_titles("title") == 2,
          f"dedup's two sources carry two distinct titles, got {two_titles('title')}")

    # A heading in both documents offered two candidates; the same question
    # asked in the model's own phrasing must reach the same heading.
    for slot in ("Limits", "  limits ", "section: Limits", "Heading: LIMITS"):
        check(one_title(slot) == 2,
              f"ordering_only carries the Limits heading in both sources; "
              f"{slot!r} resolved to {one_title(slot)}")

    # And a slot that names no heading is undeterminable, which is not one.
    # A number invented here would be a judgement wearing a measurement's
    # clothes, so the resolver refuses and the unconditional rule stands.
    for slot in ("which of two wordings", "the order of the sections", ""):
        check(one_title(slot) is None,
              f"{slot!r} names no heading in either source, so it is not "
              f"determinable; got {one_title(slot)}")

    # The rule itself, all four answers.
    check(errors(decision(1)) != [],
          "with no resolver the unconditional rule stands, so every other caller "
          "of check_merge is unaffected")
    check(errors(decision(1), one_title) == [],
          f"one candidate is the whole choice when one was offered: "
          f"{errors(decision(1), one_title)}")
    check(errors(decision(1), two_titles) != [],
          "arm 1's case: two titles were available and the decision named one, "
          "so the check must still fire")
    check(errors(decision(1), lambda slot: None) != [],
          "an undeterminable slot keeps the unconditional rule")
    check(errors(decision(2), two_titles) == [],
          f"a decision naming both candidates passes: {errors(decision(2), two_titles)}")

    # Zero is never acceptable, whatever the documents offered. A decision that
    # names nothing chose nothing.
    for available in (None, one_title, two_titles):
        check(errors(decision(0), available) != [],
              "a decision naming no candidate at all must be reported")

    # The wiring, end to end, asserted by the call count: a rejected payload is
    # fed back and re-asked, so a unit the rule recovers makes one call where it
    # used to make two.
    def one_candidate_endpoint(sources):
        calls: list[int] = []

        def responder(_body, n):
            calls.append(n)
            return 200, envelope(merged("# Shared Title\n\nThe relay listens on port 8443.\n",
                                        [decision(1)], []))
        return responder, calls

    shared = {"source_a.md": "# Shared Title\n\nThe relay listens on port 8443.\n",
              "source_b.md": "# Shared Title\n\nThe read timeout is 45 seconds.\n"}
    distinct = {"source_a.md": "# Operator Guide\n\nThe relay listens on port 8443.\n",
                "source_b.md": "# Deployment Notes\n\nThe read timeout is 45 seconds.\n"}

    for sources, expected, why in (
        (shared, 1, "one title was offered, so the first answer stands"),
        (distinct, SCHEMA_ATTEMPTS,
         "two titles were offered, so the payload is fed back and re-asked "
         "until every attempt is spent"),
    ):
        responder, calls = one_candidate_endpoint(sources)
        with endpoint(responder) as client:
            with contextlib.suppress(SchemaFailure):
                merge.merge_documents(client, sources)
        check(len(calls) == expected,
              f"{why}: expected {expected} call(s), got {len(calls)}")


def test_the_window_is_found_when_the_endpoint_spells_the_tag_in_another_case() -> None:
    """A tag is case-insensitive to the server.

    `/api/ps` reports the spelling the server holds, and the run asks for the
    spelling the operator configured. Comparing the two exactly made a model
    that generates happily report as not loaded, and `served_window` does not
    catch `WindowUnknown` -- so the whole run stopped on a difference the
    endpoint itself does not observe.

    The requested spelling stays the one on the record and the one in the
    cassette key: this is the window lookup learning to find the model, not the
    tool renaming it.
    """
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))),
                        loaded=("Test-Model",))
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        found = window.reported(settings, "test-model")
        check(found.tokens == live.served,
              f"the window must be found through a case difference, got {found.tokens}")
        check(found.model == "test-model",
              f"the record keeps the requested spelling, got {found.model!r}")
        check("Test-Model" in found.detail,
              f"the detail must name the spelling the endpoint holds, got {found.detail!r}")

        # The merge itself, because the guard is what the figure is for and
        # `served_window` lets `WindowUnknown` through.
        merge.merge_documents(Client(settings), TWO)

        # An exact match is still preferred, and a model that is genuinely not
        # there is still refused.
        exc = raises(window.WindowUnknown,
                     lambda: window.reported(settings, "no-such-model"),
                     "a model nobody loaded has no window")
        check(exc is not None and "Test-Model" in str(exc),
              f"the refusal must name what was loaded instead, got {exc!r}")

    # Two entries differing only in case make the case-insensitive answer a
    # guess, so it refuses rather than picking one.
    ambiguous = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))),
                             loaded=("Test-Model", "TEST-MODEL"))
    with tempfile.TemporaryDirectory() as raw, ambiguous as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        exc = raises(window.WindowUnknown,
                     lambda: window.reported(settings, "test-model"),
                     "two spellings differing only in case must not be guessed between")
        check(exc is not None and "only in case" in str(exc),
              f"the refusal must say why it will not choose, got {exc!r}")


def test_example_scan_fires_on_the_worked_example() -> None:
    """The raw-text half of the prompt-example guard, run before decompose."""
    check(merge.example_content_leaks("The relay listens on port 8443.") == [],
          "a clean document must leak nothing")
    check(merge.example_content_leaks("The MARLBROOK funicular climbs 412 metres.")
          == ["marlbrook", "funicular"],
          "the scan must be case-insensitive and name every marker it found")

    # The failure the claim-level assertion can miss: a copy segmented so that
    # no single claim carries a forbidden word next to a forbidden word.
    split = "The lower station has a ticket office.\nMarlbrook.\n"
    check(merge.example_content_leaks(split) == ["marlbrook"],
          "a segmented copy of the example must still be caught in the raw text")


def test_the_reason_scan_reads_the_example_rather_than_a_list() -> None:
    """Derived from `merge.md`, so it cannot fall behind the example it guards.

    The floor-free reading is the point. A scan over every sentence of the
    example would fire on "The documents disagree and this merge does not
    choose between them", which the base rules *prescribe*, and quieting that
    would need a length threshold fitted to nothing. Reason clauses carry no
    prescribed wording, so the scan needs no threshold and has none.
    """
    clauses = merge.example_reason_clauses()
    check(len(clauses) >= 3,
          f"the derivation returned {len(clauses)} clause(s); a reworded example "
          f"this stops parsing would leave the scan silently guarding nothing")
    check(all(clause == clause.lower().strip() for clause in clauses),
          f"clauses must arrive flattened, got {clauses}")
    # The prescribed sentence must not be among them, or correct output fires.
    check(not any("documents disagree" in clause for clause in clauses),
          f"the disagreement sentence is prescribed output, not a leak: {clauses}")


def test_the_reason_scan_fires_on_the_captured_leak_and_not_on_real_reasons() -> None:
    """Both directions, on real text rather than invented text.

    Must-fire is the reason `qwen3:8b` actually emitted on 2026-09-14, which
    is the example's own sentence with "because " removed. Must-not-fire is
    every reason in the nine answer keys, which are human-authored.
    """
    leaked = [{"segment": "b1",
               "reason": "The base title was kept and this one was not."}]
    fired = merge.example_reason_leaks(leaked)
    check(len(fired) == 1 and fired[0][0] == "b1",
          f"the captured leak must fire, got {fired}")

    own_words = [{"segment": "b3", "reason": "Same length, shorter wording."},
                 {"segment": "b6", "reason": "a2 states the invitation already."}]
    check(merge.example_reason_leaks(own_words) == [],
          "a reason in the model's own words must not fire, even when it is "
          "about the same thing the example is about")

    for name in sorted(p.name for p in (ROOT / "tests" / "pairs").iterdir()
                       if (p / "ideal.json").is_file()):
        records = json.loads(
            (ROOT / "tests" / "pairs" / name / "ideal.json").read_text(encoding="utf-8")
        ).get("dispositions", ())
        hits = merge.example_reason_leaks(records)
        check(not hits,
              f"{name}'s answer key reasons are human-authored and must not "
              f"read as the example: {hits}")


def test_a_decision_without_chosen_is_accepted_where_the_level_forbids_choosing() -> None:
    """The whole payload through `check_merge`, at every level.

    Two of the three places that decide what a level requires became
    level-aware, leaving the third, the field-*order* check, demanding all
    four `DECISION_FIELDS`. A schema that told the model `chosen` was optional
    and a checker that rejected the record for omitting it is a contradiction
    the model cannot satisfy, and it refused every merge at `off`, `low` and
    `mid`, which is nearly every merge.

    Built from a recorded payload rather than an invented one, with `chosen`
    removed the way a model told it was optional would omit it. Read at the
    field order its recording used: the 27B's keys arrive sorted, and a
    record short of a field is still a fault under `any`, which is the fault
    this probe is about.
    """
    recorded = json.loads(
        (ROOT / "tests" / "responses" / "m7" / "merge-018ce6c33ae44d9d.json")
        .read_text(encoding="utf-8"))
    payload = json.loads(
        json.loads(recorded["response"]["raw"])["choices"][0]["message"]["content"])
    order = recorded["meta"]["field_order"]
    check(payload["decisions"], "the recorded payload must carry a decision to be a probe")
    without = dict(payload)
    without["decisions"] = [
        {k: v for k, v in d.items() if k != "chosen"} for d in payload["decisions"]
    ]

    for level in config.FIDELITY_LEVELS:
        may = merge.MAY_CHOOSE[level]
        errors = parsing.forgiven(parsing.check_merge(without, None, may), order)
        if may:
            check(errors, f"{level} may choose, so a decision with no chosen must "
                          f"be refused; got {errors}")
        else:
            check(not errors,
                  f"{level} may not choose, so a decision with no chosen is the "
                  f"only way to record a conflict there; got {errors}")
    # And the record as recorded, with `chosen`, is still good where choosing is
    # the licence rather than the defect.
    check(not parsing.forgiven(parsing.check_merge(payload, None, True), order),
          "a complete decision must still pass at high")


def test_prompt_example_is_absent_from_every_fixture_document() -> None:
    """The markers must name the prompt and nothing in the suite, or they measure nothing."""
    for name in run_merge.fixture_names():
        for document, text in run_merge.load_sources(name).items():
            leaked = merge.example_content_leaks(text)
            check(not leaked,
                  f"{name}/{document} contains {leaked}: the example markers must be "
                  f"words no fixture uses")


# --------------------------------------------------------------------------
# the harness
# --------------------------------------------------------------------------


def test_transfer_rule_keeps_three_and_drops_the_restored_log_format() -> None:
    """A merged.md `absent` assertion transfers iff it matches neither source.

    Derived rather than a maintained exclusion list. `dropped_claim` is the case
    that makes the rule necessary: its merge omits the log format on purpose, so
    the assertion forbids a claim of it — and a correct generated merge is
    *required* to carry that fact.
    """
    kept = {
        name: [a["assertion_id"] for a in run_merge.transferable(
            run_merge.load_expected(name), run_merge.load_sources(name))]
        for name in run_merge.fixture_names()
    }
    check(kept["disjoint_sources"] == ["no-princess-to-forest", "no-forest-to-rosegarden"],
          f"both cross-story assertions must transfer, got {kept['disjoint_sources']}")
    check(kept["disjoint_domains"] == ["no-depot-to-chess", "no-chess-to-depot"],
          f"the second control's assertions must transfer too, got {kept['disjoint_domains']}")
    check(kept["ordering_only"] == ["no-misrendered-max-connections-merged"],
          f"the misrendered-count assertion must transfer, got {kept['ordering_only']}")
    check(kept["dropped_claim"] == [],
          "no-restored-log-format must NOT transfer: its pattern matches source_b.md")
    check(kept["structure_added"] == [],
          "basis: not_a_claim assertions are about one document's prose and never transfer")
    check(kept["list_structure"] == ["no-fused-port-and-connect-timeout-merged",
                                     "no-fused-connect-and-read-timeout-merged",
                                     "no-fused-connections-and-retries-merged",
                                     "no-fused-log-format-and-health-path-merged"],
          f"the fusion assertions must transfer: no source states two of these values on one "
          f"line, so a generated merge that does has fused them, got {kept['list_structure']}")
    check(sum(len(v) for v in kept.values()) == 9,
          f"exactly nine assertions transfer across the suite, got {kept}")

    # The rule, not the answer: a pattern present in a source is dropped
    # whatever it is called, and one present in neither is kept.
    expected = {
        "must_not_extract": [
            {"assertion_id": "in-a", "document": "merged.md", "basis": "absent",
             "pattern": "port 8443"},
            {"assertion_id": "in-neither", "document": "merged.md", "basis": "absent",
             "pattern": "SOCKS5"},
            {"assertion_id": "wrong-document", "document": "source_a.md", "basis": "absent",
             "pattern": "SOCKS5"},
        ]
    }
    check([a["assertion_id"] for a in run_merge.transferable(expected, TWO)] == ["in-neither"],
          "the rule must key on the pattern and the document, not on the assertion id")


def test_global_assertions_apply_unconditionally() -> None:
    """GLOBAL.json is not transferable-or-not; it is every document of every fixture."""
    ids = [a["assertion_id"] for a in run_merge.global_assertions()]
    check("no-prompt-example-marlbrook" in ids,
          "the merge prompt's worked example needs a global claim-level guard too")
    kiln = Claim("M-001", "merged.md", "The kiln fired for eleven hours.", 1, "", True)
    clean = Claim("M-002", "merged.md", "The relay listens on port 8443.", 1, "", True)
    check(run_merge.violations([kiln], run_merge.global_assertions()) == ["no-prompt-example-kiln"],
          "a claim carrying a prompt illustration must trip its global assertion")
    check(run_merge.violations([clean], run_merge.global_assertions()) == [],
          "a claim about the document must trip nothing")


def test_the_uniform_forward_rule() -> None:
    """SUPPORTED and nothing else. The declared expectations are not consulted.

    `contradiction/a-connect-timeout` is the worked case. It declares
    `expected_verdict: CONTRADICTED` and `expected_evidence_contains: ["60"]`,
    both true of the hand-written merge and both wrong for a generated one that
    surfaces A's 30 seconds and B's 60 alongside each other.
    """
    probe = next(
        p for p in run_merge.forward_probes(run_merge.load_expected("contradiction"))
        if p["probe_id"] == "a-connect-timeout"
    )
    check(probe["expected_verdict"] == "CONTRADICTED",
          "the fixture is still the one this rule was written against")

    def result(label: str, evidence: str) -> run_merge.ForwardResult:
        return run_merge.ForwardResult(
            probe_id=probe["probe_id"],
            document=probe["document"],
            verdict=Verdict(
                claim_id=probe["probe_id"], verdict=label, evidence=evidence,
                evidence_source="merged.md", rationale="", direction=SOURCE_TO_MERGED,
                grounding=GROUNDED if label != "MISSING" else NOT_GRADED,
            ),
        )

    check(result("SUPPORTED", "30 seconds").ok,
          "a merge that surfaced A's value passes, though the fixture declares CONTRADICTED")
    check(not result("CONTRADICTED", "60").ok,
          "the fixture's own declared verdict must not be accepted on a generated merge")
    check(not result("MISSING", "").ok, "a dropped fact fails")
    check(not run_merge.ForwardResult(probe["probe_id"], "source_a.md", None).ok,
          "an errored probe is not a pass")
    check(run_merge.ForwardResult(probe["probe_id"], "source_a.md", None).observed == "ERROR",
          "an errored probe must be reported as an error, not as a verdict")


def test_no_forward_probe_declares_an_evidence_source() -> None:
    """The one exclusion this grading does not have to make. Asserted so it stays true."""
    probes = [
        p for name in run_merge.fixture_names()
        for p in run_merge.forward_probes(run_merge.load_expected(name))
    ]
    check(len(probes) == 121, f"the forward denominator is 121 probes, got {len(probes)}")
    check(not [p for p in probes if p.get("expected_evidence_source")],
          "a forward probe declaring an evidence source would need excluding by name")
    declared = [p for p in probes if p.get("expected_evidence_contains")]
    check(len(declared) == 58,
          f"the docstring says 58 forward probes declare an evidence span, got {len(declared)}")


def test_the_merge_step_is_shown_two_sources_and_nothing_else() -> None:
    """The merge's *input*, checked separately from the forward pass's.

    Worth its own test because the two are different claims. Downstream the
    concern is grounding -- `verify.locate` searches only the mapping it is
    handed. Here the concern is contamination: a merge shown the hand-written
    merge would reproduce it, and every measurement after that would be of a
    document the model was given rather than one it wrote.

    Two independent guards. `load_sources` reads exactly `merge.source_names(2)`
    off disk, and `merge.check_sources` refuses a mapping with anything else in
    it, so a leak has to get past a hard error as well as a convention.
    """
    sources = run_merge.load_sources("disjoint_sources")
    check(sorted(sources) == ["source_a.md", "source_b.md"],
          f"the merge is shown two sources, got {sorted(sources)}")

    hand_written = (run_merge.FIXTURES_DIR / "disjoint_sources" / "merged.md").read_text()
    check(all(hand_written not in text for text in sources.values()),
          "no source may carry the hand-written merge, or the guard proves nothing")

    seen: list[dict] = []

    class Recorder(ScriptedClient):
        def complete(self, **kwargs):
            if kwargs.get("role") == "merge":
                seen.append(kwargs)
            return super().complete(**kwargs)

    run_merge.run_unit("disjoint_sources", "off", 0, Recorder(), PROMPTS, 25)
    check(len(seen) == 1, f"one merge call per unit, saw {len(seen)}")
    rendered = seen[0]["messages"][-1]["content"]
    check(hand_written.strip() not in rendered,
          "the hand-written merge must never reach the merge prompt")

    try:
        merge.check_sources({**sources, "merged.md": hand_written})
        check(False, "a mapping carrying merged.md must be refused, not merged")
    except merge.MergeError as exc:
        check("merged.md" in str(exc), f"the error must name the offending file, got {exc}")


def test_every_role_records_the_thinking_it_actually_ran_with() -> None:
    """The record has to name the configuration the arm ran, not the default.

    The journal line this pins used to read `THINKS[unit.condition] if step ==
    "merge" else False`, so decompose and verify were written down as thinking
    off on every run there has ever been -- including any run launched with
    `--thinking decompose`, where the calls did think, because the flag reaches
    the call through `settings.thinks(role)` and never through the step name.
    The calls were right and the record was wrong, which is the worse of the two
    failures: a sweep graded on that record attributes one arm's numbers to a
    configuration no arm used.

    Driven through the real flag rather than a hand-built frozenset, so what is
    checked is the string an operator types. The merge role is the exception on
    purpose and it is asserted as one: this harness runs the merge both ways in
    one process, so its condition is the override, and `--thinking merge` cannot
    turn on a merge the `off` condition is there to measure.
    """
    def ran(condition: str, *flags: str) -> dict:
        parser = argparse.ArgumentParser()
        config.add_arguments(parser, offline_dir=run_merge.CASSETTES)
        client = ScriptedClient()
        client.settings = config.apply_arguments(
            client.settings, parser.parse_args(list(flags))
        )
        return run_merge.run_unit("dedup", condition, 0, client, PROMPTS, 25).thinking

    # Repeated, not comma-separated: `--thinking` takes one role a time and
    # replaces the default set (`config.py:544-550`).
    every = ran("on", "--thinking", "merge", "--thinking", "verify",
                "--thinking", "decompose")
    check(every == {"merge": True, "decompose": True, "verify": True},
          f"every role asked to think must be recorded thinking, got {every}")

    default = ran("on")
    check(default == {"merge": True, "decompose": False, "verify": False},
          f"the default configuration is merge alone, got {default}")

    # The failure mode in the other direction: a record that simply echoes the
    # flags would also produce the two dicts above. This one was never asked
    # for and must not appear.
    off = ran("off", "--thinking", "merge", "--thinking", "verify",
              "--thinking", "decompose")
    check(off["merge"] is False,
          f"the off condition is a merge that did not think, recorded {off['merge']}")
    check(off["decompose"] is True and off["verify"] is True,
          f"and it must not switch the other two roles off with it, got {off}")


def test_a_unit_records_its_wall_time_and_its_schema_repairs() -> None:
    """Two figures a per-arm comparison needs and the record did not carry.

    Wall time is the unit's own, not the merge call's: `merge_seconds` already
    covers the merge, and an arm that merges quickly and then repairs its way
    through four verify batches is not a fast arm. Repairs are counted as a
    difference across the unit for the same reason every other spend figure is
    (`Spend`): the counter is per-client and the sweep runs many units through
    one.
    """
    class Repairing(ScriptedClient):
        def complete(self, **kwargs):
            self.usage.repairs += 1
            return super().complete(**kwargs)

    client = Repairing()
    unit = run_merge.run_unit("dedup", "off", 0, client, PROMPTS, 25)
    check(unit.repairs == len(client.roles) and unit.repairs > 0,
          f"one repair per call: {len(client.roles)} calls, recorded {unit.repairs}")
    check(unit.seconds > 0, f"a unit that ran took time, recorded {unit.seconds}")
    check(unit.seconds >= unit.merge_seconds,
          f"unit wall time {unit.seconds} cannot be under the merge alone "
          f"{unit.merge_seconds}")

    clean = run_merge.run_unit("dedup", "off", 0, ScriptedClient(), PROMPTS, 25)
    check(clean.repairs == 0,
          f"a client that repaired nothing must show none, got {clean.repairs}")


def test_a_forward_unit_never_opens_the_hand_written_merge() -> None:
    """Structural, not a scope statement, so it gets a test.

    `verify.locate` searches only the mapping it is handed. That mapping is built
    by `unit_documents`, which reads two files by name and takes the merge as an
    argument, so there is no path by which a fixture's own `merged.md` reaches a
    grounding check.

    The read-watch below covers the whole unit, merge step included, so it is
    also the backstop for `test_the_merge_step_is_shown_two_sources_and_nothing_else`.
    """
    documents = run_merge.unit_documents("contradiction", "GENERATED")
    check(set(documents) == {"source_a.md", "source_b.md", "merged.md"},
          f"a unit works over three documents, got {sorted(documents)}")
    check(documents["merged.md"] == "GENERATED",
          "merged.md must be the generated text, under the name the prompt shows")

    opened: list[str] = []
    original = Path.read_text

    def watched(self, *args, **kwargs):
        opened.append(str(self))
        return original(self, *args, **kwargs)

    client = ScriptedClient()
    Path.read_text = watched
    try:
        run_merge.run_unit("contradiction", "off", 0, client, PROMPTS, 25)
    finally:
        Path.read_text = original

    hand_written = [p for p in opened if p.endswith("contradiction/merged.md")]
    check(not hand_written,
          f"a forward unit must never open the fixture's own merge, opened {hand_written}")
    check(any(p.endswith("contradiction/source_a.md") for p in opened),
          "the sources are what a unit reads; the test is worthless if it read nothing")


def test_an_errored_step_reduces_the_denominator_and_the_run_is_inconclusive() -> None:
    """74/76, never 74/121 — and the JSON keeps both numbers so 121 is recoverable."""
    good = unit("contradiction", "off", 0, supported=8, measured=8)
    partial = unit("contradiction", "on", 0, supported=6, measured=6, declared=8,
                   failed_step="verify_forward")
    check(len(partial.measured) == 6 and len(partial.forward) == 8,
          "an errored batch leaves its probes declared but unmeasured")
    check(partial.rate == 1.0,
          "the rate is over what was measured; the errored probes are not counted wrong")
    check(not partial.clean, "an errored unit is never clean, whatever its measured probes said")

    dead = unit("contradiction", "on", 1, supported=0, measured=0, declared=8,
                failed_step="merge")
    check(dead.rate is None, "a unit whose merge failed measured nothing at all")
    check(dead.measured == [], "a failed merge takes every forward probe with it")

    run = fixture_run("contradiction", [good, unit("contradiction", "off", 1, 8, 8)],
                      [partial, dead])
    check(run.status == "ERROR", f"any errored unit makes the fixture ERROR, got {run.status}")

    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "out.json"
        run_merge.write_json(path, [run], 2, FakeProvenance())
        data = json.loads(path.read_text())
    check(data["inconclusive"] is True, "a run with an errored unit is inconclusive")
    check(data["forward"]["probes_declared"] == 32,
          f"the JSON keeps the declared count, got {data['forward']['probes_declared']}")
    check(data["forward"]["probes_measured"] == 22,
          f"the JSON keeps the measured count, got {data['forward']['probes_measured']}")
    steps = {u["failed_step"] for u in data["fixtures"][0]["units"]}
    check(steps == {None, "verify_forward", "merge"},
          f"the failing step must be named per unit, got {steps}")


def test_a_bad_call_errors_the_unit_rather_than_the_run() -> None:
    """Before the fix only SchemaFailure was contained.

    An earlier sweep died three times on this: `step` caught SchemaFailure and let
    everything else propagate out of `run_unit`, past the loop, into main's
    blanket handler, which exited 2 with no `sweep.json` and every finished unit
    discarded. Two of the three were transport faults and one was a
    TierUnsupported, and none of them is a statement about any unit but its own.

    The three checks are the three halves of the contract: contained, named, and
    the probes gone from the denominator rather than counted wrong.
    """
    class Broken(ScriptedClient):
        def __init__(self, step_to_break: str, exception: Exception) -> None:
            super().__init__()
            self.step_to_break = step_to_break
            self.exception = exception

        def complete(self, *, role, messages, **kwargs):
            if role == self.step_to_break:
                raise self.exception
            return super().complete(role=role, messages=messages, **kwargs)

    # A transport fault, by shape rather than by class: run_merge must not
    # import `transport`, so the exception it contains cannot be named there.
    unit = run_merge.run_unit(
        "contradiction", "off", 0,
        Broken("merge", RuntimeError("localhost took the request and did not finish")),
        PROMPTS, 25,
    )
    check(unit.failed_step == "merge",
          f"a transport fault must error the unit at its step, got {unit.failed_step!r}")
    check("RuntimeError" in (unit.error or ""),
          f"the error must name the type, got {unit.error!r}")
    check(unit.measured == [] and unit.rate is None,
          "a failed merge leaves nothing measured; it must not be scored as 0/8")

    # The other failure the sweep actually hit, one step further in.
    later = run_merge.run_unit(
        "contradiction", "off", 0,
        Broken("verify", structured.TierUnsupported("response message has empty content")),
        PROMPTS, 25,
    )
    check(later.failed_step == "verify_forward",
          f"a tier refusal must error the unit too, got {later.failed_step!r}")
    check(len(later.forward) == 8 and later.measured == [],
          "the probes stay declared and leave the denominator")

    # And the short list that still ends the run. A replay miss is not one bad
    # call: the corpus does not hold what this code asks for, every later unit
    # would miss for the same reason, and continuing would report a subset of
    # the suite as if it were the suite.
    fatal = MissingCassette("k" * 64, "merge", Path("tests/responses/m4"))
    raises(MissingCassette,
           lambda: run_merge.run_unit(
               "contradiction", "off", 0, Broken("merge", fatal), PROMPTS, 25),
           "a replay miss must still end the run, not error one unit")


def test_a_merge_near_its_token_ceiling_trips_the_guard() -> None:
    """It is a guard rather than the fix.

    The defect is that `completion_tokens` is not the generation: this endpoint
    bills the reasoning trace to `prompt_tokens` and returns the text in a
    field of its own, so the figure the harness compares against `max_tokens`
    understated thinking-on merges by 1.9x to 15.0x across earlier runs. Real token
    accounting stays on the backlog. The tripwire is set low enough that the
    understatement cannot hide an overrun -- at half the ceiling on the metric
    that exists, a 1.9x call is already over it -- and it is loud, so a
    possibly budget-limited merge can never be read as a quality result.
    """
    class Bills(ScriptedClient):
        def __init__(self, tokens: int) -> None:
            super().__init__()
            self.tokens = tokens

        def complete(self, *, role, messages, **kwargs):
            if role == "merge":
                self.usage.completion_tokens += self.tokens
            return super().complete(role=role, messages=messages, **kwargs)

    # Pinned, not read and trusted: a tripwire tested against whatever the
    # function happens to return would still pass if the function returned
    # nonsense. 2560 under the earlier one-field schema, 8960 once the budget
    # was sized for the four other fields that can hold copied text, 8448 at
    # `off` once headroom stopped being charged on the three a level that cannot
    # compose a replacement can only fill with selected text, 6912/7424 once
    # `REASON_MAX` was cut to 80: a reason is charged twice per segment, so
    # the cut lands 1792 tokens on a 22-segment pair, and 11008/11520 once
    # `REASONING_ALLOWANCE` was raised from 2048 to 6144 on the first live
    # measurement of a trace. That last move is a flat
    # +4096 at every level, which is what a flat allowance is supposed to look
    # like: if these two figures ever differ by other than the 512 the level
    # buys, the allowance has grown a branch.
    #
    # Raising `REPLACEMENT_MAX` 240 -> 640 moved neither figure. The
    # replacement term is `min(document copies, segments * REPLACEMENT_MAX)` and
    # on every fixture the first is the smaller, so the cap does not bind here;
    # that was already known and this is the check that keeps confirming it.
    #
    # 11264/11776 since `MISMATCH_ALLOWANCE` was added: one flat `BUDGET_STEP`
    # for the `mismatch` field, granted after the rounding. The move is +256 on
    # *every* fixture and on both levels, which is the shape a flat allowance
    # is supposed to have: the 512 between the two figures is still what the
    # level buys, unchanged, and that gap is what the check below pins.
    # Rounding it in instead moved one fixture a step and its neighbour none,
    # which broke the registered tie between the two disjoint controls.
    ceiling = merge.budget_tokens(run_merge.load_sources("contradiction"), LEVEL)
    check(ceiling == 11264, f"the contradiction ceiling at {LEVEL} is 11264, got {ceiling}")
    high = merge.budget_tokens(run_merge.load_sources("contradiction"), "high")
    check(high == 11776, f"and 11776 at high, got {high}")
    check((high - ceiling) % merge.BUDGET_STEP == 0,
          f"the levels must differ by a whole number of budget steps: {high - ceiling}")

    quiet = run_merge.run_unit("contradiction", "off", 0,
                               Bills(int(ceiling * run_merge.BUDGET_TRIPWIRE) - 1),
                               PROMPTS, 25)
    check(not quiet.budget_tripped,
          f"a merge below the tripwire must not fire it, spent {quiet.completion_tokens} "
          f"of {ceiling}")

    loud = run_merge.run_unit("contradiction", "off", 0,
                              Bills(int(ceiling * run_merge.BUDGET_TRIPWIRE)),
                              PROMPTS, 25)
    check(loud.budget_tripped,
          f"a merge at {run_merge.BUDGET_TRIPWIRE:.0%} of {ceiling} must fire the guard, "
          f"spent {loud.completion_tokens}")
    check(not loud.errored and loud.rate is not None,
          "the guard flags the unit; it does not throw its measurements away")

    # Loud means loud: the report says so and the JSON names which unit it was.
    clean = unit("contradiction", "on", 0, supported=8, measured=8, merged="other")
    run = fixture_run("contradiction", [loud], [clean])
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        run_merge.summarise([run], 1, run_merge.CONDITIONS, False)
    text = printed.getvalue()
    check("BUDGET GUARD" in text and "may be budget-limited" in text,
          f"the guard must reach the report, got {text[-400:]!r}")
    check(str(loud.completion_tokens) in text,
          "the report must name the spend, not only that something tripped")

    with tempfile.TemporaryDirectory() as raw:
        out = Path(raw) / "sweep.json"
        run_merge.write_json(out, [run], 1, FakeProvenance())
        data = json.loads(out.read_text())
    check(data["budget_tripped"] == ["contradiction[off]#0"],
          f"the JSON must name which units tripped, got {data.get('budget_tripped')}")

    # And a sweep holding one is inconclusive, whatever its probes said: every
    # unit here is 8/8 SUPPORTED and it still must not exit 0.
    def one_tripped(fixture, condition, sample, *_args, **_kwargs):
        tripped = unit(fixture, condition, sample, supported=8, measured=8,
                       merged=f"{fixture}-{condition}-{sample}")
        tripped.budget_tripped = fixture == "contradiction"
        return tripped

    original = run_merge.run_unit
    run_merge.run_unit = one_tripped
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            code = run_merge.main(["--offline", "--no-colour", "--samples", "1"])
    finally:
        run_merge.run_unit = original
    check(code == 2,
          f"a sweep whose probes all passed but whose budget tripped exits 2, got {code}")


def test_the_sweep_gives_up_after_three_consecutive_failures() -> None:
    """The other side: contained is not the same as never abort.

    A dead endpoint with 15 s pacing and a 300 s timeout costs about five
    minutes per unit to learn nothing, and the full plan is 96 units. So the
    sweep proves the endpoint is gone -- CONSECUTIVE_ERROR_LIMIT units in a row,
    roughly fifteen minutes -- and then stops, reporting what it measured.

    `run_unit` is replaced rather than an endpoint broken, because what is being
    checked is the loop's arithmetic and not any call's failure mode.
    """
    attempted: list[tuple] = []

    def always_fails(fixture, condition, sample, *_args, **_kwargs):
        attempted.append((fixture, condition, sample))
        return run_merge.Unit(fixture=fixture, condition=condition, sample=sample,
                              failed_step="merge", error="RuntimeError: endpoint gone")

    original = run_merge.run_unit
    run_merge.run_unit = always_fails
    printed = io.StringIO()
    try:
        with tempfile.TemporaryDirectory() as raw, contextlib.redirect_stdout(printed):
            out = Path(raw) / "sweep.json"
            code = run_merge.main([
                "--offline", "--no-colour", "--samples", "3", "--out", str(out),
            ])
            written = out.exists()  # inside the context: the directory goes away below
            data = json.loads(out.read_text())
    finally:
        run_merge.run_unit = original

    check(len(attempted) == run_merge.CONSECUTIVE_ERROR_LIMIT,
          f"the sweep must stop after {run_merge.CONSECUTIVE_ERROR_LIMIT} consecutive "
          f"failures, attempted {len(attempted)} of a 96-unit plan")
    check(code == 2, f"an abandoned run exits 2, got {code}")
    check(written, "the results file must still be written; that is the whole point")
    check("ABANDONED" in printed.getvalue(),
          "the operator must be told the sweep stopped early, not left to infer it")
    check(data["abandoned_units"] == 96 - run_merge.CONSECUTIVE_ERROR_LIMIT,
          f"the JSON must say how many units were never attempted, got "
          f"{data.get('abandoned_units')}")
    check(data["inconclusive"] is True, "an abandoned run is inconclusive")

    # And the exclusion must be in the report, not only in the line that
    # scrolled past when it happened and the field in the JSON. Everything
    # `summarise` prints is over a subset of the suite, so it has to say so
    # before it says anything else.
    report = printed.getvalue()
    report = report[report.index("Merge over the fixture set"):]
    check("ABANDONED" in report,
          "the abandonment must reach the report block, not only the sweep log")
    check(str(96 - run_merge.CONSECUTIVE_ERROR_LIMIT) in report,
          "the report must name how many units are missing from every figure in it")
    # The section heading, not the dim sentence above it that also spells
    # "Forward coverage" -- matching that one would pass whatever the order was.
    check(report.index("ABANDONED") < report.index("\n  Forward coverage\n"),
          "the warning must come before the coverage it qualifies, not after")

    clean = io.StringIO()
    with contextlib.redirect_stdout(clean):
        run_merge.summarise(
            [fixture_run("contradiction",
                         [unit("contradiction", "off", 0, supported=8, measured=8)],
                         [unit("contradiction", "on", 0, supported=8, measured=8,
                               merged="other")])],
            1, run_merge.CONDITIONS, False)
    check("ABANDONED" not in clean.getvalue(),
          "a run that attempted every unit must not carry the warning")


def test_a_timeout_says_which_of_the_two_it_was() -> None:
    """"Answered nothing" and "answered too slowly" are not one event.

    The live half proves the classification is reached on the path that actually
    occurs -- an endpoint that takes the request and then thinks about it, which
    is what a throttled local GPU is. The connect-timeout half is asserted
    against `timed_out` directly rather than provoked, because provoking one
    means opening a socket to something that is not the configured endpoint.
    """
    sent = str(transport.timed_out("localhost", 300, sent=True))
    nothing = str(transport.timed_out("localhost", 300, sent=False))
    check("too slow" in sent and "--timeout" in sent,
          f"a slow answer must send the operator to the budget, got {sent!r}")
    check("answered nothing" in nothing and "listening" in nothing,
          f"an unsent request must send the operator to the server, got {nothing!r}")
    check(sent != nothing, "the two messages must differ, which was the whole defect")

    def sleeps(_body, _n):
        time.sleep(0.6)
        return 200, merged("never arrives")

    with tempfile.TemporaryDirectory() as raw, FakeEndpoint(sleeps) as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False, timeout=0.2,
        )
        exc = raises(Exception, lambda: merge.merge_documents(Client(settings), TWO),
                     "an endpoint that never finishes must raise")
    check(exc is not None and "too slow" in str(exc),
          f"a slow endpoint must report the slow-answer message, got {exc!r}")


def test_the_comparison_is_paired() -> None:
    """Comparing 76 measured probes against 121 would blame the thinking flag for an error."""
    off = unit("f", "off", 0, supported=8, measured=8)
    on = unit("f", "on", 0, supported=5, measured=6, declared=8, failed_step="verify_forward")
    supported, total = run_merge.paired([fixture_run("f", [off], [on])])
    check(total == 6, f"the paired denominator is the intersection, got {total}")
    check(supported["off"] == 6, f"off is re-counted over the shared probes, got {supported}")
    check(supported["on"] == 5, f"on keeps its own result, got {supported}")


def test_identical_merges_report_identical_and_a_thoughtless_flag_is_a_harness_fault() -> None:
    """`identical` is a status, not a 0.0 delta, and first a suspicion about the harness.

    The discriminator is the reasoning block, corroborated by latency. It is
    deliberately *not* `completion_tokens`: the 2026-08-08 smoke pass measured
    714 tokens off against 726 on for a merge whose reasoning ran to 2901
    characters, because ollama returns qwen3's reasoning in a field of its own
    and bills only `content`. A ratio test on those numbers calls a working
    flag a fault and blocks a four-hour sweep over nothing.
    """
    def pair(off_text, on_text, *, reasoned=False, off_s=0.0, on_s=0.0, cached=False):
        off = unit("f", "off", 0, 8, 8, merged=off_text, merge_seconds=off_s)
        on = unit("f", "on", 0, 8, 8, merged=on_text, reasoned=reasoned,
                  merge_seconds=on_s, cached=cached)
        return fixture_run("f", [off], [on])

    differing = pair("A", "B")
    check(differing.identical == [], "two different merges are not identical")
    check(differing.suspect == [], "two different merges cannot be a flag that did nothing")

    genuine = pair("same", "same", reasoned=True)
    check(genuine.identical == [0], "byte-identical merges must be reported as identical")
    check(genuine.suspect == [],
          "identical text is a real null result when the model demonstrably thought")

    # The regression the token ratio would have produced: same tokens, real
    # reasoning. Nothing here even looks at completion_tokens any more.
    flat_tokens = fixture_run(
        "f",
        [unit("f", "off", 0, 8, 8, merged="same", tokens=714)],
        [unit("f", "on", 0, 8, 8, merged="same", tokens=726, reasoned=True)],
    )
    check(flat_tokens.suspect == [],
          "a reasoning block settles it; comparable token counts must not override it")

    slow = pair("same", "same", off_s=31.7, on_s=61.8)
    check(slow.suspect == [],
          "latency alone is enough evidence the flag reached the endpoint")

    fault = pair("same", "same", off_s=31.7, on_s=32.0)
    check(fault.suspect == [0],
          "no reasoning block and no extra time is a harness fault, not a finding")

    replayed = pair("same", "same")
    check(replayed.suspect == [0],
          "with no latency to read, the reasoning block decides, and there was none")

    cached = pair("same", "same", cached=True, off_s=31.7, on_s=0.0)
    check(cached.suspect == [0],
          "a cached merge has no latency; it must not be read as having been fast")
    check(not run_merge._slower(cached.cells["on"].units[0], cached.cells["off"].units[0]),
          "a cached unit yields no latency evidence either way")


def test_unresolved_is_neither_passed_nor_failed() -> None:
    clean = [unit("f", "off", i, 8, 8) for i in range(2)]
    check(fixture_run("f", clean, [unit("f", "on", i, 8, 8) for i in range(2)]).status == "ok",
          "a fixture clean in every sample is ok")

    disagreed = [unit("f", "off", 0, 8, 8), unit("f", "off", 1, 7, 8)]
    run = fixture_run("f", disagreed, [unit("f", "on", i, 8, 8) for i in range(2)])
    check(run.status == "unresolved",
          f"samples that disagree on pass/fail settle nothing, got {run.status}")

    failed = [unit("f", "off", i, 7, 8) for i in range(2)]
    check(fixture_run("f", failed, [unit("f", "on", i, 7, 8) for i in range(2)]).status == "FAIL",
          "a fixture that fails in every sample fails")

    leaked = unit("f", "off", 0, 8, 8)
    leaked.leaks = ["marlbrook"]
    check(not leaked.clean, "a unit that leaked the prompt example is not clean")
    violated = unit("f", "off", 0, 8, 8)
    violated.violated = ["no-princess-to-forest"]
    check(not violated.clean, "a unit that tripped must_not_extract is not clean")


def test_the_dry_run_table_is_the_planned_sweep() -> None:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        planned = run_merge.dry_run_table(
            run_merge.fixture_names(), 3, run_merge.CONDITIONS, 25, LEVEL, False
        )
    text = out.getvalue()
    check(planned == 432, f"the worst case is 432 calls, got {planned}")
    # The fixture count again, and again unrelated to the benchmark denominator that
    # `run_arm.py` and `test_pairs.py` pin at 14 for a different reason (7 pairs
    # x 2 levels). The two read alike until `concatenated` landed and no longer coincide.
    check("16 fixtures (+1 GLOBAL)" in text,
          "the count must say sixteen fixtures plus GLOBAL, so 17/17 cannot read as a "
          "discrepancy")
    check("121 forward probes" in text, "the forward denominator belongs in the plan")
    check("72 calls per sample per condition" in text, "the per-pass figure belongs in the plan")
    for name in run_merge.fixture_names():
        check(name in text, f"{name} must have its own row: a total hides disjoint_sources")
    # The largest budget in the suite, and the row a reader checks against the
    # server's context before committing a block. Computed rather than pinned
    # because the point is that the table prints what `merge` will actually ask
    # for, and the two moved apart once already.
    budgets = {name: merge.budget_tokens(run_merge.load_sources(name), LEVEL)
               for name in run_merge.fixture_names()}
    largest = max(budgets.values())
    check(sorted(name for name, size in budgets.items() if size == largest)
          == ["disjoint_domains", "disjoint_sources"],
          f"the two disjoint controls are held to one size class and must tie for the "
          f"largest budget in the suite, {budgets} says otherwise")
    check(str(largest) in text,
          f"the largest budget is the row a reader checks against the server's context "
          f"before committing a block; the table must print {largest}")


def test_merges_are_written_where_a_human_can_read_them() -> None:
    """78 files, one per unit. Cassette recovery is not a review path."""
    units = {
        ("contradiction", "off"): "OFF MERGE",
        ("contradiction", "on"): "ON MERGE",
    }

    def fake_unit(fixture, condition, sample, *_args, **_kwargs):
        return unit(fixture, condition, sample, 8, 8, merged=units[(fixture, condition)])

    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        (root / "replay").mkdir()
        printed = io.StringIO()
        original, run_merge.run_unit = run_merge.run_unit, fake_unit
        try:
            with contextlib.redirect_stdout(printed):
                code = run_merge.main([
                    "--fixture", "contradiction",
                    "--samples", "1",
                    "--replay", str(root / "replay"),
                    "--merges", str(root / "merges"),
                    "--out", str(root / "out.json"),
                    "--no-colour",
                ])
        finally:
            run_merge.run_unit = original

        check("graded against SUPPORTED alone" in printed.getvalue(),
              "the report must state the uniform rule where the number is read, not only "
              "in a docstring")

        written = sorted(p.name for p in (root / "merges").iterdir())
        check(written == ["contradiction-off-0.md", "contradiction-on-0.md"],
              f"one .md per unit, named for it, got {written}")
        check((root / "merges" / "contradiction-off-0.md").read_text() == "OFF MERGE",
              "the file must hold what the model wrote, unmodified")
        check(code == 0, f"a clean run exits 0, got {code}")
        check(json.loads((root / "out.json").read_text())["samples"] == 1,
              "the JSON must record how many samples produced it")


def test_the_journal_records_what_it_takes_to_re_run_a_call() -> None:
    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "journal.jsonl"
        client = ScriptedClient()
        with path.open("w", encoding="utf-8") as journal:
            run_merge.run_unit("contradiction", "on", 2, client, PROMPTS, 25, journal)

        records = [json.loads(line) for line in path.read_text().splitlines()]

    check([r["step"] for r in records] == list(run_merge.STEPS),
          f"every step of a complete unit is journalled, in order, got {[r['step'] for r in records]}")
    first = records[0]
    for key in ("fixture", "condition", "sample", "model", "temperature", "seed",
                "max_tokens", "thinking", "cassette_key", "tier", "seconds"):
        check(key in first, f"the journal must record {key}")
    ceiling = merge.budget_tokens(run_merge.load_sources("contradiction"), LEVEL)
    check(first["thinking"] is True and first["max_tokens"] == ceiling,
          f"the merge record carries this unit's condition and budget ({ceiling}), got {first}")
    check(records[1]["thinking"] is False,
          "only the merge call takes the condition; verify and decompose never think")
    check(all(r["outcome"] == "ok" for r in records), "a clean unit journals no errors")

    # Resumption reads the last step alone: a unit that stopped partway re-runs.
    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "journal.jsonl"
        path.write_text("\n".join(json.dumps(r) for r in records) + "\n")
        check(run_merge.finished(path) == {("contradiction", "on", 2)},
              "a completed unit is skipped on restart")
        path.write_text("\n".join(json.dumps(r) for r in records[:2]) + "\n")
        check(run_merge.finished(path) == set(),
              "a unit that stopped partway must be re-run, not skipped")


# --------------------------------------------------------------------------
# stubs
# --------------------------------------------------------------------------

PROMPTS = {
    "merge": prompts.load("merge"),
    "decompose": prompts.load("decompose"),
    "source_to_merged": prompts.load("verify"),
    "merged_to_sources": prompts.load("verify_reverse"),
}


MERGE = "The relay listens on port 8443.\n"


class ScriptedClient(Client):
    """A Client that answers every role from a script. Never opens a socket.

    The verify roles answer whatever they were asked about: both verify prompts
    end with `CLAIMS:` and one `id: text` line per claim, so the stub reads the
    ids back out of the rendered prompt rather than being told them. That keeps
    it honest about batching -- a stub with a fixed answer would pass a
    `verify_claims` that quietly dropped half a batch.
    """

    # Never opens a socket, so there is no served window to preflight
    # against and nothing for the guard to protect.
    sends_nothing = True

    def __init__(self) -> None:
        # Fidelity pinned rather than defaulted. The stub's level is read back
        # by `run_merge.run_unit` to size the budget tripwire, and by the
        # fragment assertions below to say which text the merger was given, so
        # leaving it to `DEFAULT_FIDELITY` made both of those move when
        # the default changed. `off` is the level those tests are about.
        super().__init__(config.Settings(
            models={"merge": "stub", "decompose": "stub", "verify": "stub"},
            use_cache=False,
            fidelity="off",
        ))
        self.roles: list[str] = []

    def served_window(self, _role):
        """No window, because there is no server.

        `complete` is overridden here, so nothing this client does reaches a
        socket -- and the base method would try to ask localhost what it is
        serving, which is both a fabrication and a socket-guard breach. The
        guard against a budget that will not fit is tested against
        `FakeEndpoint`, which answers the question for real.
        """
        return None

    def complete(self, *, role, messages, thinking=None, **_) -> Completion:
        self.roles.append(role)
        # Through the real rule, not a copy of it: a stub that decided this for
        # itself would keep passing after `Client` stopped honouring the flag.
        self.last_thinking = self.thinking_for(role, thinking)
        if role == "merge":
            return Completion({"merged_document": MERGE})
        if role == "decompose":
            return Completion({"claims": [
                {"text": MERGE.strip(), "line": 1, "span": MERGE.strip()},
            ]})
        block = messages[-1]["content"].rsplit("\nCLAIMS:\n", 1)[-1]
        ids = [line.split(":", 1)[0] for line in block.splitlines() if ":" in line]
        return Completion({"verdicts": [
            {"claim_id": claim_id, "verdict": "SUPPORTED", "rationale": "stub",
             "evidence": MERGE.strip(), "evidence_source": "merged.md"}
            for claim_id in ids
        ]})


class FakeProvenance:
    def as_dict(self) -> dict:
        return {"run_mode": "test"}


def unit(fixture, condition, sample, supported, measured, declared=None, merged="M",
         tokens=0, failed_step=None, reasoned=False, cached=False,
         merge_seconds=0.0) -> run_merge.Unit:
    """A Unit with `measured` graded probes, `supported` of them SUPPORTED."""
    declared = measured if declared is None else declared
    forward = []
    for i in range(declared):
        graded = i < measured
        label = "SUPPORTED" if graded and i < supported else "MISSING"
        forward.append(run_merge.ForwardResult(
            probe_id=f"p{i}",
            document="source_a.md",
            verdict=Verdict(
                claim_id=f"p{i}", verdict=label, evidence="e", evidence_source="merged.md",
                rationale="", direction=SOURCE_TO_MERGED,
                grounding=GROUNDED if label == "SUPPORTED" else NOT_GRADED,
            ) if graded else None,
        ))
    return run_merge.Unit(
        fixture=fixture, condition=condition, sample=sample, merged=merged,
        forward=forward, completion_tokens=tokens, failed_step=failed_step,
        merge_reasoned=reasoned, merge_cached=cached, merge_seconds=merge_seconds,
    )


def fixture_run(name, off, on) -> run_merge.FixtureRun:
    return run_merge.FixtureRun(
        fixture=name,
        cells={
            "off": run_merge.Cell(name, "off", list(off)),
            "on": run_merge.Cell(name, "on", list(on)),
        },
    )


def test_the_exclude_recorded_rule_covers_both_disk_paths() -> None:
    """`cached` alone is the wrong predicate, and was for a year.

    The cache and the cassette are separate branches of `_fetch` and only the
    cache one sets `last_cached`, so a filter written as `not record["cached"]`
    reads a replay as a live call. Nothing caught it while the rule was written
    out three times, because each copy was checked against the recording run it
    was written for, where there are no replays at all.
    """
    live = {"step": "merge", "condition": "off", "cached": False, "replayed": 0}
    from_cache = {"step": "merge", "condition": "off", "cached": True, "replayed": 0}
    from_cassette = {"step": "merge", "condition": "off", "cached": False, "replayed": 1}
    entries = [live, from_cache, from_cassette]

    check(journal.steps(entries) == [live],
          f"a replayed step is not a live call; journal.steps kept {journal.steps(entries)}")
    check(len(journal.steps(entries, include_recorded=True)) == 3,
          "include_recorded=True must return every step, replays included")
    check([journal.recorded(r) for r in entries] == [False, True, True],
          "journal.recorded must be the union of the cache and the cassette")

    # A journal written before the field existed answers what it recorded, not
    # a guess: an earlier corpus has 288 records and none of them carry `replayed`.
    old = {"step": "merge", "condition": "off", "cached": False}
    check(not journal.recorded(old), "a record with no replayed field is not recorded")

    check(not journal.measurable(run_merge.Unit(fixture="f", condition="off", sample=0,
                                                merge_replayed=True)),
          "a merge served from a cassette has no latency and is not measurable")


def test_a_journal_record_carries_every_input_that_shaped_the_call() -> None:
    """What the journal must say, asserted rather than read.

    `timeout` is deliberately out of the cassette key: the same request
    answered slowly and answered quickly is the same request, but excluding it
    from the key is not a reason to exclude it from the record: one timeout
    message was split into two precisely because a slow endpoint and an absent one
    are different diagnoses, and neither can be told from `seconds` by a reader
    who does not know what the deadline was. `replayed` is here for the reason
    above it.
    """
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "j.jsonl"
        with endpoint(lambda body, n: (200, envelope(merged("m")))) as client:
            merge.merge_documents(client, TWO)
            with path.open("w", encoding="utf-8") as handle:
                run_merge.journal_step(
                    handle,
                    run_merge.Unit(fixture="dedup", condition="off", sample=0),
                    "merge",
                    client,
                    time.monotonic() - 1.0,
                    run_merge.Spend(0, 0),
                    "ok",
                )
        record, = journal.records(path)

    for field in ("model", "tier", "seed", "temperature", "max_tokens", "thinking",
                  "timeout", "replayed", "cached", "seconds", "completion_tokens",
                  "cassette_key", "outcome"):
        check(field in record, f"a journal record must carry {field!r}; it has {sorted(record)}")
    check(record["timeout"] == client.settings.call_timeout,
          f"the journalled timeout must be the deadline the call ran under, got {record.get('timeout')}")
    check(record["timeout"] is not None,
          "and a run that stated none journals the resolved default rather "
          "than a null, or the record says the call was unbounded")
    check(record["replayed"] == 0, "a live call replayed nothing")
    check(not journal.recorded(record), "a live call is not a recorded one")


def test_an_all_replay_journal_reports_its_denominator_rather_than_nothing() -> None:
    """Silence and "no faults" must not look alike."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "j.jsonl"
        path.write_text("".join(
            json.dumps({"step": "merge", "condition": "off", "outcome": "ok",
                        "seconds": 4.0, "gap_seconds": None,
                        "cached": False, "replayed": 1}) + "\n"
            for _ in range(7)
        ), encoding="utf-8")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            run_merge.latency_summary(path)
        printed = buffer.getvalue()
    check("no live calls in 7 journalled step(s)" in printed,
          f"an all-replay journal must print its denominator; it printed {printed!r}")
    check("mean" not in printed,
          f"an all-replay journal must report no mean latency; it printed {printed!r}")


def test_a_budget_over_the_served_window_is_refused_before_anything_is_sent() -> None:
    """The refusal is worth nothing if it arrives after the request.

    Two assertions and the second is the one that matters. That it raises is
    easy; that the endpoint received no POST is the whole feature, because the
    failure being prevented -- a prompt the server silently trims from the front
    -- has already happened by the time a response comes back, and nothing in
    the response says so.
    """
    with tempfile.TemporaryDirectory() as raw, FakeEndpoint(
        lambda _b, _n: (200, envelope(merged("never asked for"))), served=64
    ) as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        client = Client(settings)
        exc = raises(window.BudgetExceedsWindow,
                     lambda: merge.merge_documents(client, TWO),
                     "a budget over the served window must be refused")
    check(exc is not None and "Nothing has been sent" in str(exc),
          f"the refusal must say nothing was sent, got {exc!r}")
    check(exc is not None and "64" in str(exc),
          f"the refusal must name the window it measured against, got {exc!r}")
    # The remedy an operator can actually apply. "Serve a larger window" is
    # advice with no verb in it: the setting is on the server, it is read once
    # at startup, and both of those have to be said or the reader raises it in
    # their shell and gets the same refusal.
    check(exc is not None and "OLLAMA_CONTEXT_LENGTH" in str(exc),
          f"the refusal must name the setting that fixes it, got {exc!r}")
    check(exc is not None and "restarting the server" in str(exc),
          f"and say that raising it takes a restart, got {exc!r}")


def test_a_model_on_the_cpu_is_said_out_loud_before_the_first_long_call() -> None:
    """The incident that started this: a pod whose container came up without its GPU.

    ollama does not fail in that case, it loads on the CPU and answers -- twenty
    to fifty times slower. What reaches the operator is a proxy timeout with a
    Cloudflare body about a slow origin, which points at the network and not at
    the container. `/api/ps` has carried the answer the whole time, in `size`
    and `size_vram`, and it is read before the first long call rather than after
    it.
    """
    told = io.StringIO()
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))),
                        vram_fraction=0.0)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        merge.merge_documents(Client(settings, console=Console(told)), TWO)
    said = told.getvalue()
    check("CPU" in said, f"a CPU load must be said out loud: {said!r}")
    check("test-model" in said, f"and must name the model: {said!r}")
    check("slower" in said, f"and what it costs: {said!r}")
    check(live.calls == 1, "and must not stop the run: a CPU load still answers")


def test_a_partly_offloaded_model_is_named_as_a_fraction_and_a_whole_one_is_silent() -> None:
    """The three cases are one boundary and two sides of it, so all three are asserted.

    A warning that fired on a healthy endpoint would be trained away within a
    day, which is the failure mode of every warning that cries wolf -- so the
    silent case is asserted as hard as the loud ones.
    """
    for fraction, wanted in ((0.62, "62% GPU"), (1.0, None), (None, None)):
        told = io.StringIO()
        live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))),
                            vram_fraction=fraction)
        with tempfile.TemporaryDirectory() as raw, live as base_url:
            settings = config.Settings(
                base_url=base_url, models={"merge": "test-model"},
                cache_dir=Path(raw) / "cache", use_cache=False,
            )
            merge.merge_documents(Client(settings, console=Console(told)), TWO)
        said = told.getvalue()
        if wanted is None:
            check(said == "", f"vram_fraction={fraction} must say nothing: {said!r}")
        else:
            check(wanted in said,
                  f"vram_fraction={fraction} must be reported as {wanted}: {said!r}")


def test_the_placement_is_read_from_the_two_figures_and_never_guessed() -> None:
    """`placement` decides on evidence or returns "", and "" is not "CPU"."""
    cases = (
        ({"size": 100, "size_vram": 0}, "CPU"),
        ({"size": 100, "size_vram": 100}, "GPU"),
        ({"size": 100, "size_vram": 150}, "GPU"),   # a runner over-reporting
        ({"size": 100, "size_vram": 25}, "25% GPU"),
        ({"size": 100}, ""),                        # ollama before the field
        ({}, ""),                                   # not ollama at all
        ({"size": 0, "size_vram": 0}, ""),          # nothing resident
        ({"size": "100", "size_vram": 0}, ""),      # a string is not a size
    )
    for entry, wanted in cases:
        got = window.placement(entry)
        check(got == wanted, f"placement({entry}) must be {wanted!r}, got {got!r}")


def test_the_refusal_reaches_the_endpoint_for_the_window_and_for_nothing_else() -> None:
    """No POST at all, and exactly one GET: the guard asked and then stopped."""
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("never asked for"))), served=64)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        raises(window.BudgetExceedsWindow,
               lambda: merge.merge_documents(Client(settings), TWO),
               "a budget over the served window must be refused")
    check(live.calls == 0, f"a refused merge must send no completion, sent {live.calls}")
    check(live.gets == ["/api/ps"], f"the guard asks /api/ps and nothing else, got {live.gets}")


def test_the_served_window_is_asked_once_per_client_and_not_once_per_merge() -> None:
    """It is a property of a running server, not of a request.

    A sweep is hundreds of merges; asking every time would put an extra
    round trip in front of each one to learn something that cannot change
    without the server restarting.
    """
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))))
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        client = Client(settings)
        merge.merge_documents(client, TWO)
        merge.merge_documents(client, TWO)
    check(live.gets == ["/api/ps"],
          f"two merges on one client ask the window once, got {live.gets}")
    check(live.calls == 2, f"both merges must still have run, got {live.calls}")


def test_a_trimmed_prompt_is_caught_from_the_endpoints_own_count() -> None:
    """This is the must-fire probe. Geometry taken from the real trim
    measured on this project's card: a ~13,000-token prompt
    against a 4,096-token total came back with `prompt_eval_count` 2050.

    The row is what a trimmed call leaves on the ledger, and the check reads
    only those two numbers, nothing about the answer's shape, which is the
    line this check draws.
    """
    trimmed = {"estimated_prompt_tokens": 13000, "prompt_tokens": 2050}
    exc = raises(window.Truncated,
                 lambda: window.assert_prompt_not_trimmed(trimmed, what="merge"),
                 "a prompt counted at 2050 of 13000 sent must be refused")
    check(exc is not None and "2050" in str(exc) and "13000" in str(exc),
          f"the refusal must carry both figures, got {exc!r}")

    # The least obvious trim this mechanism produces, with the geometry right:
    # a prompt that just fills a 4,096-token window is estimated at about
    # 4096 / 0.727 = 5634 by an estimator that over-counts, and a half-window
    # trim reports 2048 of it -- a ratio of 0.364, which is the ceiling the
    # threshold was derived against rather than the 0.5 boundary itself.
    least_obvious = {"estimated_prompt_tokens": 5634, "prompt_tokens": 2048}
    raises(window.Truncated,
           lambda: window.assert_prompt_not_trimmed(least_obvious, what="merge"),
           "a half-window trim at its real ratio must fire")

    # And the boundary is inclusive, so the threshold is not a knife-edge.
    raises(window.Truncated,
           lambda: window.assert_prompt_not_trimmed(
               {"estimated_prompt_tokens": 4096, "prompt_tokens": 2048}, what="merge"),
           "exactly TRIM_RATIO must fire; it is unreachable by an honest call")


def test_an_honest_call_and_an_endpoint_that_counts_nothing_both_stay_quiet() -> None:
    """The two must-not-fire cases, and the second is the one that matters.

    The floor over 2,200 recorded calls is 0.653 -- the estimate over-counts,
    so every honest call reports fewer tokens than were estimated, and a
    threshold that fired on that would refuse the whole corpus. And every
    vendor body reports `prompt_tokens: 0` with its billing in `credits_used`,
    which read as a count is a total shortfall.
    """
    # An ordinary call at the worst legitimate ratio ever recorded.
    ordinary = {"estimated_prompt_tokens": 1000, "prompt_tokens": 653}
    check(window.assert_prompt_not_trimmed(ordinary, what="merge") is None,
          "the worst honest ratio on record must not fire")

    # A vendor body: the key is present and the value is zero.
    vendor = {"estimated_prompt_tokens": 4000, "prompt_tokens": 0}
    check(window.assert_prompt_not_trimmed(vendor, what="merge") is None,
          "prompt_tokens: 0 means the endpoint does not report it, not a shortfall")

    # Absent takes the same path as zero, and a row with neither figure is
    # not a verdict either.
    for row in ({"estimated_prompt_tokens": 4000}, {"prompt_tokens": 900}, {}):
        check(window.assert_prompt_not_trimmed(row, what="merge") is None,
              f"a row missing a figure must stay silent, fired on {row}")


def test_the_trim_threshold_sits_between_its_two_derivations() -> None:
    """The threshold is a measured quantity, so it is pinned as one.

    Between the worst honest call on record and the most a half-window trim
    can report. A change to `TRIM_RATIO` that leaves this range is a change
    that either refuses real calls or misses real trims.
    """
    legitimate_floor = 0.653   # min over 2,200 recorded calls
    trim_ceiling = 0.364       # 0.727 median estimate ratio, halved by the trim
    check(trim_ceiling < window.TRIM_RATIO < legitimate_floor,
          f"TRIM_RATIO {window.TRIM_RATIO} must sit inside "
          f"({trim_ceiling}, {legitimate_floor})")


def test_the_measured_window_is_optimistic_by_the_probe_fill_margin() -> None:
    """`/api/ps` reports the runner's total; the prompt
    shares it with the completion, so the largest prompt a server accepts
    without trimming can sit below the reported figure.

    `measured()` confirms the report by probe, and the probe fills
    `PROBE_FILL` of the candidate -- so what it returns is confirmed only to
    97% of itself. Three regimes, and the third is the finding:

      * a budget far below the total, with no room to halve above `floor`,
        raises `WindowUnknown` and refuses the run outright;
      * a budget that halving lands under is returned conservatively;
      * a budget between `PROBE_FILL` of a halved candidate and that
        candidate is returned **above** the true budget, and a prompt in that
        band passes the guard and is silently trimmed.

    Pinned rather than fixed: the margin is a property of `PROBE_FILL`, and
    narrowing it costs a larger probe on every model of every run.
    """
    # Refuses: 4096 total, 2050 budget, `floor` leaves no candidate below it.
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))),
                        served=4096, prompt_budget=2050)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        exc = raises(window.WindowUnknown,
                     lambda: window.measured(settings, "test-model", at_most=4096),
                     "a budget with no halving room must refuse rather than guess")
        check(exc is not None and "2050" in str(exc),
              f"the refusal must carry the count the endpoint reported, got {exc!r}")

    # Conservative: halving lands under the budget.
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))),
                        served=40960, prompt_budget=30000)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        got = window.measured(settings, "test-model", at_most=40960).tokens
        check(got <= 30000, f"expected a figure at or under the budget, got {got}")

    # Optimistic: the returned figure is above the true budget by up to the
    # probe-fill margin, and a prompt in that band is trimmed with the guard green.
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))),
                        served=40960, prompt_budget=20000)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        got = window.measured(settings, "test-model", at_most=40960).tokens
        check(got == 20480, f"expected the halved candidate 20480, got {got}")
        check(got > 20000,
              "the finding: the guard's figure sits above the true budget")
        # The band is bounded by PROBE_FILL and is not unlimited.
        check(20000 >= got * window.PROBE_FILL,
              f"the band must be within the probe-fill margin: "
              f"{got} * {window.PROBE_FILL} = {got * window.PROBE_FILL}")


def test_banner_window_reports_the_served_context() -> None:
    """The banner's job: a formatted figure, from the one
    call `served_window` already makes, before anything else runs."""
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))), served=40960)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        got = window.banner_window(settings, "test-model")
        check(got == "40,960", f"expected a formatted served window, got {got!r}")
        check(live.gets == ["/api/ps"], f"expected exactly one /api/ps GET, got {live.gets}")


def test_banner_window_is_none_when_not_loaded_and_forces_no_load() -> None:
    """The must-not-fire half of the same item: a cold model must not be
    warmed just to print a banner line, which would make a status check as
    expensive as the run it precedes."""
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))), loaded=())
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        got = window.banner_window(settings, "test-model")
        check(got is None, f"expected None for a model not yet loaded, got {got!r}")
        check(not live.probes, f"banner_window must not warm the model, got {live.probes}")
        check(live.calls == 0, "banner_window must send no completion request either")


def test_banner_window_is_none_on_a_404_and_is_not_an_error() -> None:
    """A vendor endpoint with no `/api/ps` route is a normal case, not a
    refusal -- the same distinction `WindowUnmeasurable` exists for."""
    unmeasurable = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))),
                                ps_status=404)
    with tempfile.TemporaryDirectory() as raw, unmeasurable as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        got = window.banner_window(settings, "test-model")
        check(got is None, f"expected None on a 404, got {got!r}")


def test_banner_window_opens_no_socket_offline() -> None:
    """Replay and dry-run send nothing anywhere; this must not be the one
    place in an offline run that opens a socket to find out."""
    settings = config.Settings(
        base_url="http://127.0.0.1:1/v1", models={"merge": "test-model"},
        replay_dir=Path("tests/responses"), use_cache=False,
    )
    got = window.banner_window(settings, "test-model")
    check(got is None, f"an offline run must get None without trying, got {got!r}")

    settings = config.Settings(
        base_url="http://127.0.0.1:1/v1", models={"merge": "test-model"},
        dry_run=True, use_cache=False,
    )
    got = window.banner_window(settings, "test-model")
    check(got is None, f"a dry run must get None without trying, got {got!r}")


def test_a_404_on_api_ps_is_unmeasurable_not_unknown() -> None:
    """A vendor's 404 proceeds; a bad answer still refuses.

    `WindowUnmeasurable` and `WindowUnknown` are different facts and must stay
    on different sides of the refusal. Only a 404 on the route itself gets the
    new treatment -- any other failure to read `/api/ps` is unchanged.
    """
    unmeasurable = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))),
                                ps_status=404)
    with tempfile.TemporaryDirectory() as raw, unmeasurable as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        exc = raises(window.WindowUnmeasurable,
                     lambda: window.reported(settings, "test-model"),
                     "a 404 on /api/ps must raise WindowUnmeasurable")
        check(exc is not None and "does not expose it" in str(exc),
              f"the message must say the route is absent, got {exc!r}")

        client = Client(settings)
        served = client.served_window("merge")
        check(served is None, f"an unmeasurable window must return None, got {served!r}")
        mechanism = client.usage.window_mechanism.get("merge", "")
        check(mechanism.startswith("post-hoc"),
              f"the mechanism must be recorded as post-hoc, got {mechanism!r}")

        # And the merge itself proceeds -- no config, no declared window.
        merge.merge_documents(client, TWO)
        check(unmeasurable.calls == 1, "the merge call must still reach the endpoint")

    # A 500, or any status but 404, is unrelated: still fatal, still
    # WindowUnknown territory is untouched.
    broken = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))), ps_status=500)
    with tempfile.TemporaryDirectory() as raw, broken as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        raises(transport.HTTPStatusError,
              lambda: window.reported(settings, "test-model"),
              "a non-404 failure to read /api/ps must still raise, unrewritten")


# The window figure these tests state. Large enough that nothing here is
# refused for fitting badly, and a round number no local server serves, so a
# figure appearing in a report is unambiguously the one that was declared.
STATED_WINDOW = 200_000


def vendor_shaped(responder=None):
    """An endpoint with no `/api/ps` route, which is what a vendor is here.

    The 404 is the whole of what makes it a vendor for this purpose: it is
    the route `served_window` asks for, and the one route nobody
    but ollama answers.
    """
    return FakeEndpoint(responder or (lambda _b, _n: (200, envelope(merged("fits")))),
                        ps_status=404)


def stated_window_claims(report, rows, notes, check_) -> None:
    """What a report must say about a window the operator declared.

    A function rather than a block inside one test, so the seeded probe below
    runs *these* assertions against a defective build rather than a second copy
    of them that could drift into agreeing with the defect.
    """
    row = dict(rows).get("Context window")
    check_(row is not None,
           f"a stated window must reach the Provenance rows; got {sorted(dict(rows))}")
    check_(row is not None and str(STATED_WINDOW) in row,
           f"the row must carry the figure that was declared: {row!r}")
    check_(row is not None and "no probe" in row,
           f"the row must say no probe confirmed it: {row!r}")
    stated_notes = [note for note in notes if "stated, not measured" in note]
    check_(len(stated_notes) == 1,
           f"exactly one note must say the window was stated rather than "
           f"measured; got {len(stated_notes)} of {len(notes)}")
    check_(all("Preflight window guard ran" not in note for note in notes),
           "a stated window must not be reported as a preflight against a "
           "measured figure -- that is the one sentence this mechanism exists "
           "to keep out of the report")
    check_("stated" in report and "Context window" in report,
           "the rendered markdown must carry the row, not only the dict")


def test_a_stated_window_guards_every_role_on_an_endpoint_with_no_api_ps() -> None:
    """The blocker: two of three roles refuse on any hosted vendor.

    `window.preflight` raises `WindowUnmeasurable` when handed `None`, and
    `None` is what `served_window` returns for an endpoint with no `/api/ps`,
    an ollama route. The consequence was recorded rather than worked
    around: "a vendor endpoint that does not expose `/api/ps` cannot now run
    `verify`, or `merge`'s decompose and verify stages."

    A stated window is the third thing that can be true about such an endpoint,
    and it is not a default: it is `None` unless a person typed a figure. Three
    things are asserted together because any one alone would pass on a broken
    build -- that the guard is satisfied, that it is still a guard, and that
    not a single request was spent establishing it.
    """
    live = vendor_shaped()
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url,
            models={"merge": "test-model", "decompose": "test-model",
                    "verify": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
            window=STATED_WINDOW,
        )
        client = Client(settings)
        for role in ("merge", "decompose", "verify"):
            served = client.served_window(role)
            check(served is not None,
                  f"{role} must be given the stated window, got None")
            check(served is not None and served.tokens == STATED_WINDOW,
                  f"{role} must be given the figure that was stated, got {served!r}")
            check(served is not None and served.source == "stated",
                  f"{role}'s window must be provenanced as stated, got "
                  f"{served and served.source!r}")
            mechanism = client.usage.window_mechanism.get(role, "")
            check(mechanism.startswith("stated: "),
                  f"{role}'s mechanism must record a stated window, got {mechanism!r}")

        # No probe, and no `/api/ps`. `window.measured` sends a calibration
        # generation plus a probe at 97% of the figure, per model per run; on a
        # metered vendor with a 200k window that is an expensive preflight for
        # a number nobody disputed, and it is charged before the run's first
        # real call.
        check(live.gets == [],
              f"a stated window must ask the endpoint nothing, got {live.gets}")
        check(live.probes == [],
              f"a stated window must send no confirmation probe, got "
              f"{len(live.probes)} probe(s)")
        check(live.calls == 0,
              f"and no completion either, got {live.calls}")

        # Still a guard. A window that satisfied `preflight` and then let
        # anything through would be the defect one level up -- the run looks
        # guarded and is not.
        served = client.served_window("decompose")
        check(window.preflight(served, needed=10, what="a small prompt",
                               role="decompose") is None,
              "a prompt that fits a stated window must be allowed through")
        exc = raises(window.BudgetExceedsWindow,
                     lambda: window.preflight(served, needed=STATED_WINDOW + 1,
                                              what="an enormous prompt",
                                              role="decompose"),
                     "a prompt over the stated window must still be refused")
        check(exc is not None and "stated" in str(exc),
              f"the refusal must say which kind of figure it refused on: {exc!r}")

        # And the merge runs, which is what none of this could do before.
        merge.merge_documents(client, TWO)
        check(live.calls == 1, f"the merge call must reach the endpoint, got {live.calls}")
        check(live.gets == [], f"and still no /api/ps, got {live.gets}")


def test_an_unstated_window_is_exactly_what_it_was_before() -> None:
    """The must-not-fire half. Unset changes nothing, on either kind of endpoint.

    Both directions are here because the interesting failure is a stated window
    leaking into runs that did not ask for one: an endpoint that answers
    `/api/ps` must still be measured and still record `preflight`, and one that
    does not must still refuse `decompose` and `verify` outright.
    """
    live = vendor_shaped()
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model", "verify": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        check(settings.window is None,
              f"a window is unset unless somebody sets one, got {settings.window!r}")
        client = Client(settings)
        check(client.served_window("verify") is None,
              "an unmeasurable window with nothing stated must still be None")
        check(client.usage.window_mechanism.get("verify", "").startswith("post-hoc"),
              f"and must still record post-hoc, got "
              f"{client.usage.window_mechanism.get('verify')!r}")
        exc = raises(window.WindowUnmeasurable,
                     lambda: window.preflight(None, needed=10, what="a prompt",
                                              role="verify"),
                     "an unmeasurable window must still refuse the call")
        check(exc is not None and "--window" in str(exc),
              f"and the refusal must name the remedy that now exists: {exc!r}")

    measurable = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))))
    with tempfile.TemporaryDirectory() as raw, measurable as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        client = Client(settings)
        served = client.served_window("merge")
        check(served is not None and served.source == "measured",
              f"an endpoint that can be measured must still be measured, got "
              f"{served and served.source!r}")
        check(client.usage.window_mechanism.get("merge") == "preflight",
              f"and must record the same one-word mechanism every recorded run "
              f"carries, got {client.usage.window_mechanism.get('merge')!r}")
        check(measurable.probes,
              "the confirmation probe must still be sent where it can be")


def test_a_stated_window_is_reported_as_stated_and_never_as_measured() -> None:
    """A run guarded against a number the operator typed is a different claim.

    The report is where that distinction either survives or is lost, so it is
    asserted on the rendered block and not on the dict alone.
    """
    live = vendor_shaped()
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
            window=STATED_WINDOW,
        )
        client = Client(settings)
        merge.merge_documents(client, TWO)
        provenance = Provenance(settings=settings, client=client,
                                roles=("merge",), duration_seconds=0.0)
        stated_window_claims(provenance.as_markdown(), provenance.rows(),
                             provenance.notes(), check)

    # The other side of the same rule: a measured run gains no row at all, so
    # every report in the recorded corpus is unchanged by this mechanism.
    measurable = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))))
    with tempfile.TemporaryDirectory() as raw, measurable as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        client = Client(settings)
        merge.merge_documents(client, TWO)
        provenance = Provenance(settings=settings, client=client,
                                roles=("merge",), duration_seconds=0.0)
        check("Context window" not in dict(provenance.rows()),
              "a measured run must gain no Context window row, or every report "
              "this project has published changes shape for a mechanism that "
              "did not exist when they were measured")
        check(any("Preflight window guard ran" in note
                  for note in provenance.notes()),
              "and must still say its preflight ran")


def test_the_report_catches_a_stated_window_that_claims_to_be_measured() -> None:
    """The must-fire probe for the test above. A check nobody has seen fail.

    Seeded in the shipped code -- `window.stated` is the one function that
    builds the object, and `window.mechanism` derives the recorded string from
    that object's own `source`, so a window that lies about its provenance
    lies everywhere at once. That is the defect worth probing: not a missing
    row, but a declared figure wearing a measured figure's label, which reads
    to every downstream reader as a guarantee nobody gave.
    """
    original = window.stated

    def lies(tokens, model, *, declared_by):
        return window.Window(tokens=tokens, source="measured", model=model,
                             detail="a prompt of that size was sent and counted")

    live = vendor_shaped()
    seeded: list[str] = []
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
            window=STATED_WINDOW,
        )
        client = Client(settings)
        try:
            window.stated = lies
            merge.merge_documents(client, TWO)
        finally:
            window.stated = original
        provenance = Provenance(settings=settings, client=client,
                                roles=("merge",), duration_seconds=0.0)
        stated_window_claims(provenance.as_markdown(), provenance.rows(),
                             provenance.notes(),
                             lambda ok, message: None if ok else seeded.append(message))

    check(seeded,
          "the seeded defect was not caught: a stated window claiming to be "
          "measured passed every assertion the real test makes")
    check(any("Provenance rows" in message for message in seeded),
          f"the row's absence must be one of the failures, got {seeded}")
    check(any("stated rather than" in message for message in seeded),
          f"the note's absence must be another, got {seeded}")


def test_a_truncated_completion_is_caught_after_the_call_when_no_preflight_ran() -> None:
    """The post-hoc guard fires only where the preflight could not.

    A local endpoint's ordinary run is unaffected: the ceiling is checked before
    the call there, and this check never runs for it.
    """
    check(window.assert_untruncated(
        {"completion_tokens": 50, "max_tokens": 100}, what="test") is None,
        "a completion under its ceiling must not raise")
    check(window.assert_untruncated({}, what="test") is None,
          "a row with neither figure must not raise -- nothing to check")
    check(window.assert_untruncated({"completion_tokens": 50}, what="test") is None,
          "a row with no max_tokens must not raise -- no ceiling was asked for")
    exc = raises(window.Truncated,
                 lambda: window.assert_untruncated(
                     {"completion_tokens": 100, "max_tokens": 100}, what="merging 2 sources"),
                 "a completion at its ceiling must raise Truncated")
    check(exc is not None and "100 completion tokens" in str(exc) and "100-token ceiling" in str(exc),
          f"the message must name both figures, got {exc!r}")

    # End to end: an unmeasurable endpoint whose model answers right at the
    # ceiling it was given must fail the merge, not return a silently short one.
    def truncating_responder(_body, _n):
        body = json.loads(envelope(merged("x" * 500)))
        body["usage"] = {"prompt_tokens": 10, "completion_tokens": 5}
        return 200, json.dumps(body)

    live = FakeEndpoint(truncating_responder, ps_status=404)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        client = Client(settings)
        exc = raises(window.Truncated,
                     lambda: merge.merge_documents(client, TWO, max_tokens=5),
                     "a completion that used all of its max_tokens on an "
                     "unmeasurable endpoint must raise Truncated")
        check(exc is not None, "the merge must not silently return the truncated document")


def test_a_stated_window_keeps_the_post_hoc_truncation_check_as_well() -> None:
    """A preflight against an unconfirmed figure is not a reason to drop the
    weaker guard behind it -- it is the reason to keep it.

    If the operator declares more than the endpoint serves, the preflight
    passes a request that does not fit, and the run is back where it was with
    no guard at all. `assert_untruncated` reads two numbers the ledger row
    already carries, so keeping it costs nothing and covers exactly the case a
    stated window cannot rule out. The control is the measured endpoint below,
    where the figure *was* confirmed and the check stays off.
    """
    def truncating(_body, _n):
        body = json.loads(envelope(merged("x" * 500)))
        body["usage"] = {"prompt_tokens": 10, "completion_tokens": 5}
        return 200, json.dumps(body)

    live = vendor_shaped(truncating)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
            window=STATED_WINDOW,
        )
        client = Client(settings)
        exc = raises(window.Truncated,
                     lambda: merge.merge_documents(client, TWO, max_tokens=5),
                     "a completion at its ceiling under a stated window must "
                     "still raise Truncated -- the preflight it passed was "
                     "against a figure nothing confirmed")
        check(exc is not None,
              "the merge must not return a silently truncated document")

    # The control. A measured window keeps the check off, because there the
    # preflight was against a figure a probe confirmed and this weaker check
    # has nothing to add -- which is the behaviour every recorded run has.
    measurable = FakeEndpoint(truncating)
    with tempfile.TemporaryDirectory() as raw, measurable as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        client = Client(settings)
        merge.merge_documents(client, TWO, max_tokens=5)
        check(client.usage.window_mechanism.get("merge") == "preflight",
              f"the control must have measured its window, got "
              f"{client.usage.window_mechanism.get('merge')!r}")


def test_counts_omits_the_token_pair_when_nothing_reported_one() -> None:
    """Unknown is not zero, in the block a machine reads as well as the prose.

    `Usage.prompt_tokens` and `completion_tokens` are plain ints starting at
    zero, incremented only from a usage block that arrived. An endpoint that
    reports none therefore published `prompt_tokens: 0` in `counts` beside a
    `tokens_described` reading `unknown (N call(s) reported no usage)` -- two
    fields of one provenance block contradicting each other, and the machine-
    readable one saying the wrong thing.

    `usage.py` states the rule this restores: "a token-free arm and an
    unmeasured arm support opposite conclusions about cost". `Tokens.as_dict`
    already drops absent fields; `counts` now agrees with it.

    The attributes stay ints. `tests/run_merge.py` subtracts one reading from
    another to attribute spend to a unit of work, and a None there would be a
    new failure in place of an old lie.
    """
    def run(reports_usage: bool) -> dict:
        live = FakeEndpoint(
            lambda _b, _n: (200, envelope(merged("fits"), usage=reports_usage)))
        with tempfile.TemporaryDirectory() as raw, live as base_url:
            settings = config.Settings(
                base_url=base_url, models={"merge": "test-model"},
                cache_dir=Path(raw) / "cache", use_cache=False,
            )
            client = Client(settings)
            merge.merge_documents(client, TWO)
            return Provenance(settings=settings, client=client,
                              roles=("merge",), duration_seconds=0.0).as_dict()

    silent = run(False)
    check("prompt_tokens" not in silent["counts"],
          f"an endpoint reporting no usage must not publish a token count, got "
          f"{silent['counts'].get('prompt_tokens')!r}")
    check("completion_tokens" not in silent["counts"],
          "the same for the completion half")
    check("unknown" in silent["tokens_described"],
          f"and the prose must say so: {silent['tokens_described']!r}")
    check(silent["tokens"].get("unmeasured_calls", 0) >= 1,
          "the unmeasured call is still counted, because omitting the figure "
          "is not the same as there having been no call")

    # Must-not-fire: an endpoint that does report usage still publishes both,
    # or this check would pass by removing the fields altogether.
    counted = run(True)
    check("prompt_tokens" in counted["counts"] and "completion_tokens" in counted["counts"],
          f"a reported usage block must still publish both counts, got "
          f"{sorted(counted['counts'])}")
    check(counted["counts"]["prompt_tokens"] > 0,
          f"and the figure must be the real one, got "
          f"{counted['counts']['prompt_tokens']!r}")


def test_provenance_reports_the_wire_temperature_when_it_differs_from_the_constant() -> None:
    """Seeded: a live call's own body outranks the constant.

    `structured.build_body` is monkeypatched for exactly one call, the way
    the smoke run technique already does elsewhere in this suite -- the request
    is still built for real and sent for real, only the temperature argument it
    is built with differs from `TEMPERATURE`.
    """
    original = structured.build_body

    def off_temperature(**kwargs):
        kwargs["temperature"] = 0.5
        return original(**kwargs)

    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("fits"))))
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        client = Client(settings)
        try:
            structured.build_body = off_temperature
            merge.merge_documents(client, TWO)
        finally:
            structured.build_body = original

        provenance = Provenance(settings=settings, client=client,
                                roles=("merge",), duration_seconds=0.0)
        reported_temperature = provenance.as_dict()["decoding"]["temperature"]
        check(reported_temperature == 0.5,
              f"a wire temperature that differs from the constant must be reported "
              f"as sent, got {reported_temperature!r}")
    check(client.usage.wire_temperature == 0.5,
          f"Usage.wire_temperature must carry the wire value, got {client.usage.wire_temperature!r}")


def test_the_provenance_block_states_the_effort_level_of_every_role() -> None:
    """One value here would be true of one call of six and false of five.

    The merge is asked for `high` and the two roles that read its work back for
    `low`, so a scalar `decoding.effort` would describe a run nobody made. Read
    off `Settings.effort_for`, which reads the argv the call will execute --
    `retrieval.permitted`'s direction, for its reason.

    The fictional absolute path is the one `test_cli.py` uses and for the same
    reason: only the basename is load-bearing, and a home-directory path is a
    seeded positive for `scan_release`'s own detector.
    """
    known = "/opt/claude-cli/bin/claude --print --model sonnet"
    settings = config.Settings(command=known, window=200000,
                               models={"merge": "test-model"}, use_cache=False)
    block = Provenance(settings=settings, client=Client(settings),
                       roles=("merge",), duration_seconds=0.0).as_dict()
    effort = block["decoding"].get("effort")
    check(isinstance(effort, dict),
          f"decoding.effort must be a map of role -> level, got {effort!r}")
    check(effort == {"decompose": "low", "merge": "medium", "verify": "low"},
          f"and it must name every role the run will make a call for: {effort!r}")
    for role, level in (effort or {}).items():
        check(settings.command_for(role).endswith(f"--effort {level}"),
              f"the block must agree with {role}'s own argv: "
              f"{settings.command_for(role)!r}")
    check("effort_ignored" not in block["decoding"],
          "nothing was asked for that could not be delivered, so nothing is "
          "claimed to have been dropped")

    # An HTTP endpoint has no flag to carry a level, so the key is absent
    # rather than present and empty -- every recorded figure in this project
    # was produced over HTTP and none of them gains a claim about effort.
    over_http = config.Settings(base_url="http://localhost:11434/v1",
                                models={"merge": "test-model"}, use_cache=False)
    plain = Provenance(settings=over_http, client=Client(over_http),
                       roles=("merge",), duration_seconds=0.0).as_dict()
    check("effort" not in plain["decoding"],
          f"an HTTP run must claim no level: {plain['decoding']!r}")

    # And a level that was asked for and cannot be delivered is published as
    # dropped rather than silently discarded.
    asked = config.Settings(base_url="http://localhost:11434/v1",
                            models={"merge": "test-model"}, use_cache=False,
                            effort={"merge": "max"})
    told = Provenance(settings=asked, client=Client(asked),
                      roles=("merge",), duration_seconds=0.0).as_dict()
    check(told["decoding"].get("effort_ignored") == ["merge"],
          f"a level this backend cannot carry has to be said out loud: "
          f"{told['decoding']!r}")


def test_a_merge_that_fits_is_not_refused_and_the_guard_charges_both_halves() -> None:
    """The prompt is charged too, so a window between the two figures refuses.

    `budget_tokens` alone would fit; prompt plus budget does not. A guard that
    checked only the ceiling would pass this request and let the server trim the
    front of the document off, which is the silent half of the failure.
    """
    budget = merge.budget_tokens(TWO, config.DEFAULT_FIDELITY)
    prompt, fidelity_rules, _example, title_rule = merge.compose_prompt(
        merge.MergePolicy())
    rendered = prompt.render(
        fidelity_rules=fidelity_rules, fidelity_example=_example,
        title_rule=title_rule, base_filename=FIRST,
        sources=segment.render_sources(segment.segment_sources(TWO), FIRST),
    )
    needed = merge.request_tokens(rendered, budget)
    check(needed > budget,
          f"the prompt must cost something, got {needed} against a budget of {budget}")

    with tempfile.TemporaryDirectory() as raw, FakeEndpoint(
        lambda _b, _n: (200, envelope(merged("fits"))), served=needed
    ) as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        result = merge.merge_documents(Client(settings), TWO)
    check(result.document == "fits", f"a request that exactly fits must run, got {result!r}")

    with tempfile.TemporaryDirectory() as raw, FakeEndpoint(
        lambda _b, _n: (200, envelope(merged("fits"))), served=budget
    ) as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        exc = raises(window.BudgetExceedsWindow,
                     lambda: merge.merge_documents(Client(settings), TWO),
                     "a window that fits the ceiling but not the prompt must refuse")
    check(exc is not None and f"Over by {needed - budget}." in str(exc),
          f"the overrun must be exactly the prompt, {needed - budget} tokens, got {exc!r}")


def test_a_replay_run_asks_no_window_because_it_sends_nothing() -> None:
    """The one path that must open no socket, and the guard must not be it."""
    with tempfile.TemporaryDirectory() as raw:
        settings = config.Settings(
            base_url="http://127.0.0.1:1/v1", models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
            replay_dir=Path(raw) / "responses",
        )
        (Path(raw) / "responses").mkdir()
        replaying = Client(settings)
        check(replaying.served_window("merge") is None,
              "a replay run must not ask an endpoint anything")
        # And must not reach the load either. `served_window` returning None is
        # what keeps `window` -- and therefore `transport` -- out of this path;
        # warming behind it would have made the module a way for a replay to
        # open a socket, which is the one thing this path exists to rule out.
        check(replaying.usage.warmups == 0, "a replay run must warm nothing")

        dry = config.Settings(
            base_url="http://127.0.0.1:1/v1", models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False, dry_run=True,
        )
        drying = Client(dry)
        check(drying.served_window("merge") is None,
              "a dry run must not ask an endpoint anything")
        check(drying.usage.warmups == 0, "a dry run must warm nothing")


def test_an_endpoint_that_will_not_say_is_not_given_a_default() -> None:
    """A default here would be the hard-coded number this mechanism exists to remove."""
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("x"))), loaded=("something-else",))
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        # An unmatched name is a loadable cause, so this now goes through one
        # load attempt on its way to the same refusal. The console is captured
        # rather than silenced so the suite's own output stays a report.
        exc = raises(window.WindowUnknown,
                     lambda: merge.merge_documents(
                         Client(settings, console=Console(io.StringIO())), TWO),
                     "an endpoint with the model unloaded must not be guessed at")
    check(exc is not None and "test-model" in str(exc),
          f"the failure must name the model it looked for, got {exc!r}")
    check(live.calls == 0, f"nothing may be sent on an unknown window, sent {live.calls}")


def test_a_cold_endpoint_is_loaded_rather_than_reported_at() -> None:
    """The remedy window.py already described, performed instead of printed.

    `/api/ps` empty means the model is not resident, which on a pod that was
    just started is the normal first second of its life rather than a fault.
    The fake answers empty once and populated after a load, which is the whole
    of the retry logic without needing a genuinely cold pod to see it.
    """
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("x"))),
                        loaded=(), loads_on_warm=True)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        told = io.StringIO()
        client = Client(settings, console=Console(told))
        result = merge.merge_documents(client, TWO)

    check(result.document == "x", "a warmed endpoint must go on to do the work")
    # Tens of seconds of silence is the thing being fixed, so the load has to
    # announce itself without being asked for -- no `-v` was passed here.
    said = told.getvalue()
    check("test-model" in said and "loading" in said,
          f"the load must say what it is doing while it does it: {said!r}")
    check(len(live.loads) == 1, f"exactly one load attempt, made {len(live.loads)}")
    load = live.loads[0]
    check(load.get("model") == "test-model",
          f"the load must name the model the window was wanted for: {load!r}")
    check(load.get("prompt") == "",
          f"the load must generate nothing, only resident: {load!r}")
    check(load.get("keep_alive"), f"the load must say how long to stay: {load!r}")

    # The isolation that keeps this out of every measurement: a load is not a
    # call. It is keyed into no cassette, is charged to no budget, and is
    # counted on its own axis.
    check(client.usage.warmups == 1, f"the load must be counted, got {client.usage.warmups}")
    check(client.usage.calls == live.calls,
          f"and must not be charged as a call: {client.usage.calls} vs {live.calls}")


def test_a_load_that_does_not_load_gives_up_after_one_attempt() -> None:
    """One attempt, then the original error. No retry loop, no backoff.

    An endpoint that accepts the load and still reports nothing resident is
    either not ollama or is broken, and asking it twice more would only make
    the operator wait longer for the same sentence.
    """
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("x"))),
                        loaded=(), loads_on_warm=False)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        client = Client(settings, console=Console(io.StringIO()))
        exc = raises(window.WindowUnknown,
                     lambda: merge.merge_documents(client, TWO),
                     "an endpoint that will not load must still refuse to guess")

    check(exc is not None and "test-model" in str(exc),
          f"the failure must still name the model, got {exc!r}")
    check(len(live.loads) == 1, f"exactly one attempt, made {len(live.loads)}")
    check(live.calls == 0, f"and nothing may be sent after it, sent {live.calls}")
    check(client.usage.warmups == 0,
          f"a load that did not load is not a load, got {client.usage.warmups}")


def test_a_load_reaches_the_record_and_only_when_it_happened() -> None:
    """A warmed run and a warm run must be distinguishable afterwards.

    And a run that was already warm has to record exactly what it recorded
    before this mechanism existed: every published figure was measured by one,
    and an unconditional row would rewrite all of their provenance blocks to
    say `0` about a thing that did not exist when they were taken.
    """
    live = FakeEndpoint(lambda _b, _n: (200, envelope(merged("x"))),
                        loaded=(), loads_on_warm=True)
    with tempfile.TemporaryDirectory() as raw, live as base_url:
        settings = config.Settings(
            base_url=base_url, models={"merge": "test-model"},
            cache_dir=Path(raw) / "cache", use_cache=False,
        )
        warmed = Client(settings, console=Console(io.StringIO()))
        merge.merge_documents(warmed, TWO)
        was_warm = Client(settings, console=Console(io.StringIO()))  # resident now
        merge.merge_documents(was_warm, TWO)

        record = Provenance(settings=settings, client=warmed, roles=("merge",),
                            duration_seconds=1.0)
        already = Provenance(settings=settings, client=was_warm, roles=("merge",),
                             duration_seconds=1.0)

    check(record.as_dict()["counts"]["model_loads"] == 1,
          "a warmed run must say so in the record")
    check(already.as_dict()["counts"]["model_loads"] == 0,
          "and a run that found it loaded must say that")
    check("| Model loads | 1 |" in record.as_markdown(),
          f"the markdown must carry the row when it happened:\n{record.as_markdown()}")
    check("Model loads" not in already.as_markdown(),
          "and must not add a row to a run that recorded none")


def test_the_window_root_survives_a_path_prefix() -> None:
    """The hosted deployments serve under a prefix; `/v1` is the only part dropped."""
    for base, root in (
        ("http://localhost:11434/v1", "http://localhost:11434"),
        ("http://localhost:11434/v1/", "http://localhost:11434"),
        # A path prefix, which is what a proxied deployment serves under. On
        # loopback because `acceptance_7_no_secrets_committed` greps every
        # tracked file for anything shaped like a hosted endpoint, and it is
        # right to: the shape is the secret, not the host that happens to be
        # in it.
        ("http://127.0.0.1:8080/pod/abc/v1", "http://127.0.0.1:8080/pod/abc"),
        ("http://127.0.0.1:8080/pod/abc", "http://127.0.0.1:8080/pod/abc"),
    ):
        got = window._root(base)
        check(got == root, f"{base} must resolve to {root}, got {got}")


def test_merge_offline() -> None:
    """pytest entry point."""
    main()
    assert not failures, "\n".join(failures)


def test_an_addition_record_is_checked_for_shape_and_not_for_truth() -> None:
    """`check_merge`'s third list, and where the line falls in it.

    Everything this function returns is fed back to the model verbatim on
    retry, so everything said here is a prompt. That puts a hard line through
    the middle of an addition record: the shape is repairable and belongs
    here, and whether the statement is *true* is not repairable by rewriting
    the response and belongs nowhere in this package -- the documents are all
    the tool checks against, and an addition is by construction not in them.

    `corrects` is the one required field not checked for emptiness, and that
    is deliberate rather than an oversight. An addition may extend documents
    that are thin rather than wrong, and a rule demanding every one name what
    it corrects would be a rule telling the model to invent a victim.
    """
    base = {"merged_document": "text", "dispositions": [], "decisions": []}

    def record(**over):
        full = {"statement": "S", "corrects": "", "basis": "own-knowledge",
                "source": "", "reason": "why"}
        full.update(over)
        return {name: full[name] for name in parsing.ADDITION_FIELDS
                if name in full}

    def faults(additions):
        return [str(e) for e in parsing.check_merge({**base, "additions": additions})
                if "additions" in str(e)]

    check(faults([]) == [], "no additions, nothing to say about them")
    check(parsing.check_merge(base) == [],
          "and a payload with no `additions` key at all -- every level below "
          "`open` -- must not be charged for the absence of a list its schema "
          "never offered it")

    blank = faults([record(statement="   ")])
    check(len(blank) == 1 and "statement is empty" in blank[0],
          f"a declaration with nothing in it declares nothing: {blank}")
    check("copied from your merged document" in blank[0],
          "and the message says what to put there, because it is a prompt")

    reason = faults([record(reason="  ")])
    check(len(reason) == 1 and "reason is empty" in reason[0],
          f"the bargain at this level is that an addition is owned and "
          f"explained, so an unexplained one is not a declaration: {reason}")

    check(faults([record()]) == [],
          "an empty `corrects` is not a fault; forcing every addition to name "
          "a victim would be telling the model to invent one")

    out_of_order = {"reason": "why", "statement": "S", "corrects": "",
                    "basis": "own-knowledge", "source": ""}
    order = faults([out_of_order])
    check(any("in that order" in e for e in order),
          f"field order is the contract here as in the other two lists: {order}")
    check(all(isinstance(e, parsing.OrderFault)
              for e in parsing.check_merge({**base, "additions": [out_of_order]})),
          "and an out-of-order record is *only* an order fault, so the retry "
          "is the cheap one rather than a full re-answer")

    # Nothing here reads the fidelity, and nothing here should: the schema has
    # already decided whether the model was allowed to speak, and a payload
    # carrying the key at a level that does not offer it was rejected by
    # `validate` before this function ever saw it.
    check(faults([record()]) == [],
          "a well-formed record passes on its shape alone")

    # --- `basis` and `source`, and the dependency between them ---
    #
    # The single most load-bearing pair in this record. A field that makes "no
    # source" feel like a failure is a field that manufactures fake sources,
    # so `own-knowledge` has to be a complete answer -- and the check that
    # makes it one is the refusal of a source written beside it.
    missing = faults([record(basis="")])
    check(len(missing) == 1 and ".basis is ''" in missing[0],
          f"`basis` is required and has no default: a record that does not "
          f"say what it rests on is refused rather than assumed: {missing}")
    check("own-knowledge" in missing[0] and "expected one" in missing[0],
          "and because this message is a prompt, it has to say that "
          "`own-knowledge` is a respectable answer, or the retry invents a URL")

    unknown = faults([record(basis="training data")])
    check(len(unknown) == 1 and ".basis is 'training data'" in unknown[0],
          f"the enum is closed; a third basis is a third meaning nothing "
          f"downstream knows how to render: {unknown}")

    uncited = faults([record(basis="citation", source="  ")])
    check(len(uncited) == 1 and ".source is empty" in uncited[0],
          f"`citation` with nothing to cite is the word a reader weighs "
          f"attached to nothing they can check: {uncited}")
    check("own-knowledge" in uncited[0],
          "and the repair offered is the honest one, not 'think of a source'")

    both = faults([record(basis="own-knowledge",
                          source="https://example.invalid/spec")])
    check(len(both) == 1 and ".source is filled" in both[0],
          f"and the inverse, which is the failure this enum exists to stop "
          f"arriving one step later: a model that answered 'no source' and "
          f"then wrote one has produced the artefact anyway: {both}")

    check(faults([record(basis="citation", source="RFC 2119")]) == [],
          "a cited record passes on its shape; whether the source says what "
          "the statement claims is unanswerable anywhere in this package")

    # Nothing in this package resolves a citation, and the check that proves it
    # is `tests/test_socket_guard.py` over a run carrying one. Said here too
    # because this is where a reader looks for what `source` means.
    check("citation" in parsing.BASES and "own-knowledge" in parsing.BASES
          and len(parsing.BASES) == 2,
          f"two bases, and the second is not an escape hatch: {parsing.BASES}")


def test_every_schema_is_accepted_by_strict_json_schema_mode() -> None:
    """A property absent from `required` costs the whole tier, silently.

    OpenAI's `json_schema` mode is sent with `strict: true`, and strict mode
    refuses a schema whose `properties` are not all listed in `required`. The
    refusal does not say that: the tier ladder reads it as "this endpoint
    cannot do json_schema", steps down to `prompt`, and the run finishes at
    the weakest rung having reported nothing unusual.

    That is what `decisions[].chosen` did. It was made optional at `off`,
    `low` and `mid`, correctly: those levels forbid choosing a winner, and it
    left the property in `properties`. Every run at those levels against that
    vendor fell to `prompt` while `high` got `json_schema`: six runs in
    `toby-test-9`, six matches, no exceptions, and **every published figure in
    this project was measured at `json_schema`**.

    Asserted over every level and recursively, because the next optional
    property will be added somewhere else in the tree.
    """
    def optional(schema: dict, path: str = "$") -> list:
        found = []
        properties = set(schema.get("properties") or {})
        required = set(schema.get("required") or [])
        if properties - required:
            found.append((path, sorted(properties - required)))
        for name, shape in (schema.get("properties") or {}).items():
            if not isinstance(shape, dict):
                continue
            if shape.get("type") == "array" and isinstance(shape.get("items"), dict):
                found += optional(shape["items"], f"{path}.{name}[]")
            elif shape.get("type") == "object":
                found += optional(shape, f"{path}.{name}")
        return found

    for level in (*config.FIDELITY_LEVELS, None):
        loose = optional(merge.merge_schema(level))
        check(not loose,
              f"merge_schema({level!r}) has properties outside `required` "
              f"{loose}; strict json_schema refuses the whole schema for this "
              f"and the ladder degrades the run to `prompt` without saying so")

    # The other two schemas this tool sends, on the same terms.
    from llossless.decompose import CLAIM_SCHEMA
    from llossless.verify import VERDICT_SCHEMA
    for name, schema in (("CLAIM_SCHEMA", CLAIM_SCHEMA),
                         ("VERDICT_SCHEMA", VERDICT_SCHEMA)):
        loose = optional(schema, "$")
        check(not loose, f"{name} has properties outside `required`: {loose}")

    # And the property that made this reachable: a level that forbids choosing
    # drops the key rather than carrying it optional, which is the answer
    # `additions` already gets one function over.
    # Derived from `MAY_CHOOSE` rather than from two literal lists. A sixth
    # level was added to that table and to nothing else, and a check written
    # as two tuples would have gone on asserting the five it knew about.
    for level, may in merge.MAY_CHOOSE.items():
        item = merge.merge_schema(level)["properties"]["decisions"]["items"]
        if may:
            check("chosen" in item["properties"] and "chosen" in item["required"],
                  f"{level} must require it: {item['required']}")
        else:
            check("chosen" not in item["properties"],
                  f"{level} must not offer `chosen` at all: {list(item['properties'])}")


def test_only_open_is_handed_the_addition_record_at_all() -> None:
    """`basis` and `source` reach one level, in `properties` and not only in
    `required`.

    The distinction is the point the schema check above makes: a property a level does not use still
    costs that level the `json_schema` tier on a strict vendor, and the ladder
    steps down to `prompt` without saying so. So "absent from `required`" is
    not the property to assert -- `additions` has to be absent from
    `properties`, which is what keeps every level below `open` on the schema
    and the cassette keys it already had.

    Asserted by walking the schema for the field names rather than by checking
    `additions`, because the next field added to this record will be added to
    `addition_item` and to nothing else, and a check written against the list
    name would not notice.
    """
    new = ("basis", "source")

    def properties_anywhere(schema: dict) -> set[str]:
        found = set(schema.get("properties") or {})
        for shape in (schema.get("properties") or {}).values():
            if not isinstance(shape, dict):
                continue
            if shape.get("type") == "array" and isinstance(shape.get("items"), dict):
                found |= properties_anywhere(shape["items"])
            elif shape.get("type") == "object":
                found |= properties_anywhere(shape)
        return found

    # Off `ADDS`, not off a literal list, for `MAY_CHOOSE`'s reason one
    # function up: `sourced` joined that table and would have been checked by
    # neither branch of a pair of hard-coded tuples.
    for level, adds in merge.ADDS.items():
        names = properties_anywhere(merge.merge_schema(level))
        if adds:
            for field in ("additions", *new):
                check(field in names,
                      f"`{level}` must carry `{field}`: {sorted(names)}")
            continue
        check("additions" not in names,
              f"{level} must not be handed `additions` at all: {sorted(names)}")
        for field in new:
            check(field not in names,
                  f"{level} carries `{field}` in `properties`; a level that "
                  f"permits no addition must not hold the field, or strict "
                  f"json_schema costs it the whole tier")

    # And the unthreaded call, which fails closed for `decision_item`'s reason:
    # a path that forgot the level must not hand out the widest schema.
    check("additions" not in properties_anywhere(merge.merge_schema(None)),
          "`merge_schema(None)` must not offer additions; a caller that forgot "
          "the level has not established that the level permits any")

    item = merge.addition_item()
    check(item["properties"]["basis"]["enum"] == list(parsing.BASES),
          f"`basis` is a closed enum in the schema, not a free string: a "
          f"grammar-constrained model then cannot write anything but one of "
          f"the two, which is what makes 'no source' a token it can emit "
          f"rather than a sentence it has to compose: {item['properties']['basis']}")
    check(set(item["required"]) == set(parsing.ADDITION_FIELDS),
          f"every property required, or strict json_schema costs the whole tier: {item['required']}")


def test_the_sixth_level_changes_the_expectation_and_not_the_schema() -> None:
    """`sourced` asks the model to retrieve; it widens no record contract.

    The failure this is written against is the one the level exists to prevent
    in the report, moved one layer down: a level that says "go and check" and
    quietly relaxed what may be asserted undeclared would give a reader
    citations *and* a clean exit code for statements nobody checked.

    So the schema is the assertion. `sourced` gets `open`'s, deep-equal, and
    every level below it gets exactly the property set it had -- pinned as
    literals here, because the point is that adding a level changed none of
    them and a set derived from the same code that builds them could not say
    so.
    """
    def properties_anywhere(schema: dict) -> set[str]:
        found = set(schema.get("properties") or {})
        for shape in (schema.get("properties") or {}).values():
            if not isinstance(shape, dict):
                continue
            if shape.get("type") == "array" and isinstance(shape.get("items"), dict):
                found |= properties_anywhere(shape["items"])
            elif shape.get("type") == "object":
                found |= properties_anywhere(shape)
        return found

    base = ["candidates", "decisions", "disposition", "dispositions", "document",
            "merged_document", "mismatch", "reason", "replacement", "segment",
            "slot", "text"]
    pinned = {
        "off": base,
        "low": base,
        "mid": base,
        "high": sorted(base + ["chosen"]),
        "open": sorted(base + ["chosen", "additions", "basis", "corrects",
                               "source", "statement"]),
    }
    for level, names in pinned.items():
        found = sorted(properties_anywhere(merge.merge_schema(level)))
        check(found == sorted(names),
              f"adding a level moved {level}'s schema: {found} != {sorted(names)}")

    check(merge.merge_schema("sourced") == merge.merge_schema("open"),
          "sourced must be handed open's record contract unchanged; what the "
          "level moves is what the model is asked to do before it declares")

    # Every table a level has to appear in, checked as membership rather than
    # by reading the file. Four of these carry an import-time assert and fail
    # loudly; `parsing.DERIVES` is the one that does not, and a level missing
    # from it is handed the four-label schema with no error anywhere.
    check(config.SOURCED in parsing.DERIVES,
          "sourced keeps open's joint-derivation licence, so it must be in "
          "DERIVES or the reverse pass reads every licensed combination as an "
          "invention with nothing to say why")
    check(merge.ADDS[config.SOURCED] and merge.MAY_CHOOSE[config.SOURCED]
          and reconcile.COVERS[config.SOURCED],
          "sourced keeps every licence open has")
    check(reconcile.PERMITTED[config.SOURCED] == reconcile.PERMITTED["open"],
          "a disposition names what happened to a source segment, and this "
          "level adds no sixth verb for one")
    check(parsing.verdicts_for(config.SOURCED) == parsing.verdicts_for("open")
          and parsing.evidenced_for(config.SOURCED) == parsing.evidenced_for("open"),
          "the label sets must be open's, or the level is graded under rules "
          "nobody chose for it")

    # And the level really is the last rung: `FIDELITY_LEVELS` promises the
    # ladder is ordered, and a reader relies on that without reading it.
    check(config.FIDELITY_LEVELS[-1] == config.SOURCED,
          f"sourced sits above open: {config.FIDELITY_LEVELS}")


def test_the_sourced_fragments_say_what_the_level_permits_and_what_it_costs() -> None:
    """The description a person reads is the one the model is given.

    `web/api.fidelity_levels` serves the opening paragraph of the merge
    fragment as the level's explanation, so the sentence about the page's one
    disclosure -- that a query or a fetch may carry text from the documents --
    has to be *in that paragraph* rather than further down the file. A version
    of this that checked the whole text would pass on a fragment whose first
    paragraph says nothing about it, which is the only part the picker shows.
    """
    opening = " ".join(
        prompts.load("fidelity/sourced.merge").text.split("\n\n")[0].split())
    check(opening.startswith("Fidelity level: sourced."),
          f"the fragment must open with the preamble the picker strips: {opening[:60]!r}")
    for phrase in ("web tool", "documents being merged"):
        check(phrase in opening,
              f"the level's own description must say that {phrase!r} is part of "
              f"what selecting it means: {opening!r}")

    whole = prompts.load("fidelity/sourced.merge").text
    check("makes no network request of any kind" in whole,
          "the fragment must keep the sentence about what *this* tool does, "
          "which never changes and is the half a retrieval grant makes easy "
          "to forget")
    flat = " ".join(whole.split())
    check("declare every such statement in `additions`" in flat,
          "the undeclared-addition rule is open's and is not relaxed here")
    check("is an invention by every test this tool has, and is reported as one"
          in flat,
          "and the consequence of not declaring one is said in the same words "
          "open says it in")

    # Every role has a file, because `web/api.fidelity_levels` loads every cell
    # of levels x roles and a missing one is a 500 on `GET /config` rather than
    # a level that renders oddly.
    for role in ("merge", "verify", "verify_reverse", "example"):
        path = ROOT / "prompts" / "fidelity" / f"sourced.{role}.md"
        check(path.is_file(), f"prompts/fidelity/sourced.{role}.md must exist")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_merge_offline" and callable(function):
            function()

    if failures:
        print(f"{len(failures)} failing:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("merge: all offline checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
