const { test, expect } = require('@playwright/test');

test('home loads and shows Aku Workspace title', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('text=Aku Workspace')).toHaveCount(1);
});

test('can navigate to Data Insights and show cached/no data', async ({ page }) => {
  await page.goto('/');
  await page.click('text=Data');
  await expect(page.locator('text=Data Insights')).toHaveCount(1);
});
