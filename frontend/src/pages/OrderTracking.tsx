import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { apiClient } from '../api/client';
import { OrderDetailResponse } from '../api/types';
import { colors } from '../styles/colors';
import { StatusBadge } from '../components/StatusBadge';
import { WarningBanner } from '../components/WarningBanner';

export const OrderTracking: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [orderData, setOrderData] = useState<OrderDetailResponse | null>(null);
  const [selectedProduct, setSelectedProduct] = useState('prod-001');
  const [rating, setRating] = useState(5);
  const [reviewText, setReviewText] = useState('Sweet and just ripe enough. Stayed fresh through the weekend.');
  const [reviewSubmitted, setReviewSubmitted] = useState(false);

  const fetchOrderDetails = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiClient.get<OrderDetailResponse>(`/orders/${id || 'ord-001'}`);
      setOrderData(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch order details');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchOrderDetails();
  }, [fetchOrderDetails]);

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!orderData?.reviewEligibility.canSubmit) {
      setError('Reviews open after delivery. You can review items after the order is delivered.');
      return;
    }

    try {
      await apiClient.post(`/orders/${id}/reviews`, {
        productId: selectedProduct,
        rating,
        reviewText,
      });
      setReviewSubmitted(true);
      setError(null);
    } catch (err: any) {
      if (err.code === 'REVIEW_NOT_ELIGIBLE') {
        setError('Reviews open after delivery. You can review items after the order is delivered.');
      } else {
        setError(err.message || 'Failed to submit review');
      }
    }
  };

  if (loading) {
    return <div className="p-8 text-center">Loading order details...</div>;
  }

  const mockOrder = {
    orderId: 'ord-001',
    orderDate: 'Thu 15 Oct 2026, 8:12 PM',
    status: 'confirmed' as const,
    paymentStatus: 'paid',
    paymentMethod: 'UPI',
    paymentReference: 'txn-upi-8877123',
    subtotal: '185.00',
    discountAmount: '10.00',
    loyaltyRedemption: '5.00',
    finalAmount: '170.00',
    trackingUrl: 'https://track.greenbasketai.com/ord-001',
    slot: { slotId: 'slt-20261016-0900', label: 'Fri 16 Oct, 9:00 AM to 11:00 AM' },
    address: 'Home, Mumbai 400001',
    items: [
      { productId: 'prod-001', name: 'Organic Bananas', unit: '1 dozen', quantity: 1, unitPrice: '65.00', lineTotal: '65.00' },
      { productId: 'prod-005', name: 'Spinach', unit: '250 g', quantity: 2, unitPrice: '30.00', lineTotal: '60.00' },
      { productId: 'prod-010', name: 'Carrots', unit: '500 g', quantity: 1, unitPrice: '60.00', lineTotal: '60.00' },
    ],
    deliveryAgent: { agentId: 'agt-010', name: 'Rajesh', phoneNumber: '+91 98123 41234', vehicle: 'Electric scooter', rating: '4.8' },
    loyaltyPointsEarned: 17,
    loyaltyBalance: 437,
  };

  const order = mockOrder;
  const canReview = (order.status as string) === 'delivered';

  const timelineSteps = [
    { status: 'payment_pending', label: 'payment_pending', time: 'Completed 8:12 PM', done: true },
    { status: 'confirmed', label: 'confirmed', time: 'Current step | 8:13 PM', done: true, current: order.status === 'confirmed' },
    { status: 'packed', label: 'packed', time: 'Fri morning', done: false },
    { status: 'out_for_delivery', label: 'out_for_delivery', time: 'Slot starts 9:00 AM', done: false },
    { status: 'delivered', label: 'delivered', time: 'By 11:00 AM', done: false },
  ];

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
            <span className="inline-flex items-center gap-1.5 min-h-11 px-3.5 rounded-full text-sm font-semibold" style={{ backgroundColor: colors.accent, color: colors.accentInk }}>437 pts</span>
            <span className="inline-flex items-center gap-1.5 min-h-11 px-3.5 rounded-full border border-white/55 text-white text-sm font-semibold">Cart 0 | ₹0.00</span>
          </div>
        </div>
        <nav className="flex gap-2 px-16 pb-3">
          <a href="/shop" className="text-white no-underline font-semibold text-base min-h-11 inline-flex items-center px-4 rounded-md">Home</a>
          <a href="/shop/categories" className="text-white no-underline font-semibold text-base min-h-11 inline-flex items-center px-4 rounded-md">Categories</a>
          <a href="/planner/lists" className="text-white no-underline font-semibold text-base min-h-11 inline-flex items-center px-4 rounded-md">Lists</a>
          <a href="/account/orders" className="text-white no-underline font-semibold text-base min-h-11 inline-flex items-center px-4 rounded-md" style={{ backgroundColor: '#fff', color: colors.primaryDark }} aria-current="page">Orders</a>
          <a href="/account" className="text-white no-underline font-semibold text-base min-h-11 inline-flex items-center px-4 rounded-md">Account</a>
        </nav>
      </header>

      {/* Main Content */}
      <main className="px-16 py-8">
        {/* Order Header */}
        <div className="flex items-start justify-between gap-6 flex-wrap">
          <div>
            <h1 className="text-4xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif', color: colors.ink }}>Order {order.orderId}</h1>
            <p className="mt-1.5" style={{ color: colors.muted }}>Placed {order.orderDate} | 3 products, 4 units | ₹{order.finalAmount}</p>
          </div>
          <div className="flex flex-col gap-2 items-end">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-sm" style={{ color: colors.muted }}>Order status</span>
              <StatusBadge status={order.status} />
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-sm" style={{ color: colors.muted }}>Payment</span>
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border" style={{ backgroundColor: colors.status.freshBg, color: colors.status.freshText, borderColor: colors.status.freshBorder, lineHeight: '20px' }}>paid</span>
              <span className="text-sm" style={{ color: colors.muted }}>Ref {order.paymentReference} | {order.paymentMethod} | ₹{order.finalAmount}</span>
            </div>
          </div>
        </div>

        <WarningBanner type="success" className="mt-5">
          <strong>Payment confirmed.</strong> Your order is confirmed. We will tell you when it is packed and when it leaves for delivery.
        </WarningBanner>

        {/* Layout: Main + Sidebar */}
        <div className="grid grid-cols-[1fr_420px] gap-8 items-start mt-6">
          {/* Main Column */}
          <div className="flex flex-col gap-6">
            {/* Order Progress Timeline */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <h2 className="text-2xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Order progress</h2>
              <ol className="grid grid-cols-5 gap-0 mt-3" aria-label="Order status steps" style={{ counterReset: 't' }}>
                {timelineSteps.map((step, idx) => (
                  <li
                    key={step.status}
                    className="relative pt-11 pb-0 px-2 text-center"
                    aria-current={step.current ? 'step' : undefined}
                    style={{
                      paddingTop: '44px',
                    }}
                  >
                    {/* Line */}
                    <div
                      className="absolute h-1"
                      style={{
                        top: '14px',
                        left: idx === 0 ? '50%' : '0',
                        right: idx === timelineSteps.length - 1 ? '50%' : '0',
                        backgroundColor: step.done ? colors.primary : colors.border,
                      }}
                    />
                    {/* Circle */}
                    <div
                      className="absolute w-6 h-6 rounded-full border-3"
                      style={{
                        top: '4px',
                        left: 'calc(50% - 12px)',
                        backgroundColor: step.current ? colors.accent : (step.done ? colors.primary : '#fff'),
                        borderColor: step.current ? colors.accentInk : (step.done ? colors.primary : '#8A8570'),
                        borderWidth: '3px',
                      }}
                    />
                    <strong className="block text-sm">{step.label}</strong>
                    <span className="text-xs" style={{ color: colors.muted }}>{step.time}</span>
                  </li>
                ))}
              </ol>
              <p className="text-sm mt-4" style={{ color: colors.muted }}>
                <strong>Off-path states:</strong> <StatusBadge status="cancelled" /> <StatusBadge status="payment_failed" /> shown only if the order leaves the normal path. An order is never shown as confirmed while payment is still initiated.
              </p>
            </section>

            {/* Order Items */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <table className="w-full border-collapse">
                <caption className="text-left text-xl font-semibold pb-2" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Items in this order</caption>
                <thead>
                  <tr>
                    <th className="p-3 border-b text-left text-sm" style={{ backgroundColor: colors.surfaceAlt, borderColor: colors.border }}>Product</th>
                    <th className="p-3 border-b text-right text-sm" style={{ backgroundColor: colors.surfaceAlt, borderColor: colors.border }}>Quantity</th>
                    <th className="p-3 border-b text-right text-sm" style={{ backgroundColor: colors.surfaceAlt, borderColor: colors.border }}>Unit price</th>
                    <th className="p-3 border-b text-right text-sm" style={{ backgroundColor: colors.surfaceAlt, borderColor: colors.border }}>Line total</th>
                  </tr>
                </thead>
                <tbody>
                  {order.items.map((item) => (
                    <tr key={item.productId}>
                      <th scope="row" className="p-3 border-b text-left font-semibold" style={{ borderColor: colors.border }}>
                        {item.name} <span className="text-sm font-normal" style={{ color: colors.muted }}>({item.unit})</span>
                      </th>
                      <td className="p-3 border-b text-right" style={{ borderColor: colors.border }}>{item.quantity}</td>
                      <td className="p-3 border-b text-right" style={{ borderColor: colors.border }}>₹{item.unitPrice}</td>
                      <td className="p-3 border-b text-right" style={{ borderColor: colors.border }}>₹{item.lineTotal}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <dl className="mt-4 ml-auto" style={{ maxWidth: '420px' }}>
                <div className="flex justify-between py-2 border-b" style={{ borderColor: colors.border }}>
                  <dt style={{ color: colors.muted }}>Subtotal</dt>
                  <dd className="m-0 font-semibold">₹{order.subtotal}</dd>
                </div>
                <div className="flex justify-between py-2 border-b" style={{ borderColor: colors.border }}>
                  <dt style={{ color: colors.muted }}>Discount (FRESH10)</dt>
                  <dd className="m-0 font-semibold">-₹{order.discountAmount}</dd>
                </div>
                <div className="flex justify-between py-2 border-b" style={{ borderColor: colors.border }}>
                  <dt style={{ color: colors.muted }}>Loyalty redemption</dt>
                  <dd className="m-0 font-semibold">-₹{order.loyaltyRedemption}</dd>
                </div>
                <div className="flex justify-between pt-4">
                  <dt className="text-lg font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif', color: colors.ink }}>Final amount</dt>
                  <dd className="m-0 text-2xl font-bold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>₹{order.finalAmount}</dd>
                </div>
              </dl>
              <p className="text-sm mt-2" style={{ color: colors.muted }}>Packed on the morning of delivery. Freshness information is indicative.</p>
            </section>

            {/* Review Section */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <div className="flex items-center justify-between flex-wrap">
                <h2 className="text-2xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Review your items</h2>
                <span className="text-sm" style={{ color: colors.muted }}>Reviews open after delivery</span>
              </div>
              <div className="grid grid-cols-2 gap-4 mt-4">
                {/* Review Form */}
                <form className="flex flex-col gap-0" onSubmit={handleSubmitReview} aria-label="Review form">
                  <div className="flex flex-col gap-1.5">
                    <label htmlFor="rp" className="text-sm font-semibold">Product</label>
                    <select
                      id="rp"
                      name="productId"
                      className="h-11 border rounded-md px-3 text-base"
                      style={{ borderColor: '#8A8570', backgroundColor: '#fff', color: colors.ink }}
                      value={selectedProduct}
                      onChange={(e) => setSelectedProduct(e.target.value)}
                      disabled={!canReview}
                    >
                      {order.items.map(item => (
                        <option key={item.productId} value={item.productId}>{item.name} ({item.productId})</option>
                      ))}
                    </select>
                  </div>
                  <fieldset className="border rounded-lg p-2.5 mt-3" style={{ borderColor: colors.border }}>
                    <legend className="text-sm font-semibold px-1.5">Rating</legend>
                    <div className="flex gap-2 flex-wrap">
                      {[1, 2, 3, 4, 5].map((val) => (
                        <label key={val} className="inline-flex items-center gap-1.5 min-h-11 px-3 border rounded-md font-semibold" style={{ borderColor: colors.border, backgroundColor: '#fff' }}>
                          <input
                            type="radio"
                            name="rating"
                            value={val}
                            checked={rating === val}
                            onChange={(e) => setRating(parseInt(e.target.value))}
                            disabled={!canReview}
                            className="w-4.5 h-4.5"
                            style={{ accentColor: colors.primary }}
                          /> {val}
                        </label>
                      ))}
                    </div>
                  </fieldset>
                  <div className="flex flex-col gap-1.5 mt-3">
                    <label htmlFor="rt" className="text-sm font-semibold">Your review</label>
                    <textarea
                      id="rt"
                      name="reviewText"
                      className="border rounded-md px-3 py-2.5 text-base"
                      style={{ borderColor: '#8A8570', backgroundColor: '#fff', color: colors.ink, minHeight: '88px' }}
                      value={reviewText}
                      onChange={(e) => setReviewText(e.target.value)}
                      disabled={!canReview}
                    />
                  </div>
                  <button
                    className="inline-flex items-center justify-center gap-2 min-h-11 px-5 rounded-md border font-semibold text-sm text-white mt-3"
                    style={{
                      backgroundColor: canReview ? colors.primary : colors.status.greyBg,
                      borderColor: canReview ? colors.primary : colors.status.greyBorder,
                      color: canReview ? '#fff' : colors.status.greyText,
                      cursor: canReview ? 'pointer' : 'not-allowed',
                    }}
                    type="submit"
                    disabled={!canReview}
                    aria-disabled={!canReview}
                  >Submit review</button>
                </form>

                {/* Review Status */}
                <div className="flex flex-col gap-0">
                  {!canReview && (
                    <WarningBanner type="warning">
                      <strong>Reviews open after delivery.</strong> You can review items after the order is delivered.
                    </WarningBanner>
                  )}
                  {reviewSubmitted && (
                    <div>
                      <WarningBanner type="success">
                        <strong>Thank you. Your review was saved.</strong>
                      </WarningBanner>
                      <p className="flex items-center gap-2 flex-wrap mt-2">
                        <strong>Your rating: {rating} out of 5</strong>
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border" style={{ backgroundColor: colors.status.freshBg, color: colors.status.freshText, borderColor: colors.status.freshBorder, lineHeight: '20px' }}>positive</span>
                      </p>
                      <p className="text-sm mt-2" style={{ color: colors.muted }}>The sentiment label is worked out from your words. It is shown separately from your star rating.</p>
                    </div>
                  )}
                </div>
              </div>
            </section>
          </div>

          {/* Sidebar */}
          <aside className="flex flex-col gap-6" aria-label="Delivery, agent, loyalty">
            {/* Delivery Details */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <h2 className="text-xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Delivery</h2>
              <dl className="mt-2">
                <div className="flex justify-between py-2 border-b" style={{ borderColor: colors.border }}>
                  <dt style={{ color: colors.muted }}>Slot</dt>
                  <dd className="m-0 font-semibold">{order.slot.label}</dd>
                </div>
                <div className="flex justify-between py-2 border-b" style={{ borderColor: colors.border }}>
                  <dt style={{ color: colors.muted }}>Slot id</dt>
                  <dd className="m-0 font-semibold">{order.slot.slotId}</dd>
                </div>
                <div className="flex justify-between py-2">
                  <dt style={{ color: colors.muted }}>Address</dt>
                  <dd className="m-0 font-semibold">{order.address}</dd>
                </div>
              </dl>
              <p className="text-sm font-semibold mt-3">Tracking link</p>
              <span className="block px-3 py-2 rounded-md text-sm break-all" style={{ backgroundColor: colors.surfaceAlt, fontFamily: '"Courier New", monospace' }}>{order.trackingUrl}</span>
              <a
                href={order.trackingUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-2 min-h-11 px-5 rounded-md border font-semibold text-sm text-white mt-3"
                style={{ backgroundColor: colors.primary, borderColor: colors.primary }}
              >Open tracking page</a>
            </section>

            {/* Delivery Agent */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <h2 className="text-xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Delivery agent</h2>
              <div className="flex gap-4 items-center mt-3">
                <span className="w-14 h-14 rounded-full flex items-center justify-center text-white text-2xl font-bold" style={{ backgroundColor: colors.primary, fontFamily: 'Fraunces, Georgia, serif' }}>R</span>
                <div>
                  <strong className="text-lg">{order.deliveryAgent.name}</strong> <span className="text-sm" style={{ color: colors.muted }}>{order.deliveryAgent.agentId}</span>
                  <p className="text-sm">{order.deliveryAgent.phoneNumber} | {order.deliveryAgent.vehicle}</p>
                  <p className="flex items-center gap-2 text-sm flex-wrap">
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border" style={{ backgroundColor: colors.status.infoBg, color: colors.status.infoText, borderColor: colors.status.infoBorder, lineHeight: '20px' }}>assigned</span>
                    <span>Rating {order.deliveryAgent.rating} out of 5</span>
                  </p>
                </div>
              </div>
            </section>

            {/* Loyalty */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.accentTint, borderColor: '#EBCB7A' }}>
              <h2 className="text-xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Loyalty</h2>
              <p className="mt-1.5"><strong>You earned {order.loyaltyPointsEarned} points.</strong> Balance: {order.loyaltyBalance} points.</p>
              <p className="text-sm" style={{ color: colors.muted }}>Points from this order are added after delivery.</p>
            </section>

            {/* Reorder Suggestion */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: '#EBCB7A' }}>
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Reorder this basket</h2>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold" style={{ backgroundColor: colors.accent, color: colors.accentInk, lineHeight: '20px' }}>AI suggested</span>
              </div>
              <p className="flex items-center gap-2 flex-wrap mt-2">
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border" style={{ backgroundColor: '#fff', color: colors.primaryDark, borderColor: colors.primary, lineHeight: '20px' }}>Reorder reminder</span>
              </p>
              <p className="text-sm mt-1.5" style={{ color: colors.muted }}>You buy these every Sunday. Save it as a list to reorder in one tap.</p>
              <a
                href="/planner/lists"
                className="inline-flex items-center justify-center gap-2 min-h-11 px-5 rounded-md border font-semibold text-sm mt-3"
                style={{ backgroundColor: colors.surface, color: colors.primary, borderColor: colors.primary }}
              >Go to Shopping lists</a>
            </section>
          </aside>
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
