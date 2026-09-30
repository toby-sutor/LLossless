#!/usr/bin/env python3
"""The colour theme (redesign option A): three modes, no flash, AA contrast.

`static/theme.js` and `static/theme.css` are the whole of the look, layered
over `app.css`, which is untouched and still shares the report's palette.
What this module holds is what a source read can hold, each with a seeded
probe beside it:

**the toggle.** The choice is kept under `localStorage["llossless.theme"]`,
every storage access is inside a `try`, the three modes are System, Light and
Dark, and the markup carries one button for each.

**no flash.** `theme.js` is a classic script in `<head>`, before the first
stylesheet and without `defer`, `async` or `type="module"`, and it applies the
stored mode at top level rather than on a DOM event. A script that waited for
`DOMContentLoaded` would paint the page in the wrong theme first.

**both themes, the same tokens.** "System" is `prefers-color-scheme`; "Dark"
is `data-theme="dark"`. The two dark blocks must be the same values, or the
page looks different depending on how dark was reached.

**contrast.** Every text-on-background pair the stylesheet paints is WCAG AA,
4.5:1, and every UI boundary and state marker 3:1, in both themes. The pairs
are listed below by hand; `CONTRAST_PAIRS` is the table the report quotes.

Measured in a browser as well (Chromium, 1280/1024/800/380, English and
German): the pinned header row keeps one height per width across languages,
System follows the OS live, a stored Dark is on `<html>` by
`DOMContentLoaded`, and the page works with storage blocked. That is
tracked separately; this is the part a file read can hold.

Run with `python3 tests/test_web_theme.py`, or collect with pytest.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import socket_guard  # noqa: E402

# Reads files off disk and opens nothing; the guard is installed anyway, in
# the shape `tests/test_socket_guard.py` scans every module for.
socket_guard.install()

STATIC = ROOT / "src" / "llossless" / "web" / "static"
INDEX = STATIC / "index.html"
THEME_JS = STATIC / "theme.js"
THEME_CSS = STATIC / "theme.css"
LOCALES = ROOT / "src" / "llossless" / "web" / "locales"

KEY = "llossless.theme"
MODES = ("system", "light", "dark")

failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


def source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_css_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def strip_js_comments(js: str) -> str:
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    return re.sub(r"(?m)^\s*//.*$", "", js)


# --------------------------------------------------------------------------
# the toggle and the no-flash hook
# --------------------------------------------------------------------------

def toggle_problems(js: str, html: str) -> list[str]:
    """Every way the three-mode toggle is not the one this page promises."""
    found = []
    code = strip_js_comments(js)
    if f'"{KEY}"' not in code:
        found.append(f"theme.js does not use the storage key {KEY!r}")
    for mode in MODES:
        if f'"{mode}"' not in code:
            found.append(f"theme.js does not know the mode {mode!r}")
        if not re.search(rf'<button[^>]*data-theme-choice="{mode}"', html):
            found.append(f"index.html has no button for {mode!r}")
    # Every storage access inside a try: the page must work without storage.
    accesses = len(re.findall(r"localStorage\.(?:getItem|setItem|removeItem)", code))
    guarded = len(re.findall(r"try\s*\{[^{}]*localStorage\.(?:getItem|setItem|removeItem)", code))
    if accesses == 0:
        found.append("theme.js never reads or writes storage")
    if guarded != accesses:
        found.append(f"{accesses - guarded} storage access(es) in theme.js are outside a try")
    # System is the default when nothing, or nothing valid, is stored.
    if not re.search(r'return\s+"system"', code):
        found.append("theme.js has no fallback to System")
    return found


def no_flash_problems(js: str, html: str) -> list[str]:
    """Every way the stored theme could reach the page after first paint."""
    found = []
    head = html.split("</head>", 1)[0]
    tag = re.search(r'<script\s+src="theme\.js"([^>]*)>\s*</script>', head)
    if not tag:
        return ["index.html does not load theme.js in <head>"]
    for attribute in ("defer", "async", "module"):
        if attribute in tag.group(1):
            found.append(f"theme.js is loaded with {attribute!r}, so it runs after first paint")
    first_sheet = head.find('rel="stylesheet"')
    if first_sheet < 0 or tag.start() > first_sheet:
        found.append("theme.js is not loaded before the first stylesheet")
    app = head.find('href="app.css"')
    theme = head.find('href="theme.css"')
    if theme < 0 or theme < app:
        found.append("theme.css is not linked after app.css")
    # Applied at top level, not only inside the DOMContentLoaded handler.
    code = strip_js_comments(js)
    body = code.split("function wire()", 1)[0]
    if not re.search(r"^\s*apply\(stored\(\)\);", body, re.M):
        found.append("theme.js does not apply the stored mode before the DOM is ready")
    return found


def test_the_toggle_has_three_modes_a_key_and_guarded_storage() -> None:
    for problem in toggle_problems(source(THEME_JS), source(INDEX)):
        check(False, problem)


def test_the_toggle_check_fires() -> None:
    js, html = source(THEME_JS), source(INDEX)
    seeds = (
        ("another key", js.replace(f'"{KEY}"', '"theme"'), html),
        ("no dark mode", js.replace('"dark"', '"night"'), html),
        ("no light button", js, html.replace('data-theme-choice="light"', 'data-theme-choice="day"')),
        ("storage outside a try", js + '\nwindow.localStorage.getItem("x");\n', html),
    )
    for what, seeded_js, seeded_html in seeds:
        check((seeded_js, seeded_html) != (js, html), f"the toggle probe's anchor has moved: {what}")
        check(bool(toggle_problems(seeded_js, seeded_html)), f"a broken toggle is not caught: {what}")


def test_the_theme_is_applied_before_first_paint() -> None:
    for problem in no_flash_problems(source(THEME_JS), source(INDEX)):
        check(False, problem)


def test_the_no_flash_check_fires() -> None:
    js, html = source(THEME_JS), source(INDEX)
    seeds = (
        ("deferred", js, html.replace('<script src="theme.js"></script>',
                                      '<script src="theme.js" defer></script>')),
        ("after the stylesheets", js, html.replace('<script src="theme.js"></script>\n', "")
         .replace('<link rel="stylesheet" href="theme.css">',
                  '<link rel="stylesheet" href="theme.css">\n<script src="theme.js"></script>')),
        ("applied only on DOMContentLoaded", js.replace("  // Before first paint.\n  apply(stored());\n", ""), html),
    )
    for what, seeded_js, seeded_html in seeds:
        check((seeded_js, seeded_html) != (js, html), f"the no-flash probe's anchor has moved: {what}")
        check(bool(no_flash_problems(seeded_js, seeded_html)), f"a flash is not caught: {what}")


# --------------------------------------------------------------------------
# tokens and contrast
# --------------------------------------------------------------------------

def blocks(css: str) -> dict[str, dict[str, str]]:
    """The light tokens, the System-dark tokens and the pinned-dark tokens."""
    css = strip_css_comments(css)

    def read(body: str) -> dict[str, str]:
        return dict(re.findall(r"(--[a-z0-9-]+):\s*(#[0-9a-fA-F]{6})\s*;", body))

    light = re.search(r':root,\s*:root\[data-theme="light"\]\s*\{(.*?)\}', css, re.S)
    system = re.search(r'@media \(prefers-color-scheme: dark\)\s*\{\s*'
                       r':root:not\(\[data-theme="light"\]\)\s*\{(.*?)\}', css, re.S)
    pinned = re.search(r'^:root\[data-theme="dark"\]\s*\{(.*?)\}', css, re.S | re.M)
    base = read(light.group(1)) if light else {}
    return {
        "light": base,
        "system-dark": {**base, **read(system.group(1))} if system else {},
        "dark": {**base, **read(pinned.group(1))} if pinned else {},
    }


def contrast(one: str, two: str) -> float:
    """WCAG 2 contrast ratio of two #rrggbb colours."""
    def lum(colour: str) -> float:
        parts = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        parts = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in parts]
        return 0.2126 * parts[0] + 0.7152 * parts[1] + 0.0722 * parts[2]
    high, low = sorted((lum(one), lum(two)), reverse=True)
    return (high + 0.05) / (low + 0.05)


