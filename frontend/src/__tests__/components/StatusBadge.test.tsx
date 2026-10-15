import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { StatusBadge } from '../../components/StatusBadge';

describe('StatusBadge', () => {
  it('renders confirmed status with green styling', () => {
    render(<StatusBadge status="confirmed" />);
    const badge = screen.getByText('confirmed');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveStyle({ backgroundColor: '#E3F0E7', color: '#14472B' });
  });

  it('renders out_for_delivery status with blue styling', () => {
    render(<StatusBadge status="out_for_delivery" />);
    const badge = screen.getByText('out for delivery');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveStyle({ backgroundColor: '#E0EFF8', color: '#07405F' });
  });

  it('renders cancelled status with grey styling', () => {
    render(<StatusBadge status="cancelled" />);
    const badge = screen.getByText('cancelled');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveStyle({ backgroundColor: '#ECEAE2', color: '#3E4A43' });
  });

  it('renders payment_pending status with marigold styling', () => {
    render(<StatusBadge status="payment_pending" />);
    const badge = screen.getByText('payment pending');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveStyle({ backgroundColor: '#FFF1CC', color: '#5A3D00' });
  });
});
