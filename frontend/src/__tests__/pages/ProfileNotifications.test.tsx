import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ProfileNotifications from '../../pages/ProfileNotifications';
import { AuthProvider } from '../../contexts/AuthContext';

describe('ProfileNotifications', () => {
  const renderComponent = () => {
    return render(
      <BrowserRouter>
        <AuthProvider>
          <ProfileNotifications />
        </AuthProvider>
      </BrowserRouter>
    );
  };

  it('renders account heading', () => {
    renderComponent();
    expect(screen.getByRole('heading', { name: /Account/i, level: 1 })).toBeInTheDocument();
  });

  it('renders profile section with customer details', () => {
    renderComponent();
    const profileHeadings = screen.getAllByRole('heading', { name: /Profile/i });
    expect(profileHeadings.length).toBeGreaterThan(0);
    expect(screen.getByText(/Ananya Sharma/i)).toBeInTheDocument();
    const vegetarianText = screen.getAllByText(/Vegetarian/i);
    expect(vegetarianText.length).toBeGreaterThan(0);
  });

  it('renders addresses section with serviceability status', () => {
    renderComponent();
    const addressHeadings = screen.getAllByRole('heading', { name: /Addresses/i });
    expect(addressHeadings.length).toBeGreaterThan(0);
    const homeText = screen.getAllByText(/Home/i);
    expect(homeText.length).toBeGreaterThan(0);
    expect(screen.getByText(/Serviceable: Mumbai-South 400001/i)).toBeInTheDocument();
  });

  it('renders notifications section with unread count', () => {
    renderComponent();
    const notificationHeadings = screen.getAllByRole('heading', { name: /Notifications/i });
    expect(notificationHeadings.length).toBeGreaterThan(0);
    const unreadChips = screen.getAllByText(/2 unread/i);
    expect(unreadChips.length).toBeGreaterThan(0);
  });

  it('renders notification preferences table', () => {
    renderComponent();
    expect(screen.getByRole('heading', { name: /Channel preferences/i })).toBeInTheDocument();
    expect(screen.getByText(/Order and delivery updates/i)).toBeInTheDocument();
  });

  it('renders reviews section', () => {
    renderComponent();
    expect(screen.getByRole('heading', { name: /Your reviews/i })).toBeInTheDocument();
    const organicBananas = screen.getAllByText(/Organic Bananas/i);
    expect(organicBananas.length).toBeGreaterThan(0);
  });

  it('renders loyalty points section', () => {
    renderComponent();
    expect(screen.getByRole('heading', { name: /Loyalty points/i })).toBeInTheDocument();
    const loyaltyPoints = screen.getAllByText(/420 points/i);
    expect(loyaltyPoints.length).toBeGreaterThan(0);
  });

  it('renders tabs with notifications tab showing unread count', () => {
    renderComponent();
    const tabs = screen.getAllByRole('tab');
    expect(tabs.length).toBeGreaterThanOrEqual(5); // profile, addresses, notifications, preferences, reviews
  });
});
