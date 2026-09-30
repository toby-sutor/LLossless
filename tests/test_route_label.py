#!/usr/bin/env python3
"""A command route named after the model its alias answers as now.

The `opus` subscription route's alias answers as Claude Opus 5.5
(`alias_now`), and its figures are measured on that same model. An
earlier scenario measured its figures on Claude Opus 5 instead, now
retired: the operator ruled Opus 5 is not Opus 5.5 and no longer
credible as a stand-in, so opus's own `measured` moved to the
release benchmark's Opus 5.5 figures, its `resolved_model` caught up
with its alias, and `alias_now` came out with it (the schema forbids
the two agreeing). No shipped route carries `alias_now` any more, so
this file drives the three properties below against a fabricated
`alias_now` built on `claude-sonnet` instead, a synthetic construction
kept safe alongside an app.js fix for the effort card's current/pinned
split, which used to read `alias_now` alone rather than comparing a
grid's own `resolved_model` to the route's. One real assertion against
the shipped card stays: no route reads as measured on another model.
Each property is driven under node over the shipped `app.js`, with a
seeded breakage beside it:

**the name follows `alias_now`.** An unserved route row is named after the
catalogue's own `models` row for `alias_now.model` plus the route's suffix,
"Claude Opus 5.5 (subscription)" in both languages, as the stored names read;
a served row keeps its label and says "runs Claude Opus 5.5". Changing only
`alias_now.model` changes both; the stored `display_name` stays as history.

**the mark.** A route whose `resolved_model` differs from `alias_now.model`
carries "measured on <model>", explained on hover and by `aria-describedby`
pointing at its own hidden sentence. Must-fire: the fabricated route.
Must-not-fire: every other route, real or fabricated, whose alias has not
moved.

**the ranking.** On every figure sort, in both directions, such a row sorts
after every live row with a figure of its own and before every row with none;
retired rows stay last.

Run with `python3 tests/test_route_label.py`, or collect with pytest.
"""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Reads files and runs node over them; opens nothing. Installed in the shape
# `tests/test_socket_guard.py` scans every module for.
socket_guard.install()

from test_web_static import (APP_JS, EFFORT_DOM, INDEX, catalogues,  # noqa: E402
                             node_command, source)

CATALOGUE = ROOT / "src" / "llossless" / "web" / "catalogue.json"
# The suffix is the stored names' own, in both languages: every catalogue
# route name is English data, untranslated, and a derived one in German that
# alone said "(Abonnement)" would stand out among its neighbours.
SUFFIX = {"en": "(subscription)", "de": "(subscription)"}

failures: list[str] = []
unmeasured: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def decline(message: str) -> None:
    unmeasured.append(message)


# Two served routes, as `/config` reports discovered ones: the Opus alias,
# which moved, and the Sonnet alias, which did not.
SERVED = [
    {"id": "claude-opus", "model": "opus", "profile": "subscription",
     "label": "Claude Code - Opus", "comparable": False, "retrieval": [],
     "cost": "plan", "window": 200000},
    {"id": "claude-sonnet", "model": "sonnet", "profile": "subscription",
     "label": "Claude Code - Sonnet", "comparable": False, "retrieval": [],
     "cost": "plan", "window": 200000},
]

DRIVE = r"""
;(() => {
  const out = {};
  for (const [lang, table] of Object.entries(INPUT.strings)) {
    strings = table;
    locale.tag = lang;
    for (const [name, catalogue] of Object.entries(INPUT.catalogues)) {
      for (const [served, routes] of Object.entries({ unserved: [], served: INPUT.served })) {
        store.config = { commands: { routes, per_user: false }, catalogue };
        const rows = scorecardRows();
        const at = { names: {}, marks: {}, described: {}, other: [], orders: {} };
        for (const row of rows) {
          at.names[row.id] = String(row.display_name || row.id);
          if (!routeOf(row)) continue;
          const marks = routeMarks(row);
          at.marks[row.id] = marks.map((m) => m.text);
          const line = markLine(marks, "incomparable-why-picker");
          at.described[row.id] = line.childNodes.filter((n) => n.getAttribute("aria-describedby"))
            .map((n) => [n.textContent, n.getAttribute("aria-describedby"), n.title || ""]);
          if (measuredOnOtherModel(row)) at.other.push(row.id);
        }
        for (const key of ["loss", "deviations", "speed"]) {
          for (const direction of ["ascending", "descending"]) {
            at.orders[key + " " + direction] = scorecardOrder(rows, key, direction).map((m) => m.id);
          }
        }
        out[[lang, name, served].join(" ")] = at;
      }
    }
  }
  process.stdout.write(JSON.stringify(out));
})();
"""


