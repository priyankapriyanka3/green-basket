import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { OrderTracking } from '../../pages/OrderTracking';
import * as apiClient from '../../api/client';

vi.mock('../../api/client');
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useParams: () => ({ id: 'ord-001' }),
  };
});

const mockApiClient = apiClient.apiClient as any;

describe('OrderTracking', () => {
  it('renders order heading', async () => {
    mockApiClient.get = vi.fn().mockResolvedValue({
      data: {
        orderId: 'ord-001',
        status: 'confirmed',
        paymentStatus: 'paid',
        trackingUrl: 'https://track.greenbasketai.com/ord-001',
        slot: { slotId: 'slt-001', label: 'Fri 16 Oct, 9:00 AM' },
        loyalty: { pointsEarned: 17, pointsBalance: 437 },
        reviewEligibility: { canSubmit: false, reason: 'Order not delivered' },
      },
    });
    
    render(
      <BrowserRouter>
        <OrderTracking />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Order ord-001')).toBeInTheDocument();
    });
  });

  it('displays order status badge', async () => {
    mockApiClient.get = vi.fn().mockResolvedValue({
      data: {
        orderId: 'ord-001',
        status: 'confirmed',
        paymentStatus: 'paid',
        trackingUrl: 'https://track.greenbasketai.com/ord-001',
        slot: { slotId: 'slt-001', label: 'Fri 16 Oct, 9:00 AM' },
        loyalty: { pointsEarned: 17, pointsBalance: 437 },
        reviewEligibility: { canSubmit: false, reason: 'Order not delivered' },
      },
    });
    
    render(
      <BrowserRouter>
        <OrderTracking />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Order ord-001')).toBeInTheDocument();
    });
  });

  it('displays order progress timeline', async () => {
    mockApiClient.get = vi.fn().mockResolvedValue({
      data: {
        orderId: 'ord-001',
        status: 'confirmed',
        paymentStatus: 'paid',
        trackingUrl: 'https://track.greenbasketai.com/ord-001',
        slot: { slotId: 'slt-001', label: 'Fri 16 Oct, 9:00 AM' },
        loyalty: { pointsEarned: 17, pointsBalance: 437 },
        reviewEligibility: { canSubmit: false, reason: 'Order not delivered' },
      },
    });
    
    render(
      <BrowserRouter>
        <OrderTracking />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Order progress')).toBeInTheDocument();
      expect(screen.getByText('payment_pending')).toBeInTheDocument();
      expect(screen.getByText('packed')).toBeInTheDocument();
      expect(screen.getByText('delivered')).toBeInTheDocument();
    });
  });

  it('displays order items table', async () => {
    mockApiClient.get = vi.fn().mockResolvedValue({
      data: {
        orderId: 'ord-001',
        status: 'confirmed',
        paymentStatus: 'paid',
        trackingUrl: 'https://track.greenbasketai.com/ord-001',
        slot: { slotId: 'slt-001', label: 'Fri 16 Oct, 9:00 AM' },
        loyalty: { pointsEarned: 17, pointsBalance: 437 },
        reviewEligibility: { canSubmit: false, reason: 'Order not delivered' },
      },
    });
    
    render(
      <BrowserRouter>
        <OrderTracking />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Items in this order')).toBeInTheDocument();
      expect(screen.getByText('Organic Bananas')).toBeInTheDocument();
    });
  });

  it('displays review form', async () => {
    mockApiClient.get = vi.fn().mockResolvedValue({
      data: {
        orderId: 'ord-001',
        status: 'confirmed',
        paymentStatus: 'paid',
        trackingUrl: 'https://track.greenbasketai.com/ord-001',
        slot: { slotId: 'slt-001', label: 'Fri 16 Oct, 9:00 AM' },
        loyalty: { pointsEarned: 17, pointsBalance: 437 },
        reviewEligibility: { canSubmit: false, reason: 'Order not delivered' },
      },
    });
    
    render(
      <BrowserRouter>
        <OrderTracking />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Review your items')).toBeInTheDocument();
      expect(screen.getByText('Submit review')).toBeInTheDocument();
    });
  });

  it('displays delivery agent information', async () => {
    mockApiClient.get = vi.fn().mockResolvedValue({
      data: {
        orderId: 'ord-001',
        status: 'confirmed',
        paymentStatus: 'paid',
        trackingUrl: 'https://track.greenbasketai.com/ord-001',
        slot: { slotId: 'slt-001', label: 'Fri 16 Oct, 9:00 AM' },
        deliveryAgent: { agentId: 'agt-010', name: 'Rajesh', phoneNumber: '+91 98123 41234', vehicleDetails: 'Electric scooter', availabilityStatus: 'assigned' },
        loyalty: { pointsEarned: 17, pointsBalance: 437 },
        reviewEligibility: { canSubmit: false, reason: 'Order not delivered' },
      },
    });
    
    render(
      <BrowserRouter>
        <OrderTracking />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Delivery agent')).toBeInTheDocument();
      expect(screen.getByText('Rajesh')).toBeInTheDocument();
    });
  });

  it('displays tracking URL', async () => {
    mockApiClient.get = vi.fn().mockResolvedValue({
      data: {
        orderId: 'ord-001',
        status: 'confirmed',
        paymentStatus: 'paid',
        trackingUrl: 'https://track.greenbasketai.com/ord-001',
        slot: { slotId: 'slt-001', label: 'Fri 16 Oct, 9:00 AM' },
        loyalty: { pointsEarned: 17, pointsBalance: 437 },
        reviewEligibility: { canSubmit: false, reason: 'Order not delivered' },
      },
    });
    
    render(
      <BrowserRouter>
        <OrderTracking />
      </BrowserRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('https://track.greenbasketai.com/ord-001')).toBeInTheDocument();
    });
  });
});
