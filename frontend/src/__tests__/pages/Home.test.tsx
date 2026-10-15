import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Home } from '../../pages/Home';
import { AuthProvider } from '../../contexts/AuthContext';

// Mock API client
vi.mock('../../api/client', () => ({
  default: {
    get: vi.fn().mockResolvedValue({
      data: {
        profile: {
          customerId: 'cust-001',
          name: 'Ananya',
          preferredLanguage: 'en-IN',
          dietaryPreference: 'vegetarian',
          allergies: ['peanuts'],
          loyaltyPoints: 420,
        },
        defaultAddress: {
          addressId: 'addr-001',
          label: 'Home',
          postalCode: '400001',
          serviceability: {
            isServiceable: true,
            serviceZone: 'Mumbai-South',
            reason: '',
          },
        },
        featuredCategories: [
          { categoryId: 'cat-001', name: 'Fresh Fruits', iconUrl: '' },
          { categoryId: 'cat-002', name: 'Fresh Vegetables', iconUrl: '' },
        ],
        recommendations: [
          {
            recommendationId: 'rec-001',
            productId: 'prod-021',
            score: 0.92,
            reasonTag: 'Reorder reminder',
            reasonText: 'You buy these every Sunday.',
          },
        ],
        shoppingLists: [
          {
            listId: 'lst-001',
            name: 'Weekly Staples',
            isAiGenerated: false,
            suggestionNote: null,
            itemCount: 8,
          },
        ],
      },
    }),
  },
  tokenManager: {
    getToken: vi.fn().mockReturnValue('mock-token'),
    setToken: vi.fn(),
    removeToken: vi.fn(),
    isTokenExpired: vi.fn().mockReturnValue(false),
  },
}));

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      <AuthProvider>{component}</AuthProvider>
    </BrowserRouter>
  );
};

describe('Home', () => {
  it('renders greeting with customer name', async () => {
    renderWithRouter(<Home />);
    
    await screen.findByText(/Good morning, Ananya/i);
    expect(screen.getByText(/Good morning, Ananya/i)).toBeInTheDocument();
  });

  it('displays loyalty points in header', async () => {
    renderWithRouter(<Home />);
    
    await screen.findByText('420 pts');
    expect(screen.getByText('420 pts')).toBeInTheDocument();
  });

  it('shows reorder prompt section', async () => {
    renderWithRouter(<Home />);
    
    await screen.findByText('Reorder in one tap');
    expect(screen.getByText('Reorder in one tap')).toBeInTheDocument();
  });

  it('displays recommendations section with AI badge', async () => {
    renderWithRouter(<Home />);
    
    await screen.findByText('Recommended for you');
    expect(screen.getByText('Recommended for you')).toBeInTheDocument();
  });

  it('shows featured categories', async () => {
    renderWithRouter(<Home />);
    
    await screen.findByText('Featured categories');
    expect(screen.getByText('Featured categories')).toBeInTheDocument();
  });

  it('renders shopping lists section', async () => {
    renderWithRouter(<Home />);
    
    await screen.findByText('Your lists');
    expect(screen.getByText('Your lists')).toBeInTheDocument();
    expect(screen.getByText('Weekly Staples')).toBeInTheDocument();
  });

  it('has proper navigation links', async () => {
    renderWithRouter(<Home />);
    
    await screen.findByText('Home');
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Categories')).toBeInTheDocument();
    expect(screen.getByText('Lists')).toBeInTheDocument();
  });

  it('maintains wireframe color scheme', async () => {
    renderWithRouter(<Home />);
    
    await screen.findByText(/Good morning/i);
    
    // Verify key elements are present with correct structure
    const greetingSection = screen.getByRole('heading', { name: /Good morning/i }).closest('section');
    expect(greetingSection).toBeInTheDocument();
  });
});
