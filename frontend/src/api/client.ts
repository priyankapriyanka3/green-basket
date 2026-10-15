import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import type { ApiError } from './types';

// Base URL: relative /api for same-origin access (proxy in dev, nginx in production)
const BASE_URL = import.meta.env.VITE_API_URL ?? '/api';
const API_VERSION = '/v1';

// JWT token storage key
const TOKEN_KEY = 'greenbasket_token';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL + API_VERSION,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor: add JWT token to Authorization header
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor: handle errors and retry 5xx
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiError>) => {
    const originalRequest = error.config;

    // Handle 401: clear token and redirect to login
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }

    // Handle 5xx: retry once
    if (
      error.response?.status &&
      error.response.status >= 500 &&
      originalRequest &&
      !(originalRequest as any)._retry
    ) {
      (originalRequest as any)._retry = true;
      return apiClient(originalRequest);
    }

    // Parse unified error envelope
    if (error.response?.data?.error) {
      const apiError = error.response.data.error;
      return Promise.reject({
        code: apiError.code,
        message: apiError.message,
        traceId: apiError.traceId,
        details: apiError.details,
        status: error.response.status,
      });
    }

    return Promise.reject({
      code: 'UNKNOWN_ERROR',
      message: error.message || 'An unexpected error occurred',
      status: error.response?.status || 0,
    });
  }
);

// Token management utilities
export const tokenManager = {
  getToken: (): string | null => {
    return localStorage.getItem(TOKEN_KEY);
  },
  
  setToken: (token: string): void => {
    localStorage.setItem(TOKEN_KEY, token);
  },
  
  removeToken: (): void => {
    localStorage.removeItem(TOKEN_KEY);
  },
  
  isTokenExpired: (): boolean => {
    const token = tokenManager.getToken();
    if (!token) return true;
    
    try {
      // Parse JWT payload (simple base64 decode)
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expiryTime = payload.exp * 1000; // Convert to milliseconds
      return Date.now() >= expiryTime;
    } catch {
      return true;
    }
  },
};

export { apiClient };
export default apiClient;