def variants() -> dict[str, dict]:
    """The shipped catalogue, unedited, plus a fabricated `alias_now` on
    `claude-sonnet` and three edits of it alone.

    No shipped route carries `alias_now` any more (opus's own
    `resolved_model` caught up with its alias), so "the name/mark/ranking
    follow `alias_now`" is driven from a fabricated one instead, built on
    `claude-sonnet`, an arbitrary real route with its own `measured` and
    `measured_by_effort` blocks already in place. `shipped` stays the real
    file, for the one assertion that still reads it directly: nothing on the
    real card should be marked as measured on another model.
    """
    shipped = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    base = copy.deepcopy(shipped)
    sonnet = next(e for e in base["command_routes"] if e["route"] == "claude-sonnet")
    sonnet["alias_now"] = {"model": "claude-opus-5-5", "checked_on": "2026-09-26",
                           "cli_version": "2.1.283"}
    moved = copy.deepcopy(base)
    moved["models"].append({"id": "claude-opus-6", "api_model": "claude-opus-6",
                            "display_name": "Claude Opus 6", "provider": "anthropic",
                            "profile": "anthropic", "context_window": 200000,
                            "measured": None})
    unlisted = copy.deepcopy(base)
    none = copy.deepcopy(base)
    for entry in moved["command_routes"]:
        if entry.get("alias_now"):
            entry["alias_now"]["model"] = "claude-opus-6"
    for entry in unlisted["command_routes"]:
        if entry.get("alias_now"):
            entry["alias_now"]["model"] = "claude-opus-7"
    for entry in none["command_routes"]:
        entry.pop("alias_now", None)
    return {"shipped": shipped, "base": base, "moved": moved, "unlisted": unlisted,
            "none": none}


def drive(js: str, cats: dict[str, dict]) -> dict | None:
    node = node_command()
    if node is None:
        return None
    tables = catalogues()
    program = (EFFORT_DOM + "\nconst INPUT = " + json.dumps(
        {"strings": {tag: tables[tag] for tag in ("en", "de")}, "catalogues": cats,
         "served": SERVED}) + ";\n" + js + DRIVE)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as handle:
        handle.write(program)
        path = handle.name
    try:
        run = subprocess.run(node + [path], capture_output=True, text=True,
                             timeout=120, cwd=ROOT)
    finally:
        os.unlink(path)
    if run.returncode != 0:
        return {"error": run.stderr[-800:]}
    return json.loads(run.stdout or "{}")


def model_name(cat: dict, model_id: str) -> str:
    row = next((m for m in cat["models"] if model_id in (m.get("id"), m.get("api_model"))), {})
    return row.get("display_name") or model_id


def moved(entry: dict) -> bool:
    now = (entry.get("alias_now") or {}).get("model")
    return bool(now and entry.get("resolved_model") and now != entry["resolved_model"]
                and entry.get("measured"))