TEXT, UI = 4.5, 3.0

# (foreground, background, minimum, where it is painted)
CONTRAST_PAIRS: tuple[tuple[str, str, float, str], ...] = (
    ("--ink", "--bg", TEXT, "page text"),
    ("--ink", "--surface", TEXT, "card and sheet text"),
    ("--ink", "--panel", TEXT, "panel, table header, document"),
    ("--ink", "--field", TEXT, "input text"),
    ("--ink", "--accent-bg", TEXT, "selected tab, radio"),
    ("--ink", "--ok-bg", TEXT, "clean banner text, good cell"),
    ("--ink", "--warn-bg", TEXT, "warning banner text, fair cell"),
    ("--ink", "--bad-bg", TEXT, "findings banner text, poor cell"),
    ("--ink", "--none-bg", TEXT, "neutral banner text"),
    ("--ink-soft", "--bg", TEXT, "tagline, hints on the page"),
    ("--ink-soft", "--surface", TEXT, "hints in cards"),
    ("--ink-soft", "--panel", TEXT, "hints in panels, table headers"),
    ("--ink-soft", "--field", TEXT, "theme icons"),
    ("--accent", "--surface", TEXT, "card index, busy status word, route badge"),
    ("--accent", "--panel", TEXT, "route badge in a hovered row"),
    ("--accent", "--accent-bg", TEXT, "accent text on a selected tint"),
    ("--accent-ink", "--accent-fill", TEXT, "primary button, pressed theme button"),
    ("--ok", "--ok-bg", TEXT, "clean chip, band word"),
    ("--ok", "--surface", TEXT, "clean tile note"),
    ("--ok", "--panel", TEXT, "clean status word in a panel"),
    ("--warn", "--warn-bg", TEXT, "findings chip, metered badge"),
    ("--warn", "--surface", TEXT, "warning hint, tile note"),
    ("--warn", "--panel", TEXT, "warning hint in a panel"),
    ("--warn", "--bg", TEXT, "metered badge on the page"),
    ("--bad", "--bad-bg", TEXT, "bad chip, band word, danger hover"),
    ("--bad", "--surface", TEXT, "Cancel run, Start over, refusal"),
    ("--bad", "--panel", TEXT, "danger text in a panel"),
    ("--none", "--none-bg", TEXT, "not-checked chip"),
    ("--none", "--surface", TEXT, "neutral status word"),
    ("--bad-fill-ink", "--bad-fill", TEXT, "destructive confirm button"),
    ("--console-ink", "--console-bg", TEXT, "log message"),
    ("--console-ink", "--console-raise", TEXT, "run header value"),
    ("--console-soft", "--console-bg", TEXT, "log timing"),
    ("--console-soft", "--console-raise", TEXT, "run header label"),
    ("--console-info", "--console-bg", TEXT, "INFO chip (step, state)"),
    ("--console-ok", "--console-bg", TEXT, "done chip"),
    ("--console-warn", "--console-bg", TEXT, "WARN chip (warn, notice)"),
    ("--console-bad", "--console-bg", TEXT, "ERROR chip (failed)"),
    ("--line-strong", "--surface", UI, "input and button borders"),
    ("--line-strong", "--field", UI, "theme and pill track"),
    ("--line-strong", "--bg", UI, "pill border on the bar"),
    ("--focus", "--bg", UI, "focus ring on the page"),
    ("--focus", "--surface", UI, "focus ring in a card"),
    ("--focus", "--panel", UI, "focus ring in a panel"),
    ("--accent", "--field", UI, "pressed theme button ring"),
    ("--accent", "--surface", UI, "selected tab and radio border"),
    ("--ok", "--field", UI, "Ready dot and border"),
    ("--warn", "--field", UI, "No endpoint dot and border"),
    ("--bad", "--field", UI, "Server error dot and border"),
    ("--bad", "--surface", UI, "danger button outline"),
    # The workbench: the step tabs' state lines and numbers, the way to
    # a blocking step, and the empty output state.
    ("--ink-soft", "--accent-bg", TEXT, "state line in the selected step tab"),
    ("--warn", "--accent-bg", TEXT, "attention state in the selected step tab"),
    ("--ok", "--field", UI, "done step number"),
    ("--warn", "--field", UI, "attention step number"),
    ("--line-strong", "--field", UI, "step number ring"),
    # The subscription badge: its words on its own fill, and its border
    # against the card and the hovered row it sits in.
    ("--plan", "--plan-bg", TEXT, "subscription badge text on its fill"),
    ("--plan", "--surface", UI, "subscription badge border in a card"),
    ("--plan", "--panel", UI, "subscription badge border in a hovered row"),
    ("--plan", "--bg", UI, "subscription badge border on the page"),
)


