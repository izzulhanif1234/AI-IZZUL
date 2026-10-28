// Capture film.html. Stills: node film_capture.js shots name=t ...   Video frames: node film_capture.js frames <from> <to> <fps> <dir>
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const [mode, ...rest] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(__dirname, 'film.html'));
  await page.waitForTimeout(1200);
  const grab = async (t, file, q) => {
    await page.evaluate(t => window.seekTo(t), t);
    await page.screenshot({ path: file, type: 'jpeg', quality: q });
  };
  if (mode === 'shots') {
    for (const a of rest) { const [n, t] = a.split('='); await grab(parseFloat(t), path.join(__dirname, 'out', n + '.jpg'), 88); console.log('saved', n, t); }
  } else {
    const [from, to, fps, dir] = [parseFloat(rest[0]), parseFloat(rest[1]), parseInt(rest[2]), rest[3]];
    fs.mkdirSync(dir, { recursive: true });
    const i0 = Math.round(from * fps), i1 = Math.round(to * fps);
    for (let i = i0; i < i1; i++) await grab(i / fps, path.join(dir, String(i).padStart(5, '0') + '.jpg'), 82);
    console.log('frames', i0, i1);
  }
  await browser.close();
})();
