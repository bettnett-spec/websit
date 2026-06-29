const { test, expect } = require('@playwright/test');

test('test shooter.html', async ({ page }) => {
  await page.goto('http://localhost:8000/shooter.html');
  await page.waitForTimeout(5000);
});