def problems(driven: dict | None, cats: dict[str, dict]) -> list[str]:
    """Every way the drive breaks the three rules. Empty is pass."""
    if driven is None:
        return []
    if "error" in driven:
        return [f"the drive did not run under node: {driven['error']}"]
    tables = catalogues()
    found = []
    for lang in ("en", "de"):
        strings = tables[lang]
        for name, cat in cats.items():
            routes = cat["command_routes"]
            for served in ("unserved", "served"):
                at = driven[f"{lang} {name} {served}"]
                tag = f"{lang}/{name}/{served}"
                served_ids = {r["id"] for r in SERVED} if served == "served" else set()
                models = {m["id"]: m for m in cat["models"]}
                for entry in routes:
                    rid = ("command:" if entry["route"] in served_ids
                           else "catalogue-route:") + entry["route"]
                    now = (entry.get("alias_now") or {}).get("model")
                    # the name
                    if entry["route"] in served_ids:
                        want = next(r["label"] for r in SERVED if r["id"] == entry["route"])
                    elif now:
                        want = f"{model_name(cat, now)} {SUFFIX[lang]}"
                    else:
                        want = entry["display_name"]
                    if at["names"].get(rid) != want:
                        found.append(f"{tag}: {rid} is named {at['names'].get(rid)!r}, "
                                     f"not {want!r}")
                    marks = at["marks"].get(rid, [])
                    runs = strings["models.route.mark.runs"].replace(
                        "{model}", model_name(cat, now)) if now else None
                    has_runs = [m for m in marks if m == runs] if runs else []
                    if now and entry["route"] in served_ids and len(has_runs) != 1:
                        found.append(f"{tag}: served {rid} does not say {runs!r}: {marks}")
                    if now and entry["route"] not in served_ids and has_runs:
                        found.append(f"{tag}: unserved {rid} says {runs!r} beside its name")
                    # the mark
                    history = strings["models.route.mark.history.before_safe_mode"] \
                        if (entry.get("measured_by_effort") or {}).get("safe_mode") is False \
                        else strings["models.route.mark.history"]
                    history = history.replace(
                        "{model}", model_name(cat, entry.get("resolved_model") or ""))
                    fires = rid in at["other"]
                    if fires != moved(entry):
                        found.append(f"{tag}: {rid} measuredOnOtherModel is {fires}, "
                                     f"expected {moved(entry)}")
                    if moved(entry) != (history in marks):
                        found.append(f"{tag}: {rid} carries {marks}, the mark should "
                                     f"{'' if moved(entry) else 'not '}be there")
                    if moved(entry):
                        described = [d for d in at["described"].get(rid, []) if d[0] == history]
                        if not described or described[0][1] != "history-why-picker" \
                                or described[0][2] != strings["models.route.mark.history.why"]:
                            found.append(f"{tag}: {rid}'s mark is not explained: "
                                         f"{at['described'].get(rid)}")
                # the ranking
                figures = {}
                for rid in at["names"]:
                    if rid.startswith(("command:", "catalogue-route:")):
                        route_id = rid.split(":", 1)[1]
                        entry = next((r for r in routes if r["route"] == route_id), None)
                        measured = (entry or {}).get("measured") or {}
                        retired, other = False, bool(entry and moved(entry))
                    else:
                        row = models[rid]
                        measured = row.get("measured") or {}
                        retired, other = bool((row.get("retired") or {}).get("on")), False
                    figures[rid] = (measured, retired, other)
                first = {"loss": "silent_loss_per_pair", "deviations": "deviations_per_pair",
                         "speed": "seconds_per_merge"}
                for sort, order in at["orders"].items():
                    field = first[sort.split()[0]]

                    def rank(rid: str) -> int:
                        measured, retired, other = figures[rid]
                        if retired:
                            return 3
                        if not isinstance(measured.get(field), (int, float)):
                            return 2
                        return 1 if other else 0
                    ranks = [rank(rid) for rid in order]
                    if ranks != sorted(ranks):
                        found.append(f"{tag}: {sort} ranks {list(zip(order, ranks))}")
    return found


