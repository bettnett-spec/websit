const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
    const page = await browser.newPage();
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

    await page.goto('http://localhost:8126/shooter.html', { waitUntil: 'load' });

    // wait for loader to vanish
    await page.waitForFunction(() => {
        const loader = document.getElementById('loader');
        return !loader || loader.style.opacity === '0' || getComputedStyle(loader).display === 'none';
    }, {timeout: 10000});

    console.log("Loader vanished successfully!");

    await browser.close();
})();
