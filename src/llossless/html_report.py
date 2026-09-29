"""The same report, as one self-contained HTML page.

`render(run)` takes the object `report.render` takes and returns a whole
document: no CDN, no font host, no image, no fetch. A report is read by someone
deciding whether to trust a merged document, and a page that phones home to
render itself would put that decision behind a network it does not control.
Everything below is `html.escape`, string joins and one `<style>` block.

`with_download` is the single exception, and it is why `render` leaves a `SLOT`
in the page: a server showing this report may fill it with a control that saves
the file. What that control hands over is the page `render` returned, slot and
all, so the copy that leaves here stays the copy that opens anywhere.

Three rules shape the file.

**Escaping is a security property, not a cosmetic one.** Every value on this
page came from a document or a model, and a model asked to quote a source will
quote whatever the source contains. `esc` is applied to all of it; `inline` is
applied only to prose this codebase wrote, and it escapes first and *then*
honours `**bold**` and `` `code` `` markers, so a document that contains
`<script>` is inert whichever function handles it. `tests/test_html_report.py`
holds a must-fire probe for exactly that.

**No figure is computed here.** Every number, sentence and status word is
imported from `report.py`, which is where the Markdown report and the exit code
get them. A renderer that recomputed a ratio would be a second answer to a
question this project already refuses to answer twice, and the parity test
asserts the two outputs agree claim by claim rather than trusting that they do.

**Meaning is never carried by colour alone.** Every chip, bar and banner has a
word in it. The palette is four states - green carried, amber partial or
queued, red lost or violated, grey not checked - and a reader who sees none of
them reads the same report.
"""

from __future__ import annotations

import base64
import html
import re

from .report import (
    DIFF_LEGEND,
    EXIT_CODES,
    CHECKS,
    FINDING_KINDS,
    FINDING_ORDER,
    FORWARD_ORDER,
    FORWARD_STATUS,
    HEADINGS,
    MERGED,
    NOT_CHECKED,
    REVERSE_ORDER,
    REVERSE_STATUS,
    STRUCTURAL_HEADINGS,
    InventoryDisagrees,
    REFERENCE_NOTE,
    Run,
    elsewhere, stacked_lines,
    basis_word,
    budget_sentence,
    loss_row,
    mismatch_sentence,
    evidence_note,
    exit_code,
    join_names,
    judged_against_names,
    order_line,
    sourcing_sentence,
    tally,
    verdict_line,
    where_line,
)
from .verify import CONFIRMED, GROUNDED, NOT_GRADED, REJECTED

# Status word -> the state it is painted in. Keyed on the words the inventory
# tables print rather than on finding kinds, because that is what a cell holds
# and the mapping has to be total over it: an unmapped status would render as
# an unpainted chip, which reads as "fine" and is the one wrong answer.
STATE = {
    FORWARD_STATUS["none"]: "ok",
    REVERSE_STATUS["none"]: "ok",
    FORWARD_STATUS["partially_dropped"]: "warn",
    REVERSE_STATUS["partially_invented"]: "warn",
    FORWARD_STATUS["dropped"]: "bad",
    REVERSE_STATUS["hallucinated"]: "bad",
    FORWARD_STATUS["contradicted"]: "bad",
    NOT_CHECKED: "none",
}

# Same guard the Markdown report puts on its heading tables, for the same
# reason: a status word with no state would be painted grey - "not checked" -
# over a claim that was checked and lost.
assert set(STATE) == set(FORWARD_STATUS.values()) | set(REVERSE_STATUS.values()) | {
    NOT_CHECKED
}

# The exit code, as a word and a state. The banner says both; nothing on this
# page depends on the reader seeing the colour.
# Every code `report.exit_code` can return, and a bare subscript below wants
# them all: entry 420 split `3` out of `1` and this table was not told, so a
# record-only failure crashed the HTML report with `KeyError: 3` (500). The
# operator met it as an unexplained crash at the end of an otherwise finished
# run.
#
# `3` is amber rather than red on purpose. The distinction 420 exists to draw
# is that the *document* is sound as far as this tool looked and the merge's
# account of itself is not, which is a different thing to hand a reader than
# content that went missing.
BANNER = {
    0: ("ok", "Clean"),
    1: ("bad", "Findings"),
    2: ("none", "Inconclusive"),
    3: ("warn", "Record findings"),
}

assert set(BANNER) == set(EXIT_CODES), (
    "every exit code needs a banner; a bare subscript reads this table and a "
    "missing row is a crash at the end of a finished run"
)

