import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';
import { CartPricingRequest, CartPricingResponse } from '../api/types';
import { colors } from '../styles/colors';
import { WarningBanner } from '../components/WarningBanner';

export const Cart: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cartData, setCartData] = useState<CartPricingResponse | null>(null);
  const [discountCode, setDiscountCode] = useState('');
  const [loyaltyPoints, setLoyaltyPoints] = useState(0);
  const [cartItems, setCartItems] = useState<Array<{ productId: string; quantity: number; name: string; unit: string; unitPrice: string }>>([
    { productId: 'prod-001', quantity: 1, name: 'Organic Bananas', unit: '1 dozen', unitPrice: '65.00' },
    { productId: 'prod-005', quantity: 2, name: 'Spinach', unit: '250 g', unitPrice: '30.00' },
    { productId: 'prod-010', quantity: 1, name: 'Carrots', unit: '500 g', unitPrice: '60.00' },
  ]);

  const fetchCartPricing = useCallback(async () => {
    try {
      setLoading(true);
      // Transform to snake_case for API
      const apiRequest = {
        items: cartItems.map(item => ({ product_id: item.productId, quantity: item.quantity })),
        discount_code: discountCode || undefined,
        loyalty_points_to_redeem: loyaltyPoints > 0 ? loyaltyPoints : undefined,
      };
      const response = await apiClient.post<CartPricingResponse>('/cart/price', apiRequest);
      setCartData(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch cart pricing');
    } finally {
      setLoading(false);
    }
  }, [cartItems, discountCode, loyaltyPoints]);

  useEffect(() => {
    fetchCartPricing();
  }, [fetchCartPricing]);

  const updateQuantity = (productId: string, delta: number) => {
    setCartItems(prev => prev.map(item => 
      item.productId === productId 
        ? { ...item, quantity: Math.max(1, item.quantity + delta) }
        : item
    ));
  };

  const removeItem = (productId: string) => {
    setCartItems(prev => prev.filter(item => item.productId !== productId));
  };

  const handleApplyDiscount = (e: React.FormEvent) => {
    e.preventDefault();
    fetchCartPricing();
  };

  const handleLoyaltyChange = (delta: number) => {
    const newPoints = Math.max(0, loyaltyPoints + delta);
    if (newPoints <= 420) {
      setLoyaltyPoints(newPoints);
    }
  };

  const handleCheckout = () => {
    navigate('/shop/checkout');
  };

  if (loading && !cartData) {
    return <div className="p-8 text-center">Loading cart...</div>;
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: colors.background }}>
      {/* Header */}
      <header style={{ backgroundColor: colors.primaryDark }}>
        <div className="px-16 py-3.5 flex items-center justify-between gap-5">
          <a href="/shop" className="flex items-center gap-2.5 text-white text-xl font-bold no-underline">
            <span className="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-xl" style={{ backgroundColor: colors.accent, color: colors.accentInk }}>G</span>
            GreenBasket AI
          </a>
          <div className="flex items-center gap-2.5">
            <span className="inline-flex items-center gap-1.5 min-h-11 px-3.5 rounded-full border border-white/55 text-white text-sm font-semibold">Home, 400001 | Serviceable</span>
            <span className="inline-flex items-center gap-1.5 min-h-11 px-3.5 rounded-full border border-white/55 text-white text-sm font-semibold">Alerts 2</span>
            <span className="inline-flex items-center gap-1.5 min-h-11 px-3.5 rounded-full text-sm font-semibold" style={{ backgroundColor: colors.accent, color: colors.accentInk }}>420 pts</span>
            <span className="inline-flex items-center gap-1.5 min-h-11 px-3.5 rounded-full border border-white/55 text-white text-sm font-semibold" style={{ borderColor: colors.accent }}>Cart 3 | ₹{cartData?.pricing?.finalAmount || '185.00'}</span>
          </div>
        </div>
        <nav className="flex gap-2 px-16 pb-3">
          <a href="/shop" className="text-white no-underline font-semibold text-base min-h-11 inline-flex items-center px-4 rounded-md">Home</a>
          <a href="/shop/categories" className="text-white no-underline font-semibold text-base min-h-11 inline-flex items-center px-4 rounded-md">Categories</a>
          <a href="/planner/lists" className="text-white no-underline font-semibold text-base min-h-11 inline-flex items-center px-4 rounded-md">Lists</a>
          <a href="/account/orders" className="text-white no-underline font-semibold text-base min-h-11 inline-flex items-center px-4 rounded-md">Orders</a>
          <a href="/account" className="text-white no-underline font-semibold text-base min-h-11 inline-flex items-center px-4 rounded-md">Account</a>
        </nav>
      </header>

      {/* Main Content */}
      <main className="px-16 py-8">
        <div className="flex items-center justify-between gap-3 flex-wrap">
          <h1 className="text-4xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif', color: colors.ink }}>Your cart</h1>
          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border" style={{ backgroundColor: colors.status.freshBg, color: colors.status.freshText, borderColor: colors.status.freshBorder, lineHeight: '20px' }}>Serviceable: Mumbai-South 400001</span>
        </div>
        <p className="mt-1.5" style={{ color: colors.muted }}>3 products, 4 units. Prices are re-checked every time you change the cart.</p>

        {/* Warnings */}
        {cartData?.warnings && cartData.warnings.length > 0 && (
          <div className="mt-5 space-y-3">
            {cartData.warnings.map((warning, idx) => (
              <WarningBanner key={idx} type="warning">
                <strong>Limited stock.</strong> {warning}
              </WarningBanner>
            ))}
          </div>
        )}

        <WarningBanner type="info" className="mt-3">
          <strong>Prices refreshed.</strong> Prices were checked a moment ago. If anything changes before you pay, you will see the new total first.
        </WarningBanner>

        {/* Layout: Main + Sidebar */}
        <div className="grid grid-cols-[1fr_400px] gap-8 items-start mt-6">
          {/* Main Column */}
          <div className="flex flex-col gap-6">
            {/* Cart Items Table */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <table className="w-full border-collapse">
                <caption className="text-left text-xl font-semibold pb-3" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Items in your cart</caption>
                <thead>
                  <tr>
                    <th className="p-3 border-b text-left text-sm" style={{ backgroundColor: colors.surfaceAlt, borderColor: colors.border }}>Product</th>
                    <th className="p-3 border-b text-right text-sm" style={{ backgroundColor: colors.surfaceAlt, borderColor: colors.border }}>Unit price</th>
                    <th className="p-3 border-b text-left text-sm" style={{ backgroundColor: colors.surfaceAlt, borderColor: colors.border }}>Quantity</th>
                    <th className="p-3 border-b text-right text-sm" style={{ backgroundColor: colors.surfaceAlt, borderColor: colors.border }}>Line total</th>
                    <th className="p-3 border-b text-sm" style={{ backgroundColor: colors.surfaceAlt, borderColor: colors.border }}><span className="sr-only">Remove</span></th>
                  </tr>
                </thead>
                <tbody>
                  {cartItems.map((item) => {
                    const lineItem = cartData?.lineItems?.find(li => li.productId === item.productId);
                    return (
                      <tr key={item.productId}>
                        <th scope="row" className="p-3 border-b text-left font-normal" style={{ borderColor: colors.border }}>
                          <span className="font-semibold text-lg" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>{item.name}</span><br />
                          <span className="text-sm" style={{ color: colors.muted }}>{item.productId} | {item.unit}</span><br />
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border" style={{ backgroundColor: colors.status.freshBg, color: colors.status.freshText, borderColor: colors.status.freshBorder, lineHeight: '20px' }}>Harvested 13 Oct, best within 4 days</span>
                        </th>
                        <td className="p-3 border-b text-right" style={{ borderColor: colors.border }}>₹{item.unitPrice}</td>
                        <td className="p-3 border-b" style={{ borderColor: colors.border }}>
                          <div className="inline-flex items-center border rounded-md" style={{ borderColor: '#8A8570', backgroundColor: '#fff' }}>
                            <button
                              type="button"
                              className="w-11 h-11 border-0 bg-transparent font-bold text-xl"
                              style={{ color: colors.primary }}
                              onClick={() => updateQuantity(item.productId, -1)}
                              aria-label={`Decrease quantity of ${item.name}`}
                            >-</button>
                            <output className="min-w-10 text-center font-bold text-lg">{item.quantity}</output>
                            <button
                              type="button"
                              className="w-11 h-11 border-0 bg-transparent font-bold text-xl"
                              style={{ color: colors.primary }}
                              onClick={() => updateQuantity(item.productId, 1)}
                              aria-label={`Increase quantity of ${item.name}`}
                            >+</button>
                          </div>
                        </td>
                        <td className="p-3 border-b text-right" style={{ borderColor: colors.border }}><strong>₹{lineItem?.lineTotal || (parseFloat(item.unitPrice) * item.quantity).toFixed(2)}</strong></td>
                        <td className="p-3 border-b" style={{ borderColor: colors.border }}>
                          <button
                            type="button"
                            className="inline-flex items-center justify-center gap-2 min-h-11 px-3 rounded-md border-0 bg-transparent font-semibold text-sm"
                            style={{ color: '#8A1B14' }}
                            onClick={() => removeItem(item.productId)}
                            aria-label={`Remove ${item.name} from cart`}
                          >Remove</button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </section>

            {/* Discount Code */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <h2 className="text-xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Discount code</h2>
              <form className="flex items-end gap-3 flex-wrap mt-3" onSubmit={handleApplyDiscount}>
                <div className="flex flex-col gap-1.5 flex-1 min-w-60">
                  <label htmlFor="code" className="text-sm font-semibold">Have a code?</label>
                  <input
                    id="code"
                    name="discountCode"
                    className="h-11 border rounded-md px-3.5 text-base"
                    style={{ borderColor: '#8A8570', backgroundColor: '#fff', color: colors.ink }}
                    value={discountCode}
                    onChange={(e) => setDiscountCode(e.target.value)}
                  />
                </div>
                <button className="inline-flex items-center justify-center gap-2 min-h-11 px-5 rounded-md border font-semibold text-sm text-white" style={{ backgroundColor: colors.primary, borderColor: colors.primary }} type="submit">Apply</button>
              </form>
              {cartData?.appliedDiscount && (
                <p className="text-sm mt-2">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border" style={{ backgroundColor: colors.status.freshBg, color: colors.status.freshText, borderColor: colors.status.freshBorder, lineHeight: '20px' }}>Applied</span> {cartData.appliedDiscount.code}: up to {cartData.appliedDiscount.type} off, minimum order ₹{cartData.appliedDiscount.minimumOrderThreshold}. You saved ₹{cartData.pricing.discountAmount}.
                </p>
              )}
            </section>

            {/* Loyalty Points */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <div className="flex items-center justify-between flex-wrap">
                <h2 className="text-xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Loyalty points</h2>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold" style={{ backgroundColor: colors.accent, color: colors.accentInk, lineHeight: '20px' }}>420 points available</span>
              </div>
              <p className="mt-1.5" style={{ color: colors.muted }}>Redeem 100 points for ₹5.00 off. Points are used only when you check out.</p>
              <div className="flex items-center gap-3 flex-wrap mt-3">
                <div className="inline-flex items-center border rounded-md" style={{ borderColor: '#8A8570', backgroundColor: '#fff' }}>
                  <button
                    type="button"
                    className="w-11 h-11 border-0 bg-transparent font-bold text-xl"
                    style={{ color: colors.primary }}
                    onClick={() => handleLoyaltyChange(-100)}
                    aria-label="Redeem 100 fewer points"
                  >-</button>
                  <output className="text-center font-bold text-lg" style={{ minWidth: '96px' }}>{loyaltyPoints} pts</output>
                  <button
                    type="button"
                    className="w-11 h-11 border-0 bg-transparent font-bold text-xl"
                    style={{ color: colors.primary }}
                    onClick={() => handleLoyaltyChange(100)}
                    aria-label="Redeem 100 more points"
                  >+</button>
                </div>
                <span className="text-sm"><strong>Saves ₹{(loyaltyPoints / 100 * 5).toFixed(2)}</strong>, leaving {420 - loyaltyPoints} points.</span>
              </div>
            </section>
          </div>

          {/* Sidebar */}
          <aside className="flex flex-col gap-0" aria-label="Order summary">
            <section className="border rounded-lg p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <h2 className="text-2xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Order summary</h2>
              <div role="status" aria-live="polite">
                <dl className="mt-3">
                  <div className="flex justify-between py-2.5 border-b" style={{ borderColor: colors.border }}>
                    <dt style={{ color: colors.muted }}>Subtotal</dt>
                    <dd className="m-0 font-semibold">₹{cartData?.pricing?.subtotal || '185.00'}</dd>
                  </div>
                  {cartData?.appliedDiscount && (
                    <div className="flex justify-between py-2.5 border-b" style={{ borderColor: colors.border }}>
                      <dt style={{ color: colors.muted }}>Discount ({cartData.appliedDiscount.code})</dt>
                      <dd className="m-0 font-semibold" style={{ color: '#14472B' }}>-₹{cartData.pricing?.discountAmount || '0.00'}</dd>
                    </div>
                  )}
                  {loyaltyPoints > 0 && (
                    <div className="flex justify-between py-2.5 border-b" style={{ borderColor: colors.border }}>
                      <dt style={{ color: colors.muted }}>Loyalty redemption ({loyaltyPoints} pts)</dt>
                      <dd className="m-0 font-semibold" style={{ color: '#14472B' }}>-₹{cartData?.pricing?.loyaltyRedemptionAmount || '0.00'}</dd>
                    </div>
                  )}
                  <div className="flex justify-between pt-4">
                    <dt className="text-xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif', color: colors.ink }}>Final amount</dt>
                    <dd className="m-0 text-3xl font-bold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>₹{cartData?.pricing?.finalAmount || '170.00'}</dd>
                  </div>
                </dl>
              </div>
              <p className="text-sm mt-2" style={{ color: colors.muted }}>You will earn 17 loyalty points on this order.</p>
              <hr className="border-0 my-4" style={{ borderTop: `1px solid ${colors.border}` }} />
              <div className="flex flex-col gap-2">
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border self-start" style={{ backgroundColor: colors.status.freshBg, color: colors.status.freshText, borderColor: colors.status.freshBorder, lineHeight: '20px' }}>Serviceable: Mumbai-South 400001</span>
                <p className="text-sm" style={{ color: colors.muted }}>Choose a delivery slot at checkout. Produce is packed on the morning of delivery.</p>
              </div>
            </section>
            <div className="rounded-lg border p-4 mt-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <p className="text-sm" style={{ color: colors.muted }}>Delivering in Mumbai and Bengaluru only. Your address stays saved even if we cannot deliver to it yet.</p>
            </div>
          </aside>
        </div>

        {/* CTA Bar */}
        <div className="flex items-center justify-between gap-6 rounded-lg px-6 py-5 mt-8" style={{ backgroundColor: colors.primaryDark }} role="region" aria-label="Proceed to checkout">
          <div>
            <p className="text-xl font-semibold text-white" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Final amount ₹{cartData?.pricing?.finalAmount || '170.00'}</p>
            <p className="text-sm" style={{ color: '#E3F0E7' }}>Delivering to Home, Mumbai 400001</p>
          </div>
          <button
            className="inline-flex items-center justify-center gap-2 px-5 rounded-md border font-semibold text-lg"
            style={{ backgroundColor: colors.accent, color: colors.accentInk, borderColor: colors.accent, minHeight: '52px' }}
            onClick={handleCheckout}
          >Proceed to checkout</button>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t px-16 py-6" style={{ backgroundColor: colors.surfaceAlt, borderColor: colors.border, color: colors.muted, fontSize: '14px' }}>
        <p>Delivering in Mumbai and Bengaluru only.</p>
        <p className="mt-1">Prices in INR. Freshness information is indicative and based on harvest and expiry data.</p>
      </footer>
    </div>
  );
};
