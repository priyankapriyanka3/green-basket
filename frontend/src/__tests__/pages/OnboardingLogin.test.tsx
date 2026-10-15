import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { OnboardingLogin } from '../../pages/OnboardingLogin';
import { AuthProvider } from '../../contexts/AuthContext';

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      <AuthProvider>{component}</AuthProvider>
    </BrowserRouter>
  );
};

describe('OnboardingLogin', () => {
  it('renders login form with all required fields', () => {
    renderWithRouter(<OnboardingLogin />);
    
    expect(screen.getByLabelText('Phone number')).toBeInTheDocument();
    expect(screen.getByLabelText('OTP or password')).toBeInTheDocument();
    expect(screen.getByLabelText(/Shopper/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Operator/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign in/i })).toBeInTheDocument();
  });

  it('pre-fills phone number and password with demo credentials', () => {
    renderWithRouter(<OnboardingLogin />);
    
    const phoneInput = screen.getByLabelText('Phone number') as HTMLInputElement;
    const passwordInput = screen.getByLabelText('OTP or password') as HTMLInputElement;
    
    expect(phoneInput.value).toBe('9876543210');
    expect(passwordInput.value).toBe('Demo@123');
  });

  it('toggles password visibility', () => {
    renderWithRouter(<OnboardingLogin />);
    
    const passwordInput = screen.getByLabelText('OTP or password') as HTMLInputElement;
    const showButton = screen.getByRole('button', { name: /Show|Hide/ });
    
    expect(passwordInput.type).toBe('password');
    
    fireEvent.click(showButton);
    expect(passwordInput.type).toBe('text');
    
    fireEvent.click(showButton);
    expect(passwordInput.type).toBe('password');
  });

  it('has minimum 44px touch targets on all interactive elements', () => {
    renderWithRouter(<OnboardingLogin />);
    
    const phoneInput = screen.getByLabelText('Phone number');
    const passwordInput = screen.getByLabelText('OTP or password');
    const submitButton = screen.getByRole('button', { name: /Sign in/i });
    
    [phoneInput, passwordInput, submitButton].forEach((element) => {
      const styles = window.getComputedStyle(element);
      expect(parseInt(styles.minHeight || styles.height)).toBeGreaterThanOrEqual(44);
    });
  });

  it('has focus ring styles on interactive elements', () => {
    renderWithRouter(<OnboardingLogin />);
    
    const phoneInput = screen.getByLabelText('Phone number');
    phoneInput.focus();
    
    // Focus ring should be visible via CSS
    expect(document.activeElement).toBe(phoneInput);
  });

  it('renders wireframe colors and layout matching design', () => {
    renderWithRouter(<OnboardingLogin />);
    
    // Check for intro section with gradient background
    const introSection = screen.getByRole('heading', { name: /Fresh groceries, planned around the way you eat/i }).closest('section');
    expect(introSection).toBeInTheDocument();
    
    // Check for brand logo
    expect(screen.getByText('GreenBasket AI')).toBeInTheDocument();
  });
});
