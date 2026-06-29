const { test, expect } = require('@playwright/test');

test('test platformer.html', async ({ page }) => {
  await page.goto('http://localhost:8000/platformer.html');
  await page.waitForTimeout(5000);
});
