import { test, expect } from './_pipeline_guard';

test.describe('Protected Routes', () => {
  // Setup: Login before each test
  test.beforeEach(async ({ page, context }) => {
    const response = await context.request.post('http://127.0.0.1:9420/api/v1/auth/login', {
      data: {
        phone_number: '+919876543210',
        otp_or_password: 'Demo@123',
        role_hint: 'shopper'
      }
    });
    
    const data = await response.json();
    const token = data.access_token;
    
    await context.addInitScript((token) => {
      localStorage.setItem('greenbasket_token', token);
    }, token);
  });

  test('should visit /shop (Home)', async ({ page }) => {
    await page.goto('/shop');
    await page.waitForLoadState('networkidle');
    
    // Check for page content - products, categories, or heading
    const hasContent = await page.locator('h1, h2, .product, [class*="product"], [class*="category"]').first().isVisible({ timeout: 10000 });
    expect(hasContent).toBeTruthy();
  });

  test('should visit /shop/categories (Category Search)', async ({ page }) => {
    await page.goto('/shop/categories');
    await page.waitForLoadState('networkidle');
    
    // Check for categories or search interface
    const hasContent = await page.locator('h1, h2, .category, [class*="category"], input[type="search"], input[placeholder*="search" i]').first().isVisible({ timeout: 10000 });
    expect(hasContent).toBeTruthy();
  });

  test('should visit /shop/cart (Cart)', async ({ page }) => {
    await page.goto('/shop/cart');
    await page.waitForLoadState('networkidle');
    
    // Cart page should show either items or empty cart message
    const hasContent = await page.locator('h1, h2, .cart, [class*="cart"], button').first().isVisible({ timeout: 10000 });
    expect(hasContent).toBeTruthy();
  });

  test('should visit /shop/checkout (Checkout)', async ({ page }) => {
    await page.goto('/shop/checkout');
    await page.waitForLoadState('networkidle');
    
    // Checkout page should have form or content
    const hasContent = await page.locator('h1, h2, form, button').first().isVisible({ timeout: 10000 });
    expect(hasContent).toBeTruthy();
  });

  test('should visit /planner/lists (Shopping Lists)', async ({ page }) => {
    await page.goto('/planner/lists');
    await page.waitForLoadState('networkidle');
    
    // Should show lists or option to create lists
    const hasContent = await page.locator('h1, h2, button, .list, [class*="list"]').first().isVisible({ timeout: 10000 });
    expect(hasContent).toBeTruthy();
  });

  test('should visit /account (Profile)', async ({ page }) => {
    await page.goto('/account');
    await page.waitForLoadState('networkidle');
    
    // Should show profile information
    const hasContent = await page.locator('h1, h2, .profile, [class*="profile"], button').first().isVisible({ timeout: 10000 });
    expect(hasContent).toBeTruthy();
  });

  test('should visit /account/notifications (Notifications)', async ({ page }) => {
    await page.goto('/account/notifications');
    await page.waitForLoadState('networkidle');
    
    // Should show notifications or empty state
    const hasContent = await page.locator('h1, h2, .notification, [class*="notification"]').first().isVisible({ timeout: 10000 });
    expect(hasContent).toBeTruthy();
  });

  test('should visit /account/loyalty (Loyalty)', async ({ page }) => {
    await page.goto('/account/loyalty');
    await page.waitForLoadState('networkidle');
    
    // Should show loyalty points or rewards
    const hasContent = await page.locator('h1, h2, .loyalty, [class*="loyalty"], [class*="points"]').first().isVisible({ timeout: 10000 });
    expect(hasContent).toBeTruthy();
  });

  test('should visit /account/orders (Orders)', async ({ page }) => {
    await page.goto('/account/orders');
    await page.waitForLoadState('networkidle');
    
    // Should show orders list or empty state
    const hasContent = await page.locator('h1, h2, .order, [class*="order"]').first().isVisible({ timeout: 10000 });
    expect(hasContent).toBeTruthy();
  });
});
