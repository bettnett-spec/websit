const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  let hasErrors = false;

  page.on('response', response => {
    if (response.status() >= 400 && response.status() < 600) {
       const url = response.url();
       if (!url.includes('index.css') && !url.includes('index.tsx') && !url.includes('favicon.ico')) {
           console.error(`Failed to load resource: ${url} (status: ${response.status()})`);
           hasErrors = true;
       }
    }
  });

  page.on('console', msg => {
    if (msg.type() === 'error') {
      const text = msg.text();
      if (!text.includes('404') && !text.includes('Failed to load resource')) {
         console.error(`Page error: ${text}`);
         hasErrors = true;
      }
    }
  });

  console.log('Loading shooter.html...');
  await page.goto('http://localhost:8000/shooter.html');
  await page.waitForTimeout(3000); // wait for initial load

  console.log('Loading platformer.html...');
  await page.goto('http://localhost:8000/platformer.html');
  await page.waitForTimeout(3000); // wait for initial load

  await browser.close();

  if (hasErrors) {
    console.error('Tests failed due to page errors.');
    process.exit(1);
  } else {
    console.log('Tests passed! No errors detected.');
    process.exit(0);
  }
})();
