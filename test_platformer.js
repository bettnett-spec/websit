const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
  page.on('pageerror', err => console.log('BROWSER ERROR:', err));

  await page.goto('http://localhost:8000/platformer.html');
  await page.waitForTimeout(2000);

  // Click start game / instructions to trigger initialization
  await page.click('#instructions');

  await page.waitForTimeout(3000);
  await browser.close();
})();
