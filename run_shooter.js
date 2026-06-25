const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
  page.on('pageerror', err => console.error('BROWSER ERROR:', err.message));

  console.log("Loading shooter.html...");
  await page.goto('http://localhost:8000/shooter.html');
  await page.waitForTimeout(5000);

  // Try to start game
  await page.fill('#player-name-input', 'TestPlayer');
  await page.click('#start-game-btn');

  await page.waitForTimeout(5000);

  await page.screenshot({ path: 'shooter.png' });

  await browser.close();
})();
