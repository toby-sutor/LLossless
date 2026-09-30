#!/usr/bin/env python3
"""The two-pane workbench (redesign B): its tabs and the way a
blocked run leads to its step.

What a file read can hold, each with seeded probes beside it:

**the tablists.** The step tabs, the output tabs and the finding tabs are
WAI-ARIA tablists: every tab has an id and `aria-controls` naming a
`role="tabpanel"` that is `aria-labelledby` it, exactly one tab per list is
`aria-selected` and it alone is the tab stop. The steps are Documents, Model,
Settings, Tuning, numbered 1 to 4, and each step panel's heading carries its
own number. Each finding section is the panel of one tab, the tab carries the
section's chip, and a section that starts hidden starts with its tab hidden.

**the blocked run.** `readiness` names the documents step on each of its
document reasons, `blockingStep` gives the model step to the one reason
without a step, `refreshIdleStatus` hands its answer to `renderStepGoto`, and
the button that goes there sits in the run bar. Driven under node through the
shipped script as well: an empty page points at step 1, a model refusal at
step 2, a ready page at nothing.

**the second pass.** The pane divider is a focusable separator with a value
and keys; every "?" is a named button described by the text in its own box;
merge effort is the Settings step's first item and the Settings tab has a
"new" marker for it; the Compare levels dialog says it is an illustration and
has a sample and a short line per level in both languages; the language
picker is a globe with a bilingual name.

The browser half (keyboard, focus, the pointer on the disabled Run button, no
page or pane scroll at 1280x800, the divider dragged) was driven in Chromium
separately from the checks below.

Run with `python3 tests/test_web_layout.py`, or collect with pytest.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# The node drive asks a loopback server for `/config`, through the helpers
# `test_web_static` already has; nothing leaves this machine.
socket_guard.install()

import test_web_static as static  # noqa: E402

STATIC = ROOT / "src" / "llossless" / "web" / "static"
INDEX = STATIC / "index.html"
APP_JS = STATIC / "app.js"
LAYOUT_CSS = STATIC / "layout.css"

STEPS = ("documents", "model", "settings", "tuning")
FINDINGS = ("review", "conflicts", "omitted", "attributions", "numbers",
            "additions", "claims", "checks")
TABLISTS = ("step-tabs", "output-tabs", "finding-tabs")

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# the markup, parsed
# --------------------------------------------------------------------------

VOID = {"meta", "link", "input", "br", "img", "hr", "source", "col", "area",
        "base", "wbr", "track", "embed", "param"}


class Tree(HTMLParser):
    """Every element with its attributes, its parent chain and its text."""

    def __init__(self) -> None:
        super().__init__()
        self.nodes: list[dict] = []
        self.stack: list[dict] = []
        self.in_template = 0

    def handle_starttag(self, tag, attrs):
        if tag == "template":
            self.in_template += 1
        node = {"tag": tag, "attrs": dict(attrs), "parents": list(self.stack),
                "text": "", "template": self.in_template > 0}
        if not node["template"]:
            self.nodes.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if tag == "template":
            self.in_template -= 1
        while self.stack:
            if self.stack.pop()["tag"] == tag:
                break

    def handle_data(self, data):
        for node in self.stack:
            node["text"] += data


def parse(html: str) -> list[dict]:
    tree = Tree()
    tree.feed(html)
    return tree.nodes


def by_id(nodes: list[dict]) -> dict[str, dict]:
    return {n["attrs"]["id"]: n for n in nodes if "id" in n["attrs"]}


def hook(nodes: list[dict], name: str) -> dict | None:
    found = [n for n in nodes if n["attrs"].get("data-cc") == name]
    return found[0] if len(found) == 1 else None


def tabs_of(nodes: list[dict], list_hook: str) -> list[dict]:
    listing = hook(nodes, list_hook)
    if listing is None:
        return []
    return [n for n in nodes if n["attrs"].get("role") == "tab"
            and any(p is listing for p in n["parents"])]


def tablist_problems(html: str) -> list[str]:
    """Every way the three tablists break the WAI-ARIA tabs pattern."""
    nodes = parse(html)
    ids = by_id(nodes)
    found = []
    for name in TABLISTS:
        listing = hook(nodes, name)
        if listing is None:
            found.append(f"there is no single {name}")
            continue
        if listing["attrs"].get("role") != "tablist":
            found.append(f"{name} is not role=tablist")
        if not (listing["attrs"].get("aria-label") or listing["attrs"].get("aria-labelledby")):
            found.append(f"{name} has no accessible name")
        tabs = tabs_of(nodes, name)
        if len(tabs) < 2:
            found.append(f"{name} holds {len(tabs)} tabs")
        selected = [t for t in tabs if t["attrs"].get("aria-selected") == "true"]
        if len(selected) != 1:
            found.append(f"{name}: {len(selected)} tabs are aria-selected")
        for tab in tabs:
            a = tab["attrs"]
            tid = a.get("id", "")
            if tab["tag"] != "button" or a.get("type") != "button":
                found.append(f"{name}: tab {tid or '?'} is not a <button type=button>")
            if a.get("aria-selected") not in ("true", "false"):
                found.append(f"{name}: tab {tid} has no aria-selected")
            want = "0" if a.get("aria-selected") == "true" else "-1"
            if a.get("tabindex") != want:
                found.append(f"{name}: tab {tid} has tabindex {a.get('tabindex')}, not {want}")
            panel = ids.get(a.get("aria-controls", ""))
            if not tid or panel is None:
                found.append(f"{name}: tab {tid or '?'} controls nothing")
                continue
            if panel["attrs"].get("role") != "tabpanel":
                found.append(f"{name}: {panel['attrs'].get('id')} is not role=tabpanel")
            if panel["attrs"].get("aria-labelledby") != tid:
                found.append(f"{name}: {panel['attrs'].get('id')} is not labelled by {tid}")
            off = "tab-off" in panel["attrs"].get("class", "").split()
            if (a.get("aria-selected") == "true") == off:
                found.append(f"{name}: {tid}'s panel is {'off' if off else 'on'} "
                             f"while the tab is {'' if not off else 'not '}selected")
    return found


def step_problems(html: str) -> list[str]:
    """The four steps, in order, numbered, each heading carrying its number."""
    nodes = parse(html)
    ids = by_id(nodes)
    found = []
    tabs = tabs_of(nodes, "step-tabs")
    got = tuple(t["attrs"].get("data-step") for t in tabs)
    if got != STEPS:
        found.append(f"the steps are {got}, not {STEPS}")
    for n, tab in enumerate(tabs, start=1):
        step = tab["attrs"].get("data-step")
        number = [x for x in nodes if x["attrs"].get("class") == "step-n"
                  and any(p is tab for p in x["parents"])]
        if not number or number[0]["text"].strip() != str(n):
            found.append(f"step tab {step} does not show the number {n}")
        state = [x for x in nodes if x["attrs"].get("data-cc") == f"step-state-{step}"
                 and any(p is tab for p in x["parents"])]
        if not state:
            found.append(f"step tab {step} has no state line")
        panel = ids.get(f"step-{step}")
        if panel is None:
            found.append(f"there is no panel step-{step}")
            continue
        heading = [x for x in nodes if x["tag"] == "h2" and any(p is panel for p in x["parents"])]
        if not heading or heading[0]["attrs"].get("data-n") != str(n):
            found.append(f"step-{step}'s heading does not carry data-n={n}")
    # The run bar sits in the input pane, outside the part that scrolls, and
    # holds the way to a blocking step.
    run = hook(nodes, "run-card")
    body = hook(nodes, "input-body")
    goto = hook(nodes, "status-goto")
    if run is None or body is None:
        found.append("the run bar or the input pane's scroll area is missing")
    else:
        if any(p is body for p in run["parents"]):
            found.append("the run bar is inside the input pane's scroll area")
        if not any("pane-input" in p["attrs"].get("class", "") for p in run["parents"]):
            found.append("the run bar is not in the input pane")
    if goto is None or run is None or not any(p is run for p in goto["parents"]):
        found.append("the way to a blocking step is not in the run bar")
    elif goto["tag"] != "button" or "hidden" not in goto["attrs"]:
        found.append("the way to a blocking step must be a button that starts hidden")
    return found


def finding_problems(html: str) -> list[str]:
    """Each finding section is one tab's panel, the tab carries its chip, and
    a section that starts hidden starts with its tab hidden."""
    nodes = parse(html)
    ids = by_id(nodes)
    found = []
    tabs = {t["attrs"].get("aria-controls"): t for t in tabs_of(nodes, "finding-tabs")}
    for name in FINDINGS:
        section = hook(nodes, f"{name}-section")
        if section is None:
            found.append(f"there is no single {name}-section")
            continue
        sid = section["attrs"].get("id", "")
        tab = tabs.get(sid)
        if tab is None or ids.get(sid) is not section:
            found.append(f"{name}-section is no tab's panel")
            continue
        chip = [x for x in nodes if x["attrs"].get("data-cc") == f"{name}-chip"
                and any(p is tab for p in x["parents"])]
        if not chip:
            found.append(f"the {name} tab does not carry {name}-chip")
        if ("hidden" in section["attrs"]) != ("hidden" in tab["attrs"]):
            found.append(f"the {name} tab and its section disagree about hidden")
    if len(tabs) != len(FINDINGS):
        found.append(f"{len(tabs)} finding tabs for {len(FINDINGS)} sections")
    return found


# --------------------------------------------------------------------------
# the script: the blocked-run hook and the tab sync
# --------------------------------------------------------------------------

def script_problems(js: str) -> list[str]:
    """The wiring that takes a blocked run to its step."""
    js = static.strip_comments(js)
    found = []
    readiness = static.body_of(js, "function readiness()")
    docs_returns = re.findall(r'return \{ ready: false, step: "documents", text: t\("status\.', readiness)
    if len(docs_returns) != 3:
        found.append(f"readiness names the documents step on {len(docs_returns)} of its 3 document reasons")
    if "if (stranded) return { ready: false, text: stranded };" not in readiness:
        found.append("readiness no longer refuses a stranded model choice")
    blocking = static.body_of(js, "function blockingStep(")
    if 'return String(state.step || "model");' not in blocking or "state.ready" not in blocking:
        found.append("blockingStep does not give the model step to a reason without one")
    idle = static.body_of(js, "function refreshIdleStatus()")
    if "button.disabled = !state.ready;\n  setText(el(\"submit-label\"), submitLabel());\n  renderStepGoto(state);" not in idle:
        found.append("refreshIdleStatus does not hand what readiness said to renderStepGoto")
    goto = static.body_of(js, "function renderStepGoto(")
    if "go.hidden = !step;" not in goto or 'blockingStep(state)' not in goto:
        found.append("renderStepGoto does not show the button exactly while blocked")
    wired = static.body_of(js, "function wireLayout()")
    if 'el("status-goto").addEventListener("click"' not in wired or "goToBlocker(" not in wired:
        found.append("the readiness button is not wired to goToBlocker")
    if 'el("run-card").addEventListener("pointerup"' not in wired \
            or "blockingStep(readiness())" not in wired:
        found.append("a press on the disabled Run button does not lead to the blocking step")
    blocker = static.body_of(js, "function goToBlocker(")
    if "goToStep(step);" not in blocker or ".focus(" not in blocker:
        found.append("goToBlocker does not select the step and focus what needs the reader")
    sync = static.body_of(js, "function syncFindingTabs()")
    if "hidden = !panel || panel.hidden;" not in sync:
        found.append("syncFindingTabs does not hide a tab with its section")
    if "syncFindingTabs();" not in static.body_of(js, "function renderReport("):
        found.append("renderReport never syncs the finding tabs")
    if "syncHistoryTab();" not in static.body_of(js, "async function refreshHistory()"):
        found.append("refreshHistory never syncs the Previous runs tab")
    keys = static.body_of(js, "function wireTabs(")
    for key in ("ArrowRight", "ArrowLeft", "Home", "End"):
        if f'"{key}"' not in keys:
            found.append(f"the tabs do not answer {key}")
    if "wireLayout();" not in static.body_of(js, "function wire()"):
        found.append("wire never wires the layout")
    for name in ("function goToStep(", "function storedStep("):
        body = static.body_of(js, name)
        for use in re.finditer(r"localStorage", body):
            before = body[:use.start()]
            if before.count("try {") <= before.count("} catch"):
                found.append(f"{name.split()[1][:-1]} touches localStorage outside a try")
    return found


# Under node, through the shipped script, with the fake DOM `test_web_static`
# drives `readiness` with: each case sets the store, runs `refreshIdleStatus`
# and reads the button back.
GOTO_DRIVE = r"""
;(() => {
  if (!El.prototype.addEventListener) El.prototype.addEventListener = function () {};
  const out = {};
  for (const [tag, table] of Object.entries(INPUT.strings)) {
    strings = table;
    locale.tag = tag;
    store.config = INPUT.config;
    store.mergeModel = INPUT.model; store.checkModel = INPUT.model; store.splitRoles = false;
    const doc = (name, text) => ({ name, text });
    const cases = {
      none: [[doc("", ""), doc("", "")], false],
      one: [[doc("a.md", "text"), doc("", "")], false],
      ready: [[doc("", "text"), doc("", "more")], false],
      model: [[doc("", "text"), doc("", "more")], true],
    };
    out[tag] = {};
    for (const [name, [docs, typed]] of Object.entries(cases)) {
      store.docs = docs;
      store.runId = "";
      store.customOn = typed; store.customModel = typed ? "not-listed" : ""; store.customWindow = typed ? "7" : "";
      refreshIdleStatus();
      const go = hooks["status-goto"];
      out[tag][name] = { hidden: Boolean(go.hidden), step: go.getAttribute("data-step"), text: go.textContent,
                         disabled: Boolean(hooks["submit"].disabled),
                         states: ["documents", "model"].map((s) => hooks["step-state-" + s].textContent) };
    }
  }
  process.stdout.write(JSON.stringify(out));
})();
"""


def drive_goto(js: str) -> dict | None:
    node = static.node_command()
    if node is None:
        return None
    payload = static.served_config_with_routes()
    model = "command:" + payload["commands"]["routes"][0]["id"]
    program = (static.EFFORT_DOM + "\nconst INPUT = " + json.dumps(
        {"strings": static.catalogues(), "config": payload, "model": model})
        + ";\n" + js + GOTO_DRIVE)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
        handle.write(program)
        path = handle.name
    try:
        run = subprocess.run(node + [path], capture_output=True, text=True, timeout=120, cwd=ROOT)
    finally:
        os.unlink(path)
    if run.returncode != 0:
        return {"error": run.stderr[-600:]}
    return json.loads(run.stdout)


def goto_problems(driven: dict | None, tables: dict) -> list[str]:
    if driven is None:
        return []
    if "error" in driven:
        return [f"the goto drive did not run under node: {driven['error']}"]
    found = []
    for tag, table in sorted(tables.items()):
        at = driven.get(tag) or {}
        want = {"none": "documents", "one": "documents", "ready": "", "model": "model"}
        for case, step in want.items():
            got = at.get(case) or {}
            if step:
                name = table[{"documents": "documents.heading", "model": "step.model"}[step]]
                text = table["step.goto"].replace("{n}", "1" if step == "documents" else "2").replace("{name}", name)
                if got.get("hidden") or got.get("step") != step or got.get("text") != text:
                    found.append(f"{tag} {case}: the way to step {step} reads {got}")
                if not got.get("disabled"):
                    found.append(f"{tag} {case}: Run is enabled while blocked")
            elif not got.get("hidden") or got.get("disabled"):
                found.append(f"{tag} {case}: ready, but the way to a step shows or Run is disabled: {got}")
        states = (at.get("one") or {}).get("states") or ["", ""]
        short = table["step.state.docs.short"].replace("{n}", "1").replace("{min}", "2")
        if states[0] != short:
            found.append(f"{tag}: step 1's state with one of two filled reads {states[0]!r}, not {short!r}")
        fix = table["step.state.fix"]
        if ((at.get("model") or {}).get("states") or ["", ""])[1] != fix:
            found.append(f"{tag}: step 2's state on a model refusal is not {fix!r}")
    return found


# --------------------------------------------------------------------------
# the reconnecting flash: `watch`'s `EventSource.onerror` must not
# report the ordinary close at the end of a finished run as a drop.
# --------------------------------------------------------------------------

# `onStreamError` alone, over a fake `store`, a stub `poll` the scenario
# supplies, and a `say` that only records its calls. This drives the
# decision `onStreamError` makes: poll once, then judge by what came back
# and by the stream's own `readyState`, not `poll`'s own state machine,
# which belongs to `poll` itself to prove.
STREAM_ERROR_DOM = r"""
const store = { runId: "", report: null, stream: null };
globalThis.EventSource = { OPEN: 1, CONNECTING: 0, CLOSED: 2 };
let poll;
const said = [];
function say(tone, word, text) { said.push([tone, word, text]); }
function t(key) { return key; }
"""

# Four scenarios, each a stand-in `poll` that leaves `store` the way the real
# one would for that case (the real `poll` itself: a finished run closes the
# watch and sets the report; an interrupted, failed or cancelled run closes
# the watch too, with no report; a run still going touches neither; a stream
# that already reconnected on its own is read straight off the stream).
STREAM_ERROR_DRIVE = r"""
;(async () => {
  const out = {};
  async function run(name, before) {
    said.length = 0;
    store.runId = "run-1";
    store.report = null;
    const stream = { readyState: EventSource.CLOSED };
    store.stream = stream;
    before(stream);
    await onStreamError(stream, "run-1");
    out[name] = said.slice();
  }
  await run("finished", (stream) => {
    poll = async () => { store.stream = null; store.report = { ok: true }; };
  });
  await run("endedBadly", (stream) => {
    poll = async () => { store.stream = null; };
  });
  await run("stillGoing", (stream) => {
    poll = async () => {};
  });
  await run("reopened", (stream) => {
    poll = async () => { stream.readyState = EventSource.OPEN; };
  });
  process.stdout.write(JSON.stringify(out));
})();
"""


def drive_stream_error(js: str) -> dict | None:
    node = static.node_command()
    if node is None:
        return None
    program = (STREAM_ERROR_DOM + "\nasync " + static.js_function("onStreamError", js)
               + "\n}\n" + STREAM_ERROR_DRIVE)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
        handle.write(program)
        path = handle.name
    try:
        run = subprocess.run(node + [path], capture_output=True, text=True, timeout=120, cwd=ROOT)
    finally:
        os.unlink(path)
    if run.returncode != 0:
        return {"error": run.stderr[-600:]}
    return json.loads(run.stdout)


def stream_error_problems(driven: dict | None) -> list[str]:
    if driven is None:
        return []
    if "error" in driven:
        return [f"the stream-error drive did not run under node: {driven['error']}"]
    found = []
    shows = {name: any(call[1] == "word.reconnecting" for call in calls)
              for name, calls in driven.items()}
    if shows.get("finished"):
        found.append("a normally finished run shows the reconnecting status")
    if shows.get("endedBadly"):
        found.append("a run that ended interrupted, failed or cancelled shows the reconnecting status too")
    if shows.get("reopened"):
        found.append("a stream that already reconnected on its own still shows the reconnecting status")
    if not shows.get("stillGoing"):
        found.append("a run genuinely still going, with the stream not back open, never shows the reconnecting status")
    return found


# --------------------------------------------------------------------------
# the tests
# --------------------------------------------------------------------------

def test_the_three_tablists_follow_the_tabs_pattern() -> None:
    for problem in tablist_problems(source(INDEX)):
        check(False, problem)


def test_the_tablist_check_fires() -> None:
    html = source(INDEX)
    seeds = {
        "a tab that controls nothing": html.replace(' aria-controls="step-model"', "", 1),
        "two selected tabs": html.replace(
            'id="output-tab-history" aria-controls="history-panel"\n                aria-selected="false" tabindex="-1"',
            'id="output-tab-history" aria-controls="history-panel"\n                aria-selected="true" tabindex="0"', 1),
        "a panel labelled by another tab": html.replace(
            'aria-labelledby="finding-tab-claims"', 'aria-labelledby="finding-tab-checks"', 1),
        "a list that is not a tablist": html.replace(
            'class="finding-tabs" role="tablist"', 'class="finding-tabs"', 1),
        "a selected tab whose panel is off": html.replace(
            'class="card step-panel" role="tabpanel" id="step-documents"',
            'class="card step-panel tab-off" role="tabpanel" id="step-documents"', 1),
    }
    for what, seeded in seeds.items():
        check(seeded != html, f"the probe for {what} did not take")
        check(bool(tablist_problems(seeded)), f"the tablist check does not fire on {what}")


def test_the_steps_are_four_numbered_and_the_run_bar_is_pinned() -> None:
    for problem in step_problems(source(INDEX)):
        check(False, problem)


def test_the_step_check_fires() -> None:
    html = source(INDEX)
    seeds = {
        "a heading with the wrong number": html.replace('data-n="3"', 'data-n="03"', 1),
        "the steps out of order": html.replace('data-step="settings"', 'data-step="tunin"', 1),
        "the goto button out of the run bar": html.replace(
            '    <button type="button" class="ghost status-goto" data-cc="status-goto" hidden></button>\n', "", 1)
            .replace('<div class="pane-body" data-cc="input-body">',
                     '<button type="button" class="ghost status-goto" data-cc="status-goto" hidden></button>\n'
                     '    <div class="pane-body" data-cc="input-body">', 1),
    }
    for what, seeded in seeds.items():
        check(seeded != html, f"the probe for {what} did not take")
        check(bool(step_problems(seeded)), f"the step check does not fire on {what}")


def step_tab_width_problems(css: str) -> list[str]:
    """A step tab's width must come only from dividing the row, never from
    its own content, so switching a control's value (the title policy on
    Tuning, the picked model on Model, the effort marker on Settings) cannot
    resize the tab and unsettle the row. The desktop `.step-tab` rule
    is required to carry a `0` (or `0%`) flex-basis: an `auto` basis sizes
    the item off its content first and only tops it up, which is exactly
    the bug.
    """
    rule = re.search(r"\.step-tab\s*\{([^}]*)\}", css, flags=re.S)
    if not rule:
        return ["no .step-tab rule in layout.css"]
    body = rule.group(1)
    flex = re.search(r"flex:\s*([^;]+);", body)
    if not flex:
        return ["the .step-tab rule sets no `flex` shorthand"]
    basis = flex.group(1).split()[-1] if len(flex.group(1).split()) >= 3 else "auto"
    if basis not in ("0", "0%", "0rem", "0px"):
        return [f".step-tab's flex-basis is {basis!r}, not zero: its width "
                f"can track its own content and resize with it"]
    return []


def test_a_step_tabs_width_never_tracks_its_own_content() -> None:
    for problem in step_tab_width_problems(source(LAYOUT_CSS)):
        check(False, problem)


def test_the_step_tab_width_check_fires() -> None:
    css = source(LAYOUT_CSS)
    seeded = css.replace("flex: 1 1 0%; min-width: 0;", "flex: 1 1 auto; min-width: 0;", 1)
    check(seeded != css, "the probe for an auto flex-basis did not take")
    check(bool(step_tab_width_problems(seeded)), "the step-tab width check does not fire on an auto flex-basis")


# --------------------------------------------------------------------------
# the Base document row painted over by the text box above it
# --------------------------------------------------------------------------

DOC_PANE_RULES = ("#step-documents .doc-panes",
                  "#step-documents .doc-pane:not([hidden])",
                  "#step-documents .doc-pane > .field:has(> .doc-text)")


def doc_pane_overflow_problems(css: str) -> list[str]:
    """None of the containers between the documents pane and its text box may
    declare `min-height: 0`: the text box itself has the one real floor
    in that chain, `min-height: 5.5rem`, a few lines below. A `min-height: 0`
    on a container above it lets the flex algorithm size that container
    smaller than the floor without the text box agreeing to follow, and the
    text box then paints past its own container's bottom edge, over the Base
    document row that comes after it in the flow, measured in a real browser
    at 1366x768 in German, where the row read as overlapping the box above it
    rather than being pushed down by it.
    """
    found = []
    for selector in DOC_PANE_RULES:
        rule = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css, flags=re.S)
        if not rule:
            found.append(f"no {selector!r} rule in layout.css")
            continue
        if re.search(r"min-height:\s*0\b", rule.group(1)):
            found.append(f"{selector!r} carries min-height: 0 again; its text "
                        f"box can now paint past it and over the row that follows")
    return found


def test_nothing_between_the_documents_pane_and_its_text_box_can_shrink_under_it() -> None:
    for problem in doc_pane_overflow_problems(source(LAYOUT_CSS)):
        check(False, problem)


def test_the_doc_pane_overflow_check_fires() -> None:
    css = source(LAYOUT_CSS)
    for selector in DOC_PANE_RULES:
        seeded = re.sub(re.escape(selector) + r"\s*\{\s*flex:\s*1 1 auto;",
                        selector + " { flex: 1 1 auto; min-height: 0;", css, count=1)
        check(seeded != css, f"the probe for {selector!r} did not take")
        check(bool(doc_pane_overflow_problems(seeded)),
              f"the doc-pane overflow check does not fire on {selector!r} regaining min-height: 0")


def test_every_finding_section_is_a_tab_with_its_chip() -> None:
    for problem in finding_problems(source(INDEX)):
        check(False, problem)


def test_the_finding_check_fires() -> None:
    html = source(INDEX)
    seeds = {
        "a chip moved out of its tab": html.replace(
            '        <span class="chip" data-cc="omitted-chip"></span>\n', "", 1)
            .replace('<div class="section-body" data-cc="omitted"></div>',
                     '<span class="chip" data-cc="omitted-chip"></span><div class="section-body" data-cc="omitted"></div>', 1),
        "a hidden section with a shown tab": html.replace(
            'id="finding-tab-numbers" aria-controls="finding-numbers"\n              aria-selected="false" tabindex="-1" hidden>',
            'id="finding-tab-numbers" aria-controls="finding-numbers"\n              aria-selected="false" tabindex="-1">', 1),
    }
    for what, seeded in seeds.items():
        check(seeded != html, f"the probe for {what} did not take")
        check(bool(finding_problems(seeded)), f"the finding check does not fire on {what}")


def test_a_blocked_run_leads_to_its_step() -> None:
    for problem in script_problems(source(APP_JS)):
        check(False, problem)


def test_the_blocked_run_check_fires() -> None:
    js = source(APP_JS)
    seeds = {
        "a document reason with no step": js.replace(
            'return { ready: false, step: "documents", text: t("status.needdocs"',
            'return { ready: false, text: t("status.needdocs"', 1),
        "the goto never rendered": js.replace(
            "  setText(el(\"submit-label\"), submitLabel());\n  renderStepGoto(state);",
            "  setText(el(\"submit-label\"), submitLabel());", 1),
        "no pointer on the disabled Run": js.replace(
            'el("run-card").addEventListener("pointerup"', 'el("run-card").addEventListener("pointerdown"', 1),
        "a step reason defaulting nowhere": js.replace(
            'return String(state.step || "model");', 'return String(state.step || "");', 1),
        "storage outside a try": js.replace(
            '  try {\n    window.localStorage.setItem(STEP_KEY, chosen);\n  } catch (_) {\n    // No storage: the step holds for this page only.\n  }',
            '  window.localStorage.setItem(STEP_KEY, chosen);', 1),
    }
    for what, seeded in seeds.items():
        check(seeded != js, f"the probe for {what} did not take")
        check(bool(script_problems(seeded)), f"the blocked-run check does not fire on {what}")


def test_the_way_to_the_blocking_step_under_node() -> None:
    """The shipped script, in both languages, under the fake DOM."""
    tables = static.catalogues()
    driven = drive_goto(source(APP_JS))
    if driven is None:
        print("note: UNMEASURED: no node here, so the goto drive did not run")
        return
    for problem in goto_problems(driven, tables):
        check(False, problem)
    # Must-fire: a script that never shows the button is caught.
    seeded = source(APP_JS).replace("  go.hidden = !step;", "  go.hidden = true;", 1)
    check(bool(goto_problems(drive_goto(seeded), tables)),
          "the goto drive does not fire on a button that never shows")


def test_a_finished_run_never_shows_the_reconnecting_status() -> None:
    """`EventSource` reports the server's own end-of-stream close as an
    error, same as a real drop. `onStreamError` must poll before it says
    anything, and never flash "reconnecting" once the run is over, however
    it ended: only a run genuinely still going, with the stream not already
    back open, is a real reconnect."""
    js = source(APP_JS)
    driven = drive_stream_error(js)
    if driven is None:
        print("note: UNMEASURED: no node here, so the stream-error drive did not run")
        return
    for problem in stream_error_problems(driven):
        check(False, problem)


def test_the_reconnecting_check_fires() -> None:
    """Must fire: the earlier logic, which judged `store.runId`/`store.report`
    on the spot instead of polling first, flashes the status at the end of
    every run again."""
    js = source(APP_JS)
    seeded = js.replace(
        "  await poll(id);\n"
        "  if (store.stream === stream && store.runId === id && !store.report\n"
        "      && stream.readyState !== EventSource.OPEN) {\n",
        "  if (store.runId && !store.report) {\n", 1)
    check(seeded != js, "the probe for the pre-fix onerror logic did not take")
    check(bool(stream_error_problems(drive_stream_error(seeded))),
          "the stream-error check does not fire on the pre-fix logic")


def test_the_layout_uses_theme_tokens_only() -> None:
    """Every colour in layout.css is a token, so the theme's contrast table
    covers what it paints."""
    css = re.sub(r"/\*.*?\*/", "", source(LAYOUT_CSS), flags=re.S)
    literal = re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", css)
    check(not literal, f"layout.css paints literal colours: {literal}")
    seeded = css + "\n.x { color: #ff0000; }\n"
    check(bool(re.findall(r"#[0-9a-fA-F]{3,8}\b", seeded)), "the literal-colour scan does not fire")
    html = source(INDEX)
    theme = html.index('<link rel="stylesheet" href="theme.css">')
    layout = html.find('<link rel="stylesheet" href="layout.css">')
    check(layout > theme, "layout.css is not linked after theme.css")


# --------------------------------------------------------------------------
# the second pass: divider, help icons, effort on Settings, Compare
# levels, the language globe
# --------------------------------------------------------------------------

def divider_problems(html: str, js: str) -> list[str]:
    """The pane divider is a focusable separator with a value, wired for keys,
    a double-click reset and a guarded stored width."""
    nodes = parse(html)
    found = []
    divider = hook(nodes, "pane-divider")
    if divider is None:
        return ["there is no single pane-divider"]
    a = divider["attrs"]
    for name, want in (("role", "separator"), ("tabindex", "0"), ("aria-orientation", "vertical")):
        if a.get(name) != want:
            found.append(f"the divider's {name} is {a.get(name)!r}, not {want!r}")
    for name in ("aria-valuenow", "aria-valuemin", "aria-valuemax", "aria-labelledby"):
        if not a.get(name):
            found.append(f"the divider has no {name}")
    ids = by_id(nodes)
    if a.get("aria-labelledby") not in ids:
        found.append("the divider's label is missing")
    wired = static.body_of(static.strip_comments(js), "function wireDivider()")
    for key in ("ArrowLeft", "ArrowRight", "Home", "End"):
        if f'"{key}"' not in wired:
            found.append(f"the divider does not answer {key}")
    if '"dblclick"' not in wired or "setSplit(SPLIT.start, true)" not in wired:
        found.append("a double-click does not reset the divider")
    body = static.body_of(static.strip_comments(js), "function setSplit(")
    if 'divider.setAttribute("aria-valuenow"' not in body:
        found.append("the divider's aria-valuenow does not follow its position")
    for name in ("function setSplit(", "function storedSplit("):
        text = static.body_of(static.strip_comments(js), name)
        for use in re.finditer(r"localStorage", text):
            before = text[:use.start()]
            if before.count("try {") <= before.count("} catch"):
                found.append(f"{name.split()[1][:-1]} touches localStorage outside a try")
    return found


def help_problems(html: str) -> list[str]:
    """Every static "?" is a button, named for a screen reader, described by
    the tooltip in its own box."""
    nodes = parse(html)
    ids = by_id(nodes)
    found = []
    icons = [n for n in nodes if "help-icon" in n["attrs"].get("class", "").split()]
    if len(icons) < 6:
        found.append(f"only {len(icons)} help icons in the page")
    for icon in icons:
        a = icon["attrs"]
        if icon["tag"] != "button" or a.get("type") != "button":
            found.append("a help icon is not a <button type=button>")
        target = ids.get(a.get("aria-describedby", ""))
        box = icon["parents"][-1] if icon["parents"] else None
        if target is None or box is None or not any(p is box for p in target["parents"]):
            found.append(f"help icon {a.get('aria-describedby')} is not described by a text in its own box")
        name = [x for x in nodes if x["attrs"].get("data-t") == "help.more" and any(p is icon for p in x["parents"])]
        if not name:
            found.append(f"help icon {a.get('aria-describedby')} has no name")
    return found


def settings_problems(html: str, js: str) -> list[str]:
    """Effort is the first item of the Settings step, and the Settings tab
    carries a "new" marker that `renderStepStates` shows when it appears."""
    nodes = parse(html)
    ids = by_id(nodes)
    found = []
    effort = hook(nodes, "effort-block")
    panel = ids.get("step-settings")
    if effort is None or panel is None or not any(p is panel for p in effort["parents"]):
        found.append("the effort slider is not on the Settings step")
    else:
        grid = effort["parents"][-1]
        first = [n for n in nodes if n["parents"] and n["parents"][-1] is grid]
        if not first or first[0] is not effort:
            found.append("the effort slider is not the Settings step's first item")
    marker = hook(nodes, "step-new-settings")
    tab = ids.get("step-tab-settings")
    if marker is None or tab is None or not any(p is tab for p in marker["parents"]) or "hidden" not in marker["attrs"]:
        found.append("the Settings tab has no hidden \"new\" marker")
    states = static.body_of(static.strip_comments(js), "function renderStepStates()")
    if 'el("step-new-settings").hidden = !effortShown || layout.effortSeen;' not in states:
        found.append("renderStepStates does not show the marker while effort is new")
    go = static.body_of(static.strip_comments(js), "function goToStep(")
    if "layout.effortSeen = true;" not in go:
        found.append("opening the Settings step does not clear the marker")
    return found


def compare_problems(html: str, js: str, tables: dict[str, dict[str, str]]) -> list[str]:
    """The Compare levels dialog: opened from beside the slider, labelled as
    an illustration in both languages, a sample and a short line per level.

    711: the level's summary/buys/costs is an inline `<details>` disclosure,
    not `helpBox`'s hover popup. `.compare-panel` is a tall, multi-paragraph
    block inside a `<dialog>`, so a popup absolutely positioned inside it
    opened far below the "?" that opened it and was clipped by the dialog's
    edge, overlapping the dialog's own buttons ("the dialog gets garbled
    up"). Also 711: "See examples" and "Model scorecard" share one button
    class (`open-detail-btn`) rather than being sized by two separate rules
    that can drift apart.
    """
    from llossless import config
    nodes = parse(html)
    found = []
    for name in ("compare-dialog", "open-compare", "compare-tabs", "compare-panels", "close-compare", "compare-use"):
        if hook(nodes, name) is None:
            found.append(f"there is no single {name}")
    if 'data-t="compare.illustration"' not in html:
        found.append("the dialog does not say it is an illustration")
    render = static.body_of(static.strip_comments(js), "function renderCompare()")
    for key in ('t("brief.sample." + value)', 't("brief.level." + value)', 't("brief.change." + value)',
                't("fidelity." + value + "." + part)', 'markedSample(t("brief.sample." + value))'):
        if key not in render:
            found.append(f"renderCompare does not render {key}")
    if "helpBox(" in render:
        found.append("renderCompare opens the level detail with helpBox again (a hover popup)")
    if 'createElement("details")' not in render:
        found.append("renderCompare does not build a <details> disclosure for the level detail")
    for tag, strings in sorted(tables.items()):
        if not strings.get("compare.illustration", "").strip():
            found.append(f"{tag}.json has no illustration label")
        for level in config.FIDELITY_LEVELS:
            for key in (f"brief.level.{level}", f"brief.sample.{level}", f"brief.change.{level}"):
                if not strings.get(key, "").strip():
                    found.append(f"{tag}.json has no {key}")
    for name in ("open-compare", "open-scorecard"):
        button = hook(nodes, name)
        if button is None:
            continue
        classes = button["attrs"].get("class", "").split()
        if "open-detail-btn" not in classes:
            found.append(f"{name} does not carry the shared open-detail-btn class")
    return found


def language_problems(html: str, tables: dict[str, dict[str, str]]) -> list[str]:
    """The language picker is a globe with a bilingual name, no word."""
    start = html.index('data-cc="locale-field"')
    field = html[start:html.index("</div>", start)]
    found = []
    if "<svg" not in field:
        found.append("the language picker has no globe")
    if "data-t=" in field or "<label" in field:
        found.append("the language picker still shows a word")
    if 'aria-label="Language / Sprache"' not in field:
        found.append("the language picker has no bilingual name")
    for tag, strings in sorted(tables.items()):
        if "locale.label" in strings:
            found.append(f"{tag}.json still has locale.label")
    return found


def test_the_second_pass_holds() -> None:
    html, js, tables = source(INDEX), source(APP_JS), static.catalogues()
    for problem in (divider_problems(html, js) + help_problems(html) + settings_problems(html, js)
                    + compare_problems(html, js, tables) + language_problems(html, tables)):
        check(False, problem)


def test_the_second_pass_checks_fire() -> None:
    html, js, tables = source(INDEX), source(APP_JS), static.catalogues()
    seeds = [
        ("a divider with no value", lambda: divider_problems(html.replace(' aria-valuenow="60"', "", 1), js)),
        ("a divider that ignores End", lambda: divider_problems(html, js.replace(': key === "End" ? SPLIT.max', ': key === "Endless" ? SPLIT.max', 1))),
        ("a help icon described from outside its box", lambda: help_problems(html.replace(
            'aria-describedby="help-base"', 'aria-describedby="help-title"', 1))),
        ("a help icon with no name", lambda: help_problems(html.replace(
            '<button type="button" class="help-icon" aria-describedby="help-base"><span aria-hidden="true">?</span><span class="visually-hidden" data-t="help.more">More about this</span></button>',
            '<button type="button" class="help-icon" aria-describedby="help-base"><span aria-hidden="true">?</span></button>', 1))),
        ("effort back on the Model step", lambda: settings_problems(html.replace(
            '      <div class="field effort-block" data-cc="effort-block" hidden>', '      <div class="field effort-block" data-cc="effort-block-moved" hidden>', 1), js)),
        ("a marker that never shows", lambda: settings_problems(html, js.replace(
            'el("step-new-settings").hidden = !effortShown || layout.effortSeen;', 'el("step-new-settings").hidden = true;', 1))),
        ("an illustration that does not say so", lambda: compare_problems(html.replace('data-t="compare.illustration"', 'data-t="compare.note"', 1), js, tables)),
        ("the level detail back on a hover popup", lambda: compare_problems(
            html, js.replace('disclosure.appendChild(summary);', 'disclosure.appendChild(summary); helpBox(summary);', 1), tables)),
        ("the examples button split back onto its own class", lambda: compare_problems(
            html.replace('class="ghost open-detail-btn" data-cc="open-compare"',
                         'class="ghost compare-open" data-cc="open-compare"', 1), js, tables)),
        ("the word back on the language picker", lambda: language_problems(html.replace(
            '<svg class="locale-icon"', '<label for="locale-select" data-t="locale.label">Language</label><svg class="locale-icon"', 1), tables)),
    ]
    for what, run in seeds:
        check(bool(run()), f"the second-pass check does not fire on {what}")


# --------------------------------------------------------------------------
# the examples follow their levels' rules
# --------------------------------------------------------------------------

def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def sample_problems(strings: dict[str, str]) -> list[str]:
    """The English examples against `prompts/fidelity/<level>.merge.md`: the
    verbatim classes (numbers, units) copied at every level, `off` made only
    of source sentences, `low` the same sentences with the typo fixed, the
    wrong year corrected only from `open` up, and no conflicting fact."""
    raw_strings = strings
    strings = {key: (value.replace("[[", "").replace("]]", "") if key.startswith("brief.sample.") else value)
               for key, value in strings.items()}
    a, b = strings.get("compare.source.a", ""), strings.get("compare.source.b", "")
    found = []
    source_sentences = set(sentences(a)) | set(sentences(b))
    if set(re.findall(r"\d+ metres", a)) != set(re.findall(r"\d+ metres", b)):
        found.append("the two sources disagree about a fact the dialog is not about")
    off = strings.get("brief.sample.off", "")
    for sentence in sentences(off):
        if sentence not in source_sentences:
            found.append(f"off writes a sentence no source has: {sentence!r}")
    low = strings.get("brief.sample.low", "")
    if len(sentences(low)) != len(sentences(off)) or low.replace("opened", "opend") != off:
        found.append("low changes more than the typo")
    for level in ("off", "low", "mid", "high", "open", "sourced"):
        text = strings.get(f"brief.sample.{level}", "")
        raw = raw_strings.get(f"brief.sample.{level}", "")
        if level != "off" and "[[" not in raw:
            found.append(f"{level} marks nothing it changed")
        if raw.count("[[") != raw.count("]]"):
            found.append(f"{level}'s marks are unbalanced")
        for verbatim in ("330 metres", "674"):
            if verbatim not in text:
                found.append(f"{level} does not copy {verbatim!r} as written")
        year = "1889" if level in ("open", "sourced") else "1899"
        if year not in text or ("1889" if year == "1899" else "1899") in text:
            found.append(f"{level} carries the wrong year for its level")
        if level != "off" and "opend" in text:
            found.append(f"{level} keeps the typo")
    return found


def test_the_examples_follow_their_levels() -> None:
    strings = static.catalogues()["en"]
    for problem in sample_problems(strings):
        check(False, problem)
    seeds = {
        "a unit reworded": dict(strings, **{"brief.sample.high": strings["brief.sample.high"].replace("330 metres", "330-metre")}),
        "a year corrected too early": dict(strings, **{"brief.sample.high": strings["brief.sample.high"].replace("1899", "1889")}),
        "off rewording": dict(strings, **{"brief.sample.off": strings["brief.sample.off"].replace("stands in", "is in")}),
    }
    for what, seeded in seeds.items():
        check(bool(sample_problems(seeded)), f"the example check does not fire on {what}")


# --------------------------------------------------------------------------
# the effort baseline
# --------------------------------------------------------------------------

BASELINE_DRIVE = r"""
;(() => {
  if (!El.prototype.addEventListener) El.prototype.addEventListener = function () {};
  strings = INPUT.strings;
  locale.tag = "en";
  store.config = INPUT.config;
  store.fidelity = "high";
  store.docs = [{ name: "a.md", text: "A.", id: "a" }, { name: "b.md", text: "B.", id: "b" }];
  const out = {};
  for (const id of INPUT.routes) {
    store.mergeModel = COMMAND_PREFIX + id;
    store.checkModel = store.mergeModel;
    renderEffort();
    out[id] = { hidden: Boolean(hooks["effort-baseline"].hidden),
                text: hooks["effort-baseline-text"].textContent,
                detail: hooks["effort-baseline-detail"].textContent };
  }
  process.stdout.write(JSON.stringify(out));
})();
"""


def expected_baseline(payload: dict) -> dict[str, str | None]:
    """The operator's rule, formed here from the catalogue, per route."""
    entries = payload["catalogue"]["command_routes"]
    out = {}
    for route in payload["commands"]["routes"]:
        levels = ((route.get("effort") or {}).get("levels")) or []
        entry = next((e for e in entries if e["route"] == route["id"] and e["model"] == route.get("model")
                      and e["profile"] == route.get("profile")), None)
        answer = None
        if entry and len(levels) >= 2:
            now = (entry.get("alias_now") or {}).get("model") or entry.get("resolved_model")
            for block in [entry.get("measured_by_effort")] + list(entry.get("pinned_by_effort") or []):
                if not block or block.get("safe_mode") is not True or block.get("resolved_model") != now:
                    continue
                measured = [lv for lv in levels if lv in (block.get("levels") or {})]
                if len(measured) < 2 or measured[0] != levels[0]:
                    continue
                pairs = [p for p in block["levels"][measured[0]]["pairs"]
                         if all(p in block["levels"][lv]["pairs"] for lv in measured)]
                if not pairs:
                    continue
                total = lambda lv, f: sum(block["levels"][lv]["pairs"][p]["fixed"][f] for p in pairs)
                best = max(measured, key=lambda lv: (total(lv, "median"), -measured.index(lv)))
                lowest = next((lv for lv in measured
                               if total(best, "min") <= total(lv, "median") <= total(best, "max")), None)
                if lowest and lowest != measured[-1]:
                    answer = lowest
                    break
        out[route["id"]] = answer
    return out


