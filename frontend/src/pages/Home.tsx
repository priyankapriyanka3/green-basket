import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { colors } from '../styles/colors';
import { typography } from '../styles/typography';
import { accessibility } from '../styles/accessibility';
import { FreshnessChip } from '../components/FreshnessChip';
import { RecommendationCard } from '../components/RecommendationCard';
import apiClient from '../api/client';
import type { BootstrapResponse } from '../api/types';

export const Home: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [bootstrapData, setBootstrapData] = useState<BootstrapResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchBootstrapData = useCallback(async () => {
    try {
      const response = await apiClient.get<BootstrapResponse>('/app/bootstrap');
      setBootstrapData(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchBootstrapData();
  }, [fetchBootstrapData]);

  if (loading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <p>Loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <p style={{ color: colors.status.errorText }}>Error: {error}</p>
      </div>
    );
  }

  const { profile, defaultAddress, featuredCategories, recommendations, shoppingLists } = bootstrapData || {};

  const tileColors = ['#F7E7A8', '#CFE5C4', '#F2D6B8', '#DCE9D2', '#F6C9C0', '#E8DDF0'];

  return (
    <div
      style={{
        width: '100%',
        minWidth: '1440px',
        background: colors.background,
      }}
    >
      {/* Skip Link */}
      <a
        href="#main"
        style={{
          display: 'block',
          padding: '8px 64px',
          background: colors.primaryDark,
          color: '#fff',
          fontSize: '14px',
          textDecoration: 'none',
        }}
      >
        Skip to main content
      </a>

      {/* Header */}
      <header
        style={{
          background: colors.primaryDark,
          color: '#fff',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '20px',
            padding: '14px 64px',
          }}
        >
          <a
            href="/shop"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              fontFamily: typography.fontFamilies.display,
              fontWeight: 700,
              fontSize: '22px',
              color: '#fff',
              textDecoration: 'none',
            }}
          >
            <span
              style={{
                width: '36px',
                height: '36px',
                borderRadius: '10px',
                background: colors.accent,
                color: colors.accentInk,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '20px',
              }}
            >
              G
            </span>
            GreenBasket AI
          </a>

          <form
            style={{
              flex: 1,
              maxWidth: '460px',
              display: 'flex',
            }}
            role="search"
            onSubmit={(e) => {
              e.preventDefault();
              navigate('/shop/categories');
            }}
          >
            <label htmlFor="q" style={{ position: 'absolute', left: '-9999px' }}>
              Search products
            </label>
            <input
              id="q"
              name="q"
              type="search"
              title="Search fruit, vegetables, dairy"
              style={{
                flex: 1,
                height: `${accessibility.minTouchTarget}px`,
                border: 0,
                borderRadius: '6px 0 0 6px',
                padding: '0 14px',
                fontSize: '16px',
                fontFamily: typography.fontFamilies.body,
              }}
            />
            <button
              type="submit"
              style={{
                height: `${accessibility.minTouchTarget}px`,
                border: 0,
                borderRadius: '0 6px 6px 0',
                background: colors.accent,
                color: colors.accentInk,
                fontFamily: typography.fontFamilies.body,
                fontWeight: 700,
                fontSize: '15px',
                padding: '0 18px',
                cursor: 'pointer',
              }}
            >
              Search
            </button>
          </form>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <a
              href="/account"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                minHeight: `${accessibility.minTouchTarget}px`,
                padding: '0 14px',
                borderRadius: '999px',
                border: '1px solid rgba(255, 255, 255, 0.55)',
                color: '#fff',
                fontSize: '14px',
                fontWeight: 600,
                textDecoration: 'none',
              }}
            >
              {defaultAddress ? `${defaultAddress.label}, ${defaultAddress.postalCode}` : 'Address'} |{' '}
              {defaultAddress?.serviceability.isServiceable ? 'Serviceable' : 'Not serviceable'}
            </a>
            <a
              href="/account/notifications"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                minHeight: `${accessibility.minTouchTarget}px`,
                padding: '0 14px',
                borderRadius: '999px',
                border: '1px solid rgba(255, 255, 255, 0.55)',
                color: '#fff',
                fontSize: '14px',
                fontWeight: 600,
                textDecoration: 'none',
              }}
              aria-label="Notifications, 2 unread"
            >
              Alerts 2
            </a>
            <a
              href="/account/loyalty"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                minHeight: `${accessibility.minTouchTarget}px`,
                padding: '0 14px',
                borderRadius: '999px',
                border: `1px solid ${colors.accent}`,
                background: colors.accent,
                color: colors.accentInk,
                fontSize: '14px',
                fontWeight: 600,
                textDecoration: 'none',
              }}
            >
              {profile?.loyaltyPoints || 0} pts
            </a>
            <a
              href="/shop/cart"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                minHeight: `${accessibility.minTouchTarget}px`,
                padding: '0 14px',
                borderRadius: '999px',
                border: '1px solid rgba(255, 255, 255, 0.55)',
                color: '#fff',
                fontSize: '14px',
                fontWeight: 600,
                textDecoration: 'none',
              }}
              aria-label="Cart, 3 items, ₹185.00"
            >
              Cart 3 | ₹185.00
            </a>
            <button
              onClick={logout}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                minHeight: `${accessibility.minTouchTarget}px`,
                padding: '0 14px',
                borderRadius: '999px',
                border: '1px solid rgba(255, 255, 255, 0.55)',
                background: 'transparent',
                color: '#fff',
                fontSize: '14px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Logout
            </button>
          </div>
        </div>

        <nav
          style={{
            display: 'flex',
            gap: '8px',
            padding: '0 64px 12px',
          }}
          aria-label="Primary"
        >
          {['Home', 'Categories', 'Lists', 'Orders', 'Account'].map((item) => (
            <a
              key={item}
              href={item === 'Home' ? '/shop' : `/shop/${item.toLowerCase()}`}
              aria-current={item === 'Home' ? 'page' : undefined}
              style={{
                color: '#fff',
                textDecoration: 'none',
                fontWeight: 600,
                fontSize: '16px',
                minHeight: `${accessibility.minTouchTarget}px`,
                display: 'inline-flex',
                alignItems: 'center',
                padding: '0 16px',
                borderRadius: '6px',
                background: item === 'Home' ? '#fff' : 'transparent',
                ...(item === 'Home' && { color: colors.primaryDark }),
              }}
            >
              {item}
            </a>
          ))}
        </nav>
      </header>

      {/* Main Content */}
      <main id="main" style={{ padding: '32px 64px 48px' }}>
        {/* Greeting Section */}
        <section
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '24px',
            padding: '28px 32px',
            borderRadius: '8px',
            background: colors.status.freshBg,
            border: `1px solid ${colors.status.freshBorder}`,
          }}
          aria-labelledby="greet-title"
        >
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <h1
              id="greet-title"
              style={{
                fontSize: '34px',
                fontFamily: typography.fontFamilies.display,
                fontWeight: 600,
                margin: 0,
              }}
            >
              Good morning, {profile?.name || 'Guest'}
            </h1>
            <p style={{ color: colors.muted, margin: 0 }}>
              Your Friday delivery is open for booking. Here is what is fresh and what you usually reorder.
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              <FreshnessChip
                type="fresh"
                text={`Serviceable: ${defaultAddress?.serviceability.serviceZone || 'Unknown'} ${defaultAddress?.postalCode || ''}`}
              />
              <FreshnessChip type="fresh" text="Next slot: Fri 16 Oct, 9:00 AM to 11:00 AM" />
              <FreshnessChip type="warning" text={`${profile?.loyaltyPoints || 0} loyalty points`} />
            </div>
          </div>
          <a
            href="/shop/cart"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              minHeight: `${accessibility.minTouchTarget}px`,
              padding: '0 20px',
              borderRadius: '6px',
              border: `1px solid ${colors.primary}`,
              background: colors.primary,
              color: '#fff',
              fontFamily: typography.fontFamilies.body,
              fontWeight: 600,
              fontSize: '15px',
              textDecoration: 'none',
            }}
          >
            Go to cart (3 items)
          </a>
        </section>

        {/* Reorder Prompt */}
        <section
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '24px',
            background: colors.status.warningBg,
            border: `1px solid ${colors.status.warningBorder}`,
            borderRadius: '8px',
            padding: '20px 24px',
            marginTop: '40px',
          }}
          aria-labelledby="reorder-title"
        >
          <div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
              <h2
                id="reorder-title"
                style={{
                  fontSize: '24px',
                  fontFamily: typography.fontFamilies.display,
                  fontWeight: 600,
                  margin: 0,
                }}
              >
                Reorder in one tap
              </h2>
              <span
                style={{
                  display: 'inline-flex',
                  padding: '2px 10px',
                  borderRadius: '999px',
                  fontSize: '13px',
                  fontWeight: 600,
                  background: colors.surface,
                  color: colors.primaryDark,
                  border: `1px solid ${colors.primary}`,
                }}
              >
                Reorder reminder
              </span>
              <FreshnessChip type="warning" text="AI suggested" />
            </div>
            <p style={{ color: '#4F3600', marginTop: '4px', fontSize: '14px' }}>
              You buy these every Sunday.
            </p>
            <ul
              style={{
                display: 'flex',
                gap: '8px',
                flexWrap: 'wrap',
                marginTop: '8px',
                listStyle: 'none',
                padding: 0,
              }}
              aria-label="Items in the reorder bundle"
            >
              {['Organic Bananas, 1 dozen', 'Spinach, 250 g', 'Carrots, 500 g', 'Toned Milk, 1 L', 'Whole Wheat Bread, 400 g'].map(
                (item) => (
                  <li key={item}>
                    <FreshnessChip type="fresh" text={item} />
                  </li>
                )
              )}
            </ul>
          </div>
          <a
            href="/shop/cart"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              minHeight: `${accessibility.minTouchTarget}px`,
              padding: '0 20px',
              borderRadius: '6px',
              border: `1px solid ${colors.primary}`,
              background: colors.primary,
              color: '#fff',
              fontFamily: typography.fontFamilies.body,
              fontWeight: 600,
              fontSize: '15px',
              textDecoration: 'none',
              whiteSpace: 'nowrap',
            }}
          >
            Add all 5 to cart
          </a>
        </section>

        {/* Recommendations */}
        <section style={{ marginTop: '40px' }} aria-labelledby="rec-title">
          <div
            style={{
              display: 'flex',
              alignItems: 'baseline',
              justifyContent: 'space-between',
              gap: '16px',
              marginBottom: '16px',
            }}
          >
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
              <h2
                id="rec-title"
                style={{
                  fontSize: '26px',
                  fontFamily: typography.fontFamilies.display,
                  fontWeight: 600,
                  margin: 0,
                }}
              >
                Recommended for you
              </h2>
              <FreshnessChip type="warning" text="AI suggested" />
            </div>
            <a
              href="/shop/categories"
              style={{
                color: colors.primary,
                fontWeight: 600,
                textDecoration: 'none',
              }}
            >
              Browse all products
            </a>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '16px',
            }}
          >
            {recommendations && recommendations.length > 0 ? (
              recommendations.slice(0, 6).map((rec, index) => (
                <RecommendationCard
                  key={rec.recommendationId}
                  productId={rec.productId}
                  name={`Product ${rec.productId}`}
                  priceInr="65.00"
                  unit="1 dozen"
                  isOrganic={index % 2 === 0}
                  reasonTag={rec.reasonTag}
                  reasonText={rec.reasonText}
                  freshness={{
                    expiryDays: 4,
                    harvestDate: '13 Oct',
                    stockLevel: 'available',
                  }}
                  tileColor={tileColors[index % tileColors.length]}
                  onAdd={() => console.log('Add to cart')}
                  onAddToList={() => console.log('Add to list')}
                />
              ))
            ) : (
              <p style={{ color: colors.muted }}>No recommendations available</p>
            )}
          </div>
        </section>

        {/* Featured Categories */}
        <section style={{ marginTop: '40px' }} aria-labelledby="cat-title">
          <div
            style={{
              display: 'flex',
              alignItems: 'baseline',
              justifyContent: 'space-between',
              marginBottom: '16px',
            }}
          >
            <h2
              id="cat-title"
              style={{
                fontSize: '26px',
                fontFamily: typography.fontFamilies.display,
                fontWeight: 600,
                margin: 0,
              }}
            >
              Featured categories
            </h2>
            <a href="/shop/categories" style={{ color: colors.primary, fontWeight: 600 }}>
              See all categories
            </a>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '16px' }}>
            {featuredCategories && featuredCategories.length > 0 ? (
              featuredCategories.slice(0, 5).map((cat) => (
                <a
                  key={cat.categoryId}
                  href={`/shop/categories/${cat.categoryId}`}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px',
                    textDecoration: 'none',
                    color: colors.ink,
                    padding: '20px',
                    borderRadius: '8px',
                    background: colors.surface,
                    border: `1px solid ${colors.border}`,
                    minHeight: '96px',
                  }}
                >
                  <strong
                    style={{
                      fontFamily: typography.fontFamilies.display,
                      fontWeight: 600,
                      fontSize: '18px',
                    }}
                  >
                    {cat.name}
                  </strong>
                  <span style={{ color: colors.muted, fontSize: '14px', fontWeight: 400 }}>
                    142 items
                  </span>
                </a>
              ))
            ) : (
              <p style={{ color: colors.muted }}>No categories available</p>
            )}
          </div>
        </section>

        {/* Two-column layout: Lists and Orders/Notifications */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px', marginTop: '40px' }}>
          {/* Shopping Lists */}
          <section aria-labelledby="lists-title">
            <div
              style={{
                display: 'flex',
                alignItems: 'baseline',
                justifyContent: 'space-between',
                marginBottom: '16px',
              }}
            >
              <h2
                id="lists-title"
                style={{
                  fontSize: '26px',
                  fontFamily: typography.fontFamilies.display,
                  fontWeight: 600,
                  margin: 0,
                }}
              >
                Your lists
              </h2>
              <a href="/planner/lists" style={{ color: colors.primary, fontWeight: 600 }}>
                Manage lists
              </a>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
              {shoppingLists && shoppingLists.length > 0 ? (
                shoppingLists.slice(0, 2).map((list) => (
                  <article
                    key={list.listId}
                    style={{
                      background: colors.surface,
                      border: `1px solid ${colors.border}`,
                      borderRadius: '8px',
                      padding: '24px',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '8px',
                    }}
                  >
                    <h3
                      style={{
                        fontSize: '20px',
                        fontFamily: typography.fontFamilies.display,
                        fontWeight: 600,
                        margin: 0,
                      }}
                    >
                      {list.name}
                    </h3>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
                      <FreshnessChip
                        type={list.isAiGenerated ? 'warning' : 'unavailable'}
                        text={list.isAiGenerated ? 'AI generated' : 'Manual list'}
                      />
                      <span style={{ fontSize: '14px', color: colors.muted }}>
                        {list.itemCount} items
                      </span>
                    </div>
                    <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>
                      {list.suggestionNote || 'Your custom shopping list'}
                    </p>
                    <a
                      href={`/shop/lists/${list.listId}`}
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        minHeight: `${accessibility.minTouchTarget}px`,
                        padding: '0 20px',
                        borderRadius: '6px',
                        border: `1px solid ${colors.primary}`,
                        background: colors.surface,
                        color: colors.primary,
                        fontFamily: typography.fontFamilies.body,
                        fontWeight: 600,
                        fontSize: '15px',
                        textDecoration: 'none',
                      }}
                      aria-label={`Open list ${list.name}`}
                    >
                      {list.isAiGenerated ? 'Review and edit' : 'Open list'}
                    </a>
                  </article>
                ))
              ) : (
                <p style={{ color: colors.muted }}>No lists available</p>
              )}
            </div>
          </section>

          {/* Orders and Notifications Sidebar */}
          <aside style={{ display: 'flex', flexDirection: 'column', gap: '12px' }} aria-label="Order and notifications">
            <section
              style={{
                background: colors.surface,
                border: `1px solid ${colors.border}`,
                borderRadius: '8px',
                padding: '24px',
              }}
              aria-labelledby="ord-title"
            >
              <h2
                id="ord-title"
                style={{
                  fontSize: '22px',
                  fontFamily: typography.fontFamilies.display,
                  fontWeight: 600,
                  margin: 0,
                }}
              >
                Latest order
              </h2>
              <div
                style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginTop: '8px',
                }}
              >
                <strong>Order ord-001</strong>
                <FreshnessChip type="fresh" text="confirmed" />
              </div>
              <p style={{ fontSize: '14px', color: colors.muted, margin: '4px 0 0' }}>
                Fri 16 Oct, 9:00 AM to 11:00 AM | ₹170.00
              </p>
              <div style={{ display: 'flex', gap: '6px', marginTop: '8px' }} aria-hidden="true">
                {[1, 2, 0, 0].map((filled, i) => (
                  <span
                    key={i}
                    style={{
                      flex: 1,
                      height: '8px',
                      borderRadius: '4px',
                      background: filled ? colors.primary : colors.border,
                    }}
                  />
                ))}
              </div>
              <a
                href="/shop/orders/ord-001"
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  minHeight: `${accessibility.minTouchTarget}px`,
                  padding: '0 20px',
                  borderRadius: '6px',
                  border: `1px solid ${colors.primary}`,
                  background: colors.surface,
                  color: colors.primary,
                  fontFamily: typography.fontFamilies.body,
                  fontWeight: 600,
                  fontSize: '15px',
                  textDecoration: 'none',
                  marginTop: '12px',
                  width: '100%',
                }}
              >
                Track order
              </a>
            </section>

            <section
              style={{
                background: colors.surface,
                border: `1px solid ${colors.border}`,
                borderRadius: '8px',
                padding: '24px',
              }}
              aria-labelledby="nt-title"
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2
                  id="nt-title"
                  style={{
                    fontSize: '22px',
                    fontFamily: typography.fontFamilies.display,
                    fontWeight: 600,
                    margin: 0,
                  }}
                >
                  Notifications
                </h2>
                <FreshnessChip type="warning" text="2 unread" />
              </div>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ paddingTop: '12px', borderTop: 0 }}>
                  <strong>Order ord-001 is confirmed</strong>
                  <p style={{ fontSize: '14px', color: colors.muted, margin: '4px 0 0' }}>
                    Payment received. Delivery Fri 16 Oct.
                  </p>
                </li>
                <li style={{ paddingTop: '12px', borderTop: `1px solid ${colors.border}`, marginTop: '12px' }}>
                  <strong>Reorder carrots?</strong> <FreshnessChip type="warning" text="AI suggested" />
                  <p style={{ fontSize: '14px', color: colors.muted, margin: '4px 0 0' }}>
                    You buy these every Sunday.
                  </p>
                </li>
              </ul>
              <a
                href="/account/notifications"
                style={{
                  display: 'block',
                  marginTop: '12px',
                  color: colors.primary,
                  fontWeight: 600,
                  textDecoration: 'none',
                }}
              >
                Open all notifications
              </a>
            </section>
          </aside>
        </div>
      </main>

      {/* Footer */}
      <footer
        style={{
          background: colors.surfaceAlt,
          borderTop: `1px solid ${colors.border}`,
          padding: '24px 64px',
          color: colors.muted,
          fontSize: '14px',
        }}
      >
        <p style={{ margin: 0 }}>Delivering in Mumbai and Bengaluru only.</p>
        <p style={{ marginTop: '4px' }}>
          Prices in INR. Freshness information is indicative and based on harvest and expiry data.
        </p>
      </footer>
    </div>
  );
};
