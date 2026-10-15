import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Cart } from '../../pages/Cart';
import * as apiClient from '../../api/client';

vi.mock('../../api/client');

const mockApiClient = apiClient.apiClient as any;

describe('Cart', () => {
  it('renders cart heading', async () => {
    mockApiClient.post = vi.fn().mockResolvedValue({
      data: {
        cartId: 'cart-001',
        pricing: { subtotal: '185.00', discountAmount: '10.00', loyaltyRedemptionAmount: '5.00', finalAmount: '170.00', currency: 'INR' },
        lineItems: [],
        warnings: [],
      },
    });
    
    render(
      <BrowserRouter>
        <Cart />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Your cart')).toBeInTheDocument();
    });
  });

  it('displays cart items table', async () => {
    mockApiClient.post = vi.fn().mockResolvedValue({
      data: {
        cartId: 'cart-001',
        pricing: { subtotal: '185.00', discountAmount: '10.00', loyaltyRedemptionAmount: '5.00', finalAmount: '170.00', currency: 'INR' },
        lineItems: [
          { productId: 'prod-021', quantity: 1, unitPrice: '65.00', lineTotal: '65.00' },
        ],
        warnings: [],
      },
    });
    
    render(
      <BrowserRouter>
        <Cart />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Items in your cart')).toBeInTheDocument();
      expect(screen.getByText('Organic Bananas')).toBeInTheDocument();
    });
  });

  it('displays order summary with pricing breakdown', async () => {
    mockApiClient.post = vi.fn().mockResolvedValue({
      data: {
        cartId: 'cart-001',
        pricing: { subtotal: '185.00', discountAmount: '10.00', loyaltyRedemptionAmount: '5.00', finalAmount: '170.00', currency: 'INR' },
        lineItems: [],
        warnings: [],
      },
    });
    
    render(
      <BrowserRouter>
        <Cart />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Order summary')).toBeInTheDocument();
      expect(screen.getByText('Subtotal')).toBeInTheDocument();
      expect(screen.getByText('Final amount')).toBeInTheDocument();
    });
  });

  it('displays loyalty points redemption controls', async () => {
    mockApiClient.post = vi.fn().mockResolvedValue({
      data: {
        cartId: 'cart-001',
        pricing: { subtotal: '185.00', discountAmount: '0.00', loyaltyRedemptionAmount: '0.00', finalAmount: '185.00', currency: 'INR' },
        lineItems: [],
        warnings: [],
      },
    });
    
    render(
      <BrowserRouter>
        <Cart />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      const loyaltyHeading = screen.getAllByText('Loyalty points')[0];
      expect(loyaltyHeading).toBeInTheDocument();
    });
  });

  it('displays checkout button', async () => {
    mockApiClient.post = vi.fn().mockResolvedValue({
      data: {
        cartId: 'cart-001',
        pricing: { subtotal: '185.00', discountAmount: '0.00', loyaltyRedemptionAmount: '0.00', finalAmount: '185.00', currency: 'INR' },
        lineItems: [],
        warnings: [],
      },
    });
    
    render(
      <BrowserRouter>
        <Cart />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Proceed to checkout')).toBeInTheDocument();
    });
  });
});