def drive_baseline(js: str, payload: dict) -> dict | None:
    node = static.node_command()
    if node is None:
        return None
    routes = [row["id"] for row in payload["commands"]["routes"]]
    program = (static.EFFORT_DOM + "\nconst INPUT = " + json.dumps(
        {"strings": static.catalogues()["en"], "config": payload, "routes": routes})
        + ";\n" + js + BASELINE_DRIVE)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
        handle.write(program)
        path = handle.name
    try:
        run = subprocess.run(node + [path], capture_output=True, text=True, timeout=120, cwd=ROOT)
    finally:
        os.unlink(path)
    if run.returncode != 0:
        return {"error": run.stderr[-600:]}
    return json.loads(run.stdout)


def baseline_problems(driven: dict | None, payload: dict) -> list[str]:
    if driven is None:
        return []
    if "error" in driven:
        return [f"the baseline drive did not run under node: {driven['error']}"]
    strings = static.catalogues()["en"]
    found = []
    for route, level in expected_baseline(payload).items():
        got = driven.get(route) or {}
        if level is None:
            if not got.get("hidden") or got.get("text"):
                found.append(f"{route}: a baseline shows where none may: {got}")
            continue
        want = strings["effort.baseline"].replace("{level}", strings.get(f"effort.level.{level}", level))
        if got.get("hidden") or got.get("text") != want or not got.get("detail"):
            found.append(f"{route}: the baseline reads {got}, not {want!r}")
    return found


