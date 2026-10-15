import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Checkout } from '../../pages/Checkout';

describe('Checkout', () => {
  it('renders checkout heading', () => {
    render(
      <BrowserRouter>
        <Checkout />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Checkout')).toBeInTheDocument();
  });

  it('displays checkout progress steps', () => {
    render(
      <BrowserRouter>
        <Checkout />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Cart check')).toBeInTheDocument();
    expect(screen.getByText('Address serviceability')).toBeInTheDocument();
    expect(screen.getByText('Delivery slot')).toBeInTheDocument();
    expect(screen.getByText('Payment')).toBeInTheDocument();
  });

  it('displays address selection with serviceable addresses', () => {
    render(
      <BrowserRouter>
        <Checkout />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Delivery address')).toBeInTheDocument();
    const homeLabel = screen.getAllByText('Home')[0];
    expect(homeLabel).toBeInTheDocument();
  });

  it('displays delivery slot selection', () => {
    render(
      <BrowserRouter>
        <Checkout />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Delivery slot for Friday 16 Oct')).toBeInTheDocument();
    expect(screen.getByText('7:00 AM to 9:00 AM')).toBeInTheDocument();
    expect(screen.getByText('9:00 AM to 11:00 AM')).toBeInTheDocument();
  });

  it('displays payment method selection', () => {
    render(
      <BrowserRouter>
        <Checkout />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Payment method')).toBeInTheDocument();
    expect(screen.getByText('UPI')).toBeInTheDocument();
    expect(screen.getByText('Card')).toBeInTheDocument();
    expect(screen.getByText('Netbanking')).toBeInTheDocument();
  });

  it('displays order summary sidebar', () => {
    render(
      <BrowserRouter>
        <Checkout />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Order summary')).toBeInTheDocument();
    expect(screen.getByText(/Pay ₹170\.00 with/)).toBeInTheDocument();
  });
});
