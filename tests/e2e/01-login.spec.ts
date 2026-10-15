import { test, expect } from './_pipeline_guard';

test.describe('Authentication', () => {
  test('should login through the form with seed credentials', async ({ page }) => {
    // Navigate to login page
    await page.goto('/login');
    
    // Verify we're on the login page
    await expect(page).toHaveURL(/\/login/);
    
    // Fill in the login form with seed credentials (10-digit phone without +91 prefix)
    await page.fill('#phone', '9876543210');
    await page.fill('#secret', 'Demo@123');
    
    // Submit the form
    await page.click('button[type="submit"]');
    
    // Wait for navigation away from login page
    await page.waitForURL(url => !url.pathname.includes('/login'), { timeout: 10000 });
    
    // Wait for the page to fully load
    await page.waitForLoadState('networkidle');
    
    // Verify we're logged in by checking we're on a protected page
    const currentUrl = page.url();
    expect(currentUrl).not.toContain('/login');
    
    // Verify we can see some content indicating we're logged in
    // Looking for common elements like navigation, user profile, or page headings
    await expect(page.locator('h1, h2, nav, [role="navigation"]').first()).toBeVisible({ timeout: 10000 });
  });
  
  test('should fail login with invalid credentials', async ({ page, apiGuard }) => {
    // Allow 401 for invalid login
    apiGuard.allow(401, '/api/v1/auth/login');
    
    await page.goto('/login');
    
    await page.fill('#phone', '9876543210');
    await page.fill('#secret', 'WrongPassword');
    
    await page.click('button[type="submit"]');
    
    // Should still be on login page or show error
    await page.waitForTimeout(2000);
    const currentUrl = page.url();
    expect(currentUrl).toContain('/login');
  });
  
  test('should logout successfully', async ({ page, context }) => {
    // Login first via API
    const response = await context.request.post('http://127.0.0.1:9420/api/v1/auth/login', {
      data: {
        phone_number: '+919876543210',
        otp_or_password: 'Demo@123',
        role_hint: 'shopper'
      }
    });
    
    const data = await response.json();
    const token = data.access_token;
    
    // Set token in localStorage
    await context.addInitScript((token) => {
      localStorage.setItem('greenbasket_token', token);
    }, token);
    
    // Navigate to a protected page
    await page.goto('/shop');
    await page.waitForLoadState('networkidle');
    
    // Find and click logout button
    const logoutButton = page.locator('button:has-text("logout"), button:has-text("sign out"), a:has-text("logout"), a:has-text("sign out")').first();
    
    // Assert the button exists before clicking
    await expect(logoutButton).toBeVisible({ timeout: 5000 });
    await logoutButton.click();
    
    // Should redirect to login
    await page.waitForURL(/\/login/, { timeout: 10000 });
    await expect(page).toHaveURL(/\/login/);
  });
});
