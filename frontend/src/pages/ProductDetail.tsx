import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { colors } from '../styles/colors';
import { typography } from '../styles/typography';
import { accessibility } from '../styles/accessibility';
import { FreshnessChip } from '../components/FreshnessChip';
import { ReasonChip } from '../components/ReasonChip';

export const ProductDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [quantity, setQuantity] = useState(1);
  const [selectedList, setSelectedList] = useState('lst-001');

  return (
    <div style={{ width: '100%', minWidth: '1440px', background: colors.background }}>
      <a href="#main" style={{ display: 'block', padding: '8px 64px', background: colors.primaryDark, color: '#fff', fontSize: '14px', textDecoration: 'none' }}>Skip to main content</a>

      <header style={{ background: colors.primaryDark, color: '#fff' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '20px', padding: '14px 64px' }}>
          <a href="/shop" style={{ display: 'flex', alignItems: 'center', gap: '10px', fontFamily: typography.fontFamilies.display, fontWeight: 700, fontSize: '22px', color: '#fff', textDecoration: 'none' }}>
            <span style={{ width: '36px', height: '36px', borderRadius: '10px', background: colors.accent, color: colors.accentInk, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px' }}>G</span>
            GreenBasket AI
          </a>
          <form style={{ flex: 1, maxWidth: '460px', display: 'flex' }} role="search">
            <input id="q" type="search" style={{ flex: 1, height: `${accessibility.minTouchTarget}px`, border: 0, borderRadius: '6px 0 0 6px', padding: '0 14px', fontSize: '16px' }} />
            <button type="submit" style={{ height: `${accessibility.minTouchTarget}px`, border: 0, borderRadius: '0 6px 6px 0', background: colors.accent, color: colors.accentInk, fontWeight: 700, fontSize: '15px', padding: '0 18px', cursor: 'pointer' }}>Search</button>
          </form>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <a href="/account" style={{ display: 'inline-flex', minHeight: `${accessibility.minTouchTarget}px`, padding: '0 14px', borderRadius: '999px', border: '1px solid rgba(255,255,255,0.55)', color: '#fff', fontSize: '14px', fontWeight: 600, textDecoration: 'none' }}>Home, 400001 | Serviceable</a>
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
          <a href="/shop" style={{ color: colors.primary, fontWeight: 600 }}>Home</a> &gt; <a href="/shop/categories" style={{ color: colors.primary, fontWeight: 600 }}>Fresh Fruits</a> &gt; <a href="/shop/categories" style={{ color: colors.primary, fontWeight: 600 }}>Tropical Fruits</a> &gt; <span aria-current="page">Organic Bananas</span>
        </nav>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px', alignItems: 'start' }}>
          {/* Product Images */}
          <section aria-label="Product images">
            <div style={{ height: '360px', borderRadius: '8px', background: 'linear-gradient(135deg, #F7E7A8 0%, #EFD36B 100%)', border: '1px solid #E3C26B', display: 'flex', alignItems: 'flex-end', padding: '24px', fontFamily: typography.fontFamilies.display, fontWeight: 600, fontSize: '32px', color: colors.primaryDark }} role="img" aria-label="Product image tile: Organic Bananas">
              Organic Bananas
            </div>
            <div style={{ display: 'flex', gap: '12px', marginTop: '12px' }} aria-hidden="true">
              {['Bunch', 'Ripeness', 'Pack', 'Farm'].map(label => (
                <div key={label} style={{ flex: 1, height: '72px', borderRadius: '6px', border: `1px solid ${colors.border}`, background: colors.surfaceAlt, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '13px', fontWeight: 600, color: colors.muted }}>{label}</div>
              ))}
            </div>
          </section>

          {/* Product Details */}
          <section style={{ display: 'flex', flexDirection: 'column', gap: '16px' }} aria-labelledby="pname">
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              <FreshnessChip type="fresh" text="Organic" />
              <FreshnessChip type="fresh" text="Available" />
              <span style={{ fontSize: '14px', color: colors.muted }}>Product prod-001</span>
            </div>

            <h1 id="pname" style={{ fontFamily: typography.fontFamilies.display, fontSize: '36px', fontWeight: 600, margin: 0 }}>Organic Bananas</h1>

            <p style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', fontSize: '14px', margin: 0 }}>
              <strong>4.5 out of 5</strong>
              <span style={{ color: colors.muted }}>from 126 reviews</span>
              <FreshnessChip type="fresh" text="positive" />
            </p>

            <p style={{ fontFamily: typography.fontFamilies.display, fontSize: '40px', fontWeight: 700, margin: 0, fontVariantNumeric: 'tabular-nums' }}>
              ₹65.00 <small style={{ fontSize: '18px', fontWeight: 400, color: colors.muted, fontFamily: typography.fontFamilies.body }}>/ 1 dozen</small>
            </p>

            {/* Freshness Panel */}
            <div style={{ border: `1px solid ${colors.status.freshBorder}`, borderRadius: '8px', padding: '20px', background: colors.status.freshBg }} aria-labelledby="fresh-title">
              <h2 id="fresh-title" style={{ fontSize: '20px', fontFamily: typography.fontFamilies.display, fontWeight: 600, margin: 0 }}>Freshness</h2>
              <ul style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '8px', padding: 0, listStyle: 'none' }}>
                <li><strong>Harvested 13 Oct 2026</strong></li>
                <li>Best within 4 days</li>
                <li>Stock state: Available</li>
              </ul>
              <p style={{ fontSize: '14px', color: colors.muted, marginTop: '8px' }}>Freshness information is indicative and based on harvest and expiry data.</p>
            </div>

            {/* Purchase Options */}
            <form style={{ border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '20px', background: colors.surface, display: 'flex', flexDirection: 'column', gap: '12px' }} aria-label="Purchase options">
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', alignItems: 'flex-end' }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  <span id="qty-l" style={{ fontSize: '14px', fontWeight: 600 }}>Quantity</span>
                  <div style={{ display: 'inline-flex', alignItems: 'center', border: '1px solid #8A8570', borderRadius: '6px', background: '#fff' }} role="group" aria-labelledby="qty-l">
                    <button type="button" onClick={() => setQuantity(Math.max(1, quantity - 1))} aria-label="Decrease quantity of Organic Bananas" style={{ width: `${accessibility.minTouchTarget}px`, height: `${accessibility.minTouchTarget}px`, border: 0, background: 'transparent', fontFamily: typography.fontFamilies.body, fontWeight: 700, fontSize: '20px', color: colors.primary, cursor: 'pointer' }}>-</button>
                    <output style={{ minWidth: '48px', textAlign: 'center', fontWeight: 700, fontSize: '18px' }} aria-live="polite">{quantity}</output>
                    <button type="button" onClick={() => setQuantity(quantity + 1)} aria-label="Increase quantity of Organic Bananas" style={{ width: `${accessibility.minTouchTarget}px`, height: `${accessibility.minTouchTarget}px`, border: 0, background: 'transparent', fontFamily: typography.fontFamilies.body, fontWeight: 700, fontSize: '20px', color: colors.primary, cursor: 'pointer' }}>+</button>
                  </div>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  <label htmlFor="listsel">Add to list</label>
                  <select id="listsel" value={selectedList} onChange={(e) => setSelectedList(e.target.value)} style={{ height: `${accessibility.minTouchTarget}px`, border: '1px solid #8A8570', borderRadius: '6px', padding: '0 12px', fontSize: '16px', fontFamily: typography.fontFamilies.body, background: '#fff' }}>
                    <option value="lst-001">Weekly Staples (lst-001)</option>
                    <option value="lst-094">Suggested Sunday Basket (lst-094)</option>
                  </select>
                </div>
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                <button type="submit" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', minHeight: '48px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.primary, color: '#fff', fontFamily: typography.fontFamilies.body, fontWeight: 600, fontSize: '17px', cursor: 'pointer', flex: 1 }}>Add to cart</button>
                <a href="/planner/lists" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', minHeight: '48px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.surface, color: colors.primary, fontFamily: typography.fontFamilies.body, fontWeight: 600, fontSize: '17px', textDecoration: 'none' }}>Add to list</a>
              </div>
              <p style={{ borderLeft: `4px solid ${colors.primary}`, background: colors.surface, padding: '10px 16px', borderRadius: '0 6px 6px 0', fontWeight: 600, fontSize: '15px', margin: 0 }} role="status" aria-live="polite">
                Organic Bananas added to cart, 1 item, ₹65.00
              </p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                <FreshnessChip type="fresh" text="Serviceable: Mumbai-South 400001" />
                <FreshnessChip type="fresh" text="Next slot: Fri 16 Oct, 9:00 AM to 11:00 AM" />
              </div>
            </form>

            {/* AI Reason Panel */}
            <div style={{ border: `1px solid ${colors.status.warningBorder}`, borderRadius: '8px', padding: '20px', background: colors.status.warningBg }} aria-labelledby="ai-title">
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', alignItems: 'center' }}>
                <h2 id="ai-title" style={{ fontSize: '20px', fontFamily: typography.fontFamilies.display, fontWeight: 600, margin: 0 }}>Why this is shown</h2>
                <FreshnessChip type="warning" text="AI suggested" />
                <ReasonChip text="Reorder reminder" />
              </div>
              <p style={{ marginTop: '6px' }}>You buy these every Sunday.</p>
            </div>
          </section>
        </div>

        {/* Nutrition and Farmer Info */}
        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '24px', marginTop: '40px' }}>
          <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <caption style={{ textAlign: 'left', fontFamily: typography.fontFamilies.display, fontWeight: 600, fontSize: '18px', paddingBottom: '8px' }}>Nutrition per 100 g serving</caption>
              <thead>
                <tr>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', background: colors.surfaceAlt }}>Nutrient</th>
                  <th scope="col" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '15px', background: colors.surfaceAlt }}>Amount</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { nutrient: 'Calories', amount: '89 kcal' },
                  { nutrient: 'Potassium', amount: '358 mg' },
                  { nutrient: 'Carbohydrates', amount: '22.8 g' },
                  { nutrient: 'Dietary fibre', amount: '2.6 g' },
                  { nutrient: 'Sugars', amount: '12.2 g' },
                  { nutrient: 'Protein', amount: '1.1 g' },
                  { nutrient: 'Vitamin C', amount: '8.7 mg' },
                ].map(row => (
                  <tr key={row.nutrient}>
                    <th scope="row" style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', fontWeight: 400 }}>{row.nutrient}</th>
                    <td style={{ padding: '10px 12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '15px', fontVariantNumeric: 'tabular-nums' }}>{row.amount}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p style={{ fontSize: '14px', color: colors.muted, marginTop: '8px' }}>Values come from the product's structured nutrition data.</p>
          </section>

          <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px' }} aria-labelledby="src-title">
            <h2 id="src-title" style={{ fontSize: '22px', fontFamily: typography.fontFamilies.display, fontWeight: 600, margin: 0 }}>Where it comes from</h2>
            <h3 style={{ fontSize: '20px', fontFamily: typography.fontFamilies.display, fontWeight: 600, marginTop: '12px', marginBottom: 0 }}>Sahyadri Farms</h3>
            <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>Farm frm-011 | Maharashtra</p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px' }}>
              <FreshnessChip type="fresh" text="Verified" />
              <FreshnessChip type="fresh" text="Organic certified" />
            </div>
            <p style={{ fontSize: '14px', marginTop: '12px', marginBottom: 0 }}><strong>Farmer rating: 4.7 out of 5</strong></p>
            <p style={{ fontSize: '14px', color: colors.muted, marginTop: '6px' }}>Delivered within 24 hours of packing. Harvest date is shown on every pack.</p>
          </section>
        </div>

        {/* Reviews */}
        <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', marginTop: '40px' }} aria-labelledby="rev-title">
          <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
            <h2 id="rev-title" style={{ fontSize: '24px', fontFamily: typography.fontFamilies.display, fontWeight: 600, margin: 0 }}>Reviews</h2>
            <span style={{ fontSize: '14px', color: colors.muted }}>Average 4.5 out of 5 from 126 reviews</span>
          </div>
          <div style={{ marginTop: '12px' }} role="group" aria-label="Sentiment distribution">
            {[
              { label: 'positive', width: 78, count: 98, color: colors.primary },
              { label: 'neutral', width: 16, count: 20, color: '#8C8F7A' },
              { label: 'negative', width: 6, count: 8, color: colors.status.errorText },
            ].map(bar => (
              <div key={bar.label} style={{ display: 'flex', alignItems: 'center', gap: '12px', margin: '6px 0' }}>
                <span style={{ width: '84px', fontSize: '14px', fontWeight: 600 }}>{bar.label}</span>
                <span style={{ flex: 1, height: '12px', borderRadius: '6px', background: '#E6E0CC' }}>
                  <span style={{ display: 'block', width: `${bar.width}%`, height: '12px', borderRadius: '6px', background: bar.color }} />
                </span>
                <span style={{ width: '40px', textAlign: 'right', fontSize: '14px' }}>{bar.count}</span>
              </div>
            ))}
          </div>
          {[
            { rating: 5, sentiment: 'positive', name: 'Priya, Mumbai', date: '11 Oct 2026', text: 'Sweet and just ripe enough. Stayed fresh through the weekend.' },
            { rating: 4, sentiment: 'positive', name: 'Rahul, Bengaluru', date: '9 Oct 2026', text: 'Good size and flavour. A couple were slightly green on arrival.' },
            { rating: 3, sentiment: 'neutral', name: 'Meera, Mumbai', date: '5 Oct 2026', text: 'Taste is good but the dozen was a little small this time.' },
          ].map((review, i) => (
            <div key={i} style={{ padding: '14px 0', borderTop: `1px solid ${colors.border}` }}>
              <p style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', fontSize: '14px', marginBottom: '4px' }}>
                <strong>{review.rating} out of 5</strong>
                <FreshnessChip type={review.sentiment === 'positive' ? 'fresh' : 'unavailable'} text={review.sentiment} />
                <span style={{ color: colors.muted }}>{review.name} | {review.date}</span>
              </p>
              <p style={{ margin: 0 }}>{review.text}</p>
            </div>
          ))}
        </section>

        {/* Frequently Bought With */}
        <section style={{ marginTop: '40px' }} aria-labelledby="rel-title">
          <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h2 id="rel-title" style={{ fontSize: '24px', fontFamily: typography.fontFamilies.display, fontWeight: 600, margin: 0 }}>Frequently bought with Organic Bananas</h2>
            <FreshnessChip type="warning" text="AI suggested" />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
            {[
              { name: 'Spinach', reason: 'Frequently bought', price: '30.00', unit: '250 g', color: '#CFE5C4' },
              { name: 'Alphonso Mangoes', reason: 'Seasonal', price: '540.00', unit: '1 kg', color: '#F2D6B8' },
              { name: 'Rolled Oats', reason: 'Based on your diet', price: '110.00', unit: '500 g', color: '#DCE9D2' },
              { name: 'Strawberries', reason: 'Trending', price: '120.00', unit: '250 g', color: '#F6C9C0' },
            ].map(p => (
              <article key={p.name} style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                <div style={{ height: '80px', display: 'flex', alignItems: 'flex-end', padding: '12px', fontFamily: typography.fontFamilies.display, fontWeight: 600, fontSize: '16px', color: colors.primaryDark, background: p.color }} aria-hidden="true">{p.name}</div>
                <div style={{ padding: '14px', display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
                  <h3 style={{ fontSize: '18px', fontFamily: typography.fontFamilies.display, fontWeight: 600, margin: 0 }}>{p.name}</h3>
                  <ReasonChip text={p.reason} />
                  <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>{p.reason === 'Frequently bought' ? 'Bought together in 4 of your last 6 orders.' : p.reason === 'Seasonal' ? 'In season now.' : p.reason === 'Based on your diet' ? 'A vegetarian breakfast staple. No peanut ingredients.' : 'Popular in Mumbai-South this week.'}</p>
                  <p style={{ fontFamily: typography.fontFamilies.display, fontSize: '20px', fontWeight: 700, margin: 0 }}>₹{p.price} <small style={{ fontSize: '14px', fontWeight: 400, color: colors.muted, fontFamily: typography.fontFamilies.body }}>/ {p.unit}</small></p>
                  <a href="/shop/cart" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', minHeight: `${accessibility.minTouchTarget}px`, padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.surface, color: colors.primary, fontFamily: typography.fontFamilies.body, fontWeight: 600, fontSize: '15px', textDecoration: 'none' }} aria-label={`Add ${p.name} to cart`}>Add</a>
                </div>
              </article>
            ))}
          </div>
        </section>
      </main>

      <footer style={{ background: colors.surfaceAlt, borderTop: `1px solid ${colors.border}`, padding: '24px 64px', color: colors.muted, fontSize: '14px' }}>
        <p style={{ margin: 0 }}>Delivering in Mumbai and Bengaluru only.</p>
        <p style={{ marginTop: '4px' }}>Prices in INR. Freshness information is indicative and based on harvest and expiry data.</p>
      </footer>
    </div>
  );
};
