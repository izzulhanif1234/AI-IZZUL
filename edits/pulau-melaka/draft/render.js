// Render draft frames to JPG: node render.js [f1 f2 ...]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : Array.from({length: 10}, (_, i) => 'f' + (i + 1));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(__dirname, 'frames.html'));
  await page.evaluate(() => document.fonts.ready);
  for (const id of ids) {
    await page.evaluate(h => { location.hash = h; }, id);
    await page.waitForTimeout(250);
    await page.screenshot({ path: path.join(__dirname, 'out', id + '.jpg'), type: 'jpeg', quality: 90 });
    console.log('saved', id);
  }
  await browser.close();
})();
