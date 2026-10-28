// Render storyboard.html pages (#p1 storyboard, #p2 concise copy, #p3 cut plan, #p4 segment example, #p5 motion styles, #p6 boat journey) to full-page JPGs
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  for (const [hash, name] of [['p1', 'storyboard'], ['p2', 'teks-ringkas-16-pulau'], ['p3', 'pelan-potongan-video'], ['p4', 'contoh-segmen-pulau-undan'], ['p5', 'gaya-motion-grafik'], ['p6', 'draf-v4-perjalanan-bot']]) {
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    await page.goto('file://' + path.join(__dirname, 'storyboard.html') + '#' + hash);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(__dirname, 'out', name + '.jpg'), type: 'jpeg', quality: 88, fullPage: true });
    console.log('saved', name);
  }
  await browser.close();
})();
