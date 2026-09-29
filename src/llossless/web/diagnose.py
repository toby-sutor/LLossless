"""Engine failures, said again in terms of what the operator can do about them.

The engine's messages are written for whoever is reading a terminal with the
configuration in front of them. One of them reached a browser and was, in the
operator's own words, useless:

    decompose document 2: WindowUnknown: localhost has no model named
    gpt-5.6-terra loaded; loaded: qwen3-8b:latest

Every word of that is true and none of it says what happened. The operator had
picked a hosted model out of a picker, and a picker that offers a model the
server cannot reach is the defect -- but the message is the last line of
defence for the case where it still happens, and this is the line that has to
say so: the name went to an endpoint that does not serve it, here is which
endpoint answered, here is what to change.

**The engine's own message is not edited.** `window.py` raises what it raises,
`report.json` records the step detail verbatim, and the command line prints
what it always printed. This module runs at the web boundary and *adds* a
sentence, because a record and an explanation are two different jobs: a reader
comparing this run against a recorded one needs the string the engine actually
produced, and the operator needs to be told what to do. Appending rather than
replacing keeps both, and means nothing here can lose a detail by paraphrasing
it.

**Nothing is invented.** Every noun in the added sentence is lifted out of the
message being explained -- the endpoint's own name for itself, the model that
was asked for, the models it does have. A translation that reached for the
run's settings to name something the original did not would be able to disclose
more than the thing it is explaining, and the whole point of translating at
this layer is that it cannot.

**Recognised by shape, and silent when it is not.** An unrecognised message is
returned unchanged. A translator that guessed would eventually explain a
message as something it is not, which is worse than the untranslated one: the
operator would act on the explanation.
"""

from __future__ import annotations

import re

# `window.reported` ends its refusal with one of two tails: the endpoint's name
# for itself, the model that was asked for, and then either the models it does
# have or the fact that it has none. Anchored at the end of the string, because
# everything in front of it is a step name and an exception class that this
# module has no opinion about and must not eat.
#
# The endpoint's name is `Settings.endpoint_name`: a host, or -- for a labelled
# deployment -- an endpoint id and deliberately not an address. Whichever it is,
# it is what the engine chose to disclose, and repeating it discloses nothing
# further.
NO_SUCH_MODEL = re.compile(
    r"(?P<endpoint>\S+) has no model named (?P<model>.+?) loaded"
    r"(?:; loaded: (?P<loaded>.*)| and nothing else either)\Z")


def explain(message: str) -> str:
    """The message, plus a sentence saying what actually went wrong. Or unchanged.

    The one shape recognised today is a model requested from an endpoint that
    does not serve it, which is the failure a model picker with no endpoint
    behind it produces every single time. It is added to rather than replaced;
    see the module docstring.
    """
    if not isinstance(message, str) or not message:
        return message
    match = NO_SUCH_MODEL.search(message)
    if match is None:
        return message
    endpoint = match.group("endpoint")
    model = match.group("model")
    loaded = (match.group("loaded") or "").strip()
    has = (f"What {endpoint} does serve: {loaded}."
           if loaded else f"{endpoint} is serving no model at all.")
    return (
        f"{message} -- {model} was requested from the endpoint at {endpoint}, "
        f"and that endpoint does not serve it. {endpoint} answered, so this is "
        f"not a network fault: the model name went to a host that does not "
        f"have it. {has} Configure an endpoint for this model's provider on "
        f"the credentials sheet so the model is sent where it is served, or "
        f"pick a model this endpoint has.")