STYLE = """
:root {
  color-scheme: light;
  --bg: #ffffff;
  --panel: #f7f7f5;
  --ink: #1a1a1a;
  --ink-soft: #56534d;
  --line: #d8d5cf;
  --ok: #1f7a3d;
  --ok-bg: #e6f4ea;
  --warn: #8a5a00;
  --warn-bg: #fdf1dc;
  --bad: #a3272c;
  --bad-bg: #fbe9e9;
  --none: #55534f;
  --none-bg: #eeece8;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
    --bg: #16181c;
    --panel: #1f2228;
    --ink: #e9e7e3;
    --ink-soft: #a8a49c;
    --line: #343841;
    --ok: #6ed08c;
    --ok-bg: #17301f;
    --warn: #e0b25e;
    --warn-bg: #33280f;
    --bad: #f28b8b;
    --bad-bg: #3a1c1e;
    --none: #a8a49c;
    --none-bg: #262a31;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 16px/1.55 system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
}
main { max-width: 62rem; margin: 0 auto; padding: 1.5rem 1.25rem 4rem; }
h1 { font-size: 1.45rem; margin: 0 0 .25rem; }
h2 { font-size: 1.2rem; margin: 2.25rem 0 .5rem; padding-top: .4rem;
     border-top: 1px solid var(--line); }
h3 { font-size: 1rem; margin: 1.4rem 0 .4rem; }
p { margin: .5rem 0; }
code, .mono { font-family: var(--mono); font-size: .92em; }
a { color: inherit; }
.subtitle { color: var(--ink-soft); margin: 0 0 1rem; }
.banner {
  border: 1px solid var(--line);
  border-left: .5rem solid var(--none);
  background: var(--panel);
  border-radius: .4rem;
  padding: .9rem 1rem;
  margin: 0 0 1rem;
}
.banner .label {
  display: inline-block; font-weight: 700; letter-spacing: .04em;
  text-transform: uppercase; font-size: .78rem; margin-bottom: .3rem;
}
.banner.ok   { border-left-color: var(--ok);   background: var(--ok-bg); }
.banner.ok .label { color: var(--ok); }
.banner.bad  { border-left-color: var(--bad);  background: var(--bad-bg); }
.banner.bad .label { color: var(--bad); }
.banner.none { border-left-color: var(--none); background: var(--none-bg); }
.banner.none .label { color: var(--none); }
.toc { margin: 0 0 1.25rem; padding: 0; list-style: none;
       display: flex; flex-wrap: wrap; gap: .4rem .75rem; font-size: .9rem; }
.toc a { color: var(--ink-soft); text-decoration: none;
         border-bottom: 1px solid var(--line); }
.toc a:hover, .toc a:focus { color: var(--ink); }
.toolbar { margin: 0 0 1rem; display: flex; flex-wrap: wrap;
           align-items: baseline; gap: .5rem .75rem; }
.toolbar .save {
  display: inline-block; font-size: .9rem; font-weight: 600;
  text-decoration: none; padding: .35rem .7rem;
  color: var(--ink); background: var(--panel);
  border: 1px solid var(--line); border-radius: .3rem;
}
.toolbar .save:hover, .toolbar .save:focus { border-color: var(--ink-soft); }
.toolbar .note { font-size: .85rem; }
.filter { margin: 0 0 1.25rem; }
.filter label { display: block; font-size: .85rem; color: var(--ink-soft); }
.filter input {
  width: 100%; padding: .45rem .6rem; font: inherit;
  color: var(--ink); background: var(--panel);
  border: 1px solid var(--line); border-radius: .3rem;
}
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: .93rem; }
th, td { text-align: left; vertical-align: top; padding: .4rem .55rem;
         border-bottom: 1px solid var(--line); }
thead th { position: sticky; top: 0; z-index: 1;
           background: var(--panel); border-bottom: 2px solid var(--line); }
tbody tr:nth-child(even) { background: var(--panel); }
td.num, td.line { font-family: var(--mono); white-space: nowrap; }
td.claim { min-width: 18rem; }
.chip {
  display: inline-block; white-space: nowrap; font-size: .8rem; font-weight: 600;
  padding: .1rem .45rem; border-radius: .8rem; border: 1px solid transparent;
}
.chip.ok   { color: var(--ok);   background: var(--ok-bg);   border-color: var(--ok); }
.chip.warn { color: var(--warn); background: var(--warn-bg); border-color: var(--warn); }
.chip.bad  { color: var(--bad);  background: var(--bad-bg);  border-color: var(--bad); }
.chip.none { color: var(--none); background: var(--none-bg); border-color: var(--none); }
.bar { display: flex; align-items: center; gap: .5rem; }
.bar .track {
  flex: 1 1 6rem; max-width: 12rem; height: .55rem; border-radius: .3rem;
  background: var(--none-bg); border: 1px solid var(--line); overflow: hidden;
}
.bar .fill { display: block; height: 100%; background: var(--ok); }
.bar.warn .fill { background: var(--warn); }
.bar.bad .fill { background: var(--bad); }
.bar .value { font-family: var(--mono); white-space: nowrap; }
.card {
  border: 1px solid var(--line); border-left: .35rem solid var(--none);
  background: var(--panel); border-radius: .3rem;
  padding: .6rem .8rem; margin: .5rem 0;
}
.card.bad  { border-left-color: var(--bad); }
.card.warn { border-left-color: var(--warn); }
.card .head { font-family: var(--mono); font-weight: 700; }
.card .text { margin: .3rem 0; }
.card dl { margin: .3rem 0 0; }
.card dt { font-size: .8rem; color: var(--ink-soft); text-transform: uppercase;
           letter-spacing: .03em; margin-top: .35rem; }
.card dd { margin: 0; }
/* A finding's two sides, under its sentence (552). The label is a word and
   the value is document text, so the two are told apart by weight and case
   rather than by colour -- this report is read on paper and in a terminal's
   browser, and a difference carried by hue is a difference somebody misses. */
.card .detail { margin: .25rem 0 0; font-size: .9rem; }
.card .detail .label { font-size: .78rem; color: var(--ink-soft);
                       text-transform: uppercase; letter-spacing: .04em;
                       margin-right: .4rem; }
.card .detail q { font-family: var(--mono); }
/* The word diff. Monospace so the markers line up, wrapping so a long
   segment does not push the card sideways. The markers carry the meaning on
   their own, which is why nothing here is coloured. */
.card .wdiff { font-family: var(--mono); font-size: .88rem;
               white-space: pre-wrap; overflow-wrap: anywhere; }
/* The two sides stacked (561). Monospaced and wrapping, for the same two
   reasons as the diff above: the labels are padded to one width so the texts
   start in the same column, which is only true in a monospaced box, and a
   panel that grows a horizontal scrollbar is 531's defect. `overflow-wrap`
   rather than `word-break`, because a wrapped line still has to start in the
   same column for the stack to be read down. */
.card pre.stack { font-family: var(--mono); font-size: .88rem;
                  white-space: pre-wrap; overflow-wrap: anywhere;
                  margin: .4rem 0 0; padding: .5rem .6rem;
                  background: var(--panel); border: 1px solid var(--line);
                  border-radius: .3rem; }
.note { color: var(--ink-soft); }
.callout {
  border-left: .3rem solid var(--warn); background: var(--warn-bg);
  padding: .5rem .8rem; margin: .8rem 0; border-radius: .2rem;
}
details { margin: .6rem 0; }
summary { cursor: pointer; font-weight: 600; }
.empty { color: var(--ink-soft); }
pre.document {
  white-space: pre-wrap; word-break: break-word; font-family: var(--mono);
  font-size: .88rem; background: var(--panel); border: 1px solid var(--line);
  border-radius: .3rem; padding: .8rem;
}
tr.hidden, .card.hidden { display: none; }
@media print {
  body { background: #fff; color: #000; }
  /* A control that saves the file is furniture on paper, the same way the
     filter box is: neither does anything once the page is ink. */
  .filter, .toc, .toolbar { display: none; }
  details { display: block; }
  details > summary { list-style: none; }
  thead th { position: static; }
  tr.hidden, .card.hidden { display: revert; }
  h2 { break-after: avoid; }
  table, .card { break-inside: avoid; }
}
"""

