#!/usr/bin/env python3
"""One self-contained HTML page per model, marking what each merge got wrong.

The request this answers: take the completed merges, put them in an HTML file
per model, and mark the failures so a reader can see the small details.

**Everything here is derived.** Every mark comes from a stored `report.json` --
its `structural.findings`, its claim-level `verdicts` -- or from the
reconciler's own `Located.verdict`, recomputed from the same sources and the
same merged document the run used. Nothing is hand-marked. A hand-annotated
page drifts from the record it illustrates and nobody finds out; this project
has already published prose that disagreed with its own numbers.

`--check` regenerates every page into a temporary directory and requires the
committed ones to match byte for byte. That is stronger than comparing finding
counts and it is the same defect class either way: an HTML page that disagrees
with the records is a stale figure in a new format.

**Two panes, because a dropped segment is not in the merge.** It cannot be
highlighted there, so the sources pane carries what happened to each source
segment and the merge pane carries what the merge added or contradicted.

**Marks are rendered per segment, never by character offset.** A document is
exactly the concatenation of its segments plus the notation between them
(`segment.py`), so emitting one block per segment cannot mis-attribute a mark
to its neighbour, which offset arithmetic across two panes very easily does.

**Colour is never the only encoding.** Every mark carries a symbol, a word, and
the segment or claim id it came from, so the page survives greyscale printing,
colourblind readers, and a reader who wants to trace a mark back to the record.

    tests/annotate_merges.py            # write the pages
    tests/annotate_merges.py --check    # refuse if they are stale
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

ARMS = ROOT / "arms" / "2026-08-30"
OUT = ROOT / "annotated"

# The five things a reader is being shown, each with a symbol and a word so the
# colour is decoration rather than information. `dropped` and `reworded` are
# what happened to a source segment; `unsupported` and `contradicted` are what
# the merge did with a claim; `altered` is an invariant-core token that changed,
# which is neither loss nor invention and is the one most easily missed.
CLASSES = {
    "dropped": ("&#9632;", "DROPPED", "in a source, not in the merge"),
    "reworded": ("&#9650;", "REWORDED", "in the merge in altered wording"),
    "altered": ("&#9670;", "ALTERED VALUE", "an invariant token did not survive unchanged"),
    "unsupported": ("&#9679;", "UNSUPPORTED", "in the merge, grounded in no source"),
    "contradicted": ("&#10006;", "CONTRADICTED", "the merge states something different"),
    # Not a failure, and marked so it cannot be mistaken for one. A segment the
    # merge left out *and said it left out* is the tool working. It is shown
    # because a reader asking what became of a source segment wants an answer
    # for every segment, and an unmarked one would read as "still here".
    "declared": ("&#9675;", "DECLARED", "left out, and the merge said so"),
    # The detection task's four outcomes, in the same vocabulary so one legend
    # serves the whole directory. Detection asks a different question -- did the
    # arm find the planted defect -- but the reader is the same reader, and a
    # second set of symbols would be a second thing to learn.
    "caught": ("&#10003;", "CAUGHT", "planted, and the arm reported it"),
    "missed": ("&#9633;", "MISSED", "planted, and the arm did not report it"),
    "invented": ("&#9678;", "INVENTED", "reported, and no probe accounts for it"),
    "unmeasured": ("&#8709;", "UNMEASURED", "no reading could be taken on this arm"),
}

# `structural.findings` kinds that belong to a source segment, and the class
# each becomes. Kinds not named here are reported in the header totals and not
# turned into a mark, so a kind added later is visible rather than swallowed.
SOURCE_KINDS = {
    "undeclared_absence": "dropped",
    "undeclared_rewording": "reworded",
    "verbatim_violation": "altered",
    "false_departure": "altered",
}


def merges() -> list[dict]:
    """Every stored merge, grouped by the model its own record names."""
    out = []
    for report in sorted(ARMS.rglob("report.json")):
        blob = json.loads(report.read_text(encoding="utf-8"))
        merged = report.parent / "merged.md"
        if not merged.is_file():
            continue
        provenance = blob.get("provenance") or {}
        model = (provenance.get("models") or {}).get("merge")
        if model is None:
            continue
        documents = {}
        for name, path in (blob.get("documents") or {}).items():
            if name == "merged.md":
                continue
            # The record stores an absolute path from the machine that ran it.
            # Resolved against the repository so this works on a clone.
            local = Path(path)
            if not local.is_file():
                local = ROOT / str(path).split("claimcheck/", 1)[-1]
            documents[name] = local
        if not documents or not all(p.is_file() for p in documents.values()):
            continue
        out.append({
            "model": model,
            "dir": report.parent,
            "label": str(report.parent.relative_to(ARMS)),
            "blob": blob,
            "merged": merged,
            "documents": documents,
            # A draw the project set aside. Shown, because it happened and the
            # archive keeps it, and labelled, because it is not a result.
            "discarded": "discarded" in str(report.parent).lower(),
        })
    return out


def annotate(entry: dict) -> dict:
    """Every mark for one merge, keyed by the segment it belongs to."""
    from llossless import reconcile, segment as segments

    sources = {n: p.read_text(encoding="utf-8") for n, p in entry["documents"].items()}
    merged_text = entry["merged"].read_text(encoding="utf-8")
    result = reconcile.reconcile(sources, merged_text)
    blob = entry["blob"]

    # Source side. The reconciler's own verdict first, then anything the record
    # says about that segment, so a mark is never invented here and never
    # silently disagrees with the stored finding.
    #
    # A segment can be absent because the merge dropped it silently, which is a
    # finding, or because the merge declared a departure, which is not. Both
    # are shown -- a reader asking what became of a segment wants an answer for
    # every one -- and they are never the same mark. Getting this wrong marked
    # two declared departures as failures on the first build of this file.
    declared = {str(r.get("segment")): str(r.get("disposition"))
                for r in blob.get("declarations") or []}
    source_marks: dict[str, list] = defaultdict(list)
    for coverage in result.coverages:
        for located in coverage.located:
            identifier = located.segment.id
            if located.verdict == reconcile.ABSENT:
                if identifier in declared:
                    source_marks[identifier].append(
                        ("declared", identifier, declared[identifier]))
                else:
                    source_marks[identifier].append(
                        ("dropped", identifier, "Located.verdict, no record"))
            elif located.verdict == reconcile.REWORDED:
                source_marks[identifier].append(
                    ("reworded", identifier,
                     f"Located.verdict, nearest {located.nearest or 'none'} "
                     f"at {located.ratio:.2f}"))
    unmarked = []
    for finding in (blob.get("structural") or {}).get("findings") or []:
        kind = finding.get("kind")
        identifier = str(finding.get("segment") or "")
        klass = SOURCE_KINDS.get(kind)
        if klass is None or not identifier:
            unmarked.append(kind)
            continue
        already = [m for m in source_marks[identifier] if m[0] == klass]
        if not already:
            source_marks[identifier].append((klass, identifier, kind))

    # Merge side. A claim carries the span it was drawn from, so a verdict is
    # attributed to the merge segment that contains that span -- containment,
    # not offsets.
    merge_segments = segments.segment_document(merged_text, reconcile.MERGE_LETTER).segments
    claims = {c["id"]: c for c in (blob.get("claims") or [])}
    merge_marks: dict[str, list] = defaultdict(list)
    loose = []
    for verdict in blob.get("verdicts") or []:
        label = verdict.get("verdict")
        if label in (None, "SUPPORTED", "NOT_GRADED"):
            continue
        forward = verdict.get("direction") == "source_to_merged"
        if forward and label != "CONTRADICTED":
            continue          # MISSING forward is a dropped source, already marked
        klass = "contradicted" if label == "CONTRADICTED" else "unsupported"
        claim = claims.get(verdict.get("claim_id"), {})
        span = reconcile.flatten(str(claim.get("span") or claim.get("text") or ""))
        home = next((s.id for s in merge_segments
                     if span and reconcile.occurs(span, reconcile.flatten(s.text))), None)
        detail = f"{verdict.get('claim_id')}, {label}"
        if home is None:
            loose.append((klass, verdict.get("claim_id"), label,
                          str(claim.get("text") or "")))
        else:
            merge_marks[home].append((klass, verdict.get("claim_id"), detail))
    return {
        "result": result, "merge_segments": merge_segments,
        "source_marks": source_marks, "merge_marks": merge_marks,
        "loose": loose, "unmarked": sorted(set(unmarked)),
        "findings": len((blob.get("structural") or {}).get("findings") or []),
    }


def mark_html(marks: list) -> str:
    if not marks:
        return ""
    out = []
    for klass, identifier, detail in marks:
        symbol, word, _ = CLASSES[klass]
        out.append(f'<span class="tag {klass}">{symbol} {word} '
                   f'<code>{html.escape(str(identifier))}</code> '
                   f'<span class="why">{html.escape(str(detail))}</span></span>')
    return '<span class="tags">' + "".join(out) + "</span>"


def block(text: str, kind: str, identifier: str, marks: list) -> str:
    klass = marks[0][0] if marks else ""
    return (f'<div class="seg {klass}">'
            f'<div class="segid"><code>{html.escape(identifier)}</code>'
            f'<span class="kind">{html.escape(kind)}</span></div>'
            f'<div class="segtext">{html.escape(text)}</div>'
            f'{mark_html(marks)}</div>')


STYLE = """
:root { --ink:#111; --paper:#fff; --rule:#d6d6d6; --dim:#5a5a5a; }
* { box-sizing: border-box; }
body { margin:0; padding:1.5rem; background:var(--paper); color:var(--ink);
  font:14px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
h1 { font-size:1.3rem; margin:0 0 .25rem; }
h2 { font-size:1rem; margin:1.6rem 0 .5rem; }
h3 { font-size:.9rem; margin:1rem 0 .4rem; color:var(--dim); }
.head { border:1px solid var(--rule); padding:.9rem 1rem; margin-bottom:1.2rem; }
.head dl { display:grid; grid-template-columns:max-content 1fr; gap:.15rem .8rem; margin:.6rem 0 0; }
.head dt { color:var(--dim); } .head dd { margin:0; }
.key { display:flex; flex-wrap:wrap; gap:.5rem; margin:.7rem 0 0; }
.panes { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
@media (max-width:900px){ .panes { grid-template-columns:1fr; } }
.pane { border:1px solid var(--rule); padding:.6rem .8rem; min-width:0; }
.merge { margin:1.6rem 0 2.4rem; border-top:3px solid var(--ink); padding-top:.8rem; }
.seg { padding:.35rem .5rem; margin:.2rem 0; border-left:4px solid transparent; }
.segid { font-size:.72rem; color:var(--dim); display:flex; gap:.5rem; }
.segtext { white-space:pre-wrap; overflow-wrap:anywhere; }
code { font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
.tags { display:flex; flex-wrap:wrap; gap:.35rem; margin-top:.3rem; }
.tag { font-size:.72rem; padding:.05rem .4rem; border:1px solid currentColor; }
.why { color:var(--dim); }
.dropped   { border-left-color:#b3261e; } .tag.dropped   { color:#b3261e; background:#fdecea; }
.reworded  { border-left-color:#8a5a00; } .tag.reworded  { color:#8a5a00; background:#fdf3e0; }
.altered   { border-left-color:#6b3fa0; } .tag.altered   { color:#6b3fa0; background:#f3ecfb; }
.unsupported   { border-left-color:#00629b; } .tag.unsupported   { color:#00629b; background:#e7f2fa; }
.contradicted  { border-left-color:#8f0f3f; } .tag.contradicted  { color:#8f0f3f; background:#fdeaf1; }
.declared  { border-left-color:#9a9a9a; } .tag.declared  { color:#4a4a4a; background:#f2f2f2; }
.caught    { border-left-color:#1b5e20; } .tag.caught    { color:#1b5e20; background:#e8f4ea; }
.missed    { border-left-color:#b3261e; } .tag.missed    { color:#b3261e; background:#fdecea; }
.invented  { border-left-color:#00629b; } .tag.invented  { color:#00629b; background:#e7f2fa; }
.unmeasured{ border-left-color:#6a6a6a; } .tag.unmeasured{ color:#3a3a3a; background:#eeeeee; }
.fixture { border:1px solid var(--rule); padding:.5rem .7rem; margin:.45rem 0; }
.fixture h3 { margin:0 0 .3rem; color:var(--ink); }
.idxlist a { display:block; padding:.1rem 0; }
.note { color:var(--dim); font-size:.8rem; }
.flag { border:1px solid #8a5a00; background:#fdf3e0; padding:.4rem .6rem; margin:.5rem 0; }
@media print { body { padding:0; } .pane, .head { border-color:#000; }
  .tag { border-color:#000; color:#000; background:transparent; } }
"""


def page(model: str, entries: list[dict], data: list[dict]) -> str:
    totals: dict[str, int] = defaultdict(int)
    for one in data:
        for marks in list(one["source_marks"].values()) + list(one["merge_marks"].values()):
            for klass, _, _ in marks:
                totals[klass] += 1
        for klass, _, _, _ in one["loose"]:
            totals[klass] += 1
    findings = sum(one["findings"] for one in data)

    key = "".join(
        f'<span class="tag {k}">{s} {w} - {html.escape(d)}</span>'
        for k, (s, w, d) in CLASSES.items())
    rows = "".join(
        f"<dt>{html.escape(k)}</dt><dd>{html.escape(str(v))}</dd>" for k, v in (
            ("model", model),
            ("merges on this page", str(len(entries))),
            ("blocks", ", ".join(sorted({e["label"].split("/")[0] for e in entries}))),
            ("source pair", "tests/pairs/index_429"),
            ("structural findings, all merges", str(findings)),
            ("marks by class", ", ".join(f"{CLASSES[k][1].lower()} {totals[k]}"
                                         for k in CLASSES if totals[k]) or "none"),
        ))

    body = []
    for entry, one in zip(entries, data):
        flag = ('<div class="flag">This draw was set aside by the project '
                '(<code>discarded-no-cache-absent</code>). It is shown because it '
                'happened, and it is not a result.</div>') if entry["discarded"] else ""
        panes = []
        source_html = []
        for coverage in one["result"].coverages:
            name = coverage.document.filename or coverage.document.id
            source_html.append(f"<h3>{html.escape(name)}</h3>")
            for located in coverage.located:
                source_html.append(block(
                    located.segment.text, located.segment.kind, located.segment.id,
                    one["source_marks"].get(located.segment.id, [])))
        panes.append('<div class="pane"><h2>Sources</h2>'
                     '<p class="note">What became of each source segment. A dropped '
                     'segment is not in the merge, so it can only be shown here.</p>'
                     + "".join(source_html) + "</div>")
        merge_html = [block(s.text, s.kind, s.id, one["merge_marks"].get(s.id, []))
                      for s in one["merge_segments"]]
        if one["loose"]:
            merge_html.append('<h3>Claims not located in a single segment</h3>')
            for klass, cid, label, text in one["loose"]:
                symbol, word, _ = CLASSES[klass]
                merge_html.append(
                    f'<div class="seg {klass}"><div class="segid">'
                    f'<code>{html.escape(str(cid))}</code>'
                    f'<span class="kind">{html.escape(label)}</span></div>'
                    f'<div class="segtext">{html.escape(text)}</div>'
                    f'<span class="tags"><span class="tag {klass}">{symbol} {word}'
                    f'</span></span></div>')
        panes.append('<div class="pane"><h2>Merged document</h2>'
                     '<p class="note">What the merge added or contradicted. '
                     'Everything else it carries is accounted for by a source.</p>'
                     + "".join(merge_html) + "</div>")
        extra = ""
        if one["unmarked"]:
            extra = ('<p class="note">Finding kinds counted in the header and not '
                     'turned into a mark: '
                     + html.escape(", ".join(one["unmarked"])) + "</p>")
        body.append(f'<section class="merge"><h2>{html.escape(entry["label"])}</h2>'
                    f'{flag}<p class="note">record: '
                    f'<code>{html.escape(str(entry["dir"].relative_to(ROOT)))}'
                    f'/report.json</code>, structural findings '
                    f'{one["findings"]}</p>{extra}'
                    f'<div class="panes">{"".join(panes)}</div></section>')

    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(model)} - annotated merges</title>'
            f"<style>{STYLE}</style></head><body>"
            f'<div class="head"><h1>{html.escape(model)} - annotated merges</h1>'
            f'<p class="note">Generated by <code>tests/annotate_merges.py</code> from '
            f'the stored records under <code>arms/2026-08-30/</code>. Every mark is '
            f'derived; nothing on this page is hand-marked.</p>'
            f"<dl>{rows}</dl><div class=\"key\">{key}</div></div>"
            + "".join(body) + "</body></html>\n")


INVENTIONS = ROOT / "paper" / "records" / "regrade-inventions.json"
DETECT_ARMS = ROOT / "arms" / "2026-09-03"


def detections() -> list[dict]:
    """Per-arm detection outcomes, read from the record that graded them.

    The grading is not recomputed here. `regrade-inventions.json` is the
    audited answer to which plants were caught, which fixtures the exit code
    missed, and which findings no probe accounts for -- it is the record every
    detection figure in the paper is read from. A second grader in a rendering
    script is a second answer, and the one that disagreed would be the one
    nobody was looking at.
    """
    if not INVENTIONS.is_file():
        return []
    blob = json.loads(INVENTIONS.read_text(encoding="utf-8"))
    out = []
    for arm in blob.get("arms") or []:
        label = str(arm.get("label") or arm.get("arm") or "")
        reports = DETECT_ARMS / label / "detect-reports"
        fixtures = sorted(p.stem for p in reports.glob("*.json")) if reports.is_dir() else []
        unaccounted: dict[str, list] = defaultdict(list)
        for finding in arm.get("unaccounted_findings") or []:
            unaccounted[str((finding or {}).get("fixture"))].append(finding)
        out.append({
            "arm": label,
            "fixtures": fixtures,
            "matched": set(arm.get("exit_code_matched") or []),
            "missed": set(arm.get("exit_code_missed") or []),
            "unmeasured": set(arm.get("exit_code_unmeasured") or []),
            "unaccounted": dict(unaccounted),
            "disqualified": list(arm.get("disqualified") or []),
            "plants_detected": arm.get("plants_detected"),
            "plants_total": arm.get("plants_total"),
        })
    return out


def detect_page(entry: dict) -> str:
    key = "".join(
        f'<span class="tag {k}">{s} {w} - {html.escape(d)}</span>'
        for k, (s, w, d) in CLASSES.items())
    head = [f'<div class="head"><h1>Detection: {html.escape(entry["arm"])}</h1>',
            '<dl>',
            f'<dt>plants detected</dt><dd>{entry["plants_detected"]} of '
            f'{entry["plants_total"]}</dd>',
            f'<dt>fixtures</dt><dd>{len(entry["fixtures"])}</dd>',
            f'<dt>graded from</dt><dd><code>regrade-inventions.json</code>, a record withheld with the paper</dd>',
            '</dl>']
    if entry["disqualified"]:
        for reason in entry["disqualified"]:
            head.append(f'<div class="flag">{html.escape(str(reason))}</div>')
    head.append(f'<div class="key">{key}</div></div>')

    body = []
    for fixture in entry["fixtures"]:
        marks = []
        if fixture in entry["unmeasured"]:
            marks.append(("unmeasured", fixture, "no reading could be taken"))
        elif fixture in entry["missed"]:
            marks.append(("missed", fixture,
                          "the exit status did not match the fixture's key"))
        elif fixture in entry["matched"]:
            marks.append(("caught", fixture,
                          "the exit status matched the fixture's key"))
        for finding in entry["unaccounted"].get(fixture, []):
            marks.append(("invented",
                          str((finding or {}).get("claim_id") or ""),
                          str((finding or {}).get("claim_text") or "")))
        klass = marks[0][0] if marks else ""
        detail = "".join(
            f'<div class="segtext">{html.escape(str((f or {}).get("rationale") or ""))}</div>'
            for f in entry["unaccounted"].get(fixture, []))
        body.append(f'<div class="fixture {klass}">'
                    f'<h3><code>{html.escape(fixture)}</code></h3>'
                    f'{mark_html(marks)}{detail}</div>')
    return ("<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<title>Detection: {html.escape(entry['arm'])}</title>"
            f"<style>{STYLE}</style></head><body>"
            + "".join(head)
            + '<p class="note"><a href="index.html">back to the index</a></p>'
            + "".join(body)
            + '<p class="note"><a href="index.html">back to the index</a></p>'
            "</body></html>\n")


def index_page(merge_pages: dict[str, str], detect_pages: dict[str, str]) -> str:
    def section(title: str, pages: dict[str, str], note: str) -> str:
        rows = "".join(
            f'<a href="{html.escape(name)}">{html.escape(label)}</a>'
            for label, name in sorted(pages.items()))
        return (f"<h2>{html.escape(title)}</h2><p class='note'>{html.escape(note)}</p>"
                f"<div class='idxlist'>{rows}</div>")
    return ("<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<title>annotated: what each arm did</title>"
            f"<style>{STYLE}</style></head><body>"
            "<h1>annotated</h1>"
            "<p>Every page is self-contained and renders offline with scripting "
            "off. Marks carry a symbol and a word as well as a colour.</p>"
            + section("Merges, by model", merge_pages,
                      "What each merge kept, dropped, reworded or invented, "
                      "marked per segment from the stored reports.")
            + section("Detection, by arm", detect_pages,
                      "Which planted defects each arm caught, which it missed, "
                      "and which findings no probe accounts for, graded from "
                      "regrade-inventions.json, a record withheld with the paper.")
            + "</body></html>\n")


def build(out: Path) -> dict[str, int]:
    out.mkdir(parents=True, exist_ok=True)
    grouped: dict[str, list] = defaultdict(list)
    for entry in merges():
        grouped[entry["model"]].append(entry)
    written = {}
    merge_pages: dict[str, str] = {}
    for model, entries in sorted(grouped.items()):
        data = [annotate(e) for e in entries]
        name = model.replace(":", "-").replace(".", "-").replace("/", "-") + ".html"
        target = out / name
        target.write_text(page(model, entries, data), encoding="utf-8")
        written[name] = target.stat().st_size
        merge_pages[model] = name
    detect_pages: dict[str, str] = {}
    for entry in detections():
        name = "detect-" + entry["arm"].replace(":", "-").replace(".", "-") + ".html"
        target = out / name
        target.write_text(detect_page(entry), encoding="utf-8")
        written[name] = target.stat().st_size
        detect_pages[entry["arm"]] = name
    index = out / "index.html"
    index.write_text(index_page(merge_pages, detect_pages), encoding="utf-8")
    written["index.html"] = index.stat().st_size
    return written


def check() -> int:
    if not ARMS.is_dir():
        print("  arms/2026-08-30/ is absent; nothing to annotate")
        return 0
    # The detection pages are graded from `paper/records/regrade-inventions.json`
    # and a published copy withholds `paper` wholesale. The merge pages are
    # still fully checkable there, so the copy checks those and says plainly
    # that it could not check the rest: a run that prints only "ok" would
    # imply it had verified pages it never looked at.
    graded = INVENTIONS.is_file()
    scratch = Path(tempfile.mkdtemp(prefix="llossless-annotated-"))
    try:
        fresh = build(scratch)
        committed_names = (sorted(p.name for p in OUT.glob("*.html"))
                           if OUT.is_dir() else [])
        # Without the grading record no detection page can be produced, so the
        # committed ones cannot be compared and must not be reported as
        # orphans either. The index goes with them: it lists them.
        skipped = set() if graded else (
            {n for n in set(fresh) | set(committed_names)
             if n.startswith("detect-")} | {"index.html"})
        problems = []
        for name in sorted(set(fresh) - skipped):
            committed = OUT / name
            if not committed.is_file():
                problems.append(f"{name} has never been generated")
            elif committed.read_bytes() != (scratch / name).read_bytes():
                problems.append(f"{name} disagrees with the records it came from")
        for stale in committed_names:
            if stale not in fresh and stale not in skipped:
                problems.append(f"{stale} is not produced by any record")
        if problems:
            print(f"REFUSED: {len(problems)} annotated page(s) are stale.")
            for line in problems:
                print(f"  {line}")
            print("  Regenerate with `tests/annotate_merges.py`.")
            return 1
        checked = sorted(set(fresh) - skipped)
        print(f"  {len(checked)} annotated page(s) agree with the records: "
              + ", ".join(f"{n} ({fresh[n] // 1024} KiB)" for n in checked))
        if skipped:
            pages = len([n for n in skipped if n.startswith("detect-")])
            print(f"  UNMEASURED: paper/records/ is withheld from the published "
                  f"copy, so the {pages} detection page(s) and the index cannot "
                  f"be regraded here. Not a failure: the grading record ships "
                  f"with the paper, not with the tool.")
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="refuse if the committed pages are stale")
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args(argv)
    if args.check:
        return check()
    written = build(args.out)
    total = sum(written.values())
    for name, size in sorted(written.items()):
        print(f"  {name}  {size // 1024} KiB")
    print(f"  {len(written)} page(s), {total // 1024} KiB total, in "
          f"{args.out.relative_to(ROOT) if args.out.is_relative_to(ROOT) else args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
