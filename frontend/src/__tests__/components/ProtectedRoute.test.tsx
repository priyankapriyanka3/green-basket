import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ProtectedRoute } from '../../components/ProtectedRoute';
import { AuthProvider } from '../../contexts/AuthContext';

// Mock the useAuth hook
vi.mock('../../contexts/AuthContext', async () => {
  const actual = await vi.importActual('../../contexts/AuthContext');
  return {
    ...actual,
    useAuth: vi.fn(),
  };
});

import { useAuth } from '../../contexts/AuthContext';

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('ProtectedRoute', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading state when checking authentication', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      isAuthenticated: false,
      isLoading: true,
      login: vi.fn(),
      logout: vi.fn(),
    });

    renderWithRouter(
      <ProtectedRoute>
        <div>Protected content</div>
      </ProtectedRoute>
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('redirects to login when not authenticated', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
    });

    renderWithRouter(
      <ProtectedRoute>
        <div>Protected content</div>
      </ProtectedRoute>
    );

    // Navigate is rendered, so protected content should not be visible
    expect(screen.queryByText('Protected content')).not.toBeInTheDocument();
  });

  it('renders children when authenticated as shopper', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: {
        userId: 'cust-001',
        role: 'shopper',
        displayName: 'Test User',
        preferredLanguage: 'en-IN',
      },
      isAuthenticated: true,
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
    });

    renderWithRouter(
      <ProtectedRoute>
        <div>Protected content</div>
      </ProtectedRoute>
    );

    expect(screen.getByText('Protected content')).toBeInTheDocument();
  });

  it('shows 403 error when shopper tries to access operator-only route', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: {
        userId: 'cust-001',
        role: 'shopper',
        displayName: 'Test User',
        preferredLanguage: 'en-IN',
      },
      isAuthenticated: true,
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
    });

    renderWithRouter(
      <ProtectedRoute requiredRole="operator">
        <div>Operator content</div>
      </ProtectedRoute>
    );

    expect(screen.getByText('403')).toBeInTheDocument();
    expect(screen.getByText('Access Forbidden')).toBeInTheDocument();
    expect(screen.queryByText('Operator content')).not.toBeInTheDocument();
  });

  it('renders children when operator accesses operator-only route', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: {
        userId: 'cust-002',
        role: 'operator',
        displayName: 'Operator User',
        preferredLanguage: 'en-IN',
      },
      isAuthenticated: true,
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
    });

    renderWithRouter(
      <ProtectedRoute requiredRole="operator">
        <div>Operator content</div>
      </ProtectedRoute>
    );

    expect(screen.getByText('Operator content')).toBeInTheDocument();
  });
});