# One filter, over rows and cards, matching the text the reader can see. It
# hides nothing on a page with JavaScript off: the attribute it toggles is only
# ever added here, so the report's default state is everything visible.
SCRIPT = """
(function () {
  var box = document.getElementById('filter');
  if (!box) { return; }
  var items = [].slice.call(document.querySelectorAll('[data-filterable]'));
  var count = document.getElementById('filter-count');
  function apply() {
    var q = box.value.trim().toLowerCase();
    var shown = 0;
    items.forEach(function (el) {
      var hit = q === '' || el.textContent.toLowerCase().indexOf(q) !== -1;
      el.classList.toggle('hidden', !hit);
      if (hit) { shown += 1; }
    });
    count.textContent = q === ''
      ? items.length + ' row(s) and card(s)'
      : shown + ' of ' + items.length + ' matching "' + q + '"';
  }
  box.addEventListener('input', apply);
  apply();
})();
"""


# The one place the page a server shows and the file on disk are allowed to
# differ. `render` leaves it empty; `with_download` fills it. A file that is
# already on somebody's disk cannot offer to download itself -- the link would
# point at a server that reader may never have been able to reach -- so the
# copy the CLI writes, and the copy the control itself hands over, keep the
# slot empty.
#
# The marker does not contain the word "download" on purpose: the check that a
# saved copy carries no control greps it for one, and a leftover marker that
# matched the grep would make that check pass by finding itself.
SLOT = "<!--controls-->"


def esc(text: object) -> str:
    """Anything a document or a model produced, made inert.

    Quotes included: several of these values land in an attribute, and one
    function for both is one fewer place to be wrong about which.
    """
    return html.escape(str(text), quote=True)


_BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
_CODE = re.compile(r"`([^`]+)`")


def inline(text: object) -> str:
    """Prose this codebase wrote, with its `**bold**` and `` `code` `` honoured.

    Escaped first and marked up second, which is the order that makes the
    markers safe: after `esc` the string contains no `<`, so the only tags in
    the result are the ones these two patterns put there. Never called on claim
    text, evidence or a model's rationale - those go through `esc`, because a
    document that happens to contain an asterisk is not asking for emphasis and
    a report that granted it would be editing the text it exists to preserve.
    """
    out = esc(text)
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    return _CODE.sub(r"<code>\1</code>", out)


def code_only(text: object) -> str:
    """`inline` without the emphasis. For a row that quotes caller data.

    The provenance rows are built by `provenance.rows()`, which wraps a
    filename or a prompt path in backticks so both renderers show it as code.
    That mixes markup this codebase wrote with a value the caller chose, and
    `inline` cannot tell them apart -- a base document named `a**b**c.md`
    arrived as emphasis (326).

    Backticks are still honoured, because the quoting is this module's and
    `provenance._base` drops it when the name could close it. `**` is not,
    because nothing in these rows uses it and a filename may.
    """
    return _CODE.sub(r"<code>\1</code>", esc(text))


def _pct(numerator: int, denominator: int) -> float:
    return 100.0 * numerator / denominator if denominator else 0.0


def _bar(numerator: int, denominator: int, label: str) -> str:
    """A ratio, as a bar and as the ratio. The number is the fact; the bar is a hint.

    `ratio` decides what a zero denominator prints, here as everywhere else, so
    a pass that graded nothing cannot show up as an empty bar that reads like a
    zero score.
    """
    if denominator == 0:
        return f'<span class="value">{inline(label)}</span>'
    share = _pct(numerator, denominator)
    state = "ok" if share >= 99.5 else "warn" if share >= 90 else "bad"
    return (
        f'<span class="bar {state}">'
        f'<span class="track"><span class="fill" style="width: {share:.1f}%"></span></span>'
        f'<span class="value">{numerator}/{denominator}</span>'
        f"</span>"
    )


def _chip(status: str) -> str:
    return f'<span class="chip {STATE[status]}">{esc(status)}</span>'


def _rows(pairs: list[tuple[str, str]]) -> list[str]:
    """A two-column table of label and already-rendered value."""
    out = ['<div class="scroll"><table><tbody>']
    out += [
        f"<tr><th scope=\"row\">{label}</th><td>{value}</td></tr>"
        for label, value in pairs
    ]
    out.append("</tbody></table></div>")
    return out


def _section(anchor: str, title: str, body: list[str]) -> list[str]:
    return [f'<section id="{anchor}">', f"<h2>{esc(title)}</h2>", *body, "</section>"]


def verdict_block(run: Run) -> list[str]:
    """The banner: the exit code as a word, a colour and the report's own sentence."""
    code = exit_code(run)
    state, word = BANNER[code]
    return [
        f'<div class="banner {state}" data-exit-code="{code}">',
        f'<span class="label">{esc(word)} — exit {code}</span>',
        f"<p>{inline(verdict_line(run))}</p>",
        "</div>",
    ]


def coverage_block(run: Run) -> list[str]:
    """The denominators, first and in bars. Same rows as the Markdown table."""
    graded = [v for v in run.verdicts if v.grounding != NOT_GRADED]
    grounded = [v for v in graded if v.grounding == GROUNDED]
    forward_submitted = run.submitted("forward")
    reverse_submitted = run.submitted("reverse")

    pairs = [
        (
            f"Claims extracted from <code>{esc(run.display(name))}</code>",
            f'<span class="value mono">{len(run.claims[name])}</span>',
        )
        for name in sorted(run.claims)
    ]
    pairs.append((
        "Forward — source claims accounted for in the merge",
        _bar(
            len([v for v in run.forward if v.finding == "none"]),
            len(run.forward),
            f"not checked ({forward_submitted} claim(s) extracted)",
        ),
    ))
    pairs.append((
        "Forward — carried only in part",
        f'<span class="value mono">'
        f'{len([v for v in run.forward if v.finding == "partially_dropped"])}</span>',
    ))
    by_source = run.forward_by_source()
    for name in sorted(by_source):
        row = by_source[name]
        if not name:
            pairs.append((
                "Forward — claims matching no source",
                f'<span class="value mono">{row["checked"]}</span>',
            ))
            continue
        value = _bar(
            row["accounted"],
            row["checked"],
            "no claims extracted — nothing to check"
            if row["extracted"] == 0
            else f"not checked ({row['extracted']} claim(s) extracted)",
        )
        if row["partial"]:
            value += f' <span class="note">({row["partial"]} in part)</span>'
        pairs.append((
            f"Forward — <code>{esc(run.display(name))}</code> claims accounted for",
            value,
        ))
    pairs += [
        (
            "Reverse — merge claims found in a source",
            _bar(
                len([v for v in run.reverse if v.finding == "none"]),
                len(run.reverse),
                f"not checked ({reverse_submitted} claim(s) extracted)",
            ),
        ),
        (
            "Reverse — supported only in part",
            f'<span class="value mono">'
            f'{len([v for v in run.reverse if v.finding == "partially_invented"])}</span>',
        ),
        (
            "Evidence grounded",
            _bar(len(grounded), len(graded), "no verdict quoted a span"),
        ),
        (
            "Units of work errored",
            f'<span class="value mono">{len(run.errored)}</span>',
        ),
    ]

    body = _rows(pairs)
    # One naming system, not two: every row above and every finding below uses
    # `run.display`, a short name built from the caller's own path (entry 411).
    # There is nothing left here to reconcile against a canonical name.
    for step in run.errored:
        body.append(
            f'<div class="callout"><strong>{esc(step.name)} errored.</strong> '
            f"{esc(step.detail)}</div>"
        )
    return body


