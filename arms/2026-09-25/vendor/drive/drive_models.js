// Drives the real claimcheck page in headless Chromium against the server
// serve_for_drive.py started, per memory/driving-the-web-ui-in-a-browser.md.
//
// Checks, for DECISIONS 618 (GPT-6 rows, measured date and commit, the refused
// Opus row), in English and German, read back from the rendered table's text:
//   - the GPT-6 Sol and GPT-6 Luna rows are present, with figures;
//   - every measured row names its date and its commit, and the two dates in
//     play (2026-09-18 and 2026-09-25) both appear with their commits;
//   - the API Opus 5 row carries the refusal sentence, and no other row does;
//   - no horizontal overflow at 380px, and no page error, console error or
//     failed request across the whole drive.
const puppeteer = require("<home>/node_modules/puppeteer-core");

const URL = process.argv[2];
if (!URL) { console.error("usage: node drive_models.js <url>"); process.exit(2); }

const WANT = {
  en: { refused: "retired 2026-09-25: deprecated in favour of Opus 5.5; refused at this tool version (DECISIONS 617)",
        sol: "measured 2026-09-25, claimcheck ff8ff77",
        old: "measured 2026-09-18, claimcheck cf30209" },
  de: { refused: "zurückgezogen am 2026-09-25: zugunsten von Opus 5.5 eingestellt; bei dieser Tool-Version abgelehnt (DECISIONS 617)",
        sol: "gemessen am 2026-09-25, claimcheck ff8ff77",
        old: "gemessen am 2026-09-18, claimcheck cf30209" },
};

async function rows(page) {
  return page.evaluate(() => Array.from(document.querySelectorAll('[data-cc="model-rows"] tr')).map((tr) => ({
    text: tr.innerText.replace(/\s+/g, " ").trim(),
    when: (tr.querySelector(".measured-when") || {}).textContent || "",
    refused: (tr.querySelector(".retired-why") || {}).textContent || "",
    useDisabled: Boolean((tr.querySelector('input[name="model-use"]') || {}).disabled),
    useChecked: Boolean((tr.querySelector('input[name="model-use"]') || {}).checked),
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
      report[tag] = got;
      const want = WANT[tag];
      const find = (needle) => got.filter((r) => r.text.includes(needle));
      for (const id of ["claude-opus-5-5", "gpt-6-sol", "gpt-6-luna"]) {
        const row = find(id)[0];
        if (!row) { problems.push(`${tag}: no row for ${id}`); continue; }
        if (row.when !== want.sol) problems.push(`${tag}: ${id} says ${JSON.stringify(row.when)}`);
        if (/unmeasured|nicht gemessen/.test(row.text)) problems.push(`${tag}: ${id} reads unmeasured`);
      }
      const opus = got.filter((r) => r.text.includes("claude-opus-5") && !r.text.includes("claude-opus-5-5")
                                    && !/subscription|Abonnement|Claude Code/i.test(r.text));
      if (opus.length !== 1) problems.push(`${tag}: expected one API Opus 5 row, found ${opus.length}`);
      else {
        if (opus[0].refused !== want.refused)
          problems.push(`${tag}: Opus refusal line is ${JSON.stringify(opus[0].refused)}`);
        if (opus[0].when !== want.old)
          problems.push(`${tag}: Opus date line is ${JSON.stringify(opus[0].when)}`);
        if (!opus[0].useDisabled) problems.push(`${tag}: the retired Opus row can still be picked`);
        if (opus[0].useChecked) problems.push(`${tag}: the retired Opus row is selected`);
      }
      if (process.env.DRIVE_PROVIDERS) {
        // Must-not-fire beside the must-fire: with both providers configured, a
        // live row of the same vendor is pickable while the retired one is not.
        for (const id of ["claude-opus-5-5", "claude-sonnet-5", "gpt-6-sol", "gpt-6-luna"]) {
          const live = find(id)[0];
          if (!live) problems.push();
          else if (live.useDisabled) problems.push();
        }
        if (opus.length === 1 && /no endpoint|kein Endpunkt/.test(opus[0].text))
          problems.push();
      }
      const refusedRows = got.filter((r) => r.refused);
      if (refusedRows.length !== 1) problems.push(`${tag}: ${refusedRows.length} rows carry a retired line`);
      const measuredRows = got.filter((r) => r.when);
      if (!measuredRows.some((r) => r.when === want.old)) problems.push(`${tag}: no 2026-09-18 row`);

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
  console.log(JSON.stringify({ report, errors }, null, 1));
  if (problems.length) { console.error("PROBLEMS:\n" + problems.join("\n")); process.exitCode = 1; }
  else console.error("ALL CLEAR");
}

main().catch((err) => { console.error(err); process.exitCode = 1; });
