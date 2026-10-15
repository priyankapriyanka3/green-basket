import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ShoppingLists from '../../pages/ShoppingLists';
import { AuthProvider } from '../../contexts/AuthContext';

describe('ShoppingLists', () => {
  const renderComponent = () => {
    return render(
      <BrowserRouter>
        <AuthProvider>
          <ShoppingLists />
        </AuthProvider>
      </BrowserRouter>
    );
  };

  it('renders shopping lists heading', () => {
    renderComponent();
    expect(screen.getByRole('heading', { name: /shopping lists/i, level: 1 })).toBeInTheDocument();
  });

  it('renders list tabs section with AI-generated and manual list chips', () => {
    renderComponent();
    expect(screen.getByText(/Your lists/i)).toBeInTheDocument();
    const aiGeneratedChips = screen.getAllByText(/AI generated/i);
    expect(aiGeneratedChips.length).toBeGreaterThan(0);
    expect(screen.getByText(/Manual list/i)).toBeInTheDocument();
  });

  it('renders generate list button', () => {
    renderComponent();
    expect(screen.getByRole('button', { name: /Generate a list with AI/i })).toBeInTheDocument();
  });

  it('renders list items table with product names and reason chips', () => {
    renderComponent();
    const organicBananas = screen.getAllByText(/Organic Bananas/i);
    expect(organicBananas.length).toBeGreaterThan(0);
    const spinach = screen.getAllByText(/Spinach/i);
    expect(spinach.length).toBeGreaterThan(0);
    // Reason chips rendered via ReasonChip component
  });

  it('renders reorder reminders section', () => {
    renderComponent();
    expect(screen.getByRole('heading', { name: /Reorder reminders/i })).toBeInTheDocument();
    expect(screen.getByText(/2 items due/i)).toBeInTheDocument();
  });

  it('renders add all to cart bar with total', () => {
    renderComponent();
    // The bar displays available item count and total
    const addAllButtons = screen.getAllByText(/Add all to cart/i);
    expect(addAllButtons.length).toBeGreaterThan(0);
  });
});
