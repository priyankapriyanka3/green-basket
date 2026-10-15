import { describe, it, expect, beforeEach, vi } from 'vitest';
import { tokenManager } from '../../api/client';

describe('tokenManager', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  describe('getToken', () => {
    it('returns null when no token exists', () => {
      expect(tokenManager.getToken()).toBeNull();
    });

    it('returns token when it exists', () => {
      localStorage.setItem('greenbasket_token', 'test-token');
      expect(tokenManager.getToken()).toBe('test-token');
    });
  });

  describe('setToken', () => {
    it('stores token in localStorage', () => {
      tokenManager.setToken('new-token');
      expect(localStorage.getItem('greenbasket_token')).toBe('new-token');
    });
  });

  describe('removeToken', () => {
    it('removes token from localStorage', () => {
      localStorage.setItem('greenbasket_token', 'test-token');
      tokenManager.removeToken();
      expect(localStorage.getItem('greenbasket_token')).toBeNull();
    });
  });

  describe('isTokenExpired', () => {
    it('returns true when no token exists', () => {
      expect(tokenManager.isTokenExpired()).toBe(true);
    });

    it('returns true for expired token', () => {
      // Create a token that expired 1 hour ago
      const expiredTime = Math.floor(Date.now() / 1000) - 3600;
      const payload = { exp: expiredTime };
      const token = `header.${btoa(JSON.stringify(payload))}.signature`;
      
      localStorage.setItem('greenbasket_token', token);
      expect(tokenManager.isTokenExpired()).toBe(true);
    });

    it('returns false for valid token', () => {
      // Create a token that expires in 1 hour
      const futureTime = Math.floor(Date.now() / 1000) + 3600;
      const payload = { exp: futureTime };
      const token = `header.${btoa(JSON.stringify(payload))}.signature`;
      
      localStorage.setItem('greenbasket_token', token);
      expect(tokenManager.isTokenExpired()).toBe(false);
    });

    it('returns true for malformed token', () => {
      localStorage.setItem('greenbasket_token', 'invalid-token');
      expect(tokenManager.isTokenExpired()).toBe(true);
    });
  });
});
