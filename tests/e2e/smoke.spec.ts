import { test, expect } from '@playwright/test';

test('VitePress homepage renders and has expected title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/.+/);
});

test('journey-traceability docs page loads', async ({ page }) => {
  const response = await page.goto('/operations/journey-traceability');
  expect(response?.status()).toBe(200);
  await expect(page.locator('main, .VPDoc, article').first()).toBeVisible();
});
