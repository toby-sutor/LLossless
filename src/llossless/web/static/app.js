// @ts-check
/**
 * LLossless's interface. One file, no build step, no dependency.
 *
 * Three rules govern everything below, and each is enforced by a check in
 * `tests/test_web_static.py` rather than left as a habit:
 *
 * **Nothing about the engine is written down twice.** The fidelity levels, the
 * title policies, the model catalogue and the limits are read from
 * `GET /api/v1/config` and rendered from what came back. A list spelled out
 * here would keep rendering the day the server's own list changed, and would
 * do it silently -- the page would look right and be wrong.
 *
 * **Nothing from a document or a model is ever assigned as markup.** Every
 * value that came out of an upload, a model or a report reaches the page
 * through `textContent`. There is no `innerHTML` in this file and the test
 * greps for one, because `html_report.py` treats escaping as a security
 * property and this page renders the same material.
 *
 * **An unchecked check is not a passed check.** `structural.ran` and
 * `decisions.ran` are booleans, and an empty findings list underneath a false
 * one means nobody looked. That renders as "not checked" in the neutral
 * colour, never as a green all-clear; `sectionState` is the one place the
 * distinction is made and everything that shows a chip goes through it.
 */

/* ------------------------------------------------------------------ */
/* the API                                                             */
/* ------------------------------------------------------------------ */

/**
 * Every path this page knows, and the only place one is written.
 *
 * `{id}` and `{name}` are filled by `route()`. A table rather than string
 * concatenation at nine call sites so that the set can be checked against the
 * server's own routing table: `tests/test_web_static.py` asks a live server
 * for each of these and fails on the one that answers `no_route`.
 *
 * `keys` and `key` are W7's and may not be mounted yet. They are named here
 * anyway -- a path discovered at runtime is a path no test can enumerate --
 * and `loadProviders` treats a 404 on them as "this server has no credential
 * endpoint", which is a state the page renders rather than an error.
 *
 * The four account routes are the same shape. A server built with no account
 * store answers `no_account_store` on them, which the page renders as "this
 * server has nobody to be signed in as" rather than as an error: it is the
 * single-tenant arrangement, and it is a state.
 */
const ROUTES = {
  health: "/api/v1/health",
  config: "/api/v1/config",
  locales: "/api/v1/locales",
  locale: "/api/v1/locales/{tag}",
  runs: "/api/v1/runs",
  run: "/api/v1/runs/{id}",
  events: "/api/v1/runs/{id}/events",
  cancel: "/api/v1/runs/{id}/cancel",
  retry: "/api/v1/runs/{id}/retry",
  merged: "/api/v1/runs/{id}/merged",
  report: "/api/v1/runs/{id}/report.html",
  reportPage: "/api/v1/runs/{id}/report",
  bundle: "/api/v1/runs/{id}/bundle.zip",
  keys: "/api/v1/settings/keys",
  key: "/api/v1/settings/keys/{name}",
  endpoint: "/api/v1/settings/endpoints/{name}",
  commandTool: "/api/v1/settings/commands/{name}",
  session: "/api/v1/session",
  setup: "/api/v1/setup",
  accounts: "/api/v1/accounts",
  account: "/api/v1/accounts/{name}",
  password: "/api/v1/accounts/{name}/password",
  defaults: "/api/v1/defaults",
};

/**
 * One route, with its placeholders filled.
 * @param {string} template one of `ROUTES`
 * @param {Record<string, string>} [values]
 * @returns {string}
 */
function route(template, values) {
  let out = template;
  for (const [key, value] of Object.entries(values || {})) {
    out = out.split("{" + key + "}").join(encodeURIComponent(value));
  }
  return out;
}

/**
 * The nine event kinds `web/events.py` can emit.
 *
 * Listed because `EventSource` dispatches a named event only to a listener
 * registered for that name: a kind with no listener is dropped by the browser
 * in silence, which is the one failure a progress stream must not have. The
 * list is not served by `/config`, so the test asserts it equals
 * `events.KINDS` instead -- a kind added there and not here would go dark.
 */
const EVENT_KINDS = ["step", "done", "failed", "skipped", "detail", "warn",
                     "notice", "banner", "state"];

/**
 * Which findings a forward verdict can carry, in `report.FORWARD_STATUS`'s
 * order.
 *
 * The *words* are in the catalogues, under `status.forward.<finding>`, because
 * they are sentences an operator reads and this page speaks two languages.
 * What stays here is the membership question -- is this finding one the
 * forward direction defines -- which is not a string and does not translate:
 * a finding outside the list is one this page has never been told about, and
 * it reads "not checked" rather than rendering a key. `tests/test_web_i18n.py`
 * asserts this list against `report.FORWARD_STATUS`'s keys and asserts the
 * English catalogue's values against its values, so the two halves of what
 * used to be one table are still pinned to the report's own vocabulary.
 */
const FORWARD_FINDINGS = ["none", "partially_dropped", "dropped", "contradicted"];

/** The same, for a reverse verdict. Mirrored from `report.REVERSE_STATUS`. */
const REVERSE_FINDINGS = ["none", "partially_invented", "hallucinated",
                          "contradicted"];

/**
 * Which of the two sections a verdict finding belongs under, and which a
 * structural finding does. Every finding class the engine can produce is in
 * exactly one list: the test asserts the union against `report.FINDING_ORDER`
 * and `reconcile.FINDING_KINDS` and asserts the pairs disjoint, so a class
 * added to the engine fails here rather than rendering nowhere.
 */
/**
 * The one document name the engine owns rather than the caller.
 *
 * `segment.MERGED_NAME`, and `tests/test_web_static.py` asserts the two are
 * the same string -- every other name on a report is whatever the submitter
 * called their upload, and this one is the merge, which nobody uploaded. The
 * page needs it to answer "which document was this verdict judged against":
 * `report.documents` holds the sources and the merge is the rest.
 */
const MERGED_DOCUMENT = "merged.md";

const OMITTED_FINDINGS = ["dropped", "partially_dropped"];
const CONFLICT_FINDINGS = ["contradicted", "hallucinated", "partially_invented"];
const OMITTED_KINDS = ["undeclared_absence", "false_departure", "title_not_superseded"];
const CONFLICT_KINDS = ["undeclared_rewording", "invented_segment",
                        "unresolved_replacement", "disposition_not_permitted",
                        "verbatim_violation", "declared_loss_over_budget",
                        "title_not_from_source", "duplicated_content",
                        "prompt_example_leak"];
/**
 * The finding kinds with a section of their own, outside the partition above.
 *
 * `reconcile.MISATTRIBUTED` (572). It is deliberately not one of the
 * reconciler's `FINDING_KINDS` -- it reads no disposition record and is not
 * one of the nine checks -- and the report gives it an **Attributions**
 * section of its own on both commands. The page does the same rather than
 * filing it under Conflicts: the row's source field names the document the
 * merge *credited*, which is the one that does not carry the sentence, and in
 * a list of conflicts a named source reads as where the text came from.
 * `tests/test_web_static.py` holds this list to the engine's constant.
 */
const ATTRIBUTION_KINDS = ["misattributed"];
// The number format's five kinds (601, and a document against its language).
// Which of them moved the exit code is read from the report's own
// `number_format.faults`, never restated here.
const NUMBER_KINDS = ["other_convention", "readable_two_ways",
                      "reading_changed", "reading_resolved", "against_language"];
/** @type {Record<string, string>} how a document's convention was decided */
const DECIDED_BY = {
  votes: "numbers.decided.votes", language: "numbers.decided.language",
  majority: "numbers.decided.majority", none: "numbers.decided.none",
};

/* ------------------------------------------------------------------ */
/* the strings                                                         */
/* ------------------------------------------------------------------ */

/**
 * Every word this page says, fetched before anything renders.
 *
 * The table that used to be here is `web/locales/en.json`, byte for byte the
 * same strings, and `de.json` beside it. Moving it out is the whole of the
 * localisation: a sentence built at a call site is a sentence no translator
 * will ever see, so the precondition for a second language was that every
 * sentence already had a key -- and once they all do, the table is data and
 * the only question left is which file to read.
 *
 * Empty until `loadLocale` fills it. Keys that name a piece of static
 * furniture are also carried in `index.html` as `data-t` **with their English
 * text**, and `tests/test_web_static.py` asserts the two copies say the same
 * thing, so a page whose script or whose catalogue never arrives still reads
 * -- in English, which is the reference language and the one the markup can
 * honestly claim to be in.
 * @type {Record<string, string>}
 */
let strings = {};

/**
 * Which catalogue is on the page, and what the server has.
 * @type {{tag: string, available: Array<{tag: string, label: string}>}}
 */
const locale = { tag: "", available: [] };

/**
 * Where an explicit choice is kept, and the reason it is kept at all.
 *
 * `Accept-Language` is what the browser was configured with, which is
 * frequently not what the person in front of it wants this one tool in: a
 * German speaker on an English-configured work laptop is the ordinary case,
 * not the exotic one. So an explicit choice wins and is remembered, and the
 * header decides only for somebody who never expressed one.
 *
 * `localStorage` rather than a cookie: nothing here is sent to the server on
 * every request, and the choice is a property of this browser rather than of
 * this session. It is read through a `try` because a browser can refuse
 * storage entirely -- private mode, a blocked third-party context, a policy --
 * and a page that threw on boot because it could not remember a language
 * preference would be a page that does not load over a setting.
 */
const LOCALE_STORAGE_KEY = "llossless.locale";

/** The tag this browser was told to use, or "" for "ask the server". */
function storedLocale() {
  try {
    return window.localStorage.getItem(LOCALE_STORAGE_KEY) || "";
  } catch (error) {
    return "";
  }
}

/**
 * Remember an explicit choice, or forget it. Never fatal.
 * @param {string} tag
 */
function rememberLocale(tag) {
  try {
    if (tag) window.localStorage.setItem(LOCALE_STORAGE_KEY, tag);
    else window.localStorage.removeItem(LOCALE_STORAGE_KEY);
  } catch (error) {
    // A browser that will not store the choice still renders it for this
    // page load. Nothing above here needs to know.
  }
}

/**
 * Fetch one catalogue and make it the page's.
 *
 * An empty `tag` asks the server to negotiate from `Accept-Language`; a tag
 * asks for that one and is refused with a 404 if this server has no such
 * file. The refusal is what makes the fallback in `boot` a decision -- a
 * server that answered an unknown tag in English would leave the page
 * rendering English under a German picker.
 *
 * `document.documentElement.lang` is set from what came back rather than from
 * what was asked for, because a screen reader picks its voice off that
 * attribute and a page announcing `lang="de"` over English text is worse than
 * one announcing nothing.
 * @param {string} tag
 * @returns {Promise<void>}
 */
async function loadLocale(tag) {
  const payload = await getJson(tag ? route(ROUTES.locale, { tag: tag })
                                    : ROUTES.locales);
  strings = payload.strings || {};
  locale.tag = String(payload.tag || "");
  locale.available = payload.available || [];
  document.documentElement.lang = locale.tag || "en";
}

/**
 * One string, with `{placeholder}` filled.
 * @param {string} key
 * @param {Record<string, string|number>} [values]
 * @returns {string}
 */
function t(key, values) {
  let text = strings[key];
  if (text === undefined) return key;
  for (const [name, value] of Object.entries(values || {})) {
    text = text.split("{" + name + "}").join(String(value));
  }
  return text;
}

/* ------------------------------------------------------------------ */
/* the DOM                                                             */
/* ------------------------------------------------------------------ */

/**
 * The one element carrying this hook. Hooks are `data-cc` attributes in
 * `index.html`; the test asserts the set read here and the set written there
 * are the same set, in both directions.
 * @param {string} hook
 * @returns {HTMLElement}
 */
function el(hook) {
  const found = document.querySelector('[data-cc="' + hook + '"]');
  if (!found) throw new Error("no element for hook " + hook);
  return /** @type {HTMLElement} */ (found);
}

/**
 * The one element carrying this hook inside a cloned template.
 * @param {ParentNode} root
 * @param {string} hook
 * @returns {HTMLElement}
 */
function find(root, hook) {
  const found = root.querySelector('[data-cc="' + hook + '"]');
  if (!found) throw new Error("no element for hook " + hook);
  return /** @type {HTMLElement} */ (found);
}

/**
 * A fresh copy of a template's single child, with its strings filled in.
 *
 * The `applyStringsIn` call is load-bearing and its absence is invisible in
 * English. `document.querySelectorAll("[data-t]")` does **not** descend into a
 * `<template>`: the content of one is an inert fragment, not part of the
 * document, so the pass that translates the page at boot never sees it. A
 * cloned row therefore arrives carrying the English text the markup holds as
 * its no-script fallback -- which in English is the right answer by accident,
 * and in German is a pane labelled "Upload a file" under a German heading.
 * Filling here rather than at each call site because there are five templates
 * and a sixth would inherit the omission silently.
 * @param {string} hook
 * @returns {HTMLElement}
 */
function clone(hook) {
  const template = /** @type {HTMLTemplateElement} */ (el(hook));
  const original = template.content.firstElementChild;
  if (!original) throw new Error("template " + hook + " is empty");
  const copy = /** @type {HTMLElement} */ (original.cloneNode(true));
  applyStringsIn(copy);
  return copy;
}

/**
 * Text into an element. The only way anything reaches the page.
 * @param {Element} target
 * @param {string} text
 */
function setText(target, text) {
  target.textContent = text;
}

/**
 * Replace an element's children. Elements only; text goes through `setText`.
 * @param {Element} target
 * @param {Element[]} children
 */
function fill(target, children) {
  while (target.firstChild) target.removeChild(target.firstChild);
  for (const child of children) target.appendChild(child);
}

/**
 * One `state` class out of a fixed set, with the others removed.
 * @param {Element} target
 * @param {string} state one of "", "ok", "warn", "bad", "busy"
 */
function setState(target, state) {
  target.classList.remove("ok", "warn", "bad", "busy");
  if (state) target.classList.add(state);
}

/** @param {string} hook @returns {HTMLInputElement} */
function input(hook) { return /** @type {HTMLInputElement} */ (el(hook)); }

/** @param {string} hook @returns {HTMLSelectElement} */
function select(hook) { return /** @type {HTMLSelectElement} */ (el(hook)); }

let uniqueCounter = 0;
/** A DOM id nothing else holds. @returns {string} */
function uniqueId() { uniqueCounter += 1; return "cc-" + uniqueCounter; }

/**
 * A label and its control, tied together by a generated id.
 * @param {HTMLElement} label
 * @param {HTMLElement} control
 */
function associate(label, control) {
  const id = uniqueId();
  control.id = id;
  label.setAttribute("for", id);
}

/* ------------------------------------------------------------------ */
/* formatting                                                          */
/* ------------------------------------------------------------------ */

/**
 * A number the way this page shows numbers: grouped, and never invented.
 *
 * In the page's own language, not the browser's (606). `toLocaleString`'s
 * `undefined` locale reads the browser's configured language, which is
 * routinely not the one the page is rendering in -- a German reader on an
 * English-configured work laptop is the ordinary case LLossless's own
 * number-convention check (601, 602) exists to catch in a *document*, and the
 * German page showing "4,096" was the same defect in the tool itself. The
 * page's own tag (`locale.tag`, set from what the server actually served,
 * `loadLocale`) is the one this and every other number on the page must use;
 * `"en"` is the boot-time fallback before it is known, matching
 * `document.documentElement.lang`'s own default.
 *
 * The one path for a number: nothing else on this page calls `Intl.NumberFormat`
 * or builds a separator by hand. The one other locale-sensitive call this file
 * makes, a run's timestamp in the history list, takes the same `locale.tag ||
 * "en"` rather than a second convention.
 * @param {number|null|undefined} value
 * @param {number} [places]
 * @returns {string|null} null when there is no measurement
 */
function figure(value, places) {
  if (value === null || value === undefined || typeof value !== "number") return null;
  if (!isFinite(value)) return null;
  return new Intl.NumberFormat(locale.tag || "en", {
    minimumFractionDigits: places || 0,
    maximumFractionDigits: places === undefined ? 0 : places,
  }).format(value);
}

/**
 * Seconds as something a person reads while waiting.
 * @param {number} seconds
 * @returns {string}
 */
function duration(seconds) {
  const whole = Math.max(0, Math.round(seconds));
  if (whole < 60) return t("time.seconds", { n: whole });
  return t("time.minutes", { m: Math.floor(whole / 60), s: whole % 60 });
}

/**
 * A short, quotable piece of a long string. Never mid-word where avoidable.
 * @param {string} text
 * @param {number} limit
 * @returns {string}
 */
function shorten(text, limit) {
  const flat = String(text || "").replace(/\s+/g, " ").trim();
  if (flat.length <= limit) return flat;
  const cut = flat.slice(0, limit);
  const space = cut.lastIndexOf(" ");
  return (space > limit * 0.6 ? cut.slice(0, space) : cut) + "…";
}

/* ------------------------------------------------------------------ */
/* state                                                               */
/* ------------------------------------------------------------------ */

/**
 * @typedef {{name: string, text: string, id: string}} Doc
 */

/**
 * @typedef {Object} Store
 * @property {any} config the `/config` payload, once it has arrived
 * @property {any} health the `/health` payload
 * @property {any} session the `/session` payload: whether this server has
 *   accounts, whether one is signed in, and who. Never a credential -- the
 *   session id is in an `HttpOnly` cookie the browser attaches by itself and
 *   this script has no way to read it, which is the point of it being one
 * @property {Doc[]} docs
 * @property {number} active which pane is open
 * @property {string} base the name of the base document, or ""
 * @property {string} fidelity
 * @property {string} verifyDepth
 * @property {string} titlePolicy
 * @property {number} lossBudget
 * @property {string} mergeModel the picked row's id, not its wire name. A
 *   command route's row carries `COMMAND_PREFIX + <route id>`, which is what
 *   makes the route and the model one selection rather than two -- see
 *   `chosenRoute`
 * @property {string} checkModel the same, for the verification role
 * @property {boolean} splitRoles is the check column showing
 * @property {boolean} customOn is "Use a model id not in the table" ticked? Off,
 *   nothing typed is sent and the table is in charge; see `typedId`
 * @property {string} customModel a model id typed in, which overrides the table
 * @property {string} customEndpoint which configured endpoint the typed id goes
 *   to, by provider name; "" is this server's own
 * @property {string} customWindow the context window typed beside the id, as
 *   typed; sent as `window` only while an id is in charge. See `typedWindow`
 * @property {string} runId
 * @property {boolean} hasRun has a run been submitted, followed or replayed
 *   this page load (717)? Drives whether the Current run tab is offered as
 *   live or `aria-disabled`; `startOver` puts it back to false, matching the
 *   pane it empties.
 * @property {boolean} running
 * @property {boolean} cancelling a cancel was taken and the run has not landed (639)
 * @property {EventSource|null} stream
 * @property {number} pollTimer
 * @property {number} tickTimer
 * @property {number} startedAt
 * @property {string} lastMessage
 * @property {any} report
 * @property {string} merged the merged document, kept so that a language
 *   change can redraw the page from what already arrived rather than
 *   re-fetching an artefact that does not change with the language
 * @property {any} cliEquivalent the CLI-equivalent block's payload
 *   (`web/cli_render.py`), or null before a run has one. Kept for the same
 *   reason `merged` is: `renderCliEquivalent` redraws its catalogue strings
 *   on a language change without asking the server again
 * @property {number|null} expiresIn seconds this server said were left before
 *   retention forgets the shown run, at the moment it said so. `null` when
 *   there is nothing to count down to. Never a timestamp: see `remaining`
 * @property {number} readAt `performance.now()` when `expiresIn` arrived, so
 *   the countdown is driven by elapsed time on this machine and never by what
 *   time this machine thinks it is
 * @property {boolean} forgotten has this server said the shown run is gone?
 *   Set from `forgotten_at`, and by a 410 from any download -- which outranks
 *   the countdown, because a suspended tab's elapsed time under-counts
 * @property {string} effort the merge effort level the slider is set to, or
 *   "" before a subscription route that takes one has been picked (613)
 * @property {string} effortRoute the route `effort` was set for, so picking
 *   another route starts from that route's own default
 * @property {number} retentionTimer the interval that re-renders the note
 * @property {number} historyTimer the next history refresh while a run in the
 *   list is queued or running, so a queue position moves without a reload (660)
 * @property {string} retryId the followed run the Retry button would retry,
 *   or "" when it is hidden (660)
 * @property {Set<string>} notify runs the reader asked to be notified about,
 *   by id; filled only by a click on "Notify me" (660)
 * @property {Set<string>} notified runs already notified, so a finish is
 *   announced once however many polls see it
 * @property {any} defaults the reader's saved settings as the server kept
 *   them, or null when there are none (674)
 * @property {{field: string, value: string}[]} defaultsDropped saved values
 *   the server or this page could not use, each named in the notice
 * @property {string} defaultsProblem why the saved settings could not be read
 * @property {boolean} defaultsApplied whether they were applied on this page
 * @property {boolean} defaultsHidden whether the notice was dismissed this
 *   page load, for the dropped set it was shown for (see `DEFAULTS_DISMISS_KEY`
 *   for the persisted half, across page loads)
 * @property {boolean} defaultsReset whether they were just reset
 * @property {string} defaultsUpdateProblem why "Update my defaults" failed
 * @property {{key: string, tone: string, detail: string}|null} defaultsNote
 *   what the last save did, as a catalogue key, a tone and a reason
 */

/** @type {Store} */
const store = {
  config: null,
  health: null,
  session: null,
  docs: [],
  active: 0,
  base: "",
  fidelity: "",
  verifyDepth: "",
  titlePolicy: "",
  lossBudget: 0,
  mergeModel: "",
  checkModel: "",
  splitRoles: false,
  customOn: false,
  customModel: "",
  customEndpoint: "",
  customWindow: "",
  runId: "",
  hasRun: false,
  // Is a run in flight? `setRunning` is the only writer, so "the button says
  // RUNNING" and "this flag is true" cannot disagree -- which is what lets
  // `refreshIdleStatus` refresh the idle label without stepping on the
  // running one.
  running: false,
  // A cancel was asked for and the server took it (639): the status line
  // says "cancelling" until the run lands, whatever the stream says.
  cancelling: false,
  stream: null,
  pollTimer: 0,
  tickTimer: 0,
  startedAt: 0,
  lastMessage: "",
  report: null,
  merged: "",
  // The CLI-equivalent block's payload (`web/cli_render.py`), or null before
  // a run has one. Held so a language change can redraw it -- the notes and
  // the documents sentence are catalogue strings -- without asking the
  // server for anything (`renderCliEquivalent`).
  cliEquivalent: null,
  expiresIn: null,
  readAt: 0,
  forgotten: false,
  effort: "",
  effortRoute: "",
  retentionTimer: 0,
  historyTimer: 0,
  retryId: "",
  notify: new Set(),
  notified: new Set(),
  // The reader's saved settings (674), as the server kept them, or null when
  // there are none. `defaultsDropped` is what the server or this page could
  // not use, as `{field, value}`; `defaultsProblem` is why they could not be
  // read at all. `defaultsApplied` holds them to one application per page:
  // a second sign-in on the same page (a password change) keeps what the
  // reader has set since.
  defaults: null,
  defaultsDropped: [],
  defaultsProblem: "",
  defaultsApplied: false,
  defaultsHidden: false,
  defaultsReset: false,
  defaultsUpdateProblem: "",
  // The line that says what the last save did: a catalogue key, its tone and
  // the server's reason when it failed. Formed at render, so a language
  // switch re-says it.
  defaultsNote: null,
};

/* ------------------------------------------------------------------ */
/* talking to the server                                               */
/* ------------------------------------------------------------------ */

/**
 * A GET that answers with JSON, or throws with the server's own message.
 * @param {string} path
 * @returns {Promise<any>}
 */
async function getJson(path) {
  const answer = await fetch(path, { headers: { Accept: "application/json" } });
  const body = await answer.json().catch(() => null);
  if (!answer.ok) throw new Error(errorMessage(body, answer.status));
  return body;
}

/**
 * A body-carrying request that answers with JSON, or nothing.
 *
 * A 204 is read to its end before it is answered, although it has no body.
 * Returning on the status alone left the response unread, and the browser
 * then cancelled it and reported the request as failed: sign-out's `DELETE`
 * showed as `net::ERR_ABORTED` after its 204 had arrived (649).
 * @param {string} method
 * @param {string} path
 * @param {any} payload
 * @returns {Promise<any>}
 */
async function sendJson(method, path, payload) {
  const answer = await fetch(path, {
    method: method,
    headers: { "Content-Type": "application/json" },
    body: payload === undefined ? undefined : JSON.stringify(payload),
  });
  if (answer.status === 204) {
    await answer.arrayBuffer().catch(() => null);
    return null;
  }
  const body = await answer.json().catch(() => null);
  if (!answer.ok) throw new Error(errorMessage(body, answer.status));
  return body;
}

/**
 * What went wrong, in the server's words where it gave any.
 * @param {any} body
 * @param {number} status
 * @returns {string}
 */
function errorMessage(body, status) {
  if (body && body.error && typeof body.error.message === "string") {
    return body.error.message;
  }
  return "HTTP " + status;
}

/* ------------------------------------------------------------------ */
/* the documents                                                       */
/* ------------------------------------------------------------------ */

/**
 * The two bounds on how many documents one merge may carry.
 *
 * `0` when `/config` has not arrived, and never the real number. These used to
 * fall back to `2`, which is `merge.MIN_SOURCES` -- so the page carried a copy
 * of one of the two bounds it was meant to be reading, and would have gone on
 * enforcing it after the server's own value changed. A page that cannot yet
 * say what the bound is has to say that, and `0` is the answer that refuses
 * rather than the answer that guesses; nothing renders before `/config`
 * anyway, because `boot` returns without rendering when the fetch fails.
 * `tests/test_web_static.py` asserts these two bodies hold no number but `0`.
 * @returns {number}
 */
function maxDocuments() {
  return (store.config && store.config.limits && store.config.limits.max_documents) || 0;
}

/** The floor, read the same way and from the same payload. @returns {number} */
function minDocuments() {
  return (store.config && store.config.limits && store.config.limits.min_documents) || 0;
}

/** @returns {number} */
function maxBodyBytes() {
  return (store.config && store.config.limits && store.config.limits.max_body_bytes) || 0;
}

/** @returns {number} */
function maxLabel() {
  return (store.config && store.config.limits && store.config.limits.max_label) || 200;
}

/**
 * Why the last add or remove did not happen, in a sentence, where the operator
 * is looking.
 *
 * A bound that is enforced silently is a control that looks broken. Both
 * bounds are the server's -- `merge.MIN_SOURCES` and `merge.MAX_SOURCES`
 * through `/config` -- and the server refuses the same submission with the
 * same numbers, so this is not the enforcement: it is the part that says which
 * number was hit and what to do instead. Cleared by the next `renderDocuments`,
 * so it never stands over a page the operator has since fixed.
 * @param {string} text
 */
function refuse(text) {
  setText(el("doc-refusal"), text);
}

/**
 * Add a pane. Named for the position it lands in, which the operator can edit.
 * @param {string} [name]
 * @param {string} [text]
 */
function addDocument(name, text) {
  if (store.docs.length >= maxDocuments()) {
    refuse(t("documents.refused.max",
             { max: maxDocuments(), n: store.docs.length }));
    return;
  }
  const position = store.docs.length + 1;
  store.docs.push({
    id: uniqueId(),
    name: name || t("documents.untitled", { n: position }),
    text: text || "",
  });
  store.active = store.docs.length - 1;
  renderDocuments();
}

/**
 * Drop a pane, or say why it stays.
 * @param {number} index
 */
function removeDocument(index) {
  if (store.docs.length <= minDocuments()) {
    refuse(t("documents.refused.min",
             { min: minDocuments(), n: store.docs.length }));
    return;
  }
  store.docs.splice(index, 1);
  if (store.active >= store.docs.length) store.active = store.docs.length - 1;
  renderDocuments();
}

/**
 * The line under the panes: how many documents *have text*, not how many
 * panes are open (654). A fresh page has two empty panes and used to read
 * "2 documents added ... needs at least 2" over zero characters typed
 * anywhere -- a fact about the empty tabs, not about what the operator had
 * done. Its own function, called on every keystroke as well as on
 * `renderDocuments`, because typing into a pane is exactly the moment this
 * line has to change and a full re-render on every keystroke would drop the
 * cursor out of the textarea it just moved in.
 *
 * Four sentences rather than one template: "none" and "some" are states the
 * single template never had reason to name, and "ready" (at or over the
 * floor) does not repeat "needs at least" -- the readiness line already
 * says what is missing, in its own words, whenever every pane is empty, and
 * repeating it here was the other half of what read wrong.
 */
function renderDocTotal() {
  const filledCount = store.docs.filter((doc) => doc.text.trim().length > 0).length;
  const floor = minDocuments(), ceiling = maxDocuments();
  const variant = filledCount === 0 ? "none"
    : filledCount === 1 ? "one"
    : filledCount < floor ? "some"
    : "ready";
  setText(el("doc-total"), t("documents.count." + variant,
    { n: filledCount, min: floor, max: ceiling }));
}

/** Tabs, panes, the base selector and the counts, from `store.docs`. */
function renderDocuments() {
  refuse("");
  /** @type {HTMLElement[]} */
  const tabs = [];
  /** @type {HTMLElement[]} */
  const panes = [];
  store.docs.forEach((doc, index) => {
    tabs.push(documentTab(doc, index));
    panes.push(documentPane(doc, index));
  });
  fill(el("doc-tabs"), tabs);
  fill(el("doc-panes"), panes);
  renderBaseSelector();
  renderDocTotal();
  // `aria-disabled` rather than `disabled`, here and on every remove control.
  // A disabled button is unclickable, so the one press that would have asked
  // "why not?" never reaches a handler and the operator is left with a greyed
  // control and no sentence. This one is announced as unavailable and still
  // answers, with `refuse` writing the reason.
  const addButton = /** @type {HTMLButtonElement} */ (el("add-document"));
  addButton.setAttribute("aria-disabled",
    store.docs.length >= maxDocuments() ? "true" : "false");
  addButton.title = t("documents.add");
  // The depth picker prices each option in model calls, and the price is one
  // call per document -- so adding or removing a pane changes it. Guarded on
  // `/config` having arrived, because this function also runs on a page whose
  // configuration fetch failed, and a count rendered from nothing would be the
  // page inventing the one figure it is here to state exactly.
  if (store.config) renderVerifyDepth();
  refreshIdleStatus();
}

/**
 * @param {Doc} doc
 * @param {number} index
 * @returns {HTMLElement}
 */
function documentTab(doc, index) {
  const tab = clone("tpl-doc-tab");
  const selected = index === store.active;
  tab.setAttribute("aria-selected", selected ? "true" : "false");
  tab.setAttribute("tabindex", selected ? "0" : "-1");
  tab.setAttribute("aria-controls", doc.id);
  const shown = doc.name || t("documents.untitled", { n: index + 1 });
  setText(find(tab, "tab-name"), shown);
  // Named explicitly, because the remove button lives inside the tab and a
  // name computed from the contents would be "document 1, empty, Remove
  // document 1" -- the tab announcing its own delete control as part of what
  // it is. A browser check caught this; no file-level rule could have.
  tab.setAttribute("aria-label", shown);
  setText(find(tab, "tab-size"), doc.text.length
    ? t("documents.chars", { n: figure(doc.text.length) || "0" })
    : t("documents.empty"));

  // The tab's own remove. Named after the document rather than labelled
  // "remove", because a screen reader reads the twelfth of these out of
  // context and "remove" twelve times over is not a set of twelve controls.
  const close = /** @type {HTMLButtonElement} */ (find(tab, "tab-remove"));
  setText(find(tab, "tab-remove-label"), t("documents.remove.one", { name: shown }));
  const atFloor = store.docs.length <= minDocuments();
  close.setAttribute("aria-disabled", atFloor ? "true" : "false");
  // The reason reaches a screen reader through `refuse` once the press is
  // made (654); this is the same sentence, reachable on hover before it is.
  if (atFloor) close.title = t("documents.refused.min", { min: minDocuments() });
  else close.removeAttribute("title");
  close.addEventListener("click", (event) => {
    // Without this the tab underneath also takes the click and selects an
    // index the splice has already moved.
    event.stopPropagation();
    removeDocument(index);
  });

  tab.addEventListener("click", () => { store.active = index; renderDocuments(); });
  tab.addEventListener("keydown", (event) => {
    const key = /** @type {KeyboardEvent} */ (event).key;
    const step = key === "ArrowRight" ? 1 : key === "ArrowLeft" ? -1 : 0;
    if (!step) return;
    event.preventDefault();
    store.active = (index + step + store.docs.length) % store.docs.length;
    renderDocuments();
    const tabsNow = el("doc-tabs").children;
    const next = /** @type {HTMLElement} */ (tabsNow[store.active]);
    if (next) next.focus();
  });
  return tab;
}

/**
 * @param {Doc} doc
 * @param {number} index
 * @returns {HTMLElement}
 */
function documentPane(doc, index) {
  const pane = clone("tpl-doc-pane");
  pane.id = doc.id;
  pane.hidden = index !== store.active;

  const nameInput = /** @type {HTMLInputElement} */ (find(pane, "doc-name"));
  associate(find(pane, "name-label"), nameInput);
  nameInput.value = doc.name;
  nameInput.maxLength = maxLabel();
  nameInput.addEventListener("input", () => {
    doc.name = nameInput.value;
    setText(find(el("doc-tabs").children[index] || pane, "tab-name"), doc.name);
    renderBaseSelector();
  });

  const textArea = /** @type {HTMLTextAreaElement} */ (find(pane, "doc-text"));
  associate(find(pane, "text-label"), textArea);
  textArea.value = doc.text;
  textArea.addEventListener("input", () => {
    doc.text = textArea.value;
    const tab = el("doc-tabs").children[index];
    if (tab) {
      setText(find(tab, "tab-size"), doc.text.length
        ? t("documents.chars", { n: figure(doc.text.length) || "0" })
        : t("documents.empty"));
    }
    renderDocTotal();
    refreshIdleStatus();
  });

  const fileInput = /** @type {HTMLInputElement} */ (find(pane, "doc-file"));
  associate(find(pane, "file-label"), fileInput);
  fileInput.addEventListener("change", () => {
    // Snapshotted before the reset, not after: clearing `value` empties
    // `files` in the same tick, and `loadFiles` is a promise that reads its
    // argument later. The single-file version got away with this by taking
    // `files[0]` on the line above the reset.
    const chosen = Array.from(fileInput.files || []);
    fileInput.value = "";
    void loadFiles(chosen, doc);
  });

  const remove = /** @type {HTMLButtonElement} */ (find(pane, "doc-remove"));
  const removeAtFloor = store.docs.length <= minDocuments();
  remove.setAttribute("aria-disabled", removeAtFloor ? "true" : "false");
  if (removeAtFloor) remove.title = t("documents.refused.min", { min: minDocuments() });
  else remove.removeAttribute("title");
  remove.addEventListener("click", () => removeDocument(index));

  pane.addEventListener("dragover", (event) => {
    event.preventDefault();
    pane.classList.add("dropping");
  });
  pane.addEventListener("dragleave", () => pane.classList.remove("dropping"));
  pane.addEventListener("drop", (event) => {
    event.preventDefault();
    pane.classList.remove("dropping");
    const transfer = /** @type {DragEvent} */ (event).dataTransfer;
    // `DataTransfer.files` is in the order the operator selected them, and
    // that order is the merge's document order, which decides the base. It is
    // copied once, here, and nothing downstream sorts it.
    void loadFiles(Array.from((transfer && transfer.files) || []), doc);
  });

  return pane;
}

/**
 * Decoded bytes that were never text.
 *
 * `File.text()` decodes as UTF-8 whatever it is handed, so a PDF, a PNG or a
 * zip arrives as a string and pastes into a textarea as mojibake -- which is
 * what the shipped page did, silently, and then named the document after the
 * file so the merge would have run on it. Both markers are ones UTF-8 text
 * does not carry: a NUL byte, and U+FFFD, which the decoder emits exactly
 * where the bytes were not UTF-8.
 *
 * By content and not by extension, because a drop ignores the picker's
 * `accept` list, and because the extensions that are text are not a closed
 * set -- a `.csv`, a `.json` or a file with no extension at all is text and
 * merges fine. The cost is that a text file which genuinely contains a
 * replacement character is refused; it is refused **by name**, which is a
 * sentence the operator can act on, rather than pasted as rubbish.
 * @param {string} text
 * @returns {boolean}
 */
function looksBinary(text) {
  return text.indexOf("\u0000") >= 0 || text.indexOf("\uFFFD") >= 0;
}

/**
 * Every file from one drop or one picker press, one document each, in order.
 *
 * The shipped page took `files[0]` and threw the rest away without a word, so
 * dropping three files produced one document and no explanation. It also
 * wrote straight over whatever was in the pane.
 *
 * Three rules, and the reasons are in `internal/docs/DECISIONS.md` (559):
 *
 * - **Nothing typed is ever written over.** Placement starts at the pane the
 *   files were dropped on and walks forward over any pane that already holds
 *   text, then adds panes. A pane that was passed over is named in the line
 *   under the documents, because a file that did not land where it was aimed
 *   is exactly the kind of surprise this function exists to stop.
 * - **The order is the drop's order.** The base document defaults to the
 *   first, so a reordering here would change the merge's result silently.
 * - **Nothing is dropped in silence.** A file refused for its type, its size
 *   or the document ceiling is named, with the bound it hit.
 * @param {File[]} files in the order they were dropped or chosen
 * @param {Doc} target the document whose pane took the drop
 */
async function loadFiles(files, target) {
  if (!files.length) return;
  const bytes = maxBodyBytes();
  /** @type {string[]} */ const notext = [];
  /** @type {string[]} */ const toolarge = [];
  /** @type {string[]} */ const surplus = [];
  /** @type {{name: string, text: string}[]} */ const ready = [];

  // Read first, place second. A refusal that names three files cannot be
  // written until all three have been looked at, and placing as we read would
  // leave half a drop on the page under a message about the other half.
  for (const file of files) {
    const name = String(file.name || "").slice(0, maxLabel());
    if (bytes && file.size > bytes) { toolarge.push(name); continue; }
    const text = await file.text();
    if (looksBinary(text)) { notext.push(name); continue; }
    ready.push({ name, text });
  }

  const from = Math.max(0, store.docs.indexOf(target));
  let at = from;
  let skipped = "";
  let opened = -1;
  for (const file of ready) {
    while (at < store.docs.length && store.docs[at].text.trim()) {
      if (!skipped) skipped = paneLabel(at);
      at += 1;
    }
    if (at >= store.docs.length) {
      if (store.docs.length >= maxDocuments()) { surplus.push(file.name); continue; }
      store.docs.push({
        id: uniqueId(),
        name: t("documents.untitled", { n: store.docs.length + 1 }),
        text: "",
      });
    }
    store.docs[at].text = file.text;
    if (file.name) store.docs[at].name = file.name;
    if (opened < 0) opened = at;
    at += 1;
  }
  if (opened >= 0) store.active = opened;
  renderDocuments();

  // After the render, never before: `renderDocuments` opens by clearing this
  // line, so a reason written first is a reason nobody ever reads.
  const problems = [];
  if (skipped) problems.push(t("documents.dropped.kept", { name: skipped }));
  if (notext.length) {
    problems.push(t("documents.dropped.notext", { names: notext.join(", ") }));
  }
  if (toolarge.length) {
    problems.push(t("documents.dropped.toolarge",
                    { names: toolarge.join(", "), max: bytes }));
  }
  if (surplus.length) {
    problems.push(t("documents.dropped.overmax",
                    { names: surplus.join(", "), max: maxDocuments() }));
  }
  if (problems.length) refuse(problems.join(" "));
}

/**
 * What to call document `index` in a sentence about it.
 * @param {number} index
 * @returns {string}
 */
function paneLabel(index) {
  const doc = store.docs[index];
  return (doc && doc.name) || t("documents.untitled", { n: index + 1 });
}

/** The base picker, rebuilt from the current names. */
function renderBaseSelector() {
  const picker = select("base-select");
  const options = store.docs.map((doc, index) => {
    const option = document.createElement("option");
    option.value = doc.name;
    setText(option, doc.name || t("documents.untitled", { n: index + 1 }));
    return option;
  });
  fill(picker, options);
  if (!store.docs.some((doc) => doc.name === store.base)) {
    store.base = store.docs.length ? store.docs[0].name : "";
  }
  picker.value = store.base;
}

/* ------------------------------------------------------------------ */
/* the controls                                                        */
/* ------------------------------------------------------------------ */

/** Fidelity, depth, title policy, loss budget and the model table, from `/config`. */
function renderControls() {
  renderFidelity();
  renderVerifyDepth();
  renderTitlePolicy();
  renderLossBudget();
  renderModels();
  renderDefaults();
  // The button's label names the route, so it is part of the controls rather
  // than part of the run. Without this a language change redrew the table and
  // left the one control that commits the money reading the previous
  // language's word for it.
  refreshIdleStatus();
}

/** The slider. Stops, labels and the three sentences under it are the server's. */
function renderFidelity() {
  const levels = store.config.fidelity.levels || [];
  const slider = input("fidelity-range");
  slider.max = String(Math.max(0, levels.length - 1));

  const stops = levels.map((/** @type {any} */ level) => {
    const option = document.createElement("option");
    option.value = String(levels.indexOf(level));
    option.label = level.name;
    return option;
  });
  fill(el("fidelity-stops"), stops);

  const chosen = levels.findIndex(
    (/** @type {any} */ level) => level.value === store.fidelity);
  const index = chosen >= 0
    ? chosen
    : Math.max(0, levels.findIndex((/** @type {any} */ level) => level.default));
  slider.value = String(index);
  store.fidelity = levels[index] ? levels[index].value : "";

  const legend = levels.map((/** @type {any} */ level, /** @type {number} */ position) => {
    const span = document.createElement("span");
    setText(span, level.name);
    // Where its stop is, as a fraction of the track: the stylesheet puts the
    // word under the thumb there (686).
    span.style.setProperty("--at", String(levels.length > 1 ? position / (levels.length - 1) : 0));
    if (position === index) span.classList.add("on");
    return span;
  });
  fill(el("fidelity-legend"), legend);

  const level = levels[index];
  // Three strings, three places, out of the catalogue and keyed by the value
  // `/config` just gave us -- the same shape as `t("basis." + value)` (550).
  // The page holds no level vocabulary of its own: it does not know the word
  // `open`, and it never sees the prompt the model is given, which is where
  // this copy used to come from and why it read *"you are expected"* at a
  // person choosing a setting.
  const copy = (/** @type {string} */ part) =>
    level ? t("fidelity." + String(level.value) + "." + part) : "";
  // One short line under the slider, one line high at every level (673); the
  // summary, what it buys and what it costs are in the Compare levels dialog
  // (`renderCompare`) and in the slider's `aria-valuetext` below.
  setText(el("fidelity-brief"), level ? t("brief.level." + String(level.value)) : "");
  // The whole thing for a screen reader, because the slider announces one
  // string and the three under it are what a sighted reader gets for free.
  slider.setAttribute("aria-valuetext", level
    ? level.name + ": " + [copy("summary"), copy("buys"), copy("costs")].join(" ")
    : "");

  slider.oninput = () => {
    const picked = levels[Number(slider.value)];
    if (!picked) return;
    store.fidelity = picked.value;
    renderFidelity();
    // The effort card's one fidelity-dependent line (613).
    renderEffortCard();
  };
}

/**
 * The depths the server serves, and what each one costs and does not ask.
 *
 * Everything rendered here arrives in `/config`: the names, the sentences, the
 * flag saying whether a depth checks for invention, and the two numbers the
 * call count is formed from. The page holds no depth vocabulary of its own --
 * it does not know the word `coverage` and must not learn it, because the only
 * thing it would ever use it for is to decide which option to warn about, and
 * that is what `detects_invention` is for.
 *
 * The description is rendered *inside* the option rather than under the group.
 * A sentence below the radios that changes when you pick one is a sentence a
 * reader can change the setting without having read, and the thing to be read
 * here is not a nuance of degree: one of these options stops asking whether
 * the merge invented anything.
 */
function renderVerifyDepth() {
  const depths = (store.config.verify_depth || {}).depths || [];
  if (!depths.some((/** @type {any} */ depth) => depth.value === store.verifyDepth)) {
    const fallback = depths.find((/** @type {any} */ depth) => depth.default)
      || depths[0];
    store.verifyDepth = fallback ? fallback.value : "";
  }
  const options = depths.map((/** @type {any} */ depth) => {
    const label = document.createElement("label");
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "verify-depth";
    radio.value = depth.value;
    radio.checked = depth.value === store.verifyDepth;
    radio.addEventListener("change", () => {
      store.verifyDepth = depth.value;
      renderVerifyDepth();
    });

    const body = document.createElement("span");
    body.className = "stacked-body";
    const heading = document.createElement("span");
    heading.className = "stacked-title";
    const name = document.createElement("span");
    // The depth's name and what it does, from the catalogue by value (643):
    // `/config` serves both in English, and a German page rendered them as
    // served.
    setText(name, depthName(String(depth.value || "")));
    heading.appendChild(name);
    const cost = document.createElement("span");
    cost.className = "stacked-cost mono";
    setText(cost, t(exactCalls(depth)
                      ? "controls.depth.calls"
                      : "controls.depth.calls.atleast",
                    { n: callsAt(depth) }));
    heading.appendChild(cost);
    body.appendChild(heading);
    // One short line in the option, and the whole sentence behind a "?"
    // beside it (673). The short line keeps what the option does not check
    // in the option itself, for the reason the sentence was there (643).
    const brief = document.createElement("span");
    brief.className = "stacked-brief";
    setText(brief, t("brief.depth." + String(depth.value || "")));
    const explains = document.createElement("span");
    explains.className = "stacked-explains";
    setText(explains, t("depth." + String(depth.value || "") + ".explains"));
    brief.appendChild(helpBox(explains));
    body.appendChild(brief);

    label.appendChild(radio);
    label.appendChild(body);
    return label;
  });
  fill(el("verify-depth"), options);
  renderDepthDelta();
  renderDepthEstimate();
}

/**
 * What the cheap depth costs in detection, from the field rather than from here.
 *
 * `/config` has carried `verify_depth.quality_delta` since 504 and nothing read
 * it, while the paragraph under the picker was a static catalogue string. The
 * two could not disagree out loud: setting a measured delta on the server would
 * have left the page saying "unmeasured" and nothing would have gone red. A
 * served field no surface reads is a field that is not really served.
 *
 * The page still invents no figure. `unmeasured` selects the sentence that says
 * there is none. Anything else is the catalogue's `verify_depth` block, which
 * the server validated with its run, artefacts and derived_by (585), and every
 * number below is one of its fields, formatted by `figure` and put into a
 * sentence the catalogue owns. Nothing here adds, divides, rounds or compares a
 * figure: the block publishes the speedup rather than two timings, and the
 * reader is shown both depths' counts side by side rather than told they match.
 *
 * It names no depth either. The measured depths are the block's entries other
 * than its `comparator`, and their names come from the served rows by value.
 * What a depth cannot reach is no longer said here (673): the option's own
 * short line says it, and the paragraph sits behind the picker's "?".
 */
function renderDepthDelta() {
  const served = store.config.verify_depth || {};
  const delta = served.quality_delta || "unmeasured";
  if (delta === "unmeasured" || typeof delta !== "object") {
    setText(el("depth-delta"), t("controls.depth.unmeasured"));
    return;
  }
  const rows = served.depths || [];
  const nameOf = (/** @type {string} */ value) => {
    const row = rows.find((/** @type {any} */ entry) => entry.value === value);
    return row ? depthName(value) : value;
  };
  // A published figure, formatted. The block is validated on the server, so
  // an absent one is a malformed block and shows as a dash, never as a zero.
  const shown = (/** @type {any} */ value, places = 0) =>
    figure(value, places) || "-";
  const measured = Array.isArray(delta.depths) ? delta.depths : [];
  const base = measured.find(
    (/** @type {any} */ entry) => entry.value === delta.comparator);
  const parts = [];
  for (const entry of measured) {
    if (!base || entry === base) continue;
    const depth = nameOf(entry.value);
    // What a depth cannot catch is said in its option's own line (673); the
    // benchmark sentence that used to repeat it here is gone.
    const mine = entry.source_to_merged || {};
    const theirs = base.source_to_merged || {};
    parts.push(t("controls.depth.measured.keeps", {
      depth: depth,
      caught: shown(mine.plants_detected), planted: shown(mine.plants),
      comparator: nameOf(base.value),
      base_caught: shown(theirs.plants_detected), base_planted: shown(theirs.plants),
    }));
    if (typeof entry.speedup === "number") {
      parts.push(t("controls.depth.measured.saves", {
        depth: depth, comparator: nameOf(base.value),
        speedup: shown(entry.speedup, 1),
      }));
    }
  }
  parts.push(t("controls.depth.measured.caveat", {
    date: String(delta.measured_on || ""), model: String(delta.model || ""),
    fixtures: shown(delta.fixtures), draws: shown(delta.draws),
  }));
  setText(el("depth-delta"), parts.join(" "));
}

/**
 * What this run will cost in model calls, and what that figure is not.
 *
 * The one number about this choice that can be stated without measuring
 * anything: `cli.pipeline` makes one call per source plus a fixed few, and the
 * server sends both halves so the count is for the documents actually loaded
 * rather than for an assumed two. It falls from six to three on a two-document
 * merge, which is the entire reason the cheap depth exists.
 *
 * It is a count of calls and not a price on purpose. The calls are not the
 * same size -- a fused coverage call carries the merged document that a
 * decompose call does not -- so a dollar figure formed by scaling the model
 * table's measured cost per merge would be invented, and this project's rule
 * for a number nobody measured is to name what is exact and decline the rest
 * (`pricing.py`, and `config.merge_model_calls`).
 *
 * And at a depth whose count is only a floor it says so, because the server
 * says so. `full` batches each verify pass, 25 claims a call over HTTP and
 * 100 through a command, so long documents cost more than the figure and
 * never less; a minimum rendered as a quote is read as a quote (505).
 */
function renderDepthEstimate() {
  const depths = (store.config.verify_depth || {}).depths || [];
  const chosen = depths.find(
    (/** @type {any} */ depth) => depth.value === store.verifyDepth);
  setText(el("depth-estimate"), chosen
    ? t(exactCalls(chosen)
          ? "controls.depth.estimate"
          : "controls.depth.estimate.atleast", {
        n: callsAt(chosen),
        docs: store.docs.length,
      })
    : "");
}

/**
 * Whether a depth's count is the number of calls or the fewest of them.
 *
 * Read off the `exact` flag the server sends beside the two counts, and never
 * off the depth's name -- `suspendedGuarantee`'s rule, for its reason. A row
 * that omits the flag is treated as a floor: "at least" is true of an exact
 * count as well, so the unknown case errs towards the weaker claim.
 *
 * Both keys are written out at each call site rather than built by appending
 * a suffix here. A key formed by concatenation is a key no reader and no
 * check can find by searching for it, and `keys_used_in_js` would report two
 * live strings as dead.
 * @param {any} depth a row from `/config`'s `verify_depth.depths`
 * @returns {boolean}
 */
function exactCalls(depth) {
  const calls = (depth && depth.calls) || {};
  return calls.exact === true;
}

/**
 * The model calls one depth makes over the documents currently loaded.
 * @param {any} depth a row from `/config`'s `verify_depth.depths`
 * @returns {number}
 */
function callsAt(depth) {
  const calls = (depth && depth.calls) || {};
  const fixed = typeof calls.fixed === "number" ? calls.fixed : 0;
  const each = typeof calls.per_source === "number" ? calls.per_source : 0;
  return fixed + each * store.docs.length;
}

/** The title policy, one radio per policy the server names. */
function renderTitlePolicy() {
  const policies = store.config.title_policy.policies || [];
  if (!policies.some((/** @type {any} */ policy) => policy.value === store.titlePolicy)) {
    const fallback = policies.find((/** @type {any} */ policy) => policy.default)
      || policies[0];
    store.titlePolicy = fallback ? fallback.value : "";
  }
  const group = policies.map((/** @type {any} */ policy) => {
    const label = document.createElement("label");
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "title-policy";
    radio.value = policy.value;
    radio.checked = policy.value === store.titlePolicy;
    radio.addEventListener("change", () => {
      store.titlePolicy = policy.value;
      renderTitlePolicy();
    });
    const text = document.createElement("span");
    setText(text, policy.value);
    label.appendChild(radio);
    label.appendChild(text);
    return label;
  });
  fill(el("title-policy"), group);
  const active = policies.find(
    (/** @type {any} */ policy) => policy.value === store.titlePolicy);
  // From the catalogue by value (643), for `renderVerifyDepth`'s reason.
  setText(el("title-explains"), active ? t("title." + String(active.value) + ".explains") : "");
  // The one line under the pills (673); the sentence above sits behind "?".
  setText(el("title-brief"), active ? t("brief.title." + String(active.value)) : "");
}

/**
 * A verification depth's name in the reader's language, by its value (643).
 * @param {string} value
 * @returns {string}
 */
function depthName(value) {
  return t("depth." + value + ".name");
}

/** The declared-loss ceiling, defaulted from the server and shown as a percentage. */
function renderLossBudget() {
  const field = input("loss-budget");
  const fallback = store.config.loss_budget ? store.config.loss_budget.default : 0;
  if (!field.value) {
    store.lossBudget = typeof fallback === "number" ? fallback : 0;
    field.value = String(store.lossBudget);
  }
  setText(el("loss-budget-pct"), (store.lossBudget * 100).toFixed(1) + "%");
  field.oninput = () => {
    const value = Number(field.value);
    store.lossBudget = isFinite(value) ? value : 0;
    setText(el("loss-budget-pct"), (store.lossBudget * 100).toFixed(1) + "%");
  };
}

/**
 * The picker, and everything that decides what it has selected (631).
 *
 * The picker lists only the rows this reader can run (`pickerRows`); every
 * catalogue row, with its measured figures, is `renderScorecard`'s. The
 * selection rules below still read every row `pickable` builds, so a row that
 * is not offered is cleared from the selection exactly as before.
 */
function renderModels() {
  const models = pickable();
  // **A selection that is no longer offered is not a selection.** Switching a
  // discovered route off removes its row while `store.mergeModel` still names
  // it, and the page then held an id nothing matches: the button read `route
  // not identified` -- honest, and the state before 524 read `metered API`,
  // which was not -- and `chosenModel` would have sent the prefixed row id to
  // an endpoint as a model name. Clearing it here puts the preselection below
  // back in charge, which is the one place that decides what an untouched page
  // is pointed at.
  // A retired row (618) is shown, with its figures, and never offered: a
  // selection that names one is cleared like any selection no longer offered.
  const offered = new Set(models.filter((/** @type {any} */ model) => !isRetired(model))
    .map((/** @type {any} */ model) => model.id));
  if (store.mergeModel && !offered.has(store.mergeModel)) store.mergeModel = "";
  if (store.checkModel && !offered.has(store.checkModel)) store.checkModel = "";
  // **A command route is preselected over a metered one, never the reverse.**
  //
  // The two mistakes are not symmetric. Firing at a metered API when you
  // believed you were on the subscription spends money you did not mean to
  // spend, and you find out on a bill; firing at the subscription when you
  // meant the API costs a run against a plan you are already paying for. A
  // default has to be wrong in the direction that is cheap to be wrong in.
  //
  // It is also the only preselection that can be *checked* by the person it
  // affects: the button names the route it is about to use, so a reader who
  // wanted the metered one sees that they have to say so.
  //
  // **And among the command routes, the Opus route** (612), the operator's
  // ruling on the subscription grid. A route the operator wrote themselves
  // still comes first, because it is a deliberate act by somebody with a
  // shell; then the discovered row the server marks `preselect`; then the
  // first command route, which is what a server too old to mark one gets.
  const routes = models.filter((/** @type {any} */ model) =>
    reachable(model) && routeOf(model));
  const first = routes.find((/** @type {any} */ model) => !routeOf(model).discovered)
    || routes.find((/** @type {any} */ model) => routeOf(model).preselect)
    || routes[0]
    || models.find((/** @type {any} */ model) => reachable(model) && !isRetired(model));
  if (!store.mergeModel && first) store.mergeModel = first.id;
  if (!store.checkModel && first) store.checkModel = first.id;
  // One program answers every role, so there is nothing to split. Forced
  // rather than merely hidden: a checkbox left ticked under a route that
  // ignores it is a setting the page shows and the run does not have.
  if (chosenRoute()) {
    store.splitRoles = false;
    store.checkModel = store.mergeModel;
  }
  // **A check selection the Check column cannot offer is not a selection**
  // (570), the rule two paragraphs up applied to the second role. The column
  // disables a command row under an HTTP merge, and the preselection above
  // prefers a command row, so a cleared check role could land on one the
  // column would never let a reader pick. It is joined back to the merge's
  // row, which is the selection the page shows when the roles are not split.
  const checking = models.find(
    (/** @type {any} */ model) => model.id === store.checkModel);
  if (store.splitRoles && checking && !answersChecks(checking)) {
    store.checkModel = store.mergeModel;
  }
  const split = /** @type {HTMLInputElement} */ (el("split-models"));
  split.checked = store.splitRoles;
  // **The reason and the state are one value** (596): the box is disabled
  // exactly when `splitBlocked` has a sentence, and that sentence is what the
  // tooltip, the visible hint and `aria-describedby` carry. A second copy of
  // the condition for the text would be free to drift from the one that
  // greys the box.
  const blocked = splitBlocked(models);
  split.disabled = Boolean(blocked);
  const why = el("split-blocked");
  setText(why, blocked);
  why.hidden = !blocked;
  if (blocked) {
    split.title = blocked;
    split.setAttribute("aria-describedby", "split-blocked");
  } else {
    split.removeAttribute("title");
    split.removeAttribute("aria-describedby");
  }
  el("models-check-head").hidden = !store.splitRoles;
  // Why the command rows' Check radios are greyed, said where the reader who
  // just ticked the split is looking. Only while it is true: under a command
  // merge there is no Check column, and on a server with no command route
  // there is nothing greyed to explain.
  const routesNote = el("split-routes");
  routesNote.hidden = !(store.splitRoles && !chosenRoute()
    && models.some((/** @type {any} */ model) => routeOf(model)));
  setText(routesNote, routesNote.hidden ? "" : t("models.split.commands"));

  // **Only what this reader can run** (631). A row with no endpoint and a
  // retired row are the scorecard's alone; with nothing left, a sentence says
  // so and offers the credentials sheet instead of an empty table.
  const nothing = renderPickerRows(models) === 0;
  el("picker-empty").hidden = !nothing;
  el("picker-box").hidden = nothing;
  renderPill(nothing ? "empty" : "ready");
  renderScorecard();
  renderCustomModel();
  renderEffort();
}

/**
 * The picker's rows, in the order its headers ask for (635). Returns how many.
 *
 * Only the rows: the radios read `store.mergeModel` and `store.checkModel`,
 * so a sort redraws them checked where they were and never changes which
 * model is selected. `renderModels` is the caller that also settles the
 * selection; a header click calls this alone.
 * @param {any[]} [models] the rows `pickable` built
 * @returns {number}
 */
function renderPickerRows(models) {
  const offered = pickerRows(models || pickable());
  const rows = scorecardOrder(offered, pickerSort.key, pickerSort.direction);
  fill(el("picker-rows"), rows.map((/** @type {any} */ model) => pickerRow(model)));
  paintSortHeads(pickerSort);
  return rows.length;
}

/**
 * The rows the picker offers: every row `pickable` builds that can be run (631).
 *
 * `reachable` is the endpoint half -- a provider with an endpoint configured,
 * or no provider at all, which is a command route or a row for the server's
 * own endpoint -- and a retired row is never offered (618), whatever its
 * endpoint. The order is `pickable`'s, so the command routes stay first.
 * @param {any[]} models the rows `pickable` built
 * @returns {any[]}
 */
function pickerRows(models) {
  return models.filter((/** @type {any} */ model) =>
    reachable(model) && !isRetired(model));
}

/**
 * The name, and the route badge after it, as one span (565).
 *
 * The name in a span of its own so it stays whole while the badge after it
 * may drop to the next line: the `<wbr>` is the one place the line may break.
 * @param {any} model
 * @returns {HTMLElement}
 */
function modelNameLine(model) {
  const strong = document.createElement("span");
  strong.className = "model-name";
  const called = document.createElement("span");
  setText(called, model.display_name || model.id);
  strong.appendChild(called);
  // **Every row names its route, not only the command ones.** A list where
  // one kind of row is annotated and the rest are bare model names is a list
  // that asks the reader to infer the difference, and the inference is the
  // failure: "I may have Opus 5 token based or behind a subscription and it
  // needs to be clear which one is selected". So `Claude Opus 5` reads with
  // `metered API` beside it and the operator's own `Opus 5 - Subscription`
  // reads with `subscription` -- two rows for one model, told apart by the
  // thing that differs.
  //
  // A badge rather than a second column: the route is a property of the row
  // rather than a measurement, and a column of it would sort and band
  // alongside the four that are.
  const badge = document.createElement("span");
  badge.className = "route-badge " + routeKind(model);
  setText(badge, routeLabel(routeKind(model)));
  // A `<wbr>` rather than a space: it adds no width and no character to the
  // row's text. With the wire name free to wrap, the German table with the
  // Check column on was held 18px past its box by `Claude Code - Sonnet` +
  // `ABONNEMENT` as one 242px run.
  strong.appendChild(document.createElement("wbr"));
  strong.appendChild(badge);
  return strong;
}

/**
 * The short markers a command row carries, each said in full once under the
 * table by `renderRouteCaveats`.
 *
 * A route the catalogue measured and this server does not serve (631) has no
 * served `comparable`, `retrieval` or sharing to report, so it carries the
 * sentence that it is not switched on here and its measured level alone.
 *
 * A marker with `why` carries its explanation on the marker itself (638):
 * `markLine` gives it a `title` for a pointer and `aria-describedby` for the
 * keyboard, pointing at a hidden element that holds the same sentence.
 * @param {any} model
 * @returns {{text: string, why?: string, hook?: string}[]}
 */
function routeMarks(model) {
  const route = routeOf(model);
  if (!route) return [];
  /** @type {{text: string, why?: string, hook?: string}[]} */
  const marks = [];
  const say = (/** @type {string} */ text) => marks.push({ text });
  // **The model the alias answers as now, first** (675). A served row is
  // named by its label, which names an alias and no version; this is where
  // the reader learns which model a run through it gets today. An unserved
  // row already carries it in its name (`routeNameNow`).
  const now = aliasNow(route);
  if (now && !route.unserved) {
    say(t("models.route.mark.runs", { model: catalogueModelName(now.model) }));
  }
  if (route.unserved) {
    say(t("models.route.unserved"));
  } else {
    if (!route.comparable) {
      // Plain words on the row and the reason one hover or one Tab away
      // (638). The tier's identifier (`prompt`) used to follow the marker in
      // brackets; it is a profile's internal name, and the sentence behind
      // the marker now says what it means without naming it.
      marks.push({ text: t("models.route.mark.incomparable"),
                   why: "models.route.mark.incomparable.why" });
    }
    if (!commandsArePerUser()) say(t("models.route.mark.shared"));
    // **The grant, on the row.** A `sourced` run through this route lets the
    // model reach the network, and at that level the grant is made
    // automatically rather than written by hand -- so the one place it must
    // not be is invisible (548). `retrieval` is served rather than derived
    // here for `comparable`'s reason: a page that worked it out by matching
    // a command it is never shown against a program name it would have to
    // learn is a page carrying vocabulary it is supposed to be given.
    if ((route.retrieval || []).length) {
      say(t("models.route.mark.retrieval",
            { tools: (route.retrieval || []).join(", ") }));
    }
    // **A model the server's CLI is too old to run** (661). Served, not
    // derived: the server read the CLI's version off its install and holds
    // the table of minimums, and the page only says what it was told.
    const old = cliTooOld(route, route.model);
    if (old) say(t("models.route.mark.cli_old", old));
  }
  // **The level this row's figures were measured at** (613). The effort
  // slider shows figures from other levels for the same model, and a row
  // that named none would read as true of all of them.
  if (model.measured && model.measured.merge_effort) {
    say(t("models.route.mark.effort",
          { level: effortName(String(model.measured.merge_effort)) }));
  }
  // **Figures for a model the alias no longer answers as** (661): the row's
  // numbers stay, named as the model they were measured on (675: by its
  // catalogue name, "measured on Claude Opus 5"), and the reason, with the
  // ranking rule, one hover or one Tab away.
  const entry = routeEntry(route);
  if (measuredOnOtherModel(model)) {
    const before = entry.measured_by_effort && entry.measured_by_effort.safe_mode === false;
    marks.push({ text: t(before ? "models.route.mark.history.before_safe_mode"
                                : "models.route.mark.history",
                         { model: catalogueModelName(String(entry.resolved_model)) }),
                 why: "models.route.mark.history.why", hook: "history-why" });
  }
  return marks;
}

/**
 * A row's markers as one line, `·` between them (638).
 *
 * A marker with a `why` is its own focusable span: `title` for a pointer,
 * `aria-describedby` for a screen reader, at `describedBy`, a hidden element
 * in the same table's surroundings that holds the same sentence.
 * @param {{text: string, why?: string, hook?: string}[]} marks
 * @param {string} describedBy the id of that hidden element
 * @returns {HTMLSpanElement}
 */
function markLine(marks, describedBy) {
  const line = document.createElement("span");
  line.className = "model-meta route-note";
  marks.forEach((mark, i) => {
    if (i) line.appendChild(document.createTextNode(" \u00b7 "));
    const piece = document.createElement("span");
    setText(piece, mark.text);
    if (mark.why) {
      piece.className = "route-mark explained";
      piece.title = t(mark.why);
      piece.setAttribute("tabindex", "0");
      piece.setAttribute("aria-describedby", describedBy);
      // A marker explained by a sentence of its own points at that sentence's
      // hidden copy in the same table (675): `<hook>-picker`, `<hook>-scorecard`.
      if (mark.hook) {
        piece.setAttribute("aria-describedby",
          describedBy.replace("incomparable-why", mark.hook));
      }
    }
    line.appendChild(piece);
  });
  return line;
}

/**
 * "measured on the free tier", for a row whose figures were, or "" (632).
 *
 * Not a `routeMarks` addition: that function's markers belong to a command
 * route (`routeOf(model)`), and a free-tier row is answered over an ordinary
 * endpoint, badged `metered API` correctly -- a paid key at the same address
 * is billed per token, so the endpoint kind is not what changed. What changed
 * is what these particular figures cost to make, and that is a fact about
 * the row rather than about its route, so it is checked and shown on every
 * row the catalogue marks `measured.billed: "free-tier"` (625), independent
 * of `routeOf`.
 * @param {any} model
 * @returns {string}
 */
function freeTierNote(model) {
  return model && model.measured && model.measured.billed === "free-tier"
    ? t("models.route.mark.freetier") : "";
}

/**
 * Append `freeTierNote`'s line to a name cell, right under the badge -- the
 * one place both `pickerRow` and `scorecardRow` put a row's other markers,
 * so a reader who has learned to look there for what a badge does not say
 * finds this one too.
 * @param {HTMLElement} name
 * @param {any} model
 */
function appendFreeTierNote(name, model) {
  const text = freeTierNote(model);
  if (!text) return;
  const note = document.createElement("span");
  note.className = "model-meta route-note";
  setText(note, text);
  name.appendChild(note);
}

/**
 * One picker row: the radios, the name, one meta line and two figures (631).
 *
 * The meta line is the route's markers on a command row -- the retrieval
 * grant must never be invisible where the row is picked (548) -- and the
 * provider on every other row, so two rows for one model are told apart by
 * where they go. The two figures are the cost cell, whose words for a plan,
 * a free tier and GPU minutes are `costCell`'s own, and the silent-loss band:
 * silent loss is the defect this tool exists to find, and the column says
 * that is what it is rather than calling itself "quality". Every other figure
 * is in the scorecard.
 * @param {any} model
 * @returns {HTMLTableRowElement}
 */
function pickerRow(model) {
  const row = document.createElement("tr");
  const open = reachable(model) && !isRetired(model);
  row.appendChild(useCell(model, open));
  row.appendChild(checkCell(model, open));
  const name = document.createElement("td");
  name.appendChild(modelNameLine(model));
  let meta = document.createElement("span");
  if (routeOf(model)) {
    meta = markLine(routeMarks(model), "incomparable-why-picker");
  } else {
    // Where it goes and what it is asked for: the provider, and the wire
    // name `chosenModel` sends, each kept whole with the one space between
    // them as the only break (565). A listed row's name already is its wire
    // name, so it is not said twice.
    meta.className = "model-meta mono model-wire";
    const parts = [String(model.provider || "")];
    if (wireName(model) !== String(model.display_name || "")) parts.push(wireName(model));
    const shown = parts.filter(Boolean);
    shown.forEach((/** @type {string} */ part, /** @type {number} */ i) => {
      if (i) meta.appendChild(document.createTextNode(" "));
      const piece = document.createElement("span");
      setText(piece, part + (i < shown.length - 1 ? " \u00b7" : ""));
      meta.appendChild(piece);
    });
  }
  if (meta.firstChild) name.appendChild(meta);
  appendFreeTierNote(name, model);
  row.appendChild(name);
  row.appendChild(costCell(model));
  // Seconds and deviations, back on the main page (655): 631 moved every
  // figure but cost and silent loss to the scorecard on the operator's "only
  // runnable models" ruling, not on a request to drop columns, and that was
  // an overreach. Band only, as silent loss already was: the raw number and
  // the test count it was formed over stay in the scorecard, so this row's
  // height does not change.
  row.appendChild(bandOnlyCell(model.measured, "seconds_per_merge",
                               RANK_SCALES.seconds_per_merge));
  row.appendChild(bandOnlyCell(model.measured, "silent_loss_per_pair",
                               RANK_SCALES.silent_loss_per_pair));
  row.appendChild(bandOnlyCell(model.measured, "deviations_per_pair",
                               RANK_SCALES.deviations_per_pair));
  return row;
}

/**
 * A figure's band word and colour and nothing else, or the word for none.
 *
 * The picker's second figure (631): the number itself, and the pair count it
 * was formed over, are in the scorecard. An unmeasured figure is uncoloured
 * and says so, never a band.
 * @param {any} measured
 * @param {string} field
 * @param {{good: number, poor: number, ideal?: number, poorInclusive?: boolean}} scale
 * @returns {HTMLTableCellElement}
 */
function bandOnlyCell(measured, field, scale) {
  const cell = document.createElement("td");
  cell.className = "num";
  const name = band(measured ? measured[field] : null, scale);
  if (!name) {
    cell.classList.add("unmeasured");
    setText(cell, t("models.unmeasured"));
    return cell;
  }
  rankCell(cell, name);
  return cell;
}

/* ------------------------------------------------------------------ */
/* the model scorecard (631)                                           */
/* ------------------------------------------------------------------ */

/**
 * The id prefix of a catalogue command route this server does not serve.
 * Its own prefix, so it can never be taken for a served route's row, which
 * `COMMAND_PREFIX` names and `chosenRoute` reads.
 */
const UNSERVED_PREFIX = "catalogue-route:";

/**
 * Every row the scorecard shows: every catalogue model and every route (631).
 *
 * `pickable`'s rows without the ones an endpoint listed -- those carry no
 * figures and are in the picker -- and, after the served command routes,
 * every catalogue command route this server does not serve, matched on id,
 * model and profile as `routeFigures` matches. A configured row and one with
 * no endpoint are both here; the scorecard is the whole catalogue.
 * @returns {any[]}
 */
function scorecardRows() {
  const rows = pickable().filter((/** @type {any} */ model) => !model.listed);
  const served = commandRoutes();
  const block = (store.config.catalogue && store.config.catalogue.command_routes) || [];
  const unserved = block.filter((/** @type {any} */ entry) => !served.some(
    (/** @type {any} */ route) => route.id === entry.route
      && route.model === entry.model && route.profile === entry.profile))
    .map((/** @type {any} */ entry) => ({
      id: UNSERVED_PREFIX + entry.route,
      api_model: entry.model || "",
      display_name: routeNameNow(entry),
      provider: null,
      context_window: null,
      measured: entry.measured || null,
      notes: entry.notes || "",
      // A subscription profile is a flat-rate plan, the same reading
      // `routeKind` makes, so its cost cell is the plan's word; a route with
      // any other profile has no cost word to borrow and says unmeasured.
      command: { id: entry.route, model: entry.model, profile: entry.profile,
                 cost: entry.profile === ROUTE_SUBSCRIPTION ? "plan" : "",
                 unserved: true },
    }));
  const after = rows.findIndex((/** @type {any} */ model) => !routeOf(model));
  const at = after < 0 ? rows.length : after;
  return rows.slice(0, at).concat(unserved, rows.slice(at));
}

/**
 * The catalogue's `notes` for a row, or "".
 *
 * A catalogue row carries its own; a served command route's are on the
 * `command_routes` entry it matches, id, model and profile together.
 * @param {any} model
 * @returns {string}
 */
function rowNotes(model) {
  if (model.notes) return String(model.notes);
  const route = routeOf(model);
  if (!route) return "";
  const block = (store.config.catalogue && store.config.catalogue.command_routes) || [];
  const entry = block.find((/** @type {any} */ row) => row.route === route.id
    && row.model === route.model && row.profile === route.profile);
  return entry && entry.notes ? String(entry.notes) : "";
}

/**
 * The columns the scorecard sorts on, and the measured fields each one reads,
 * in order: a later field breaks a tie on an earlier one.
 *
 * `loss` is quality: silent loss per pair first, deviations per pair second.
 * Rates, never the raw counts, for `RANK_SCALES`' reason: the rows were
 * measured over different numbers of pairs. `name` reads no figure.
 * @type {Record<string, string[]>}
 */
const SCORECARD_SORTS = {
  name: [],
  cost: ["usd_per_merge"],
  speed: ["seconds_per_merge"],
  loss: ["silent_loss_per_pair", "deviations_per_pair"],
  deviations: ["deviations_per_pair"],
};

/**
 * Each sort column's header hook, button hook and tooltip key, written out so
 * every hook and key is a literal the markup and catalogue checks can see.
 * @type {Record<string, {head: string, control: string, title: string}>}
 */
const SCORECARD_SORT_HEADS = {
  name: { head: "sort-head-name", control: "sort-name", title: "scorecard.sort.name" },
  cost: { head: "sort-head-cost", control: "sort-cost", title: "scorecard.sort.cost" },
  speed: { head: "sort-head-speed", control: "sort-speed", title: "scorecard.sort.speed" },
  loss: { head: "sort-head-loss", control: "sort-loss", title: "scorecard.sort.loss" },
  deviations: { head: "sort-head-deviations", control: "sort-deviations",
                title: "scorecard.sort.perpair" },
};

/**
 * The picker's sortable headers (635, 655): the same columns, hooks of their
 * own. The Use and Check columns hold radios and do not sort.
 * @type {Record<string, {head: string, control: string, title: string}>}
 */
const PICKER_SORT_HEADS = {
  name: { head: "picker-sort-head-name", control: "picker-sort-name", title: "scorecard.sort.name" },
  cost: { head: "picker-sort-head-cost", control: "picker-sort-cost", title: "scorecard.sort.cost" },
  speed: { head: "picker-sort-head-speed", control: "picker-sort-speed", title: "scorecard.sort.speed" },
  loss: { head: "picker-sort-head-loss", control: "picker-sort-loss", title: "scorecard.sort.loss" },
  deviations: { head: "picker-sort-head-deviations", control: "picker-sort-deviations",
                title: "scorecard.sort.perpair" },
};

/**
 * One table's sort (631, 635): a key of `SCORECARD_SORTS` and a direction,
 * or "" for the served order, with the headers it paints, where it is kept
 * per browser, and what redraws the table. A per-viewer convenience, not
 * form state, so "Start over" leaves it alone.
 *
 * **One sorter, two states.** The scorecard and the picker share
 * `scorecardOrder`, `sortFigure` and the functions below; each keeps its own
 * key and direction under its own storage key, so sorting one never sorts
 * the other.
 * @typedef {{key: string, direction: string, storage: string,
 *            heads: Record<string, {head: string, control: string, title: string}>,
 *            render: () => void}} SortState
 */

/** @type {SortState} */
const scorecardSort = { key: "", direction: "", storage: "llossless.scorecard.sort",
                        heads: SCORECARD_SORT_HEADS, render: () => renderScorecard() };

/** @type {SortState} */
const pickerSort = { key: "", direction: "", storage: "llossless.picker.sort",
                     heads: PICKER_SORT_HEADS, render: () => renderPickerRows() };

/**
 * Read a table's kept sort, and keep the served order when there is none.
 * @param {SortState} state
 */
function loadSort(state) {
  try {
    const raw = window.localStorage.getItem(state.storage);
    const kept = raw ? JSON.parse(raw) : null;
    if (kept && Object.prototype.hasOwnProperty.call(state.heads, kept.key)
        && (kept.direction === "ascending" || kept.direction === "descending")) {
      state.key = kept.key;
      state.direction = kept.direction;
    }
  } catch (error) {
    // Blocked or absent storage: the page sorts and forgets.
  }
}

/**
 * Keep a table's sort for this browser, if it will keep anything.
 * @param {SortState} state
 */
function rememberSort(state) {
  try {
    window.localStorage.setItem(state.storage,
      JSON.stringify({ key: state.key, direction: state.direction }));
  } catch (error) {
    // As above: the sort still applies, it is only not remembered.
  }
}

/**
 * One row's figure for a sort field, or null when it has none.
 *
 * **Null is not zero.** A route's cost is its plan's word, a self-hosted row
 * bills GPU minutes, a free tier billed nothing and an unmeasured row was
 * never run: none of them is a price, and `pricing.py`'s rule is that an
 * unmeasured figure is never $0.00. `scorecardOrder` puts every null last.
 * @param {any} model
 * @param {string} field
 * @returns {number|null}
 */
function sortFigure(model, field) {
  if (field === "usd_per_merge" && routeOf(model)) return null;
  const measured = model && model.measured;
  const value = measured ? measured[field] : null;
  return typeof value === "number" && isFinite(value) ? value : null;
}

/**
 * A table's rows in the order `key` and `direction` ask for: the scorecard's
 * and, since 635, the picker's, through this one function.
 *
 * Retired rows after every live row, whichever way. Within each, a row with
 * no figure for a field sorts after every row that has one **in both
 * directions**: reversing a column reverses the measured rows and never
 * brings the unmeasured ones to the top. Ties keep the served order, so the
 * sort is stable. An unknown key is the served order.
 *
 * **Figures measured on a model the route no longer runs** (675,
 * `measuredOnOtherModel`) sort after every row that has a figure of its own
 * for the field, in both directions, and before the rows that have none:
 * they are not the figures of the model a run gets today, so they never
 * rank among those, and they are still measured figures, so they do not
 * read as unmeasured either. The name sort reads no figure and ignores it.
 * @param {any[]} rows
 * @param {string} key
 * @param {string} direction "ascending" or "descending"
 * @returns {any[]}
 */
function scorecardOrder(rows, key, direction) {
  const fields = SCORECARD_SORTS[key];
  if (!fields) return rows.slice();
  const sign = direction === "descending" ? -1 : 1;
  const indexed = rows.map((/** @type {any} */ model, /** @type {number} */ i) => ({ model, i }));
  indexed.sort((/** @type {any} */ a, /** @type {any} */ b) => {
    const retired = Number(isRetired(a.model)) - Number(isRetired(b.model));
    if (retired) return retired;
    if (key === "name") {
      const byName = String(a.model.display_name || a.model.id || "").localeCompare(
        String(b.model.display_name || b.model.id || ""), locale.tag || undefined,
        { sensitivity: "base", numeric: true });
      if (byName) return sign * byName;
    }
    const other = Number(measuredOnOtherModel(a.model)) - Number(measuredOnOtherModel(b.model));
    for (const field of fields) {
      const left = sortFigure(a.model, field);
      const right = sortFigure(b.model, field);
      if (left === null && right === null) continue;
      if (left === null) return 1;
      if (right === null) return -1;
      if (other) return other;
      if (left !== right) return sign * (left - right);
    }
    return a.i - b.i;
  });
  return indexed.map((/** @type {any} */ entry) => entry.model);
}

/**
 * `aria-sort` on every sortable header of one table, and each tooltip.
 *
 * The one writer of both, so the state a screen reader announces is the
 * order on screen.
 * @param {SortState} state
 */
function paintSortHeads(state) {
  for (const key of Object.keys(state.heads)) {
    const hooks = state.heads[key];
    el(hooks.head).setAttribute("aria-sort",
      state.key === key ? state.direction : "none");
    el(hooks.control).title = t(hooks.title);
  }
}

/**
 * Every figure column's help icon, on both tables: its hook and the
 * catalogue key for what it explains (655). Not "Model" or "Use"/"Check" --
 * those are not a figure -- and one key per meaning, carried by two icons
 * (a picker one and a scorecard one) because the dialog is a second subtree
 * with its own hidden paragraph for `aria-describedby` to reach.
 * @type {{icon: string, key: string}[]}
 */
const COLUMN_HELP = [
  { icon: "help-picker-cost", key: "models.help.cost" },
  { icon: "help-picker-speed", key: "models.help.speed" },
  { icon: "help-picker-loss", key: "models.help.loss" },
  { icon: "help-picker-deviations", key: "models.help.deviations_per_pair" },
  { icon: "help-scorecard-cost", key: "models.help.cost" },
  { icon: "help-scorecard-speed", key: "models.help.speed" },
  { icon: "help-scorecard-loss", key: "models.help.loss" },
  { icon: "help-scorecard-deviations", key: "models.help.deviations_per_pair" },
];

/**
 * `title` and `aria-label` on every column-help icon (655): the mouse half
 * of the pattern 638 set for a row marker, `aria-describedby` and the
 * hidden paragraph it points at being static markup that `applyStringsIn`
 * already keeps in the current language. Not `data-t` on the icon itself --
 * that would overwrite the visible "?" with the sentence. Static, so one
 * call after every locale change is enough -- unlike `paintSortHeads`,
 * nothing here depends on which rows are on screen or how they are sorted.
 */
function paintColumnHelp() {
  const label = t("models.help.icon.label");
  for (const { icon, key } of COLUMN_HELP) {
    const node = el(icon);
    node.title = t(key);
    node.setAttribute("aria-label", label);
  }
}

/**
 * A header was clicked: ascending first, then each click reverses (631).
 * @param {SortState} state
 * @param {string} key
 */
function sortBy(state, key) {
  if (!Object.prototype.hasOwnProperty.call(state.heads, key)) return;
  state.direction = state.key === key
    && state.direction === "ascending" ? "descending" : "ascending";
  state.key = key;
  rememberSort(state);
  state.render();
}

/**
 * The scorecard: every catalogue row with its measured figures, sorted (631).
 *
 * `deviations` is deliberately not shown. It is a raw count over each row's
 * own `pairs`, and two rows with different `pairs` cannot be compared by it --
 * the catalogue says so in its own `notes`. `deviations_per_pair` is the
 * figure that survives the comparison, so it is the one in the column, with
 * the pair count beside it as the denominator it came from.
 */
function renderScorecard() {
  const rows = scorecardOrder(scorecardRows(), scorecardSort.key, scorecardSort.direction);
  fill(el("model-rows"), rows.map((/** @type {any} */ model) => scorecardRow(model)));
  paintSortHeads(scorecardSort);
  renderRouteCaveats();

  // Hidden where this server has no command routes, which is the default and
  // is every deployment until an operator writes a file. A sentence about a
  // capability that is not there teaches a reader to skip the hints.
  el("commands-hint").hidden = commandRoutes().length === 0;

  // `/config` serves `catalogue.notes` in English, unconditionally -- it is
  // part of the served contract (643's reasoning: other clients may read
  // it) -- but the page no longer prints it as served (656). It reads
  // `models.catalogue.notes` instead, pinned equal to the shipped
  // catalogue's own text by `test_contract_parity`, so a German page reads
  // German rather than the vendor-neutral disclaimer a German reader cannot
  // parse. Still hidden when the catalogue carries none, a fork's own
  // possibility rather than left as a gap.
  const notes = store.config.catalogue && store.config.catalogue.notes;
  setText(el("catalogue-note"), notes ? t("models.catalogue.notes") : "");
  el("catalogue-note").hidden = !notes;
  setText(el("model-bands"), t("models.bands", {
    // Through `figure` so that the legend says $0.50 where the column says
    // $0.611, rather than the $0.5 a raw number would print.
    cheap: figure(RANK_SCALES.usd_per_merge.good, 2) || "",
    dear: figure(RANK_SCALES.usd_per_merge.poor, 2) || "",
    fast: RANK_SCALES.seconds_per_merge.good,
    slow: RANK_SCALES.seconds_per_merge.poor,
    clean: RANK_SCALES.deviations_per_pair.good,
    noisy: RANK_SCALES.deviations_per_pair.poor,
  }));
}

/**
 * One scorecard row: the name cell with everything said about the row, and
 * the four measured figures. No radios: the scorecard is read, the picker is
 * where a row is chosen.
 * @param {any} model
 * @returns {HTMLTableRowElement}
 */
function scorecardRow(model) {
  const row = document.createElement("tr");
  const live = reachable(model);
  // A retired row says why it cannot be picked, and the endpoint's remedy
  // is not it: configuring one would not make the row pickable again.
  const unconfigured = !live && !isRetired(model);
  if (unconfigured) row.classList.add("unreachable");
  if (isRetired(model)) row.classList.add("retired");
  if (unconfigured) {
    // The remedy, on the row itself. `models.unreachable` names the state and
    // `models.unreachable.blocked` names the fix. `title` is a poor primary
    // channel, which is why the state is still said in words in the cell
    // below; this is the answer to the question a greyed row provokes.
    row.title = t("models.unreachable.blocked", {
      name: String(model.display_name || model.id || ""),
      provider: String(model.provider || ""),
    });
  }

  const name = document.createElement("td");
  name.appendChild(modelNameLine(model));
  const meta = document.createElement("span");
  meta.className = "model-meta mono model-wire";
  const window = figure(model.context_window);
  const route = routeOf(model);
  // The wire name, not the catalogue id. They differ on four of the six
  // shipped rows, and the one an operator has to recognise is the one the
  // endpoint is actually asked for: `claude-haiku-4-5` is a label this
  // catalogue made up, `claude-haiku-4-5-20251001` is the model.
  //
  // A command route's model is the one its route states, and a route that
  // states none is refused on read -- `commands._row`, on the operator's
  // rule that relying on the app default is not strategy. So there is no
  // unstated case left to render: the line names the model the program will
  // be told to use.
  //
  // **Two unbreakable halves with one place to break between them** (565).
  // Wrapping the whole line would let the browser break a model id at its
  // hyphens, and a wire name split as `claude-haiku-` / `4-5-20251001` is a
  // different string to the reader who has to type it. So the id and the
  // window are each kept whole, and the one space between them is the only
  // break.
  const wire = document.createElement("span");
  setText(wire, (route ? route.model : wireName(model))
    + (window ? " ·" : ""));
  meta.appendChild(wire);
  if (window) {
    meta.appendChild(document.createTextNode(" "));
    const size = document.createElement("span");
    setText(size, t("models.window", { n: window }));
    meta.appendChild(size);
  }
  name.appendChild(meta);
  // **When, and by which build, this row's figures were measured** (618).
  // The table holds rows measured on different days by different commits
  // of this tool, and a figure with no date reads as current. Its own line,
  // allowed to wrap between the date and the commit, so it can never widen
  // the column.
  const when = measuredWhen(model.measured);
  if (when) {
    const line = document.createElement("span");
    line.className = "model-meta measured-when";
    setText(line, when);
    name.appendChild(line);
  }
  // **Markers here, and the sentences they stand for once under the table**
  // (531). A subscription row genuinely is not comparable to the measured
  // figures, and it genuinely is shared by everybody on this instance; the
  // full sentences are `renderRouteCaveats`', below the table, for every
  // marker actually on a row. Not a `title` tooltip: hover does not exist on
  // touch and is not reliably announced.
  const marks = routeMarks(model);
  if (marks.length) name.appendChild(markLine(marks, "incomparable-why-scorecard"));
  // A free-tier row (632): its own line rather than folded into `marks`,
  // since `routeMarks` is a command route's own markers and this is true of
  // an ordinary metered row just as much.
  appendFreeTierNote(name, model);
  // **A retired row says so, dated** (618). Its figures stay, because they
  // were measured; this line says why it can no longer be picked and what
  // to use instead. Words, not a colour, for the reason below.
  if (isRetired(model)) {
    const retired = document.createElement("span");
    retired.className = "model-meta retired-why";
    setText(retired, retiredSentence(model.retired));
    name.appendChild(retired);
  }
  if (unconfigured) {
    // Said in words, never by the row merely looking different. A state
    // this page signals with colour alone is a state half its readers are
    // never told about, which is the rule `rankCell` and the chips follow.
    const why = document.createElement("span");
    why.className = "model-meta unreachable-why";
    setText(why, t("models.unreachable", { provider: String(model.provider || "") }));
    name.appendChild(why);
  }
  // The catalogue's own notes for the row, closed: they are paragraphs, and
  // a cell that opened on them would be the wall of text this dialog exists
  // to hold rather than show. English, as the catalogue is -- a measurement
  // record (who ran it, at which commit, over how many pairs), not page
  // prose, so it stays English rather than being translated (656). `lang`
  // marks that for a screen reader, which is invisible to everyone else, so
  // on a page in any other language the summary also says so in words --
  // closed or open, never merely by the paragraph's language attribute --
  // rather than reading like a translation somebody forgot.
  const notes = rowNotes(model);
  if (notes) {
    const fold = document.createElement("details");
    fold.className = "row-notes";
    const summary = document.createElement("summary");
    const label = locale.tag && locale.tag !== "en"
      ? t("scorecard.notes") + " " + t("scorecard.notes.foreign")
      : t("scorecard.notes");
    setText(summary, label);
    const text = document.createElement("p");
    text.lang = "en";
    setText(text, notes);
    fold.appendChild(summary);
    fold.appendChild(text);
    name.appendChild(fold);
  }
  row.appendChild(name);

  const measured = model.measured;
  row.appendChild(costCell(model));
  row.appendChild(measuredCell(measured, "seconds_per_merge", 1, "",
                               RANK_SCALES.seconds_per_merge));
  row.appendChild(silentLossCell(measured));
  row.appendChild(deviationCell(measured));
  return row;
}

/**
 * Where each measured column's three bands begin, lower being better in all
 * four.
 *
 * `good` is the highest value still good and `poor` is the highest value still
 * fair, so a scale is two numbers rather than four and the bands cannot
 * overlap or leave a gap between them.
 *
 * The numbers are chosen against the spread the shipped catalogue actually
 * holds, and `tests/test_web_static.py` asserts every band has at least one
 * row in it. A band no model occupies is a colour the table can never show,
 * which makes the legend describe a scale that is not the one being applied.
 *
 * Two of the four are **rates, not counts**. `silent_loss` and `deviations`
 * are raw totals over each row's own `pairs`, and the rows were measured over
 * different numbers of pairs -- nine for the hosted models, two and three for
 * the self-hosted ones -- so ranking either on the raw number would rank the
 * sample size. The catalogue publishes `deviations_per_pair` for exactly that
 * reason and its own `notes` say so; silent loss has no published rate, so the
 * band is taken on `silent_loss / pairs`, which is the same arithmetic over
 * the same denominator the catalogue used for the other one.
 * @type {Record<string, {good: number, poor: number, ideal?: number, poorInclusive?: boolean}>}
 */
const RANK_SCALES = {
  // Under a quarter of a dollar a merge is good and over half a dollar is
  // poor. Round money rather than quantiles of six rows: a scale fitted to
  // this catalogue would move every time a row was added.
  usd_per_merge: { good: 0.25, poor: 0.5 },
  // Two minutes and five minutes, which is how a person waiting reads a
  // duration. The catalogue's own spread runs from a minute to eleven.
  seconds_per_merge: { good: 120, poor: 300 },
  // None at all is the only good answer -- silent loss is the defect this
  // tool exists to find -- and averaging one or more per pair is poor. None
  // is also the column's ideal, so it reads "excellent" (598) and nothing on
  // this scale is "good": a positive rate goes straight to fair.
  silent_loss_per_pair: { good: 0, poor: 1, ideal: 0 },
  // Ruling 16 (2026-09-28): anchored to the mechanical-union floor DECISIONS
  // 684 N5 defines, not to where the catalogue's own rows happen to sit
  // (682's rule, which this replaces). `poor` starts AT the floor -- a merge
  // no better than gluing the two sources together mechanically is poor, not
  // fair -- and `good` is at or below half the floor; `fair` is the gap
  // between. Halving is the only floor-derived split available with no
  // second reference point, so it is the rule rather than a second
  // measurement.
  // GENERATED by `python3 tests/rank_scale_floor.py --write` from
  // `lineup_figures.baselines`/`_floor` over the nine registered pairs
  // (`run_lineup.PAIRS`, base `source_a.md`), scored with no model call;
  // `--check` fails if this drifts from the recomputed floor. Do not edit the
  // numbers by hand. A merge that matched the reference exactly would still
  // sit at 0, the ideal.
  deviations_per_pair: { good: 3.89, poor: 7.78, poorInclusive: true, ideal: 0 },
};

/**
 * The `provider` a row carries when there is no per-token price to report.
 *
 * `catalogue.py` states the rule -- a self-hosted model never gets a real
 * `usd_per_merge`, because that hardware bills per minute of wall clock and a
 * per-merge dollar figure would need a utilisation rate nobody knows. The
 * consequence for this page is that `null` in that cell means two different
 * things depending on the row, and `costCell` has to tell them apart.
 */
const SELF_HOSTED = "self-hosted";

/**
 * What a command route's row is called in the one list.
 *
 * Every row in the picker is a **route to a model**, never a bare model name,
 * and that is the whole presentation decision behind this milestone: `Opus 5 -
 * API (metered)` and `Opus 5 - Subscription` are two rows a reader can see at
 * once, and a model picker with a route toggle beside it is a second piece of
 * state to misread. The prefix is what lets one `store.mergeModel` hold either
 * kind, so there is exactly one selection on this page and nothing to keep in
 * step with anything else.
 *
 * A colon, which `commands.ROUTE_ID` cannot contain, so a route id can never
 * collide with a catalogue id and a catalogue id can never be read as a route.
 */
const COMMAND_PREFIX = "command:";

/**
 * The three kinds of route a row can be, in the words the button uses.
 *
 * Not the model, and never inferred from a model name. What a reader is
 * choosing between is *how the run is paid for*, which is a property of the
 * destination: a metered API bills per token, a subscription counts against a
 * plan, and a self-hosted endpoint bills GPU minutes. Those are the three
 * sentences `costCell` already tells apart, said once on the control that
 * commits the money.
 */
const ROUTE_METERED = "metered";
const ROUTE_SUBSCRIPTION = "subscription";
const ROUTE_COMMAND = "command";
const ROUTE_SELFHOSTED = "selfhosted";

/**
 * The fifth, which is not a route but an answer: *this page cannot tell*.
 *
 * It exists so that nothing falls through to one of the four. The button used
 * to read `Merge and check - metered API` whenever the selection matched no
 * row in the picker, which is a sentence about where the money goes, asserted
 * from an absence. The operator's rule is the right one and is worth stating:
 * naming *every* case is what makes the naming trustworthy, because a label
 * that appears for some routes and not others teaches a reader that its
 * absence means nothing in particular.
 */
const ROUTE_UNKNOWN = "unknown";

/**
 * Every route kind, and the catalogue key each one reads under.
 *
 * **Written out rather than built with `"route." + kind`.** Two things follow
 * from that and both are the point. `test_web_static.keys_named_in_js` sees a
 * literal key and cannot see a concatenation, so these five are checked
 * against both catalogues by name instead of by the weaker "something under
 * this prefix exists" rule a family gets. And `routeLabel` cannot render a
 * kind that is missing from the table, because there is no expression in it
 * that builds a key.
 * @type {Record<string, string>}
 */
const ROUTE_LABEL_KEYS = {
  metered: "route.metered",
  subscription: "route.subscription",
  command: "route.command",
  selfhosted: "route.selfhosted",
  unknown: "route.unknown",
};

/**
 * Every kind `routeKind` and `chosenRouteKind` are allowed to answer with.
 *
 * The check below is the guard the operator asked for: a fifth route class
 * added to the constants and not to the table fails when this file loads,
 * rather than shipping a button with a blank where the route should be. It is
 * the pattern `merge.MAY_CHOOSE` and `report.FINDING_ORDER` use on the Python
 * side -- `assert set(X) == set(Y)` at import -- and it is a `throw` here for
 * the same reason it is an `assert` there: a page that renders a run's
 * destination wrong is worse than a page that does not render.
 */
const ROUTE_KINDS = [ROUTE_METERED, ROUTE_SUBSCRIPTION, ROUTE_COMMAND,
                     ROUTE_SELFHOSTED, ROUTE_UNKNOWN];

(function checkRouteLabelsAreExhaustive() {
  const declared = ROUTE_KINDS.slice().sort().join(",");
  const mapped = Object.keys(ROUTE_LABEL_KEYS).sort().join(",");
  if (declared !== mapped) {
    throw new Error("every route kind must have a label: ROUTE_KINDS is ["
                    + declared + "] and ROUTE_LABEL_KEYS is [" + mapped + "]");
  }
})();

/**
 * What one route kind is called, in the reader's language. **Total.**
 *
 * The one place a route kind becomes a sentence, and it throws on a kind it
 * has never been told about rather than answering with the empty string. An
 * unlabelled button is the state this function exists to remove, so producing
 * one quietly is the one behaviour it must not have.
 * @param {string} kind one of `ROUTE_KINDS`
 * @returns {string}
 */
function routeLabel(kind) {
  const key = ROUTE_LABEL_KEYS[kind];
  if (!key) throw new Error("no label for route kind " + String(kind));
  return t(key);
}

/**
 * Which band a figure falls in, or "" for no band at all.
 *
 * `""` for anything that is not a finite number, which is what makes the
 * unmeasured case uncolourable rather than merely uncoloured by convention:
 * `rankCell` paints nothing when handed `""`, so an absent measurement cannot
 * reach a colour through any call site. Shading a missing figure green or red
 * would be a judgement invented out of an absence, which is this project's
 * most repeated failure and is the same rule the `notchecked` chip follows.
 *
 * **"excellent" is the ideal and nothing else** (598): a figure exactly at its
 * column's `ideal`, which only the two rate columns have -- no silent loss at
 * all, no deviation at all. Cost and speed have no ideal, so they never reach
 * it. Not "perfect": these figures come from a handful of pairs, and the word
 * must not claim more than a handful of pairs can show.
 * `poorInclusive` makes the poor boundary itself poor rather than fair --
 * `deviations_per_pair`'s scale sets it because 684 N5's floor is a value a
 * real row can land on exactly, and "poor" there means "at or worse than a
 * mechanical union", not "strictly worse". Every other scale leaves it unset
 * and keeps the plain `value > scale.poor` split.
 * @param {number|null|undefined} value
 * @param {{good: number, poor: number, ideal?: number, poorInclusive?: boolean}|undefined} scale
 * @returns {string} "excellent", "good", "fair", "poor", or ""
 */
function band(value, scale) {
  if (value === null || value === undefined || typeof value !== "number") return "";
  if (!isFinite(value)) return "";
  if (!scale) return "";
  if (scale.ideal !== undefined && value === scale.ideal) return "excellent";
  if (value <= scale.good) return "good";
  if (scale.poorInclusive ? value >= scale.poor : value > scale.poor) return "poor";
  return "fair";
}

/**
 * Paint one cell with its band, and say the band in a word beside the colour.
 *
 * The only place in this file that writes a `rank-` class, and it writes the
 * word in the same breath. Colour never carries meaning alone here --
 * `html_report.py` has held that rule since it was written and the chips
 * follow it -- so the two cannot be separated by a later edit to one call
 * site: there is one call site for both.
 * @param {HTMLElement} cell
 * @param {string} name one of `band`'s answers
 */
function rankCell(cell, name) {
  if (!name) return;
  cell.classList.add("rank-" + name);
  const word = document.createElement("span");
  word.className = "rank-word";
  setText(word, t("models.band." + name));
  cell.appendChild(word);
}

/**
 * Every row the picker offers: the measured catalogue, then what endpoints listed.
 *
 * Two sources and one list, because to an operator they are one question --
 * what can I run -- and a page with a measured table and a separate
 * discovered table would make them scroll to find out that the answer is in
 * the other one.
 *
 * A discovered row is `measured: null`, which is the catalogue's own word for
 * a model nobody has run through this tool. Nothing about it is estimated:
 * every figure column says "unmeasured" rather than borrowing a number from a
 * similarly-named row that was measured. That state was in `catalogue.py` from
 * the day it shipped and nothing had ever produced one until endpoints started
 * listing themselves, so this is also the first caller that puts it on screen.
 *
 * A listed name that a measured row already claims is dropped rather than
 * shown twice: the measured row is the same model with figures attached.
 * @returns {any[]}
 */
function pickable() {
  const measured = (store.config.catalogue && store.config.catalogue.models) || [];
  const rows = measured.slice();
  // The operator's command routes, first in the list. Order is the one signal
  // a list has before anything is read, and the row that does not cost money
  // per token belongs above the rows that do -- see `renderModels` for the
  // preselection, which is the same argument on the control that commits.
  //
  // `display_name` is the operator's label **verbatim**. Nothing here derives
  // a model name from a command: `commands.py` refuses a route without a
  // label precisely so that this line has something true to render, and
  // guessing that `claude` means Opus 5 is how a correct-looking screen
  // produces a wrong bill.
  //
  // `measured` is the catalogue's figures for this route when it has any
  // (`routeFigures`, 597) and otherwise null, the catalogue's own word for a
  // route nobody has run through this tool. Either way the route answers at a
  // rung the endpoint rows were not measured at, and `route.comparable`
  // carries that half, from the server.
  // **In the order the server gave them, which is not what a loop of
  // `unshift` produces.** Each call puts its row at the front, so iterating
  // cheapest-first and unshifting each one leaves the *dearest* at index 0 --
  // and `renderModels` preselects the first command route it finds. The page
  // therefore pointed at Fable while `describe()` was ordering for Haiku,
  // which is the one thing the operator asked not to happen. Found by reading
  // the preselected row back out of the browser.
  rows.unshift(...commandRoutes().map((/** @type {any} */ route) => ({
    id: COMMAND_PREFIX + route.id,
    api_model: route.model || "",
    display_name: route.label,
    provider: null,
    context_window: route.window,
    measured: routeFigures(route),
    command: route,
  })));
  const known = new Set(rows.map((/** @type {any} */ model) => wireName(model)));
  for (const provider of providerRows()) {
    for (const name of provider.models || []) {
      if (known.has(name)) continue;
      known.add(name);
      rows.push({
        id: provider.name + ":" + name,
        api_model: name,
        display_name: name,
        provider: provider.name,
        context_window: null,
        measured: null,
        listed: true,
      });
    }
  }
  return rows;
}

/**
 * The catalogue's measured block for one command route, or null (597).
 *
 * Matched on the route's id, its model alias and its profile together: the
 * figures describe that route running that model in that request shape, and
 * an operator's own route reusing an id for something else was not measured.
 * Null for a route the catalogue has no figures for, which the columns render
 * as "unmeasured" -- the `claude-fable` route, deliberately never run.
 * @param {any} route
 * @returns {any}
 */
function routeFigures(route) {
  const block = (store.config.catalogue && store.config.catalogue.command_routes) || [];
  const entry = block.find((/** @type {any} */ row) => row.route === route.id
    && row.model === route.model && row.profile === route.profile);
  return (entry && entry.measured) || null;
}

/* ------------------------------------------------------------------ */
/* the merge effort slider (613)                                       */
/* ------------------------------------------------------------------ */

/**
 * The two test documents the per-effort figures were measured on, in the
 * order the card lists them. A pair the catalogue carries that is not named
 * here is not shown: the card has a sentence for each of these and none for
 * a pair it has never been told about.
 */
const EFFORT_PAIRS = ["voyager", "bip39"];

/**
 * The picked command route's own served row, or null.
 * @returns {any}
 */
function chosenRouteRow() {
  const id = chosenRoute();
  if (!id) return null;
  return commandRoutes().find((/** @type {any} */ route) => route.id === id) || null;
}

/**
 * The catalogue's per-effort figures for one command route, or null (613).
 *
 * Matched as `routeFigures` matches: the route's id, its model alias and its
 * profile together. Null for a route nobody ran the grid through -- Fable,
 * or an operator's own route -- and every level then reads unmeasured.
 * @param {any} route
 * @returns {any}
 */
function routeEffortFigures(route) {
  const block = (store.config.catalogue && store.config.catalogue.command_routes) || [];
  const entry = block.find((/** @type {any} */ row) => route && row.route === route.id
    && row.model === route.model && row.profile === route.profile);
  return (entry && entry.measured_by_effort) || null;
}

/**
 * The catalogue's figures for models this route's program was pinned to by
 * full id rather than through the route's own alias (661), or `[]`.
 *
 * Matched as `routeEffortFigures` matches. Each block names the id it asked
 * for and the id that answered; the card shows each under its own heading,
 * so figures for one model are never read as the route's.
 * @param {any} route
 * @returns {any[]}
 */
function routePinnedFigures(route) {
  const block = (store.config.catalogue && store.config.catalogue.command_routes) || [];
  const entry = block.find((/** @type {any} */ row) => route && row.route === route.id
    && row.model === route.model && row.profile === route.profile);
  return (entry && Array.isArray(entry.pinned_by_effort)) ? entry.pinned_by_effort : [];
}

/**
 * The catalogue's `command_routes` entry for a route, or null, matched as
 * `routeFigures` matches.
 * @param {any} route
 * @returns {any}
 */
function routeEntry(route) {
  const block = (store.config.catalogue && store.config.catalogue.command_routes) || [];
  return block.find((/** @type {any} */ row) => route && row.route === route.id
    && row.model === route.model && row.profile === route.profile) || null;
}

/**
 * What the route's alias answers as now, when that is no longer the model its
 * own figures were measured on (661), or null. Then those figures are history
 * and the pinned block for the new model, if the card has one, comes first.
 * @param {any} route
 * @returns {{model: string, checked_on: string, cli_version: string}|null}
 */
function aliasNow(route) {
  const entry = routeEntry(route);
  return (entry && entry.alias_now && entry.alias_now.model) ? entry.alias_now : null;
}

/**
 * The model id this route's figures are current for right now (704, 708):
 * `alias_now.model` when the alias has moved past what the route's own
 * `measured`/`measured_by_effort` were measured on, else the route's own
 * `resolved_model`. A route with no `alias_now` is not a route with no
 * current model: it is one whose alias and `resolved_model` already
 * agree, which is the ordinary case (`aliasNow`'s own docstring) and, since
 * 708, the opus route's: its `measured_by_effort` grid and `alias_now` are
 * gone together, leaving `resolved_model` itself as the only source of
 * "what this route runs today". A pinned block (661) whose own
 * `resolved_model` matches this is the figures for that model, wherever the
 * answer came from, an alias check or the route's own measurement,
 * rather than only where `alias_now` happens to be set.
 * @param {any} route
 * @returns {string}
 */
function currentRouteModel(route) {
  const now = aliasNow(route);
  const entry = routeEntry(route);
  return now ? String(now.model) : String((entry && entry.resolved_model) || "");
}

/**
 * A model id's name from the catalogue's own `models` row, matched on `id` or
 * `api_model`, or the id itself when no row names it (675). Never a name
 * typed for the occasion: the next alias move then needs only `alias_now`.
 * @param {string} id
 * @returns {string}
 */
function catalogueModelName(id) {
  const rows = (store.config.catalogue && store.config.catalogue.models) || [];
  const row = rows.find((/** @type {any} */ m) => m.id === id || m.api_model === id);
  return row && row.display_name ? String(row.display_name) : String(id || "");
}

/**
 * A catalogue route's name today (675): after the model its alias answers as
 * now when `alias_now` says that moved -- that model's catalogue name and the
 * route's suffix, "Claude Opus 5.5 (subscription)" -- and otherwise the
 * entry's stored `display_name`, which stays in the file as what the figures
 * were measured on.
 * @param {any} entry a `command_routes` entry
 * @returns {string}
 */
function routeNameNow(entry) {
  const now = entry && entry.alias_now && entry.alias_now.model;
  if (!now) return String((entry && (entry.display_name || entry.route)) || "");
  const name = catalogueModelName(String(now));
  return entry.profile === ROUTE_SUBSCRIPTION ? t("models.route.name", { model: name }) : name;
}

/**
 * Whether a command row's figures were measured on a model its alias no
 * longer answers as (661, 675): the entry's `resolved_model` differs from
 * `alias_now.model` and the row has figures. Such a row is marked "measured
 * on <that model>" and ranks after every current figure (`scorecardOrder`).
 * @param {any} model a picker or scorecard row
 * @returns {boolean}
 */
function measuredOnOtherModel(model) {
  const route = routeOf(model);
  const entry = route ? routeEntry(route) : null;
  return Boolean(entry && entry.alias_now && entry.alias_now.model && entry.resolved_model
    && entry.alias_now.model !== entry.resolved_model && (model.measured || entry.measured));
}

/**
 * `{needs, found}` when the server's CLI for this route is older than `model`
 * requires (661), or null. Only ever the server's own answer: `cli_too_old`
 * lists the models the version its install names falls short of, and
 * `cli_version` is that version.
 * @param {any} route
 * @param {string} model
 * @returns {{needs: string, found: string}|null}
 */
function cliTooOld(route, model) {
  const hit = ((route && route.cli_too_old) || [])
    .find((/** @type {any} */ row) => row.model === model);
  return hit ? { needs: String(hit.needs), found: String(route.cli_version || "") } : null;
}

/**
 * A ratio as a person says it: whole above one and a half, one place below.
 * @param {number} ratio
 * @returns {string}
 */
function timesText(ratio) {
  return ratio >= 1.5 ? (figure(Math.round(ratio)) || "") : (figure(ratio, 1) || "");
}

/**
 * `max` against the level below it in the same block, in plain words (661):
 * whether it fixed more, the same or fewer, by the ranges' overlap rule the
 * grid registered (609), and how much more time and usage it took. Null when
 * the block does not carry both levels for a pair the card shows.
 * @param {any} block
 * @param {string} level
 * @param {string} lower
 * @returns {string|null}
 */
function effortComparison(block, level, lower) {
  const at = block && block.levels ? block.levels[level] : null;
  const below = block && block.levels ? block.levels[lower] : null;
  if (!at || !below || !at.pairs || !below.pairs) return null;
  const pair = EFFORT_PAIRS.find((each) => at.pairs[each] && below.pairs[each]);
  if (!pair) return null;
  const mine = at.pairs[pair];
  const theirs = below.pairs[pair];
  const name = effortName(lower);
  const overlap = mine.fixed.min <= theirs.fixed.max && theirs.fixed.min <= mine.fixed.max;
  const words = { level: name, fixed: figure(mine.fixed.median) || "",
                  other: figure(theirs.fixed.median) || "",
                  planted: figure(mine.planted) || "" };
  const result = overlap
    ? t(mine.fixed.median === theirs.fixed.median ? "effort.card.vs.same"
                                                   : "effort.card.vs.within", words)
    : t(mine.fixed.median > theirs.fixed.median ? "effort.card.vs.more"
                                                : "effort.card.vs.fewer", words);
  const time = timesText(mine.seconds.median / theirs.seconds.median);
  const usd = at.api_equivalent_usd && below.api_equivalent_usd
    && below.api_equivalent_usd.median > 0
    ? timesText(at.api_equivalent_usd.median / below.api_equivalent_usd.median) : "";
  const cost = !usd ? t("effort.card.vs.cost.time", { n: time })
    : usd === time ? t("effort.card.vs.cost.both", { n: time })
    : t("effort.card.vs.cost.split", { time, usage: usd });
  return t("effort.card.vs.value", { result, cost });
}

/**
 * Does any block on this card carry `max` beside a cheaper `xhigh` (661)?
 * Then the cost warning says what was measured rather than that nothing was.
 * @param {any[]} blocks
 * @returns {boolean}
 */
function maxMeasuredDearer(blocks) {
  return blocks.some((block) => {
    const at = block && block.levels ? block.levels.max : null;
    const below = block && block.levels ? block.levels.xhigh : null;
    if (!at || !below) return false;
    return EFFORT_PAIRS.some((pair) => at.pairs[pair] && below.pairs[pair]
      && at.pairs[pair].seconds.median > below.pairs[pair].seconds.median);
  });
}

/**
 * The pairs a block measured, as the caveat names them.
 * @param {any} block
 * @returns {string}
 */
function effortPairsText(block) {
  const seen = EFFORT_PAIRS.filter((pair) => Object.values((block && block.levels) || {})
    .some((/** @type {any} */ level) => level && level.pairs && level.pairs[pair]));
  return seen.map((pair) => t("effort.pair." + pair)).join(t("effort.card.and"));
}

/**
 * One pinned block's section of the card (661): whose figures these are, the
 * figures at this level or the unmeasured sentence, `max` against `xhigh` in
 * plain words, the CLI note, and when and how it was measured.
 * The block for the model the route's alias answers as now (`aliasNow`) is
 * headed as that, and the card puts it above the route's own figures.
 * @param {any} route
 * @param {any} primary the route's own block, for the model its alias answered as
 * @param {any} block
 * @param {string} level
 * @returns {HTMLElement}
 */
function pinnedSection(route, primary, block, level) {
  const section = document.createElement("div");
  section.className = "effort-pinned-block";
  const head = document.createElement("p");
  head.className = "effort-model";
  const now = aliasNow(route);
  // 704, 708: "current" is this pinned block's own `resolved_model` matching
  // what the route runs today (`currentRouteModel`), not only whether
  // `alias_now` happens to be set. A route whose alias and `resolved_model`
  // already agree (no `alias_now`, e.g. opus since 708) has no checked date
  // to show, so it reads as plainly asked for by full id rather than as
  // "checked on" a date that was never recorded.
  const current = currentRouteModel(route);
  const isCurrent = Boolean(current) && current === block.requested_model;
  setText(head, isCurrent && now
    ? t("effort.card.model.current", { model: String(block.requested_model),
                                       alias: String(route.model || ""),
                                       date: String(now.checked_on) })
    : isCurrent
    ? t("effort.card.model.pinned.bare", { model: String(block.requested_model),
                                           alias: String(route.model || "") })
    : primary && primary.resolved_model
    ? t("effort.card.model.pinned", { model: String(block.requested_model),
                                      alias: String(route.model || ""),
                                      resolved: String(primary.resolved_model) })
    : t("effort.card.model.pinned.bare", { model: String(block.requested_model),
                                           alias: String(route.model || "") }));
  section.appendChild(head);
  const rows = effortCardRows(block, level);
  if (rows && level === "max") {
    const said = effortComparison(block, "max", "xhigh");
    if (said) rows.push([t("effort.card.vs", { level: effortName("xhigh") }), said]);
  }
  if (rows) {
    const list = document.createElement("dl");
    list.className = "effort-figures";
    fill(list, rows.flatMap(([label, said]) => {
      const term = document.createElement("dt");
      setText(term, label);
      const value = document.createElement("dd");
      setText(value, said);
      return [term, value];
    }));
    section.appendChild(list);
  } else {
    const none = document.createElement("p");
    none.className = "hint";
    setText(none, t("effort.card.unmeasured"));
    section.appendChild(none);
  }
  const old = cliTooOld(route, String(block.requested_model));
  if (old) {
    const note = document.createElement("p");
    note.className = "hint warn";
    setText(note, t("effort.card.cli_old", old));
    section.appendChild(note);
  }
  const caveat = document.createElement("p");
  caveat.className = "hint effort-caveat";
  setText(caveat, t(block.safe_mode ? "effort.card.caveat.pinned.isolated"
                                    : "effort.card.caveat.pinned",
                    { date: String(block.measured_on || ""), pairs: effortPairsText(block) }));
  section.appendChild(caveat);
  return section;
}

/**
 * A level's name for a person, in the page's language. The identifier itself
 * where the catalogue has no word for it, rather than a blank.
 * @param {string} level
 * @returns {string}
 */
function effortName(level) {
  const key = "effort.level." + level;
  const word = t(key);
  return word === key ? level : word;
}

/**
 * The card's rows for one level: label and sentence pairs, or null when the
 * block holds no figures at that level. Only ever the catalogue's own numbers,
 * through `figure` and `duration`, so the card cannot show a figure the block
 * does not carry.
 * @param {any} block a route's `measured_by_effort`, or null
 * @param {string} level
 * @returns {Array<[string, string]>|null}
 */
function effortCardRows(block, level) {
  const at = block && block.levels ? block.levels[level] : null;
  if (!at || !at.pairs) return null;
  /** @type {Array<[string, string]>} */
  const rows = [];
  const shown = EFFORT_PAIRS.filter((pair) => at.pairs[pair]);
  for (const pair of shown) {
    const cell = at.pairs[pair];
    let said = t("effort.card.fixed", {
      fixed: figure(cell.fixed.median) || "", planted: figure(cell.planted) || "",
      min: figure(cell.fixed.min) || "", max: figure(cell.fixed.max) || "",
      runs: figure(cell.draws) || "",
    });
    if (typeof cell.licence_fixed === "number") {
      said += " " + t("effort.card.licence", {
        n: figure(cell.licence_fixed) || "", runs: figure(cell.draws) || "" });
    }
    rows.push([t("effort.pair." + pair), said]);
  }
  if (shown.length) {
    rows.push([t("effort.card.time"), shown.map((pair) => t("effort.card.time.pair", {
      time: duration(at.pairs[pair].seconds.median),
      pair: t("effort.pair.short." + pair),
    })).join(", ")]);
  }
  rows.push([t("effort.card.searched"), t("effort.card.searched.value", {
    n: figure(at.searched) || "", runs: figure(at.runs) || "" })]);
  return rows;
}

/**
 * The level a submitted run carries, or undefined (613).
 *
 * Only beside a route whose served row says it takes one, and only a level
 * that row lists: a slider left on a level the newly picked route does not
 * offer is not a choice the server could honour, and it refuses one by name.
 * @returns {string|undefined}
 */
function chosenEffort() {
  const route = chosenRouteRow();
  const choice = route && route.effort;
  if (!choice || !(choice.levels || []).length) return undefined;
  return choice.levels.indexOf(store.effort) >= 0 ? store.effort : undefined;
}

/**
 * The slider: shown with a subscription route that takes a level, set to that
 * route's default the first time it is picked, and hidden otherwise.
 */
function renderEffort() {
  const route = chosenRouteRow();
  const choice = route && route.effort;
  const levels = (choice && choice.levels) || [];
  const block = el("effort-block");
  // The one-level line takes the slider's place for a model this build knows
  // has no graded scale (688, ruling 11) -- shown instead of the control
  // rather than beside it, the same way `effort-block` itself replaces
  // nothing for a route with no effort concept at all.
  const singleLevel = el("effort-single-level");
  const isSingleLevel = !!(choice && choice.single_level);
  singleLevel.hidden = !isSingleLevel;
  setText(singleLevel, isSingleLevel ? t("effort.single_level") : "");
  block.hidden = !levels.length;
  if (!levels.length) {
    // Lives beside the submit button, outside `effort-block`, so hiding that
    // block does not hide it too (615): a route with no effort level at all
    // must not leave a stale `max` warning from whatever was picked before it.
    const submitWarning = el("effort-submit-max-warning");
    submitWarning.hidden = true;
    setText(submitWarning, "");
    renderEffortBaseline(null);
    return;
  }
  renderEffortBaseline(route);
  if (store.effortRoute !== route.id || levels.indexOf(store.effort) < 0) {
    store.effortRoute = route.id;
    store.effort = levels.indexOf(choice.default) >= 0 ? choice.default : levels[0];
  }
  const slider = input("effort-slider");
  slider.min = "0";
  slider.max = String(levels.length - 1);
  slider.value = String(levels.indexOf(store.effort));
  slider.oninput = () => {
    const picked = levels[Number(slider.value)];
    if (!picked) return;
    store.effort = picked;
    // In the same handler, so the card and the slider never show two levels.
    renderEffortCard();
  };
  renderEffortCard();
}

/**
 * The lowest merge effort measurably as good as the best, from a route's
 * catalogue figures (673), or null. Nothing is typed in: the level is found
 * in the block each time the route is picked.
 *
 * The rule is the operator's. Over the pairs measured at every level, sum
 * each level's median planted errors fixed; the best level is the highest
 * sum, and its range is the sum of the pairs' minimums to the sum of their
 * maximums. The answer is the lowest level whose sum lies in that range.
 *
 * **Only a measurement of what the route runs now.** The block's resolved
 * model must be the one the route answers as today (`alias_now` when the
 * alias has moved on, else the route's own), and it must have run in safe
 * mode, which is how every command route runs since 610: a block from
 * before is a measurement of another configuration, which is also why
 * Sonnet's, stale on the current CLI, is not used. It must cover the
 * slider's lowest level and at least one above the answer, or "as good as
 * any higher level" says nothing. The route's own block is tried first,
 * then its pinned blocks (661).
 * @param {any} route
 * @returns {{level: string, block: any, pairs: string[]}|null}
 */
function effortBaseline(route) {
  const levels = (route && route.effort && route.effort.levels) || [];
  const entry = routeEntry(route);
  if (!entry || levels.length < 2) return null;
  const current = currentRouteModel(route);
  const blocks = [entry.measured_by_effort].concat(routePinnedFigures(route));
  for (const block of blocks) {
    const found = baselineIn(block, levels, current);
    if (found) return found;
  }
  return null;
}

/**
 * `effortBaseline`'s rule over one block, or null.
 * @param {any} block
 * @param {string[]} levels the slider's levels, lowest first
 * @param {string} current the model the route answers as now
 * @returns {{level: string, block: any, pairs: string[]}|null}
 */
function baselineIn(block, levels, current) {
  if (!block || !block.levels || block.safe_mode !== true || !current
      || String(block.resolved_model || "") !== current) return null;
  const measured = levels.filter((level) => block.levels[level] && block.levels[level].pairs);
  if (measured.length < 2 || measured[0] !== levels[0]) return null;
  const pairs = Object.keys(block.levels[measured[0]].pairs)
    .filter((pair) => measured.every((level) => block.levels[level].pairs[pair]));
  if (!pairs.length) return null;
  const sum = (/** @type {string} */ level, /** @type {string} */ field) => pairs.reduce(
    (total, pair) => total + Number(block.levels[level].pairs[pair].fixed[field]), 0);
  let best = measured[0];
  for (const level of measured) {
    if (sum(level, "median") > sum(best, "median")) best = level;
  }
  const floor = sum(best, "min");
  const ceiling = sum(best, "max");
  const lowest = measured.find((level) => {
    const middle = sum(level, "median");
    return middle >= floor && middle <= ceiling;
  });
  if (!lowest || lowest === measured[measured.length - 1]) return null;
  return { level: lowest, block: block, pairs: pairs };
}

/**
 * The baseline line under the effort slider, or nothing at all.
 * @param {any} route
 */
function renderEffortBaseline(route) {
  const found = route ? effortBaseline(route) : null;
  const line = el("effort-baseline");
  line.hidden = !found;
  if (!found) {
    setText(el("effort-baseline-text"), "");
    setText(el("effort-baseline-detail"), "");
    return;
  }
  setText(el("effort-baseline-text"), t("effort.baseline", { level: effortName(found.level) }));
  const names = found.pairs.map((pair) => {
    const key = "effort.pair.short." + pair;
    const word = t(key);
    return word === key ? pair : word;
  });
  const pairs = names.length > 1
    ? names.slice(0, -1).join(", ") + " " + t("word.and") + " " + names[names.length - 1]
    : names.join("");
  setText(el("effort-baseline-detail"), t("effort.baseline.detail", {
    date: String(found.block.measured_on || ""),
    model: String(found.block.resolved_model || ""),
    fidelity: String(found.block.fidelity || ""),
    draws: figure(found.block.draws) || String(found.block.draws || ""),
    pairs: pairs,
  }));
}

/**
 * The card beside the slider, for the level it is set to: the figures the
 * grid measured there, or a sentence saying nothing was measured there.
 */
function renderEffortCard() {
  const route = chosenRouteRow();
  const choice = route && route.effort;
  const levels = (choice && choice.levels) || [];
  if (!levels.length || el("effort-block").hidden) return;
  const level = store.effort;
  const name = effortName(level);
  const slider = input("effort-slider");
  slider.setAttribute("aria-valuetext", name);
  fill(el("effort-ticks"), levels.map((/** @type {string} */ each, /** @type {number} */ position) => {
    const span = document.createElement("span");
    setText(span, effortName(each));
    // Under its thumb position, as the fidelity words are (686).
    span.style.setProperty("--at", String(levels.length > 1 ? position / (levels.length - 1) : 0));
    if (each === level) span.classList.add("on");
    return span;
  }));
  setText(el("effort-card-title"), t("effort.card.title", { level: name }));

  const block = routeEffortFigures(route);
  const pinned = routePinnedFigures(route);
  // Whose figures the route's own block holds, said only when a pinned block
  // sits beside it (661): alone, the card is about the route and needs no
  // heading; beside another model's figures, it must say which model is which.
  // Where the alias answers as another model now, the route's own figures are
  // history and say so, and that model's block goes above them.
  const now = aliasNow(route);
  const model = el("effort-model");
  model.hidden = !(pinned.length && block && block.resolved_model);
  const history = block && block.safe_mode === false
    ? "effort.card.model.history.before_safe_mode" : "effort.card.model.history";
  setText(model, model.hidden ? "" : t(now ? history : "effort.card.model.route", {
    model: String(block.resolved_model), alias: String(route.model || "") }));
  // 704, 708: a pinned block is "current" when its own `resolved_model`
  // matches what the route runs today (`currentRouteModel`), whether that
  // answer came from `alias_now` or, once the two agree, from the route's
  // own `resolved_model` directly, not only when `alias_now` is set.
  const currentModel = currentRouteModel(route);
  const current = pinned.filter((each) => currentModel && each.requested_model === currentModel);
  const others = pinned.filter((each) => current.indexOf(each) < 0);
  fill(el("effort-current"), current.map((each) => pinnedSection(route, block, each, level)));
  el("effort-current").hidden = !current.length;
  fill(el("effort-pinned"), others.map((each) => pinnedSection(route, block, each, level)));
  el("effort-pinned").hidden = !others.length;
  const rows = effortCardRows(block, level);
  fill(el("effort-figures"), (rows || []).flatMap(([label, said]) => {
    const term = document.createElement("dt");
    setText(term, label);
    const value = document.createElement("dd");
    setText(value, said);
    return [term, value];
  }));
  el("effort-figures").hidden = !rows;
  const unmeasured = el("effort-unmeasured");
  unmeasured.hidden = Boolean(rows);
  setText(unmeasured, rows ? "" : t("effort.card.unmeasured"));

  // `max` (615): a fifth stop the grid never ran, so `rows` above is already
  // null for it and the unmeasured sentence already shows. This is the
  // further cost warning the operator asked for, in the card and, so it
  // cannot be missed by picking the last stop and never reading the card,
  // repeated by the submit button below.
  //
  // Where a block on the card measured `max` and it cost more than `xhigh`
  // (661), the warning says so instead of calling the level untested; the
  // cost warning itself stays either way.
  const atMax = level === "max";
  const warningText = maxMeasuredDearer([block, ...pinned])
    ? t("effort.max_warning.measured") : t("effort.max_warning");
  const maxWarning = el("effort-max-warning");
  maxWarning.hidden = !atMax;
  setText(maxWarning, atMax ? warningText : "");
  const submitWarning = el("effort-submit-max-warning");
  submitWarning.hidden = !atMax;
  setText(submitWarning, atMax ? warningText : "");

  // The ruling in 612 is about the default; the choice is the requester's, so
  // a level it keeps out of `sourced` is said out loud there rather than
  // refused. Both halves are served: the levels on the route, the flag on the
  // fidelity level.
  const fidelity = ((store.config.fidelity && store.config.fidelity.levels) || [])
    .find((/** @type {any} */ each) => each.value === store.fidelity);
  const warning = el("effort-warning");
  warning.hidden = !(fidelity && fidelity.retrieves
    && (choice.not_at_sourced || []).indexOf(level) >= 0);
  setText(warning, warning.hidden ? ""
    : t("effort.card.low_sourced", { fidelity: String(fidelity.name || fidelity.value) }));

  const caveat = el("effort-caveat");
  caveat.hidden = !block;
  setText(caveat, block ? t(block.safe_mode ? "effort.card.caveat.isolated"
                                           : "effort.card.caveat", {
    date: String(block.measured_on || ""), runs: figure(block.draws) || "",
  }) : "");
}

/**
 * What the endpoint is asked for. The wire name, with the id as a last resort.
 *
 * The fallback exists for a catalogue written against an older schema, where
 * `api_model` was the id and the two could not differ. `catalogue.validate`
 * requires the field now, so a server on this build never sends one without
 * it; the page is still the thing a stale file reaches first.
 * @param {any} model
 * @returns {string}
 */
function wireName(model) {
  return String((model && (model.api_model || model.id)) || "");
}

/**
 * The command routes `/config` reports, or `[]`.
 *
 * Empty is the ordinary answer and the default: a server that was never given
 * a routes file offers no command backend at all, and the page then looks
 * exactly as it did before this existed.
 * @returns {any[]}
 */
function commandRoutes() {
  const block = store.config && store.config.commands;
  return (block && block.routes) || [];
}

/**
 * Is a command route a thing everyone on this server shares? The server says.
 *
 * Read from `/config` rather than assumed, for `verify_depths`' reason: the
 * page holds no vocabulary of its own, and the day a per-account route exists
 * this sentence stops appearing with no edit here.
 * @returns {boolean}
 */
function commandsArePerUser() {
  const block = store.config && store.config.commands;
  return Boolean(block && block.per_user);
}

/**
 * The command route a row carries, or null for every other row.
 * @param {any} model
 * @returns {any}
 */
function routeOf(model) {
  return (model && model.command) || null;
}

/**
 * What the markers on a subscription row mean, said once under the table.
 *
 * **The information, moved rather than cut.** These two sentences used to sit
 * in the Model cell of every command row, and `model-meta` does not wrap, so
 * four subscription rows widened that column from 410px to 670px and pushed
 * the table 311px past its box. The operator asked for the scroll to go; the
 * caveats may not, because a subscription row really is not comparable to the
 * measured figures beside it and really is shared by everyone on the server.
 * So the row carries a two-word marker and the sentence lives here, once, for
 * every row that carries it.
 *
 * **Only the halves that are on a row.** A sentence explaining a marker
 * nothing is marked with is a caveat about a deployment this is not, and it
 * teaches a reader to skip the hints -- the same rule `commands-hint` above
 * already follows by hiding itself where there is no command route.
 */
function renderRouteCaveats() {
  const target = el("route-caveats");
  if (!target) return;
  const routes = commandRoutes();
  const said = [];
  if (routes.some((/** @type {any} */ route) => !route.comparable)) {
    said.push(t("models.route.caveat.incomparable"));
  }
  if (routes.length && !commandsArePerUser()) {
    said.push(t("models.route.caveat.shared"));
  }
  // And what the Cost column says for these rows, which is a word rather than
  // a figure. `pricing.py`'s rule is that an unmeasured cost is never `$0.00`
  // and never blank, because a zero reads as "measured, and free"; `on plan`
  // is the honest cell and this is the sentence behind it.
  if (routes.some((/** @type {any} */ route) => route.cost === "plan")) {
    said.push(t("models.route.caveat.cost"));
  }
  // What the retrieval marker means, and the half of it a marker cannot say:
  // *when* the grant applies. It is the `sourced` level that turns it on, and
  // a reader who saw the marker and not that sentence would think every run
  // through this row reaches the network (548).
  if (routes.some((/** @type {any} */ route) => (route.retrieval || []).length)) {
    said.push(t("models.route.caveat.retrieval"));
  }
  // A free-tier row (632). Not gated on `commandRoutes()`, the way the four
  // above are: the marker itself is not a command-route marker (see
  // `freeTierNote`), so its caveat is asked of the same rows the marker
  // could appear on -- everything the scorecard shows.
  if (scorecardRows().some(
      (/** @type {any} */ model) => Boolean(freeTierNote(model)))) {
    said.push(t("models.route.caveat.freetier"));
  }
  target.hidden = said.length === 0;
  setText(target, said.join(" "));
}

/**
 * Which of the four route kinds this row is.
 *
 * A command route's own kind comes from its profile: `subscription` is the
 * profile that exists for a flat-rate plan, and any other profile an operator
 * names is a program this tool has no claim to make about. Everything else is
 * the split `costCell` already draws -- a self-hosted endpoint bills GPU
 * minutes and every other provider bills tokens.
 * @param {any} model
 * @returns {string}
 */
function routeKind(model) {
  const route = routeOf(model);
  if (route) {
    return route.profile === ROUTE_SUBSCRIPTION ? ROUTE_SUBSCRIPTION : ROUTE_COMMAND;
  }
  // **No row is no answer.** `routeKind(undefined)` used to read `metered`,
  // which is a claim about where the money goes made out of an absence. Every
  // other branch below is a fact about the row: a self-hosted provider bills
  // GPU minutes, any other named provider bills tokens, and a row with no
  // provider at all is one this page cannot classify and says so.
  if (!model) return ROUTE_UNKNOWN;
  if (model.provider === SELF_HOSTED) return ROUTE_SELFHOSTED;
  return model.provider ? ROUTE_METERED : ROUTE_UNKNOWN;
}

/** The endpoint rows `/config` reports, or `[]`. @returns {any[]} */
function providerRows() {
  const endpoints = store.config && store.config.endpoints;
  return (endpoints && endpoints.providers) || [];
}

/**
 * The address a model this catalogue does not know about would be sent to.
 * @returns {string}
 */
function defaultEndpoint() {
  const endpoints = store.config && store.config.endpoints;
  return String((endpoints && endpoints.default) || "");
}

/**
 * Can this server reach this model at all?
 *
 * A model is sent to the endpoint stored for its provider and to nowhere
 * else, so a provider with no endpoint is a model with nowhere to go. It is
 * answered here, before the operator commits a document, because the
 * alternative is what the picker used to do: offer it, accept it, and fail
 * two steps into the run with a message about a model nobody typed.
 *
 * A row with no provider at all is reachable: it is not from the catalogue
 * and it goes to the server's own endpoint, which always exists.
 * @param {any} model
 * @returns {boolean}
 */
function reachable(model) {
  const provider = model && model.provider;
  if (!provider) return true;
  const row = providerRows().find((/** @type {any} */ entry) => entry.name === provider);
  return Boolean(row && row.configured);
}

/**
 * Why "Use a different model for the checks" is disabled, or "" when it is not.
 *
 * **One condition, and it is the whole of it** (596): a command route is
 * picked for the merge. A route runs one program for every role -- the
 * engine holds one `command` for the run (483) -- so there is no second model
 * for the checks to go to, and `renderModels` forces the split off under it.
 * Nothing else disables the box: a typed id, a run in flight and a server
 * with one reachable row all leave it enabled. The sentence names the picked
 * row and says what enables the box: picking a row that is reached over an
 * endpoint.
 * @param {any[]} models the rows `pickable` offers
 * @returns {string}
 */
function splitBlocked(models) {
  const route = chosenRoute();
  if (!route) return "";
  const row = models.find(
    (/** @type {any} */ model) => model.id === COMMAND_PREFIX + route);
  return t("models.split.blocked.route",
           { name: row ? String(row.display_name || row.id) : route });
}

/**
 * The one radio in the first column. It sets both roles at once.
 *
 * One control, because one model doing both is what almost every run wants
 * and two radios per row asked the operator to make the same choice twice --
 * "the user would expect not to click two option bullets to switch the
 * model". Splitting the roles is still available and is still reported in
 * `provenance.models`; it is behind the checkbox under the table, which is
 * where a second decision belongs.
 *
 * Setting both here rather than leaving the check role to follow at submit
 * time is deliberate: what the page shows is then what the request carries,
 * and a hidden "same as merge" rule would be a second place the two could
 * disagree.
 * @param {any} model
 * @param {boolean} open is this model reachable
 * @returns {HTMLTableCellElement}
 */
function useCell(model, open) {
  const cell = document.createElement("td");
  cell.className = "pick";
  const radio = document.createElement("input");
  radio.type = "radio";
  radio.name = "model-use";
  radio.value = model.id;
  radio.checked = store.mergeModel === model.id;
  radio.disabled = !open || Boolean(typedId());
  radio.setAttribute("aria-label",
    t("models.pick.use", { name: model.display_name || model.id }));
  radio.addEventListener("change", () => {
    const wasRoute = Boolean(chosenRoute());
    store.mergeModel = model.id;
    if (!store.splitRoles) store.checkModel = model.id;
    // **Crossing between a command route and anything else re-renders the
    // table** (566). `renderModels` is what sets the split control from
    // `chosenRoute()`, and this handler used to call only
    // `refreshIdleStatus`: in a browser the button moved to `metered API`
    // while `Use a different model for the checks` stayed disabled from the
    // preselected subscription row, and in the other direction a ticked split
    // and its Check column stayed on screen under a command route that
    // ignores both.
    //
    // Only on a crossing, and focus put back on the radio just chosen. Arrow
    // keys move the selection one row at a time and fire `change` on each, so
    // a rebuild on every change would drop keyboard focus to the page body on
    // every step; a crossing is the one step whose state the rebuild owns.
    if (Boolean(chosenRoute()) !== wasRoute) {
      renderModels();
      const chosen = [...document.querySelectorAll('input[name="model-use"]')]
        .find((input) => /** @type {HTMLInputElement} */ (input).value === model.id);
      if (chosen instanceof HTMLInputElement) chosen.focus();
    }
    // A row picked here may be one the catalogue states no window for (605):
    // `renderModels` is not always called above, so this is the one place a
    // plain pick -- no route crossed -- would otherwise leave the field
    // showing the previous row's answer.
    renderCustomWindow();
    // And the effort slider, for the same reason: one subscription route to
    // another crosses nothing, and each has its own default and figures.
    renderEffort();
    refreshIdleStatus();
  });
  cell.appendChild(radio);
  return cell;
}

/**
 * The second column's radio, present only while the roles are split.
 *
 * The cell itself is always built so that every row has the same number of
 * cells as the header does; what is hidden is the cell, not the column, and
 * the header cell is hidden in the same breath by `renderModels`.
 * @param {any} model
 * @param {boolean} open
 * @returns {HTMLTableCellElement}
 */
function checkCell(model, open) {
  const cell = document.createElement("td");
  cell.className = "pick";
  cell.hidden = !store.splitRoles;
  if (!store.splitRoles) return cell;
  const radio = document.createElement("input");
  radio.type = "radio";
  radio.name = "model-check";
  radio.value = model.id;
  radio.checked = store.checkModel === model.id;
  // **A row the merge's route cannot reach is not offered for the checks**
  // (570). It used to be: a subscription row's radio was live under a metered
  // merge, and picking it sent that route's model name, as a model, over the
  // metered route -- while the button went on naming the metered API alone.
  const answers = answersChecks(model);
  radio.disabled = !open || Boolean(typedId()) || !answers;
  radio.setAttribute("aria-label",
    t("models.pick.check", { name: model.display_name || model.id }));
  // The reason is the sentence under the split control, not a tooltip: a
  // disabled radio is the control a reader asks "why not?" of, and the answer
  // has to be somewhere a keyboard and a screen reader reach as well.
  if (!answers) radio.setAttribute("aria-describedby", "split-routes");
  radio.addEventListener("change", () => {
    store.checkModel = model.id;
    // Same reason as the merge radio above (605): the check role can name a
    // row the catalogue states no window for just as the merge role can.
    renderCustomWindow();
    refreshIdleStatus();
  });
  cell.appendChild(radio);
  return cell;
}

/**
 * Can this row answer the checks, given the row picked for the merge? (570)
 *
 * **A run answers through one command or over HTTP, never both.** The engine
 * holds one `command` for the whole run -- per-role endpoints are dead
 * configuration beside it (483) -- so there is no run in which the merge goes
 * to a metered API and the checks go to a subscription. The page used to offer
 * that pairing anyway, and the request it built carried the subscription
 * route's model name as an ordinary model: on the discovered `claude` routes
 * that is `haiku`, which went to the server's own endpoint and failed; on an
 * operator's route whose model is `claude-opus-5` it would have gone to the
 * metered API and been billed, while the page said the checks were on the plan.
 *
 * The server cannot refuse that request, which is why the rule is here. It is
 * byte for byte the request a reader makes by picking the metered row for the
 * checks -- 519's second shape, a well-formed metered request that says
 * nothing about what the page was showing.
 *
 * Under a command merge the split is forced off (`renderModels`), so the only
 * row that could answer is that route's own, and it is said that way rather
 * than as "never" so the rule stays true if the split is ever allowed there.
 * @param {any} model
 * @returns {boolean}
 */
function answersChecks(model) {
  const route = routeOf(model);
  const merging = chosenRoute();
  if (merging) return Boolean(route) && COMMAND_PREFIX + merging === model.id;
  return !route;
}

/**
 * The typed model id, or "" when none is in charge.
 *
 * **The one reader**, so the checkbox is the switch everywhere at once: the
 * request, the button, the summary and the disabled radios all ask this. An
 * id counts only while "Use a model id not in the table" is ticked; unticking
 * also clears the field, so nothing typed can ride along unseen (591).
 * @returns {string}
 */
function typedId() {
  return store.customOn ? store.customModel.trim() : "";
}

/**
 * The table row a typed id names byte for byte, or null.
 *
 * **The server routes such an id by the row, not by the select.**
 * `jobs.endpoint_plan` looks a model up in the catalogue first and in what the
 * configured endpoints listed second, and only a name neither knows goes where
 * the request says. So a typed `gpt-5.6-terra` goes to the OpenAI endpoint
 * whatever "Send it to" reads, and the page has to say that rather than name
 * an address the run will not use. A command row is never matched: its model
 * is an alias the server routes nowhere, which is the typed case.
 * @returns {any}
 */
function typedRow() {
  const typed = typedId();
  if (!typed) return null;
  return pickable().find((/** @type {any} */ model) =>
    !routeOf(model) && model.provider && wireName(model) === typed) || null;
}

/**
 * The checkbox, the field, the select beside it, and the sentence saying
 * which one is in charge and where the id goes.
 *
 * The select lists this server's own endpoint and the providers configured on
 * the Credentials sheet, and nothing else, because a request can only name an
 * endpoint the operator stored. It is shown with the field, never apart from
 * it: "where does this go" is the question a typed id raises.
 */
function renderCustomModel() {
  input("custom-toggle").checked = store.customOn;
  el("custom-block").hidden = !store.customOn;
  const typed = typedId();
  const menu = /** @type {HTMLSelectElement} */ (el("custom-endpoint"));
  const options = [option("", t("models.custom.default", { url: defaultEndpoint() }))];
  for (const provider of providerRows()) {
    if (!provider.configured) continue;
    options.push(option(provider.name, provider.name + " \u2014 " + provider.base_url));
  }
  fill(menu, options);
  menu.value = store.customEndpoint;
  if (menu.value !== store.customEndpoint) {
    // The endpoint that was chosen has since been deleted. Falling back in
    // the store as well as in the control, so the request cannot carry a name
    // the page is no longer showing.
    store.customEndpoint = "";
    menu.value = "";
  }
  const row = typedRow();
  // Disabled, not hidden, for an id the table already routes: the control
  // stays where the reader looks for it, and the sentence says why it is out.
  menu.disabled = Boolean(row);
  let note = "";
  if (store.customOn && !typed) note = t("models.custom.empty");
  else if (row) note = t("models.custom.known", { model: typed, provider: String(row.provider) });
  else if (typed) note = t("models.custom.active", { model: typed, url: endpointLabel() });
  setText(el("custom-model-note"), note);
  // A typed id naming a retired row (621). `typedRow` finds it, because a
  // retired row is still in `pickable()` with its radios disabled, and the
  // server routes the id by that row -- so a typed `claude-opus-5` reaches
  // the vendor that refuses it. Warned, never blocked: the operator may know
  // something this build does not, and a refusal costs one call to find out.
  const retired = row && isRetired(row) ? retiredWarning(typed, row.retired) : "";
  for (const hook of ["custom-model-retired", "submit-retired-warning"]) {
    const warning = el(hook);
    warning.hidden = !retired;
    setText(warning, retired);
  }
  renderCustomWindow();
}

/**
 * The warning for a typed id that names a retired row (621), in the page's
 * language, out of the row's own `retired` block.
 * @param {string} typed
 * @param {any} retired
 * @returns {string}
 */
function retiredWarning(typed, retired) {
  return t("models.custom.retired", {
    model: typed,
    why: retiredSentence(retired),
    replacement: String(retired.replacement || ""),
  });
}

/**
 * The row the window question is about with no id typed: whichever picked
 * role -- both are checked, in this order, when the checks are split -- names
 * a row `pickable()` marks `listed`: an id an endpoint offered that no
 * catalogue entry names, so there is no `context_window` to show in the
 * Model column and none for `endpoint_plan` to read either. A route is never
 * this row: `route_plan` refuses `window` beside one, because the route's own
 * file states it.
 *
 * Closes the gap 604 left on the table's own side of it (605): a typed copy
 * of such an id already had somewhere to state the window; a row picked
 * straight from the table did not.
 * @returns {any}
 */
function pickedUnknownModel() {
  const ids = store.splitRoles ? [store.mergeModel, store.checkModel]
                                : [store.mergeModel];
  const models = pickable();
  for (const id of ids) {
    const model = models.find((/** @type {any} */ entry) => entry.id === id);
    if (model && !routeOf(model) && model.provider && model.context_window == null) {
      return model;
    }
  }
  return null;
}

/**
 * Is the context window field in charge of anything right now?
 *
 * Ticked open (604) -- whatever it states, even nothing yet -- or, with the
 * checkbox off, a picked row `pickedUnknownModel` finds (605). The two never
 * overlap: the radios are disabled while an id is typed, so a picked row only
 * counts while there is no typed one to override it.
 * @returns {boolean}
 */
function windowFieldActive() {
  return store.customOn || Boolean(pickedUnknownModel());
}

/**
 * The context window field, and the sentence under it saying whether the
 * model in charge -- typed or picked from the table -- needs it and where the
 * figure is (604, 605).
 *
 * The rule is the server's: `endpoints.providers[].window_required` is
 * `jobs.window_unreportable`, the predicate `endpoint_plan` refuses on, so
 * the page asks for the field exactly where the server would refuse without
 * it. A row the table already states a window for needs none.
 */
function renderCustomWindow() {
  const active = windowFieldActive();
  el("window-block").hidden = !active;
  if (!active) {
    setText(el("custom-window-note"), "");
    return;
  }
  const field = input("custom-window");
  const limits = (store.config && store.config.limits) || {};
  if (typeof limits.min_window === "number") field.min = String(limits.min_window);
  if (typeof limits.max_window === "number") field.max = String(limits.max_window);
  const need = windowNeed();
  field.required = need === "required";
  let note = "";
  if (need === "stated") {
    note = t("models.custom.window.stated", { tokens: figure(windowStatedByRow()) || "" });
  } else if (need === "required") {
    note = t("models.custom.window.required", { url: windowDestination() })
      + " " + t("models.custom.window.where");
  } else {
    note = t("models.custom.window.optional") + " " + t("models.custom.window.where");
  }
  setText(el("custom-window-note"), note);
}

/**
 * The window the table states for the row a typed id names, or null.
 *
 * Only ever answers for the typed-id case: a row `pickedUnknownModel` finds is
 * by definition one with no `context_window`, so this is null for every row
 * that reaches this page through it.
 * @returns {number|null}
 */
function windowStatedByRow() {
  const row = typedRow();
  const tokens = row && row.context_window;
  return typeof tokens === "number" && tokens > 0 ? tokens : null;
}

/**
 * Where the model in charge of the window question goes, in words: the row's
 * endpoint, when a row is in charge (typed and matched, or picked from the
 * table); otherwise the one "Send it to" names, for a free-form typed id.
 * @returns {string}
 */
function windowDestination() {
  const row = store.customOn ? typedRow() : pickedUnknownModel();
  if (!row) return endpointLabel();
  const entry = providerRows().find(
    (/** @type {any} */ provider) => provider.name === row.provider);
  return entry ? String(entry.base_url || entry.name) : String(row.provider);
}

/**
 * Does the model in charge of the window question need it stated?
 *
 * "stated" when the table's row already states one (a typed id only: a row
 * `pickedUnknownModel` finds never has one), "required" when the endpoint
 * cannot report one (the server's `window_required`), "optional" otherwise --
 * this server's own endpoint and a self-hosted one may be an ollama, which
 * reports its window. "none" while the field carries no question at all --
 * `renderCustomWindow` hides it there, and `windowFieldActive` is the same
 * predicate asked as a yes-or-no.
 * @returns {"stated"|"required"|"optional"|"none"}
 */
function windowNeed() {
  if (store.customOn) {
    if (windowStatedByRow() !== null) return "stated";
    const row = typedRow();
    const name = row ? String(row.provider || "") : store.customEndpoint;
    if (!name) return "optional";
    const entry = providerRows().find(
      (/** @type {any} */ provider) => provider.name === name);
    return entry && entry.window_required ? "required" : "optional";
  }
  const row = pickedUnknownModel();
  if (!row) return "none";
  const entry = providerRows().find(
    (/** @type {any} */ provider) => provider.name === row.provider);
  return entry && entry.window_required ? "required" : "optional";
}

/**
 * The stated window the request carries: a whole number of tokens, or
 * undefined when none is typed and nothing needs one (`windowFieldActive`).
 * NaN for a figure that is typed and is not one, which `windowRefusal` names
 * before submit.
 * @returns {number|undefined}
 */
function typedWindow() {
  if (!windowFieldActive()) return undefined;
  const text = store.customWindow.trim();
  if (!text) return undefined;
  return /^[0-9]+$/.test(text) ? Number(text) : NaN;
}

/**
 * The name to put in a sentence about the window: the typed id, or -- with
 * none typed -- the display name of the row `pickedUnknownModel` found.
 * @returns {string}
 */
function windowSubjectLabel() {
  if (typedId()) return typedId();
  const row = pickedUnknownModel();
  return row ? String(row.display_name || row.id || "") : "";
}

/**
 * Why the window in charge stops the run, or "" when it does not.
 *
 * The page's half of the server's two refusals: a figure outside the bounds
 * it serves (`api._overrides`, `bad_window`), and no figure where the
 * destination cannot report one (`endpoint_plan`) -- for a typed id (604) or
 * a row picked straight from the table (605), whichever is in charge.
 * @returns {string}
 */
function windowRefusal() {
  if (!windowFieldActive()) return "";
  const tokens = typedWindow();
  const limits = (store.config && store.config.limits) || {};
  const low = typeof limits.min_window === "number" ? limits.min_window : 1;
  const high = typeof limits.max_window === "number" ? limits.max_window : Infinity;
  if (tokens !== undefined && !(tokens >= low && tokens <= high)) {
    return t("models.custom.window.bad", {
      min: figure(low) || String(low), max: figure(high) || String(high),
    });
  }
  if (tokens === undefined && windowNeed() === "required") {
    return t("models.custom.window.missing", {
      model: windowSubjectLabel(), url: windowDestination(),
    });
  }
  return "";
}

/**
 * Which address the typed model would be sent to, in words.
 * @returns {string}
 */
function endpointLabel() {
  if (!store.customEndpoint) return defaultEndpoint();
  const row = providerRows().find(
    (/** @type {any} */ entry) => entry.name === store.customEndpoint);
  return row ? String(row.base_url || row.name) : store.customEndpoint;
}

/**
 * One `<option>`.
 * @param {string} value
 * @param {string} label
 * @returns {HTMLOptionElement}
 */
function option(value, label) {
  const node = document.createElement("option");
  node.value = value;
  setText(node, label);
  return node;
}

/**
 * Whether a catalogue row is retired (618): shown with its figures, never offered.
 * @param {any} model
 * @returns {boolean}
 */
function isRetired(model) {
  return Boolean(model && model.retired && model.retired.on);
}

/**
 * The retired row's sentence, from the catalogue's own `retired` block (618).
 * @param {any} retired
 * @returns {string}
 */
function retiredSentence(retired) {
  const values = {
    date: String(retired.on || ""),
    replacement: String(retired.replacement || ""),
    decision: String(retired.decision || ""),
    refused: String(retired.refused || ""),
  };
  return t(retired.refused ? "models.retired.refused" : "models.retired", values);
}

/**
 * "measured <date>" for a row's figures, or "" (618).
 *
 * Read off the measured block's own `measured_on`, which `catalogue.py`
 * requires of every block, so the line says what the figures' `derived_by`
 * checks and nothing the page worked out. An unmeasured row has no line:
 * there is no measurement to date.
 *
 * The commit this run was measured at (`llossless_commit` or the pre-rename
 * `claimcheck_commit`) is read by `catalogue.py` and kept in the row's own
 * data, but not printed here (717): a commit id names nothing to a reader
 * holding only the published copy, which is what a public page's reader
 * always is. A user's own run keeps its "LLossless commit" provenance row --
 * that copy is never published, and the commit it names is the one that ran
 * it.
 *
 * @param {any} measured a row's `measured` block, or null
 * @returns {string}
 */
function measuredWhen(measured) {
  if (!measured || !measured.measured_on) return "";
  return t("models.measured.on", { date: String(measured.measured_on) });
}

/**
 * One measured figure, or the word for not having one.
 *
 * Two ways to have no figure and they are the same answer to the operator: the
 * whole `measured` block absent, meaning nobody has run this model through the
 * tool, and one field null inside it, meaning the run happened and that
 * quantity was not derivable from it. Neither is estimated and neither is
 * interpolated from a neighbouring row.
 * @param {any} measured
 * @param {string} field
 * @param {number} places
 * @param {string} prefix
 * @param {{good: number, poor: number, ideal?: number, poorInclusive?: boolean}} [scale]
 * @returns {HTMLTableCellElement}
 */
function measuredCell(measured, field, places, prefix, scale) {
  const cell = document.createElement("td");
  cell.className = "num";
  const value = measured ? figure(measured[field], places) : null;
  if (value === null) {
    cell.classList.add("unmeasured");
    setText(cell, t("models.unmeasured"));
    return cell;
  }
  cell.classList.add("mono");
  setText(cell, prefix + value);
  rankCell(cell, band(measured[field], scale));
  return cell;
}

/**
 * The cost column, which has three states rather than two.
 *
 * A measured price, a price nobody measured, and a row that has no price to
 * measure: a self-hosted endpoint bills per minute of GPU time, so there is no
 * per-merge dollar figure to attribute without assuming a utilisation rate.
 * The third is kept apart from the second and from `$0.000` on purpose. Zero
 * reads as "measured and free", which inverts the comparison against every row
 * that does carry a real figure, and "unmeasured" would say nobody had looked
 * at a row that was in fact run end to end.
 * @param {any} model
 * @returns {HTMLTableCellElement}
 */
function costCell(model) {
  const cell = document.createElement("td");
  cell.className = "num";
  // A fourth state, and it is the one this milestone is for. A subscription
  // reports no token counts at all, so `pricing.estimate` answers `unmeasured`
  // for every call -- and what the *operator* pays is a monthly plan this tool
  // has no way to divide by a merge. Neither of those is a number and neither
  // of them is zero: `$0.00` reads as "measured, and free", which is the exact
  // inversion `pricing.py` refuses to make against the rows that do carry a
  // real figure.
  //
  // The word comes from `route.cost`, which the server serves, so there is no
  // branch on this page that can produce a price for a route.
  const route = routeOf(model);
  // `route.cost` is always served for a route this server runs; only a
  // catalogue route it does not serve can lack one (631), and that row then
  // reads its measured block like any other.
  if (route && route.cost) {
    cell.classList.add("onplan");
    // **The word, not the sentence.** `td.num` does not wrap, so `counts
    // against your plan` held the Cost column open at 215px against a 95px
    // header and was 37px of the table's overflow on its own. It is still a
    // word and never a zero -- `renderRouteCaveats` writes out below the
    // table what an `on plan` cell means, for the same reason the two row
    // markers do.
    setText(cell, t("models.cost." + String(route.cost) + ".cell"));
    return cell;
  }
  const measured = model.measured;
  const value = measured ? figure(measured.usd_per_merge, 3) : null;
  if (value === null && measured && measured.billed === "free-tier") {
    // Measured, and billed nothing: a vendor's free tier (625). A word, as a
    // subscription row's is, and not "unmeasured" -- the run happened -- nor
    // a zero, which would read as a price.
    cell.classList.add("freetier");
    setText(cell, t("models.cost.freetier.cell"));
    return cell;
  }
  if (value === null) {
    const metered = Boolean(measured) && model.provider === SELF_HOSTED;
    cell.classList.add(metered ? "notpriced" : "unmeasured");
    setText(cell, t(metered ? "models.notpriced" : "models.unmeasured"));
    return cell;
  }
  cell.classList.add("mono");
  setText(cell, "$" + value);
  rankCell(cell, band(measured.usd_per_merge, RANK_SCALES.usd_per_merge));
  return cell;
}

/**
 * Silent loss as it was counted, banded as a rate.
 *
 * The number shown is the catalogue's own count and the line under it is the
 * pair count that produced it, exactly as the deviations column does. The
 * *colour* comes from the quotient, because 19 over nine pairs and 10 over
 * three are not the same finding and a column sorted by the raw totals would
 * put the worse row second.
 * @param {any} measured
 * @returns {HTMLTableCellElement}
 */
function silentLossCell(measured) {
  const cell = document.createElement("td");
  cell.className = "num";
  const value = measured ? figure(measured.silent_loss, 0) : null;
  if (value === null) {
    cell.classList.add("unmeasured");
    setText(cell, t("models.unmeasured"));
    return cell;
  }
  const number = document.createElement("span");
  number.className = "mono";
  setText(number, value);
  cell.appendChild(number);
  const pairs = perPairDenominator(measured);
  const note = document.createElement("span");
  note.className = "model-meta";
  setText(note, pairs ? t("models.perpair", { n: figure(pairs) || "0" }) : "");
  cell.appendChild(note);
  // The published rate, not one formed here. The catalogue carries
  // `silent_loss_per_pair` beside `deviations_per_pair`, and `validate()`
  // refuses either if it disagrees with its own numerator over `pairs` -- so a
  // rate read from the file is a checked number, while one divided here was
  // only ever as right as this line. Dividing in the renderer also put the
  // arithmetic somewhere no Python test could reach it.
  rankCell(cell, band(measured.silent_loss_per_pair,
                      RANK_SCALES.silent_loss_per_pair));
  return cell;
}

/**
 * The `pairs` a row was measured over, or 0 when it does not say.
 *
 * 0 rather than 1: a row with no pair count is a row whose rate cannot be
 * formed, and dividing by an assumed 1 would turn a missing denominator into
 * a confident band.
 * @param {any} measured
 * @returns {number}
 */
function perPairDenominator(measured) {
  const pairs = measured ? measured.pairs : null;
  return typeof pairs === "number" && pairs > 0 ? pairs : 0;
}

/**
 * Deviations per pair, with the pair count that produced it.
 * @param {any} measured
 * @returns {HTMLTableCellElement}
 */
function deviationCell(measured) {
  const cell = document.createElement("td");
  cell.className = "num";
  const value = measured ? figure(measured.deviations_per_pair, 2) : null;
  if (value === null) {
    cell.classList.add("unmeasured");
    setText(cell, t("models.unmeasured"));
    return cell;
  }
  const number = document.createElement("span");
  number.className = "mono";
  setText(number, value);
  const pairs = document.createElement("span");
  pairs.className = "model-meta";
  const count = figure(measured.pairs);
  setText(pairs, count ? t("models.perpair", { n: count }) : "");
  cell.appendChild(number);
  cell.appendChild(pairs);
  rankCell(cell, band(measured.deviations_per_pair,
                      RANK_SCALES.deviations_per_pair));
  return cell;
}

/* ------------------------------------------------------------------ */
/* the status line                                                     */
/* ------------------------------------------------------------------ */

/**
 * The one sentence and the one dot. Everything that changes state says so here.
 * @param {string} tone one of "", "ok", "warn", "bad", "busy"
 * @param {string} word the state, in a word, beside the colour and never instead of it
 * @param {string} text one sentence of plain prose
 */
function say(tone, word, text) {
  setState(el("status"), tone);
  setState(el("status-dot"), tone);
  setText(el("status-word"), word);
  setText(el("status-text"), text);
}

/**
 * Why this run cannot be submitted, or "" when it can.
 *
 * Only one reason so far and it is the one this milestone exists for: a model
 * whose provider has no endpoint configured is a model this server has no way
 * to reach, and the picker offering it anyway is what produced a run that was
 * accepted, queued, started and then failed with a message about a model
 * nobody had typed. The server refuses the same request with the same reason
 * -- this is the half that refuses it before the documents go anywhere.
 *
 * The sentence is the catalogue's, not this file's. It has to be, for the
 * same reason every other sentence on this page is: a refusal written in
 * English inside a script is a refusal that stays in English.
 * @returns {string}
 */
function unreachableChoice() {
  const named = typedRow();
  if (named && !reachable(named)) {
    return t("models.unreachable.blocked", {
      name: typedId(), provider: String(named.provider || ""),
    });
  }
  if (typedId()) return windowRefusal();
  const roles = store.splitRoles ? [store.mergeModel, store.checkModel]
                                 : [store.mergeModel];
  for (const id of roles) {
    const model = pickable().find((/** @type {any} */ entry) => entry.id === id);
    if (model && !reachable(model)) {
      return t("models.unreachable.blocked", {
        name: model.display_name || model.id,
        provider: String(model.provider || ""),
      });
    }
  }
  // A row picked here, not typed, can still be one the catalogue states no
  // window for (605): reachability comes first because a provider with no
  // endpoint at all is the more basic problem.
  const stated = windowRefusal();
  if (stated) return stated;
  // The second guard on 570, behind the disabled radio and the re-join in
  // `renderModels`: if a check role on a row the merge's route cannot reach is
  // ever reached anyway, the button refuses rather than sending that row's
  // model name down the merge's route. Not a fallback to the merge's row
  // either -- that would run the checks somewhere the reader did not pick.
  if (store.splitRoles) {
    const check = pickable().find(
      (/** @type {any} */ entry) => entry.id === store.checkModel);
    if (check && !answersChecks(check)) {
      return t("models.split.blocked", { name: check.display_name || check.id });
    }
  }
  return "";
}

/** What the status line says when no run is in flight. */
function refreshIdleStatus() {
  if (store.runId) {
    // The status line belongs to the finished run and must not be overwritten
    // by an idle sentence. **The button's label does not.** It is a claim
    // about where the *next* click goes, and a settings change that removed
    // the route it names left it naming one the picker no longer offers --
    // found in the browser, after switching two routes off with a result on
    // screen. `setRunning` owns it while a run is in flight; this is the
    // other half, for a page that has one behind it.
    if (!store.running) setText(el("submit-label"), submitLabel());
    renderStepGoto(null);
    renderStepStates();
    renderSaveDefaults();
    syncSaveDefaultsChecked();
    return;
  }
  const state = readiness();
  // Amber for "more input needed", green for "ready" (640): the one line on
  // this page a reader has to act on before anything else can happen.
  say(state.ready ? "ok" : "warn",
      t(state.ready ? "word.ready" : "word.notready"), state.text);
  const button = /** @type {HTMLButtonElement} */ (el("submit"));
  button.disabled = !state.ready;
  setText(el("submit-label"), submitLabel());
  renderStepGoto(state);
  renderStepStates();
  renderSaveDefaults();
  syncSaveDefaultsChecked();
}

/**
 * Can this form be submitted, and what the status line says about it (640).
 *
 * The documents first, because a fresh page has two empty panes and that is
 * the first thing to fix: none with text asks for the minimum, and otherwise
 * each empty one is named, as its tab names it. Then the model choice
 * (`unreachableChoice`). Ready says how many documents will be merged. The
 * button is disabled exactly when this says not ready. `step` names the
 * input step that holds a documents reason (673); the one reason without a
 * step is the model choice (`blockingStep`).
 * @returns {{ready: boolean, text: string, step?: string}}
 */
function readiness() {
  const min = minDocuments();
  const empty = store.docs
    .map((doc, index) => ({ doc, index }))
    .filter((entry) => !entry.doc.text.trim())
    .map((entry) => entry.doc.name || t("documents.untitled", { n: entry.index + 1 }));
  if (store.docs.length < min || empty.length === store.docs.length) {
    return { ready: false, step: "documents", text: t("status.needdocs", { min: min }) };
  }
  if (empty.length === 1) {
    return { ready: false, step: "documents", text: t("status.empty.one", { name: empty[0] }) };
  }
  if (empty.length > 1) {
    return { ready: false, step: "documents", text: t("status.empty.many", {
      names: empty.slice(0, -1).join(", ") + " " + t("word.and") + " "
        + empty[empty.length - 1],
    }) };
  }
  const stranded = unreachableChoice();
  if (stranded) return { ready: false, text: stranded };
  return { ready: true, text: t("status.ready", { n: store.docs.length }) };
}

/**
 * What the button that starts the run says. **It names the route.**
 *
 * The irreversible moment is the click, and until now the control at that
 * moment said `Merge and check` whether the next four minutes were going to
 * bill a metered API, spend a subscription, or run a GPU. Naming the route on
 * the button is the cheapest place to put the disclosure and the only one that
 * is unavoidably in front of the person deciding.
 *
 * It reads `chosenRouteKind`, which reads `store.mergeModel`, which is the
 * same value `submission` sends -- so the label and the request cannot
 * disagree without somebody deleting one of the two calls.
 * @returns {string}
 */
function submitLabel() {
  // **Both roles, whenever they are billed differently** (570). With the
  // split on, the checks are a second destination, and a label naming only
  // the merge's route described half the run at the moment the money is
  // committed: a metered merge with local checks read `metered API` alone.
  const check = checkRouteKind();
  if (check !== chosenRouteKind()) {
    return t("run.submit.split", { merge: routeLabel(chosenRouteKind()),
                                   check: routeLabel(check) });
  }
  return t("run.submit.route", { route: routeLabel(chosenRouteKind()) });
}

/**
 * Which kind of route the checks are about to take, in a word (570).
 *
 * `chosenRouteKind`'s twin, read off `store.checkModel` -- which is what
 * `chosenModel("check")` sends -- and only while the roles are split. Joined,
 * or with a model typed, the checks go wherever the merge goes, and a second
 * reading of the same fact would be a second place for it to be wrong.
 * @returns {string}
 */
function checkRouteKind() {
  if (!store.splitRoles || typedId()) return chosenRouteKind();
  const model = pickable().find(
    (/** @type {any} */ entry) => entry.id === store.checkModel);
  return routeKind(model);
}

/* ------------------------------------------------------------------ */
/* running a merge                                                     */
/* ------------------------------------------------------------------ */

/**
 * Which model string one role's request carries.
 *
 * The typed id wins over the table, entirely and for both roles: a text field
 * that silently lost to a radio somewhere off screen would be a control that
 * does nothing, and the radios are disabled while it has anything in it so
 * that the page says which of the two is in charge.
 *
 * Otherwise it is the picked row's **wire name**, never its catalogue id.
 * The two differ on four of the six shipped rows -- `claude-haiku-4-5` is a
 * display key and `claude-haiku-4-5-20251001` is what the vendor answers to --
 * and sending the id is what produced a run that failed two steps in on a
 * model name the operator had never typed.
 * @param {"merge"|"check"} role
 * @returns {string|undefined}
 */
function chosenModel(role) {
  const typed = typedId();
  if (typed) return typed;
  // A command route carries the model with it, so the request carries none.
  // That is not tidiness: `jobs.route_plan` **refuses** a request that names
  // both, because a route is one whole row in this picker and a request
  // carrying a route and a model is a page and a request that disagree about
  // where the documents are going. Returning `undefined` here is what makes
  // the page's own selection the only thing that decides.
  if (chosenRoute()) return undefined;
  const id = role === "merge" ? store.mergeModel : store.checkModel;
  const model = pickable().find((/** @type {any} */ entry) => entry.id === id);
  return model ? wireName(model) : (id || undefined);
}

/**
 * Which command route is selected, as an id, or "" for none.
 *
 * **The one reader of the selection, and every consumer goes through it.** The
 * submit button's label, the status line and the request body all call this
 * function, so a page showing one route and sending another is not a bug that
 * can be introduced by editing one of the three -- there is one value and
 * three renderings of it. That is the same rule `setRunning` keeps for the
 * running state, applied to the decision that costs money.
 *
 * A typed model id wins over the table exactly as it does for a model, and for
 * the same reason: the radios are disabled while it has anything in it, so the
 * page says which of the two is in charge.
 * @returns {string}
 */
function chosenRoute() {
  if (typedId()) return "";
  const id = store.mergeModel || "";
  return id.startsWith(COMMAND_PREFIX) ? id.slice(COMMAND_PREFIX.length) : "";
}

/**
 * Which kind of route the run is about to take, in a word.
 *
 * Read off the same `store.mergeModel` `chosenRoute` reads, for the same
 * reason. A typed model id goes to the server's own endpoint, to whichever
 * one the select names, or -- when the table already has a row by that name --
 * to that row's (`typedRow`), and all of those are metered or self-hosted --
 * never a command, because a command route cannot be typed.
 * @returns {string}
 */
function chosenRouteKind() {
  if (typedId()) return typedModelKind();
  const model = pickable().find(
    (/** @type {any} */ entry) => entry.id === store.mergeModel);
  // No row means nothing has been picked, or the picked id is no longer in
  // the list. Either way this page does not know where the run would go, and
  // it used to say `metered API` anyway.
  return routeKind(model);
}

/**
 * Where a *typed* model id goes, in one of `ROUTE_KINDS`.
 *
 * **The server classifies the address; this reads the answer.** The old test
 * here was `provider.name === SELF_HOSTED`, which is a question about a
 * provider's *name* rather than about where its endpoint points -- so a
 * provider row called anything else, pointed at a box on this network, read
 * as metered. And with no endpoint named at all, the request falls to the
 * server's own default, which this never looked at.
 *
 * Both are now one field: `endpoints.default_kind` for the unnamed case and
 * the row's own `kind` for the named one, both from `discover.kind_of`. A
 * server too old to send them yields `unknown`, which is the honest label
 * rather than a guess.
 * @returns {string}
 */
function typedModelKind() {
  // An id the table already routes is billed as that row is (`typedRow`).
  const row = typedRow();
  if (row) return routeKind(row);
  const block = (store.config && store.config.endpoints) || {};
  if (!store.customEndpoint) return endpointKind(block.default_kind);
  const provider = providerRows().find(
    (/** @type {any} */ entry) => entry.name === store.customEndpoint);
  return endpointKind(provider && provider.kind);
}

/**
 * One of the server's endpoint classifications, checked against the kinds this
 * page can label.
 *
 * A word the server sends that this build has no label for reads `unknown`
 * rather than reaching `routeLabel` and throwing. The two vocabularies are
 * asserted equal by `tests/test_web_static.py`; this is what a deployment with
 * mismatched halves does in the meantime, and it is the same choice
 * `routeKind` makes about a row it cannot classify.
 * @param {any} kind
 * @returns {string}
 */
function endpointKind(kind) {
  return ROUTE_KINDS.indexOf(String(kind)) >= 0 ? String(kind) : ROUTE_UNKNOWN;
}

/**
 * Which of the server's configured endpoints a typed model should go to.
 *
 * Only ever a provider *name*, and only when a model was typed. A picked row
 * carries its own provider, which the server reads off the catalogue itself --
 * where a model is served from is a fact about the model rather than something
 * a request gets to assert.
 * @returns {string|undefined}
 */
function chosenEndpoint() {
  if (!typedId()) return undefined;
  return store.customEndpoint || undefined;
}

/** The submitted body, exactly the fields the contract defines. */
function submission() {
  /** @type {Record<string, any>} */
  const body = {
    documents: store.docs.map((doc) => ({ name: doc.name, text: doc.text })),
    base: store.base || undefined,
    fidelity: store.fidelity || undefined,
    verify_depth: store.verifyDepth || undefined,
    title_policy: store.titlePolicy || undefined,
    merge_model: chosenModel("merge"),
    model: chosenModel("check"),
    endpoint: chosenEndpoint(),
    // An **id**, never a command. The server looks it up in a file only the
    // operator can write and supplies the program itself; there is no shape of
    // this body that carries a command string, and `jobs.REQUEST_SETTABLE`
    // holds the other end of that by not carrying `LLOSSLESS_COMMAND`.
    command_route: chosenRoute() || undefined,
    // The stated window, only beside a typed id (604). `windowRefusal` has
    // already stopped the button on a figure that is not a whole number in
    // the server's bounds, so what reaches here is one.
    window: typedWindow(),
    // The merge's effort level, only beside a route that takes one (613):
    // the slider's position, which the server maps onto the merge's argv.
    effort: chosenEffort(),
  };
  if (isFinite(store.lossBudget)) body.loss_budget = store.lossBudget;
  for (const key of Object.keys(body)) {
    if (body[key] === undefined) delete body[key];
  }
  return body;
}

/* ------------------------------------------------------------------ */
/* saved defaults (674)                                                */
/* ------------------------------------------------------------------ */

/**
 * The reader's saved settings, from the server, into `store.defaults`.
 *
 * The server has already dropped what it no longer offers (a model gone from
 * an endpoint, a level removed) and named it in `dropped`; `applyDefaults`
 * adds what this page cannot use on top. A failure to read is said, never
 * taken for "no defaults": the page then starts from the server's.
 */
async function loadDefaults() {
  store.defaults = null;
  store.defaultsDropped = [];
  store.defaultsProblem = "";
  try {
    const answer = await getJson(ROUTES.defaults);
    if (answer && answer.saved) {
      store.defaults = answer.defaults || {};
      store.defaultsDropped = (answer.dropped || []).map(
        (/** @type {any} */ entry) => ({ field: String(entry.field || ""),
                                         value: String(entry.value || "") }));
    }
  } catch (error) {
    store.defaultsProblem = describe(error);
  }
}

/**
 * The page's row id for a saved model choice.
 * @param {any} choice `{kind, id, endpoint}` as the server keeps it
 * @returns {string}
 */
function savedRowId(choice) {
  if (!choice || typeof choice.id !== "string") return "";
  if (choice.kind === "route") return COMMAND_PREFIX + choice.id;
  if (choice.kind === "listed") return String(choice.endpoint || "") + ":" + choice.id;
  return choice.id;
}

/**
 * A row this reader can pick right now, by id, or null.
 * @param {string} id
 * @returns {any}
 */
function offeredRow(id) {
  return pickable().find((/** @type {any} */ model) =>
    model.id === id && !isRetired(model) && reachable(model)) || null;
}

/**
 * How a picked row is saved: a route, a catalogue row, or a listed name.
 * @param {any} row
 * @returns {Record<string, string>}
 */
function savedChoice(row) {
  const route = routeOf(row);
  if (route) return { kind: "route", id: String(route.id) };
  if (row.listed) return { kind: "listed", id: wireName(row), endpoint: String(row.provider) };
  return { kind: "catalogue", id: String(row.id) };
}

/**
 * Put saved settings into the store, before the controls render from it.
 *
 * Each value is used only where this page offers it now, and every one it
 * cannot use goes on `store.defaultsDropped` to be named: never a quiet
 * substitute. The render functions then keep what is set here, because
 * each of them keeps a value it offers -- the fidelity slider, the depth and
 * title radios, the loss field when it is not empty, the picked rows, and
 * the effort slider when `effortRoute` names the route it is on. Nothing in
 * the existing order is reordered. A restored effort counts as seen, so the
 * Settings tab does not call it "new" to the reader who chose it.
 * @param {any} saved
 */
function applyDefaults(saved) {
  if (!saved || !store.config) return;
  const dropped = store.defaultsDropped;
  const miss = (/** @type {string} */ field, /** @type {any} */ value) => {
    dropped.push({ field: field, value: String(value) });
  };
  const offers = (/** @type {any[]} */ rows, /** @type {any} */ value) =>
    rows.some((/** @type {any} */ row) => row.value === value);
  const config = store.config;
  if (saved.fidelity !== undefined) {
    if (offers((config.fidelity || {}).levels || [], saved.fidelity)) store.fidelity = saved.fidelity;
    else miss("fidelity", saved.fidelity);
  }
  if (saved.verify_depth !== undefined) {
    if (offers((config.verify_depth || {}).depths || [], saved.verify_depth)) store.verifyDepth = saved.verify_depth;
    else miss("verify_depth", saved.verify_depth);
  }
  if (saved.title_policy !== undefined) {
    if (offers((config.title_policy || {}).policies || [], saved.title_policy)) store.titlePolicy = saved.title_policy;
    else miss("title_policy", saved.title_policy);
  }
  if (typeof saved.loss_budget === "number" && saved.loss_budget >= 0 && saved.loss_budget <= 1) {
    store.lossBudget = saved.loss_budget;
    input("loss-budget").value = String(saved.loss_budget);
  } else if (saved.loss_budget !== undefined) {
    miss("loss_budget", saved.loss_budget);
  }
  const model = saved.model;
  if (model && model.kind === "typed") {
    const endpoint = String(model.endpoint || "");
    const known = !endpoint || providerRows().some(
      (/** @type {any} */ provider) => provider.name === endpoint && provider.configured);
    if (known) {
      store.customOn = true;
      store.customModel = String(model.id);
      store.customEndpoint = endpoint;
      input("custom-model").value = store.customModel;
    } else {
      miss("model", model.id);
    }
  } else if (model) {
    const id = savedRowId(model);
    if (offeredRow(id)) {
      store.mergeModel = id;
      store.checkModel = id;
    } else {
      miss("model", model.id);
    }
  }
  if (saved.check_model) {
    const id = savedRowId(saved.check_model);
    const row = offeredRow(id);
    if (row && store.mergeModel && !typedId() && !chosenRoute() && answersChecks(row)) {
      store.splitRoles = true;
      store.checkModel = id;
    } else {
      miss("check_model", saved.check_model.id);
    }
  }
  if (saved.window !== undefined) {
    if (windowFieldActive()) {
      store.customWindow = String(saved.window);
      input("custom-window").value = store.customWindow;
    } else {
      miss("window", saved.window);
    }
  }
  const route = chosenRouteRow();
  const levels = (route && route.effort && route.effort.levels) || [];
  if (saved.effort !== undefined) {
    if (levels.indexOf(saved.effort) >= 0) {
      store.effortRoute = route.id;
      store.effort = saved.effort;
    } else {
      miss("effort", saved.effort);
    }
  }
  if (model && levels.length) {
    layout.effortShown = true;
    layout.effortSeen = true;
  }
}

/**
 * Every setting back to "not chosen", so the controls render the server's
 * defaults: the reset's half of `startOver`, with the model and effort too.
 */
function clearSettings() {
  store.fidelity = "";
  store.verifyDepth = "";
  store.titlePolicy = "";
  store.lossBudget = 0;
  store.mergeModel = "";
  store.checkModel = "";
  store.splitRoles = false;
  store.customOn = false;
  store.customModel = "";
  store.customEndpoint = "";
  store.customWindow = "";
  store.effort = "";
  store.effortRoute = "";
  input("split-models").checked = false;
  input("custom-toggle").checked = false;
  input("custom-model").value = "";
  input("custom-window").value = "";
  input("loss-budget").value = "";
}

/**
 * The settings this page would run with now, in the shape the server saves.
 *
 * Read through the same functions `submission` reads, so what is saved is
 * what was sent. The stated window goes with the model it was asked for and
 * never alone; effort only beside a route that takes one. No document, no
 * base document, nothing about the run.
 * @returns {Record<string, any>}
 */
function currentDefaults() {
  /** @type {Record<string, any>} */
  const out = {};
  const typed = typedId();
  if (typed) {
    out.model = { kind: "typed", id: typed, endpoint: store.customEndpoint || "" };
  } else {
    const rows = pickable();
    const merge = rows.find((/** @type {any} */ row) => row.id === store.mergeModel);
    if (merge) out.model = savedChoice(merge);
    const check = store.splitRoles && !chosenRoute()
      ? rows.find((/** @type {any} */ row) => row.id === store.checkModel) : null;
    if (merge && check && check.id !== merge.id) out.check_model = savedChoice(check);
  }
  const tokens = typedWindow();
  if (typeof tokens === "number" && isFinite(tokens)) out.window = tokens;
  const effort = chosenEffort();
  if (effort) out.effort = effort;
  if (store.fidelity) out.fidelity = store.fidelity;
  if (store.verifyDepth) out.verify_depth = store.verifyDepth;
  if (store.titlePolicy) out.title_policy = store.titlePolicy;
  if (isFinite(store.lossBudget)) out.loss_budget = store.lossBudget;
  return out;
}

/**
 * Save the settings a run started with. Called once the server accepted it.
 *
 * The box is left exactly as the reader set it (717): it used to untick
 * itself the moment a save worked, "does not remain checked after starting a
 * merge, that is rather unexpected" in the operator's own words. It now
 * stays ticked here and from then on tracks whether the page's current
 * settings still equal what is saved (`syncSaveDefaultsChecked`), so a save
 * that changes nothing further reads as still ticked and a save that is
 * later edited away from reads as unticked again, without this function
 * having to decide either case itself. One that failed leaves the box as it
 * was and says why; the run goes on either way.
 * @param {Record<string, any>} chosen
 */
async function saveDefaults(chosen) {
  try {
    const answer = await sendJson("PUT", ROUTES.defaults, chosen);
    store.defaults = (answer && answer.defaults) || chosen;
    store.defaultsDropped = [];
    store.defaultsProblem = "";
    store.defaultsReset = false;
    store.defaultsNote = { key: "defaults.saved", tone: "ok", detail: "" };
  } catch (error) {
    store.defaultsNote = { key: "defaults.failed", tone: "warn", detail: describe(error) };
  }
  renderDefaults();
}

/**
 * Ask, then reset (723). "Reset to server defaults" both forgets the saved
 * set on the server and puts every live control on the page back to the
 * server's own defaults at once, so it is asked for the same way
 * `confirmStartOver` is: a `<dialog>`, not `window.confirm`, "Keep my
 * settings" first and focused, Escape and the backdrop both keeping
 * everything as it was.
 */
async function confirmResetDefaults() {
  const dialog = /** @type {HTMLDialogElement} */ (el("reset-defaults-dialog"));
  const answer = await new Promise((resolve) => {
    const finish = (/** @type {boolean} */ yes) => {
      el("reset-defaults-ok").onclick = null;
      el("reset-defaults-keep").onclick = null;
      dialog.onclose = null;
      if (dialog.open) {
        if (typeof dialog.close === "function") dialog.close();
        else dialog.removeAttribute("open");
      }
      resolve(yes);
    };
    el("reset-defaults-ok").onclick = () => finish(true);
    el("reset-defaults-keep").onclick = () => finish(false);
    dialog.onclose = () => finish(false);
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "open");
  });
  if (answer) await resetDefaults();
}

/** Forget the saved settings and put the controls back on the server's. */
async function resetDefaults() {
  try {
    await sendJson("DELETE", ROUTES.defaults, undefined);
  } catch (error) {
    setText(el("defaults-line"), t("defaults.reset.failed", { detail: describe(error) }));
    return;
  }
  store.defaults = null;
  store.defaultsDropped = [];
  store.defaultsProblem = "";
  store.defaultsNote = null;
  store.defaultsReset = true;
  clearSettings();
  // Nothing left to be in step with (717): `syncSaveDefaultsChecked` no
  // longer touches the box once `store.defaults` is null, so this is the one
  // place that has to.
  input("save-defaults").checked = false;
  renderControls();
  el("defaults-line").focus();
}

/**
 * "Update my defaults": re-save the stored set with exactly the fields
 * `store.defaultsDropped` named removed, everything else untouched.
 *
 * Distinct from `saveDefaults`, which saves whatever the page is about to
 * run with; this never touches a control the reader has not saved before,
 * it only clears out what the server can no longer use, so the notice does
 * not return for the same drop next time.
 */
async function updateDefaults() {
  const cleaned = Object.assign({}, store.defaults || {});
  for (const entry of store.defaultsDropped) delete cleaned[entry.field];
  try {
    const answer = await sendJson("PUT", ROUTES.defaults, cleaned);
    store.defaults = (answer && answer.defaults) || cleaned;
    store.defaultsDropped = [];
    store.defaultsProblem = "";
    store.defaultsUpdateProblem = "";
    rememberDismissedDrop("");
  } catch (error) {
    store.defaultsUpdateProblem = describe(error);
  }
  renderDefaults();
}

/**
 * The notice's own dismissal (674/686), scoped to the dropped set it was
 * shown for. `localStorage` in a `try`, the same pattern as `storedLocale`:
 * Dismiss must not silence a *later*, different drop, so it is keyed by a
 * hash of the set rather than a bare flag, and a browser that refuses
 * storage still hides the notice for the rest of this page's life through
 * `store.defaultsHidden`.
 */
const DEFAULTS_DISMISS_KEY = "llossless.defaults.dismissed";

/**
 * A small, order-independent hash of the dropped set. Change detection only,
 * not a security digest, so a synchronous 32-bit rolling hash needs no
 * `crypto.subtle` round trip.
 * @param {{field: string, value: string}[]} dropped
 * @returns {string}
 */
function droppedHash(dropped) {
  const text = dropped.map((entry) => entry.field + "=" + entry.value)
    .sort().join("|");
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    hash = (Math.imul(31, hash) + text.charCodeAt(i)) | 0;
  }
  return String(hash >>> 0);
}

/** The dropped-set hash Dismiss was last pressed for in this browser, or "". */
function storedDismissedDrop() {
  try {
    return window.localStorage.getItem(DEFAULTS_DISMISS_KEY) || "";
  } catch (error) {
    return "";
  }
}

/**
 * Remember (or forget) which dropped set Dismiss was pressed for. Never
 * fatal: a browser that will not store the choice still hides the notice
 * for this page load, through `store.defaultsHidden`.
 * @param {string} hash
 */
function rememberDismissedDrop(hash) {
  try {
    if (hash) window.localStorage.setItem(DEFAULTS_DISMISS_KEY, hash);
    else window.localStorage.removeItem(DEFAULTS_DISMISS_KEY);
  } catch (error) {
    // Nothing above needs to know it did not persist.
  }
}

/**
 * One saved value the page did not use, as the notice names it.
 * @param {{field: string, value: string}} entry
 * @returns {string}
 */
function droppedName(entry) {
  const key = "defaults.field." + entry.field;
  const name = t(key);
  const field = name === key ? entry.field : name;
  const value = entry.field === "effort" ? effortName(entry.value)
    : entry.field === "window" ? (figure(Number(entry.value)) || entry.value) : entry.value;
  return value ? field + " " + value : field;
}

/**
 * The three places saved defaults show: the notice in the run bar, the
 * field in the Tuning step, and the checkbox beside Run with its note.
 */
function renderDefaults() {
  const notice = el("defaults-dropped");
  let said = "";
  if (store.defaultsUpdateProblem) {
    said = t("defaults.update.failed", { detail: store.defaultsUpdateProblem });
  } else if (store.defaultsProblem) {
    said = t("defaults.unreadable", { detail: store.defaultsProblem });
  } else if (store.defaultsDropped.length) {
    // A window, an effort level or a checks model belongs to the model it was
    // saved with: when that model is named, they go with it unnamed.
    const lost = store.defaultsDropped.some((entry) => entry.field === "model");
    const named = store.defaultsDropped.filter((entry) =>
      !(lost && ["window", "effort", "check_model"].indexOf(entry.field) >= 0));
    said = t("defaults.dropped", { list: named.map(droppedName).join(", ") });
  }
  // The persisted half of Dismiss: hidden in this browser only while the
  // dropped set is the one it was pressed for (686); a later, different drop
  // is not silenced by an old click.
  const dismissedForThisDrop = store.defaultsDropped.length > 0
    && !store.defaultsUpdateProblem
    && storedDismissedDrop() === droppedHash(store.defaultsDropped);
  notice.hidden = !said || store.defaultsHidden || dismissedForThisDrop;
  el("defaults-update").hidden = !store.defaultsDropped.length;
  setText(el("defaults-dropped-text"), said);

  const field = el("defaults-field");
  field.hidden = !store.defaults && !store.defaultsReset;
  el("defaults-reset").hidden = !store.defaults;
  setText(el("defaults-line"), t(store.defaults ? "defaults.using" : "defaults.reset.done"));
  renderSaveDefaults();
}

/**
 * The checkbox beside Run, and the line that says what the save did.
 *
 * Offered while the run can start (the way to a blocking step holds that
 * cell otherwise) and never while a run goes: it acts at the click. While a
 * run goes, the cell says what the save did; a failure stays said until the
 * next click.
 */
function renderSaveDefaults() {
  const note = store.defaultsNote;
  const button = /** @type {HTMLButtonElement} */ (el("submit"));
  el("save-defaults-field").hidden = store.running || button.disabled;
  const line = el("save-defaults-note");
  const shown = Boolean(note && (store.running || note.tone !== "ok"));
  line.hidden = !shown;
  setState(line, shown && note ? note.tone : "");
  setText(line, shown && note ? t(note.key, { detail: note.detail }) : "");
}

/**
 * Order-independent equality over the plain shapes `currentDefaults` and a
 * saved-defaults object are built from: strings, numbers, booleans and
 * nested objects such as `model`, no arrays. `JSON.stringify` alone is not
 * enough (717): insertion order is not guaranteed to match between a value
 * this page just built and the same value read back from the server.
 * @param {any} a
 * @param {any} b
 * @returns {boolean}
 */
function sameShape(a, b) {
  if (a === b) return true;
  if (typeof a !== "object" || typeof b !== "object" || a === null || b === null) return false;
  const keysA = Object.keys(a), keysB = Object.keys(b);
  if (keysA.length !== keysB.length) return false;
  return keysA.every((key) => sameShape(a[key], b[key]));
}

/**
 * The box beside Run stops being a one-shot request the moment a saved set
 * exists (717): it becomes a live "are these my saved defaults" reading,
 * ticked exactly while the settings the page would submit now agree with
 * what is saved. Called after every settings change and once at load; never
 * from the box's own `change` handler, the one place a reader's click has to
 * be left alone rather than immediately recomputed away. Before a first save
 * (`store.defaults` is null) there is nothing to compare against, so the box
 * stays a plain checkbox the reader ticks to ask for that first save.
 */
function syncSaveDefaultsChecked() {
  if (!store.defaults) return;
  input("save-defaults").checked = sameShape(currentDefaults(), store.defaults);
}

/**
 * Show, on the control that started it, that a run is in flight.
 *
 * The previous signal was the button going grey and the word RUNNING at
 * .78rem in the status line beside it -- "easy to miss", and a merge takes
 * between 23 and 4,559 seconds, so a reader who missed it has nothing to look
 * at for a quarter of an hour. Three things change together and the spinner is
 * only one of them: the label becomes a different word, and `aria-busy` says
 * the same thing to a screen reader, which sees no animation at all.
 * @param {boolean} running
 */
function setRunning(running) {
  store.running = running;
  const button = /** @type {HTMLButtonElement} */ (el("submit"));
  button.disabled = running;
  button.setAttribute("aria-busy", running ? "true" : "false");
  el("submit-spinner").hidden = !running;
  // The idle label names the route; the running one does not, because by then
  // the decision has been made and the banner above says what it was.
  setText(el("submit-label"), running ? t("run.running") : submitLabel());
  // The destructive control is not offered mid-run. Clearing the form under a
  // job that is still going would leave the operator watching a stream whose
  // inputs are gone from the page, and "Stop watching" is the control for
  // stepping away from a run.
  /** @type {HTMLButtonElement} */ (el("start-over")).disabled = running;
  // The save-defaults cell follows the run: the box while idle, the note
  // while a run goes (674). A success note ends with the run.
  if (!running && store.defaultsNote && store.defaultsNote.tone === "ok") store.defaultsNote = null;
  renderSaveDefaults();
}

/** Submit, then watch. */
async function submit() {
  const button = /** @type {HTMLButtonElement} */ (el("submit"));
  // Read at the click, before anything changes, so what is saved is what was
  // sent (674). Saved only once the server has accepted the run.
  const keep = input("save-defaults").checked ? currentDefaults() : null;
  store.defaultsNote = null;
  enableRunTab();
  setRunning(true);
  say("busy", t("word.sending"), t("status.submitting"));
  el("results").hidden = true;
  el("run-card").classList.remove("settled");
  el("progress-wrap").hidden = false;
  renderCliEquivalent(null);
  fill(el("events"), []);
  renderStepGoto(null);
  revealRun(true);
  try {
    const accepted = await sendJson("POST", ROUTES.runs, submission());
    showRetry("");
    store.runId = accepted.id;
    store.cancelling = false;
    store.startedAt = Date.now();
    store.lastMessage = "";
    say("busy", t("word.queued"), (t("status.queued") + " " + expectation()).trim());
    watch(accepted.id);
    startTicking();
    void refreshHistory();
    if (keep) void saveDefaults(keep);
  } catch (error) {
    say("bad", t("word.refused"), t("error.submit", { detail: describe(error) }));
    setRunning(false);
  }
}

/**
 * How long this merge is likely to take, if anybody has measured this model.
 *
 * Only ever from the catalogue's own `seconds_per_merge`, and silent where
 * there is none: a merge takes between 23 and 4,559 seconds, and an invented
 * estimate over a wait that long is worse than no estimate at all.
 * @returns {string}
 */
function expectation() {
  const models = (store.config && store.config.catalogue
    && store.config.catalogue.models) || [];
  const chosen = models.find((/** @type {any} */ model) => model.id === store.mergeModel);
  const seconds = chosen && chosen.measured ? chosen.measured.seconds_per_merge : null;
  if (typeof seconds !== "number") return "";
  return t("run.expect", {
    name: chosen.display_name || chosen.id,
    seconds: duration(seconds),
  });
}

/**
 * @param {unknown} error
 * @returns {string}
 */
function describe(error) {
  if (error instanceof Error && error.message) return error.message;
  if (typeof error === "string" && error) return error;
  return t("error.unknown");
}

/**
 * Follow a run to its end.
 *
 * Two mechanisms, and the second is not redundant. `EventSource` carries the
 * progress the operator watches, resends `Last-Event-ID` on its own when the
 * connection drops, and replays the tail rather than the whole log -- that is
 * the server's `stream()` contract and the reason the page shows detail during
 * a wait that can run to 4,559 seconds. The poll is what fetches the *report*,
 * which the stream does not carry, and it is also the fallback for a browser
 * or a proxy that will not hold a stream open at all.
 * @param {string} id
 */
function watch(id) {
  stopWatching();
  el("cancel").hidden = false;
  showCancelRun(true);
  showNotify(id);

  const stream = new EventSource(route(ROUTES.events, { id: id }));
  store.stream = stream;
  for (const kind of EVENT_KINDS) {
    stream.addEventListener(kind, (event) => {
      onEvent(kind, /** @type {MessageEvent} */ (event));
    });
  }
  stream.onerror = () => { void onStreamError(stream, id); };

  poll(id);
  store.pollTimer = window.setInterval(() => poll(id), 4000);
}

/**
 * `watch`'s `EventSource.onerror`: a closed stream is how a finished run
 * ends too, so an error here is not necessarily a fault.
 *
 * `EventSource` reports the server's ordinary end-of-stream close the same
 * way it reports a real drop, so firing on the error alone flashed
 * "reconnecting" at the end of every run, for the few seconds until the next
 * scheduled poll fetched the report. Polling immediately, here, removes that
 * gap; the reconnecting status is shown only once that poll comes back and
 * the run is still genuinely going, with the stream not already back open by
 * itself (`EventSource` retries `Last-Event-ID` on its own).
 * @param {EventSource} stream
 * @param {string} id
 */
async function onStreamError(stream, id) {
  if (!store.runId || store.report) return;
  await poll(id);
  if (store.stream === stream && store.runId === id && !store.report
      && stream.readyState !== EventSource.OPEN) {
    say("busy", t("word.reconnecting"), t("status.reconnect"));
  }
}

/**
 * Ask, then act. The only path to `startOver`.
 *
 * A confirmation and not an undo: the pasted documents were never on this
 * server in a form the page can get back -- retention exists to delete the
 * copies that were -- so there is nothing to restore and the question has to
 * be asked before rather than after.
 *
 * `<dialog>` rather than `window.confirm` for two reasons. A native confirm
 * paints its buttons in the *browser's* language, which would make "OK" and
 * "Cancel" the only two strings on this page no catalogue can reach; and its
 * body is one run of unstyled prose with no room to say what survives, which
 * here is the run on the server and its entry in the history list.
 */
async function confirmStartOver() {
  const dialog = /** @type {HTMLDialogElement} */ (el("confirm-dialog"));
  const answer = await new Promise((resolve) => {
    const finish = (/** @type {boolean} */ yes) => {
      el("confirm-ok").onclick = null;
      el("confirm-cancel").onclick = null;
      dialog.onclose = null;
      if (dialog.open) {
        if (typeof dialog.close === "function") dialog.close();
        else dialog.removeAttribute("open");
      }
      resolve(yes);
    };
    el("confirm-ok").onclick = () => finish(true);
    el("confirm-cancel").onclick = () => finish(false);
    // Escape, and the backdrop on browsers that dismiss on it. Both are
    // dismissals, so both keep everything -- a dialog that cleared the form
    // because somebody pressed Escape would be worse than no dialog.
    dialog.onclose = () => finish(false);
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "open");
  });
  if (answer) startOver();
}

/**
 * Back to a fresh page, without reloading one.
 *
 * Everything the operator put in and everything that came back: the panes,
 * the base, the settings they moved off the server's defaults, the result and
 * the progress log. The settings are reset by emptying the store fields and
 * re-rendering -- every `render*` in `renderControls` falls back to the
 * server's own default when its store field is empty, which is the same path
 * a first page load takes.
 *
 * What is deliberately *not* touched: the run on the server, the history list
 * and the language. The first two are records with their own retention, and a
 * language is a property of the reader rather than of the form.
 */
function startOver() {
  stopWatching();
  showRetry("");
  store.runId = "";
  // Back to a pane with nothing in it (717): the Current run tab goes back to
  // `aria-disabled`, matching the same pane on a first page load.
  store.hasRun = false;
  const runTab = document.getElementById("output-tab-run");
  if (runTab) runTab.setAttribute("aria-disabled", "true");
  store.cancelling = false;
  store.report = null;
  store.merged = "";
  store.lastMessage = "";
  store.startedAt = 0;
  store.docs = [];
  store.active = 0;
  store.base = "";
  store.fidelity = "";
  store.verifyDepth = "";
  store.titlePolicy = "";
  store.lossBudget = 0;
  store.splitRoles = false;
  store.customOn = false;
  store.customModel = "";
  store.customEndpoint = "";
  store.customWindow = "";
  /** @type {HTMLInputElement} */ (el("split-models")).checked = false;
  input("custom-toggle").checked = false;
  /** @type {HTMLInputElement} */ (el("custom-model")).value = "";
  input("custom-window").value = "";
  // `renderLossBudget` only writes the default into an *empty* field, so the
  // field is emptied here rather than left holding the last typed figure.
  /** @type {HTMLInputElement} */ (el("loss-budget")).value = "";
  // A clean slate for the box too (717): if there is a saved set, applying it
  // below puts the controls back on exactly what it holds and
  // `syncSaveDefaultsChecked` (through `refreshIdleStatus` further down) picks
  // this up as ticked again; if there is none, this is the only place left to
  // set it, since that function only ever touches the box once a save exists.
  input("save-defaults").checked = false;
  // Back to where this reader starts: their saved settings when they have
  // some (674). Nothing is named again that the notice already named.
  if (store.defaults) {
    const named = store.defaultsDropped.slice();
    applyDefaults(store.defaults);
    store.defaultsDropped = named;
  }
  stopRetentionClock();
  store.expiresIn = null;
  store.forgotten = false;
  el("retention-note").hidden = true;
  el("results").hidden = true;
  el("judged-note").hidden = true;
  el("progress-wrap").hidden = true;
  renderCliEquivalent(null);
  el("run-card").classList.remove("settled");
  fill(el("events"), []);
  setText(el("elapsed"), "");
  setRunning(false);
  if (store.config) renderControls();
  while (store.docs.length < minDocuments()) addDocument();
  store.active = 0;
  renderDocuments();
  refreshIdleStatus();
  // Back to the first step and the top, because the control that was clicked
  // is at the bottom of a page whose content has just gone.
  goToStep(STEPS[0]);
  revealRun(false);
  window.scrollTo({ top: 0 });
}

/** Drop the stream and the timers. Leaves the run running on the server. */
function stopWatching() {
  if (store.stream) { store.stream.close(); store.stream = null; }
  if (store.pollTimer) { window.clearInterval(store.pollTimer); store.pollTimer = 0; }
  if (store.tickTimer) { window.clearInterval(store.tickTimer); store.tickTimer = 0; }
  el("cancel").hidden = true;
  el("notify").hidden = true;
  showCancelRun(false);
}

/**
 * Follow a run the page did not submit: one from the history list (660).
 *
 * What a reader who comes back after a restart, or from another tab, needs:
 * the same progress panel and the same status line a submit gives, attached
 * to a run that is already queued or running. The form is left as it is --
 * the documents of that run are on the server, not in these panes.
 * @param {string} id
 */
function follow(id) {
  showRetry("");
  enableRunTab();
  store.runId = id;
  store.report = null;
  store.cancelling = false;
  store.lastMessage = "";
  store.startedAt = Date.now();
  el("results").hidden = true;
  el("run-card").classList.remove("settled");
  el("progress-wrap").hidden = false;
  renderCliEquivalent(null);
  fill(el("events"), []);
  setRunning(true);
  say("busy", t("word.queued"), t("status.queued"));
  watch(id);
  startTicking();
  el("run-card").scrollIntoView({ block: "nearest" });
  revealRun(true);
}

/**
 * Show the log of a run that has stopped: an interrupted or failed one (660).
 *
 * Not `follow`: that polls at once, finds the run over and closes the stream
 * before the replay has arrived, so the reader saw an empty log and the
 * browser an aborted request. Here the stream is read to its end -- the
 * server closes it after the last event of a finished log -- and only then
 * is the status asked for, which puts the reason and the Retry beside it.
 * @param {string} id
 */
function replay(id) {
  stopWatching();
  showRetry("");
  enableRunTab();
  store.runId = id;
  store.report = null;
  store.cancelling = false;
  store.lastMessage = "";
  el("results").hidden = true;
  el("run-card").classList.remove("settled");
  el("progress-wrap").hidden = false;
  renderCliEquivalent(null);
  setText(el("elapsed"), "");
  fill(el("events"), []);
  const stream = new EventSource(route(ROUTES.events, { id: id }));
  store.stream = stream;
  let settled = false;
  const settle = () => {
    if (settled) return;
    settled = true;
    stream.close();
    if (store.stream === stream) store.stream = null;
    if (store.runId === id) void poll(id);
  };
  for (const kind of EVENT_KINDS) {
    stream.addEventListener(kind, (event) => {
      /** @type {any} */
      let payload = null;
      try { payload = JSON.parse(/** @type {MessageEvent} */ (event).data); } catch (_) { return; }
      appendEvent(kind, payload);
      // A backstop for a stream that stays open after its last event: the
      // server ends it, and `onerror` below is the ordinary way out.
      if (kind === "state" && payload.fields && payload.fields.terminal) {
        window.setTimeout(settle, 5000);
      }
    });
  }
  stream.onerror = settle;
  el("run-card").scrollIntoView({ block: "nearest" });
  revealRun(true);
}

/**
 * The run-card Retry button, for `id`, or hidden for "" (660).
 * @param {string} id
 */
function showRetry(id) {
  store.retryId = id;
  const button = /** @type {HTMLButtonElement} */ (el("retry-run"));
  button.hidden = !id;
  button.disabled = false;
}

/**
 * Ask, then retry (660). The dialog says the new run is billed again before
 * anything is sent; "Do not retry", Escape and the backdrop all leave it.
 * On success the page follows the new run, which names the old one.
 * @param {string} id
 */
async function confirmRetry(id) {
  if (!id) return;
  const dialog = /** @type {HTMLDialogElement} */ (el("retry-dialog"));
  const answer = await new Promise((resolve) => {
    const finish = (/** @type {boolean} */ yes) => {
      el("retry-ok").onclick = null;
      el("retry-keep").onclick = null;
      dialog.onclose = null;
      if (dialog.open) {
        if (typeof dialog.close === "function") dialog.close();
        else dialog.removeAttribute("open");
      }
      resolve(yes);
    };
    el("retry-ok").onclick = () => finish(true);
    el("retry-keep").onclick = () => finish(false);
    dialog.onclose = () => finish(false);
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "open");
  });
  if (!answer) return;
  try {
    const accepted = await sendJson("POST", route(ROUTES.retry, { id: id }), {});
    follow(String(accepted.id));
  } catch (error) {
    say("bad", t("word.refused"), t("error.retry", { detail: describe(error) }));
  }
  void refreshHistory();
}

/**
 * Can this browser show a notification the reader could still allow? (660)
 *
 * False where there is no `Notification` at all -- an older browser, an
 * insecure origin -- and where the reader has already refused, so the button
 * is simply not there rather than a control that does nothing.
 * @returns {boolean}
 */
function notifiable() {
  return typeof window.Notification === "function"
    && window.Notification.permission !== "denied";
}

/**
 * The "Notify me" button for the followed run, or hidden (660).
 * @param {string} id
 */
function showNotify(id) {
  const button = /** @type {HTMLButtonElement} */ (el("notify"));
  button.hidden = !id || !notifiable();
  const on = store.notify.has(id);
  button.disabled = on;
  setText(button, t(on ? "run.notify.on" : "run.notify"));
}

/**
 * Ask the browser for permission -- here, on a click, and nowhere else -- and
 * remember that this run should be announced when it lands (660). Silent on
 * every failure: a refusal hides the button and nothing else changes.
 */
async function askToNotify() {
  const id = store.runId;
  if (!id || typeof window.Notification !== "function") return;
  let permission = window.Notification.permission;
  try {
    if (permission === "default") {
      permission = await window.Notification.requestPermission();
    }
  } catch (_) {
    permission = "denied";
  }
  if (permission === "granted") store.notify.add(id);
  showNotify(store.runId === id ? id : "");
}

/**
 * Announce a run that landed, once, if the reader asked (660). The title is
 * "Run finished" or "Run failed" and the body the short id: nothing of any
 * document, since a notification is shown outside this page and can sit on
 * a locked screen.
 * @param {any} run a status payload
 */
function announceLanding(run) {
  const id = String(run.id || "");
  const state = String(run.state || "");
  if (!store.notify.has(id) || store.notified.has(id)) return;
  if (state === "queued" || state === "running") return;
  store.notified.add(id);
  try {
    new window.Notification(t(state === "failed" || state === "interrupted"
      ? "notify.failed" : "notify.done"), { body: id.slice(0, 8), tag: id });
  } catch (_) {
    // A browser that takes the permission and then will not construct one
    // (some mobile ones) degrades to nothing, which is the promise.
  }
}

/**
 * The "Cancel run" button, shown while the page follows a queued or running
 * run (639). Enabled again every time it is shown, so a cancel refused for a
 * run that had just finished does not leave the next run's button dead.
 * @param {boolean} shown
 */
function showCancelRun(shown) {
  const button = /** @type {HTMLButtonElement} */ (el("cancel-run"));
  button.hidden = !shown;
  button.disabled = false;
}

/**
 * Ask, then cancel (639). The dialog says what a cancel cannot undo -- the
 * calls already made are billed -- before anything is sent; "Keep it
 * running", Escape and the backdrop all leave the run alone.
 */
async function confirmCancel() {
  const id = store.runId;
  if (!id) return;
  const dialog = /** @type {HTMLDialogElement} */ (el("cancel-dialog"));
  const answer = await new Promise((resolve) => {
    const finish = (/** @type {boolean} */ yes) => {
      el("cancel-ok").onclick = null;
      el("cancel-keep").onclick = null;
      dialog.onclose = null;
      if (dialog.open) {
        if (typeof dialog.close === "function") dialog.close();
        else dialog.removeAttribute("open");
      }
      resolve(yes);
    };
    el("cancel-ok").onclick = () => finish(true);
    el("cancel-keep").onclick = () => finish(false);
    dialog.onclose = () => finish(false);
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "open");
  });
  if (answer && store.runId === id) await requestCancel(id);
}

/**
 * Send the cancel and say so. The run is not over until the poll reads
 * `cancelled`: a call in flight is being abandoned and the report of what ran
 * is being written, so the status line says "cancelling" until then.
 * @param {string} id
 */
async function requestCancel(id) {
  const button = /** @type {HTMLButtonElement} */ (el("cancel-run"));
  button.disabled = true;
  try {
    await sendJson("POST", route(ROUTES.cancel, { id: id }), {});
    store.cancelling = true;
    say("busy", t("word.cancelling"), t("status.cancelling"));
    void poll(id);
  } catch (error) {
    button.disabled = false;
    say("bad", t("word.refused"), t("error.cancel", { detail: describe(error) }));
  }
}

/** The elapsed clock, which is the only thing that moves during a long wait. */
function startTicking() {
  const tick = () => {
    if (!store.startedAt) return;
    setText(el("elapsed"), t("run.elapsed", {
      time: duration((Date.now() - store.startedAt) / 1000),
    }));
  };
  tick();
  store.tickTimer = window.setInterval(tick, 1000);
}

/**
 * The pipeline stage a progress message belongs to, in a reader's words (714).
 *
 * The stream's messages are the command line's own ("decompose: asking
 * qwen/qwen3-8b", "verify (forward)"), and the status line under the Run
 * button showed them as they came, so a first-time reader was told the run
 * was decomposing. The first word names the stage; each known stage gets
 * one plain sentence here, and the full message stays in the Progress log.
 * Written out rather than built from the word, the `ROUTE_LABEL_KEYS` rule:
 * a stage this table does not name falls back to the message as sent.
 * @type {Record<string, string>}
 */
const STAGE_KEYS = {
  merge: "progress.merge",
  reconcile: "progress.structure",
  title: "progress.structure",
  decompose: "progress.decompose",
  verify: "progress.verify",
  cover: "progress.verify",
};

/**
 * @param {string} message
 * @returns {string}
 */
function stageSaid(message) {
  const word = (/^[a-z]+/.exec(message) || [""])[0];
  const key = Object.prototype.hasOwnProperty.call(STAGE_KEYS, word) ? STAGE_KEYS[word] : "";
  return key ? t(key) : message;
}

/**
 * One frame off the stream.
 * @param {string} kind
 * @param {MessageEvent} event
 */
function onEvent(kind, event) {
  /** @type {any} */
  let payload = null;
  try { payload = JSON.parse(event.data); } catch (_) { return; }
  appendEvent(kind, payload);
  if (kind === "state") return;
  store.lastMessage = String(payload.message || "");
  if (store.cancelling) return;
  if (!store.report) {
    say("busy", t("word.running"), store.lastMessage
      ? t("status.running", { last: stageSaid(store.lastMessage) })
      : t("status.running.nodetail"));
  }
}

/**
 * The `banner` event's seven fields, each with the name it is shown under.
 *
 * `web/events.py` sends seven -- command, model, endpoint, window, fidelity,
 * depth, retrieval -- and its docstring says why: *"here they are seven fields,
 * because the page has seven places to put them"*. The page had none. It rendered every
 * event as its kind plus `message`, and `message` for a banner is the short
 * form `claimcheck merge`, so the first thing an operator saw of their run was
 * **"BANNER / claimcheck merge"** (500).
 *
 * Pairs rather than a joined string, which is the change from that fix. The
 * joined form put five dot-separated values in the column every other row uses
 * for one short sentence, under the word BANNER in the column every other row
 * uses for STEP or DONE -- neither the same as its neighbours nor different on
 * purpose. The operator's words: it *"looks odd, and it is not clear to the
 * user why that is"*. `bannerRow` gives each value its own name and makes the
 * whole thing a header for the run; this function is where the seven are read,
 * and it is still the only place they are read. An eighth, `roles`, arrives
 * only when the model and the endpoint are one role's and not the run's (576).
 * @param {any} payload
 * @returns {Array<[string, string, string?]>} catalogue key, value, and a
 *   literal label for a role group the catalogue has no name for
 */
function bannerFields(payload) {
  // Under `fields`, not flat: `Event.as_dict` nests everything that is not
  // one of the five lifecycle keys, and reading them off the top level got
  // `undefined` five times and fell straight back to the short message --
  // which looked exactly like the bug it was meant to fix.
  const f = payload.fields || {};
  // The depth is on the line an operator reads *while waiting*, not only in
  // the block they read afterwards. Which questions this run is going to ask
  // is decided before the first call and cannot be changed once it is running,
  // so it belongs where the model and the endpoint are: on the line that says
  // what is about to happen.
  /** @type {Array<[string, any]>} */
  const named = [
    ["banner.command", f.command],
    ["banner.model", f.model],
    ["banner.endpoint", f.endpoint],
    ["banner.fidelity", f.fidelity],
    ["banner.depth", f.depth],
    // Before the window rather than after it, because it is the one field on
    // this line that says something may leave the machine (548). A grant the
    // model has is decided before the first call and cannot change once the
    // run is going, so it belongs where the endpoint is: on the line that says
    // what is about to happen, not only in the block read afterwards.
    ["banner.retrieval", f.retrieval],
    ["banner.window", f.window],
    // The merge's effort level on a command run (613), the slider's choice or
    // the route's default, named the way the slider names it.
    ["banner.effort", f.effort ? effortName(String(f.effort)) : ""],
  ];
  // Each role apart, when the server says one Model and one Endpoint row
  // would each describe one role and not the run (576). The groups replace
  // those two rows where they stood: kept beside them, the check's model
  // would still read as the run's. The route is the one the run was billed
  // under, in the words the button used before the click.
  const groups = Array.isArray(f.roles) && f.roles.length > 1 ? f.roles : null;
  /** @type {Array<[string, string, string?]>} */
  const out = [];
  for (const [key, value] of named) {
    if (groups && (key === "banner.model" || key === "banner.endpoint")) {
      if (key === "banner.model") out.push(...groups.map(roleField));
      continue;
    }
    const text = String(value == null ? "" : value).trim();
    if (text) out.push([key, text]);
  }
  return out;
}

/**
 * One role group of the run header: its name, and model, endpoint and route.
 *
 * Named in the button's words when the group is one of the button's two --
 * the merge, or the checks, which are decompose and verify -- and by the
 * engine's role names otherwise, which is what the provenance Route row does
 * for the same case.
 * @param {any} group
 * @returns {[string, string, string?]} catalogue key, value, literal label
 */
function roleField(group) {
  const roles = (group.roles || []).map(String);
  const value = [group.model, group.endpoint,
                 routeLabel(endpointKind(group.route))]
    .map((part) => String(part == null ? "" : part).trim())
    .filter(Boolean).join(" · ");
  if (roles.length === 1 && roles[0] === "merge") return ["banner.role.merge", value];
  if (roles.length === 2 && roles.indexOf("decompose") >= 0
      && roles.indexOf("verify") >= 0) return ["banner.role.check", value];
  return ["", value, roles.join(", ")];
}

/**
 * The banner as a header for the run rather than as a step in it.
 *
 * Full width, no kind column, a label of its own and one name per value. A
 * reader who cannot tell why this row looks different from the rows under it
 * is a reader who has been shown an inconsistency; a reader who can is being
 * told that the run's configuration is not one of its steps.
 * @param {any} payload
 * @returns {HTMLElement}
 */
function bannerRow(payload) {
  const line = document.createElement("li");
  const fields = bannerFields(payload);
  // An older server, or a partial event, degrades to what this row used to
  // show rather than to an empty box with a heading over it.
  if (!fields.length) return eventRow("banner", payload);
  line.className = "run-header";
  const label = document.createElement("span");
  label.className = "run-header-label";
  setText(label, t("banner.heading"));
  line.appendChild(label);
  const grid = document.createElement("div");
  grid.className = "run-header-fields";
  for (const [key, value, literal] of fields) {
    const field = document.createElement("span");
    field.className = "run-field";
    const name = document.createElement("span");
    name.className = "run-field-name";
    setText(name, literal || t(key));
    const shown = document.createElement("span");
    shown.className = "run-field-value mono";
    setText(shown, value);
    field.appendChild(name);
    field.appendChild(shown);
    grid.appendChild(field);
  }
  line.appendChild(grid);
  return line;
}

/**
 * One ordinary line in the progress log: kind, message, and how long it took.
 * @param {string} kind
 * @param {any} payload
 * @returns {HTMLElement}
 */
function eventRow(kind, payload) {
  const line = document.createElement("li");
  const label = document.createElement("span");
  label.className = "kind " + kind;
  setText(label, kind);
  const message = document.createElement("span");
  message.className = "message";
  setText(message, String(payload.message || ""));
  line.appendChild(label);
  line.appendChild(message);
  const seconds = figure(payload.seconds, 1);
  if (seconds !== null) {
    const timing = document.createElement("span");
    timing.className = "secs mono";
    setText(timing, seconds + "s");
    line.appendChild(timing);
  }
  return line;
}

/**
 * One entry in the progress log, whichever of the two shapes it has.
 * @param {string} kind
 * @param {any} payload
 */
function appendEvent(kind, payload) {
  const log = el("events");
  log.appendChild(kind === "banner" ? bannerRow(payload) : eventRow(kind, payload));
  log.scrollTop = log.scrollHeight;
}

/**
 * The status poll. Carries the report once there is one.
 * @param {string} id
 */
async function poll(id) {
  /** @type {any} */
  let status;
  try {
    status = await getJson(route(ROUTES.run, { id: id }));
    // Before anything branches on the state. A page that read the countdown
    // only on the payload that happened to carry a report would have no
    // answer for a run opened from the history list.
    noteExpiry(status);
    // Same reason, one line down: shown from the moment a run is `running`
    // (`web/jobs.py` sets it then, before any model call), not only once
    // there is a report -- so a reader watching the progress log already
    // sees how to reproduce the run they are waiting on.
    renderCliEquivalent(status.cli_equivalent || null);
  } catch (error) {
    say("bad", t("word.lost"), t("status.gone"));
    stopWatching();
    setRunning(false);
    return;
  }
  if ((status.state === "queued" || status.state === "running")
      && status.cancel_requested) {
    store.cancelling = true;
    say("busy", t("word.cancelling"), t("status.cancelling"));
    return;
  }
  if (status.state === "queued") {
    // Where it stands (660), from the server's own count on every poll, so
    // the number moves as the runs ahead of it start.
    if (typeof status.queue_position === "number") {
      say("busy", t("word.queued"), t("status.queued.position", {
        position: status.queue_position, total: status.queue_length,
      }));
    } else if (!store.lastMessage) {
      say("busy", t("word.queued"), t("status.queued"));
    }
    return;
  }
  if (status.state === "running") return;
  stopWatching();
  announceLanding(status);
  if (status.state === "interrupted") {
    // The server stopped under it (660). Never re-run on its own; the reader
    // decides, with the Retry beside this line.
    say("bad", t("word.interrupted"), t("status.interrupted"));
    showRetry(status.retryable ? id : "");
    setRunning(false);
    void refreshHistory();
    return;
  }
  if (status.state === "cancelled") {
    // What the cancel left billed (639), from the report's own count.
    store.cancelling = false;
    say("warn", t("word.cancelled"), typeof status.calls_made === "number"
      ? t("status.cancelled", { n: status.calls_made })
      : t("status.cancelled.queued"));
    setRunning(false);
    void refreshHistory();
    return;
  }
  if (status.state === "failed") {
    say("bad", t("word.failed"), t("status.failed", {
      error: status.error ? shorten(status.error, 200) : t("error.unknown"),
    }));
    showRetry(status.retryable ? id : "");
    setRunning(false);
    void refreshHistory();
    return;
  }
  store.report = status.report || null;
  if (store.report) await showResult(id, store.report);
  setRunning(false);
  void refreshHistory();
}

/* ------------------------------------------------------------------ */
/* the result                                                          */
/* ------------------------------------------------------------------ */

/**
 * @param {string} id
 * @param {any} report
 */
async function showResult(id, report) {
  el("results").hidden = false;
  // Unstick the run bar. Pinned to the bottom of the viewport it is the right
  // place for a control the operator watches for up to 4,559 seconds; over a
  // claims table it is a bar covering the thing it was waiting for.
  el("run-card").classList.add("settled");
  // A new result opens on its own most urgent tab, not the last one's.
  layout.finding = "";
  renderReport(report);
  revealRun(false);

  const download = /** @type {HTMLAnchorElement} */ (el("download-merged"));
  download.href = route(ROUTES.merged, { id: id });
  // The report to *read* is its own route, and it is the only copy that knows
  // this server exists: the server fills `html_report.SLOT` in it with a
  // control that saves the report, so a reader who opened the full report and
  // then wanted to keep it does not have to come back here for this button.
  const open = /** @type {HTMLAnchorElement} */ (el("open-report"));
  open.href = route(ROUTES.reportPage, { id: id });
  // The report to *keep* is the file itself, unchanged: one document with its
  // stylesheet inline and nothing fetched, so saving those bytes *is* the
  // self-contained file. There is one renderer, and the two links differ only
  // in whether the slot is filled. This link works here and could not work on
  // the report page: this page is the server's own origin, so the browser
  // sends the session with it, while the report is sandboxed into an opaque
  // origin whose requests arrive with no cookie at all.
  const save = /** @type {HTMLAnchorElement} */ (el("download-report"));
  save.href = route(ROUTES.report, { id: id });
  // Sources, merged document, `report.json` and `report.html`, in one archive.
  // The same `href` treatment as the two above and for the same reason: the
  // click is intercepted (`wireDownload`), and this is what a reader who
  // copies the link address gets.
  const everything = /** @type {HTMLAnchorElement} */ (el("download-bundle"));
  everything.href = route(ROUTES.bundle, { id: id });
  renderRetention();
  startRetentionClock();

  let merged = "";
  try {
    const answer = await fetch(route(ROUTES.merged, { id: id }));
    merged = answer.ok ? await answer.text() : "";
    if (!answer.ok) {
      setText(el("merged"), t("error.merged", { detail: "HTTP " + answer.status }));
    }
  } catch (error) {
    setText(el("merged"), t("error.merged", { detail: describe(error) }));
  }
  store.merged = merged;
  if (merged) setText(el("merged"), merged);
  announceOutcome(report, merged);
}

/* ------------------------------------------------------------------ */
/* how long this run is kept                                           */
/* ------------------------------------------------------------------ */

/**
 * How often the note is redrawn while a result is on screen, in milliseconds.
 *
 * Five seconds. The work is two catalogue lookups and one `textContent`, so
 * the cost of the fastest useful tick is not worth reasoning about, and the
 * thing being watched for -- the moment the downloads beside it stop working
 * -- is one a reader should not have to refresh the page to find out about.
 */
const RETENTION_TICK_MS = 5000;

/**
 * What this server said was left, minus what has elapsed here since it said it.
 *
 * `null` when there is nothing to count down to, which is a state and not a
 * missing value: retention may be off, or the run may already be a tombstone.
 *
 * **Elapsed time on this machine, never a difference between two clocks.** The
 * server sends seconds remaining rather than an expiry timestamp precisely so
 * that this can be a subtraction of one monotonic reading from another. A page
 * that compared `finished_at` with `Date.now()` would be measuring the gap
 * between the browser's clock and the server's as well as the gap between two
 * moments -- and the laptop that is half an hour out is not rare, it is the
 * one whose owner never fixed it.
 * @returns {number|null}
 */
function remaining() {
  if (store.expiresIn === null) return null;
  return Math.max(0, store.expiresIn - (monotonic() - store.readAt) / 1000);
}

/**
 * A reading from a clock that only goes forwards, in milliseconds.
 *
 * `performance.now()` where there is one. It is monotonic, so an NTP step in
 * the middle of a long-lived tab moves it by nothing at all, where `Date.now()`
 * would jump and take the countdown with it.
 * @returns {number}
 */
function monotonic() {
  return (window.performance && typeof window.performance.now === "function")
    ? window.performance.now() : Date.now();
}

/**
 * Remember what the server just said about this run's remaining life.
 *
 * Called with every run payload, including the ones for runs that have not
 * finished -- `expires_in` is `null` on those, which is the right answer and
 * not a gap: there is no window until there is a finish time to measure it
 * from.
 * @param {any} payload a `/runs/{id}` body
 */
function noteExpiry(payload) {
  const left = payload && payload.expires_in;
  store.expiresIn = typeof left === "number" ? left : null;
  store.forgotten = !!(payload && payload.forgotten_at);
  store.readAt = monotonic();
}

/**
 * Seconds as a span a person reads: days, hours, minutes, or "very soon".
 *
 * The unit is chosen so the number is always two or more, which is why there
 * is no singular of any of these strings to translate and no way for this page
 * to render "1 days". Below two minutes there is no number at all: the exact
 * count is not the useful thing there, and a span that ticks 119, 118, 117 is
 * a countdown clock, which this is deliberately not.
 * @param {number} seconds
 * @returns {string}
 */
function longSpan(seconds) {
  const whole = Math.max(0, seconds);
  if (whole >= 2 * 86400) return t("span.days", { n: Math.round(whole / 86400) });
  if (whole >= 2 * 3600) return t("span.hours", { n: Math.round(whole / 3600) });
  if (whole >= 2 * 60) return t("span.minutes", { n: Math.round(whole / 60) });
  return t("span.soon");
}

/**
 * The retention window this server is on, or `null` for "kept until deleted".
 *
 * `undefined` means `/config` has not arrived, or came from a server old
 * enough not to carry the block. The page says nothing at all in that case,
 * which is the rule every other server-owned bound on this page follows: a
 * sentence about how long documents are kept, written by a page that has not
 * been told, would be a guess about somebody's confidential files.
 * @returns {number|null|undefined}
 */
function retentionBlock() {
  const block = store.config && store.config.retention;
  if (!block) return undefined;
  return typeof block.seconds === "number" ? block.seconds : null;
}

/** How long before the window passes this page starts warning, or null. */
function retentionWarnAt() {
  const block = store.config && store.config.retention;
  const warn = block && block.warn_seconds;
  return typeof warn === "number" ? warn : null;
}

/**
 * The one sentence under the downloads, and whether there are downloads.
 *
 * Four states, and they are four sentences rather than one with a number in
 * it, because they say four different things. Retention off is not a very
 * large window; the last stretch is not the same message as the first; and a
 * run that is gone needs the controls taken away, not greyed out beside an
 * explanation of why they no longer work.
 */
function renderRetention() {
  const note = el("retention-note");
  const actions = el("result-actions");
  const window_ = retentionBlock();
  if (!store.report || window_ === undefined) {
    note.hidden = true;
    return;
  }
  note.hidden = false;
  const left = remaining();
  if (store.forgotten || (window_ !== null && left !== null && left <= 0)) {
    // Gone. The controls come off the page rather than staying as four
    // controls that answer 410 -- which is the shape the operator met: a click
    // that did nothing at all, and one link that explained it.
    setState(note, "bad");
    actions.hidden = true;
    setText(note, t("retention.gone"));
    stopRetentionClock();
    return;
  }
  actions.hidden = false;
  if (window_ === null) {
    setState(note, "");
    setText(note, t("retention.off"));
    return;
  }
  const warn = retentionWarnAt();
  if (left !== null && warn !== null && left <= warn) {
    setState(note, "warn");
    setText(note, t("retention.soon", { left: longSpan(left) }));
    return;
  }
  setState(note, "");
  setText(note, left === null
    ? t("retention.window.only", { window: longSpan(window_) })
    : t("retention.window", { window: longSpan(window_), left: longSpan(left) }));
}

/** Start re-rendering the note. Idempotent: one interval, however often called. */
function startRetentionClock() {
  if (store.retentionTimer) return;
  store.retentionTimer = window.setInterval(renderRetention, RETENTION_TICK_MS);
}

/** Stop it. Called when the run leaves the page, and when it is past saving. */
function stopRetentionClock() {
  if (store.retentionTimer) {
    window.clearInterval(store.retentionTimer);
    store.retentionTimer = 0;
  }
}

/**
 * This run is gone, told to us by a route rather than worked out from a clock.
 *
 * A 410 from any download is the authoritative answer, and it outranks the
 * countdown: a browser suspended in a closed laptop for a day comes back with
 * a `performance.now()` that under-counts, so the page can believe a run is
 * alive that this server forgot hours ago. The first click then says so.
 */
function forgetShownRun() {
  store.forgotten = true;
  store.expiresIn = 0;
  renderRetention();
}

/**
 * Fetch one of this run's artefacts and save it, or say why that did not work.
 *
 * **The whole reason this is not a plain anchor.** `download` on an `<a>`
 * pointed at a route is a control with no failure path: a non-200 is not
 * rendered, not saved and not reported, so a reader whose run had been
 * forgotten clicked Download and *nothing happened*. That is the operator's
 * report, word for word, and it is the worst available shape of this bug --
 * the one route that did explain itself was the link they were least likely
 * to click. Fetching first means the server's own sentence reaches the status
 * line, including the one that names the retention flag.
 *
 * The bytes are handed over through a `blob:` URL belonging to this document,
 * which reaches no network. The report page's own control is **not** this
 * mechanism: that page is sandboxed into an opaque origin and cannot ask this
 * server for anything, so it carries the file in a `data:` URL instead (534).
 * Two controls, two mechanisms, and the difference is the isolation rather
 * than a preference.
 * @param {string} url
 * @param {string} filename
 * @returns {Promise<void>}
 */
async function saveFrom(url, filename) {
  /** @type {Response} */
  let answer;
  try {
    answer = await fetch(url, { headers: { Accept: "*/*" } });
  } catch (error) {
    say("bad", t("word.lost"), t("download.failed", { detail: describe(error) }));
    return;
  }
  if (!answer.ok) {
    const body = await answer.json().catch(() => null);
    say("bad", t("word.lost"), t("download.failed", {
      detail: errorMessage(body, answer.status),
    }));
    if (answer.status === 410) forgetShownRun();
    return;
  }
  const blob = await answer.blob();
  const href = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = href;
  anchor.download = filename;
  // In the document for the click. A detached anchor downloads in some
  // browsers and is ignored in others, and this is a control that has already
  // failed once by doing nothing.
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  // Not in the same tick as the click: revoking an object URL while the
  // download it names is still being started cancels the download.
  window.setTimeout(() => URL.revokeObjectURL(href), RETENTION_TICK_MS);
}

/**
 * Turn one download anchor into a fetch that can report a refusal.
 *
 * The `href` stays what it was -- the route this control points at, which is
 * what a reader copying the link address gets and what the suite asserts --
 * and the filename comes from the anchor's own `download` attribute, so the
 * markup goes on being the one place the saved name is written down.
 * @param {HTMLElement} anchor
 * @param {string} template one of `ROUTES`
 */
function wireDownload(anchor, template) {
  anchor.addEventListener("click", (event) => {
    event.preventDefault();
    if (!store.runId) return;
    const name = /** @type {HTMLAnchorElement} */ (anchor).download;
    void saveFrom(route(template, { id: store.runId }), name);
  });
}

/* ------------------------------------------------------------------ */
/* the merged document: selecting it, and copying it                   */
/* ------------------------------------------------------------------ */

/**
 * Select exactly the merged document, and nothing else on the page (561).
 *
 * The operator: *"if we select the text box and press ctrl+a it would select
 * the text in the box and not the entire website"*. The box is a `<pre>`, so
 * the browser has nothing to scope the shortcut to and selects the document.
 * A `<textarea>` would scope it for free and would also make a read-only
 * artefact editable, which is a worse answer to a keyboard shortcut than
 * writing the shortcut.
 * @returns {boolean} false when there is nothing to select
 */
function selectMerged() {
  const box = el("merged");
  const selection = window.getSelection();
  if (!selection || !box.textContent) return false;
  const range = document.createRange();
  range.selectNodeContents(box);
  selection.removeAllRanges();
  selection.addRange(range);
  return true;
}

/**
 * The copy fallback: select the document and let the browser do the copy.
 *
 * Reached on a page that is **not a secure context** -- plain `http` to a LAN
 * address, which is a deployment this project supports and where
 * `navigator.clipboard` is simply absent. `execCommand` is deprecated and is
 * the only thing left that can complete a copy there; where even that refuses,
 * the selection stands and the reader is told to press the shortcut
 * themselves. What this must never do is nothing: a control that goes quiet is
 * a control somebody presses again.
 * @returns {string} "selected" when the browser copied it, "manual" otherwise
 */
function copyBySelection() {
  if (!selectMerged()) return "";
  let done = false;
  try {
    done = document.execCommand("copy");
  } catch (error) {
    done = false;
  }
  return done ? "selected" : "manual";
}

/**
 * Copy the merged document, and say which of the three paths ran.
 *
 * `store.merged` rather than the box's text: where the fetch failed the box
 * holds the sentence saying so, and copying an error message would be a
 * control that reports success over a failure.
 */
async function copyMerged() {
  const note = el("copy-note");
  const say = (/** @type {string} */ key) => {
    setText(note, t(key));
    note.hidden = false;
  };
  if (!store.merged) { say("results.copy.nothing"); return; }
  // `isSecureContext` as well as the object: a browser can expose the object
  // and refuse the write, and the two failures read the same to a user.
  if (window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText) {
    try {
      await navigator.clipboard.writeText(store.merged);
      say("results.copy.done");
      return;
    } catch (error) {
      // Permission refused at the prompt, or a browser that offers the API and
      // will not use it here. Fall through rather than report a failure: the
      // selection path still works and still ends with the text copied.
    }
  }
  const how = copyBySelection();
  say(how === "selected" ? "results.copy.done"
      : how === "manual" ? "results.copy.manual" : "results.copy.nothing");
}

/* ------------------------------------------------------------------ */
/* the CLI-equivalent block                                            */
/* ------------------------------------------------------------------ */

/**
 * Select exactly the CLI-equivalent block's command, and nothing else (561's
 * reason, applied to the second `<pre>` this page grew).
 * @returns {boolean} false when there is nothing to select
 */
function selectCliCommand() {
  const box = el("cli-command");
  const selection = window.getSelection();
  if (!selection || !box.textContent) return false;
  const range = document.createRange();
  range.selectNodeContents(box);
  selection.removeAllRanges();
  selection.addRange(range);
  return true;
}

/** `copyBySelection`'s fallback, aimed at the command box. @returns {string} */
function copyCliCommandBySelection() {
  if (!selectCliCommand()) return "";
  let done = false;
  try {
    done = document.execCommand("copy");
  } catch (error) {
    done = false;
  }
  return done ? "selected" : "manual";
}

/** Copy the rendered command (env lines and all), and say which path ran. */
async function copyCliCommand() {
  const note = el("cli-copy-note");
  const say = (/** @type {string} */ key) => {
    setText(note, t(key));
    note.hidden = false;
  };
  const text = el("cli-command").textContent || "";
  if (!text) { say("cli.copy.nothing"); return; }
  if (window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      say("cli.copy.done");
      return;
    } catch (error) {
      // Falls through to the selection path, `copyMerged`'s reason.
    }
  }
  const how = copyCliCommandBySelection();
  say(how === "selected" ? "cli.copy.done"
      : how === "manual" ? "cli.copy.manual" : "cli.copy.nothing");
}

/**
 * The CLI-equivalent block: how this run reads as an `llossless merge`
 * command, off the payload `web/cli_render.py` rendered from the settings the
 * job actually ran with (`{command, env, documents, shell, notes}`).
 *
 * Redrawable from `store.cliEquivalent` alone, on `renderReport`'s terms: a
 * language change re-words the documents sentence and the notes -- both are
 * catalogue strings, not server prose -- without a new request. `null` hides
 * the block, which is its state before a run has started and after
 * `startOver`.
 *
 * **Notes are `{key, ...params}`, never sentences.** `cli_render.py`'s own
 * docstring says why: the five things a note can say are a closed set, and
 * the sentence belongs in `locales/{en,de}.json` under `cli.note.<key>`, read
 * the same way `t("kind." + finding.kind)` reads a family of keys elsewhere
 * on this page.
 * @param {any} payload
 */
function renderCliEquivalent(payload) {
  store.cliEquivalent = payload || null;
  const block = /** @type {HTMLDetailsElement} */ (el("cli-equivalent"));
  if (!payload) {
    block.hidden = true;
    return;
  }
  block.hidden = false;
  el("cli-copy-note").hidden = true;
  setText(el("cli-copy-note"), "");

  const docs = Array.isArray(payload.documents) ? payload.documents : [];
  el("cli-documents-hint").hidden = docs.length === 0;
  fill(el("cli-docs"), docs.map((/** @type {any} */ doc) => {
    const row = document.createElement("li");
    const label = document.createElement("span");
    setText(label, doc.label + " → ");
    const filename = document.createElement("span");
    filename.className = "cli-filename";
    setText(filename, doc.filename);
    row.appendChild(label);
    row.appendChild(filename);
    return row;
  }));

  const lines = (Array.isArray(payload.env) ? payload.env : [])
    .concat(payload.command ? [payload.command] : []);
  setText(el("cli-command"), lines.join("\n"));
  setText(el("cli-shell"), t("cli.shell.posix"));

  const notes = Array.isArray(payload.notes) ? payload.notes : [];
  el("cli-notes-wrap").hidden = notes.length === 0;
  fill(el("cli-notes"), notes.map((/** @type {any} */ note) => {
    const row = document.createElement("li");
    const params = Object.assign({}, note);
    delete params.key;
    if (note.key === "command_route") {
      params.label = note.label ? ("“" + note.label + "”") : t("cli.route.generic");
    }
    setText(row, t("cli.note." + note.key, params));
    return row;
  }));
}

/**
 * Every part of the result that is made of sentences, drawn from one report.
 *
 * Split out of `showResult` so that a language change can redraw it without
 * asking the server for anything. What is deliberately **not** in here is the
 * merged document and the four controls beside it -- three saves and the link
 * that opens the report as a page. The merged document is the operator's own
 * text, and `merged.md`, `report.html` and `bundle.zip` are records whose
 * bytes do not depend on which language this page happens to be in. A record
 * that came back in a different language because the reader's browser was
 * configured differently would not be reproducible, and the four controls go
 * on pointing at the same artefacts whatever the picker says.
 * @param {any} report
 */
function renderReport(report) {
  // The copy note is about an action, and this function runs again on a
  // language change (561). A sentence saying "Copied." in the language the
  // reader has just left is a stale string in the wrong language, and the
  // action it describes is over.
  el("copy-note").hidden = true;
  setText(el("copy-note"), "");
  for (const hook of FINDING_SECTIONS) el(hook).removeAttribute("data-attention");
  renderVerdict(report);
  // Over a run that graded nothing there is no rationale on the page and no
  // document any verdict was read against, so the sentence explaining both
  // would be furniture. `sectionState`'s rule, applied to a note.
  el("judged-note").hidden = (report.verdicts || []).length === 0;
  renderMismatch(report);
  renderReview(report);
  const conflicts = renderConflicts(report);
  const omitted = renderOmitted(report);
  renderAttributions(report);
  renderNumbers(report);
  renderAdditions(report);
  const claimed = renderClaims(report);
  const checked = renderChecks(report);
  renderProvenance(report);
  renderTiles([conflicts, omitted, claimed, checked]);
  syncFindingTabs();
}

/**
 * One stat tile (redesign A): a section's title key, and the state and count
 * its chip was just given. The tiles restate the chips; they count nothing.
 * @typedef {{ title: string, state: string, count: number }} Tile
 */

/**
 * @param {string} title catalogue key of the section's title
 * @param {string} state a key of `CHIP_STATES`
 * @param {number} count
 * @returns {Tile}
 */
function tileOf(title, state, count) {
  return { title: title, state: state, count: count };
}

/**
 * The tiles under the verdict: the figure large, the section's name above it
 * and the chip's own words under it. A section that did not run shows a dash
 * and "not checked", never a zero, which is `sectionState`'s rule.
 * @param {Tile[]} tiles
 */
function renderTiles(tiles) {
  fill(el("stat-tiles"), tiles.map((tile) => {
    const item = document.createElement("li");
    item.className = "stat-tile";
    const chosen = CHIP_STATES[tile.state] || CHIP_STATES.notchecked;
    setState(item, chosen.tone);
    const shown = document.createElement("span");
    shown.className = "tile-figure";
    setText(shown, tile.state === "notchecked" ? "-" : (figure(tile.count) || "0"));
    const label = document.createElement("span");
    label.className = "tile-label";
    setText(label, t(tile.title));
    const note = document.createElement("span");
    note.className = "tile-note";
    chipFor(note, tile.state, tile.count);
    item.appendChild(shown);
    item.appendChild(label);
    item.appendChild(note);
    return item;
  }));
}

/**
 * The one sentence at the top, with the merged length in it.
 * @param {any} report
 * @param {string} merged
 */
function announceOutcome(report, merged) {
  const code = report.exit_code;
  const tone = code === 0 ? "ok" : code === 2 ? "warn" : "bad";
  const word = code === 0 ? t("word.clean")
    : code === 2 ? t("word.inconclusive")
    : t("word.findings");
  const advice = adviceFor(report);
  say(tone, word, t("status.done", {
    chars: figure(merged.length) || "0",
    advice: advice,
  }));
}

/**
 * The banner. Four outcomes, because `report.exit_code` has four.
 * @param {any} report
 */
function renderVerdict(report) {
  const code = report.exit_code;
  const tone = code === 0 ? "ok" : code === 2 ? "warn" : "bad";
  const label = code === 0 ? t("verdict.clean")
    : code === 1 ? t("verdict.document")
    : code === 2 ? t("verdict.inconclusive")
    : code === 3 ? t("verdict.record")
    : t("verdict.unknown");
  const advice = adviceFor(report);
  const banner = el("verdict");
  banner.classList.remove("none");
  setState(banner, tone);
  setText(el("verdict-label"), label);
  // The one caveat that suspends a guarantee rather than narrowing one, so it
  // goes on every verdict and not only on the clean one: a reader who chose
  // `open` is owed it whatever the exit code, and a notice that appears only
  // when nothing else went wrong is a notice missing from the report anyone
  // reads carefully. Counted in claims excused rather than records declared,
  // because one declaration can cover several claims and the number that
  // matters is how much went unchecked.
  const excused = (report.additions_cover || [])
    .reduce((/** @type {number} */ n, /** @type {any} */ ids) => n + (ids || []).length, 0);
  const said = [
    advice,
    excused ? t("advice.additions", { n: excused }) : "",
    retrievalAdvice(report),
    suspendedGuarantee(report),
  ].filter(Boolean).join(" ");
  setText(el("verdict-text"), said);
}

/**
 * The three outcomes a run at the retrieving level can reach, and their words.
 *
 * Written out rather than built from `"advice.retrieval." + outcome`, the
 * `ROUTE_LABEL_KEYS` rule: the key checks see a literal and cannot see a
 * concatenation, and an outcome this table does not name renders nothing
 * rather than a key.
 * @type {Record<string, string>}
 */
const RETRIEVAL_KEYS = {
  retrieved: "advice.retrieval.retrieved",
  "not-retrieved": "advice.retrieval.notretrieved",
  unmeasured: "advice.retrieval.unmeasured",
};

/**
 * What a run at the retrieving level achieved, on the verdict (571).
 *
 * `sourcing.retrieval` is `retrieved`, `not-retrieved`, `unmeasured`, or empty
 * below that level, where nothing was promised -- the server works it out
 * (`report.retrieval_outcome`) and the page never does, because it holds no
 * fidelity vocabulary and would have to learn which level retrieves.
 *
 * On every exit code and in the report's own words, the rule
 * `suspendedGuarantee` follows: the verdict line says it on all three written
 * surfaces, and before this the page was the one surface a reader of an
 * unmeasured run could read from top to bottom without being told that nobody
 * knows whether a source was looked up. `unmeasured` is never folded into
 * either of the other two; it is the one outcome that can stand over a run
 * that really did retrieve.
 * @param {any} report
 * @returns {string}
 */
function retrievalAdvice(report) {
  const sourcing = report.sourcing || {};
  const key = RETRIEVAL_KEYS[String(sourcing.retrieval || "")];
  if (!key) return "";
  const turns = sourcing.tool_use || {};
  const silent = Number(turns.unmeasured_calls) || 0;
  return t(key, {
    n: Number(turns.calls_with_tool_use) || 0,
    m: Number(turns.measured_calls) || 0,
    // A run with no silent call counted -- none reported at all -- has no
    // number to give, and "0 of its calls" would read as none being silent.
    k: silent ? silent : t("word.all"),
    // The merge's calls on a merge (665): the counts are the merge role's,
    // and "none of its 1 call(s)" over a run that made six would be a false
    // sentence with a true number in it.
    calls: sourcing.retrieval_judged_on === "merge"
      ? t("word.calls.merge")
      : t("word.calls"),
  });
}

/**
 * The sentence a run that never checked for invention owes its reader.
 *
 * The second caveat that suspends a guarantee rather than narrowing one, and
 * it sits beside `open`'s for the same reason: a notice that appears only on a
 * clean exit is a notice missing from the report anyone reads carefully, so it
 * goes on every verdict. The distinction it draws is this project's
 * most-repeated one -- "not checked" is not "checked and clean"
 * (`sectionState`) -- said at the level of the whole run rather than of one
 * section, because at this depth the reverse pass did not run at all.
 *
 * Decided from the server's `detects_invention` flag and never from the depth's
 * name. The page is served its vocabulary; the day a third depth exists it will
 * be described correctly here without an edit, and a `store.config` that never
 * arrived leaves this silent rather than guessing -- a page in that state
 * renders `error.config` and no report at all.
 * @param {any} report
 * @returns {string}
 */
function suspendedGuarantee(report) {
  const policy = ((report.provenance || {}).merge_policy) || {};
  const depths = ((store.config || {}).verify_depth || {}).depths || [];
  const ran = depths.find(
    (/** @type {any} */ depth) => depth.value === policy.verify_depth);
  return ran && ran.detects_invention === false ? t("advice.noinvention") : "";
}

/**
 * The six things a chip can say, and the colour each is allowed.
 *
 * Only `clean` is green and only `findings` is amber. The other four are
 * neutral, because none of them is a result: `notchecked` is nobody looked,
 * `notapplicable` is this level never asks for that, `ungraded` is the
 * merge's own account of itself which this tool does not grade, and
 * `measured` is a number with no pass or fail attached to it. Every one of
 * them carries a word as well as a colour.
 *
 * `notchecked` and `notapplicable` read alike at a glance and mean two
 * different things (716): a check that did not run is a gap in the answer,
 * one that does not apply at the chosen level was never asked for, the same
 * way this level's schema never hands the merge the field. Telling them
 * apart is why the summary tile's "N did not run" counts the first and not
 * the second -- an `open`-only check reading as a gap on every `high` run
 * would be a false alarm on the common case.
 * @type {Record<string, {tone: string, key: string}>}
 */
const CHIP_STATES = {
  clean: { tone: "ok", key: "chip.clean" },
  findings: { tone: "warn", key: "chip.findings" },
  notchecked: { tone: "", key: "chip.notchecked" },
  notapplicable: { tone: "", key: "chip.notapplicable" },
  ungraded: { tone: "", key: "chip.ungraded" },
  measured: { tone: "", key: "chip.measured" },
  unchecked: { tone: "", key: "chip.unchecked" },
};

/**
 * Write one of those six onto a chip.
 * @param {HTMLElement} chip
 * @param {string} state a key of `CHIP_STATES`
 * @param {number} [count] for the states whose word carries one
 */
function chipFor(chip, state, count) {
  const chosen = CHIP_STATES[state] || CHIP_STATES.notchecked;
  setState(chip, chosen.tone);
  setText(chip, t(chosen.key, { n: count || 0 }));
}

/**
 * How a section's chip reads, which is where "not checked" is kept apart
 * from "checked and clean".
 *
 * The distinction is the project's most-repeated failure: an empty findings
 * list under `ran: false` means nobody looked, and a green all-clear over it
 * is a lie the operator has no way to see through. So a section that did not
 * run gets the neutral chip and the words "not checked", and the body says in
 * a sentence that an empty list there is not a result.
 * @param {HTMLElement} chip
 * @param {boolean} ran
 * @param {number} count
 * @returns {string} which state was chosen
 */
function sectionState(chip, ran, count) {
  const state = !ran ? "notchecked" : count > 0 ? "findings" : "clean";
  chipFor(chip, state, count);
  return state;
}

/**
 * Mark a finding section for attention, or leave it unmarked.
 *
 * Only ever marks. A section that has findings in it, or that could not be
 * checked at all, is the one a reader has to see without going looking. The
 * sections are tabs since 673, not folds, so the mark is what
 * `syncFindingTabs` reads to pick the tab a new result opens on; the marks
 * are cleared by `renderReport` before the renderers run.
 * @param {string} hook
 * @param {boolean} should
 */
function openIf(hook, should) {
  if (should) el(hook).setAttribute("data-attention", "true");
}

/**
 * A sentence in place of a list, for a section with nothing in it.
 * @param {boolean} ran
 * @param {string} emptyKey
 * @returns {HTMLElement}
 */
function emptyNote(ran, emptyKey) {
  const note = document.createElement("p");
  note.className = "hint";
  setText(note, ran ? t(emptyKey) : t("section.notchecked"));
  return note;
}

/**
 * A short, stable id for one finding, addition or verdict, built from its own
 * content rather than from where it happens to land in any one list (717).
 *
 * `renderReview`'s list and a section's own list walk the same findings
 * through two different filters and orders -- `renderNumbers` sorts faults
 * before warnings, say -- so a position-based id would silently point at the
 * wrong entry the moment either order changed, and nothing would fail loudly
 * enough to notice. This is content, not a security digest: the same 32-bit
 * rolling hash `droppedHash` already uses, prefixed with a family tag so a
 * verdict, a structural finding and an addition record can never collide.
 * @param {string} family "verdict", "structural" or "addition"
 * @param {string} content whatever makes this one entry distinct within its family
 * @returns {string}
 */
function findingId(family, content) {
  const text = family + "|" + content;
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    hash = (Math.imul(31, hash) + text.charCodeAt(i)) | 0;
  }
  return "finding-" + family + "-" + (hash >>> 0).toString(36);
}

/**
 * One bulleted item: a bold lead-in, a sentence, and named detail under it.
 * @param {string} label
 * @param {string} text
 * @param {Array<[string, string, boolean]>} detail name, value, quote it
 * @param {string} tone
 * @param {HTMLElement|null} [extra] one block below the named detail
 * @param {string} [id] this entry's `findingId`, so the review list (488, 717)
 *   can jump a reader here directly; omitted for a card nothing ever jumps to.
 * @returns {HTMLElement}
 */
function findingItem(label, text, detail, tone, extra, id) {
  const item = clone("tpl-finding");
  if (tone) item.classList.add(tone);
  if (id) item.id = id;
  setText(find(item, "finding-label"), label);
  setText(find(item, "finding-text"), text);
  const list = find(item, "finding-detail");
  for (const [name, value, quote] of detail) {
    if (!value) continue;
    const term = document.createElement("dt");
    setText(term, name);
    const definition = document.createElement("dd");
    if (quote) definition.className = "quote";
    setText(definition, value);
    list.appendChild(term);
    list.appendChild(definition);
  }
  // Outside the `<dl>` rather than as a fourth `<dd>`, because it is not a
  // named value: it is the same two texts again in a layout, and a definition
  // list item whose term is "here they are again" would be a term nobody
  // needs to read.
  if (extra) find(item, "finding-extra").appendChild(extra);
  return item;
}

/**
 * The two sides of one finding, one directly above the other (561).
 *
 * **The same three lines the Markdown report writes**, in the same order, with
 * the labels padded to one width so the texts start in the same column -- that
 * column is the whole request: *"so the difference can be read by scanning
 * down a column rather than along a sentence"*. The strings are localised
 * here, as the row's own labels already were, but the *diff* is the engine's
 * published one; the page never diffs anything itself (544's rule).
 *
 * Returns null where there is nothing to stack, and where there is only one
 * side: a disclosure over a single line is a control that hides one line.
 * @param {any} finding
 * @returns {HTMLElement|null}
 */
function stackPanel(finding) {
  /** @type {Array<[string, string]>} */
  const rows = [];
  if (finding.source_text) rows.push([t("detail.insource"), String(finding.source_text)]);
  if (finding.merge_text) rows.push([t("detail.inmerge"), String(finding.merge_text)]);
  if (rows.length < 2) return null;
  const shown = String(finding.difference || "");
  if (shown) rows.push([t("detail.changed"), shown]);
  const width = Math.max(...rows.map(([name]) => name.length));
  const stack = clone("tpl-stack");
  setText(find(stack, "stack-summary"), t("detail.stack"));
  setText(find(stack, "finding-stack"), rows.map(
    ([name, value]) => (name + ":").padEnd(width + 1) + " " + value).join("\n"));
  return stack;
}

/**
 * Every structural finding the engine publishes, from all three blocks.
 *
 * `structural.findings` is deliberately *not* all of them: `report.as_dict`
 * keeps the prompt-leak and restated-claim findings in their own blocks,
 * because they are not among the nine mechanical checks. The page read only
 * the first block, so those two families were counted in the checks table --
 * "Restated claims, 1 to read" -- and rendered nowhere at all (488). An
 * operator reading a long document saw a chip pointing at an item no section
 * contained.
 *
 * Collected in one place so the two section renderers below cannot disagree
 * about where a family lives, and so a fourth block added to the engine has
 * one obvious place to be added here.
 * @param {any} report
 * @returns {Array<any>}
 */
function structuralFindings(report) {
  return [
    ...((report.structural || {}).findings || []),
    ...((report.prompt_leaks || {}).findings || []),
    ...((report.restated_claims || {}).findings || []),
    // The fourth block (569), and the reason this collector exists: a merge
    // that credited a fact to the wrong document exits 1, and until this line
    // the page showed that exit and no section holding the reason (572). It
    // goes to a section of its own, not to either partition below, so the two
    // renderers that filter by kind skip it and `renderAttributions` takes it.
    ...((report.attributions || {}).findings || []),
    // The fifth (601): a decimal written in the other convention, a numeral
    // readable two ways, a merged value that changed, a document whose
    // numerals go against its language. Its own section again,
    // `renderNumbers`, and the partitions below skip it by kind.
    ...((report.number_format || {}).findings || []),
  ];
}

/**
 * What a clean run says, affirmatively and with its denominators (495).
 *
 * The old string read "Nothing was dropped, contradicted or invented that
 * this tool could find" and had three faults. It was negative, where the
 * result is positive. It listed three failure classes and not the fourth --
 * `partially_dropped` -- which is the narrowing `report.verdict_line`'s own
 * comment says task 13 already had to fix in the CLI's version of this
 * sentence. And "that this tool could find" hedges without informing: a
 * reader cannot act on it, while the number of claims checked is exactly what
 * tells them how much the clean result is worth.
 *
 * So it mirrors the CLI: what held, then how much was examined to establish
 * it. A run with nothing to check says that instead, because "every claim
 * survived" over zero claims is true and worthless.
 * @param {any} report
 * @returns {string}
 */
function cleanAdvice(report) {
  const coverage = report.coverage || {};
  const forward = Number(coverage.forward_submitted || 0);
  const reverse = Number(coverage.reverse_submitted || 0);
  if (!forward && !reverse) return t("advice.clean.nothing");
  // A clean run with nothing coming back from the reverse direction cannot be
  // told it was checked "in both directions". Found by driving the page: at
  // `--verify-depth coverage` the banner read *"nothing in the merge goes
  // beyond them ... in both directions"* over a run in which the merged
  // document was never read back -- the one sentence on the page that says
  // outright what this depth does not check, said about a run that did not
  // check it. The suspended-guarantee sentence then followed and contradicted
  // it.
  //
  // Keyed on the reverse count rather than on the depth, which is both more
  // general and more honest: a `full` run whose reverse pass returned nothing
  // is in the same position, and "none in the other direction" is true of
  // every way of getting here. It is the section chips' rule (`sectionState`)
  // applied to the run's one-line verdict.
  if (!reverse) return t("advice.clean.forward", { forward: forward });
  return t("advice.clean", { forward: forward, reverse: reverse });
}

/**
 * What to tell a reader to do (488, 717).
 *
 * `advice.look` used to name which sections held something -- "Conflicts and
 * omitted content below need a look" -- because the review list above them
 * was itself unnamed and unreachable: a run whose one finding was a
 * misattribution sent the reader to two empty sections while the item sat in
 * a third (572), so naming the *right* sections became the fix. Now that the
 * review list ("What needs your attention") names each item's own section and
 * jumps a reader straight to it on a click (717), the sentence naming
 * sections again in prose above that list is the thing it used to fix
 * happening a second time, in German rendered from a mid-sentence list of
 * capitalised section names that read as a grammar mistake. One plain
 * sentence for every run that exits 1, whatever it found and wherever it is.
 *
 * One function and two callers, because the banner and the status line
 * carried the same four-line expression twice and that is how they would
 * drift.
 * @param {any} report
 * @returns {string}
 */
function adviceFor(report) {
  const code = report.exit_code;
  if (code === 0) return cleanAdvice(report);
  // 665. A 2 whose only reason is a `sourced` merge that looked nothing up:
  // the run finished, so "part of the check did not complete" would be false.
  // Served as a boolean, `recall_only`'s rule: the page holds no fidelity
  // vocabulary and does not work out which level retrieves.
  if (code === 2) {
    return (report.sourcing || {}).inconclusive_not_sourced
      ? t("advice.notsourced")
      : t("advice.inconclusive");
  }
  if (code === 3) return t("advice.record");
  return t("advice.look");
}

/**
 * The merge's own warning that these documents may not belong together (497).
 *
 * Above the review list and below the verdict, because it is not a finding
 * and must not be read as one: a merge of a C# file and a Java file can be
 * flawless by every check here and still be a thing nobody wanted. The
 * operator's words were "we do not need to fail but we should provide a
 * friendly hint", and the placement is what keeps that distinction visible --
 * a clean banner, then the reason the clean banner may not be the answer.
 *
 * Quoted and attributed. The sentence is the model's, nothing checks it, and
 * a reader deciding what to do with it needs both facts.
 * @param {any} report
 */
function renderMismatch(report) {
  const said = String(report.mismatch || "").trim();
  const banner = el("mismatch");
  banner.hidden = !said;
  if (!said) return;
  setState(banner, "warn");
  setText(el("mismatch-text"), t("mismatch.text", { said: said }));
}

/**
 * Everything that needs a decision, in one list, above the sections (488).
 *
 * The operator's report: a long document produces dozens of green rows and
 * one amber chip, and finding the chip is work this page should not be
 * making anybody do. Sorting helps inside one table; it cannot help across
 * six, and the item that matters is as likely to be in Structure as in
 * Conflicts.
 *
 * **It repeats rather than moves.** Every entry here is also rendered in its
 * own section below, because this list is an index and an index that removed
 * its targets would make the sections lie about what they contain. The count
 * on the chip is the number of things to look at, not a seventh finding.
 *
 * Hidden outright when there is nothing in it: a standing empty panel headed
 * "what needs your attention" trains a reader to stop looking at it, and the
 * banner already says the run was clean.
 *
 * **This is not the report's `Review queue`, and the two are deliberately
 * different things** (545). That section is 2.5's list -- claims the merge
 * declared dropped and the forward pass confirms are gone -- with a membership
 * rule and a budget line of its own; this is an index over sections that
 * already exist, and it has no counterpart in the Markdown report because a
 * Markdown report is read top to bottom with every section present. The page
 * is a set of collapsible panels where the one item that matters can be behind
 * a closed one, which is the whole of 488. The report's queue has its
 * counterpart here in `renderOmitted`, wider by construction: it lists every
 * `dropped` declaration rather than only the confirmed ones.
 * @param {any} report
 */
function renderReview(report) {
  const items = [];

  // Verdict findings first: a claim the sources contradict or the merge
  // invented is the most expensive kind of wrong to ship.
  for (const verdict of report.findings || []) {
    items.push(reviewItem(
      statusWord(verdict),
      claimTextOf(report, verdict.claim_id) || String(verdict.claim_id || ""),
      OMITTED_FINDINGS.indexOf(verdict.finding) >= 0
        ? "results.omitted" : "results.conflicts",
      verdictId(verdict)));
  }

  // Then the mechanical ones, from all three blocks -- the same collector the
  // sections use, so nothing counted in the checks table can be missing here.
  for (const finding of structuralFindings(report)) {
    items.push(reviewItem(
      t("kind." + finding.kind), String(finding.detail || finding.segment || ""),
      ATTRIBUTION_KINDS.indexOf(finding.kind) >= 0 ? "results.attributions"
        : NUMBER_KINDS.indexOf(finding.kind) >= 0 ? "results.numbers"
        : OMITTED_KINDS.indexOf(finding.kind) >= 0
          ? "results.omitted" : "results.conflicts",
      structuralFindingId(finding)));
  }

  // Declared additions are not defects and are listed last, without a tone:
  // at `open` they are the one thing the tool stopped checking, so they need
  // a reader even though nothing went wrong.
  const additions = report.additions || [];
  for (let i = 0; i < additions.length; i += 1) {
    const record = additions[i] || {};
    // The label follows the record's own basis. It read "stated without a
    // source" for every addition, which went false the moment one could carry
    // a citation (537) -- and false in the direction that matters, because a
    // reader scanning this list would take a cited record for an uncited one
    // and stop weighing it.
    const basis = String(record.basis || "");
    items.push(reviewItem(
      basis === "citation" ? t("review.addition.cited")
                           : t("review.addition"),
      String(record.statement || ""), "results.additions",
      additionId(i, record)));
  }

  const section = el("review-section");
  section.hidden = items.length === 0;
  if (!items.length) return;
  chipFor(el("review-chip"), "findings", items.length);
  const note = document.createElement("p");
  note.className = "hint";
  setText(note, t("review.note"));
  fill(el("review"), [note, listOf(items)]);
}

/**
 * One row of the review list: what it is, what it is about, the one-line
 * decision it calls for, and where it lives (488, 717). The whole row is a
 * button -- clicking it, or pressing Enter or Space on it, switches to the
 * section's own tab if another one is showing, scrolls the matching card
 * into view, moves focus onto it and flashes it briefly, through
 * `jumpToFinding`. Kept apart from `findingItem`'s template (which every
 * other card, including the one this jumps to, still uses unchanged)
 * because a `<button>`'s content model has no room for this one's `<dl>`,
 * and the "In section" row reads better beside the button than inside it.
 * @param {string} label
 * @param {string} detail
 * @param {string} sectionKey a `results.*` locale key naming the section
 * @param {string} jumpId the target card's own `findingId`
 * @returns {HTMLElement}
 */
function reviewItem(label, detail, sectionKey, jumpId) {
  const item = clone("tpl-review-item");
  setText(find(item, "finding-label"), label);
  setText(find(item, "finding-text"), shorten(detail, 200));
  setText(find(item, "review-decide"),
         t(sectionKey.replace("results.", "review.decide.")));
  const list = find(item, "finding-detail");
  const term = document.createElement("dt");
  setText(term, t("review.where"));
  const definition = document.createElement("dd");
  setText(definition, t(sectionKey));
  list.appendChild(term);
  list.appendChild(definition);
  const tab = sectionKey.replace("results.", "");
  find(item, "review-jump").addEventListener(
    "click", () => jumpToFinding(jumpId, tab));
  return item;
}

/**
 * Bring one finding into view from the review list (488, 717).
 *
 * Switches to its section's finding-tab first, only when another one is
 * current -- a section a renderer hid takes its tab with it (`syncFindingTabs`),
 * so a hidden target is left alone rather than switched to a tab with nothing
 * behind it. Opens the card's own stacked comparison, when it has one, the
 * same panel Escape closes elsewhere on this page (`wireLayout`'s keydown
 * handler) -- collapsed by default, and a reader jumping here from "What
 * needs your attention" has not clicked to open anything themselves. Focus
 * moves onto the card itself, not just its section, so a screen reader
 * announces landing on the finding and not merely "tab changed"; the visible
 * flash is for the sighted reader whose eye needs the same answer the
 * keyboard just got. The class is removed and re-added on a second jump to
 * the same card (a forced reflow between the two) so pressing the review row
 * twice restarts the flash instead of silently doing nothing the second time.
 * @param {string} id the target card's `findingId`
 * @param {string} tab the finding-tabs suffix its section answers to
 */
function jumpToFinding(id, tab) {
  const finTab = document.getElementById("finding-tab-" + tab);
  if (finTab && !finTab.hidden && finTab.getAttribute("aria-selected") !== "true") {
    selectTab(el("finding-tabs"), finTab);
    layout.finding = tab;
  }
  const target = document.getElementById(id);
  if (!target) return;
  const stack = target.querySelector('[data-cc="stack-panel"]');
  if (stack instanceof HTMLDetailsElement) stack.open = true;
  target.scrollIntoView({ block: "center", behavior: "smooth" });
  target.classList.remove("just-found");
  void target.offsetWidth;
  target.classList.add("just-found");
  window.setTimeout(() => target.classList.remove("just-found"), 2000);
  if (typeof target.focus === "function") target.focus({ preventScroll: true });
}

/**
 * The three finding families' own `findingId` inputs, kept beside
 * `jumpToFinding` rather than beside `findingId` itself so a caller sees the
 * jump and the id it jumps to in one place.
 * @param {any} verdict @returns {string}
 */
function verdictId(verdict) {
  return findingId("verdict", String(verdict.claim_id) + "|" + String(verdict.direction));
}

/** @param {any} finding @returns {string} */
function structuralFindingId(finding) {
  return findingId("structural", [finding.kind, finding.segment, finding.document, finding.detail]
    .map((value) => String(value || "")).join("|"));
}

/** @param {number} index @param {any} record @returns {string} */
function additionId(index, record) {
  return findingId("addition", String(index) + "|" + String((record || {}).statement || ""));
}

/**
 * A merged- or source-claim's text by id, for the review list.
 * @param {any} report
 * @param {string} claimId
 * @returns {string}
 */
function claimTextOf(report, claimId) {
  for (const claim of report.claims || []) {
    if (claim.id === claimId) return String(claim.text || "");
  }
  return "";
}

/**
 * Conflicts: what the merge chose between, and what a check found altered,
 * invented, repeated or contradicted.
 * @param {any} report
 * @returns {Tile} the section chip's figure, for the tiles
 */
function renderConflicts(report) {
  const items = [];
  const decisions = report.decisions || {};
  const structural = report.structural || {};

  for (const record of decisions.records || []) {
    // A candidate is an object, not a string: `merge._CANDIDATE_ITEM` gives it
    // `text` and `document`, and `parsing.CANDIDATE_FIELDS` requires both.
    // `String(one)` on it renders `[object Object]`, which is what shipped --
    // every conflict in the operator's first real run read "Candidates:
    // [object Object] [object Object]", so the section that exists to show
    // what the merge chose between showed nothing at all.
    //
    // Nothing caught it because nothing else renders them: `html_report.py`
    // has no candidate rendering, so this page is the only reader of the
    // shape and it was reading it wrong. A string is still accepted, because
    // a record that arrived without the wrapper is worth showing badly rather
    // than not at all.
    const candidates = (record.candidates || []).map((/** @type {any} */ one) => {
      const text = one && typeof one === "object" ? String(one.text || "") : String(one);
      const from = one && typeof one === "object" ? String(one.document || "") : "";
      return shorten(from ? from + ": " + text : text, 220);
    });
    const text = record.resolved
      ? String(record.reason || "")
      : t("detail.unresolved") + " " + String(record.reason || "");
    items.push(findingItem(
      String(record.slot || ""), text,
      [[t("detail.candidates"), candidates.join("\n\n"), true],
       [t("detail.chosen"), String(record.chosen || ""), true]],
      record.resolved ? "" : "warn"));
  }

  for (const verdict of report.findings || []) {
    if (CONFLICT_FINDINGS.indexOf(verdict.finding) < 0) continue;
    items.push(verdictItem(report, verdict));
  }

  for (const finding of structuralFindings(report)) {
    if (CONFLICT_KINDS.indexOf(finding.kind) < 0) continue;
    items.push(structuralItem(finding));
  }

  const ran = Boolean(decisions.ran) || Boolean(structural.ran);
  const state = sectionState(el("conflicts-chip"), ran, items.length);
  openIf("conflicts-section", items.length > 0 || !ran);
  const conflictShown = structuralFindings(report).filter(
    (/** @type {any} */ f) => CONFLICT_KINDS.indexOf(f.kind) >= 0);
  fill(el("conflicts"), items.length
    ? [...diffLegend(conflictShown), listOf(items)]
    : [emptyNote(ran, "section.none.conflicts")]);
  return tileOf("results.conflicts", state, items.length);
}

/**
 * Statements the merge brought from outside the documents, and what each one
 * excused.
 *
 * Its own section rather than rows under Conflicts, for the reason the
 * markdown report gives: a declared addition is not a defect, and listing it
 * among defects would say that it was. It is also not a finding this tool
 * made -- nothing here was found, it was declared, and the section exists so
 * a reader can do the one thing the tool cannot, which is decide whether each
 * statement is true.
 *
 * Hidden outright when there is nothing to show. Every other section stays up
 * saying "not checked", because a reader needs to know a check did not run.
 * This one is not a check: at a level that permits no additions there is no
 * question left open by its absence, and a permanent empty row headed "added
 * from outside your documents" would suggest there was.
 * @param {any} report
 */
function renderAdditions(report) {
  const records = report.additions || [];
  // Positional, and `report.as_dict` builds it that way on purpose: these are
  // the tool's account of what each declaration bought, kept out of the
  // records themselves because those three fields are the merge's own words.
  const cover = report.additions_cover || [];
  const section = el("additions-section");
  section.hidden = records.length === 0;
  if (!records.length) return;

  const items = [];
  for (let i = 0; i < records.length; i += 1) {
    const record = records[i] || {};
    const covers = (cover[i] || []).join(", ");
    const basis = String(record.basis || "");
    items.push(findingItem(
      shorten(String(record.statement || ""), 220),
      String(record.reason || ""),
      [[t("detail.corrects"), String(record.corrects || "") || t("detail.nothing"), false],
       // What the merge says it went on, and what it named. Both plain text:
       // `setText` is what puts a detail on the page, so a source is never an
       // anchor. A link is an invitation, and an invitation the page drew
       // reads as a destination the page has been to -- which is exactly the
       // impression a fabricated citation needs in order to do damage (537).
       // `t` answers with the key itself when a string is missing, which is
       // this file's convention and the right one here: an unrecognised basis
       // is visible rather than silently rendered as one of the two.
       [t("detail.basis"), basis ? t("basis." + basis) : t("detail.nothing"),
        false],
       // "no source" is rendered as the answer it is, never as a blank. A row
       // that made the empty cell look like an omission would push the next
       // merge into inventing one.
       [t("detail.source"), String(record.source || "") || t("detail.source.none"),
        false],
       // Named rather than counted. One declaration covering a dozen claims
       // and a dozen covering one each produce the same total, and only the
       // second is what this level is for.
       [t("detail.covers"), covers || t("detail.covers.none"), false]],
      "", null, additionId(i, record)));
  }
  chipFor(el("additions-chip"), "ungraded", records.length);
  const note = document.createElement("p");
  note.className = "hint";
  setText(note, t("section.additions.note"));
  // Two facts, in the section that lists the sources rather than in a
  // footnote elsewhere: what this tool did about them, which is nothing and
  // never changes, and what the model did, which is a measurement with three
  // states off `server_tool_use`. `unmeasured` is not `not-searched` (537).
  const sourcing = report.sourcing || {};
  const state = String(sourcing.state || "unmeasured");
  const searched = (Number(sourcing.web_search) || 0)
                 + (Number(sourcing.web_fetch) || 0);
  /** @type {Record<string, string>} */
  const said = {searched: "section.additions.searched",
                "not-searched": "section.additions.notsearched"};
  const toolUse = sourcing.tool_use || {};
  const toolState = String(toolUse.state || "unmeasured");
  // What the level that promised retrieval achieved, or "" below it (571).
  const outcome = String(sourcing.retrieval || "");
  const about = document.createElement("p");
  about.className = "hint";
  // **The blind counter keeps its number and loses its conclusion** once the
  // turn counter has reported (548). `not-searched` ends "so every source here
  // is recalled rather than looked up", and beside a turn count that saw tool
  // use that half is simply false: `server_tool_use` counts a vendor's
  // server-side tools and cannot see a command backend's local one.
  //
  // **And it loses it at the retrieving level whether or not turns reported**
  // (571). A run there is a command run by construction -- the level refuses
  // HTTP -- so the counter is blind on every one of them, and over an
  // unmeasured turn count its zero was the only instrument on the page: it
  // said "every source here is recalled" about a run nobody measured, which
  // is `unmeasured` read as none. `report.sourcing_sentence` makes the same
  // swap on the three written surfaces.
  const blind = toolState === "unmeasured" && outcome && state === "not-searched";
  const firstSaid = blind
    ? t("section.additions.blindcounter")
    : toolState === "unmeasured"
      ? t(said[state] || "section.additions.unmeasured", { n: searched })
      : (state === "searched"
          ? t("section.additions.searched", { n: searched })
          : state === "not-searched"
            ? t("section.additions.blindcounter")
            : "");
  setText(about, (t("section.additions.sourcing") + " " + firstSaid).trim());
  /** @type {HTMLElement[]} */
  const blocks = [note, about];
  // The turn counter's own word for an absence, where a run at the retrieving
  // level has nothing else to say about it: without this the section would end
  // on the web-request counter's sentence and leave the reader to take its
  // silence for an answer.
  if (toolState === "unmeasured" && outcome) {
    const silent = document.createElement("p");
    silent.className = "hint";
    setText(silent, t("toolstate.unmeasured"));
    blocks.push(silent);
  }
  // The second instrument, before the first rather than instead of it (548).
  // `state` above is read off `server_tool_use`, which counts a vendor's
  // server-side web tools and is blind to a command backend's own -- measured:
  // a call that demonstrably fetched reported zero. `tool_use` counts turns,
  // which is the round trip a tool call costs, and does see it. Both are
  // printed where they both reported, because a reader meeting a zero needs to
  // know which instrument wrote it.
  if (toolState !== "unmeasured") {
    const turns = document.createElement("p");
    turns.className = "hint";
    // `state` is read off the calls that reported, so one silent call beside
    // two short ones is `no-tool-use` -- whose sentence concludes "retrieved
    // nothing" over a call that may be the one that fetched (568). The
    // counter's own `retrieval` is `unmeasured` there, and that is what is
    // said (571).
    setText(turns, t(toolSentenceKey(toolUse),
                     { n: Number(toolUse.calls_with_tool_use) || 0,
                       turns: Number(toolUse.turns) || 0 }));
    blocks.push(turns);
    // **A run at a level that expects retrieval and retrieved nothing is the
    // interesting case.** The level asked the model to go and look; it did
    // not, so every source under this heading is a recollection and the reader
    // is told so here rather than left to infer it from a turn count.
    //
    // Served as a boolean and not worked out from the level's name. The page
    // holds no fidelity vocabulary -- it renders the ladder out of `/config`
    // and does not know the word `open`, let alone which level expects a
    // fetch -- and this is the one branch that would have taught it some. It
    // is the same rule `detects_invention` follows one picker over.
    if (sourcing.recall_only) {
      const recall = document.createElement("p");
      recall.className = "hint warn";
      setText(recall, t("section.additions.sourcednothing"));
      blocks.push(recall);
    }
  }
  // A declared correction is still a finding and still moves the exit code
  // (490's rule, applied). Said where the reader meets the row that caused
  // it, so a clean-looking declaration beside a red banner is explained.
  const corrections = records.filter(
    (/** @type {any} */ row) => String((row || {}).corrects || "").trim()).length;
  if (corrections) {
    const why = document.createElement("p");
    why.className = "hint";
    setText(why, t("section.additions.corrections", { n: corrections }));
    blocks.push(why);
  }
  blocks.push(listOf(items));
  fill(el("additions"), blocks);
}

/**
 * Which `toolstate.*` sentence the turn counter's reading earns (571).
 *
 * `state` alone, except where some calls reported and some did not: then
 * `state` is `no-tool-use` off the ones that reported and its sentence says
 * "it retrieved nothing and every source here is recalled", while the counter's
 * own `retrieval` says `unmeasured`. The absence is unproven, so the unmeasured
 * sentence is the true one. `report.sourcing_sentence` swaps it the same way.
 * @param {any} toolUse `sourcing.tool_use` or `provenance.retrieval.tool_use`
 * @returns {string}
 */
function toolSentenceKey(toolUse) {
  const state = String((toolUse || {}).state || "unmeasured");
  if (String((toolUse || {}).retrieval || "") === "unmeasured") {
    return "toolstate.unmeasured";
  }
  return TOOL_STATE_KEYS[state] || "toolstate.unmeasured";
}

/**
 * The turn counter's three readings and their sentences, written out.
 * @type {Record<string, string>}
 */
const TOOL_STATE_KEYS = {
  "tool-use": "toolstate.tool-use",
  "no-tool-use": "toolstate.no-tool-use",
  unmeasured: "toolstate.unmeasured",
};

/**
 * Omitted content: declared drops, and what a check found missing.
 * @param {any} report
 * @returns {Tile} the section chip's figure, for the tiles
 */
function renderOmitted(report) {
  const items = [];
  const structural = report.structural || {};

  for (const declaration of report.declarations || []) {
    if (declaration.disposition !== "dropped") continue;
    items.push(findingItem(
      t("disposition.dropped"),
      String(declaration.reason || declaration.detail || ""),
      [[t("detail.segment"), shorten(String(declaration.segment || ""), 300), true],
       [t("detail.evidence"), declaration.grade
         ? t("declaration.grade", { grade: String(declaration.grade) }) : "", false]],
      "warn"));
  }

  for (const verdict of report.findings || []) {
    if (OMITTED_FINDINGS.indexOf(verdict.finding) < 0) continue;
    items.push(verdictItem(report, verdict));
  }

  for (const finding of structuralFindings(report)) {
    if (OMITTED_KINDS.indexOf(finding.kind) < 0) continue;
    items.push(structuralItem(finding));
  }

  const ran = Boolean(structural.ran) || (report.claims || []).length > 0;
  const state = sectionState(el("omitted-chip"), ran, items.length);
  openIf("omitted-section", items.length > 0 || !ran);
  const omittedShown = structuralFindings(report).filter(
    (/** @type {any} */ f) => OMITTED_KINDS.indexOf(f.kind) >= 0);
  fill(el("omitted"), items.length
    ? [...diffLegend(omittedShown), listOf(items)]
    : [emptyNote(ran, "section.none.omitted")]);
  return tileOf("results.omitted", state, items.length);
}

/**
 * Sentences the merge credited to a source that does not state them (572).
 *
 * The page's half of 569. The engine publishes `attributions: {ran,
 * predicate, findings}` on both commands and moves the exit code to 1 on a
 * firing; `structuralFindings` collects the findings and this is the section
 * that shows them, so a run whose only finding is a misattribution has a
 * section holding the reason and a banner that names it.
 *
 * Hidden when nothing fired, which is the report's rule for its own
 * **Attributions** section: a standing empty panel about a mistake the merge
 * did not make is a heading a reader learns to skip. Whether the check ran is
 * still said on every run, in the checks table, so "not checked" and "checked,
 * clean" stay apart where they always have been.
 * @param {any} report
 */
function renderAttributions(report) {
  const found = structuralFindings(report).filter(
    (/** @type {any} */ f) => ATTRIBUTION_KINDS.indexOf(f.kind) >= 0);
  const section = el("attributions-section");
  section.hidden = found.length === 0;
  if (!found.length) return;
  chipFor(el("attributions-chip"), "findings", found.length);
  openIf("attributions-section", true);
  const note = document.createElement("p");
  note.className = "hint";
  setText(note, t("section.attributions.note"));
  fill(el("attributions"), [note, ...diffLegend(found),
    listOf(found.map((/** @type {any} */ finding) => attributionItem(report, finding)))]);
}

/**
 * One misattribution as a row: issue, source, merge, why (552, 561).
 *
 * `structuralItem`'s layout with one field renamed, and the rename is the
 * point. `document` on this finding is the source the merge *named*, which is
 * the one that does not carry the sentence -- so it is labelled as credited,
 * by the name the submitter gave it, and never as "Source", which beside the
 * stacked "In the source" line would read as where that line came from. That
 * line is the other document's, and `detail` -- the why -- names both.
 * @param {any} report
 * @param {any} finding
 * @returns {HTMLElement}
 */
function attributionItem(report, finding) {
  const names = report.documents || {};
  const credited = String(names[finding.document] || finding.document || "");
  /** @type {Array<[string, string, boolean]>} */
  const rows = [
    [t("detail.segment"), shorten(String(finding.segment || ""), 300), true],
    [t("detail.credited"), credited, false],
  ];
  const shown = String(finding.difference || "");
  if (shown) rows.push([t("detail.changed"), shown, true]);
  return findingItem(t("kind." + finding.kind), String(finding.detail || ""),
                     rows, "bad", stackPanel(finding), structuralFindingId(finding));
}

/**
 * How each document writes its decimals, and the numerals that break it (601).
 *
 * The page's half of `numerals.check`. Hidden when nothing was flagged, the
 * report's rule for its own **Number format** section; whether the check ran
 * is a row in the checks table on every run. Each document's decision comes
 * first, because every row below is "written in the other convention" or
 * "readable two ways" *relative to it*, and a reader who cannot see what was
 * decided and from what cannot weigh the row. A fault is `bad`; a warning is
 * `warn`, and the engine's `faults` list says which is which.
 * @param {any} report
 */
function renderNumbers(report) {
  const block = report.number_format || {};
  const found = structuralFindings(report).filter(
    (/** @type {any} */ f) => NUMBER_KINDS.indexOf(f.kind) >= 0);
  const section = el("numbers-section");
  section.hidden = found.length === 0;
  if (!found.length) return;
  chipFor(el("numbers-chip"), "findings", found.length);
  openIf("numbers-section", true);
  const faults = /** @type {string[]} */ (block.faults || []);
  const names = report.documents || {};
  const note = document.createElement("p");
  note.className = "hint";
  setText(note, t("section.numbers.note"));
  const decided = (block.documents || []).map((/** @type {any} */ d) => {
    const line = document.createElement("li");
    setText(line, t("numbers.convention", {
      document: String(names[d.document] || d.document || ""),
      convention: t(d.convention === "decimal point" ? "numbers.convention.point"
        : d.convention === "decimal comma" ? "numbers.convention.comma"
          : "numbers.convention.none"),
      decided: t(DECIDED_BY[String(d.decided_by || "")] || "numbers.decided.none"),
      point: ((d.votes || {}).decimal_point || []).join(", ") || "-",
      comma: ((d.votes || {}).decimal_comma || []).join(", ") || "-",
    }));
    return line;
  });
  const conventions = document.createElement("ul");
  conventions.className = "hint";
  for (const line of decided) conventions.appendChild(line);
  const ordered = found.filter((/** @type {any} */ f) => faults.indexOf(f.kind) >= 0)
    .concat(found.filter((/** @type {any} */ f) => faults.indexOf(f.kind) < 0));
  fill(el("numbers"), [note, conventions, ...diffLegend(found),
    listOf(ordered.map((/** @type {any} */ finding) => {
      /** @type {Array<[string, string, boolean]>} */
      const rows = [
        [t("detail.segment"), shorten(String(finding.segment || ""), 300), true],
        [t("detail.document"),
         String(names[finding.document] || finding.document || ""), false],
      ];
      return findingItem(t("kind." + finding.kind), String(finding.detail || ""),
                         rows, faults.indexOf(finding.kind) >= 0 ? "bad" : "warn",
                         stackPanel(finding), structuralFindingId(finding));
    }))]);
}

/**
 * The word diff's notation, once above a list that uses it (552).
 *
 * `[-...-]` and `{+...+}` carry the difference without colour, which is what
 * lets one rendering serve the page, the Markdown report and a terminal. A
 * reader meeting the markers for the first time needs one clause to read them
 * by -- and a legend above a list where nothing uses them is a line that
 * teaches a reader to skip the hints, so it is conditional.
 * @param {Array<any>} findings
 * @returns {HTMLElement[]}
 */
function diffLegend(findings) {
  if (!findings.some((/** @type {any} */ f) => String((f || {}).difference || ""))) {
    return [];
  }
  const note = document.createElement("p");
  note.className = "hint";
  setText(note, t("section.difference.legend"));
  return [note];
}

/**
 * @param {HTMLElement[]} items
 * @returns {HTMLElement}
 */
function listOf(items) {
  const list = document.createElement("ul");
  list.className = "findings";
  fill(list, items);
  return list;
}

/**
 * One verdict as a bulleted item, with the claim it is about.
 * @param {any} report
 * @param {any} verdict
 * @returns {HTMLElement}
 */
function verdictItem(report, verdict) {
  const claim = (report.claims || []).find(
    (/** @type {any} */ one) => one.id === verdict.claim_id);
  const label = statusWord(verdict);
  return findingItem(
    label,
    claim ? shorten(String(claim.text), 300) : String(verdict.claim_id || ""),
    // `detail.against` sits directly above `detail.reason`, because the reason
    // is the model's own prose and that prose says "the reference" -- which is
    // the merged document on a forward verdict and the sources on a reverse
    // one. The operator read two forward findings and asked, twice, which
    // document was meant. Not the same field as `detail.source`, which is
    // where the *claim* came from, nor as the evidence's file, which is where
    // the model *said* it quoted from.
    [[t("detail.source"), claim ? String(claim.source || "") : "", false],
     [t("detail.evidence"), shorten(String(verdict.evidence || ""), 300), true],
     [t("detail.against"), judgedAgainst(report, verdict.direction), false],
     [t("detail.reason"), String(verdict.rationale || ""), false]],
    verdict.finding === "none" ? "" : "bad", null, verdictId(verdict));
}

/**
 * Which document a verdict in this direction was read against, by name.
 *
 * `report.judged_against` is the same answer on the two written reports, and
 * the rule is the engine's rather than this page's: the forward pass reads the
 * merge, the reverse pass reads every source. `report.documents` maps the
 * canonical names the model saw to the labels the submitter gave, and it is
 * the labels a reader recognises.
 * @param {any} report
 * @param {string} direction
 * @returns {string}
 */
function judgedAgainst(report, direction) {
  if (direction !== "merged_to_sources") return MERGED_DOCUMENT;
  const names = Object.keys(report.documents || {})
    .filter((name) => name !== MERGED_DOCUMENT)
    .map((name) => String((report.documents || {})[name] || name));
  if (!names.length) return t("detail.against.sources");
  if (names.length === 1) return names[0];
  return names.slice(0, -1).join(", ") + " " + t("word.and") + " "
    + names[names.length - 1];
}

/**
 * One structural finding as a bulleted item.
 * @param {any} finding
 * @returns {HTMLElement}
 */
function structuralItem(finding) {
  // **Issue, source, merge, why -- in one row** (552). The operator's report:
  // *"the user does not need to refer to sections or the documents but gets
  // the full understanding of the claims directly in one row"*. `detail` is
  // the why and was all a row carried, so a reader met "this is reworded" and
  // had to go and find both texts to see how.
  //
  // The difference is served rather than computed here, so the page, the
  // Markdown report and the HTML download show one string. Where it is empty
  // -- two texts too far apart to diff usefully, or no second side at all --
  // the two texts are shown instead, which is what the engine's own renderer
  // does. The notation is `[-was-] {+is+}`, which carries itself without
  // colour; the page explains it once, above the list.
  /** @type {Array<[string, string, boolean]>} */
  const rows = [
    [t("detail.segment"), shorten(String(finding.segment || ""), 300), true],
    [t("detail.source"), String(finding.document || ""), false],
  ];
  // The compact form stays on the row (552) and the stack goes below it (561).
  // Both, because they answer two questions: the one-liner says *what* changed
  // at a glance and earns its place in a list of rows, and the stack says what
  // the two texts are -- the question a reader asks next and used to have to
  // leave the row to answer.
  const shown = String(finding.difference || "");
  if (shown) {
    rows.push([t("detail.changed"), shown, true]);
  } else {
    // Only where the stack below will not carry it anyway: printing one text
    // twice on one row is how a reader learns the row repeats itself. The
    // stack takes over as soon as there are two sides to stack.
    if (finding.source_text && !finding.merge_text) {
      rows.push([t("detail.insource"), String(finding.source_text), true]);
    }
    if (finding.merge_text && !finding.source_text) {
      rows.push([t("detail.inmerge"), String(finding.merge_text), true]);
    }
  }
  return findingItem(t("kind." + finding.kind), String(finding.detail || ""),
                     rows, "bad", stackPanel(finding), structuralFindingId(finding));
}

/**
 * What one verdict's finding is called, by the direction it was reached in.
 * @param {any} verdict
 * @returns {string}
 */
function statusWord(verdict) {
  const reverse = verdict.direction === "merged_to_sources";
  const known = reverse ? REVERSE_FINDINGS : FORWARD_FINDINGS;
  const finding = String(verdict.finding);
  if (known.indexOf(finding) < 0) return t("status.notchecked");
  return t((reverse ? "status.reverse." : "status.forward.") + finding);
}

/**
 * Does this claim's verdict ask the reader for anything? (495)
 *
 * `finding: "none"` is a claim that came back clean, and an absent verdict is
 * one nothing was said about -- which is *not* clean and is not a finding
 * either. It ranks between the two: a reader sorting by status wants the
 * findings first and the unchecked rows next, because an unchecked claim is
 * the one place a clean-looking table can be hiding something.
 * @param {any} verdict
 * @returns {number}
 */
function claimNeedsReview(verdict) {
  if (!verdict) return 1;
  return verdict.finding && verdict.finding !== "none" ? 2 : 0;
}

/**
 * The claims table: `claims[]` joined to `verdicts[]`, one row per claim.
 * @param {any} report
 * @returns {Tile} the section chip's figure, for the tiles
 */
function renderClaims(report) {
  const claims = report.claims || [];
  const verdicts = report.verdicts || [];
  /** @type {Record<string, any>} */
  const byClaim = {};
  for (const verdict of verdicts) {
    if (!byClaim[verdict.claim_id]) byClaim[verdict.claim_id] = verdict;
  }

  const rows = claims.map((/** @type {any} */ claim, /** @type {number} */ index) => {
    const verdict = byClaim[claim.id];
    const row = clone("tpl-claim-row");
    setText(find(row, "claim-n"), String(index + 1));
    setText(find(row, "claim-text"), String(claim.text || ""));
    const chip = find(row, "claim-status");
    if (!verdict) {
      setState(chip, "");
      setText(chip, t("status.notchecked"));
    } else {
      const word = statusWord(verdict);
      setState(chip, verdict.finding === "none" ? "ok" : "bad");
      setText(chip, word);
    }
    const note = verdict && verdict.rationale
      ? shorten(String(verdict.rationale), 160)
      : t(claim.source === "merged.md" ? "claims.reverse" : "claims.forward",
          { source: String(claim.source || "") });
    setText(find(row, "claim-note"), note);
    return row;
  });

  // Sortable by status, because on a long document this table is where the
  // one item that matters hides (495). 140 rows on the operator's `unrelated`
  // run, all but a handful green.
  //
  // Two states and not three: reading order, and everything that needs a
  // decision first. A third state sorting the *clean* rows to the top would
  // be a control whose only use is to hide the findings, and the reading
  // order is already what the reader gets without touching it.
  const ranked = rows.map((/** @type {HTMLElement} */ row,
                           /** @type {number} */ i) => ({
    row, i, needs: claimNeedsReview(byClaim[(claims[i] || {}).id]),
  }));
  const head = el("claims-sort-head");
  /** @param {boolean} byStatus */
  const paint = (byStatus) => {
    const order = byStatus
      ? ranked.slice().sort((/** @type {any} */ a, /** @type {any} */ b) =>
          (b.needs - a.needs) || (a.i - b.i))
      : ranked;
    // Renumbered after sorting: the `#` column is the reader's position in
    // what they are looking at. Leaving the original numbers would make a
    // sorted table read as a shuffled one.
    order.forEach((/** @type {any} */ entry, /** @type {number} */ n) =>
      setText(find(entry.row, "claim-n"), String(n + 1)));
    fill(el("claim-rows"), order.map((/** @type {any} */ entry) => entry.row));
    head.setAttribute("aria-sort", byStatus ? "descending" : "none");
  };
  paint(false);
  const control = el("claims-sort");
  control.onclick = () => paint(head.getAttribute("aria-sort") === "none");

  const findings = (report.findings || []).length;
  const state = sectionState(el("claims-chip"), claims.length > 0, findings);
  openIf("claims-section", findings > 0);
  setText(el("claims-empty"), claims.length ? "" : t("claims.none"));

  const filter = input("claim-filter");
  filter.oninput = () => {
    const needle = filter.value.trim().toLowerCase();
    let shown = 0;
    for (const row of rows) {
      const hit = !needle || String(row.textContent || "").toLowerCase().indexOf(needle) >= 0;
      row.classList.toggle("hidden", !hit);
      if (hit) shown += 1;
    }
    setText(el("claims-empty"), needle
      ? t("claims.hidden", { n: shown, total: rows.length })
      : (rows.length ? "" : t("claims.none")));
  };
  return tileOf("results.claims", state, findings);
}

/**
 * What the run cost, or why there is no figure (488).
 *
 * Never a bare number and never `$0.00`. The figure is arithmetic over a
 * table of rates somebody read off a pricing page on a stated date, so the
 * sentence says `estimate`, says when the rates were read, and says plainly
 * when it is a floor rather than a total. The four non-priced states get a
 * sentence each rather than a dash, because a dash reads as a rendering
 * failure and these are answers.
 * @param {any} block `provenance.cost`
 * @returns {string}
 */
function costSentence(block) {
  const state = block.state;
  if (state === "none") return t("cost.none");
  if (state === "unmeasured") {
    return t("cost.unmeasured", { n: block.unmeasured_calls || 0 });
  }
  if (state === "unpriced") {
    return t("cost.unpriced", {
      models: (block.unpriced_models || []).join(", ") || t("cost.thisendpoint"),
    });
  }
  if (typeof block.usd !== "number") return "";
  const parts = [t("cost.estimate", { usd: block.usd.toFixed(2) })];
  if (state === "partial") {
    parts.push(t("cost.floor", {
      unpriced: block.unpriced_calls || 0,
      unmeasured: block.unmeasured_calls || 0,
    }));
  }
  if (block.rates_read_on) {
    parts.push(t("cost.read_on", { date: block.rates_read_on }));
  }
  return parts.join(" ");
}

/**
 * Whether this run's fidelity level ever hands the merge the `additions`
 * field at all (716).
 *
 * Read from `/config`'s own `adds` flag (`merge.ADDS`, served per level)
 * rather than from the level's name, the rule every picker on this page
 * follows. `report.additions` is empty both when a level never asks for it
 * and when `open`/`sourced` asked and the merge declared none -- the report
 * itself carries nothing to tell those apart, so this is the one place that
 * does. A level this page cannot find (config not yet loaded, or a value
 * older than the running server) answers `true`, the same as before this
 * existed: a check the page cannot place is a gap to report, not one to
 * hide.
 * @param {any} report
 * @returns {boolean}
 */
function addsAtThisLevel(report) {
  const fidelity = String(((report.provenance || {}).merge_policy || {}).fidelity || "");
  const levels = ((store.config || {}).fidelity || {}).levels || [];
  const level = levels.find((/** @type {any} */ entry) => entry.value === fidelity);
  return level ? Boolean(level.adds) : true;
}

/**
 * Every check the report accounts for, each saying whether it ran.
 * @param {any} report
 * @returns {Tile} the section chip's figure, for the tiles
 */
function renderChecks(report) {
  const structural = report.structural || {};
  const decisions = report.decisions || {};
  const leaks = report.prompt_leaks || {};
  const restated = report.restated_claims || {};
  const attributions = report.attributions || {};
  const numbers = report.number_format || {};
  const loss = report.declared_loss || {};
  const title = report.title || {};
  const order = report.order || {};
  const coverage = report.coverage || {};
  const addsHere = addsAtThisLevel(report);

  /** @type {Array<[string, string, number, string]>} name, chip state, count, note */
  const rows = [
    ["check.structural", structural.ran ? "clean" : "notchecked",
     (structural.findings || []).length,
     t("check.structural.note", {
       segments: figure(structural.segments) || "0",
       checks: figure(structural.checks) || "0",
     })],
    ["check.decisions", decisions.ran ? "ungraded" : "notchecked", 0,
     t("check.decisions.note", { n: (decisions.records || []).length })],
    // `notapplicable` where the level never hands the merge the field at
    // all (716) -- most runs, and not a gap in the answer. Where it is
    // applicable, `notchecked` would mean the report is missing the field
    // entirely, which does not happen at `open`/`sourced` (`additions` is
    // `required` there); `ungraded` otherwise, the same as before: nothing
    // here grades a declared addition, only lists it.
    ["check.additions",
     !addsHere ? "notapplicable" : (report.additions || []).length ? "ungraded" : "notchecked",
     0,
     addsHere
       ? t("check.additions.note", { n: (report.additions || []).length })
       : t("check.additions.notapplicable")],
    ["check.leaks", leaks.ran ? "clean" : "notchecked", (leaks.findings || []).length,
     t("check.leaks.note", { n: (leaks.markers || []).length })],
    ["check.restated", restated.ran ? "clean" : "notchecked",
     (restated.findings || []).length,
     t("check.restated.note", {
       claims: figure(restated.claims) || "0",
       source: figure(restated.source_claims) || "0",
     })],
    // Whether the attribution check ran, on every run (572). Its section is
    // hidden when clean, so this row is where "checked, clean" and "not
    // checked" are told apart for it.
    ["check.attributions", attributions.ran ? "clean" : "notchecked",
     (attributions.findings || []).length, t("check.attributions.note")],
    // The number format (601), on every run for the attribution row's reason:
    // its section is hidden when nothing was flagged.
    ["check.numbers", numbers.ran ? "clean" : "notchecked",
     (numbers.findings || []).length, t("check.numbers.note")],
    // What the merge actually did, beside what was asked of it (488). The
    // row used to give the two counts and the ceiling and leave the division
    // to the reader, so a run at 0.4% and a run at 2.9% read identically
    // against a 3% ceiling -- one is nowhere near it and the other is about
    // to fail. `ratio` is null when there are no segments, which is a ratio
    // that does not exist rather than one that is zero.
    ["check.loss", loss.check_disabled ? "notchecked" : "clean",
     loss.over_budget ? 1 : 0,
     loss.check_disabled ? t("check.loss.disabled") : t("check.loss.note", {
       drops: figure(loss.drops) || "0",
       segments: figure(loss.segments) || "0",
       achieved: typeof loss.ratio === "number"
         ? (loss.ratio * 100).toFixed(1) + "%" : t("check.loss.noratio"),
       budget: typeof loss.budget === "number"
         ? (loss.budget * 100).toFixed(1) + "%" : "-",
     })],
    ["check.title", title.policy ? "clean" : "notchecked", 0,
     title.policy
       ? t(title.has_referent ? "check.title.note" : "check.title.noreferent", {
           policy: String(title.policy),
           n: figure(title.sources_with_a_title) || "0",
         })
       : t("check.title.note", { policy: "-", n: "0" })],
    ["check.order", order.attributed ? "measured" : "notchecked", 0,
     order.attributed ? t("check.order.note", {
       runs: figure(order.runs) || "0",
       attributed: figure(order.attributed) || "0",
       shape: orderShape(order),
       present: figure(order.headings_present) || "0",
       total: figure(order.headings_total) || "0",
     }) : t("check.order.nothing")],
    ["check.coverage", (report.claims || []).length ? "clean" : "notchecked",
     coverage.errored || 0,
     t("check.coverage.note", {
       grounded: figure(coverage.grounded) || "0",
       graded: figure(coverage.graded) || "0",
       errored: figure(coverage.errored) || "0",
       ungraded: figure(coverage.ungraded) || "0",
     })],
  ];

  // Anything that is not clean, first (488). A long document produces dozens
  // of rows and one of them matters; the operator's report was that a single
  // amber chip among them is unfindable, and hunting for it is not work this
  // page should be making anybody do.
  //
  // A stable sort over three ranks, so the engine's own check order survives
  // inside each rank and the table does not reshuffle between two runs that
  // found the same things. `findings` first because it is the only rank that
  // asks for a decision; `notchecked` second because a check that did not run
  // is a gap in the answer rather than an answer; everything else keeps its
  // place.
  /** @type {Record<string, number>} */
  const RANK = { findings: 0, notchecked: 1 };
  const ranked = rows
    .map((/** @type {any} */ row, /** @type {number} */ i) => ({ row, i }))
    .sort((a, b) => {
      const ra = RANK[a.row[1] === "clean" && a.row[2] > 0 ? "findings" : a.row[1]];
      const rb = RANK[b.row[1] === "clean" && b.row[2] > 0 ? "findings" : b.row[1]];
      return (ra === undefined ? 2 : ra) - (rb === undefined ? 2 : rb) || a.i - b.i;
    })
    .map((/** @type {any} */ entry) => entry.row);

  let unchecked = 0;
  const items = ranked.map(([key, state, count, note]) => {
    const item = document.createElement("li");
    const name = document.createElement("span");
    name.className = "check-name";
    setText(name, t(key));
    const chip = document.createElement("span");
    chip.className = "chip";
    const shown = state === "clean" && count > 0 ? "findings" : state;
    chipFor(chip, shown, count);
    if (shown === "notchecked") unchecked += 1;
    const detail = document.createElement("span");
    detail.className = "check-note";
    setText(detail, note);
    item.appendChild(name);
    item.appendChild(chip);
    item.appendChild(detail);
    return item;
  });
  fill(el("checks"), items);
  chipFor(el("checks-chip"), unchecked ? "unchecked" : "clean", unchecked);
  openIf("checks-section", unchecked > 0);
  return tileOf("results.checks", unchecked ? "unchecked" : "clean", unchecked);
}

/**
 * What shape the merge laid its sources out in, in `report.py`'s own words.
 *
 * A measurement and never a finding: whether the shape is right depends on
 * whether the sources had anything to interleave, which this tool does not
 * measure. `conclusive` is asked before the other two because below a certain
 * evidence base the observation is empty rather than weak, and reporting an
 * empty observation as "each source in one unbroken block" is how a correct
 * merge gets called a staple.
 * @param {any} order
 * @returns {string}
 */
function orderShape(order) {
  if (!order.conclusive) return t("order.inconclusive");
  if (order.stapled) return t("order.stapled");
  if (order.interleaved) return t("order.interleaved");
  if (!order.monotone) return t("order.unordered");
  return t("order.inconclusive");
}

/**
 * The provenance block: what ran this, with what, and when.
 * @param {any} report
 */
function renderProvenance(report) {
  const provenance = report.provenance || {};
  const models = provenance.models || {};
  const policy = provenance.merge_policy || {};
  const endpoint = provenance.endpoint || {};
  const structuredOut = provenance.structured_output || {};
  const decoding = provenance.decoding || {};
  const counts = provenance.counts || {};
  const windows = provenance.window || {};
  // What the model was permitted to reach for, and what the turn counter saw
  // (548). Two facts on one row and in this order, because the permission is
  // the half no counter carries: a run that did not look and a run that could
  // not look are the same empty result and opposite conclusions about the
  // citations under it.
  const retrieval = provenance.retrieval || {};
  const permitted = (retrieval.permitted || []).join(", ");
  const toolUse = retrieval.tool_use || {};
  const retrievalSaid = permitted
    ? t("provenance.retrieval.permitted", { tools: permitted }) + " · "
      + t(toolSentenceKey(toolUse),
          { n: Number(toolUse.calls_with_tool_use) || 0,
            turns: Number(toolUse.turns) || 0 })
    : "";

  // Whether the command backend that answered ran isolated: safe mode, and
  // the exact `--tools` grant, per role, off the argv `command_for` really
  // built (611). Unlike `retrieval` above, this is not empty below `sourced`
  // -- 610 put safe mode on at every level -- so it is the only place a
  // `high` report says the operator's own CLAUDE.md, skills, plugins and MCP
  // servers were kept out of the run. Roles that share a state are named
  // together, the `windowSaid` shape above: the roles share one command by
  // construction today, and three identical clauses would read as three
  // different answers. A role's `tools` is `null` when its argv carries no
  // `--tools` at all (unrestricted) and `[]` for `--tools ""` (granted
  // nothing); the two render apart because they are opposite facts.
  const isolation = provenance.isolation || {};
  const isolationGroups = new Map();
  for (const role of Object.keys(isolation).sort()) {
    const info = isolation[role] || {};
    const tools = info.tools == null ? null : [...info.tools].sort();
    const key = JSON.stringify([!!info.safe_mode, tools]);
    if (!isolationGroups.has(key)) {
      isolationGroups.set(key, { roles: [], safeMode: !!info.safe_mode, tools: tools });
    }
    isolationGroups.get(key).roles.push(role);
  }
  const isolationSaid = [...isolationGroups.values()].map((group) => {
    const state = group.safeMode
      ? t("provenance.isolation.safe_mode", { roles: group.roles.join(", ") })
      : t("provenance.isolation.not_isolated", { roles: group.roles.join(", ") });
    const toolState = group.tools === null
      ? ""
      : " · " + (group.tools.length
          ? t("provenance.isolation.tools", { tools: group.tools.join(", ") })
          : t("provenance.isolation.no_tools"));
    return state + toolState;
  }).join("; ");

  // Which box answered, and whether a document left this machine. The pair
  // is the one disclosure the local-first claim actually owes a reader, and
  // it was the field this block was missing that mattered most: a run against
  // a vendor looked exactly like a run against localhost.
  // Said in words, not only by the location. `content_left_this_machine` is
  // the field a reader is actually relying on, and `(hosted)` beside an id is
  // a classification rather than an answer -- it was the whole of what this
  // panel used to say about where a document went, which was nothing.
  // `endpoint.route` is the operator's own name for a command backend, and
  // it is here because the id is a hash of the command by design and
  // `location: command` names a mechanism rather than a route. Without it a
  // reader coming back to this panel a week later could tell that *a*
  // program answered and not *which* -- which is exactly the question "did
  // this go to the subscription or to the metered API" is. Absent on every
  // HTTP run, which is every recorded figure in this project.
  const where = [String(endpoint.id || ""),
                 endpoint.location ? "(" + String(endpoint.location) + ")" : "",
                 endpoint.route ? "— " + String(endpoint.route) : "",
                 endpoint.content_left_this_machine === true
                   ? "— " + t("provenance.left_machine")
                   : endpoint.content_left_this_machine === false
                     ? "— " + t("provenance.stayed_here") : ""]
    .filter(Boolean).join(" ");

  // How each role was paid for, as the server recorded it when it chose the
  // route (570): the words the submit button used before the click, said
  // after it, per role. `endpointKind` rather than the raw word, so a kind a
  // newer server sends reads `route not identified` rather than throwing in
  // `routeLabel`. Roles sharing a route are named together, and named every
  // time, because the question is asked about one role -- "did the checks go
  // to the subscription?" -- and a bare route word leaves the reader to infer
  // which roles it covered. Absent on a run the command line made.
  // In the order the models rows above it use, whatever order the JSON
  // arrived in, so the two read down together and match the report's row.
  const billed = endpoint.billed || {};
  const roles = ["merge", "decompose", "verify"].filter((role) => role in billed)
    .concat(Object.keys(billed).filter(
      (role) => ["merge", "decompose", "verify"].indexOf(role) < 0));
  const byRoute = new Map();
  for (const [role, kind] of roles.map((role) => [role, billed[role]])) {
    const word = routeLabel(endpointKind(kind));
    byRoute.set(word, (byRoute.get(word) || []).concat(role));
  }
  const routeSaid = [...byRoute.entries()]
    .map(([word, roles]) => roles.join(", ") + ": " + word)
    .join("; ");

  // `window` is a map of role to a sentence the engine already composed,
  // which is where the "stated, not measured" wording lives. Roles sharing a
  // sentence are named together rather than repeated, because three identical
  // rows read as three different answers.
  const byWindow = new Map();
  for (const [role, said] of Object.entries(windows)) {
    const key = String(said);
    byWindow.set(key, (byWindow.get(key) || []).concat(role));
  }
  const windowSaid = [...byWindow.entries()]
    .map(([said, roles]) => roles.length === Object.keys(windows).length
      ? said : roles.join(", ") + ": " + said)
    .join(" · ");

  // How hard each role was asked to think, as the run recorded it (567).
  // `decoding.effort` is a role -> level map read back off the argv the
  // backend really ran, so a page that printed a level of its own would be
  // printing the build's default rather than the run's. Per role and never
  // folded, the report's own rule: the merge is asked for more than the two
  // roles that read it back, and "effort medium" would be true of one call.
  // Absent on an HTTP run, where there is no level, and then nothing is said.
  const effort = Object.entries(decoding.effort || {})
    .map(([role, level]) => role + "=" + String(level));
  // A model with one level rather than a scale (688, ruling 11). The roles
  // come off the report; the sentence is this page's own translated string,
  // not the engine's English label -- `decoding.effort_single_level`'s value
  // is data for a CLI or a JSON reader, and this panel is localised.
  const singleLevel = Object.keys(decoding.effort_single_level || {}).sort().join(", ");
  const ignored = (decoding.effort_ignored || []).join(", ");
  const requested = Object.entries(decoding.effort_requested || {})
    .map(([role, level]) => role + "=" + String(level));
  // What the endpoint did when it differed from what was asked: a role whose
  // call asked for thinking off and whose answer carried a reasoning block
  // anyway. The report has always said so; this panel did not, so a run on a
  // model that ignores the switch read here as a run that obeyed it.
  const reasoned = (decoding.reasoned_anyway || []).join(", ");
  const knobs = [
    decoding.temperature ? t("provenance.temperature") + " " + decoding.temperature : "",
    decoding.seed ? t("provenance.seed") + " " + decoding.seed : "",
    decoding.profile ? String(decoding.profile) : "",
    (decoding.thinking || []).length
      ? t("provenance.thinking") + " " + (decoding.thinking || []).join(", ") : "",
    effort.length ? t("provenance.effort") + " " + effort.join(", ") : "",
  ].filter(Boolean).join(", ")
    + (reasoned ? "; " + t("provenance.reasoned_anyway", { roles: reasoned }) : "")
    // A single-level model, beside a graded one where a run used both kinds
    // of backend across roles (688, ruling 11).
    + (singleLevel ? "; " + t("provenance.effort_single_level", { roles: singleLevel }) : "")
    // A level asked for and dropped, beside the ones that went out. It is
    // dropped rather than refused, so this clause is the only place an
    // operator who set one for an HTTP endpoint learns it went nowhere.
    + (ignored ? "; " + t("provenance.effort_ignored", { roles: ignored }) : "")
    // Whose choice a level was, when it was the requester's on the effort
    // slider (613): the report's own clause, in the page's words.
    + (requested.length
      ? "; " + t("provenance.effort_requested", { roles: requested.join(", ") }) : "");

  const called = [
    counts.calls ? t("provenance.calls.live", { n: counts.calls }) : "",
    counts.cache_hits ? t("provenance.calls.cached", { n: counts.cache_hits }) : "",
    counts.replayed ? t("provenance.calls.replayed", { n: counts.replayed }) : "",
  ].filter(Boolean).join(", ");

  /** @type {Array<[string, string]>} */
  const pairs = [
    [t("provenance.run_mode"), String(provenance.run_mode || "")],
    [t("provenance.endpoint"), where],
    [t("provenance.route"), routeSaid],
    [t("provenance.merge_model"), String(models.merge || "")],
    [t("provenance.decompose_model"), String(models.decompose || "")],
    [t("provenance.verify_model"), String(models.verify || "")],
    [t("provenance.fidelity"), String(policy.fidelity || "")],
    [t("provenance.verify_depth"), String(policy.verify_depth || "")],
    [t("provenance.title_policy"), String(policy.title_policy || "")],
    [t("provenance.base"), policy.base
      ? String(policy.base) + (policy.base_chosen
          ? " (" + String(policy.base_chosen) + ")" : "") : ""],
    [t("provenance.structured"), structuredOut.mode
      ? String(structuredOut.mode) + (structuredOut.how
          ? " (" + String(structuredOut.how) + ")" : "")
        + (structuredOut.field_order
          ? ", " + t("provenance.field_order") + " "
            + String(structuredOut.field_order) : "") : ""],
    [t("provenance.decoding"), knobs],
    [t("provenance.window"), windowSaid],
    [t("provenance.calls"), called],
    [t("provenance.tokens"), String(provenance.tokens_described || "")],
    [t("provenance.cost"), costSentence(provenance.cost || {})],
    // Only when non-zero. A row reading "0 errors" on every clean run is a
    // row a reader stops seeing, and then does not see the one that says 3.
    [t("provenance.repairs"), counts.schema_repairs
      ? String(counts.schema_repairs) : ""],
    // Only where something was granted, the rule every conditional row here
    // follows: an always-present row saying "nothing" would be added to the
    // provenance block of every run in the recorded corpus, about a mechanism
    // that did not exist when they were measured.
    [t("provenance.retrieval"), retrievalSaid],
    [t("provenance.isolation"), isolationSaid],
    [t("provenance.errors"), counts.errors ? String(counts.errors) : ""],
    [t("provenance.salvaged"), counts.salvaged ? String(counts.salvaged) : ""],
    [t("provenance.loads"), counts.model_loads ? String(counts.model_loads) : ""],
    [t("provenance.commit"),
     String(provenance.llossless_commit || provenance.claimcheck_commit || "")],
    [t("provenance.duration"), provenance.duration_seconds
      ? duration(Number(provenance.duration_seconds)) : ""],
    [t("provenance.generated"), String(provenance.generated_at || "")],
  ];
  const nodes = [];
  for (const [name, value] of pairs) {
    if (!value) continue;
    const term = document.createElement("dt");
    setText(term, name);
    const definition = document.createElement("dd");
    setText(definition, value);
    nodes.push(term, definition);
  }
  fill(el("provenance"), nodes);
}

/* ------------------------------------------------------------------ */
/* history                                                             */
/* ------------------------------------------------------------------ */

/**
 * Every run this server still holds, as tombstones.
 *
 * Since 660 the list is also where a reader who comes back -- after a few
 * hours, or after the server restarted -- picks their runs up: a queued run
 * says where it stands and can be followed, an interrupted or failed one can
 * be retried, and while anything in it is queued or running the list asks
 * again every few seconds, so a position moves without a reload.
 */
async function refreshHistory() {
  if (store.historyTimer) { window.clearTimeout(store.historyTimer); store.historyTimer = 0; }
  /** @type {any} */
  let payload;
  try { payload = await getJson(ROUTES.runs); } catch (error) { return; }
  const runs = (payload.runs || []).slice().reverse();
  el("history-section").hidden = runs.length === 0;
  syncHistoryTab();
  let live = false;
  const items = runs.map((/** @type {any} */ run) => {
    const state = String(run.state || "");
    const runId = String(run.id || "");
    if (state === "queued" || state === "running") live = true;
    announceLanding(run);
    const item = document.createElement("li");
    const id = document.createElement("span");
    id.className = "id";
    setText(id, runId.slice(0, 8));
    const summary = document.createElement("span");
    setText(summary, t("history.entry", {
      documents: run.documents, state: stateWord(state),
    }) + (state === "queued" && typeof run.queue_position === "number"
      ? ", " + t("history.position", {
        position: run.queue_position, total: run.queue_length,
      }) : "")
      + (run.retry_of ? ", " + t("history.retryof", {
        id: String(run.retry_of).slice(0, 8),
      }) : ""));
    const when = document.createElement("span");
    when.className = "when";
    // The page's language, not the browser's (606) -- same reason as `figure`,
    // and the same fallback: a date is formatted digits too.
    setText(when, run.created_at
      ? new Date(run.created_at * 1000).toLocaleString(locale.tag || "en") : "");
    const open = document.createElement("a");
    open.className = "ghost";
    open.href = route(ROUTES.report, { id: String(run.id) });
    open.target = "_blank";
    open.rel = "noopener";
    setText(open, t("history.open"));
    item.appendChild(id);
    item.appendChild(summary);
    item.appendChild(when);
    // A cancelled run's report is the account of what ran (639), and it
    // opens by saying it was cancelled.
    if (state === "done" || state === "cancelled") item.appendChild(open);
    // Follow a live run; replay the log of one that stopped short, which is
    // where an interrupted run's finished steps are (660).
    const followable = state === "queued" || state === "running";
    if ((followable || state === "interrupted" || state === "failed")
        && store.runId !== runId) {
      const watchIt = document.createElement("button");
      watchIt.type = "button";
      watchIt.className = "ghost";
      setText(watchIt, t(followable ? "history.follow" : "history.log"));
      watchIt.addEventListener("click", () => (followable ? follow(runId) : replay(runId)));
      item.appendChild(watchIt);
    }
    if (run.retryable) {
      const again = document.createElement("button");
      again.type = "button";
      again.className = "ghost";
      setText(again, t("history.retry"));
      again.addEventListener("click", () => void confirmRetry(runId));
      item.appendChild(again);
    }
    if ((state === "interrupted" || state === "failed") && run.error) {
      // What ran before the stop, from what reached the server's disk (660).
      // The server's own sentence, which names steps and never a document.
      const why = document.createElement("span");
      why.className = "note";
      setText(why, state === "interrupted" ? t("status.interrupted")
        : shorten(String(run.error), 240));
      why.title = String(run.error);
      item.appendChild(why);
    }
    return item;
  });
  fill(el("history"), items);
  if (live) store.historyTimer = window.setTimeout(() => void refreshHistory(), 5000);
}

/**
 * A run's state in the reader's language (639); the raw state for one this
 * page has no word for, rather than a blank.
 * @type {Record<string, string>}
 */
const STATE_KEYS = {
  queued: "state.queued",
  running: "state.running",
  done: "state.done",
  failed: "state.failed",
  cancelled: "state.cancelled",
  interrupted: "state.interrupted",
};

/**
 * @param {string} state
 * @returns {string}
 */
function stateWord(state) {
  return STATE_KEYS[state] ? t(STATE_KEYS[state]) : state;
}

/* ------------------------------------------------------------------ */
/* signing in                                                          */
/* ------------------------------------------------------------------ */

/**
 * Whether this server has accounts, and whether one is signed in.
 *
 * The first request the page makes, before the catalogue and before
 * `/health`, because everything else on this server answers 401 until it is
 * answered. A server built with no account store says `tenanted: false` and
 * the page renders exactly as it always has -- no gate, no sign-out, no
 * accounts panel -- which is the single-tenant arrangement rather than a
 * degraded one.
 *
 * A failure here is not an error either. An older server has no such route,
 * so the answer is `null` and the page goes on as though it were untenanted;
 * that is the same treatment `loadProviders` gives a missing credential
 * endpoint, and for the same reason.
 */
async function refreshSession() {
  try {
    store.session = await getJson(ROUTES.session);
  } catch (error) {
    store.session = null;
  }
  renderSession();
}

/** Is there a gate in front of this page right now? @returns {boolean} */
function gated() {
  const session = store.session;
  return Boolean(session && session.tenanted && !session.authenticated);
}

/** Is this server asking for its first account? @returns {boolean} */
function unconfigured() {
  return Boolean(store.session && store.session.setup_required);
}

/** Who is signed in, in the topbar, or nothing at all. */
function renderSession() {
  const session = store.session;
  const signedIn = Boolean(session && session.user);
  el("session-field").hidden = !signedIn;
  // Its own element now, rather than a child of `session-field`. The account
  // group is "who you are, your credentials, the way out", and Credentials is
  // offered on a server with no account store while the other two are not --
  // so the two controls are hidden separately and the group holds all three.
  el("sign-out").hidden = !signedIn;
  const name = signedIn ? String(session.user.username || "") : "";
  const said = signedIn ? t("auth.as", { name: name }) : "";
  // The name is shown in full and alone (673): the sentence around it is the
  // part that changes with the language, so it goes to a screen reader and to
  // `title`, and the row keeps one width in every language (649) without
  // cutting the name off.
  setText(el("session-user"), name);
  setText(el("session-said"), said);
  if (said) el("session-field").setAttribute("title", said);
  else el("session-field").removeAttribute("title");
}

/**
 * The setup token out of the address bar, or "".
 *
 * The server prints it in a URL *fragment*, which no browser sends to any
 * server: it is not in this server's access log, not in an intermediary's,
 * and not in a `Referer` on the way out. The page can still read it, which is
 * the whole point -- so this is where a one-time credential is allowed to
 * come from and a query string is not.
 * @returns {string}
 */
function setupToken() {
  const hash = String(location.hash || "").replace(/^#/, "");
  for (const part of hash.split("&")) {
    const [name, value] = part.split("=");
    if (name === "setup" && value) return decodeURIComponent(value);
  }
  return "";
}

/**
 * Show the gate: the login form, or the one that makes the first account.
 *
 * One form for both. The difference is a heading, a button and one extra
 * field, and two forms would be two places the field names, the autocomplete
 * hints and the error line are written.
 */
function showGate() {
  renderPill("signedout");
  const setting = unconfigured();
  el("workspace").hidden = true;
  el("gate").hidden = false;
  // The credentials sheet is behind the gate too, and a button that opens a
  // dialog every route of which answers 401 is a control that looks broken.
  el("open-settings").hidden = true;
  setText(el("gate-heading"),
    t(setting ? "auth.setup.heading" : "auth.signin.heading"));
  setText(el("gate-hint"), t(setting ? "auth.setup.hint" : "auth.signin.hint"));
  setText(el("gate-submit"),
    t(setting ? "auth.setup.submit" : "auth.signin.submit"));
  el("gate-token-field").hidden = !setting;
  input("gate-password").autocomplete = setting ? "new-password" : "current-password";
  if (setting) input("gate-token").value = setupToken();
  setText(el("gate-status"), "");
  input(setting && !setupToken() ? "gate-token" : "gate-username").focus();
}

/** Take the gate away and show the tool. */
function hideGate() {
  el("gate").hidden = true;
  el("workspace").hidden = false;
  el("open-settings").hidden = false;
}

/**
 * Exchange what was typed for a session, then load the page behind it.
 *
 * The password is read out of the field and the field is cleared in the same
 * step, for the reason the key field is: a credential that stays in a DOM
 * node is a credential in whatever reads the DOM next.
 *
 * **Nothing here stores a session id.** The answer sets an `HttpOnly` cookie
 * and this script cannot read it, which is what that attribute is for; the
 * page's own state is "the server said I am signed in", which is a boolean.
 */
async function signIn() {
  const setting = unconfigured();
  const username = input("gate-username").value.trim();
  const password = input("gate-password").value;
  const token = input("gate-token").value.trim();
  input("gate-password").value = "";
  input("gate-token").value = "";
  setText(el("gate-status"), t("auth.working"));
  /** @type {any} */
  let answer = null;
  try {
    answer = setting
      ? await sendJson("POST", ROUTES.setup,
                       { token: token, username: username, password: password })
      : await sendJson("POST", ROUTES.session,
                       { username: username, password: password });
  } catch (error) {
    setText(el("gate-status"), describe(error));
    return;
  }
  // The fragment goes, so a reload does not re-offer a token that has already
  // been spent and a copied URL does not carry one.
  if (setting && location.hash) history.replaceState(null, "", location.pathname);
  input("gate-username").value = "";
  await refreshSession();
  hideGate();
  await start();
  const note = answer && answer.migrated && answer.migrated.note;
  if (note) say("ok", t("word.ready"), String(note));
}

/** End the session and put the gate back. */
async function signOut() {
  try {
    await sendJson("DELETE", ROUTES.session, undefined);
  } catch (error) {
    // A logout that could not reach the server still ends this page's idea of
    // being signed in; the next request will answer 401 and say so.
  }
  stopWatching();
  store.runId = "";
  // A fresh page for whoever signs in next (674): the documents, the settings
  // and the result on screen were this reader's, and a page that kept them
  // showed them to the next account on this browser.
  window.location.reload();
}

/* ------------------------------------------------------------------ */
/* accounts                                                            */
/* ------------------------------------------------------------------ */

/**
 * The operator's list of accounts, or nothing at all.
 *
 * A 403 is the ordinary answer for everybody who is not the operator, and a
 * 404 used to be the answer from a server with no account store -- caught
 * here and hidden rather than reported, since neither is a failure. But a
 * server that has no account store also has no `/api/v1/accounts` route at
 * all, so that catch was firing after this page had already made a request
 * its own `/api/v1/session` answer said would 404. `session.tenanted` is
 * this page's first request (`refreshSession`, above) and settles the
 * question before this one is made, so an untenanted server now asks
 * nothing and hides the panel without a round trip.
 */
async function loadAccounts() {
  const section = el("accounts-section");
  if (!(store.session && store.session.tenanted)) {
    section.hidden = true;
    return;
  }
  /** @type {any} */
  let payload = null;
  try {
    payload = await getJson(ROUTES.accounts);
  } catch (error) {
    section.hidden = true;
    return;
  }
  section.hidden = false;
  const rows = (payload && payload.accounts) || [];
  fill(el("accounts-list"), rows.map((/** @type {any} */ row) => accountRow(row)));
  setText(el("accounts-note"), rows.length ? "" : t("accounts.none"));
}

/**
 * One account in the operator's list.
 * @param {any} account
 * @returns {HTMLElement}
 */
function accountRow(account) {
  const row = clone("tpl-account");
  const name = String(account.username || "");
  setText(find(row, "account-name"), name);
  const chip = find(row, "account-chip");
  setState(chip, account.operator ? "ok" : "");
  setText(chip, t(account.operator ? "accounts.operator" : "accounts.member"));
  const remove = /** @type {HTMLButtonElement} */ (find(row, "account-remove"));
  setText(remove, t("accounts.remove.one", { name: name }));
  const me = store.session && store.session.user
    && store.session.user.username === name;
  // Your own row has no remove button that works. The server refuses the last
  // operator anyway, but an operator who deleted themselves and was told it
  // worked would be looking at a page that is no longer theirs.
  remove.disabled = Boolean(me);
  remove.addEventListener("click", async () => {
    try {
      await sendJson("DELETE", route(ROUTES.account, { name: name }), undefined);
      setText(el("accounts-note"), t("accounts.removed", { name: name }));
    } catch (error) {
      setText(el("accounts-note"), describe(error));
    }
    await loadAccounts();
  });
  return row;
}

/** Add one, from the two fields under the list. */
async function addAccount() {
  const name = input("new-account-name").value.trim();
  const password = input("new-account-password").value;
  input("new-account-password").value = "";
  try {
    await sendJson("POST", ROUTES.accounts,
                   { username: name, password: password });
    input("new-account-name").value = "";
    setText(el("accounts-note"), t("accounts.added", { name: name }));
  } catch (error) {
    setText(el("accounts-note"), describe(error));
  }
  await loadAccounts();
}

/**
 * Change your own password, which signs you out everywhere including here.
 *
 * That is the server's behaviour and this follows it rather than hiding it: a
 * password changed because it may have leaked has bought nothing while the
 * session opened with the old one is still live, so the page goes back to the
 * gate and says why.
 */
async function changePassword() {
  const who = store.session && store.session.user;
  if (!who) return;
  const current = input("current-password").value;
  const wanted = input("new-password").value;
  input("current-password").value = "";
  input("new-password").value = "";
  try {
    await sendJson("PUT", route(ROUTES.password, { name: String(who.username) }),
                   { current: current, password: wanted });
  } catch (error) {
    setText(el("password-note"), describe(error));
    return;
  }
  setText(el("password-note"), t("password.changed"));
  await refreshSession();
  showGate();
  setText(el("gate-status"), t("password.changed"));
}

/* ------------------------------------------------------------------ */
/* credentials                                                         */
/* ------------------------------------------------------------------ */

/**
 * The credential sheet.
 *
 * No endpoint on this server ever answers with a key and this page never holds
 * one: a saved value is posted and the field is cleared in the same step, and
 * what is rendered afterwards is whether one is set plus the last four
 * characters the server reports. There is no state here that a key could
 * survive in.
 *
 * **It renders the provider rows and nothing else** (561). It used to call
 * `renderCommandTools` as well, which made two owners for one panel: this one
 * rendering from whatever `store.config` still held, and `reloadAfterSettings`
 * rendering again once it had refetched. Measured on a toggle, the sequence
 * was off -> on -> **off** -> on, with the wrong value standing for about 110
 * ms. The comment beside the surviving call already said rendering before the
 * refetch would show the state the toggle was clicked out of; it did, from
 * here. The owner is the caller now, so the panel is built once per refresh
 * and from one source.
 */
async function loadProviders() {
  /** @type {any} */
  let payload = null;
  try {
    payload = await getJson(ROUTES.keys);
  } catch (error) {
    payload = null;
  }
  if (!payload || !payload.providers) {
    fill(el("providers"), []);
    setText(el("settings-note"), t("settings.none"));
    renderHealthProviders();
    return;
  }
  setText(el("settings-note"), "");
  const items = payload.providers.map(
    (/** @type {any} */ provider) => providerRow(provider));
  fill(el("providers"), items);
}

/**
 * The subscription tools this server found on its own machine, a toggle each.
 *
 * **Beside the endpoints, because it is the same question one mechanism
 * over.** The operator's report was that they could not find this feature at
 * all: it existed, it worked, and the only way to configure it was a file they
 * were never told about. An endpoint is an address and a key; this is a
 * program already on the machine. Both are "how does this server reach a
 * model", so they are in one sheet.
 *
 * **What the browser sends is an id the server already found.** There is no
 * field in this panel. The checkbox `PUT`s or `DELETE`s a path whose last
 * segment is one of `commands.KNOWN_TOOLS`' ids, and the server supplies the
 * command from `shutil.which`. Nothing typed here can reach a command line
 * because nothing here can be typed.
 *
 * **An empty panel is the failure this exists to fix, so there isn't one.**
 * Three states and a sentence for each: this server cannot record a route at
 * all, this server found nothing, or here is what it found.
 */
function renderCommandTools() {
  const section = el("commands-section");
  const block = (store.config && store.config.commands) || {};
  const tools = block.discovered || [];
  const note = el("commands-note");
  // A library-embedded server has no commands file to write into, so there is
  // nothing to offer and the panel says which of the two empty states this is.
  // "Nothing found" and "nowhere to put it" have different remedies.
  // **Where a route that was in the picker yesterday went.** Its own element
  // and above the list, because it tells the reader to switch one on *below*
  // and because it is not a note about a control they just used -- which is
  // what the note at the foot is, and what `reloadAfterSettings` overwrites
  // on every toggle. Said on all three branches: a server that found nothing
  // still has to explain a route it retired.
  const retired = block.retired || [];
  const retiredNote = el("commands-retired");
  if (retiredNote) {
    retiredNote.hidden = !retired.length;
    setText(retiredNote, retired.length
      ? t("commands.retired", { ids: retired.join(", ") }) : "");
  }
  if (!block.configurable) {
    fill(el("commands-list"), []);
    renderCommandProblems([]);
    setText(note, t("commands.unconfigurable"));
    section.hidden = false;
    return;
  }
  if (!tools.length) {
    fill(el("commands-list"), []);
    renderCommandProblems([]);
    setText(note, t("commands.none"));
    section.hidden = false;
    return;
  }
  // Every row of the file this build could not use that is not one of the four
  // below. A row that *is* one of them carries its own message, because a
  // sentence naming one route belongs beside that route.
  const ids = tools.map((/** @type {any} */ tool) => String(tool.id));
  renderCommandProblems((block.problems || []).filter(
    (/** @type {any} */ bad) => !ids.includes(String(bad.id))));
  // The rows are the table and are always all of them, so "nothing was found"
  // is a property of the rows rather than of their count. Said once at the
  // foot of the panel as well as on each row, because the panel-level question
  // a reader arrives with is "can I use this at all" and an answer they have
  // to assemble from four rows is an answer they may not assemble.
  const found = tools.some((/** @type {any} */ tool) => tool.available);
  // What the panel says at its foot, unchanged. A problem that belongs to a
  // row is **not** here and the retirement notice is not here either: the
  // operator met a page-level wall of text about one stale route, and a
  // message that names one route belongs beside that route.
  setText(note, block.editable === false ? t("commands.notyours")
                : (found ? "" : t("commands.none")));
  // Said once, above the list. `models.route.*`, not new strings: these are
  // the same three sentences the picker puts on a command row, and two
  // wordings of one fact is how the two stop agreeing.
  setText(el("commands-shared"), t("models.route.shared"));
  setText(el("commands-tier"), t("models.route.incomparable"));
  setText(el("commands-cost"), t("models.cost.plan"));
  fill(el("commands-list"), tools.map(
    (/** @type {any} */ tool) => commandToolRow(tool, block.editable !== false)));
  section.hidden = false;
}

/**
 * The rows of the commands file this build could not use. Usually none.
 *
 * **A row, not a banner.** The operator's report was a page-level wall of text
 * about one stale route -- it was the whole panel, it took the picker with it,
 * and it said nothing about which of their routes it meant. Each message names
 * exactly one route, so each one is rendered as that route's row.
 *
 * There is no control on these. A row this page wrote is retired at startup by
 * `Commands.migrate`, so a row that reaches here is one the operator wrote and
 * one the server refuses to edit.
 * @param {any[]} problems
 */
function renderCommandProblems(problems) {
  const list = el("commands-problems");
  if (!list) return;
  list.hidden = !problems.length;
  fill(list, problems.map((/** @type {any} */ bad) => {
    const row = clone("tpl-command-problem");
    setText(find(row, "command-problem-name"), String(bad.id || ""));
    const chip = find(row, "command-problem-chip");
    setState(chip, "bad");
    setText(chip, t("commands.problem"));
    setText(find(row, "command-problem-note"), String(bad.reason || ""));
    return row;
  }));
}

/**
 * One discovered tool.
 *
 * The three sentences under the name are the ones a command route owes its
 * reader, and they are the **same catalogue keys** the picker puts on the row
 * rather than a second wording of them: not per-user, answers at a tier none
 * of the published figures were measured at, and a cost that is a word and
 * never a zero. Two wordings of one fact is how the two stop agreeing.
 * @param {any} tool
 * @param {boolean} editable
 * @returns {HTMLElement}
 */
function commandToolRow(tool, editable) {
  const row = clone("tpl-command");
  setText(find(row, "command-name"), String(tool.label || tool.id || ""));
  const chip = find(row, "command-chip");
  setState(chip, tool.available ? "ok" : "");
  setText(chip, t(tool.available ? "commands.found" : "commands.missing"));

  // Said in words as well as by the chip, with the remedy in it. A tool that
  // is not installed for the account this server runs as is the ordinary case
  // on a server, and "install it or name it in the file" is the whole answer.
  //
  // The available case names the **model** this route pins and the window it
  // would carry. Which model is the whole of the operator's second
  // complaint -- *"It is not clear which one would be used"* -- and it is a
  // fact the server states rather than one this page derives from a label.
  // A row of the file already holds this id and did not load. Said here, on
  // the row it is about, and in the server's own words -- the same sentence
  // the write path would have refused with, so the page and the refusal
  // cannot say two different things about one route.
  setText(find(row, "command-note"), tool.problem ? String(tool.problem)
    : (tool.available
       ? (tool.owned ? t("commands.owned")
                     : t("commands.pins", { model: String(tool.model || ""),
                                            n: tool.window }))
       : t("commands.missing.hint")));

  const toggle = /** @type {HTMLInputElement} */ (find(row, "command-toggle"));
  const label = find(row, "command-toggle-label");
  associate(label, toggle);
  setText(find(row, "command-toggle-text"), t("commands.enable"));
  toggle.checked = Boolean(tool.enabled);
  // Which route this box is, in the DOM, so the rebuilt panel can be asked for
  // the same one afterwards (561). The `data-cc` hooks are how this page finds
  // *a* control of a kind, and every row carries the same ones; this says
  // *which* row, which is the question a focus restore has to answer. By id
  // rather than by position: a retired route shortens the list between the
  // click and the rebuild, and an index would then move the focus to a
  // neighbour without saying so.
  toggle.setAttribute("data-command", String(tool.id));
  // Inert for three reasons, each of which the row already states in words: it
  // is not installed, it is somebody else's row, or this account is not the
  // operator. A control the server would answer 403 or 409 to is a control
  // that explains a refusal after the fact.
  // Inert for a fourth reason as well: the file already holds a row with this
  // id that this build cannot read and that this page may not replace. The
  // row says which in words; `owned` is what the server has already decided
  // about a broken row's ownership, so the page does not decide it twice.
  toggle.disabled = !editable || !tool.available || Boolean(tool.owned);
  toggle.addEventListener("change", async () => {
    const wanted = toggle.checked;
    let said = "";
    try {
      await sendJson(wanted ? "PUT" : "DELETE",
                     route(ROUTES.commandTool, { name: String(tool.id) }),
                     undefined);
      said = t(wanted ? "commands.enabled" : "commands.disabled");
    } catch (error) {
      // Put back, because the server is the state and this box is a view of
      // it. A tick left standing after a refusal is a page claiming a route
      // exists that the picker will not offer.
      toggle.checked = !wanted;
      said = describe(error);
    }
    // Whether the keyboard was on this box when it was used. Read before the
    // reload, because the reload is what destroys the element it is about.
    const had = document.activeElement === toggle;
    // After the reload, not before. `reloadAfterSettings` re-renders this
    // panel and the re-render clears the note, so saying it first made the
    // confirmation flash and vanish -- visible only by watching the page,
    // which is where it was found.
    await reloadAfterSettings();
    setText(el("commands-note"), said);
    // Put the keyboard back where it was (561). The panel is rebuilt from the
    // server's answer, so the control that was just used is a different
    // element by the time the answer arrives, and focus had been landing on
    // `body` -- which sends the next Tab back to the top of the sheet. Found
    // by measuring rather than by reading: `document.activeElement` was `BODY`
    // after all four toggles in the drive, mouse and keyboard alike.
    if (had) {
      const again = document.querySelector(
        '[data-command="' + String(tool.id) + '"]');
      if (again instanceof HTMLElement) again.focus();
    }
  });
  return row;
}

/**
 * The read-only view, for a server with no credential endpoint: `/health`
 * still says which variable each role reads and whether it is configured.
 */
function renderHealthProviders() {
  const providers = (store.health && store.health.providers) || [];
  /** @type {Record<string, boolean>} */
  const seen = {};
  /** @type {HTMLElement[]} */
  const items = [];
  for (const provider of providers) {
    if (seen[provider.variable]) continue;
    seen[provider.variable] = true;
    items.push(providerRow({
      name: provider.role, variable: provider.variable,
      configured: provider.configured, suffix: "",
    }, true));
  }
  fill(el("providers"), items);
}

/**
 * Two endpoint addresses that name one place: the server stores an address
 * without its trailing slash (`clean_base_url`), and a typed one may have it.
 * @param {string} one
 * @param {string} two
 * @returns {boolean}
 */
function sameAddress(one, two) {
  return one.trim().replace(/\/+$/, "") === two.trim().replace(/\/+$/, "");
}

/**
 * @param {any} provider
 * @param {boolean} [readOnly]
 * @returns {HTMLElement}
 */
function providerRow(provider, readOnly) {
  const row = clone("tpl-provider");
  setText(find(row, "provider-name"), String(provider.name || ""));
  const chip = find(row, "provider-chip");
  setState(chip, provider.configured ? "ok" : "");
  setText(chip, provider.configured
    ? t("settings.configured") + (provider.suffix ? " · …" + provider.suffix : "")
    : t("settings.unconfigured"));
  // Whose row this is. Empty when nobody has configured one, because an unset
  // provider belongs to nobody and a chip saying otherwise would be a claim.
  const owner = find(row, "provider-owner");
  setText(owner, provider.owner
    ? t(provider.owner === "you" ? "settings.owner.you" : "settings.owner.operator")
    : "");
  setState(owner, "");
  // Hidden rather than empty. A chip is a bordered pill, so an empty one
  // renders as a small blank box beside the state chip -- found by looking at
  // the page, which is the only place it is visible at all.
  owner.hidden = !provider.owner;
  // Both variables on one line: the key's and the endpoint's. An operator
  // reading `configured: false` needs to know which variables were looked at,
  // and the endpoint half is what lets them set it in the unit file that
  // starts the server instead of on this page.
  setText(find(row, "provider-variable"),
    String(provider.variable || "")
    + (provider.url_variable ? " \u00b7 " + String(provider.url_variable) : ""));

  const url = /** @type {HTMLInputElement} */ (find(row, "provider-url"));
  associate(find(row, "provider-url-label"), url);
  url.value = String(provider.base_url || "");
  // A description, not the variable name and not an example address. The
  // variable belongs on the line above; in the field it reads as something to
  // type, which is how an operator ends up with a base URL of
  // `LLOSSLESS_PROVIDER_URL_OPENAI`. An example URL cannot go here either --
  // `tests/test_web_static.py` refuses any address in a shipped file, on the
  // grounds that a self-hosted page must reach nothing off this machine, and
  // it is right to refuse a literal it cannot tell from a live one.
  // The server's example for a provider with no well-known address (676):
  // served, never written here, for the reason above.
  url.placeholder = provider.example_url
    ? t("settings.endpoint.example", { url: String(provider.example_url) })
    : t("settings.endpoint.placeholder");
  const urlSave = /** @type {HTMLButtonElement} */ (find(row, "provider-url-save"));
  const urlClear = /** @type {HTMLButtonElement} */ (find(row, "provider-url-clear"));
  const note = find(row, "provider-note");
  const listed = (provider.models || []).length;
  // A vendor's listing needs a key, and the probe never sends one, so a
  // stored vendor address usually lists nothing. Its catalogue rows are in
  // the picker all the same (676): say that, not "type a model id".
  const known = ((store.config && store.config.catalogue && store.config.catalogue.models) || [])
    .filter((/** @type {any} */ model) => model.provider === provider.name && !isRetired(model)).length;
  setText(note, provider.base_url
    ? (listed ? t("settings.listed", { n: listed })
       : known ? t("settings.catalogue", { n: known }) : t("settings.notlisted", { n: listed }))
    : t("settings.noendpoint"));

  const field = /** @type {HTMLInputElement} */ (find(row, "provider-key"));
  associate(find(row, "provider-input-label"), field);
  const save = /** @type {HTMLButtonElement} */ (find(row, "provider-save"));
  const clear = /** @type {HTMLButtonElement} */ (find(row, "provider-clear"));
  // A row the operator owns is not yours to change, and the page says so
  // rather than offering four controls the server answers 403 to. Configuring
  // your own for the same provider is the way to use a different one, and the
  // sentence says that too.
  if (provider.editable === false) {
    setText(note, t("settings.notyours"));
    readOnly = true;
  }
  if (readOnly) {
    field.disabled = true; save.disabled = true; clear.disabled = true;
    url.disabled = true; urlSave.disabled = true; urlClear.disabled = true;
    return row;
  }
  // **The well-known address, offered** (676). With none stored, the field
  // holds the provider's usual address and the row shows it as a line with
  // "Change address", so a person only pastes a key; saving the key saves
  // this address first, as an explicit value. A stored address that is the
  // usual one reads the same way. Any other stored address shows the field.
  const preset = String(provider.preset_url || "");
  const stored = String(provider.base_url || "");
  const offered = Boolean(preset) && (!stored || sameAddress(stored, preset));
  if (!stored && preset) {
    url.value = preset;
    setText(note, t("settings.preset.note"));
  }
  const line = find(row, "provider-address");
  const fieldRow = find(row, "provider-url-row");
  line.hidden = !offered;
  fieldRow.hidden = offered;
  setText(find(row, "provider-address-text"), stored || preset);
  find(row, "provider-address-change").addEventListener("click", () => {
    line.hidden = true;
    fieldRow.hidden = false;
    url.focus();
    url.select();
  });
  urlSave.addEventListener("click", async () => {
    try {
      // The answer carries what the endpoint said it serves, so the note is
      // the probe's own sentence rather than a guess about whether it worked.
      const answer = await sendJson(
        "PUT", route(ROUTES.endpoint, { name: String(provider.name) }),
        { base_url: url.value });
      setText(el("settings-note"), t("settings.endpoint.saved"));
      setText(note, String((answer && answer.note) || ""));
    } catch (error) {
      setText(el("settings-note"), describe(error));
    }
    await reloadAfterSettings();
  });
  urlClear.addEventListener("click", async () => {
    try {
      await sendJson("DELETE", route(ROUTES.endpoint, { name: String(provider.name) }),
                     undefined);
      setText(el("settings-note"), t("settings.endpoint.cleared"));
    } catch (error) {
      setText(el("settings-note"), describe(error));
    }
    await reloadAfterSettings();
  });
  save.addEventListener("click", async () => {
    const key = field.value;
    field.value = "";
    if (!key) return;
    // **A key goes to the address on screen, and only there** (676). When
    // the address shown is not the one stored -- the offered well-known one,
    // or an edit not yet saved -- it is saved first, which clears any key
    // bound to the old one (`Endpoint.moved_to`), and the key is then stored
    // against it. A refused address stops the key from being sent at all.
    const shown = url.value.trim();
    let said = t("settings.saved");
    try {
      if (shown && !sameAddress(shown, String(provider.base_url || ""))) {
        await sendJson("PUT", route(ROUTES.endpoint, { name: String(provider.name) }),
                       { base_url: shown });
      }
      await sendJson("PUT", route(ROUTES.key, { name: String(provider.name) }), { key: key });
    } catch (error) {
      said = describe(error);
    }
    await reloadAfterSettings();
    // After the reload, which clears this line (`loadProviders`).
    setText(el("settings-note"), said);
  });
  clear.addEventListener("click", async () => {
    try {
      await sendJson("DELETE", route(ROUTES.key, { name: String(provider.name) }), undefined);
      setText(el("settings-note"), t("settings.cleared"));
    } catch (error) {
      setText(el("settings-note"), describe(error));
    }
    await reloadAfterSettings();
  });
  return row;
}

/**
 * Re-read everything a credential change can move, in one place.
 *
 * `/config` is in the list and was the thing the first version of this
 * forgot: saving an endpoint changes which rows in the picker are reachable
 * and which models the picker even has, and a page that refreshed only the
 * credentials sheet would leave the operator looking at a table that still
 * said their model was unreachable after they had just made it reachable.
 */
async function reloadAfterSettings() {
  await loadProviders();
  await refreshHealth();
  try {
    store.config = await getJson(ROUTES.config);
  } catch (error) {
    return;
  }
  renderModels();
  // After the refetch, not during `loadProviders`. The discovered rows and
  // their enabled state come from `/config`, which is re-read three lines up,
  // so rendering them before it would show the state the toggle was just
  // clicked out of -- the same staleness `renderModels` is called here for.
  renderCommandTools();
  refreshIdleStatus();
}

/** `/health`, for the version line and the credential states. */
async function refreshHealth() {
  try {
    store.health = await getJson(ROUTES.health);
    setText(el("version"), String(store.health.version || "") +
      " · " + String(store.health.api || ""));
  } catch (error) {
    setText(el("version"), "");
  }
}

/* ------------------------------------------------------------------ */
/* boot                                                                */
/* ------------------------------------------------------------------ */

/**
 * The top bar's readiness pill (redesign A), one of five states, each a
 * literal key so the key checks can see it. The key is written onto the text
 * as `data-t`, so a language change redraws it with everything else.
 * @type {Record<string, [string, string]>}
 */
const PILL_STATES = {
  loading: ["pill.loading", ""],
  ready: ["pill.ready", "ok"],
  empty: ["pill.empty", "warn"],
  signedout: ["pill.signedout", ""],
  unreachable: ["pill.unreachable", "bad"],
};

/**
 * Say how ready this server is to run a merge, in the top bar.
 * @param {string} state a key of `PILL_STATES`
 */
function renderPill(state) {
  const [key, tone] = PILL_STATES[state] || PILL_STATES.loading;
  const pill = el("status-pill");
  setState(pill, tone);
  const text = el("status-pill-text");
  text.setAttribute("data-t", key);
  setText(text, t(key));
  pill.hidden = false;
}

/**
 * Fill every element carrying a `data-t` key from the catalogue.
 *
 * Over the whole document, which reaches the static furniture and every row
 * already cloned out of a template and inserted -- so a language chosen in the
 * middle of a session redraws the credential sheet without it having to be
 * reopened. It does not reach the templates themselves; `clone` does that, for
 * the reason given there.
 */
function applyStrings() {
  applyStringsIn(document);
  paintColumnHelp();
}

/**
 * The same, over one subtree.
 * @param {ParentNode} root
 */
function applyStringsIn(root) {
  const nodes = root.querySelectorAll("[data-t]");
  for (let index = 0; index < nodes.length; index += 1) {
    const node = /** @type {HTMLElement} */ (nodes[index]);
    const key = node.getAttribute("data-t");
    if (key && strings[key] !== undefined) {
      setText(node, strings[key]);
    }
  }
}

/**
 * The language picker: one option per catalogue the server holds.
 *
 * Hidden when there is only one. A picker with a single option is a control
 * that cannot be operated, and it would tell an operator this server offers a
 * choice it does not have.
 */
function renderLocalePicker() {
  const field = el("locale-field");
  field.hidden = locale.available.length < 2;
  const picker = select("locale-select");
  fill(picker, locale.available.map((entry) => {
    const option = document.createElement("option");
    option.value = String(entry.tag);
    // The label is the language's name in that language -- "Deutsch", not
    // "German" -- because the one person who needs to read this control is
    // the one who cannot currently read the page.
    setText(option, String(entry.label || entry.tag));
    return option;
  }));
  picker.value = locale.tag;
}

/**
 * Change the language, remember the choice, and redraw everything made of
 * sentences.
 *
 * Redrawn from what is already in `store` rather than re-fetched. The config,
 * the report and the merged document do not change with the language -- the
 * server does not localise any of them, on purpose -- so a round trip here
 * would cost a request per keystroke on the picker and could not produce a
 * different answer.
 * @param {string} tag
 * @returns {Promise<void>}
 */
async function changeLocale(tag) {
  // A document still under the name the page gave it -- "document 2" -- was
  // named in the old language and nobody typed it, so it follows the new one
  // (640); the status line names it. A name somebody typed is theirs and is
  // never touched. Matched by the old template with its number, so a pane
  // that moved when another was removed keeps its own number.
  const template = t("documents.untitled", { n: "\u0000" });
  const [head, tail] = template.split("\u0000");
  const numbered = store.docs.map((doc) => {
    if (tail === undefined || !doc.name.startsWith(head) || !doc.name.endsWith(tail)) return "";
    const n = doc.name.slice(head.length, doc.name.length - tail.length);
    return /^[0-9]+$/.test(n) ? n : "";
  });
  try {
    await loadLocale(tag);
  } catch (error) {
    // The chosen catalogue is gone or unreadable. The page is still in the
    // language it was in, and saying so beats leaving a picker showing a
    // language the page is not in.
    renderLocalePicker();
    return;
  }
  rememberLocale(tag);
  store.docs.forEach((doc, index) => {
    if (!numbered[index]) return;
    const renamed = t("documents.untitled", { n: numbered[index] });
    // The base is held by name, so it moves with the rename rather than
    // falling back to the first document.
    if (store.base === doc.name) store.base = renamed;
    doc.name = renamed;
  });
  applyStrings();
  renderLocalePicker();
  // The header's one sentence the catalogue pass cannot reach: it carries the
  // user's name (673; it stayed in the old language before).
  renderSession();
  if (store.config) renderControls();
  renderDocuments();
  if (store.report) {
    renderReport(store.report);
    announceOutcome(store.report, store.merged);
    // Made of sentences and of a span, both of which are in the catalogue.
    renderRetention();
  }
  // The documents sentence and the notes are catalogue strings; the command
  // and the env lines are not (they are the operator's addresses and this
  // build's own flags), so this redraws the labels around unchanged bytes.
  if (store.cliEquivalent) renderCliEquivalent(store.cliEquivalent);
  void refreshHistory();
}

/* ------------------------------------------------------------------ */
/* the workbench: step tabs, output tabs, finding tabs (673)           */
/* ------------------------------------------------------------------ */

/**
 * The input steps, in order. Each is a tab `#step-tab-<step>` in the
 * `step-tabs` list and a panel `#step-<step>`; the number a step shows is its
 * place here plus one.
 */
const STEPS = ["documents", "model", "settings", "tuning"];

/**
 * Each step's name, by the catalogue key its tab and panel heading render.
 * @type {Record<string, string>}
 */
const STEP_NAMES = {
  documents: "documents.heading",
  model: "step.model",
  settings: "controls.heading",
  tuning: "step.tuning",
};

/**
 * The hook of the state line under each step's name.
 * @type {Record<string, string>}
 */
const STEP_STATE_HOOKS = {
  documents: "step-state-documents",
  model: "step-state-model",
  settings: "step-state-settings",
  tuning: "step-state-tuning",
};

/**
 * The finding sections' hooks, in tab order. `openIf` marks one for
 * attention; `renderReport` clears the marks before the renderers run.
 */
const FINDING_SECTIONS = [
  "review-section", "conflicts-section", "omitted-section", "attributions-section",
  "numbers-section", "additions-section", "claims-section", "checks-section",
];

/** Where the selected step is remembered, per browser. Every access guarded. */
const STEP_KEY = "llossless.step";

/**
 * Which tab each set has selected. `finding` is a section name, and empty
 * until a result has picked one. `effortShown` is whether the effort slider
 * was showing at the last look, and `effortSeen` whether the Settings step
 * has been opened since it appeared (the tab's "new" marker).
 */
const layout = { step: "documents", output: "run", finding: "", effortShown: false, effortSeen: true };

/** @returns {boolean} true under 1024px, where the panes stack */
function narrowLayout() {
  return typeof window.matchMedia === "function"
    && window.matchMedia("(max-width: 63.99rem)").matches;
}

/**
 * The tabs of one set that are shown.
 * @param {HTMLElement} list
 * @returns {HTMLElement[]}
 */
function shownTabs(list) {
  return /** @type {HTMLElement[]} */ (Array.from(list.querySelectorAll('[role="tab"]')))
    .filter((tab) => !tab.hidden);
}

/**
 * The panel a tab controls.
 * @param {Element} tab
 * @returns {HTMLElement|null}
 */
function panelOf(tab) {
  return document.getElementById(tab.getAttribute("aria-controls") || "");
}

/**
 * Select one tab of a set: `aria-selected`, the roving tabindex, and which
 * panel shows. A panel that is not selected carries `tab-off`; `hidden` stays
 * with the renderers, which use it for "does not apply to this run".
 * @param {HTMLElement} list
 * @param {HTMLElement} chosen
 */
function selectTab(list, chosen) {
  for (const tab of Array.from(list.querySelectorAll('[role="tab"]'))) {
    const on = tab === chosen;
    tab.setAttribute("aria-selected", on ? "true" : "false");
    tab.setAttribute("tabindex", on ? "0" : "-1");
    const panel = panelOf(tab);
    if (panel) panel.classList.toggle("tab-off", !on);
  }
}

/**
 * The WAI-ARIA tabs pattern on one list, with automatic activation: a click
 * selects, Left and Right move and select (wrapping), Home and End go to the
 * ends. Only shown tabs are stepped through.
 * @param {HTMLElement} list
 * @param {(tab: HTMLElement) => void} choose
 */
function wireTabs(list, choose) {
  list.addEventListener("click", (event) => {
    const target = /** @type {Element} */ (event.target);
    const tab = /** @type {HTMLElement|null} */ (target.closest('[role="tab"]'));
    if (tab && list.contains(tab)) choose(tab);
  });
  list.addEventListener("keydown", (event) => {
    const tabs = shownTabs(list);
    const at = tabs.indexOf(/** @type {HTMLElement} */ (document.activeElement));
    if (at < 0 || !tabs.length) return;
    const key = /** @type {KeyboardEvent} */ (event).key;
    const next = key === "ArrowRight" ? (at + 1) % tabs.length
      : key === "ArrowLeft" ? (at - 1 + tabs.length) % tabs.length
      : key === "Home" ? 0
      : key === "End" ? tabs.length - 1
      : -1;
    if (next < 0) return;
    event.preventDefault();
    choose(tabs[next]);
    tabs[next].focus();
    tabs[next].scrollIntoView({ block: "nearest", inline: "nearest" });
  });
}

/**
 * Show one input step.
 * @param {string} step one of `STEPS`
 * @param {boolean} [focusPanel] move focus to the panel and, stacked, the
 *   page to the steps (Back, Next); a tab click and the restore on load do not
 */
function goToStep(step, focusPanel) {
  const chosen = STEPS.indexOf(step) >= 0 ? step : STEPS[0];
  layout.step = chosen;
  const tab = document.getElementById("step-tab-" + chosen);
  if (tab) {
    selectTab(el("step-tabs"), tab);
    tab.scrollIntoView({ block: "nearest", inline: "nearest" });
  }
  try {
    window.localStorage.setItem(STEP_KEY, chosen);
  } catch (_) {
    // No storage: the step holds for this page only.
  }
  el("input-body").scrollTop = 0;
  if (chosen === "settings") {
    layout.effortSeen = true;
    el("step-new-settings").hidden = true;
  }
  // Stacked, the steps may be a screen above what the reader is looking at.
  if (focusPanel && narrowLayout()) el("step-tabs").scrollIntoView({ block: "start" });
  const panel = document.getElementById("step-" + chosen);
  if (focusPanel && panel) panel.focus({ preventScroll: true });
}

/** @returns {string} the step this browser was on last, or the first */
function storedStep() {
  try {
    const value = window.localStorage.getItem(STEP_KEY) || "";
    return STEPS.indexOf(value) >= 0 ? value : STEPS[0];
  } catch (_) {
    return STEPS[0];
  }
}

/**
 * Take the reader to the step that is holding the run back, and to the
 * control in it that needs them: the first empty document, or the model
 * field that refused. A blocked run never fails silently behind a tab.
 * @param {string} step
 */
function goToBlocker(step) {
  if (step === "documents") {
    const empty = store.docs.findIndex((doc) => !String(doc.text || "").trim());
    if (empty >= 0 && empty !== store.active) {
      store.active = empty;
      renderDocuments();
    }
  }
  goToStep(step);
  /** @type {HTMLElement|null} */
  let target = null;
  if (step === "documents") {
    const doc = store.docs[store.active];
    const pane = doc ? document.getElementById(doc.id) : null;
    target = pane ? pane.querySelector('[data-cc="doc-text"]') : null;
  } else if (step === "model") {
    target = !el("window-block").hidden ? input("custom-window")
      : store.customOn ? input("custom-model")
      : el("picker-rows").querySelector("input:checked:not(:disabled)")
        || el("picker-rows").querySelector("input:not(:disabled)");
  }
  const focusable = target || document.getElementById("step-" + step);
  if (focusable) focusable.focus({ preventScroll: false });
}

/**
 * Which input step holds the run back, or "" when it is ready. `readiness`
 * names the documents step on its document reasons; the only other reason
 * it gives is `unreachableChoice`, which is the model step's.
 * @param {{ready: boolean, step?: string}|null} state
 * @returns {string}
 */
function blockingStep(state) {
  if (!state || state.ready) return "";
  return String(state.step || "model");
}

/**
 * A step's name in the reader's language.
 * @param {string} step
 * @returns {string}
 */
function stepName(step) {
  return STEP_NAMES[step] ? t(STEP_NAMES[step]) : step;
}

/**
 * The button under the status line that goes to the blocking step, or
 * hidden. `refreshIdleStatus` calls it with what `readiness` said.
 * @param {{ready: boolean, step?: string}|null} state
 */
function renderStepGoto(state) {
  const go = el("status-goto");
  const step = blockingStep(state);
  go.hidden = !step;
  go.setAttribute("data-step", step);
  setText(go, step ? t("step.goto", { n: STEPS.indexOf(step) + 1, name: stepName(step) }) : "");
}

/**
 * The line under each step's name: what it holds, and whether it is done or
 * needs attention (`ok` or `warn` on the line, which `layout.css` carries to
 * the tab's number). The words carry it; the colour repeats them.
 */
function renderStepStates() {
  if (!store.config) return;
  const paint = (/** @type {string} */ step, /** @type {string} */ text, /** @type {boolean} */ done) => {
    const line = el(STEP_STATE_HOOKS[step]);
    setState(line, done ? "ok" : "warn");
    setText(line, text);
    // The line ends in an ellipsis when the tab is narrow; the whole of it
    // for a pointer.
    line.setAttribute("title", text);
  };

  const filled = store.docs.filter((doc) => String(doc.text || "").trim()).length;
  const empty = store.docs.length - filled;
  if (filled < minDocuments()) {
    paint("documents", t("step.state.docs.short", { n: filled, min: minDocuments() }), false);
  } else if (empty > 0) {
    paint("documents", t("step.state.docs.empty", { n: empty }), false);
  } else {
    paint("documents", t("step.state.docs", { n: filled, max: maxDocuments() }), true);
  }

  const stranded = unreachableChoice();
  paint("model", stranded ? t("step.state.fix") : modelSummary(), !stranded);

  const levels = ((store.config.fidelity || {}).levels) || [];
  const level = levels.find((/** @type {any} */ entry) => entry.value === store.fidelity);
  const settings = [level ? String(level.name) : "", store.verifyDepth ? depthName(store.verifyDepth) : ""]
    .filter(Boolean).join(", ");
  paint("settings", settings, true);
  // The effort slider lives on the Settings step and shows only for a route
  // that takes it (673). When it appears, the tab says "new" until the step
  // is opened, so a reader who picked such a route cannot miss it.
  const effortShown = !el("effort-block").hidden;
  if (effortShown && !layout.effortShown) layout.effortSeen = layout.step === "settings";
  layout.effortShown = effortShown;
  el("step-new-settings").hidden = !effortShown || layout.effortSeen;

  paint("tuning", t("step.state.tuning", {
    pct: (store.lossBudget * 100).toFixed(1) + "%", title: store.titlePolicy || "-",
  }), true);
}

/**
 * The model step's state line: the typed id, or the picked row's name (both
 * rows when the checks have their own), or the server's own default.
 * @returns {string}
 */
function modelSummary() {
  const typed = typedId();
  if (typed) return typed;
  const rows = pickable();
  const name = (/** @type {string} */ id) => {
    const row = rows.find((/** @type {any} */ entry) => entry.id === id);
    return row ? String(row.display_name || row.id) : "";
  };
  const merge = name(store.mergeModel);
  if (!merge) return t("step.state.model.default");
  const check = store.splitRoles ? name(store.checkModel) : "";
  return check && check !== merge ? merge + " + " + check : merge;
}

/**
 * Show the current run, or the previous ones, in the output pane.
 * @param {"run"|"history"} which
 */
function showOutput(which) {
  const tab = document.getElementById(which === "history" ? "output-tab-history" : "output-tab-run");
  // `aria-disabled` (717), not `hidden`: both tabs are always on the page, and
  // one with nothing behind it yet refuses a click or an arrow-key selection
  // the same way, while a caller that has just put something behind it
  // (`enableRunTab`, `refreshHistory`) clears the attribute before it ever
  // calls this.
  if (!tab || tab.hidden || tab.getAttribute("aria-disabled") === "true") return;
  layout.output = which;
  selectTab(el("output-tabs"), tab);
}

/**
 * The Current run tab stops being `aria-disabled` the moment there is a run
 * behind it: submitted, followed from the list, or replayed (717). Idempotent,
 * so every caller can call it without first asking whether it already ran.
 */
function enableRunTab() {
  store.hasRun = true;
  const tab = document.getElementById("output-tab-run");
  if (tab) tab.setAttribute("aria-disabled", "false");
}

/**
 * Bring this run into view: its tab, the top of the pane and, stacked, the
 * pane itself. Called when a run starts, is followed, or lands.
 * @param {boolean} scrollPage
 */
function revealRun(scrollPage) {
  showOutput("run");
  el("output-body").scrollTop = 0;
  if (scrollPage && narrowLayout()) el("output-pane").scrollIntoView({ block: "start" });
}

/**
 * The Previous runs tab is always shown (717) but stays `aria-disabled` while
 * the list it opens is empty, exactly as `history-section` (`refreshHistory`)
 * is: a reader on it when the last entry disappears is put back on the
 * current run rather than left on a tab that no longer answers a click.
 */
function syncHistoryTab() {
  const tab = document.getElementById("output-tab-history");
  if (!tab) return;
  const empty = el("history-section").hidden;
  tab.setAttribute("aria-disabled", empty ? "true" : "false");
  if (empty && layout.output === "history") showOutput("run");
}

/**
 * The finding tabs follow their sections: a section a renderer hid takes its
 * tab with it, so there is never an empty tab. The selection stays where the
 * reader put it while that tab is shown; otherwise it goes to the review
 * list, then to the first section marked for attention, then to the first.
 */
function syncFindingTabs() {
  const list = el("finding-tabs");
  for (const tab of Array.from(list.querySelectorAll('[role="tab"]'))) {
    const panel = panelOf(tab);
    /** @type {HTMLElement} */ (tab).hidden = !panel || panel.hidden;
  }
  const shown = shownTabs(list);
  const named = (/** @type {string} */ name) =>
    shown.find((tab) => tab.id === "finding-tab-" + name);
  const chosen = named(layout.finding)
    || named("review")
    || shown.find((tab) => {
      const panel = panelOf(tab);
      return Boolean(panel && panel.hasAttribute("data-attention"));
    })
    || shown[0];
  if (!chosen) return;
  layout.finding = chosen.id.replace("finding-tab-", "");
  selectTab(list, chosen);
}

/**
 * Keep the stacked layout's padding equal to the fixed run bar, and the
 * scroll margin equal to the sticky top bar, as either changes height.
 */
function watchBars() {
  if (typeof ResizeObserver !== "function") return;
  const root = document.documentElement;
  const topbar = /** @type {HTMLElement|null} */ (document.querySelector(".topbar"));
  const observer = new ResizeObserver(() => {
    root.style.setProperty("--runbar-h", el("run-card").offsetHeight + "px");
    if (topbar) root.style.setProperty("--topbar-h", topbar.offsetHeight + "px");
  });
  observer.observe(el("run-card"));
  if (topbar) observer.observe(topbar);
}


/**
 * A "?" that shows `content` on hover and on keyboard focus (673): the
 * button is named for a screen reader and described by the text it opens.
 * The static ones are markup (`.help` in `index.html`); this builds the ones
 * that live inside a rendered option.
 * @param {HTMLElement} content
 * @returns {HTMLElement}
 */
function helpBox(content) {
  const box = document.createElement("span");
  box.className = "help";
  const button = document.createElement("button");
  button.type = "button";
  button.className = "help-icon";
  const mark = document.createElement("span");
  mark.setAttribute("aria-hidden", "true");
  setText(mark, "?");
  const name = document.createElement("span");
  name.className = "visually-hidden";
  setText(name, t("help.more"));
  button.appendChild(mark);
  button.appendChild(name);
  const pop = document.createElement("span");
  pop.className = "help-pop";
  pop.setAttribute("role", "tooltip");
  pop.id = uniqueId();
  button.setAttribute("aria-describedby", pop.id);
  pop.appendChild(content);
  box.appendChild(button);
  box.appendChild(pop);
  return box;
}

/**
 * A sample merge as a paragraph, with the words that changed from the level
 * before it in `<mark>`. The catalogue marks them with `[[` and `]]`, by
 * hand, because what changed is an editorial statement (a detail folded into
 * another sentence has moved, not changed, to a word diff). The brackets
 * never reach the page.
 * @param {string} text
 * @returns {HTMLElement}
 */
function markedSample(text) {
  const paragraph = document.createElement("p");
  paragraph.className = "compare-merge mono";
  text.split(/(\[\[[^\]]*\]\])/).forEach((part) => {
    if (!part) return;
    const marked = part.startsWith("[[") && part.endsWith("]]");
    const node = document.createElement(marked ? "mark" : "span");
    setText(node, marked ? part.slice(2, -2) : part);
    paragraph.appendChild(node);
  });
  return paragraph;
}

/**
 * The examples dialog (673): one tab a level this server offers, each with
 * the sample merge (the words changed from the level before it marked), a
 * line saying what changed, and the level's short line with its summary,
 * what it buys and what it costs (the sentences `--fidelity --help` prints)
 * behind a disclosure. The tab it opens on is the slider's.
 *
 * The summary/buys/costs used to sit behind a hover popup (`helpBox`)
 * absolutely positioned inside `.compare-panel`. Fine where `helpBox` is
 * used elsewhere (a one-line `.label-row` or `.radio-stack` option), but
 * `.compare-panel` is a tall, multi-paragraph block inside a `<dialog>`,
 * so the popup's containing block became the whole panel, not the small
 * "?" button. It opened far below the button, overlapped the dialog's own
 * "Close" button and was clipped by the dialog's edge (711, reported as
 * "the dialog gets garbled up"). A `<details>` in normal flow cannot
 * escape its container like that: opening it just pushes the panel, and
 * the dialog, taller. It also needs no separate keyboard wiring.
 */
function renderCompare() {
  const levels = ((store.config && store.config.fidelity) || {}).levels || [];
  const tabs = [];
  const panels = [];
  for (const level of levels) {
    const value = String(level.value || "");
    const tab = document.createElement("button");
    tab.type = "button";
    tab.className = "compare-tab";
    tab.setAttribute("role", "tab");
    tab.id = "compare-tab-" + value;
    tab.setAttribute("aria-controls", "compare-panel-" + value);
    tab.setAttribute("data-level", value);
    setText(tab, String(level.name || value));
    const panel = document.createElement("div");
    panel.className = "compare-panel";
    panel.id = "compare-panel-" + value;
    panel.setAttribute("role", "tabpanel");
    panel.setAttribute("aria-labelledby", tab.id);
    panel.tabIndex = 0;
    panel.appendChild(markedSample(t("brief.sample." + value)));
    const change = document.createElement("p");
    change.className = "compare-change";
    setText(change, t("brief.change." + value));
    panel.appendChild(change);
    const brief = document.createElement("p");
    brief.className = "compare-brief";
    setText(brief, t("brief.level." + value));
    panel.appendChild(brief);
    const disclosure = document.createElement("details");
    disclosure.className = "about-list fidelity-detail";
    const summary = document.createElement("summary");
    setText(summary, t("help.more"));
    disclosure.appendChild(summary);
    for (const part of ["summary", "buys", "costs"]) {
      const line = document.createElement("p");
      line.className = "hint help-line";
      setText(line, t("fidelity." + value + "." + part));
      disclosure.appendChild(line);
    }
    panel.appendChild(disclosure);
    tabs.push(tab);
    panels.push(panel);
  }
  fill(el("compare-tabs"), tabs);
  fill(el("compare-panels"), panels);
  const current = tabs.find((tab) => tab.getAttribute("data-level") === store.fidelity) || tabs[0];
  if (current) selectTab(el("compare-tabs"), current);
}

/** Open the Compare levels dialog on the slider's level. */
function openCompare() {
  renderCompare();
  const dialog = /** @type {HTMLDialogElement} */ (el("compare-dialog"));
  if (typeof dialog.showModal === "function") dialog.showModal();
  else dialog.setAttribute("open", "open");
}

/** Close it, and put focus back on the button that opened it. */
function closeCompare() {
  const dialog = /** @type {HTMLDialogElement} */ (el("compare-dialog"));
  if (dialog.open) {
    if (typeof dialog.close === "function") dialog.close();
    else dialog.removeAttribute("open");
  }
}

/** The dialog's selected level becomes the slider's. */
function useComparedLevel() {
  const tab = el("compare-tabs").querySelector('[aria-selected="true"]');
  const value = tab ? String(tab.getAttribute("data-level") || "") : "";
  const levels = ((store.config && store.config.fidelity) || {}).levels || [];
  if (levels.some((/** @type {any} */ level) => level.value === value)) {
    store.fidelity = value;
    renderFidelity();
    renderEffortCard();
    renderStepStates();
  }
  closeCompare();
}

/** The input pane's share of the width, in percent: bounds and default. */
const SPLIT = { min: 30, max: 75, start: 60 };

/** Where the divider's position is kept, per browser. Every access guarded. */
const SPLIT_KEY = "llossless.split";

/**
 * Put the divider at `percent` of the workbench: the two panes' columns,
 * the separator's value, and (when asked) the stored position.
 * @param {number} percent
 * @param {boolean} [remember]
 */
function setSplit(percent, remember) {
  const value = Math.round(Math.min(SPLIT.max, Math.max(SPLIT.min, percent)));
  const root = document.documentElement;
  root.style.setProperty("--pane-input", value + "fr");
  root.style.setProperty("--pane-output", (100 - value) + "fr");
  const divider = el("pane-divider");
  divider.setAttribute("aria-valuenow", String(value));
  divider.setAttribute("aria-valuetext", value + "%");
  if (!remember) return;
  try {
    window.localStorage.setItem(SPLIT_KEY, String(value));
  } catch (_) {
    // No storage: the width holds for this page only.
  }
}

/** @returns {number} the stored position, or the default */
function storedSplit() {
  try {
    const value = Number(window.localStorage.getItem(SPLIT_KEY));
    return value >= SPLIT.min && value <= SPLIT.max ? value : SPLIT.start;
  } catch (_) {
    return SPLIT.start;
  }
}

/**
 * The divider: drag it, or focus it and use Left/Right (2%), Page Up/Down
 * (10%), Home and End; a double-click, or Enter, puts it back.
 */
function wireDivider() {
  const divider = el("pane-divider");
  const main = el("workspace");
  const now = () => Number(divider.getAttribute("aria-valuenow")) || SPLIT.start;
  divider.addEventListener("keydown", (event) => {
    const key = /** @type {KeyboardEvent} */ (event).key;
    const next = key === "ArrowLeft" ? now() - 2
      : key === "ArrowRight" ? now() + 2
      : key === "PageDown" ? now() - 10
      : key === "PageUp" ? now() + 10
      : key === "Home" ? SPLIT.min
      : key === "End" ? SPLIT.max
      : key === "Enter" ? SPLIT.start
      : NaN;
    if (!isFinite(next)) return;
    event.preventDefault();
    setSplit(next, true);
  });
  divider.addEventListener("dblclick", () => setSplit(SPLIT.start, true));
  divider.addEventListener("pointerdown", (event) => {
    const down = /** @type {PointerEvent} */ (event);
    if (down.button !== 0) return;
    down.preventDefault();
    divider.setPointerCapture(down.pointerId);
    divider.classList.add("dragging");
    const move = (/** @type {Event} */ moved) => {
      const at = /** @type {PointerEvent} */ (moved);
      const box = main.getBoundingClientRect();
      if (box.width > 0) setSplit(((at.clientX - box.left) / box.width) * 100, false);
    };
    const up = () => {
      divider.removeEventListener("pointermove", move);
      divider.removeEventListener("pointerup", up);
      divider.removeEventListener("pointercancel", up);
      divider.classList.remove("dragging");
      setSplit(now(), true);
    };
    divider.addEventListener("pointermove", move);
    divider.addEventListener("pointerup", up);
    divider.addEventListener("pointercancel", up);
  });
  setSplit(storedSplit(), false);
}

/** Wire the three tab sets, Back and Next, and the way to a blocking step. */
function wireLayout() {
  wireTabs(el("step-tabs"), (tab) => goToStep(String(tab.getAttribute("data-step") || "")));
  wireTabs(el("output-tabs"), (tab) =>
    showOutput(tab.id === "output-tab-history" ? "history" : "run"));
  wireTabs(el("finding-tabs"), (tab) => {
    layout.finding = tab.id.replace("finding-tab-", "");
    selectTab(el("finding-tabs"), tab);
  });
  for (const button of Array.from(document.querySelectorAll("[data-step-go]"))) {
    button.addEventListener("click", () =>
      goToStep(String(button.getAttribute("data-step-go") || ""), true));
  }
  el("status-goto").addEventListener("click", () =>
    goToBlocker(String(el("status-goto").getAttribute("data-step") || "")));
  // A press on the Run button while it is disabled. A disabled button gets no
  // click, but the pointer's release still reaches the bar around it, and the
  // reader who pressed it wants to know why nothing happened.
  el("run-card").addEventListener("pointerup", (event) => {
    const button = /** @type {HTMLButtonElement} */ (el("submit"));
    const target = /** @type {Node} */ (event.target);
    if (!button.disabled || store.running || !button.contains(target)) return;
    const step = blockingStep(readiness());
    if (step) goToBlocker(step);
  });
  // A step's state follows every edit in the input pane, including the
  // controls whose own handlers do not come back through `refreshIdleStatus`
  // (the fidelity slider, the verify-depth radios, title policy, the loss
  // field): the save-defaults box has to follow the same edits (717), so it
  // unticks the moment they take the settings away from what is saved.
  const onEdit = () => { renderStepStates(); syncSaveDefaultsChecked(); };
  el("input-body").addEventListener("input", onEdit);
  el("input-body").addEventListener("change", onEdit);
  // The Compare levels dialog and its tabs.
  el("open-compare").addEventListener("click", openCompare);
  el("close-compare").addEventListener("click", closeCompare);
  el("compare-use").addEventListener("click", useComparedLevel);
  wireTabs(el("compare-tabs"), (tab) => selectTab(el("compare-tabs"), tab));
  el("compare-dialog").addEventListener("close", () => el("open-compare").focus());
  // Escape closes an open "?" by taking the focus off it (WCAG 1.4.13).
  document.addEventListener("keydown", (event) => {
    const active = document.activeElement;
    if (/** @type {KeyboardEvent} */ (event).key === "Escape"
        && active instanceof HTMLElement && active.classList.contains("help-icon")) {
      active.blur();
    }
  });
  wireDivider();
  watchBars();
  goToStep(storedStep());
}

/** Wire the buttons that are always there. */
function wire() {
  select("locale-select").addEventListener("change", () => {
    void changeLocale(select("locale-select").value);
  });
  el("submit").addEventListener("click", () => void submit());
  el("cancel-run").addEventListener("click", () => void confirmCancel());
  el("retry-run").addEventListener("click", () => void confirmRetry(store.retryId));
  el("notify").addEventListener("click", () => void askToNotify());
  el("cancel").addEventListener("click", () => {
    stopWatching();
    store.runId = "";
    setRunning(false);
    refreshIdleStatus();
  });
  el("start-over").addEventListener("click", () => void confirmStartOver());
  // The three saves, each through `saveFrom` rather than off its own `href`.
  // See `saveFrom` for why an anchor is not enough on its own.
  wireDownload(el("download-merged"), ROUTES.merged);
  wireDownload(el("download-report"), ROUTES.report);
  wireDownload(el("download-bundle"), ROUTES.bundle);
  el("copy-merged").addEventListener("click", () => void copyMerged());
  el("cli-copy").addEventListener("click", () => void copyCliCommand());
  // **On the box, not on the document** (561). A document-level handler would
  // have to decide for itself whether the reader meant this box, and it would
  // own Ctrl+A everywhere else on the page while it did. Hung here, the
  // shortcut exists exactly where the reader is: the `<pre>` carries
  // `tabindex="0"`, so clicking into it or tabbing to it focuses it, and
  // anywhere else on the page Ctrl+A still selects the page.
  el("merged").addEventListener("keydown", (event) => {
    const key = /** @type {KeyboardEvent} */ (event);
    if (key.key !== "a" && key.key !== "A") return;
    // The platform's own modifier on each platform, and neither of the two
    // that mean something else: Ctrl+Shift+A and Ctrl+Alt+A are other
    // shortcuts, and swallowing them would be this handler taking keys it was
    // not asked for.
    if (!(key.ctrlKey || key.metaKey) || key.altKey || key.shiftKey) return;
    if (!selectMerged()) return;
    key.preventDefault();
  });
  // **Escape closes the stacked view** (557, 561). The rule 557 settled for
  // the credentials sheet is that everything dismissible on this page agrees
  // with Escape, and a disclosure is dismissible. Only when the keyboard is
  // inside the open one: Escape over the page at large belongs to the dialogs,
  // which handle it themselves, and a handler that closed every stack on the
  // page from anywhere would be taking a key it was not given.
  //
  // Focus goes back to the summary that opened it, because the element the
  // keyboard was on is inside the part that just disappeared.
  document.addEventListener("keydown", (event) => {
    const key = /** @type {KeyboardEvent} */ (event);
    if (key.key !== "Escape" || key.defaultPrevented) return;
    const here = document.activeElement;
    if (!(here instanceof Element)) return;
    const panel = here.closest('[data-cc="stack-panel"]');
    if (!(panel instanceof HTMLDetailsElement) || !panel.open) return;
    panel.open = false;
    const summary = panel.querySelector('[data-cc="stack-summary"]');
    if (summary instanceof HTMLElement) summary.focus();
    key.preventDefault();
  });
  el("add-document").addEventListener("click", () => addDocument());
  const split = /** @type {HTMLInputElement} */ (el("split-models"));
  split.addEventListener("change", () => {
    store.splitRoles = split.checked;
    // Turning the split off re-joins the two rather than leaving the check
    // role wherever it was last put: the column is gone, so a value only that
    // column could show would be a setting nothing on the page reports.
    if (!store.splitRoles) store.checkModel = store.mergeModel;
    renderModels();
    refreshIdleStatus();
  });
  const toggle = input("custom-toggle");
  toggle.addEventListener("change", () => {
    store.customOn = toggle.checked;
    if (!store.customOn) {
      // Unticked is "the table is in charge", so the request carries nothing
      // typed and the field does not keep an id to surprise the next tick.
      store.customModel = "";
      store.customEndpoint = "";
      store.customWindow = "";
      input("custom-model").value = "";
      input("custom-window").value = "";
    }
    renderModels();
    refreshIdleStatus();
    if (store.customOn) input("custom-model").focus();
  });
  const custom = /** @type {HTMLInputElement} */ (el("custom-model"));
  associate(el("custom-model-label"), custom);
  custom.addEventListener("input", () => {
    store.customModel = custom.value;
    renderModels();
    refreshIdleStatus();
  });
  const windowField = input("custom-window");
  associate(el("custom-window-label"), windowField);
  windowField.addEventListener("input", () => {
    // A number field reports "" for text it cannot parse ("200k"), which
    // would read as no figure at all; `badInput` keeps it a figure that is
    // wrong, so the page names the bounds instead of asking for a number.
    store.customWindow = windowField.validity.badInput ? "?" : windowField.value;
    renderCustomWindow();
    refreshIdleStatus();
  });
  const endpoint = /** @type {HTMLSelectElement} */ (el("custom-endpoint"));
  associate(el("custom-endpoint-label"), endpoint);
  endpoint.addEventListener("change", () => {
    store.customEndpoint = endpoint.value;
    renderCustomModel();
    // The button names the route, and the endpoint decides it for a typed id.
    refreshIdleStatus();
  });
  select("base-select").addEventListener("change", () => {
    store.base = select("base-select").value;
  });
  const dialog = /** @type {HTMLDialogElement} */ (el("settings-dialog"));
  el("open-settings").addEventListener("click", () => {
    void loadProviders();
    // The commands panel's other owner (561). `loadProviders` used to do this
    // on the way past, which is what gave one panel two renderers; opening the
    // sheet renders it from the `/config` this page already holds, exactly as
    // before, and the toggle path renders it once from the `/config` it has
    // just refetched. Unconditional, where `loadProviders` had it on both of
    // its branches: a server with no credential endpoint can still have a
    // command route, and the panel must not depend on which branch ran.
    renderCommandTools();
    void loadAccounts();
    // Your own password, for anybody signed in. Hidden on a server with no
    // account store, where there is no password to change.
    el("password-section").hidden = !(store.session && store.session.user);
    setText(el("password-note"), "");
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "open");
  });
  el("close-settings").addEventListener("click", () => {
    if (typeof dialog.close === "function") dialog.close();
    else dialog.removeAttribute("open");
  });
  // **Every way out of this sheet has to be the same way out.**
  //
  // There is nothing buffered here to save or to discard: each row commits
  // itself the moment its own button or checkbox is used -- `PUT`, `DELETE`,
  // `POST`, one request per row -- and closing sends no request at all. So the
  // only thing a close decides is what becomes of text that was typed into a
  // field and never saved, and there were two answers to that in one sheet.
  // The provider rows are rebuilt from the server on every open and had always
  // dropped it; the four standing fields kept it, which left a password
  // standing in the DOM of a closed sheet and made the top half of the sheet
  // behave differently from the bottom.
  //
  // Hung on the dialog's own `close` rather than on the button, because that
  // is the event Escape fires too. A second handler on the button would be a
  // second answer that has to be kept in step with this one, and the way that
  // goes wrong is silent: Escape would quietly keep what the button drops.
  dialog.addEventListener("close", () => {
    for (const hook of ["new-account-name", "new-account-password",
                        "current-password", "new-password"]) {
      input(hook).value = "";
    }
  });
  // **The model scorecard** (631), on the credentials sheet's pattern:
  // `showModal`, Escape and the backdrop left to the dialog itself, the one
  // way out focused on open by its `autofocus`, and focus put back on the
  // button that opened it, because the element the keyboard was on is inside
  // what just closed. Rendered on open from the `/config` this page holds,
  // so it is current whatever changed since the last render.
  const scorecard = /** @type {HTMLDialogElement} */ (el("scorecard-dialog"));
  loadSort(scorecardSort);
  loadSort(pickerSort);
  el("open-scorecard").addEventListener("click", () => {
    if (store.config) renderScorecard();
    if (typeof scorecard.showModal === "function") scorecard.showModal();
    else scorecard.setAttribute("open", "open");
  });
  el("close-scorecard").addEventListener("click", () => {
    if (typeof scorecard.close === "function") scorecard.close();
    else scorecard.removeAttribute("open");
  });
  scorecard.addEventListener("close", () => el("open-scorecard").focus());
  for (const state of [scorecardSort, pickerSort]) {
    for (const key of Object.keys(state.heads)) {
      el(state.heads[key].control).addEventListener("click", () => sortBy(state, key));
    }
  }
  // The empty picker's way to a fix: the same sheet the top bar opens.
  el("picker-credentials").addEventListener("click", () => el("open-settings").click());
  el("gate-submit").addEventListener("click", () => void signIn());
  // Enter in either field submits. A login form where the password field does
  // nothing on Enter is a login form people think is broken.
  for (const hook of ["gate-username", "gate-password", "gate-token"]) {
    el(hook).addEventListener("keydown", (event) => {
      if (/** @type {KeyboardEvent} */ (event).key === "Enter") void signIn();
    });
  }
  el("sign-out").addEventListener("click", () => void signOut());
  // Saved defaults (674): the reset in the Tuning step, the notice's own
  // dismissal (persisted per dropped set, 686), "Update my defaults" beside
  // it, and a failure note that ends when the box is touched.
  el("defaults-reset").addEventListener("click", () => void confirmResetDefaults());
  el("defaults-dropped-close").addEventListener("click", () => {
    store.defaultsHidden = true;
    rememberDismissedDrop(droppedHash(store.defaultsDropped));
    el("defaults-dropped").hidden = true;
  });
  el("defaults-update").addEventListener("click", () => void updateDefaults());
  input("save-defaults").addEventListener("change", () => {
    store.defaultsNote = null;
    renderSaveDefaults();
  });
  el("add-account").addEventListener("click", () => void addAccount());
  el("change-password").addEventListener("click", () => void changePassword());
  // The four standing fields in the credential sheet. Paired here rather than
  // where they are read, because a label with no `for` is a field a screen
  // reader announces as "edit text" and that is true from the moment the
  // markup exists, not from the first click.
  //
  // These calls did nothing until the markup changed under them: the `for` was
  // being written onto a `<span>`, where the attribute is inert, and what was
  // actually tying each label to its field was the `<label>` wrapped around
  // both. The spans are now real `<label>` elements and visible, which is the
  // operator's report -- *"there are two unlabeled fields. I suppose that is
  // username and password or similar"* -- and the hidden defect behind it.
  associate(el("new-account-name-label"), input("new-account-name"));
  associate(el("new-account-password-label"), input("new-account-password"));
  associate(el("current-password-label"), input("current-password"));
  associate(el("new-password-label"), input("new-password"));
  wireLayout();
}

/**
 * Read the server, render the page.
 *
 * The catalogue is fetched first and everything else waits for it, because
 * every sentence below this line comes out of it -- including the one that
 * says the configuration could not be read. Two attempts: the tag this
 * browser was told to use, then, if that catalogue is not on this server any
 * more, whatever `Accept-Language` negotiates. A stale choice in
 * `localStorage` for a language a later version dropped would otherwise be a
 * page that never loads, fixable only by clearing site data.
 *
 * Both attempts failing is not fatal either. `index.html` carries the English
 * text of every static string beside its key, so a page with no catalogue is
 * a page that reads in the reference language with the dynamic parts empty --
 * which is what it already did with the script blocked.
 */
async function boot() {
  try {
    await loadLocale(storedLocale());
  } catch (error) {
    try {
      await loadLocale("");
    } catch (second) {
      rememberLocale("");
    }
  }
  applyStrings();
  renderPill("loading");
  renderLocalePicker();
  wire();
  // Before the catalogue and before `/health`, because on a server with
  // accounts every other route answers 401 until this one has been answered.
  await refreshSession();
  if (gated()) {
    showGate();
    return;
  }
  await start();
}

/**
 * Everything behind the gate. Called by `boot` and again after a sign-in.
 *
 * Split out of `boot` rather than inlined twice, because the two callers have
 * to load the same things in the same order: the first version of this
 * re-fetched the catalogue after a login and not the history, so a user who
 * signed in saw an empty run list until they reloaded the page.
 */
async function start() {
  hideGate();
  await refreshHealth();
  try {
    store.config = await getJson(ROUTES.config);
  } catch (error) {
    say("bad", t("word.unconfigured"), t("error.config", { detail: describe(error) }));
    renderPill("unreachable");
    return;
  }
  // Saved defaults first, then the server's for anything missing (674): the
  // store is filled before `renderControls`, whose renderers keep any value
  // they offer. Once per page, so a second sign-in keeps what was set since.
  await loadDefaults();
  if (!store.defaultsApplied) {
    applyDefaults(store.defaults);
    store.defaultsApplied = true;
  }
  renderControls();
  while (store.docs.length < minDocuments()) addDocument();
  // `addDocument` opens the pane it just made, which is what a click should do
  // and the wrong answer for the seeding loop above: it left the page opening
  // on the last pane it created, so a fresh page showed document 2 and the
  // operator typed their first source into their second document.
  store.active = 0;
  renderDocuments();
  void refreshHistory();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => void boot());
} else {
  void boot();
}
