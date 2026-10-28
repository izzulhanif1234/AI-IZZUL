// Capture journey.html at given timeline times: node render_journey.js name=t [name=t ...]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const shots = process.argv.slice(2).map(a => a.split('='));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(__dirname, 'journey.html'));
  await page.waitForTimeout(1000);
  for (const [name, t] of shots) {
    await page.evaluate(t => { window.tl.seek(t, false); }, parseFloat(t));
    await page.waitForTimeout(150);
    await page.screenshot({ path: path.join(__dirname, 'out', name + '.jpg'), type: 'jpeg', quality: 88 });
    console.log('saved', name, t);
  }
  await browser.close();
})();