def _judged_against(run: Run, verdict) -> list[str]:
    """The document this verdict was read against, on the card that quotes it.

    Directly above the rationale in both branches, because the rationale is
    the prose that says *"the reference"* and this is the line that says what
    the reference was. The operator asked the question twice off one report
    and the answer -- `merged.md` both times -- was nowhere on the page.
    `report.judged_against` is the one implementation; this renders it.

    Labelled "Checked against" (717), not "Judged against": the operator read
    it as sounding like the named document had to defend itself, which is not
    the point -- the point is which document the verdict was read against.
    """
    return ["<dt>Checked against</dt>", f"<dd>{_against(run, verdict.direction)}</dd>"]


def _against(run: Run, direction: str) -> str:
    """The document names, escaped and wrapped, never routed through `inline`.

    `inline` honours `**` and backticks, and a filename is the caller's text:
    `tests/test_html_report.py` probes with `a`b**c**d.md` for exactly this.
    So `report.judged_against_names` hands over the bare names and the markup
    is built here, the same way every other filename on this page is.
    """
    names = [f"<code>{esc(name)}</code>"
             for name in judged_against_names(run, direction)]
    return join_names(names)


def _finding_card(run: Run, verdict, claim, kind: str) -> list[str]:
    """One finding, with everything the Markdown list puts under it.

    A card rather than a row because the entries are ragged: a contradiction
    carries two statements and a `dropped` carries one, and a table wide enough
    for the first prints the second as mostly empty cells.
    """
    where = (
        f"{run.display(claim.source)}:{claim.line}" if claim else "unknown line"
    )
    text = claim.text if claim else verdict.claim_id
    state = "warn" if kind in ("partially_dropped", "partially_invented") else "bad"
    out = [
        f'<article class="card {state}" data-filterable data-kind="{esc(kind)}" '
        f'data-claim-id="{esc(verdict.claim_id)}">',
        f'<div class="head">{esc(verdict.claim_id)} '
        f'<span class="mono note">{esc(where)}</span></div>',
        f'<p class="text">{esc(text)}</p>',
        "<dl>",
    ]
    if kind == "contradicted":
        # Both halves, labelled by side, and no line saying which is right -
        # the Markdown section's reasoning, unchanged.
        if verdict.evidence:
            mark = "grounded" if verdict.grounded else verdict.grounding
            out += [
                f"<dt>{esc(run.display(verdict.evidence_source))} says</dt>",
                f"<dd>{esc(repr(verdict.evidence))} "
                f'<span class="note">({esc(mark)})</span></dd>',
            ]
        else:
            out += [
                "<dt>The other side</dt>",
                "<dd>quoted nothing, so what it says instead is not on the "
                "record</dd>",
            ]
        out += _judged_against(run, verdict)
        if verdict.rationale:
            out += [
                "<dt>Why this was read as a contradiction</dt>",
                f"<dd>{esc(verdict.rationale)}</dd>",
            ]
    else:
        if verdict.evidence:
            mark = "grounded" if verdict.grounded else verdict.grounding
            out += [
                "<dt>Evidence</dt>",
                f"<dd>{esc(repr(verdict.evidence))} in "
                f"<code>{esc(run.display(verdict.evidence_source))}</code> "
                f'<span class="note">({esc(mark)})</span></dd>',
            ]
        out += _judged_against(run, verdict)
        if verdict.rationale:
            # Whose words these are (717): see `report.py`'s matching line.
            out += ["<dt>Why it was flagged (the checker's words)</dt>",
                    f"<dd>{esc(verdict.rationale)}</dd>"]
    out += ["</dl>", "</article>"]
    return out


def findings_block(run: Run) -> list[str]:
    if not run.findings:
        if run.structural or run.attributions or run.number_faults:
            # The Markdown section's sentence, less its markup (569).
            return [
                f'<p class="empty">'
                f'{esc(elsewhere(run).replace("`## ", "").replace("`", ""))}</p>'
            ]
        return ['<p class="empty">None.</p>']

    by_id = {claim.id: claim for claims in run.claims.values() for claim in claims}
    # One copy of the Markdown section's own lead-in, for the reason every
    # other sentence here is imported: two surfaces answering "was this the
    # model's outside knowledge?" in two sets of words is how a reader comes
    # to believe they mean two different things.
    out: list[str] = [f'<p class="note">{inline(REFERENCE_NOTE)}</p>']
    for kind in FINDING_ORDER:
        hits = [v for v in run.findings if v.finding == kind]
        if not hits:
            continue
        out.append(f"<h3>{esc(HEADINGS[kind])}</h3>")
        for verdict in hits:
            out += _finding_card(run, verdict, by_id.get(verdict.claim_id), kind)
    return out


