// Low-res motion preview of journey.html: node preview_journey.js <from> <to> <fps> <out.mp4>
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
(async () => {
  const [from, to, fps, out] = [parseFloat(process.argv[2]), parseFloat(process.argv[3]), parseInt(process.argv[4]), process.argv[5]];
  const dir = path.join(__dirname, 'out', '.frames'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(__dirname, 'journey.html'));
  await page.waitForTimeout(1000);
  const n = Math.round((to - from) * fps);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => { window.tl.seek(t, false); }, from + i / fps);
    await page.screenshot({ path: path.join(dir, String(i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 80 });
  }
  await browser.close();
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(fps), '-i', path.join(dir, '%05d.jpg'), '-vf', 'scale=1280:720', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', out]);
  fs.rmSync(dir, { recursive: true, force: true });
  console.log('wrote', out, n, 'frames');
})();
