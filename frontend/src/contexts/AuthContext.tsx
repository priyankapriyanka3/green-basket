import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { tokenManager } from '../api/client';
import apiClient from '../api/client';
import type { LoginRequest, LoginResponse } from '../api/types';

interface User {
  userId: string;
  role: 'shopper' | 'operator';
  displayName: string;
  preferredLanguage: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check token on app load
  useEffect(() => {
    const checkAuth = () => {
      const token = tokenManager.getToken();
      
      if (!token) {
        setIsLoading(false);
        return;
      }

      // Check if token is expired
      if (tokenManager.isTokenExpired()) {
        tokenManager.removeToken();
        setUser(null);
        setIsLoading(false);
        return;
      }

      // Parse user from token
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        
        // Extract user info from token (assuming standard JWT structure)
        // The actual structure depends on backend implementation
        const userData: User = {
          userId: payload.sub || '',
          role: payload.role || 'shopper',
          displayName: payload.name || 'User',
          preferredLanguage: payload.lang || 'en-IN',
        };
        
        setUser(userData);
      } catch (error) {
        console.error('Failed to parse token:', error);
        tokenManager.removeToken();
        setUser(null);
      }

      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (credentials: LoginRequest): Promise<void> => {
    try {
      // Transform camelCase to snake_case for API
      const apiPayload = {
        phone_number: credentials.phoneNumber,
        otp_or_password: credentials.otpOrPassword,
        role_hint: credentials.roleHint,
      };
      
      const response = await apiClient.post<any>('/auth/login', apiPayload);
      const apiResponse = response.data;
      
      // Transform snake_case to camelCase
      const accessToken = apiResponse.access_token;
      const userData = {
        userId: apiResponse.user.customer_id || apiResponse.user.operator_id,
        role: apiResponse.user.role,
        displayName: apiResponse.user.full_name,
        preferredLanguage: apiResponse.user.preferred_language || 'en',
      };

      // Store token
      tokenManager.setToken(accessToken);

      // Set user state
      setUser(userData);
    } catch (error) {
      // Re-throw for component-level error handling
      throw error;
    }
  };

  const logout = () => {
    tokenManager.removeToken();
    setUser(null);
    window.location.href = '/login';
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