def _inventory_table(
    run: Run, name: str, reverse: bool
) -> tuple[list[str], list[str]]:
    """One document's claims and what became of each. Statuses returned, as in Markdown.

    The caller holds them against the coverage table. This function counts
    nothing on its own: `FORWARD_STATUS` and `REVERSE_STATUS` decide the word,
    `tally` decides the summary, and both come from `report.py`.
    """
    source = run.reverse if reverse else run.forward
    verdicts = {v.claim_id: v for v in source}
    claims = run.claims.get(name, [])
    statuses, rows = [], []
    labels = REVERSE_STATUS if reverse else FORWARD_STATUS
    order = REVERSE_ORDER if reverse else FORWARD_ORDER
    for index, claim in enumerate(claims, start=1):
        verdict = verdicts.get(claim.id)
        status = labels[verdict.finding] if verdict else NOT_CHECKED
        statuses.append(status)
        rows.append((index, claim, status, verdict))
    rank = {labels[kind]: i for i, kind in enumerate(order)}
    rows.sort(key=lambda row: rank.get(row[2], len(rank)))

    heading = (
        f"<h3><code>{esc(run.display(name))}</code> — {len(claims)} claim(s): "
        f"{esc(tally(statuses, order, labels))}</h3>"
    )
    if not claims:
        empty = (
            "No claim was extracted from the merged document, so nothing in it "
            "was checked back against the sources."
            if reverse
            else "No claim was extracted from this document, so the merge was "
            "checked against nothing from it."
        )
        return [heading, f'<p class="empty">{esc(empty)}</p>'], statuses

    head = (
        "<tr><th>#</th><th>Claim</th><th>Status</th><th>Found in</th><th>Note</th></tr>"
        if reverse
        else "<tr><th>#</th><th>Claim</th><th>Line</th><th>Status</th><th>Note</th></tr>"
    )
    # The Markdown table's caption, for the same reason: the Note column is the
    # model's rationale verbatim and that prose says "the reference".
    against = _against(run, "merged_to_sources" if reverse else "source_to_merged")
    out = [heading,
           f'<p class="note">Each claim below was read against {against}.</p>',
           '<div class="scroll"><table>', f"<thead>{head}</thead>", "<tbody>"]
    for index, claim, status, verdict in rows:
        cells = [
            f'<td class="num">{index}</td>',
            f'<td class="claim">{esc(claim.text)}</td>',
        ]
        if reverse:
            found = (
                f"<code>{esc(run.display(verdict.evidence_source))}</code>"
                if verdict
                and verdict.evidence_source
                and verdict.finding != "hallucinated"
                else '<span class="note">--</span>'
            )
            cells += [f"<td>{_chip(status)}</td>", f"<td>{found}</td>"]
        else:
            cells += [
                f'<td class="line">{esc(where_line(run, claim))}</td>',
                f"<td>{_chip(status)}</td>",
            ]
        cells.append(f'<td class="note">{esc(evidence_note(verdict, run))}</td>')
        out.append(
            f'<tr data-filterable data-claim-id="{esc(claim.id)}" '
            f'data-status="{esc(status)}">' + "".join(cells) + "</tr>"
        )
    out += ["</tbody></table></div>"]
    return out, statuses


def inventory_block(run: Run) -> list[str]:
    """Every claim, carried or not, inside a `<details>` per document.

    Collapsed because these are the long tables and the exceptions are above
    them; open in print, where there is no one to click. The counts in each
    summary are `report.tally` over the statuses the rows were printed with, so
    the heading cannot disagree with the rows under it.
    """
    out = [
        "<p>Every claim that was extracted, and what became of it. The sections "
        "above list only the exceptions; this lists all of them, so a claim that "
        "is not here was never checked.</p>"
    ]
    by_source = run.forward_by_source()
    names = [(name, False) for name in run.sources()]
    if MERGED in run.claims:
        names.append((MERGED, True))
    for name, reverse in names:
        rows, statuses = _inventory_table(run, name, reverse)
        out += ["<details open>", "<summary>", *rows[:1], "</summary>", *rows[1:],
                "</details>"]
        # The same guard `report.inventory_section` raises, over the same two
        # figures. A page that can disagree with the Markdown report is worse
        # than one that refuses, and the check is free here: the statuses came
        # from the rows that were printed.
        if reverse:
            accounted = len([v for v in run.reverse if v.finding == "none"])
            if statuses.count(REVERSE_STATUS["none"]) != accounted:
                raise InventoryDisagrees(
                    f"{run.display(MERGED)}: the inventory counts "
                    f"{statuses.count(REVERSE_STATUS['none'])} supported and the "
                    f"coverage table counts {accounted}. One report, two answers."
                )
            continue
        row = by_source.get(name)
        counted = {
            "extracted": len(statuses),
            "checked": len([s for s in statuses if s != NOT_CHECKED]),
            "accounted": statuses.count(FORWARD_STATUS["none"]),
            "partial": statuses.count(FORWARD_STATUS["partially_dropped"]),
        }
        if row is not None and counted != row:
            raise InventoryDisagrees(
                f"{name}: the inventory rows count {counted} and the coverage "
                f"table counts {row}. One report, two answers."
            )
    return out


def structural_block(run: Run) -> list[str]:
    if run.reconciled is None:
        return [
            '<p class="empty"><strong>Not checked.</strong> The reconciler did not '
            "run over this merge, so nothing below the claim level was examined: "
            "no title, no invariant-core token, and no source segment that "
            "produced no claim.</p>"
        ]
    out = [
        f"<p><strong>{CHECKS}</strong> mechanical check(s) over "
        f"<strong>{run.reconciled.segments}</strong> source segment(s) and what the "
        f"merge declared about them. No model was asked anything: every check here "
        f"is a set difference, a string containment or a division.</p>",
        f'<p class="note">{inline(order_line(run))}</p>',
    ]
    if not run.structural:
        out.append('<p class="empty">No structural finding.</p>')
        return out
    # The notation, once, and only where a row below will use it (552).
    if any(finding.difference for finding in run.structural):
        out.append(f'<p class="note">{inline(DIFF_LEGEND)}</p>')
    for kind in FINDING_KINDS:
        hits = [f for f in run.structural if f.kind == kind]
        if not hits:
            continue
        out.append(f"<h3>{esc(STRUCTURAL_HEADINGS[kind])}</h3>")
        for finding in hits:
            where = " ".join(
                part
                for part in (
                    f"<code>{esc(finding.segment)}</code>" if finding.segment else "",
                    f"(<code>{esc(run.display(finding.document))}</code>)"
                    if finding.document
                    else "",
                )
                if part
            )
            # Issue, then the two sides stacked, in the card rather than in a
            # section a reader has to go and find (552, 561). `esc` on it: the
            # stack is built out of document text, and a document is somebody's
            # input.
            #
            # One `<pre>` holding the same three lines the Markdown report
            # prints, from the same function. Two renderings of one layout is
            # how a column that lines up in one file stops lining up in the
            # other -- and the padding `stacked_lines` does is only true in a
            # monospaced box, which is what `<pre>` is for. It wraps rather
            # than scrolls; 531's rule is that a panel does not grow a
            # horizontal scrollbar.
            stack = stacked_lines(finding)
            evidence = (f'<pre class="stack">{esc(chr(10).join(stack))}</pre>'
                        if stack else "")
            out.append(
                f'<article class="card bad" data-filterable data-kind="{esc(kind)}">'
                + (f'<div class="head">{where}</div>' if where else "")
                + f'<p class="text">{esc(finding.detail)}</p>{evidence}</article>'
            )
    return out


