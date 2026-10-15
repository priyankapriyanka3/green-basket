import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { colors } from '../styles/colors';

interface OpsSummary {
  open_slot_alerts: number;
  promotion_warnings: number;
  negative_sentiment_products: number;
}

export default function AdminDashboard() {
  const { user } = useAuth();
  const [opsSummary, setOpsSummary] = useState<OpsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadOperationsData();
  }, []);

  const loadOperationsData = async () => {
    try {
      setLoading(true);
      
      // Check if user is operator
      if (user?.role !== 'operator') {
        setError('FORBIDDEN_ROLE_SCOPE');
        return;
      }

      // Mock data for wireframe fidelity
      setOpsSummary({
        open_slot_alerts: 2,
        promotion_warnings: 1,
        negative_sentiment_products: 3,
      });
      setError(null);
    } catch (err) {
      setError('Failed to load operations data');
    } finally {
      setLoading(false);
    }
  };

  // Show 403 for non-operator users
  if (error === 'FORBIDDEN_ROLE_SCOPE' || (user && user.role !== 'operator')) {
    return (
      <div style={{ background: colors.background, minHeight: '100vh' }}>
        {/* Header */}
        <header style={{ background: colors.primaryDark, color: '#fff' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '20px', padding: '14px 64px' }}>
            <a href="/shop" style={{ display: 'flex', alignItems: 'center', gap: '10px', fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 700, color: '#fff', textDecoration: 'none' }}>
              <span style={{ width: '36px', height: '36px', borderRadius: '10px', background: colors.accent, color: colors.accentInk, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px', fontWeight: 700 }}>G</span>
              GreenBasket AI Operations
            </a>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', minHeight: '44px', padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,.55)', color: '#fff', fontSize: '14px', fontWeight: 600 }}>
                {user?.displayName || 'Guest'} | Shopper
              </span>
              <a href="/login" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', minHeight: '44px', padding: '0 14px', borderRadius: '999px', background: colors.accent, color: colors.accentInk, border: `1px solid ${colors.accent}`, fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>
                Sign out
              </a>
            </div>
          </div>
          <nav style={{ display: 'flex', gap: '8px', padding: '0 64px 12px' }} aria-label="Operations">
            <a href="/ops" style={{ background: '#fff', color: colors.primaryDark, textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }} aria-current="page">
              Operations
            </a>
            <a href="/shop" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>
              Customer view
            </a>
          </nav>
        </header>

        {/* Main content */}
        <main style={{ padding: '32px 64px 48px' }}>
          <h1 style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '36px', fontWeight: 600, lineHeight: 1.2, margin: 0 }}>Access state for shoppers</h1>
          <div style={{ border: '2px dashed #8A8570', borderRadius: '8px', padding: '14px', background: '#fff', marginTop: '12px' }}>
            <span style={{ display: 'inline-block', fontFamily: "'Courier New', monospace", fontSize: '12px', fontWeight: 700, background: '#ECEFF1', color: '#26343B', padding: '2px 8px', borderRadius: '4px', marginBottom: '8px' }}>
              FORBIDDEN_ROLE_SCOPE
            </span>
            <div role="alert" style={{ display: 'flex', gap: '10px', padding: '12px 16px', borderRadius: '6px', border: '1px solid #E0A09B', fontSize: '15px', background: colors.dangerTint, color: '#7A1710' }}>
              <div>
                <strong>Operations access is limited to operator accounts.</strong> You are signed in as a shopper.{' '}
                <a href="/shop">Return to Home</a>
              </div>
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer style={{ background: colors.surfaceAlt, borderTop: `1px solid ${colors.border}`, padding: '24px 64px', color: colors.muted, fontSize: '14px' }}>
          <p style={{ margin: 0 }}>Delivering in Mumbai and Bengaluru only.</p>
          <p style={{ marginTop: '4px', margin: 0 }}>Prices in INR. Freshness information is indicative and based on harvest and expiry data.</p>
        </footer>
      </div>
    );
  }

  if (loading) {
    return (
      <div style={{ padding: '32px 64px' }}>
        <p>Loading operations dashboard...</p>
      </div>
    );
  }

  return (
    <div style={{ background: colors.background, minHeight: '100vh' }}>
      {/* Header */}
      <header style={{ background: colors.primaryDark, color: '#fff' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '20px', padding: '14px 64px' }}>
          <a href="/ops" style={{ display: 'flex', alignItems: 'center', gap: '10px', fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 700, color: '#fff', textDecoration: 'none' }}>
            <span style={{ width: '36px', height: '36px', borderRadius: '10px', background: colors.accent, color: colors.accentInk, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px', fontWeight: 700 }}>G</span>
            GreenBasket AI Operations
          </a>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', minHeight: '44px', padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,.55)', color: '#fff', fontSize: '14px', fontWeight: 600 }}>
              Kavya Nair | Operator
            </span>
            <a href="/login" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', minHeight: '44px', padding: '0 14px', borderRadius: '999px', background: colors.accent, color: colors.accentInk, border: `1px solid ${colors.accent}`, fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>
              Sign out
            </a>
          </div>
        </div>
        <nav style={{ display: 'flex', gap: '8px', padding: '0 64px 12px' }} aria-label="Operations">
          <a href="/ops" style={{ background: '#fff', color: colors.primaryDark, textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }} aria-current="page">
            Operations
          </a>
          <a href="/shop" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>
            Customer view
          </a>
        </nav>
      </header>

      {/* Operations band */}
      <div role="status" aria-live="polite" style={{ background: colors.primaryTint, borderBottom: '1px solid #B9D8C4', padding: '12px 64px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '16px', flexWrap: 'wrap' }}>
        <span>
          <strong>Data refreshed at 09:45 AM</strong> | Auto-refresh every 5 minutes | Thu 15 Oct 2026
        </span>
        <span style={{ fontSize: '14px', color: colors.muted }}>
          Counts, ids and categories only. No customer names, phone numbers or allergy details appear here.
        </span>
      </div>

      {/* Main content */}
      <main style={{ padding: '32px 64px 48px' }}>
        <h1 style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '36px', fontWeight: 600, lineHeight: 1.2, margin: 0 }}>Operations overview</h1>
        <p style={{ color: colors.muted, marginTop: '6px', margin: 0 }}>A single view of delivery slots, promotions, serviceability, freshness, recommendation reasons, review sentiment and notifications.</p>

        {/* KPI cards */}
        <section style={{ marginTop: '20px' }} aria-labelledby="kpi-title">
          <h2 id="kpi-title" style={{ position: 'absolute', left: '-9999px' }}>Key counters</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '16px' }}>
            <div style={{ border: '2px solid #E3C26B', borderRadius: '8px', background: colors.accentTint, padding: '20px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '44px', fontWeight: 700, lineHeight: 1 }}>{opsSummary?.open_slot_alerts || 0}</span>
              <span style={{ fontWeight: 600, fontSize: '15px' }}>Open slot alerts</span>
              <span style={{ fontSize: '13px', color: colors.muted }}>openSlotAlerts | slots at 90% or more</span>
            </div>
            <div style={{ border: '2px solid #E3C26B', borderRadius: '8px', background: colors.accentTint, padding: '20px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '44px', fontWeight: 700, lineHeight: 1 }}>{opsSummary?.promotion_warnings || 0}</span>
              <span style={{ fontWeight: 600, fontSize: '15px' }}>Promotion warnings</span>
              <span style={{ fontSize: '13px', color: colors.muted }}>promotionWarnings | needs a look</span>
            </div>
            <div style={{ border: '2px solid #E0A09B', borderRadius: '8px', background: colors.dangerTint, padding: '20px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '44px', fontWeight: 700, lineHeight: 1 }}>{opsSummary?.negative_sentiment_products || 0}</span>
              <span style={{ fontWeight: 600, fontSize: '15px' }}>Negative-sentiment products</span>
              <span style={{ fontSize: '13px', color: colors.muted }}>negativeSentimentProducts | flagged</span>
            </div>
            <div style={{ border: `1px solid ${colors.border}`, borderRadius: '8px', background: '#fff', padding: '20px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '44px', fontWeight: 700, lineHeight: 1 }}>248</span>
              <span style={{ fontWeight: 600, fontSize: '15px' }}>Orders today</span>
              <span style={{ fontSize: '13px', color: colors.muted }}>Mumbai 171 | Bengaluru 77</span>
            </div>
            <div style={{ border: `1px solid ${colors.border}`, borderRadius: '8px', background: '#fff', padding: '20px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '44px', fontWeight: 700, lineHeight: 1 }}>96.4%</span>
              <span style={{ fontWeight: 600, fontSize: '15px' }}>Fulfilment on time</span>
              <span style={{ fontSize: '13px', color: colors.muted }}>Last 7 days</span>
            </div>
          </div>
        </section>

        {/* Slot utilization table */}
        <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)', marginTop: '32px' }} aria-labelledby="slot-title">
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <caption id="slot-title" style={{ textAlign: 'left', fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 600, paddingBottom: '10px' }}>
              Slot utilisation by zone and window, Fri 16 Oct
            </caption>
            <thead>
              <tr>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Zone</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Window</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>Reserved</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>Max</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Utilisation</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Risk</th>
              </tr>
            </thead>
            <tbody>
              {[
                { zone: 'Mumbai-South', window: '7:00 to 9:00 AM', reserved: 38, max: 50, pct: 76, risk: 'Normal', riskColor: 'fresh' },
                { zone: 'Mumbai-South', window: '9:00 to 11:00 AM', reserved: 46, max: 50, pct: 92, risk: 'Overbooking risk', riskColor: 'warning' },
                { zone: 'Mumbai-South', window: '12:00 to 2:00 PM', reserved: 50, max: 50, pct: 100, risk: 'Full', riskColor: 'danger' },
                { zone: 'Bengaluru-Central', window: '9:00 to 11:00 AM', reserved: 27, max: 40, pct: 68, risk: 'Normal', riskColor: 'fresh' },
              ].map((slot, i) => (
                <tr key={i}>
                  <th scope="row" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontWeight: 400, fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {slot.zone}
                  </th>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {slot.window}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {slot.reserved}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {slot.max}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ flex: 1, minWidth: '80px', height: '12px', background: '#E6E0CC', borderRadius: '6px', overflow: 'hidden' }}>
                        <span
                          style={{
                            display: 'block',
                            height: '12px',
                            borderRadius: '6px',
                            background: slot.pct >= 100 ? colors.danger : slot.pct >= 90 ? colors.accent : colors.primary,
                            width: `${slot.pct}%`,
                          }}
                        />
                      </span>
                      <span>{slot.pct}%</span>
                    </div>
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    <span
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '2px 10px',
                        borderRadius: '999px',
                        fontSize: '13px',
                        fontWeight: 600,
                        lineHeight: '20px',
                        background:
                          slot.riskColor === 'fresh'
                            ? colors.primaryTint
                            : slot.riskColor === 'warning'
                            ? colors.accentTint
                            : colors.dangerTint,
                        color:
                          slot.riskColor === 'fresh'
                            ? '#14472B'
                            : slot.riskColor === 'warning'
                            ? '#5A3D00'
                            : '#7A1710',
                        border:
                          slot.riskColor === 'fresh'
                            ? '1px solid #B9D8C4'
                            : slot.riskColor === 'warning'
                            ? '1px solid #EBCB7A'
                            : '1px solid #E0A09B',
                      }}
                    >
                      {slot.risk}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* Promotions table */}
        <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)', marginTop: '32px' }} aria-labelledby="promo-title">
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <caption id="promo-title" style={{ textAlign: 'left', fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 600, paddingBottom: '10px' }}>
              Promotions
            </caption>
            <thead>
              <tr>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Code</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Type</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>Minimum</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Valid</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>Used / limit</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Status</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Warning</th>
              </tr>
            </thead>
            <tbody>
              {[
                { code: 'GREEN10', type: 'Percentage, 10%', min: '₹200.00', valid: '1 Oct to 31 Oct', used: 212, limit: 1000, status: 'Active', warning: 'Active but low usage: threshold mismatch' },
                { code: 'FIRSTORDER', type: 'Flat, ₹50.00', min: '₹299.00', valid: '1 Oct to 31 Dec', used: 640, limit: 2000, status: 'Active', warning: 'None' },
                { code: 'FREEDEL', type: 'Free delivery', min: '₹499.00', valid: '1 Oct to 31 Oct', used: 88, limit: 500, status: 'Active', warning: 'None' },
                { code: 'ORGANIC10', type: 'Percentage, 10%', min: '₹200.00', valid: '10 Oct to 20 Oct', used: 143, limit: 600, status: 'Active', warning: 'Points at a product with 3 left' },
                { code: 'BUY2GET1', type: 'Buy 2 get 1', min: '₹0.00', valid: '1 Oct to 15 Oct', used: 301, limit: 300, status: 'Expired', warning: 'None' },
              ].map((promo, i) => (
                <tr key={i}>
                  <th scope="row" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontWeight: 400, fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {promo.code}
                  </th>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {promo.type}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {promo.min}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {promo.valid}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {promo.used} / {promo.limit}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    <span
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '2px 10px',
                        borderRadius: '999px',
                        fontSize: '13px',
                        fontWeight: 600,
                        lineHeight: '20px',
                        background: promo.status === 'Active' ? colors.primaryTint : '#ECEAE2',
                        color: promo.status === 'Active' ? '#14472B' : '#3E4A43',
                        border: promo.status === 'Active' ? '1px solid #B9D8C4' : '1px solid #C9C4B2',
                      }}
                    >
                      {promo.status}
                    </span>
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {promo.warning !== 'None' && (
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: colors.accentTint, color: '#5A3D00', border: '1px solid #EBCB7A' }}>
                        {promo.warning}
                      </span>
                    )}
                    {promo.warning === 'None' && 'None'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* Two-column layout */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', alignItems: 'start', marginTop: '32px' }}>
          {/* Serviceability */}
          <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }} aria-labelledby="svc-title">
            <h2 id="svc-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 600, margin: 0 }}>Serviceability</h2>
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '8px' }}>
              <caption style={{ position: 'absolute', left: '-9999px' }}>Saved addresses by service state</caption>
              <thead>
                <tr>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>City</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>Serviceable</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>Saved, not serviceable</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>Blocked checkouts today</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { city: 'Mumbai', serviceable: 3420, saved: 18, blocked: 4 },
                  { city: 'Bengaluru', serviceable: 1980, saved: 11, blocked: 2 },
                  { city: 'Delhi', serviceable: 0, saved: 96, blocked: 9 },
                  { city: 'Other', serviceable: 0, saved: 41, blocked: 3 },
                ].map((city, i) => (
                  <tr key={i}>
                    <th scope="row" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontWeight: 400, fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {city.city}
                    </th>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {city.serviceable.toLocaleString()}
                    </td>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {city.saved}
                    </td>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {city.blocked}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p style={{ fontSize: '14px', color: colors.muted, marginTop: '8px', margin: 0 }}>
              Saved but not serviceable addresses show where demand exists outside Mumbai and Bengaluru.
            </p>
          </section>

          {/* Recommendation reasons */}
          <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }} aria-labelledby="rec-title">
            <h2 id="rec-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 600, margin: 0 }}>Recommendation reasons</h2>
            <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>Count of recommendations shown in the last 24 hours, by reason tag.</p>
            <div role="group" aria-label="Recommendation reason distribution">
              {[
                { label: 'Frequently bought', count: 1560, pct: 78 },
                { label: 'Reorder reminder', count: 1240, pct: 62 },
                { label: 'Based on your diet', count: 880, pct: 44 },
                { label: 'Seasonal', count: 600, pct: 30 },
                { label: 'Trending', count: 420, pct: 21 },
              ].map((reason, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '12px', margin: '8px 0' }}>
                  <span style={{ width: '150px', fontSize: '14px', fontWeight: 600 }}>{reason.label}</span>
                  <span style={{ flex: 1, height: '14px', borderRadius: '7px', background: '#E6E0CC', overflow: 'hidden' }}>
                    <span style={{ display: 'block', height: '14px', borderRadius: '7px', background: colors.primary, width: `${reason.pct}%` }} />
                  </span>
                  <span style={{ width: '72px', textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums' }}>
                    {reason.count.toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
            <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>
              Frequently bought: frequently_bought | Reorder reminder: reorder_reminder | Based on your diet: based_on_diet | Seasonal: seasonal | Trending: trending
            </p>
          </section>
        </div>

        {/* Inventory freshness table */}
        <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)', marginTop: '32px' }} aria-labelledby="inv-title">
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <caption id="inv-title" style={{ textAlign: 'left', fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 600, paddingBottom: '10px' }}>
              Inventory freshness
            </caption>
            <thead>
              <tr>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Product</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>Stock</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>Reorder level</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Harvest</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Expiry</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Zone</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Availability</th>
                <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Flag</th>
              </tr>
            </thead>
            <tbody>
              {[
                { product: 'Organic Bananas (prod-001)', stock: 64, reorder: 30, harvest: '13 Oct', expiry: '17 Oct', zone: 'Ambient-A', avail: 'available', flag: 'None' },
                { product: 'Spinach (prod-005)', stock: 3, reorder: 20, harvest: '14 Oct', expiry: '16 Oct', zone: 'Cold-A', avail: 'low_stock', flag: 'Low stock, Expires in 1 day' },
                { product: 'Fresh Paneer', stock: 22, reorder: 15, harvest: '13 Oct', expiry: '16 Oct', zone: 'Cold-B', avail: 'available', flag: 'Expires in 1 day' },
                { product: 'Rolled Oats', stock: 140, reorder: 40, harvest: 'Not applicable', expiry: '14 Mar 2027', zone: 'Dry-A', avail: 'available', flag: 'None' },
                { product: 'Organic Quinoa', stock: 0, reorder: 25, harvest: 'Not applicable', expiry: 'Not applicable', zone: 'Dry-A', avail: 'unavailable', flag: 'Out of stock' },
              ].map((inv, i) => (
                <tr key={i}>
                  <th scope="row" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontWeight: 400, fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {inv.product}
                  </th>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {inv.stock}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {inv.reorder}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {inv.harvest}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {inv.expiry}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {inv.zone}
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    <span
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '2px 10px',
                        borderRadius: '999px',
                        fontSize: '13px',
                        fontWeight: 600,
                        lineHeight: '20px',
                        background:
                          inv.avail === 'available'
                            ? colors.primaryTint
                            : inv.avail === 'low_stock'
                            ? colors.accentTint
                            : '#ECEAE2',
                        color:
                          inv.avail === 'available'
                            ? '#14472B'
                            : inv.avail === 'low_stock'
                            ? '#5A3D00'
                            : '#3E4A43',
                        border:
                          inv.avail === 'available'
                            ? '1px solid #B9D8C4'
                            : inv.avail === 'low_stock'
                            ? '1px solid #EBCB7A'
                            : '1px solid #C9C4B2',
                      }}
                    >
                      {inv.avail}
                    </span>
                  </td>
                  <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                    {inv.flag !== 'None' && inv.flag.split(', ').map((f, j) => (
                      <React.Fragment key={j}>
                        {j > 0 && ' '}
                        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: f.includes('Out') ? colors.dangerTint : colors.accentTint, color: f.includes('Out') ? '#7A1710' : '#5A3D00', border: f.includes('Out') ? '1px solid #E0A09B' : '1px solid #EBCB7A' }}>
                          {f}
                        </span>
                      </React.Fragment>
                    ))}
                    {inv.flag === 'None' && 'None'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* Bottom two-column layout */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', alignItems: 'start', marginTop: '32px' }}>
          {/* Review sentiment */}
          <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <caption id="sent-title" style={{ textAlign: 'left', fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 600, paddingBottom: '10px' }}>
                Review sentiment by category
              </caption>
              <thead>
                <tr>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Category</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>positive</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>neutral</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>negative</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { category: 'Fresh Fruits', positive: 412, neutral: 64, negative: 18 },
                  { category: 'Fresh Vegetables', positive: 388, neutral: 71, negative: 34 },
                  { category: 'Dairy & Eggs', positive: 201, neutral: 39, negative: 12 },
                  { category: 'Bakery', positive: 96, neutral: 30, negative: 21 },
                ].map((cat, i) => (
                  <tr key={i}>
                    <th scope="row" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontWeight: 400, fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {cat.category}
                    </th>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {cat.positive}
                    </td>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {cat.neutral}
                    </td>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {cat.negative}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <h3 style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '18px', fontWeight: 600, marginTop: '16px', margin: 0 }}>
              Flagged products (negative sentiment)
            </h3>
            <ul style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '8px', margin: 0, padding: 0, listStyle: 'none' }}>
              {[
                'Romaine Lettuce | prod-014 | 7 of 11 reviews',
                'Sourdough Bread | prod-020 | 9 of 30 reviews',
                'Curly Kale | prod-013 | 6 of 19 reviews',
              ].map((item, i) => (
                <li key={i}>
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: colors.dangerTint, color: '#7A1710', border: '1px solid #E0A09B' }}>
                    negative
                  </span>
                  {' '}
                  {item}
                </li>
              ))}
            </ul>
          </section>

          {/* Notification performance */}
          <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <caption id="nf-title" style={{ textAlign: 'left', fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 600, paddingBottom: '10px' }}>
                Notification performance, last 24 hours
              </caption>
              <thead>
                <tr>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Channel</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>sent</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>pending</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>failed</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { channel: 'push', sent: 5210, pending: 34, failed: 61 },
                  { channel: 'email', sent: 2840, pending: 12, failed: 104 },
                  { channel: 'in_app', sent: 6120, pending: 0, failed: 3 },
                ].map((ch, i) => (
                  <tr key={i}>
                    <th scope="row" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontWeight: 400, fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {ch.channel}
                    </th>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {ch.sent.toLocaleString()}
                    </td>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {ch.pending}
                    </td>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {ch.failed}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '16px' }}>
              <caption style={{ textAlign: 'left', fontFamily: "'Fraunces', Georgia, serif", fontSize: '18px', fontWeight: 600, paddingBottom: '10px' }}>
                By type
              </caption>
              <thead>
                <tr>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Type</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>sent</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>pending</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '13px', background: colors.surfaceAlt }}>failed</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { type: 'order_update', sent: 4020, pending: 8, failed: 22 },
                  { type: 'delivery_update', sent: 3310, pending: 19, failed: 31 },
                  { type: 'ai_suggestion', sent: 2460, pending: 6, failed: 18 },
                  { type: 'promotion', sent: 2180, pending: 9, failed: 74 },
                  { type: 'restock_alert', sent: 930, pending: 3, failed: 11 },
                  { type: 'expiry_reminder', sent: 1270, pending: 1, failed: 12 },
                ].map((ty, i) => (
                  <tr key={i}>
                    <th scope="row" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontWeight: 400, fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {ty.type}
                    </th>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {ty.sent.toLocaleString()}
                    </td>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {ty.pending}
                    </td>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                      {ty.failed}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        </div>

        {/* Rule controls section */}
        <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)', marginTop: '32px' }} aria-labelledby="rules-title">
          <h2 id="rules-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '24px', fontWeight: 600, margin: 0 }}>Rule controls</h2>
          <p style={{ fontSize: '14px', color: colors.muted, marginTop: '4px', margin: 0 }}>
            Changes are recorded in the audit log for 180 days.
          </p>
          <p role="status" aria-live="polite" style={{ display: 'flex', gap: '10px', padding: '12px 16px', borderRadius: '6px', border: '1px solid #B9D8C4', fontSize: '15px', background: colors.primaryTint, color: '#14472B', marginTop: '12px', margin: 0 }}>
            Saved: ORGANIC10 status updated. Recorded in the audit log.
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginTop: '16px' }}>
            <form style={{ display: 'flex', flexDirection: 'column', gap: '12px' }} aria-label="Serviceability rule editor">
              <h3 style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '20px', fontWeight: 600, margin: 0 }}>
                Serviceability rule
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <label htmlFor="pc" style={{ fontSize: '14px', fontWeight: 600 }}>Serviceable postal codes (one per line)</label>
                <textarea
                  id="pc"
                  name="postalCodes"
                  defaultValue="400001&#10;400021&#10;560001"
                  style={{ border: '1px solid #8A8570', borderRadius: '6px', padding: '10px 12px', fontSize: '16px', background: '#fff', color: colors.ink, width: '100%', minHeight: '72px' }}
                />
              </div>
              <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', minHeight: '44px', fontWeight: 600 }}>
                <input type="checkbox" checked readOnly style={{ width: '22px', height: '22px', accentColor: colors.primary }} />
                Rule enabled
              </label>
              <button type="submit" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.primary, color: '#fff', fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                Save change
              </button>
            </form>

            <form style={{ display: 'flex', flexDirection: 'column', gap: '12px' }} aria-label="Promotion status control">
              <h3 style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '20px', fontWeight: 600, margin: 0 }}>
                Promotion status
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <label htmlFor="pcode" style={{ fontSize: '14px', fontWeight: 600 }}>Promotion</label>
                <select id="pcode" style={{ border: '1px solid #8A8570', borderRadius: '6px', padding: '0 12px', fontSize: '16px', background: '#fff', color: colors.ink, width: '100%', height: '44px' }}>
                  <option>ORGANIC10</option>
                  <option>GREEN10</option>
                  <option>FREEDEL</option>
                  <option>FIRSTORDER</option>
                  <option>BUY2GET1</option>
                </select>
              </div>
              <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', minHeight: '44px', fontWeight: 600 }}>
                <input type="checkbox" checked readOnly style={{ width: '22px', height: '22px', accentColor: colors.primary }} />
                Active
              </label>
              <button type="submit" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.primary, color: '#fff', fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                Save change
              </button>
            </form>

            <form style={{ display: 'flex', flexDirection: 'column', gap: '12px' }} aria-label="Slot capacity control">
              <h3 style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '20px', fontWeight: 600, margin: 0 }}>
                Slot capacity
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <label htmlFor="sl" style={{ fontSize: '14px', fontWeight: 600 }}>Slot</label>
                <select id="sl" style={{ border: '1px solid #8A8570', borderRadius: '6px', padding: '0 12px', fontSize: '16px', background: '#fff', color: colors.ink, width: '100%', height: '44px' }}>
                  <option>Mumbai-South, 9:00 to 11:00 AM</option>
                  <option>Mumbai-South, 12:00 to 2:00 PM</option>
                  <option>Bengaluru-Central, 9:00 to 11:00 AM</option>
                </select>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <label htmlFor="cap" style={{ fontSize: '14px', fontWeight: 600 }}>Maximum orders</label>
                <input
                  id="cap"
                  name="maxCapacity"
                  type="number"
                  min="1"
                  defaultValue="50"
                  style={{ border: '1px solid #8A8570', borderRadius: '6px', padding: '0 12px', fontSize: '16px', background: '#fff', color: colors.ink, width: '100%', height: '44px' }}
                />
              </div>
              <button type="submit" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.primary, color: '#fff', fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                Save change
              </button>
            </form>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer style={{ background: colors.surfaceAlt, borderTop: `1px solid ${colors.border}`, padding: '24px 64px', color: colors.muted, fontSize: '14px' }}>
        <p style={{ margin: 0 }}>Delivering in Mumbai and Bengaluru only.</p>
        <p style={{ marginTop: '4px', margin: 0 }}>Prices in INR. Freshness information is indicative and based on harvest and expiry data.</p>
      </footer>
    </div>
  );
}
