import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';
import { CheckoutRequest, CheckoutResponse } from '../api/types';
import { colors } from '../styles/colors';
import { WarningBanner } from '../components/WarningBanner';

export const Checkout: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedAddress, setSelectedAddress] = useState('addr-001');
  const [selectedSlot, setSelectedSlot] = useState('slt-20261016-0900');
  const [selectedPayment, setSelectedPayment] = useState('upi');
  const [checkoutStep, setCheckoutStep] = useState(2); // 1=cart, 2=address, 3=slot, 4=payment

  const addresses = [
    { id: 'addr-001', label: 'Home', address: 'Flat 12, Marine Drive, Mumbai 400001', isDefault: true, serviceable: true, zone: 'Mumbai-South 400001' },
    { id: 'addr-002', label: 'Work', address: '4th Floor, Nariman Point, Mumbai 400021', isDefault: false, serviceable: true, zone: 'Mumbai-South 400021' },
    { id: 'addr-003', label: "Parents' home", address: 'B-22, Vasant Vihar, Delhi 110057', isDefault: false, serviceable: false, zone: '' },
  ];

  const slots = [
    { id: 'slt-20261016-0700', label: '7:00 AM to 9:00 AM', booked: 38, capacity: 50, available: true },
    { id: 'slt-20261016-0900', label: '9:00 AM to 11:00 AM', booked: 46, capacity: 50, available: true, express: true },
    { id: 'slt-20261016-1200', label: '12:00 PM to 2:00 PM', booked: 50, capacity: 50, available: false },
    { id: 'slt-20261016-1800', label: '6:00 PM to 8:00 PM', booked: 28, capacity: 50, available: true },
  ];

  const payments = [
    { id: 'upi', label: 'UPI', description: 'Approve the payment in your UPI app.' },
    { id: 'card', label: 'Card', description: "You will finish this on the payment provider's secure page." },
    { id: 'netbanking', label: 'Netbanking', description: "You will choose your bank on the payment provider's page." },
  ];

  const selectedAddressData = addresses.find(a => a.id === selectedAddress);
  const selectedSlotData = slots.find(s => s.id === selectedSlot);
  const selectedPaymentData = payments.find(p => p.id === selectedPayment);

  const canProceed = selectedAddressData?.serviceable && selectedSlotData?.available;

  const handleSubmitOrder = async () => {
    if (!canProceed) {
      setError('Please select a serviceable address and an available slot.');
      return;
    }

    try {
      setLoading(true);
      const request: CheckoutRequest = {
        cartId: 'cart-001',
        addressId: selectedAddress,
        slotId: selectedSlot,
        paymentMethod: selectedPayment,
        clientAmount: '170.00',
      };
      const response = await apiClient.post<CheckoutResponse>('/checkout/submit', request);
      // Redirect to order tracking page
      navigate(`/shop/orders/${response.data.order.orderId}`);
    } catch (err: any) {
      if (err.code === 'ADDRESS_NOT_SERVICEABLE') {
        setError('We cannot deliver to this address yet. GreenBasket AI delivers in Mumbai and Bengaluru only.');
      } else if (err.code === 'SLOT_CAPACITY_EXCEEDED') {
        setError('This delivery slot is now full. Please choose another slot.');
      } else if (err.code === 'AMOUNT_MISMATCH') {
        setError('Prices changed since you last viewed your cart. Please review the new total.');
      } else if (err.code === 'MISSING_REQUIRED_CHECKOUT_INPUT') {
        setError('Please complete all required fields: address, delivery slot, and payment method.');
      } else {
        setError(err.message || 'Failed to submit order');
      }
    } finally {
      setLoading(false);
    }
  };

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
            <span className="inline-flex items-center gap-1.5 min-h-11 px-3.5 rounded-full border border-white/55 text-white text-sm font-semibold">Cart 3 | ₹185.00</span>
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
        <h1 className="text-4xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif', color: colors.ink }}>Checkout</h1>
        <p className="mt-1.5" style={{ color: colors.muted }}>We check your cart, your address, your delivery slot and your payment in this order. You can place the order only when every step passes.</p>

        {/* Checkout Progress Steps */}
        <ol className="grid grid-cols-4 gap-3 mt-5" aria-label="Checkout progress">
          {[
            { num: 1, title: 'Cart check', status: 'Passed' },
            { num: 2, title: 'Address serviceability', status: 'Passed for Home' },
            { num: 3, title: 'Delivery slot', status: 'Selected: Fri 16 Oct, 9:00 AM' },
            { num: 4, title: 'Payment', status: 'Pending' },
          ].map((step) => (
            <li
              key={step.num}
              className="flex items-center gap-3 px-4 py-3.5 border rounded-lg"
              style={{
                backgroundColor: step.num === checkoutStep ? colors.primaryTint : '#fff',
                borderColor: step.num === checkoutStep ? colors.primary : colors.border,
                borderWidth: step.num === checkoutStep ? '2px' : '1px',
              }}
              aria-current={step.num === checkoutStep ? 'step' : undefined}
            >
              <span
                className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-bold"
                style={{ backgroundColor: step.num <= checkoutStep ? colors.primary : '#8A8570', color: '#fff' }}
              >{step.num}</span>
              <div>
                <strong className="block text-base">{step.title}</strong>
                <span className="text-xs font-semibold" style={{ color: colors.muted }}>{step.status}</span>
              </div>
            </li>
          ))}
        </ol>

        {/* Error Display */}
        {error && (
          <WarningBanner type="error" className="mt-5">
            <strong>Error:</strong> {error}
          </WarningBanner>
        )}

        {/* Layout: Form + Sidebar */}
        <div className="grid grid-cols-[1fr_400px] gap-8 items-start mt-8">
          {/* Form Column */}
          <div className="flex flex-col gap-6">
            {/* Address Selection */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <fieldset className="border-0 m-0 p-0">
                <legend className="text-xl font-semibold pb-3" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Delivery address</legend>
                <div className="flex flex-col gap-0">
                  {addresses.map((addr) => (
                    <div
                      key={addr.id}
                      className="flex gap-3.5 items-start border rounded-lg p-4"
                      style={{
                        backgroundColor: selectedAddress === addr.id ? colors.primaryTint : (addr.serviceable ? '#fff' : '#F3F1EA'),
                        borderColor: selectedAddress === addr.id ? colors.primary : colors.border,
                        borderWidth: selectedAddress === addr.id ? '2px' : '1px',
                        borderStyle: addr.serviceable ? 'solid' : 'dashed',
                        minHeight: '64px',
                        marginBottom: '12px',
                      }}
                    >
                      <input
                        type="radio"
                        name="addressId"
                        id={addr.id}
                        value={addr.id}
                        checked={selectedAddress === addr.id}
                        onChange={(e) => setSelectedAddress(e.target.value)}
                        className="w-5.5 h-5.5 mt-0.5"
                        style={{ accentColor: colors.primary }}
                      />
                      <div>
                        <label htmlFor={addr.id} className="font-bold text-lg block">
                          {addr.label} {addr.isDefault && <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border ml-1.5" style={{ backgroundColor: colors.status.infoBg, color: colors.status.infoText, borderColor: colors.status.infoBorder, lineHeight: '20px' }}>Default</span>}
                        </label>
                        <p className="text-sm">{addr.address} | {addr.id}</p>
                        {addr.serviceable ? (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border" style={{ backgroundColor: colors.status.freshBg, color: colors.status.freshText, borderColor: colors.status.freshBorder, lineHeight: '20px' }}>Serviceable: {addr.zone}</span>
                        ) : (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border" style={{ backgroundColor: colors.status.errorBg, color: colors.status.errorText, borderColor: colors.status.errorBorder, lineHeight: '20px' }}>Saved, not serviceable</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
                {selectedAddressData && !selectedAddressData.serviceable && (
                  <WarningBanner type="error" className="mt-4">
                    <strong>We cannot deliver to this address yet.</strong> GreenBasket AI delivers in Mumbai and Bengaluru only. Your address stays saved.
                  </WarningBanner>
                )}
              </fieldset>
            </section>

            {/* Slot Selection */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <fieldset className="border-0 m-0 p-0">
                <legend className="text-xl font-semibold pb-3" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Delivery slot for Friday 16 Oct</legend>
                <WarningBanner type="info" className="mb-3">
                  <strong>Your usual Friday morning slot is selected.</strong> <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border ml-1.5" style={{ backgroundColor: '#fff', color: colors.primaryDark, borderColor: colors.primary, lineHeight: '20px' }}>Reorder reminder</span> You chose 9:00 AM to 11:00 AM on your last 4 orders.
                </WarningBanner>
                <div className="grid grid-cols-2 gap-4">
                  {slots.map((slot) => (
                    <div
                      key={slot.id}
                      className="flex gap-3.5 items-start border rounded-lg p-4"
                      style={{
                        backgroundColor: selectedSlot === slot.id ? colors.primaryTint : (slot.available ? '#fff' : '#F3F1EA'),
                        borderColor: selectedSlot === slot.id ? colors.primary : colors.border,
                        borderWidth: selectedSlot === slot.id ? '2px' : '1px',
                        borderStyle: slot.available ? 'solid' : 'dashed',
                      }}
                    >
                      <input
                        type="radio"
                        name="slotId"
                        id={slot.id}
                        value={slot.id}
                        checked={selectedSlot === slot.id}
                        onChange={(e) => setSelectedSlot(e.target.value)}
                        disabled={!slot.available}
                        className="w-5.5 h-5.5 mt-0.5"
                        style={{ accentColor: colors.primary }}
                      />
                      <div>
                        <label htmlFor={slot.id} className="font-bold text-lg block">
                          {slot.label} {slot.express && <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border ml-1.5" style={{ backgroundColor: colors.accentTint, color: colors.accentInk, borderColor: '#EBCB7A', lineHeight: '20px' }}>Express</span>}
                          {!slot.available && <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border ml-1.5" style={{ backgroundColor: colors.status.greyBg, color: colors.status.greyText, borderColor: colors.status.greyBorder, lineHeight: '20px' }}>Full</span>}
                        </label>
                        <p className="text-sm">{slot.booked} of {slot.capacity} booked | {slot.capacity - slot.booked} left{slot.available ? '' : '. This window cannot take more orders.'} {!slot.available && <strong>SLOT_CAPACITY_EXCEEDED</strong>}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <p className="text-sm mt-3" style={{ color: colors.muted }}>Produce is packed on the morning of delivery.</p>
              </fieldset>
            </section>

            {/* Payment Method */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <fieldset className="border-0 m-0 p-0">
                <legend className="text-xl font-semibold pb-3" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Payment method</legend>
                <div className="flex flex-col gap-0">
                  {payments.map((payment) => (
                    <div
                      key={payment.id}
                      className="flex gap-3.5 items-start border rounded-lg p-4"
                      style={{
                        backgroundColor: selectedPayment === payment.id ? colors.primaryTint : '#fff',
                        borderColor: selectedPayment === payment.id ? colors.primary : colors.border,
                        borderWidth: selectedPayment === payment.id ? '2px' : '1px',
                        minHeight: '64px',
                        marginBottom: '12px',
                      }}
                    >
                      <input
                        type="radio"
                        name="paymentMethod"
                        id={payment.id}
                        value={payment.id}
                        checked={selectedPayment === payment.id}
                        onChange={(e) => setSelectedPayment(e.target.value)}
                        className="w-5.5 h-5.5 mt-0.5"
                        style={{ accentColor: colors.primary }}
                      />
                      <div>
                        <label htmlFor={payment.id} className="font-bold text-lg block">{payment.label}</label>
                        <p className="text-sm">{payment.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <p className="text-sm mt-3" style={{ color: colors.muted }}>GreenBasket AI never asks for or stores card numbers. Payment is completed with our payment provider.</p>
              </fieldset>
            </section>

            {/* Validation Status */}
            <section className="rounded-lg border p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <h2 className="text-xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Before you can place the order</h2>
              <ul className="flex flex-col gap-0 mt-3" role="alert">
                <WarningBanner type="success" className="mb-3"><strong>Passed.</strong> Cart prices are current.</WarningBanner>
                <WarningBanner type={selectedAddressData?.serviceable ? 'success' : 'error'} className="mb-3">
                  <strong>{selectedAddressData?.serviceable ? 'Passed' : 'Failed'}.</strong> {selectedAddressData?.label}, {selectedAddressData?.serviceable ? `${selectedAddressData.zone} is serviceable` : 'not serviceable'}.
                </WarningBanner>
                <WarningBanner type={selectedSlotData?.available ? 'success' : 'error'} className="mb-3">
                  <strong>{selectedSlotData?.available ? 'Passed' : 'Failed'}.</strong> Slot {selectedSlotData?.label} {selectedSlotData?.available ? `has ${selectedSlotData.capacity - selectedSlotData.booked} places left` : 'is full'}.
                </WarningBanner>
                <WarningBanner type="info"><strong>Pending.</strong> Payment will be requested when you press Pay.</WarningBanner>
              </ul>
            </section>
          </div>

          {/* Sidebar */}
          <aside className="flex flex-col gap-0" aria-label="Order summary and action">
            <section className="border rounded-lg p-6 shadow-sm" style={{ backgroundColor: colors.surface, borderColor: colors.border }}>
              <h2 className="text-2xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>Order summary</h2>
              <p className="text-sm mt-1.5" style={{ color: colors.muted }}>3 products, 4 units | Cart cart-001</p>
              <div role="status" aria-live="polite">
                <dl className="mt-3">
                  <div className="flex justify-between py-2.5 border-b" style={{ borderColor: colors.border }}>
                    <dt style={{ color: colors.muted }}>Subtotal</dt>
                    <dd className="m-0 font-semibold">₹185.00</dd>
                  </div>
                  <div className="flex justify-between py-2.5 border-b" style={{ borderColor: colors.border }}>
                    <dt style={{ color: colors.muted }}>Discount (FRESH10)</dt>
                    <dd className="m-0 font-semibold" style={{ color: '#14472B' }}>-₹10.00</dd>
                  </div>
                  <div className="flex justify-between py-2.5 border-b" style={{ borderColor: colors.border }}>
                    <dt style={{ color: colors.muted }}>Loyalty redemption (100 pts)</dt>
                    <dd className="m-0 font-semibold" style={{ color: '#14472B' }}>-₹5.00</dd>
                  </div>
                  <div className="flex justify-between pt-4">
                    <dt className="text-xl font-semibold" style={{ fontFamily: 'Fraunces, Georgia, serif', color: colors.ink }}>Final amount</dt>
                    <dd className="m-0 text-3xl font-bold" style={{ fontFamily: 'Fraunces, Georgia, serif' }}>₹170.00</dd>
                  </div>
                </dl>
              </div>
              <p className="text-sm mt-2">
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold" style={{ backgroundColor: colors.accent, color: colors.accentInk, lineHeight: '20px' }}>17 points</span> will be added after delivery.
              </p>
              <button
                className="w-full text-lg font-semibold rounded-md border mt-5"
                style={{
                  backgroundColor: canProceed ? colors.accent : colors.status.greyBg,
                  color: canProceed ? colors.accentInk : colors.status.greyText,
                  borderColor: canProceed ? colors.accent : colors.status.greyBorder,
                  minHeight: '52px',
                  cursor: canProceed ? 'pointer' : 'not-allowed',
                }}
                onClick={handleSubmitOrder}
                disabled={!canProceed || loading}
                aria-disabled={!canProceed}
              >
                {loading ? 'Processing...' : `Pay ₹170.00 with ${selectedPaymentData?.label || 'UPI'}`}
              </button>
              <p className="text-sm mt-2" style={{ color: canProceed ? colors.muted : '#7A1710', fontWeight: canProceed ? 'normal' : '600' }}>
                {canProceed ? 'Enabled because the address, slot and payment method are all valid.' : 'Choose a serviceable address and an open slot to continue.'}
              </p>
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
