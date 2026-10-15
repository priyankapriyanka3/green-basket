import { afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';

// Cleanup after each test case
afterEach(() => {
  cleanup();
  localStorage.clear();
});

// Mock window.location for tests that need it
Object.defineProperty(window, 'location', {
  value: {
    href: 'http://localhost:3000',
    origin: 'http://localhost:3000',
    pathname: '/',
    replace: vi.fn(),
    reload: vi.fn(),
  },
  writable: true,
});

// Mock console methods to reduce test noise
global.console = {
  ...console,
  error: vi.fn(),
  warn: vi.fn(),
};