def queue_block(run: Run) -> list[str]:
    """Losses the merge owned. Amber, never red: this is work, not a fault."""
    out: list[str] = []
    if run.queued:
        out.append(
            f"<p><strong>{len(run.queued)}</strong> claim(s) the merge declared "
            f"dropped and the forward pass confirms are gone. Each is a decision to "
            f"review — put the fact back, or agree it stays out — and none of them "
            f"is counted as a finding above.</p>"
        )
        by_id = {claim.id: claim for claims in run.claims.values() for claim in claims}
        # The same filter the Markdown queue uses: a rejected record, or one
        # that declared something other than a drop, owns nothing here.
        owner = {
            claim_id: item
            for item in run.declarations
            if item.disposition == "dropped" and item.grade == CONFIRMED
            for claim_id in item.claims
        }
        for verdict in run.queued:
            claim = by_id.get(verdict.claim_id)
            where = (
                f"{run.display(claim.source)}:{claim.line}" if claim else "unknown line"
            )
            text = claim.text if claim else verdict.claim_id
            item = owner.get(verdict.claim_id)
            confirmed = (
                f"the forward pass looked for this claim in "
                f"{run.display(MERGED)} and did not find it"
            )
            if verdict.rationale:
                confirmed += f" -- {verdict.rationale}"
            out += [
                f'<article class="card warn" data-filterable '
                f'data-claim-id="{esc(verdict.claim_id)}" data-kind="review_queue">',
                f'<div class="head">{esc(verdict.claim_id)} '
                f'<span class="mono note">{esc(where)}</span></div>',
                f'<p class="text">{esc(text)}</p>',
                "<dl>",
                "<dt>Left out of</dt>",
                f"<dd><code>{esc(item.segment)}</code></dd>"
                if item and item.segment
                else "<dd>a segment the record did not name</dd>",
                "<dt>The merge's reason</dt>",
                f"<dd>{esc(item.reason)}</dd>"
                if item and item.reason
                else "<dd>none was recorded</dd>",
                "<dt>Confirmed absent</dt>",
                f"<dd>{esc(confirmed)}</dd>",
                "</dl>",
                "</article>",
            ]
    else:
        out.append(
            '<p class="empty">None. Every claim the forward pass found missing is a '
            "finding above, and no declared drop accounts for one.</p>"
        )
    # Before the budget callout, because this one is about whether the run was
    # worth making at all (497).
    if run.mismatch:
        out.append(
            f'<div class="callout"><strong>Possibly not one document.</strong> '
            f"{inline(mismatch_sentence(run))}</div>"
        )
    if run.over_budget:
        out.append(
            f'<div class="callout"><strong>Over budget.</strong> '
            f"{inline(budget_sentence(run))}</div>"
        )
    return out


def declarations_block(run: Run) -> list[str]:
    if not run.declarations:
        return [
            "<p>The merge declared no departures from its sources, which under the "
            "disposition model is itself a claim: every source segment is asserted "
            "to survive into the merge character for character.</p>"
        ]
    confirmed = len([d for d in run.declarations if d.grade == CONFIRMED])
    rejected = len([d for d in run.declarations if d.grade == REJECTED])
    unchecked = len(run.declarations) - confirmed - rejected
    out = [
        f"<p>The merge declared <strong>{len(run.declarations)}</strong> departure(s) "
        f"from its sources. Checking them confirms {confirmed}, rejects {rejected}, "
        f"and leaves {unchecked} unchecked — a declaration is unchecked when no claim "
        f"was drawn from the segment it names <em>and</em> the reconciler's location "
        f"of that text settles nothing about what was declared, and that is not "
        f"agreement.</p>",
        f"<p>Declared loss: {inline(loss_row(run))}.</p>",
        '<div class="scroll"><table>',
        "<thead><tr><th>Segment</th><th>Declared</th><th>The merge's reason</th>"
        "<th>Confirmed?</th><th>On what evidence</th></tr></thead>",
        "<tbody>",
    ]
    for item in run.declarations:
        claims = ", ".join(f"<code>{esc(c)}</code>" for c in item.claims) or (
            '<span class="note">no claim traced to it</span>'
        )
        grade = "ok" if item.grade == CONFIRMED else (
            "bad" if item.grade == REJECTED else "none"
        )
        reason = esc(item.reason) if item.reason else '<span class="note">none '\
                                                     'recorded</span>'
        out.append(
            f"<tr data-filterable data-segment=\"{esc(item.segment)}\">"
            f'<td class="mono">{esc(item.segment)}</td>'
            f"<td>{esc(item.disposition)}</td>"
            f"<td>{reason}</td>"
            f'<td><span class="chip {grade}">{esc(item.grade)}</span></td>'
            f"<td>{esc(item.detail)} ({claims})</td></tr>"
        )
    out += ["</tbody></table></div>"]
    return out


