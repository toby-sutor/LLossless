// Drives the real page: a typed id naming the retired claude-opus-5 row warns
// before submit (field and run bar) and does not block; a live id does not warn.
// English and German, read back from the rendered text.
const puppeteer = require("<home>/node_modules/puppeteer-core");
const URL = process.argv[2];
const WANT = {
  en: "Warning: claude-opus-5, retired 2026-09-25: deprecated in favour of Opus 5.5; refused at this tool version (DECISIONS 617). Use Opus 5.5 instead. The run is not blocked and goes out as typed.",
  de: "Warnung: claude-opus-5, zurückgezogen am 2026-09-25: zugunsten von Opus 5.5 eingestellt; bei dieser Tool-Version abgelehnt (DECISIONS 617). Verwenden Sie stattdessen Opus 5.5. Der Lauf wird nicht blockiert und so gesendet, wie eingegeben.",
};
async function state(page) {
  return page.evaluate(() => {
    const q = (h) => document.querySelector('[data-cc="' + h + '"]');
    const vis = (n) => Boolean(n && !n.hidden && n.offsetParent !== null);
    return {
      field: { visible: vis(q("custom-model-retired")), text: q("custom-model-retired").innerText.trim() },
      runbar: { visible: vis(q("submit-retired-warning")), text: q("submit-retired-warning").innerText.trim() },
      note: q("custom-model-note").innerText.trim(),
      submitDisabled: q("submit").disabled,
      status: q("status-text").innerText.trim(),
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    };
  });
}
async function type(page, text) {
  await page.$eval('[data-cc="custom-model"]', (n) => { n.value = ""; });
  await page.type('[data-cc="custom-model"]', text);
  await new Promise((r) => setTimeout(r, 150));
}
(async () => {
  const errors = { pageerror: [], console: [], requestfailed: [] };
  const problems = [];
  const report = {};
  const browser = await puppeteer.launch({ executablePath: "/usr/bin/chromium", headless: "new", args: ["--no-sandbox", "--disable-gpu"] });
  try {
    const page = await browser.newPage();
    page.on("pageerror", (e) => errors.pageerror.push(String(e)));
    page.on("console", (m) => { if (m.type() === "error") errors.console.push(m.text()); });
    page.on("requestfailed", (r) => errors.requestfailed.push(r.url() + " " + (r.failure() && r.failure().errorText)));
    await page.setViewport({ width: 1280, height: 900 });
    await page.goto(URL, { waitUntil: "networkidle0", timeout: 30000 });
    await page.waitForSelector('[data-cc="model-rows"] tr', { timeout: 15000 });
    const posts = [];
    page.on("request", (r) => { if (r.method() === "POST") posts.push({ url: r.url(), body: r.postData() || "" }); });
    // Two documents, so the only thing that could disable the button is the id.
    const areas = await page.$$('[data-cc="doc-text"]');
    report.docAreas = areas.length;
    let n = 0;
    for (const area of areas) {
      n += 1;
      await area.evaluate((x, k) => { x.value = "Doc " + k + " says the dock opens at 9."; x.dispatchEvent(new Event("input", { bubbles: true })); }, n);
    }
    report.docValues = await page.$$eval('[data-cc="doc-text"]', (ns) => ns.map((x) => x.value.length));
    await new Promise((r) => setTimeout(r, 200));
    for (const tag of ["en", "de"]) {
      if (tag === "de") {
        await page.select("#locale-select", "de");
        await page.waitForFunction(() => document.documentElement.lang === "de", { timeout: 10000 });
        await new Promise((r) => setTimeout(r, 300));
      }
      const box = await page.$eval('[data-cc="custom-toggle"]', (n) => n.checked);
      if (!box) await page.click('[data-cc="custom-toggle"]');
      const before = await state(page);
      await type(page, "claude-opus-5");
      const retired = await state(page);
      await page.setViewport({ width: 380, height: 900 });
      await new Promise((r) => setTimeout(r, 150));
      const narrow = await state(page);
      await page.setViewport({ width: 1280, height: 900 });
      await type(page, "claude-opus-5-5");
      const live = await state(page);
      report[tag] = { before, retired, narrow, live };
      if (before.field.visible || before.runbar.visible) problems.push(tag + ": warning shown before anything was typed");
      for (const where of ["field", "runbar"]) {
        if (!retired[where].visible) problems.push(tag + ": " + where + " warning not visible for claude-opus-5");
        if (retired[where].text !== WANT[tag]) problems.push(tag + ": " + where + " text " + JSON.stringify(retired[where].text));
        if (live[where].visible || live[where].text) problems.push(tag + ": " + where + " warning fired for claude-opus-5-5");
      }
      if (retired.submitDisabled) problems.push(tag + ": submit is disabled for the retired id (must warn, not block)");
      if (live.submitDisabled !== retired.submitDisabled) problems.push(tag + ": submit state differs between retired and live ids");
      if (narrow.scrollWidth > narrow.clientWidth + 1) problems.push(tag + ": overflow at 380px " + narrow.scrollWidth);
      await page.$eval('[data-cc="custom-model"]', (n) => { n.value = ""; n.dispatchEvent(new Event("input")); });
    }
    // Not blocked: type the retired id once more and press the button. The
    // server's anthropic URL is anthropic.invalid, so nothing is billed.
    await page.click('[data-cc="custom-model"]');
    await type(page, "claude-opus-5");
    await page.click('[data-cc="submit"]');
    await new Promise((r) => setTimeout(r, 1500));
    report.posts = posts.map((p) => ({ url: p.url, carriesId: p.body.includes('"claude-opus-5"') }));
    if (!posts.some((p) => p.body.includes('"claude-opus-5"'))) problems.push("no submit carried claude-opus-5");
  } finally { await browser.close(); }
  for (const k of Object.keys(errors)) if (errors[k].length) problems.push(k + ": " + JSON.stringify(errors[k]));
  console.log(JSON.stringify({ report, errors }, null, 1));
  if (problems.length) { console.error("PROBLEMS:\n" + problems.join("\n")); process.exitCode = 1; } else console.error("ALL CLEAR");
})().catch((e) => { console.error(e); process.exitCode = 1; });
