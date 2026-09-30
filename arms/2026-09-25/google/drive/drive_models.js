// Drives the real claimcheck page in headless Chromium against the server
// serve_for_drive.py started, per memory/driving-the-web-ui-in-a-browser.md.
//
// Checks, for DECISIONS 625 (the Gemini rows), in English and German, read
// back from the rendered table's text:
//   - the Gemini 3.5 Flash-Lite row is present, dated with its commit, and its
//     cost cell reads the free-tier word: never "$0", never "unmeasured";
//   - the Gemini 3.8 Flash row is present, unmeasured, with no date line;
//   - with the Google provider configured (DRIVE_PROVIDERS), both are pickable;
//   - the GPT-6 and Opus 5.5 rows still carry their own dates (must-not-fire);
//   - no horizontal overflow at 380px, and no page error, console error or
//     failed request across the whole drive.
const puppeteer = require("<home>/node_modules/puppeteer-core");

const URL = process.argv[2];
if (!URL) { console.error("usage: node drive_models.js <url>"); process.exit(2); }

const WANT = {
  en: { lite: "measured 2026-09-25, claimcheck 0771aa6", vendor: "measured 2026-09-25, claimcheck ff8ff77",
        free: "free tier", unmeasured: "unmeasured" },
  de: { lite: "gemessen am 2026-09-25, claimcheck 0771aa6", vendor: "gemessen am 2026-09-25, claimcheck ff8ff77",
        free: "kostenlose Stufe", unmeasured: "nicht gemessen" },
};

async function rows(page) {
  return page.evaluate(() => Array.from(document.querySelectorAll('[data-cc="model-rows"] tr')).map((tr) => ({
    text: tr.innerText.replace(/\s+/g, " ").trim(),
    when: (tr.querySelector(".measured-when") || {}).textContent || "",
    free: (tr.querySelector("td.freetier") || {}).textContent || "",
    useDisabled: Boolean((tr.querySelector('input[name="model-use"]') || {}).disabled),
  })));
}

async function main() {
  const errors = { pageerror: [], console: [], requestfailed: [] };
  const browser = await puppeteer.launch({
    executablePath: "/usr/bin/chromium", headless: "new", args: ["--no-sandbox", "--disable-gpu"],
  });
  const report = {};
  const problems = [];
  try {
    const page = await browser.newPage();
    page.on("pageerror", (e) => errors.pageerror.push(String(e)));
    page.on("console", (msg) => { if (msg.type() === "error") errors.console.push(msg.text()); });
    page.on("requestfailed", (req) =>
      errors.requestfailed.push(`${req.url()} ${req.failure() && req.failure().errorText}`));
    await page.setViewport({ width: 1280, height: 900 });
    await page.goto(URL, { waitUntil: "networkidle0", timeout: 30000 });
    await page.waitForSelector('[data-cc="model-rows"] tr', { timeout: 15000 });

    for (const tag of ["en", "de"]) {
      if (tag === "de") {
        await page.select("#locale-select", "de");
        await page.waitForFunction(() => document.documentElement.lang === "de", { timeout: 10000 });
        await page.waitForSelector('[data-cc="model-rows"] tr', { timeout: 15000 });
      }
      const got = await rows(page);
      report[tag] = got.filter((r) => /gemini|gpt-6-sol|claude-opus-5-5/.test(r.text));
      const want = WANT[tag];
      const find = (needle) => got.filter((r) => r.text.includes(needle));
      const lite = find("gemini-3.5-flash-lite")[0];
      if (!lite) problems.push(`${tag}: no Flash-Lite row`);
      else {
        if (lite.when !== want.lite) problems.push(`${tag}: Flash-Lite date line ${JSON.stringify(lite.when)}`);
        if (lite.free !== want.free) problems.push(`${tag}: Flash-Lite cost cell ${JSON.stringify(lite.free)}`);
        if (lite.text.includes("$0")) problems.push(`${tag}: Flash-Lite shows a dollar zero`);
        if (lite.text.includes(want.unmeasured)) problems.push(`${tag}: Flash-Lite reads unmeasured`);
        if (process.env.DRIVE_PROVIDERS && lite.useDisabled) problems.push(`${tag}: Flash-Lite cannot be picked`);
      }
      const flash = find("gemini-3.8-flash")[0];
      if (!flash) problems.push(`${tag}: no 3.8 Flash row`);
      else {
        if (flash.when) problems.push(`${tag}: 3.8 Flash has a date line ${JSON.stringify(flash.when)}`);
        if (!flash.text.includes(want.unmeasured)) problems.push(`${tag}: 3.8 Flash does not read unmeasured`);
        if (flash.free) problems.push(`${tag}: 3.8 Flash carries the free-tier word`);
        if (process.env.DRIVE_PROVIDERS && flash.useDisabled) problems.push(`${tag}: 3.8 Flash cannot be picked`);
      }
      for (const id of ["gpt-6-sol", "claude-opus-5-5"]) {
        const row = find(id)[0];
        if (!row || row.when !== want.vendor) problems.push(`${tag}: ${id} date line changed`);
        if (row && row.free) problems.push(`${tag}: ${id} carries the free-tier word`);
      }
      if (got.filter((r) => r.free).length !== 1) problems.push(`${tag}: free-tier word on ${got.filter((r) => r.free).length} rows`);

      await page.setViewport({ width: 380, height: 900 });
      await new Promise((r) => setTimeout(r, 100));
      const widths = await page.evaluate(() => ({
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
      }));
      report[`${tag}_380`] = widths;
      if (widths.scrollWidth > widths.clientWidth + 1)
        problems.push(`${tag}: horizontal overflow at 380px: ${JSON.stringify(widths)}`);
      await page.setViewport({ width: 1280, height: 900 });
    }
  } finally {
    await browser.close();
  }
  if (errors.pageerror.length) problems.push(`page errors: ${JSON.stringify(errors.pageerror)}`);
  if (errors.console.length) problems.push(`console errors: ${JSON.stringify(errors.console)}`);
  if (errors.requestfailed.length) problems.push(`failed requests: ${JSON.stringify(errors.requestfailed)}`);
  console.log(JSON.stringify({ report, errors, problems }, null, 1));
  if (problems.length) { console.error("PROBLEMS:\n" + problems.join("\n")); process.exitCode = 1; }
  else console.error("ALL CLEAR");
}

main().catch((err) => { console.error(err); process.exitCode = 1; });
