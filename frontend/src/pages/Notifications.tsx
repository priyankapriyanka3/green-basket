import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { colors } from '../styles/colors';
import { typography } from '../styles/typography';
import { accessibility } from '../styles/accessibility';
import apiClient from '../api/client';

interface Notification {
  notification_id: string;
  title: string;
  message: string;
  channel: string;
  dispatch_status: string;
  created_at: string;
}

export const Notifications: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchNotifications = async () => {
      try {
        const response = await apiClient.get('/notifications/');
        setNotifications(response.data.notifications || []);
      } catch (error) {
        console.error('Failed to fetch notifications:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchNotifications();
  }, [isAuthenticated, navigate]);

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
          <a href="/account/orders" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Orders</a>
          <a href="/account" style={{ textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px', background: '#fff', color: colors.primaryDark }}>Account</a>
        </nav>
      </header>

      <main style={{ padding: '24px 64px 48px' }}>
        <h1 style={{ fontFamily: typography.fontFamilies.display, fontSize: '36px', fontWeight: 600, margin: '0 0 20px' }}>Notifications</h1>

        {loading ? (
          <p style={{ color: colors.muted }}>Loading notifications...</p>
        ) : notifications.length === 0 ? (
          <div style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '40px', textAlign: 'center' }}>
            <p style={{ fontSize: '18px', color: colors.muted }}>No notifications yet</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {notifications.map((notification) => (
              <div key={notification.notification_id} style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '16px' }}>
                <h3 style={{ fontSize: '18px', fontWeight: 600, margin: '0 0 8px' }}>{notification.title}</h3>
                <p style={{ color: colors.muted, margin: '0 0 8px' }}>{notification.message}</p>
                <div style={{ display: 'flex', gap: '12px', fontSize: '14px', color: colors.muted }}>
                  <span>Channel: {notification.channel}</span>
                  <span>Status: {notification.dispatch_status}</span>
                  <span>{new Date(notification.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default Notifications;
