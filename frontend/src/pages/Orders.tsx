import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { colors } from '../styles/colors';
import { typography } from '../styles/typography';
import { accessibility } from '../styles/accessibility';
import apiClient from '../api/client';

interface Order {
  order_id: string;
  status: string;
  total_amount: number;
  created_at: string;
  items_count: number;
}

export const Orders: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchOrders = async () => {
      try {
        const response = await apiClient.get('/orders');
        setOrders(response.data.orders || []);
      } catch (error) {
        console.error('Failed to fetch orders:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [isAuthenticated, navigate]);

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'delivered':
        return { bg: colors.status.freshBg, text: colors.status.freshText, border: colors.status.freshBorder };
      case 'processing':
      case 'shipped':
        return { bg: colors.status.warningBg, text: '#fff', border: colors.status.warningBg };
      case 'cancelled':
        return { bg: '#fee', text: '#c00', border: '#fcc' };
      default:
        return { bg: colors.surface, text: colors.ink, border: colors.border };
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: colors.background }}>
      <header style={{ background: colors.primaryDark, color: '#fff', padding: '16px 64px 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingBottom: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <h1 style={{ fontFamily: typography.fontFamilies.display, fontSize: '28px', fontWeight: 700, margin: 0 }}>GreenBasket AI</h1>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <a href="/account" style={{ display: 'inline-flex', alignItems: 'center', minHeight: `${accessibility.minTouchTarget}px`, padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,0.55)', color: '#fff', fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>Account</a>
            <a href="/shop/cart" style={{ display: 'inline-flex', minHeight: `${accessibility.minTouchTarget}px`, padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,0.55)', color: '#fff', fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>Cart</a>
          </div>
        </div>
        <nav style={{ display: 'flex', gap: '8px', paddingBottom: '12px' }}>
          <a href="/shop" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Home</a>
          <a href="/shop/categories" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Categories</a>
          <a href="/planner/lists" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Lists</a>
          <a href="/account/orders" style={{ textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px', background: '#fff', color: colors.primaryDark }}>Orders</a>
          <a href="/account" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Account</a>
        </nav>
      </header>

      <main style={{ padding: '24px 64px 48px' }}>
        <h1 style={{ fontFamily: typography.fontFamilies.display, fontSize: '36px', fontWeight: 600, margin: '0 0 20px' }}>Your Orders</h1>

        {loading ? (
          <p style={{ color: colors.muted }}>Loading orders...</p>
        ) : orders.length === 0 ? (
          <div style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '40px', textAlign: 'center' }}>
            <p style={{ fontSize: '18px', color: colors.muted }}>No orders yet</p>
            <a href="/shop" style={{ display: 'inline-block', marginTop: '16px', padding: '12px 24px', background: colors.primary, color: '#fff', borderRadius: '6px', textDecoration: 'none', fontWeight: 600 }}>Start Shopping</a>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {orders.map((order) => {
              const statusColors = getStatusColor(order.status);
              return (
                <div key={order.order_id} style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '20px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '12px' }}>
                    <div>
                      <h3 style={{ fontSize: '20px', fontWeight: 600, margin: '0 0 4px' }}>Order {order.order_id}</h3>
                      <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>Placed on {new Date(order.created_at).toLocaleDateString()}</p>
                    </div>
                    <span style={{ display: 'inline-block', padding: '4px 12px', borderRadius: '6px', fontSize: '14px', fontWeight: 600, background: statusColors.bg, color: statusColors.text, border: `1px solid ${statusColors.border}` }}>
                      {order.status}
                    </span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <p style={{ fontSize: '16px', color: colors.muted, margin: 0 }}>{order.items_count} items</p>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                      <p style={{ fontSize: '20px', fontWeight: 700, margin: 0 }}>₹{order.total_amount.toFixed(2)}</p>
                      <a href={`/shop/orders/${order.order_id}`} style={{ padding: '8px 16px', background: colors.primary, color: '#fff', borderRadius: '6px', textDecoration: 'none', fontWeight: 600 }}>Track Order</a>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
};

export default Orders;
