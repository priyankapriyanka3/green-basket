import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { colors } from '../styles/colors';
import { typography } from '../styles/typography';
import { accessibility } from '../styles/accessibility';
import { ProductCard } from '../components/ProductCard';
import { FreshnessChip } from '../components/FreshnessChip';

export const CategorySearch: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [isOrganic, setIsOrganic] = useState(false);
  const [isFeatured, setIsFeatured] = useState(false);

  const tileColors = ['#CFE5C4', '#F7E7A8', '#F2D6B8', '#DCE9D2', '#F6C9C0', '#E8DDF0', '#D5E7F0', '#EADFC2'];

  const sampleProducts = [
    { id: 'prod-001', name: 'Organic Bananas', price: '65.00', unit: '1 dozen', organic: true, rating: 4.5, reviews: 126, sentiment: 'positive', stock: 'available', harvest: '13 Oct', expiry: 4 },
    { id: 'prod-002', name: 'Alphonso Mangoes', price: '180.00', unit: '1 kg', organic: true, rating: 4.7, reviews: 145, sentiment: 'positive', stock: 'available', harvest: '12 Oct', expiry: 5 },
    { id: 'prod-003', name: 'Red Apples', price: '120.00', unit: '1 kg', organic: false, rating: 4.3, reviews: 98, sentiment: 'positive', stock: 'available', harvest: '11 Oct', expiry: 7 },
    { id: 'prod-004', name: 'Organic Tomatoes', price: '45.00', unit: '500 g', organic: true, rating: 4.4, reviews: 112, sentiment: 'positive', stock: 'available', expiry: 3 },
    { id: 'prod-005', name: 'Spinach', price: '30.00', unit: '250 g', organic: true, rating: 4.4, reviews: 88, sentiment: 'positive', stock: 'available', harvest: '14 Oct', expiry: 2 },
    { id: 'prod-006', name: 'Carrots', price: '35.00', unit: '500 g', organic: false, rating: 4.2, reviews: 76, sentiment: 'positive', stock: 'available', harvest: '13 Oct', expiry: 5 },
    { id: 'prod-007', name: 'Fresh Coriander', price: '15.00', unit: '1 bunch', organic: false, rating: 4.0, reviews: 52, sentiment: 'neutral', stock: 'available', expiry: 1 },
    { id: 'prod-008', name: 'Green Cabbage', price: '40.00', unit: '1 piece', organic: false, rating: 4.2, reviews: 63, sentiment: 'positive', stock: 'available', harvest: '12 Oct', expiry: 6 },
  ];

  return (
    <div style={{ width: '100%', minWidth: '1440px', background: colors.background }}>
      <a href="#main" style={{ display: 'block', padding: '8px 64px', background: colors.primaryDark, color: '#fff', fontSize: '14px', textDecoration: 'none' }}>
        Skip to main content
      </a>

      {/* Header */}
      <header style={{ background: colors.primaryDark, color: '#fff' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '20px', padding: '14px 64px' }}>
          <a href="/shop" style={{ display: 'flex', alignItems: 'center', gap: '10px', fontFamily: typography.fontFamilies.display, fontWeight: 700, fontSize: '22px', color: '#fff', textDecoration: 'none' }}>
            <span style={{ width: '36px', height: '36px', borderRadius: '10px', background: colors.accent, color: colors.accentInk, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px' }}>G</span>
            GreenBasket AI
          </a>
          <form style={{ flex: 1, maxWidth: '460px', display: 'flex' }} role="search">
            <input id="q" type="search" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} style={{ flex: 1, height: `${accessibility.minTouchTarget}px`, border: 0, borderRadius: '6px 0 0 6px', padding: '0 14px', fontSize: '16px' }} />
            <button type="submit" style={{ height: `${accessibility.minTouchTarget}px`, border: 0, borderRadius: '0 6px 6px 0', background: colors.accent, color: colors.accentInk, fontWeight: 700, fontSize: '15px', padding: '0 18px', cursor: 'pointer' }}>Search</button>
          </form>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <a href="/account" style={{ display: 'inline-flex', alignItems: 'center', minHeight: `${accessibility.minTouchTarget}px`, padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,0.55)', color: '#fff', fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>Home, 400001 | Serviceable</a>
            <a href="/account/notifications" style={{ display: 'inline-flex', minHeight: `${accessibility.minTouchTarget}px`, padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,0.55)', color: '#fff', fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>Alerts 2</a>
            <a href="/account/loyalty" style={{ display: 'inline-flex', minHeight: `${accessibility.minTouchTarget}px`, padding: '0 14px', borderRadius: '999px', background: colors.accent, color: colors.accentInk, fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>420 pts</a>
            <a href="/shop/cart" style={{ display: 'inline-flex', minHeight: `${accessibility.minTouchTarget}px`, padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,0.55)', color: '#fff', fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>Cart 3 | ₹185.00</a>
          </div>
        </div>
        <nav style={{ display: 'flex', gap: '8px', padding: '0 64px 12px' }} aria-label="Primary">
          {['Home', 'Categories', 'Lists', 'Orders', 'Account'].map((item) => (
            <a key={item} href={item === 'Home' ? '/shop' : `/shop/${item.toLowerCase()}`} aria-current={item === 'Categories' ? 'page' : undefined} style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px', background: item === 'Categories' ? '#fff' : 'transparent', ...(item === 'Categories' && { color: colors.primaryDark }) }}>{item}</a>
          ))}
        </nav>
      </header>

      <main id="main" style={{ padding: '24px 64px 48px' }}>
        <nav style={{ fontSize: '14px', color: colors.muted, marginBottom: '12px' }} aria-label="Breadcrumb">
          <a href="/shop" style={{ color: colors.primary, fontWeight: 600 }}>Home</a> &gt; <a href="/shop/categories" style={{ color: colors.primary, fontWeight: 600 }}>Fresh Vegetables</a> &gt; <span aria-current="page">Leafy Greens</span>
        </nav>
        <h1 style={{ fontFamily: typography.fontFamilies.display, fontSize: '36px', fontWeight: 600, margin: 0 }}>Leafy Greens</h1>

        <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: '32px', alignItems: 'start', marginTop: '20px' }}>
          {/* Filters Sidebar */}
          <form style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '20px' }} aria-label="Filters">
            <fieldset style={{ border: 0, padding: 0, margin: '0 0 20px' }}>
              <legend style={{ fontFamily: typography.fontFamilies.display, fontWeight: 600, fontSize: '18px', marginBottom: '8px', padding: 0 }}>Categories</legend>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li><a href="/shop/categories?category=fruits" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', minHeight: '36px', padding: '0 8px', textDecoration: 'none', color: colors.ink, fontWeight: 400, borderRadius: '6px' }}>Fresh Fruits <span style={{ fontSize: '13px', color: colors.muted }}>142</span></a></li>
                <li><a href="/shop/categories?category=vegetables" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', minHeight: '36px', padding: '0 8px', textDecoration: 'none', color: colors.primaryDark, fontWeight: 700, borderRadius: '6px', background: colors.status.freshBg }} aria-current="true">Fresh Vegetables <span style={{ fontSize: '13px' }}>132</span></a></li>
              </ul>
            </fieldset>
            <fieldset style={{ border: 0, padding: 0, margin: '0 0 20px' }}>
              <legend style={{ fontFamily: typography.fontFamilies.display, fontWeight: 600, fontSize: '18px', marginBottom: '8px', padding: 0 }}>Filter results</legend>
              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', minHeight: `${accessibility.minTouchTarget}px`, fontSize: '16px' }}>
                <input type="checkbox" checked={isOrganic} onChange={(e) => setIsOrganic(e.target.checked)} style={{ width: '20px', height: '20px', accentColor: colors.primary }} /> Organic only
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', minHeight: `${accessibility.minTouchTarget}px`, fontSize: '16px' }}>
                <input type="checkbox" checked={isFeatured} onChange={(e) => setIsFeatured(e.target.checked)} style={{ width: '20px', height: '20px', accentColor: colors.primary }} /> Featured only
              </label>
            </fieldset>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              <button type="submit" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', minHeight: `${accessibility.minTouchTarget}px`, padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.primary, color: '#fff', fontWeight: 600, fontSize: '15px', cursor: 'pointer' }}>Apply filters</button>
              <a href="/shop/categories" style={{ display: 'inline-flex', alignItems: 'center', minHeight: `${accessibility.minTouchTarget}px`, padding: '0 12px', borderRadius: '6px', border: 'none', background: 'transparent', color: colors.primary, fontWeight: 600, fontSize: '15px', textDecoration: 'none' }}>Clear filters</a>
            </div>
          </form>

          {/* Results */}
          <section aria-labelledby="res-title">
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '16px' }}>
              <div>
                <h2 id="res-title" style={{ fontSize: '22px', fontFamily: typography.fontFamilies.display, fontWeight: 600, margin: 0 }}>Results</h2>
                <p style={{ color: colors.muted, fontSize: '14px', margin: 0 }} role="status" aria-live="polite">Showing 1 to 24 of 132 products</p>
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
                {searchQuery && <FreshnessChip type="fresh" text={`Search: ${searchQuery}`} />}
                {isOrganic && <FreshnessChip type="fresh" text="Organic only" />}
                <label htmlFor="sort" style={{ fontSize: '14px', fontWeight: 600 }}>Sort by</label>
                <select id="sort" style={{ height: `${accessibility.minTouchTarget}px`, border: '1px solid #8A8570', borderRadius: '6px', padding: '0 12px', fontSize: '16px', background: '#fff' }}>
                  <option>Relevance</option>
                  <option>Price: low to high</option>
                  <option>Freshest first</option>
                </select>
              </div>
            </div>

            {/* AI Picks Row */}
            <div style={{ background: colors.status.warningBg, border: `1px solid ${colors.status.warningBorder}`, borderRadius: '8px', padding: '20px', marginBottom: '24px' }} aria-labelledby="pick-title">
              <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', marginBottom: '12px' }}>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
                  <h3 id="pick-title" style={{ fontSize: '20px', fontFamily: typography.fontFamilies.display, fontWeight: 600, margin: 0 }}>Picked for your diet</h3>
                  <FreshnessChip type="warning" text="AI suggested" />
                </div>
                <span style={{ fontSize: '14px', color: colors.muted }}>Separate from the search results below</span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
                {sampleProducts.slice(0, 3).map((p, i) => (
                  <article key={p.id} style={{ background: colors.surface, border: `1px solid ${colors.status.warningBorder}`, borderRadius: '8px', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                    <div style={{ height: '80px', display: 'flex', alignItems: 'flex-end', padding: '12px', fontFamily: typography.fontFamilies.display, fontWeight: 600, fontSize: '16px', color: colors.primaryDark, background: tileColors[i] }} aria-hidden="true">{p.name}</div>
                    <div style={{ padding: '14px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      <h4 style={{ fontSize: '18px', fontFamily: typography.fontFamilies.display, fontWeight: 600, margin: 0 }}>{p.name}</h4>
                      <span style={{ display: 'inline-flex', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, background: colors.surface, color: colors.primaryDark, border: `1px solid ${colors.primary}`, alignSelf: 'flex-start' }}>Based on your diet</span>
                      <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>Fits your vegetarian preference.</p>
                      <p style={{ fontFamily: typography.fontFamilies.display, fontSize: '20px', fontWeight: 700, margin: 0 }}>₹{p.price} <small style={{ fontSize: '14px', fontWeight: 400, color: colors.muted }}>/ {p.unit}</small></p>
                    </div>
                  </article>
                ))}
              </div>
            </div>

            {/* Product Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }} aria-label="Product results">
              {sampleProducts.map((product, idx) => (
                <ProductCard
                  key={product.id}
                  productId={product.id}
                  name={product.name}
                  priceInr={product.price}
                  unit={product.unit}
                  isOrganic={product.organic}
                  freshness={{
                    expiryDays: product.expiry,
                    harvestDate: product.harvest,
                    stockLevel: product.stock as 'available' | 'low_stock' | 'unavailable',
                  }}
                  reviewSummary={{
                    averageRating: product.rating,
                    reviewCount: product.reviews,
                    sentiment: product.sentiment,
                  }}
                  tileColor={tileColors[idx % tileColors.length]}
                  onAdd={() => console.log('Add')}
                  onView={() => navigate(`/shop/product/${product.id}`)}
                />
              ))}
            </div>

            {/* Pagination */}
            <nav style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', marginTop: '32px' }} aria-label="Pagination">
              <a href="#" style={{ minWidth: `${accessibility.minTouchTarget}px`, minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', border: `1px solid ${colors.border}`, borderRadius: '6px', background: '#fff', textDecoration: 'none', fontWeight: 600 }} aria-label="Previous page">Prev</a>
              <span style={{ minWidth: `${accessibility.minTouchTarget}px`, minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', background: colors.primary, color: '#fff', borderRadius: '6px', fontWeight: 600 }} aria-current="page">1</span>
              {[2, 3, 4, 5, 6].map(n => <a key={n} href="#" style={{ minWidth: `${accessibility.minTouchTarget}px`, minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', border: `1px solid ${colors.border}`, borderRadius: '6px', background: '#fff', textDecoration: 'none', fontWeight: 600 }}>{n}</a>)}
              <a href="#" style={{ minWidth: `${accessibility.minTouchTarget}px`, minHeight: `${accessibility.minTouchTarget}px`, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', border: `1px solid ${colors.border}`, borderRadius: '6px', background: '#fff', textDecoration: 'none', fontWeight: 600 }} aria-label="Next page">Next</a>
            </nav>
            <p style={{ color: colors.muted, fontSize: '14px', textAlign: 'center', marginTop: '8px' }}>Page 1 of 6 | 24 products per page</p>
          </section>
        </div>
      </main>

      <footer style={{ background: colors.surfaceAlt, borderTop: `1px solid ${colors.border}`, padding: '24px 64px', color: colors.muted, fontSize: '14px' }}>
        <p style={{ margin: 0 }}>Delivering in Mumbai and Bengaluru only.</p>
        <p style={{ marginTop: '4px' }}>Prices in INR. Freshness information is indicative and based on harvest and expiry data.</p>
      </footer>
    </div>
  );
};
