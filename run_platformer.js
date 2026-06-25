const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
  page.on('pageerror', err => console.error('BROWSER ERROR:', err.message));

  console.log("Loading platformer.html...");
  await page.goto('http://localhost:8000/platformer.html');
  await page.waitForTimeout(5000);
  await page.screenshot({ path: 'platformer.png' });

  await browser.close();
})();