def contrast_table(css: str) -> list[tuple[str, str, str, float, float, str]]:
    """One row per theme and pair: theme, fg, bg, ratio, minimum, where."""
    rows = []
    for theme, tokens in blocks(css).items():
        for fg, bg, minimum, where in CONTRAST_PAIRS:
            if fg not in tokens or bg not in tokens:
                rows.append((theme, fg, bg, 0.0, minimum, where + " (token missing)"))
                continue
            rows.append((theme, fg, bg, round(contrast(tokens[fg], tokens[bg]), 2), minimum, where))
    return rows


def contrast_problems(css: str) -> list[str]:
    found = []
    tokens = blocks(css)
    for theme in ("light", "system-dark", "dark"):
        if len(tokens[theme]) < 30:
            found.append(f"only {len(tokens[theme])} tokens parsed for {theme}; the parse has drifted")
    if tokens["system-dark"] != tokens["dark"]:
        differ = sorted(k for k in set(tokens["dark"]) | set(tokens["system-dark"])
                        if tokens["dark"].get(k) != tokens["system-dark"].get(k))
        found.append(f"System-dark and pinned Dark differ on {differ}")
    for theme, fg, bg, ratio, minimum, where in contrast_table(css):
        if ratio < minimum:
            found.append(f"{theme}: {fg} on {bg} is {ratio}:1, under {minimum}:1 ({where})")
    return found