def with_block(payload: dict, route: str, change) -> dict:
    copy = json.loads(json.dumps(payload))
    for entry in copy["catalogue"]["command_routes"]:
        if entry["route"] == route:
            change(entry)
    return copy


def test_the_effort_baseline_is_computed_and_only_for_the_current_model() -> None:
    """Formed from the catalogue at render time; hidden unless the block
    measured what the route runs now (model and safe mode) and covers the
    slider from its lowest level."""
    js = source(APP_JS)
    payload = static.served_config_with_routes()
    real = expected_baseline(payload)
    check(all(level is None for level in real.values()),
          f"the shipped catalogue now supports a baseline somewhere: {real}; "
          f"the operator ruled none for Opus 5.5, Sonnet and Haiku as measured")
    driven = drive_baseline(js, payload)
    if driven is None:
        print("note: UNMEASURED: no node here, so the baseline drive did not run")
        return
    for problem in baseline_problems(driven, payload):
        check(False, problem)

    def safe(entry):
        entry["measured_by_effort"]["safe_mode"] = True
    positive = with_block(payload, "claude-sonnet", safe)
    want = expected_baseline(positive)["claude-sonnet"]
    check(want is not None, "the positive seed does not support a baseline; the probe is vacuous")
    shown = drive_baseline(js, positive)
    for problem in baseline_problems(shown, positive):
        check(False, f"positive seed: {problem}")
    check(not (shown or {}).get("claude-sonnet", {}).get("hidden", True),
          "a current, safe-mode block with every level shows no baseline (must-not-fire)")

    def lower(entry):
        safe(entry)
        cell = entry["measured_by_effort"]["levels"][want]["pairs"]["voyager"]["fixed"]
        cell["median"] = cell["min"] = 0
    moved = with_block(payload, "claude-sonnet", lower)
    after = expected_baseline(moved)["claude-sonnet"]
    check(after != want, "the median seed did not move the expected level")
    driven_moved = drive_baseline(js, moved)
    for problem in baseline_problems(driven_moved, moved):
        check(False, f"median seed: {problem}")
    check((driven_moved or {}).get("claude-sonnet", {}).get("text") != (shown or {}).get("claude-sonnet", {}).get("text"),
          "changing a median in the catalogue does not change the line")

    def other_model(entry):
        safe(entry)
        entry["measured_by_effort"]["resolved_model"] = "claude-sonnet-4"
    mismatch = with_block(payload, "claude-sonnet", other_model)
    check(expected_baseline(mismatch)["claude-sonnet"] is None, "the mismatch seed still expects a line")
    hidden = drive_baseline(js, mismatch)
    check((hidden or {}).get("claude-sonnet", {}).get("hidden") is True,
          "a block measured on another model shows a baseline (must-fire)")

    # The Opus route's grid measured Opus 5 and was removed from the
    # card; a block measured on another model is the Sonnet seed above.
    opus_entry = next(e for e in payload["catalogue"]["command_routes"]
                      if e["route"] == "claude-opus")
    check(opus_entry.get("measured_by_effort") is None,
          "the Opus route carries an effort grid again; 708 removed Opus 5's")
    check((driven or {}).get("claude-opus", {}).get("hidden", True) is True,
          "the Opus route shows a baseline with no grid to form it from")

    seeded = js.replace('|| String(block.resolved_model || "") !== current) return null;', ") return null;", 1)
    check(seeded != js, "the model-match probe's anchor has moved")
    check(bool(baseline_problems(drive_baseline(seeded, mismatch), mismatch)),
          "a baseline that ignores the model is not caught")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_layout" and callable(function):
            function()
    failures.extend(f for f in static.failures if f not in failures)
    if failures:
        print(f"web layout: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"web layout: {checks} checks pass over {len(TABLISTS)} tablists, "
          f"{len(STEPS)} steps and {len(FINDINGS)} finding tabs")
    return 0


