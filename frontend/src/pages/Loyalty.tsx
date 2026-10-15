import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { colors } from '../styles/colors';
import { typography } from '../styles/typography';
import { accessibility } from '../styles/accessibility';
import apiClient from '../api/client';

interface LoyaltyData {
  balance: number;
  tier: string;
  transactions: Array<{
    transaction_id: string;
    points_change: number;
    balance_after: number;
    reason: string;
    created_at: string;
  }>;
}

export const Loyalty: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [loyaltyData, setLoyaltyData] = useState<LoyaltyData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchLoyalty = async () => {
      try {
        const response = await apiClient.get('/loyalty');
        setLoyaltyData(response.data);
      } catch (error) {
        console.error('Failed to fetch loyalty data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchLoyalty();
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
        <h1 style={{ fontFamily: typography.fontFamilies.display, fontSize: '36px', fontWeight: 600, margin: '0 0 20px' }}>Loyalty Points</h1>

        {loading ? (
          <p style={{ color: colors.muted }}>Loading loyalty data...</p>
        ) : loyaltyData ? (
          <div>
            <div style={{ background: colors.accent, color: colors.accentInk, borderRadius: '12px', padding: '32px', marginBottom: '24px' }}>
              <p style={{ fontSize: '18px', fontWeight: 600, margin: '0 0 8px' }}>Your Balance</p>
              <p style={{ fontSize: '48px', fontWeight: 700, margin: '0' }}>{loyaltyData.balance} points</p>
              <p style={{ fontSize: '16px', margin: '8px 0 0' }}>Tier: {loyaltyData.tier}</p>
            </div>

            <h2 style={{ fontSize: '24px', fontWeight: 600, margin: '0 0 16px' }}>Transaction History</h2>
            {loyaltyData.transactions && loyaltyData.transactions.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {loyaltyData.transactions.map((txn) => (
                  <div key={txn.transaction_id} style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <p style={{ fontSize: '16px', fontWeight: 600, margin: '0 0 4px' }}>{txn.reason}</p>
                      <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>{new Date(txn.created_at).toLocaleDateString()}</p>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <p style={{ fontSize: '20px', fontWeight: 700, margin: '0', color: txn.points_change > 0 ? colors.status.freshText : colors.status.warningBg }}>{txn.points_change > 0 ? '+' : ''}{txn.points_change}</p>
                      <p style={{ fontSize: '14px', color: colors.muted, margin: '4px 0 0' }}>Balance: {txn.balance_after}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: colors.muted }}>No transactions yet</p>
            )}
          </div>
        ) : (
          <p style={{ color: colors.muted }}>Unable to load loyalty data</p>
        )}
      </main>
    </div>
  );
};

export default Loyalty;