def additions_block(run: Run) -> list[str]:
    """Statements the merge brought from outside the documents.

    Its own section rather than rows in Findings, for the reason the Markdown
    report gives: a declared addition is not a defect, and listing it among
    defects would say that it was. It is also not a finding this tool made --
    nothing here was found, it was declared, and the section exists so a
    reader can do the one thing the tool cannot, which is decide whether each
    statement is true.

    Six columns and none of them a grade. `Claims it covers` is the one this
    module adds over a bare list of declarations, because one statement
    covering a dozen claims and a dozen covering one each give a reader the
    same count and are not the same thing.

    **`Source` is escaped text and never an anchor** (537). A link is an
    invitation, and an invitation rendered by the tool reads as a destination
    the tool has been to -- which is exactly the impression a fabricated
    citation needs in order to do damage. Nothing here fetched, resolved or
    checked any of these strings, so none of them is presented as something
    that resolves. The sentence above the table says so before the reader
    reaches a row, rather than in a footnote they meet afterwards.
    """
    covered = sum(len(run.covering(str(record.get("statement", ""))))
                  for record in run.additions)
    out = [
        f"<p>The merge declared <strong>{len(run.additions)}</strong> statement(s) "
        f"your documents do not contain, covering {covered} claim(s). "
        f"<strong>Nothing here has been checked against your documents</strong>, "
        f"because they are the only thing this tool checks against. Each one is "
        f"the model's own claim, and reviewing it is the reader's job rather than "
        f"the tool's.</p>",
        f"<p>{esc(sourcing_sentence(run))}</p>",
    ]
    corrections = run.corrections
    if corrections:
        out.append(
            f"<p><strong>{len(corrections)}</strong> of them correct(s) something "
            f"a document states. A correction is a departure from your documents, "
            f"so it is also reported as a finding and it moves the exit code: "
            f"nothing here can tell a correction from a corruption, and the "
            f"declaration buys you this row rather than a clean run.</p>")
    out += [
        '<div class="scroll"><table>',
        "<thead><tr><th>Statement</th><th>Corrects</th><th>Basis</th>"
        "<th>Source</th><th>The merge's reason</th>"
        "<th>Claims it covers</th></tr></thead>",
        "<tbody>",
    ]
    for record in run.additions:
        statement = str(record.get("statement", ""))
        corrects = esc(str(record.get("corrects", ""))) or (
            '<span class="note">nothing named</span>')
        # The reader's phrase and never the enum, from `report.BASIS_WORDS`:
        # this table and the page's are one column, and they printed two
        # vocabularies until 544.
        basis = esc(basis_word(str(record.get("basis", "")))) or (
            '<span class="note">none recorded</span>')
        # Plain text, deliberately. An empty cell under `own-knowledge` reads
        # as the answer it is rather than as a field left blank, because a
        # column that makes "no source" look like an omission is a column that
        # pushes the next merge into inventing one.
        source = esc(str(record.get("source", ""))) or (
            '<span class="note">no source</span>')
        reason = esc(str(record.get("reason", ""))) or (
            '<span class="note">none recorded</span>')
        claims = ", ".join(f"<code>{esc(c)}</code>" for c in run.covering(statement)) or (
            '<span class="note">none</span>')
        out.append(
            "<tr data-filterable>"
            f"<td>{esc(statement) or '<span class=\"note\">nothing recorded</span>'}</td>"
            f"<td>{corrects}</td><td>{basis}</td><td>{source}</td>"
            f"<td>{reason}</td><td>{claims}</td></tr>"
        )
    out += ["</tbody></table></div>"]
    return out


def provenance_block(run: Run) -> list[str]:
    """The same rows the Markdown block prints, from `Provenance.rows`."""
    # Labels are this module's prose; values may quote a filename the caller
    # chose, so they get code spans and no emphasis (326).
    out = _rows([(inline(label), code_only(value)) for label, value in
                 run.provenance.rows()])
    for note in run.provenance.notes():
        out.append(f'<div class="callout">{inline(note)}</div>')
    return out


def planned_block(run: Run) -> list[str]:
    out = ["<ul>"]
    out += [f"<li>{esc(step.name)}</li>" for step in run.planned]
    out += [
        "</ul>",
        f"<p><strong>{len(run.planned)} call(s) planned, none made.</strong> The rest "
        f"of the run cannot be counted from here: one verify call covers "
        f"{run.verify_batch} claims, "
        f"and how many claims these documents hold is what the decompose calls above "
        f"were going to find out.</p>",
    ]
    return out


def _document(title: str, body: list[str], toc: list[tuple[str, str]]) -> str:
    """The page. One file, no request to anywhere."""
    nav = "".join(
        f'<li><a href="#{anchor}">{esc(name)}</a></li>' for anchor, name in toc
    )
    return "\n".join([
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(title)}</title>",
        f"<style>{STYLE}</style>",
        "</head>",
        "<body>",
        "<main>",
        f"<h1>{esc(title)}</h1>",
        SLOT,
        *body,
        "</main>",
        f"<script>{SCRIPT}</script>",
        "</body>",
        "</html>",
        "",
    ]).replace("<!--TOC-->", f'<ul class="toc">{nav}</ul>')


def with_download(page: str, *, filename: str = "report.html") -> str:
    """The same page with a control that saves it. Only for a served copy.

    Takes the rendered page rather than the `Run` it came from, because a
    server reads the report back from the file the job wrote (`api.report_html`
    says why: the `Run` is gone once retention forgets the job, and a page
    re-rendered per request would be a second artefact able to differ from the
    one on disk). So the page is the only thing there is to work from, and this
    is a fill rather than a render.

    **The control carries the report rather than pointing at it.** Its `href`
    is a `data:` URL holding `page` itself, so pressing it asks nothing of
    anything: no server, no session, no network. That is not a stylistic
    choice. A served report is sandboxed into an opaque origin, and a request
    a sandboxed document starts is cross-site by definition, so the session
    cookie -- `SameSite=Strict`, which is this server's CSRF defence -- is not
    sent with it. A control that linked to the report's own URL was measured
    answering 401 in a browser whose tab had just loaded that same report.

    What it hands over is `page` exactly: the empty-slot copy, byte for byte,
    which is the copy the command line writes and the copy that opens on a
    machine that never heard of this server. The cost is the page weighing
    itself plus a base64 of itself, and that is the trade -- a control that
    works without a network, for a page about 2.3 times its own size.

    A page with no slot comes back unchanged. That is a job directory written
    by an older version of this tool, which survives an upgrade, and the
    honest answer for it is the page without a control rather than a crash.
    """
    if SLOT not in page:
        return page
    # Not passed through `esc`, and this is the one value on this page that
    # is not: `b64encode` answers in the base64 alphabet, which holds no
    # character `esc` would change. The filename beside it is escaped because
    # it is an argument and could be anything.
    carried = base64.b64encode(page.encode("utf-8")).decode("ascii")
    control = (
        '<p class="toolbar">'
        f'<a class="save" href="data:text/html;charset=utf-8;base64,{carried}" '
        f'download="{esc(filename)}">Download this report</a>'
        '<span class="note">One file, with its stylesheet inside it: it opens '
        "from disk, on a machine that has never heard of this server.</span>"
        "</p>"
    )
    return page.replace(SLOT, control, 1)