def stop_word_problems(css: str, js: str) -> list[str]:
    """Each stop word is placed on the thumb's line, not spread over the track.

    What a source read can hold. The measurement, every word within 2 px of
    its thumb at 1280/1024/800/380, English and German, both sliders, is a
    separate browser harness's, because only
    a browser knows where its thumb is.
    """
    found = []
    flat = " ".join(css.split())
    if "left: calc(var(--range-thumb) / 2 + (100% - var(--range-thumb)) * var(--at, 0))" not in flat:
        found.append("a stop word is not placed at half a thumb plus its share of the track less a thumb")
    if not re.search(r"\.range-legend\s*\{[^}]*position:\s*relative", css):
        found.append("the stop words are not positioned against their legend")
    for renderer in ("renderFidelity", "renderEffortCard"):
        body = js.split(f"function {renderer}(", 1)[-1].split("\n}\n", 1)[0]
        if 'span.style.setProperty("--at"' not in body:
            found.append(f"{renderer} does not tell each stop word where its stop is")
    for hook in ("effort-slider", "fidelity-range"):
        if f'input[type="range"][data-cc="{hook}"]' not in css:
            found.append(f"the {hook} slider is not inset with its words")
    return found


def test_the_stop_words_sit_under_their_thumbs() -> None:
    css, js = source(LAYOUT_CSS), source(APP_JS)
    for problem in stop_word_problems(css, js):
        check(False, problem)
    # Must fire: the words spread over the whole track again (the defect), and
    # one renderer that stops saying where its stops are.
    seeded = css.replace("left: calc(var(--range-thumb) / 2 + (100% - var(--range-thumb)) * var(--at, 0));",
                         "left: calc(100% * var(--at, 0));")
    check(seeded != css and bool(stop_word_problems(seeded, js)),
          "a word placed across the whole track is not caught")
    seeded = js.replace('    // Under its thumb position, as the fidelity words are.\n'
                        '    span.style.setProperty("--at", String(levels.length > 1 ? position / (levels.length - 1) : 0));\n', "")
    check(seeded != js and bool(stop_word_problems(css, seeded)),
          "an effort legend with no stop positions is not caught")


def test_web_layout() -> None:
    """pytest entry point."""
    assert main() == 0, "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