def test_every_pair_is_aa_in_both_themes() -> None:
    for problem in contrast_problems(source(THEME_CSS)):
        check(False, problem)


def test_the_contrast_check_fires() -> None:
    css = source(THEME_CSS)
    seeds = (
        ("a pale hint in light", "--ink-soft: #52575e;", "--ink-soft: #a0a4aa;"),
        ("the two dark blocks drift", "  --ok: #62d08a;\n  --ok-bg: #13291b;\n  --warn: #ff9d5c;\n  --warn-bg: #33200f;\n  --bad: #ff8a80;\n  --bad-bg: #3a1917;\n  --bad-fill: #c8302a;\n  --bad-fill-ink: #ffffff;\n  --none: #a6abb1;\n  --none-bg: #252a2f;\n\n  --console-bg: #0a0b0d;\n  --console-raise: #15181b;\n  --console-line: #24282d;\n\n  --shadow: 0 1px 2px rgba(0, 0, 0, .45), 0 8px 24px rgba(0, 0, 0, .35);\n}",
         "  --ok: #2a6b40;\n  --ok-bg: #13291b;\n  --warn: #ff9d5c;\n  --warn-bg: #33200f;\n  --bad: #ff8a80;\n  --bad-bg: #3a1917;\n  --bad-fill: #c8302a;\n  --bad-fill-ink: #ffffff;\n  --none: #a6abb1;\n  --none-bg: #252a2f;\n\n  --console-bg: #0a0b0d;\n  --console-raise: #15181b;\n  --console-line: #24282d;\n\n  --shadow: 0 1px 2px rgba(0, 0, 0, .45), 0 8px 24px rgba(0, 0, 0, .35);\n}"),
        ("an amber focus ring on white", "  --focus: #8f5200;", "  --focus: #f2a516;"),
    )
    for what, anchor, replacement in seeds:
        seeded = css.replace(anchor, replacement)
        check(seeded != css, f"the contrast probe's anchor has moved: {what}")
        check(bool(contrast_problems(seeded)), f"a contrast failure is not caught: {what}")


