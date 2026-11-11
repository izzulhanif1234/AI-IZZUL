// Render storyboard.html pages to JPG: node scripts/spd_storyboard_render.js <dir>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = path.resolve(process.argv[2]);
  const b = await chromium.launch({ args: ['--proxy-server=' + (process.env.HTTPS_PROXY || 'direct://'), '--ignore-certificate-errors'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await p.goto('file://' + dir + '/storyboard.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  console.log(await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight).join(', ')));
  const names = { p1: '01-timeline', p2: '02-storyboard-S01-S10', p3: '03-storyboard-S11-S19', p4: '04-spd2-laman-utama' };
  for (const [id, n] of Object.entries(names)) {
    await p.locator('#' + id).screenshot({ path: path.join(dir, n + '.jpg'), type: 'jpeg', quality: 88 });
  }
  await b.close();
})();
