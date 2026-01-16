import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should load dashboard page', async ({ page }) => {
    await expect(page).toHaveTitle(/Clawdbot Dashboard/);
  });

  test('should display session header', async ({ page }) => {
    await expect(page.getByText('Session Status')).toBeVisible();
    await expect(page.getByText('Session ID:')).toBeVisible();
  });

  test('should display tab navigation', async ({ page }) => {
    await expect(page.getByText('Overview')).toBeVisible();
    await expect(page.getByText('Tool Calls')).toBeVisible();
    await expect(page.getByText('Messages')).toBeVisible();
    await expect(page.getByText('Tasks')).toBeVisible();
  });

  test('should display search button', async ({ page }) => {
    const searchButton = page.getByText('Search');
    await expect(searchButton).toBeVisible();
  });

  test('should display refresh button', async ({ page }) => {
    const refreshButton = page.getByText('Refresh');
    await expect(refreshButton).toBeVisible();
  });

  test('should display export button', async ({ page }) => {
    const exportButton = page.getByText('Export');
    await expect(exportButton).toBeVisible();
  });

  test('should display session summary', async ({ page }) => {
    await expect(page.getByText('Session Summary')).toBeVisible();
    await expect(page.getByText('Tool Calls')).toBeVisible();
    await expect(page.getByText('Messages')).toBeVisible();
    await expect(page.getByText('Tasks')).toBeVisible();
  });

  test('should switch between tabs', async ({ page }) => {
    // Click on Tools tab
    await page.getByText('Tool Calls').click();
    await expect(page.getByText('Tool Call Stream')).toBeVisible();

    // Click on Messages tab
    await page.getByText('Messages').click();
    await expect(page.getByText('Message Stream')).toBeVisible();

    // Click on Tasks tab
    await page.getByText('Tasks').click();
    await expect(page.getByText('Task Tracker')).toBeVisible();

    // Return to Overview tab
    await page.getByText('Overview').click();
    await expect(page.getByText('Session Summary')).toBeVisible();
  });

  test('should toggle search bar', async ({ page }) => {
    // Open search bar
    await page.getByText('Search').click();
    await expect(page.getByPlaceholderText(/Search across all data/)).toBeVisible();

    // Close search bar
    await page.getByRole('button').filter({ hasText: /close/i }).first().click();
    await expect(page.getByPlaceholderText(/Search across all data/)).not.toBeVisible();
  });

  test('should enter search query', async ({ page }) => {
    // Open search bar
    await page.getByText('Search').click();

    // Enter search query
    const searchInput = page.getByPlaceholderText(/Search across all data/);
    await searchInput.fill('test query');

    // Check input has value
    await expect(searchInput).toHaveValue('test query');
  });

  test('should clear search query', async ({ page }) => {
    // Open search bar
    await page.getByText('Search').click();

    // Enter search query
    const searchInput = page.getByPlaceholderText(/Search across all data/);
    await searchInput.fill('test query');

    // Clear search
    await page.getByRole('button').filter({ hasText: /clear/i }).first().click();

    // Check input is empty
    await expect(searchInput).toHaveValue('');
  });

  test('should display connection status', async ({ page }) => {
    // Check for connection status indicator
    await expect(page.locator('[data-testid="connection-status"]')).toBeVisible();
  });
});

test.describe('Theme Toggle', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should toggle between light and dark mode', async ({ page }) => {
    // Find theme toggle button
    const themeButton = page.getByLabel(/toggle theme/i);

    // Click to toggle theme
    await themeButton.click();

    // Wait for theme change
    await page.waitForTimeout(500);

    // Verify theme changed (check for theme attribute on html)
    const html = page.locator('html');
    const initialTheme = await html.getAttribute('class');
    expect(initialTheme).toContain('dark');

    // Toggle back
    await themeButton.click();
    await page.waitForTimeout(500);

    const newTheme = await html.getAttribute('class');
    expect(newTheme).not.toContain('dark');
  });
});

test.describe('Responsive Design', () => {
  test('should work on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    // Check key elements are visible on mobile
    await expect(page.getByText('Session Status')).toBeVisible();
    await expect(page.getByText('Overview')).toBeVisible();
  });

  test('should work on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');

    // Check key elements are visible on tablet
    await expect(page.getByText('Session Status')).toBeVisible();
    await expect(page.getByText('Overview')).toBeVisible();
  });

  test('should work on desktop viewport', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/');

    // Check key elements are visible on desktop
    await expect(page.getByText('Session Status')).toBeVisible();
    await expect(page.getByText('Overview')).toBeVisible();
  });
});
