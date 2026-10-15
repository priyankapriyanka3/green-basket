import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { colors } from '../styles/colors';

interface Address {
  address_id: string;
  label: string;
  street: string;
  postal_code: string;
  serviceability_status: 'serviceable' | 'not_serviceable';
  zone?: string;
  is_default: boolean;
}

interface Notification {
  notification_id: string;
  type: string;
  title: string;
  message: string;
  channel: 'push' | 'email' | 'in_app';
  is_read: boolean;
  dispatch_status: 'pending' | 'sent' | 'failed';
  created_at: string;
}

interface Review {
  product_name: string;
  order_id: string;
  rating: number;
  sentiment: 'positive' | 'neutral' | 'negative';
  review_text: string;
  reviewed_at: string;
}

export default function ProfileNotifications() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<'profile' | 'addresses' | 'notifications' | 'preferences' | 'reviews'>('notifications');
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      // Mock data for wireframe fidelity
      setAddresses([
        {
          address_id: 'addr-001',
          label: 'Home',
          street: 'Flat 12, Marine Drive, Mumbai 400001',
          postal_code: '400001',
          serviceability_status: 'serviceable',
          zone: 'Mumbai-South 400001',
          is_default: true,
        },
        {
          address_id: 'addr-002',
          label: 'Work',
          street: '4th Floor, Nariman Point, Mumbai 400021',
          postal_code: '400021',
          serviceability_status: 'serviceable',
          zone: 'Mumbai-South 400021',
          is_default: false,
        },
        {
          address_id: 'addr-003',
          label: "Parents' home",
          street: 'B-22, Vasant Vihar, Delhi 110057',
          postal_code: '110057',
          serviceability_status: 'not_serviceable',
          is_default: false,
        },
      ]);

      setNotifications([
        {
          notification_id: 'ntf-001',
          type: 'order_update',
          title: 'Order ord-001 is confirmed',
          message: 'Payment received. Delivery Fri 16 Oct, 9:00 AM to 11:00 AM.',
          channel: 'push',
          is_read: false,
          dispatch_status: 'sent',
          created_at: '2026-10-15T20:13:00Z',
        },
        {
          notification_id: 'ntf-002',
          type: 'ai_suggestion',
          title: 'Reorder carrots?',
          message: 'You buy these every Sunday.',
          channel: 'in_app',
          is_read: false,
          dispatch_status: 'sent',
          created_at: '2026-10-15T18:30:00Z',
        },
        {
          notification_id: 'ntf-003',
          type: 'delivery_update',
          title: 'Rajesh is about 30 minutes away',
          message: 'Your delivery agent is on the way.',
          channel: 'push',
          is_read: true,
          dispatch_status: 'pending',
          created_at: '2026-10-14T14:00:00Z',
        },
        {
          notification_id: 'ntf-004',
          type: 'promotion',
          title: 'ORGANIC10: 10% off organic products',
          message: 'Valid on orders above ₹200.00 this week.',
          channel: 'email',
          is_read: true,
          dispatch_status: 'sent',
          created_at: '2026-10-12T10:00:00Z',
        },
        {
          notification_id: 'ntf-005',
          type: 'restock_alert',
          title: 'Alphonso Mangoes are back in stock',
          message: 'Available for Mumbai-South delivery.',
          channel: 'push',
          is_read: true,
          dispatch_status: 'sent',
          created_at: '2026-10-11T09:00:00Z',
        },
        {
          notification_id: 'ntf-006',
          type: 'expiry_reminder',
          title: 'Sourdough bread expires tomorrow',
          message: 'Use or reorder fresh loaves from your list.',
          channel: 'email',
          is_read: true,
          dispatch_status: 'failed',
          created_at: '2026-10-10T08:00:00Z',
        },
      ]);

      setReviews([
        {
          product_name: 'Organic Bananas',
          order_id: 'ord-001',
          rating: 5,
          sentiment: 'positive',
          review_text: 'Sweet and just ripe enough. Stayed fresh through the weekend.',
          reviewed_at: '2026-10-16',
        },
        {
          product_name: 'Spinach',
          order_id: 'ord-000',
          rating: 4,
          sentiment: 'positive',
          review_text: 'Fresh and crisp, a few leaves were wilted.',
          reviewed_at: '2026-10-09',
        },
        {
          product_name: 'Whole Wheat Bread',
          order_id: 'ord-000',
          rating: 3,
          sentiment: 'neutral',
          review_text: 'Good taste but it was a day old on arrival.',
          reviewed_at: '2026-10-09',
        },
      ]);
    } catch (err) {
      console.error('Failed to load data:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffHours < 24) {
      return `${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')} ${date.getHours() >= 12 ? 'PM' : 'AM'}`;
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else {
      return `${date.getDate()} ${date.toLocaleString('en-IN', { month: 'short' })}`;
    }
  };

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  if (loading) {
    return (
      <div style={{ padding: '32px 64px' }}>
        <p>Loading account information...</p>
      </div>
    );
  }

  return (
    <div style={{ background: colors.background, minHeight: '100vh' }}>
      {/* Header */}
      <header style={{ background: colors.primaryDark, color: '#fff' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '20px', padding: '14px 64px' }}>
          <a href="/shop" style={{ display: 'flex', alignItems: 'center', gap: '10px', fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 700, color: '#fff', textDecoration: 'none' }}>
            <span style={{ width: '36px', height: '36px', borderRadius: '10px', background: colors.accent, color: colors.accentInk, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px', fontWeight: 700 }}>G</span>
            GreenBasket AI
          </a>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <a href="/account" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', minHeight: '44px', padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,.55)', color: '#fff', fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>
              Home, 400001 | Serviceable
            </a>
            <a href="/account" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', minHeight: '44px', padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,.55)', color: '#fff', fontSize: '14px', fontWeight: 600, textDecoration: 'none' }} aria-label="Notifications, 2 unread">
              Alerts 2
            </a>
            <a href="/account" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', minHeight: '44px', padding: '0 14px', borderRadius: '999px', background: colors.accent, color: colors.accentInk, border: `1px solid ${colors.accent}`, fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>
              420 pts
            </a>
            <a href="/shop/cart" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', minHeight: '44px', padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,.55)', color: '#fff', fontSize: '14px', fontWeight: 600, textDecoration: 'none' }} aria-label="Cart, 3 items, ₹185.00">
              Cart 3 | ₹185.00
            </a>
          </div>
        </div>
        <nav style={{ display: 'flex', gap: '8px', padding: '0 64px 12px' }} aria-label="Primary">
          <a href="/shop" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Home</a>
          <a href="/shop/categories" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Categories</a>
          <a href="/planner/lists" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Lists</a>
          <a href="/account/orders" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Orders</a>
          <a href="/account" style={{ background: '#fff', color: colors.primaryDark, textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }} aria-current="page">Account</a>
        </nav>
      </header>

      {/* Main content */}
      <main style={{ padding: '32px 64px 48px' }}>
        <h1 style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '36px', fontWeight: 600, lineHeight: 1.2, margin: 0 }}>Account</h1>
        <p style={{ color: colors.muted, marginTop: '6px', margin: 0 }}>Manage your details, addresses and how GreenBasket AI contacts you.</p>

        {/* Tabs */}
        <div role="tablist" aria-label="Account sections" style={{ display: 'flex', gap: '4px', borderBottom: `2px solid ${colors.border}`, marginTop: '20px' }}>
          {(['profile', 'addresses', 'notifications', 'preferences', 'reviews'] as const).map((tab) => (
            <a
              key={tab}
              role="tab"
              href="#"
              onClick={(e) => { e.preventDefault(); setActiveTab(tab); }}
              aria-selected={activeTab === tab ? 'true' : 'false'}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                minHeight: '48px',
                padding: '0 20px',
                textDecoration: 'none',
                color: activeTab === tab ? colors.primaryDark : colors.muted,
                border: activeTab === tab ? `2px solid ${colors.border}` : '2px solid transparent',
                borderBottom: 0,
                borderRadius: '8px 8px 0 0',
                fontWeight: 600,
                fontSize: '16px',
                background: activeTab === tab ? colors.surface : 'transparent',
                marginBottom: activeTab === tab ? '-2px' : 0,
                borderBottomColor: activeTab === tab ? colors.surface : undefined,
              }}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
              {tab === 'notifications' && unreadCount > 0 && (
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: colors.accent, color: colors.accentInk, marginLeft: '8px' }}>
                  {unreadCount} unread
                </span>
              )}
            </a>
          ))}
        </div>

        {/* Two-column layout */}
        <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 1fr', gap: '24px', alignItems: 'start', marginTop: '24px' }}>
          {/* Left column */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {/* Profile section */}
            <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }} aria-labelledby="pf-title">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
                <h2 id="pf-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '24px', fontWeight: 600, margin: 0 }}>Profile</h2>
                <span style={{ display: 'inline-flex', gap: '6px', alignItems: 'center', fontSize: '13px', fontWeight: 600, color: '#14472B', background: colors.primaryTint, border: '1px solid #B9D8C4', borderRadius: '999px', padding: '2px 10px' }}>
                  Only you can see this
                </span>
              </div>
              <dl style={{ margin: 0, marginTop: '8px' }}>
                {[
                  { term: 'Name', desc: 'Ananya Sharma' },
                  { term: 'Phone', desc: '+91 98765 43210' },
                  { term: 'Preferred language', desc: 'English (India)' },
                  { term: 'Dietary preference', desc: 'Vegetarian' },
                  { term: 'Allergies', desc: 'Peanut' },
                  { term: 'Customer id', desc: 'cust-001' },
                ].map((item) => (
                  <div key={item.term} style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: `1px solid ${colors.border}` }}>
                    <dt style={{ color: colors.muted, margin: 0 }}>{item.term}</dt>
                    <dd style={{ margin: 0, fontWeight: 600, textAlign: 'right' }}>{item.desc}</dd>
                  </div>
                ))}
              </dl>
              <div style={{ display: 'flex', flexWrap: 'wrap', marginTop: '16px' }}>
                <button style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.primary, color: '#fff', fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                  Edit profile
                </button>
              </div>
            </section>

            {/* Addresses section */}
            <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }} aria-labelledby="ad-title">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
                <h2 id="ad-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '24px', fontWeight: 600, margin: 0 }}>Addresses</h2>
                <button style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.surface, color: colors.primary, fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                  Add address
                </button>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '12px' }}>
                {addresses.map((addr) => (
                  <div
                    key={addr.address_id}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      justifyContent: 'space-between',
                      gap: '16px',
                      border: addr.is_default ? `2px solid ${colors.primary}` : addr.serviceability_status === 'not_serviceable' ? '1px dashed #8A8570' : `1px solid ${colors.border}`,
                      borderRadius: '8px',
                      padding: '16px',
                      background: addr.is_default ? colors.primaryTint : addr.serviceability_status === 'not_serviceable' ? '#F8F6EF' : '#fff',
                    }}
                  >
                    <div>
                      <strong style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '18px', fontWeight: 600 }}>{addr.label}</strong>
                      {addr.is_default && (
                        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: colors.infoTint, color: '#07405F', border: '1px solid #9CC6DD', marginLeft: '8px' }}>
                          Default
                        </span>
                      )}
                      <p style={{ fontSize: '14px', margin: 0 }}>
                        {addr.street}{addr.address_id ? ` | ${addr.address_id}` : ''}
                      </p>
                      {addr.serviceability_status === 'serviceable' ? (
                        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: colors.primaryTint, color: '#14472B', border: '1px solid #B9D8C4' }}>
                          Serviceable: {addr.zone}
                        </span>
                      ) : (
                        <>
                          <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: colors.dangerTint, color: '#7A1710', border: '1px solid #E0A09B' }}>
                            Saved, not serviceable
                          </span>
                          <p style={{ fontSize: '14px', color: colors.muted, marginTop: '6px', margin: 0 }}>
                            We deliver in Mumbai and Bengaluru only. This address stays saved and will work if we start delivering there.
                          </p>
                        </>
                      )}
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                      <button style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 12px', background: 'transparent', borderColor: 'transparent', color: colors.primary, fontSize: '15px', fontWeight: 600, border: 0, cursor: 'pointer' }}>
                        Edit
                      </button>
                      {!addr.is_default && (
                        <button style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.surface, color: colors.primary, fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                          Set as default
                        </button>
                      )}
                      <button style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 12px', background: 'transparent', borderColor: 'transparent', color: '#8A1B14', fontSize: '15px', fontWeight: 600, border: 0, cursor: 'pointer' }}>
                        Remove
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              <p style={{ fontSize: '14px', color: colors.muted, marginTop: '8px', margin: 0 }}>Exactly one address is your default.</p>
            </section>

            {/* Loyalty section */}
            <section style={{ background: colors.accentTint, border: '1px solid #EBCB7A', borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }} aria-labelledby="loy-title">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
                <h2 id="loy-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '24px', fontWeight: 600, margin: 0 }}>Loyalty points</h2>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: colors.accent, color: colors.accentInk }}>
                  420 points
                </span>
              </div>
              <p style={{ marginTop: '6px', margin: 0 }}>Your last order ord-001 will add 17 points after delivery.</p>
              <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>Redeem 100 points for ₹5.00 off in your cart.</p>
            </section>
          </div>

          {/* Right column */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {/* Notifications section */}
            <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }} aria-labelledby="nf-title">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
                <h2 id="nf-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '24px', fontWeight: 600, margin: 0 }}>Notifications</h2>
                <button style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.surface, color: colors.primary, fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                  Mark all as read
                </button>
              </div>
              <form style={{ display: 'flex', flexWrap: 'wrap', marginTop: '12px' }} aria-label="Filter notifications">
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', minWidth: '200px' }}>
                  <label htmlFor="nt" style={{ fontSize: '14px', fontWeight: 600 }}>Type</label>
                  <select id="nt" style={{ border: '1px solid #8A8570', borderRadius: '6px', padding: '0 12px', fontSize: '16px', background: '#fff', color: colors.ink, width: '100%', height: '44px' }}>
                    <option>All types</option>
                    <option>order_update</option>
                    <option>delivery_update</option>
                    <option>ai_suggestion</option>
                    <option>promotion</option>
                    <option>restock_alert</option>
                    <option>expiry_reminder</option>
                  </select>
                </div>
                <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', minHeight: '44px', alignSelf: 'flex-end', marginLeft: '12px' }}>
                  <input type="checkbox" style={{ width: '22px', height: '22px', accentColor: colors.primary }} />
                  Unread only
                </label>
              </form>
              <ul style={{ margin: 0, padding: 0, listStyle: 'none', marginTop: '8px' }}>
                {notifications.map((notif) => (
                  <li
                    key={notif.notification_id}
                    style={{
                      display: 'grid',
                      gridTemplateColumns: '20px 1fr auto',
                      gap: '12px',
                      padding: '14px 4px',
                      borderTop: `1px solid ${colors.border}`,
                      alignItems: 'start',
                    }}
                  >
                    <span
                      aria-hidden="true"
                      style={{
                        width: '12px',
                        height: '12px',
                        borderRadius: '50%',
                        background: notif.is_read ? 'transparent' : colors.info,
                        border: notif.is_read ? '2px solid #8A8570' : undefined,
                        marginTop: '7px',
                      }}
                    />
                    <div>
                      <strong style={{ fontWeight: notif.is_read ? 400 : 700 }}>{notif.title}</strong>
                      {!notif.is_read && (
                        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: colors.infoTint, color: '#07405F', border: '1px solid #9CC6DD', marginLeft: '8px' }}>
                          Unread
                        </span>
                      )}
                      {notif.type === 'ai_suggestion' && (
                        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: colors.accent, color: colors.accentInk, marginLeft: '8px' }}>
                          AI suggested
                        </span>
                      )}
                      <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>
                        {notif.message}
                        {notif.type === 'ai_suggestion' && (
                          <>
                            {' '}
                            <a href="/planner/lists">Open your list</a>
                          </>
                        )}
                      </p>
                      <p style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '4px', margin: 0 }}>
                        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: '#ECEAE2', color: '#3E4A43', border: '1px solid #C9C4B2' }}>
                          {notif.type}
                        </span>
                        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: '#ECEAE2', color: '#3E4A43', border: '1px solid #C9C4B2' }}>
                          {notif.channel}
                        </span>
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
                              notif.dispatch_status === 'sent'
                                ? colors.primaryTint
                                : notif.dispatch_status === 'failed'
                                ? colors.dangerTint
                                : colors.accentTint,
                            color:
                              notif.dispatch_status === 'sent'
                                ? '#14472B'
                                : notif.dispatch_status === 'failed'
                                ? '#7A1710'
                                : '#5A3D00',
                            border:
                              notif.dispatch_status === 'sent'
                                ? '1px solid #B9D8C4'
                                : notif.dispatch_status === 'failed'
                                ? '1px solid #E0A09B'
                                : '1px solid #EBCB7A',
                          }}
                        >
                          {notif.dispatch_status}
                        </span>
                      </p>
                    </div>
                    <span style={{ fontSize: '14px', color: colors.muted }}>
                      {notif.is_read && 'Read | '}
                      {formatTime(notif.created_at)}
                    </span>
                  </li>
                ))}
              </ul>
            </section>

            {/* Preferences section */}
            <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }} aria-labelledby="pref-title">
              <h2 id="pref-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '24px', fontWeight: 600, margin: 0 }}>Channel preferences</h2>
              <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '8px' }}>
                <caption style={{ textAlign: 'left', fontFamily: "'Source Sans 3', 'Segoe UI', system-ui, sans-serif", fontSize: '14px', fontWeight: 400, color: colors.muted, paddingBottom: '10px' }}>
                  Choose how each type of message reaches you.
                </caption>
                <thead>
                  <tr>
                    <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '13px', background: colors.surfaceAlt }}>Notification type</th>
                    <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'center', fontSize: '13px', background: colors.surfaceAlt }}>Push</th>
                    <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'center', fontSize: '13px', background: colors.surfaceAlt }}>Email</th>
                    <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'center', fontSize: '13px', background: colors.surfaceAlt }}>In-app</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { type: 'Order and delivery updates', push: true, email: true, inApp: true },
                    { type: 'AI suggestions', push: false, email: false, inApp: true },
                    { type: 'Promotions', push: false, email: true, inApp: false },
                    { type: 'Restock and expiry alerts', push: true, email: false, inApp: true },
                  ].map((pref, i) => (
                    <tr key={i}>
                      <th scope="row" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', fontWeight: 400, verticalAlign: 'middle' }}>
                        {pref.type}
                      </th>
                      <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'center', fontSize: '14px', verticalAlign: 'middle' }}>
                        <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', minHeight: '44px' }}>
                          <input type="checkbox" checked={pref.push} readOnly aria-label={`Push for ${pref.type}`} style={{ width: '22px', height: '22px', accentColor: colors.primary }} />
                        </label>
                      </td>
                      <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'center', fontSize: '14px', verticalAlign: 'middle' }}>
                        <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', minHeight: '44px' }}>
                          <input type="checkbox" checked={pref.email} readOnly aria-label={`Email for ${pref.type}`} style={{ width: '22px', height: '22px', accentColor: colors.primary }} />
                        </label>
                      </td>
                      <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'center', fontSize: '14px', verticalAlign: 'middle' }}>
                        <label style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', minHeight: '44px' }}>
                          <input type="checkbox" checked={pref.inApp} readOnly aria-label={`In-app for ${pref.type}`} style={{ width: '22px', height: '22px', accentColor: colors.primary }} />
                        </label>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <p style={{ fontSize: '14px', color: colors.muted, marginTop: '8px', margin: 0 }}>
                <strong>Consent for promotions:</strong> Promotional messages are sent only on the channels you tick above. You can change this at any time.
              </p>
              <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>
                Turning off AI suggestions stops these messages. Recommendations on the Home page still show a reason.
              </p>
              <p role="status" style={{ display: 'flex', gap: '10px', padding: '12px 16px', borderRadius: '6px', border: '1px solid #B9D8C4', fontSize: '15px', background: colors.primaryTint, color: '#14472B', marginTop: '12px', margin: 0 }}>
                Preferences saved.
              </p>
            </section>
          </div>
        </div>

        {/* Reviews section */}
        <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)', marginTop: '32px' }} aria-labelledby="rv-title">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
            <h2 id="rv-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '24px', fontWeight: 600, margin: 0 }}>Your reviews</h2>
            <a href="/shop/orders/ord-001">Go to order ord-001</a>
          </div>
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '8px' }}>
            <caption style={{ textAlign: 'left', fontFamily: "'Source Sans 3', 'Segoe UI', system-ui, sans-serif", fontSize: '14px', fontWeight: 400, color: colors.muted, paddingBottom: '10px' }}>
              Reviews you have written, newest first.
            </caption>
            <thead>
              <tr>
                <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', background: colors.surfaceAlt }}>Product</th>
                <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', background: colors.surfaceAlt }}>Order</th>
                <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', background: colors.surfaceAlt }}>Rating</th>
                <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', background: colors.surfaceAlt }}>Sentiment</th>
                <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', background: colors.surfaceAlt }}>Date</th>
                <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', background: colors.surfaceAlt }}>Your review</th>
              </tr>
            </thead>
            <tbody>
              {reviews.map((review, i) => (
                <tr key={i}>
                  <th scope="row" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', fontWeight: 400, verticalAlign: 'top' }}>
                    {review.product_name}
                  </th>
                  <td style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', verticalAlign: 'top' }}>
                    <a href={`/shop/orders/${review.order_id}`}>{review.order_id}</a>
                  </td>
                  <td style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', fontWeight: 700, verticalAlign: 'top' }}>
                    {review.rating} out of 5
                  </td>
                  <td style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', verticalAlign: 'top' }}>
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
                        background: review.sentiment === 'positive' ? colors.primaryTint : review.sentiment === 'neutral' ? '#ECEAE2' : colors.dangerTint,
                        color: review.sentiment === 'positive' ? '#14472B' : review.sentiment === 'neutral' ? '#3E4A43' : '#7A1710',
                        border: review.sentiment === 'positive' ? '1px solid #B9D8C4' : review.sentiment === 'neutral' ? '1px solid #C9C4B2' : '1px solid #E0A09B',
                      }}
                    >
                      {review.sentiment}
                    </span>
                  </td>
                  <td style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', verticalAlign: 'top' }}>
                    {review.reviewed_at}
                  </td>
                  <td style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', verticalAlign: 'top' }}>
                    {review.review_text}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
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
