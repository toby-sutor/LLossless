// @ts-check
/* LLossless, the colour theme: System (the default), Light or Dark.
 *
 * A classic script, loaded in <head> before the stylesheets and without
 * `defer`, `async` or `type="module"`: it runs before first paint, so a page
 * pinned to dark never flashes light on load. The CSP is `script-src 'self'`,
 * which forbids an inline script, so this is a file of its own.
 *
 * The choice is kept under `localStorage["llossless.theme"]`. Every storage
 * access is wrapped: a private window, blocked site data or a browser with no
 * storage leaves the page on System and the buttons still work for the visit.
 *
 * "System" is the absence of `data-theme` on <html>; `theme.css` then follows
 * `prefers-color-scheme` live. "light" and "dark" set the attribute.
 *
 * The three buttons are `[data-theme-choice]` in the top bar. Their names are
 * visually hidden `data-t` spans that `app.js` fills from the catalogue like
 * every other string; this file never writes a sentence.
 */
(function () {
  "use strict";

  var KEY = "llossless.theme";
  var MODES = ["system", "light", "dark"];

  /** @returns {string} */
  function stored() {
    try {
      var value = window.localStorage.getItem(KEY);
      return value && MODES.indexOf(value) >= 0 ? value : "system";
    } catch (_) {
      return "system";
    }
  }

  /** @param {string} mode */
  function remember(mode) {
    try {
      window.localStorage.setItem(KEY, mode);
    } catch (_) {
      // No storage: the choice holds for this page only.
    }
  }

  /** @param {string} mode */
  function apply(mode) {
    var root = document.documentElement;
    if (mode === "light" || mode === "dark") {
      root.setAttribute("data-theme", mode);
    } else {
      root.removeAttribute("data-theme");
    }
    var buttons = document.querySelectorAll("[data-theme-choice]");
    for (var i = 0; i < buttons.length; i += 1) {
      var button = buttons[i];
      button.setAttribute("aria-pressed",
        button.getAttribute("data-theme-choice") === mode ? "true" : "false");
    }
  }

  // Before first paint.
  apply(stored());

  function wire() {
    var buttons = document.querySelectorAll("[data-theme-choice]");
    for (var i = 0; i < buttons.length; i += 1) {
      var button = /** @type {HTMLElement} */ (buttons[i]);
      button.addEventListener("click", function (event) {
        var target = /** @type {HTMLElement} */ (event.currentTarget);
        var mode = target.getAttribute("data-theme-choice") || "system";
        if (MODES.indexOf(mode) < 0) mode = "system";
        remember(mode);
        apply(mode);
      });
      // A pointer gets the name as a tooltip, in whatever language the page
      // is in at that moment: the hidden label is the one source of it.
      button.addEventListener("pointerenter", function (event) {
        var target = /** @type {HTMLElement} */ (event.currentTarget);
        var label = target.querySelector(".visually-hidden");
        if (label) target.title = String(label.textContent || "").trim();
      });
    }
    apply(stored());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
