const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    let success = true;

    async function checkPage(url) {
        const page = await browser.newPage();
        const errors = [];
        page.on('pageerror', err => {
            console.error(`Page error on ${url}: ${err.message}`);
            errors.push(err);
        });

        console.log(`Checking ${url}...`);
        await page.goto(url, { waitUntil: 'networkidle' });

        // Wait a bit to let any asynchronous initialization (like Three.js scripts) run
        await page.waitForTimeout(3000);

        if (errors.length > 0) {
            console.error(`❌ Errors found on ${url}`);
            success = false;
        } else {
            console.log(`✅ No errors found on ${url}`);
        }
        await page.close();
    }

    await checkPage('http://localhost:8000/shooter.html');
    await checkPage('http://localhost:8000/platformer.html');

    await browser.close();
    if (!success) {
        process.exit(1);
    }
})();