def render(run: Run) -> str:
    """The whole report as one HTML document, in the order `report.render` uses."""
    documents = ", ".join(
        run.display(name) for name in sorted(run.paths)
    ) or "no document"
    title = f"LLossless {run.command} — {documents}"

    if run.planned:
        body = _section("planned", "Planned calls", planned_block(run))
        if run.provenance is not None:
            body += _section("provenance", "Provenance", provenance_block(run))
        return _document(title, body, [])

    toc = [("verdict", "Verdict"), ("coverage", "Coverage"),
           ("findings", "Findings"), ("inventory", "Inventory")]
    body = [
        *verdict_block(run),
        "<!--TOC-->",
        '<div class="filter">',
        '<label for="filter">Filter claims and findings</label>',
        '<input id="filter" type="search" autocomplete="off" '
        'placeholder="type to narrow the tables and cards below">',
        '<p class="note" id="filter-count"></p>',
        "</div>",
        *_section("coverage", "Coverage", coverage_block(run)),
        *_section("findings", "Findings", findings_block(run)),
    ]
    # `report.render`'s order and its condition: after Findings, on either
    # command, and only when the merge misattributed something (569).
    if run.attributions:
        toc.insert(3, ("attributions", "Attributions"))
        body += _section("attributions", "Attributions", attributions_block(run))
    # The same order and condition again, for the number format (601).
    if run.number_format:
        toc.insert(3 + bool(run.attributions), ("numbers", "Number format"))
        body += _section("numbers", "Number format", number_format_block(run))
    body += _section("inventory", "Inventory", inventory_block(run))
    if run.command == "merge" and run.merged is not None:
        toc += [("structure", "Structure"), ("queue", "Review queue"),
                ("declarations", "Declarations")]
        body += [
            *_section("structure", "Structure", structural_block(run)),
            *_section("queue", "Review queue", queue_block(run)),
            *_section("declarations", "Declarations", declarations_block(run)),
        ]
        # Only where there is something to show. Every other section stays up
        # saying nothing was found; this one is not a check, and at a level
        # permitting no additions its absence leaves no question open.
        if run.additions:
            toc.append(("additions", "Added from outside"))
            body += _section("additions", "Added from outside",
                             additions_block(run))
    if run.provenance is not None:
        toc.append(("provenance", "Provenance"))
        body += _section("provenance", "Provenance", provenance_block(run))
    # The merged document itself, only where the Markdown report carries it:
    # when nothing wrote it to a file, so this page is the only copy.
    if run.merged is not None and run.merged_written_to is None:
        toc.append(("merged", "Merged document"))
        body += _section(
            "merged", "Merged document",
            [f'<pre class="document">{esc(run.merged.rstrip())}</pre>'],
        )
    return _document(title, body, toc)


def attributions_block(run: Run) -> list[str]:
    """The Attributions section as HTML cards, from the Markdown rows (569).

    At the foot of the module, and importing its one constant here rather
    than at the top, so that no line another file cites in this one moves.
    """
    from .report import ATTRIBUTIONS_NOTE

    out = [f"<p>{esc(ATTRIBUTIONS_NOTE)}</p>"]
    for finding in run.attributions:
        where = (f"<code>{esc(finding.segment)}</code> "
                 f"(<code>{esc(run.display(finding.document))}</code>)")
        stack = stacked_lines(finding)
        evidence = (f'<pre class="stack">{esc(chr(10).join(stack))}</pre>'
                    if stack else "")
        out.append(
            f'<article class="card bad" data-filterable '
            f'data-kind="{esc(finding.kind)}">'
            f'<div class="head">{where}</div>'
            f'<p class="text">{esc(finding.detail)}</p>{evidence}</article>'
        )
    return out


def number_format_block(run: Run) -> list[str]:
    """The Number format section as HTML: the conventions table, then cards.

    The Markdown section's note, table columns and row words, imported here
    for the reason `attributions_block` imports its note: one wording.
    """
    from .numerals import FAULTS, NAMES
    from .report import _NUMBER_KIND_WORDS, NUMBER_FORMAT_NOTE

    out = [f"<p>{esc(NUMBER_FORMAT_NOTE)}</p>", "<table>",
           "<thead><tr><th>document</th><th>convention</th><th>decided by</th>"
           "<th>votes, decimal point</th><th>votes, decimal comma</th>"
           "<th>language (stop words en / de)</th></tr></thead><tbody>"]
    for convention in run.conventions:
        language = {"en": "English", "de": "German"}.get(convention.language,
                                                         "unknown")
        out.append(
            f"<tr><td><code>{esc(run.display(convention.document))}</code></td>"
            f"<td>{esc(NAMES.get(convention.convention, 'none'))}</td>"
            f"<td>{esc(convention.decided_by)}</td>"
            f"<td>{esc(', '.join(convention.point_votes) or 'none')}</td>"
            f"<td>{esc(', '.join(convention.comma_votes) or 'none')}</td>"
            f"<td>{esc(language)} ({convention.english_words} / "
            f"{convention.german_words})</td></tr>")
    out.append("</tbody></table>")
    for finding in sorted(run.number_format, key=lambda f: f.kind not in FAULTS):
        where = (f"<code>{esc(finding.segment)}</code> "
                 f"(<code>{esc(run.display(finding.document))}</code>)")
        stack = stacked_lines(finding) if finding.merge_text else []
        evidence = (f'<pre class="stack">{esc(chr(10).join(stack))}</pre>'
                    if stack else "")
        tone = "bad" if finding.kind in FAULTS else "warn"
        out.append(
            f'<article class="card {tone}" data-filterable '
            f'data-kind="{esc(finding.kind)}">'
            f'<div class="head"><strong>{esc(_NUMBER_KIND_WORDS[finding.kind])}'
            f'</strong> {where}</div>'
            f'<p class="text">{esc(finding.detail)}</p>{evidence}</article>'
        )
    return out