BADGE_RULE = re.compile(r"table\.models \.route-badge\.subscription,\s*"
                        r"table\.models \.route-badge\.command\s*\{([^}]*)\}")


def badge_problems(css: str) -> list[str]:
    """The subscription badge is the blue plan colour, not the amber."""
    rules = BADGE_RULE.findall(strip_css_comments(css))
    if not rules:
        return ["theme.css has no rule for the subscription badge"]
    body = rules[-1]
    found = [f"the subscription badge has no {want!r}"
             for want in ("color: var(--plan)", "background: var(--plan-bg)",
                          "border-color: var(--plan)") if want not in body]
    for amber in ("--accent", "--warn"):
        if f"var({amber}" in body:
            found.append(f"the subscription badge still paints with {amber}, "
                         f"the amber a metered route owns")
    return found


def test_the_subscription_badge_is_blue_and_not_amber() -> None:
    """Must not fire as shipped; must fire on the old amber rule."""
    css = source(THEME_CSS)
    for problem in badge_problems(css):
        check(False, problem)
    seeded = css.replace(
        "  border-color: var(--plan); color: var(--plan); background: var(--plan-bg);",
        "  border-color: var(--accent); color: var(--accent);")
    check(seeded != css, "the badge probe's anchor has moved")
    check(bool(badge_problems(seeded)), "an amber subscription badge is not caught")
    seeded = css.replace("  --plan-bg: #e6f0fb;", "  --plan-bg: #6f9fd6;")
    check(seeded != css and bool(contrast_problems(seeded)),
          "a plan fill too dark for its text is not caught")


def test_the_new_strings_are_in_both_catalogues() -> None:
    """Every theme and pill key in English and German, and none left English."""
    import json
    keys = ("theme.label", "theme.system", "theme.light", "theme.dark", "pill.loading",
            "pill.ready", "pill.empty", "pill.signedout", "pill.unreachable")
    en = json.loads(source(LOCALES / "en.json"))["strings"]
    de = json.loads(source(LOCALES / "de.json"))["strings"]
    for key in keys:
        check(bool(en.get(key)) and bool(de.get(key)), f"{key} is missing from a catalogue")
    check(de.get("theme.light") != en.get("theme.light"), "the German Light label is English")
    check(de.get("pill.empty") != en.get("pill.empty"), "the German pill is English")


def print_table() -> None:
    for theme, fg, bg, ratio, minimum, where in contrast_table(source(THEME_CSS)):
        mark = "ok" if ratio >= minimum else "FAIL"
        print(f"{theme:12} {fg:16} {bg:16} {ratio:6.2f} >= {minimum:.1f} {mark:4} {where}")


def main() -> int:
    if "--table" in sys.argv:
        print_table()
        return 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and name != "test_web_theme" and callable(function):
            function()
    if failures:
        print(f"web theme: {len(failures)} of {checks} checks failed")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    rows = contrast_table(source(THEME_CSS))
    print(f"web theme: {checks} checks pass; {len(rows)} contrast pairs AA "
          f"(lowest {min(r[3] for r in rows):.2f}:1)")
    return 0


def test_web_theme() -> None:
    """pytest entry point."""
    assert main() == 0, "\n".join(failures)


if __name__ == "__main__":
    sys.exit(main())