def test_the_route_is_named_marked_and_ranked_by_what_its_alias_runs_now() -> None:
    """Name, mark and ranking, both languages, four catalogues.

    Must-fire: the stored name kept, the "runs" mark dropped, the "measured
    on" mark dropped, the mark fired on every measured route, the ranking rule
    removed and the mark's own explanation unhooked are each caught.
    Must-not-fire: the shipped script.
    """
    cats = variants()
    js = source(APP_JS)
    driven = drive(js, cats)
    if driven is None:
        decline("UNMEASURED: no node here, so the route names and marks were not driven")
        return
    for problem in problems(driven, cats):
        check(False, problem)
    # The real shipped catalogue has no route measured on another
    # model any more, opus's own resolved_model caught up with its alias.
    really_shipped = driven["en shipped unserved"]
    check(really_shipped["other"] == [],
          f"the real shipped catalogue reads {really_shipped['other']} as measured on "
          f"another model; no route should carry alias_now any more")
    # The fabricated scenario (built on claude-sonnet, since no shipped route
    # carries alias_now) fires for sonnet alone; the name really moved.
    base = driven["en base unserved"]
    check(base["other"] == ["catalogue-route:claude-sonnet"],
          f"the routes measured on another model are {base['other']}, not sonnet alone")
    check(base["names"].get("catalogue-route:claude-sonnet") == "Claude Opus 5.5 (subscription)",
          f"the Sonnet route reads {base['names'].get('catalogue-route:claude-sonnet')!r}")
    check(driven["de base unserved"]["names"].get("catalogue-route:claude-sonnet")
          == "Claude Opus 5.5 (subscription)", "the German Sonnet route name is wrong")
    check(driven["en moved unserved"]["names"].get("catalogue-route:claude-sonnet")
          == "Claude Opus 6 (subscription)", "an alias_now edit alone did not rename the route")
    check(driven["en none unserved"]["names"].get("catalogue-route:claude-sonnet")
          == "Claude Sonnet 5 (subscription)", "without alias_now the stored name is not used")
    check("measured on Claude Sonnet 5, before safe mode"
          in driven["en base served"]["marks"].get("command:claude-sonnet", []),
          f"the served Sonnet row is not marked: {driven['en base served']['marks']}")
    stored = next(e for e in cats["base"]["command_routes"] if e["route"] == "claude-sonnet")
    check(stored["display_name"] == "Claude Sonnet 5 (subscription)",
          "the stored display_name, kept as history, was edited")
    seeds = {
        "the stored name kept":
            js.replace("display_name: routeNameNow(entry),",
                       "display_name: entry.display_name || entry.route,"),
        "no runs mark":
            js.replace('say(t("models.route.mark.runs",', 'void (t("models.route.mark.runs",'),
        "no measured-on mark":
            js.replace("  if (measuredOnOtherModel(model)) {", "  if (false) {"),
        "the mark on every measured route":
            js.replace("return Boolean(entry && entry.alias_now && entry.alias_now.model "
                       "&& entry.resolved_model\n    && entry.alias_now.model !== "
                       "entry.resolved_model && (model.measured || entry.measured));",
                       "return Boolean(entry && (model.measured || entry.measured));"),
        "ranked as current":
            js.replace("      if (other) return other;\n", ""),
        "the explanation unhooked":
            js.replace('describedBy.replace("incomparable-why", mark.hook)', "describedBy"),
    }
    for what, seeded in seeds.items():
        check(seeded != js, f"the seed {what!r} did not change the script")
        check(bool(problems(drive(seeded, cats), cats)), f"the check did not fire on {what}")


def test_the_marks_explanation_is_in_both_tables() -> None:
    """The hidden sentence the mark's `aria-describedby` points at, once per
    table, keyed to the catalogue string. Must-fire: one removed."""
    def missing(html: str) -> list[str]:
        return [where for where in ("picker", "scorecard")
                if f'id="history-why-{where}" data-t="models.route.mark.history.why" hidden'
                not in html]
    html = source(INDEX)
    check(not missing(html), f"no hidden explanation in {missing(html)}")
    seeded = html.replace('id="history-why-scorecard"', 'id="elsewhere"')
    check(seeded != html and bool(missing(seeded)), "a missing explanation is not caught")
    for tag, strings in catalogues().items():
        for key in ("models.route.mark.runs", "models.route.name",
                    "models.route.mark.history.why"):
            check(bool(strings.get(key)), f"{tag} has no {key}")


def main() -> int:
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
    for line in unmeasured:
        print(line)
    if failures:
        print(f"route label: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"route label: {checks} checks pass"
          + (f", {len(unmeasured)} declined" if unmeasured else ""))
    return 3 if unmeasured else 0


if __name__ == "__main__":
    sys.exit(main())
