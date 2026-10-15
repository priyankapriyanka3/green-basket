import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { colors } from '../styles/colors';
import { FreshnessChip } from '../components/FreshnessChip';
import { ReasonChip } from '../components/ReasonChip';

interface ShoppingListItem {
  product_id: string;
  product_name: string;
  unit: string;
  quantity: number;
  price_inr: number;
  source_reason_tag: string;
  reason_text: string;
  is_organic?: boolean;
  freshness_text?: string;
  freshness_status?: 'fresh' | 'warning' | 'unavailable';
  available: boolean;
}

interface ShoppingList {
  list_id: string;
  name: string;
  is_ai_generated: boolean;
  suggestion_note?: string;
  items: ShoppingListItem[];
  created_at: string;
}

interface GenerateListRequest {
  mode: 'weekly_reorder' | 'diet_boost' | 'seasonal_refresh';
  sourceOrderWindowDays: number;
  targetListName: string;
}

export default function ShoppingLists() {
  const { user } = useAuth();
  const [lists, setLists] = useState<ShoppingList[]>([]);
  const [currentList, setCurrentList] = useState<ShoppingList | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showGenerateDialog, setShowGenerateDialog] = useState(false);
  const [generateMode, setGenerateMode] = useState<'weekly_reorder' | 'diet_boost' | 'seasonal_refresh'>('weekly_reorder');
  const [sourceWindowDays, setSourceWindowDays] = useState(42);
  const [listName, setListName] = useState('Suggested Sunday Basket');
  const [generationSuccess, setGenerationSuccess] = useState(false);

  useEffect(() => {
    loadLists();
  }, []);

  const loadLists = async () => {
    try {
      setLoading(true);
      // Mock data for wireframe fidelity
      const mockLists: ShoppingList[] = [
        {
          list_id: 'lst-001',
          name: 'Weekly Staples',
          is_ai_generated: false,
          items: [],
          created_at: new Date().toISOString(),
        },
        {
          list_id: 'lst-094',
          name: 'Suggested Sunday Basket',
          is_ai_generated: true,
          suggestion_note: 'Based on your last 6 orders and weekly cadence.',
          items: [
            {
              product_id: 'prod-001',
              product_name: 'Organic Bananas',
              unit: '1 kg',
              quantity: 1,
              price_inr: 65.0,
              source_reason_tag: 'reorder_reminder',
              reason_text: 'You buy these every Sunday.',
              is_organic: true,
              freshness_text: 'Harvested 13 Oct, best within 4 days',
              freshness_status: 'fresh',
              available: true,
            },
            {
              product_id: 'prod-005',
              product_name: 'Spinach',
              unit: '500 g',
              quantity: 2,
              price_inr: 30.0,
              source_reason_tag: 'based_on_diet',
              reason_text: 'Fits your vegetarian preference.',
              freshness_text: 'Low stock: 3 left',
              freshness_status: 'warning',
              available: true,
            },
            {
              product_id: 'prod-006',
              product_name: 'Carrots',
              unit: '500 g',
              quantity: 1,
              price_inr: 60.0,
              source_reason_tag: 'reorder_reminder',
              reason_text: 'You buy these every Sunday.',
              freshness_text: 'Harvested 12 Oct, best within 7 days',
              freshness_status: 'fresh',
              available: true,
            },
            {
              product_id: 'prod-010',
              product_name: 'Toned Milk',
              unit: '1 L',
              quantity: 1,
              price_inr: 32.0,
              source_reason_tag: 'frequently_bought',
              reason_text: 'Bought in 5 of your last 6 orders.',
              freshness_text: 'Expires in 1 day',
              freshness_status: 'warning',
              available: true,
            },
            {
              product_id: 'prod-012',
              product_name: 'Fresh Paneer',
              unit: '200 g',
              quantity: 1,
              price_inr: 95.0,
              source_reason_tag: 'frequently_bought',
              reason_text: 'Often bought together with Spinach.',
              freshness_text: 'Expires in 1 day',
              freshness_status: 'warning',
              available: true,
            },
            {
              product_id: 'prod-015',
              product_name: 'Organic Quinoa',
              unit: '500 g',
              quantity: 1,
              price_inr: 310.0,
              source_reason_tag: 'based_on_diet',
              reason_text: 'A plant protein that fits your vegetarian preference.',
              is_organic: true,
              freshness_text: 'Unavailable until Mon',
              freshness_status: 'unavailable',
              available: false,
            },
          ],
          created_at: new Date().toISOString(),
        },
        {
          list_id: 'lst-082',
          name: 'Vegan Essentials',
          is_ai_generated: true,
          suggestion_note: 'You buy these every Sunday.',
          items: [],
          created_at: new Date().toISOString(),
        },
      ];
      setLists(mockLists);
      setCurrentList(mockLists[1]); // Default to AI-generated list
      setError(null);
    } catch (err) {
      setError('Failed to load shopping lists');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateList = async (e: React.FormEvent) => {
    e.preventDefault();
    setGenerationSuccess(true);
    setShowGenerateDialog(false);
    // In real implementation, would call POST /api/v1/shopping-lists/generate
  };

  const updateQuantity = (productId: string, delta: number) => {
    if (!currentList) return;
    setCurrentList({
      ...currentList,
      items: currentList.items.map((item) =>
        item.product_id === productId
          ? { ...item, quantity: Math.max(1, item.quantity + delta) }
          : item
      ),
    });
  };

  const removeItem = (productId: string) => {
    if (!currentList) return;
    setCurrentList({
      ...currentList,
      items: currentList.items.filter((item) => item.product_id !== productId),
    });
  };

  const calculateTotal = () => {
    if (!currentList) return { count: 0, total: 0 };
    const availableItems = currentList.items.filter((item) => item.available);
    return {
      count: availableItems.length,
      total: availableItems.reduce((sum, item) => sum + item.price_inr * item.quantity, 0),
    };
  };

  if (loading) {
    return (
      <div style={{ padding: '32px 64px' }}>
        <p>Loading shopping lists...</p>
      </div>
    );
  }

  const { count: availableCount, total: totalAmount } = calculateTotal();

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
          <a href="/planner/lists" style={{ background: '#fff', color: colors.primaryDark, textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }} aria-current="page">Lists</a>
          <a href="/account/orders" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Orders</a>
          <a href="/account" style={{ color: '#fff', textDecoration: 'none', fontWeight: 600, fontSize: '16px', minHeight: '44px', display: 'inline-flex', alignItems: 'center', padding: '0 16px', borderRadius: '6px' }}>Account</a>
        </nav>
      </header>

      {/* Main content */}
      <main style={{ padding: '32px 64px 48px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
          <div>
            <h1 style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '36px', fontWeight: 600, lineHeight: 1.2, margin: 0 }}>Shopping lists</h1>
            <p style={{ color: colors.muted, marginTop: '6px', margin: 0 }}>Keep your regular lists, or let GreenBasket AI draft one from your past orders. You review everything before it goes to your cart.</p>
          </div>
          <button
            onClick={() => setShowGenerateDialog(true)}
            style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.primary, color: '#fff', fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}
          >
            Generate a list with AI
          </button>
        </div>

        {generationSuccess && (
          <div role="status" aria-live="polite" style={{ background: colors.primaryTint, border: `1px solid #B9D8C4`, borderRadius: '6px', padding: '12px 16px', fontSize: '15px', marginTop: '20px', color: '#14472B' }}>
            List generated with 6 items. Review the suggestions and save it when you are happy.
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '340px 1fr', gap: '32px', alignItems: 'start', marginTop: '24px' }}>
          {/* Sidebar - Your lists */}
          <aside style={{ display: 'flex', flexDirection: 'column', gap: '12px' }} aria-label="Your lists">
            <h2 style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 600, margin: 0 }}>Your lists</h2>
            {lists.map((list) => (
              <a
                key={list.list_id}
                href="#"
                onClick={(e) => { e.preventDefault(); setCurrentList(list); }}
                style={{
                  display: 'block',
                  textDecoration: 'none',
                  color: colors.ink,
                  border: currentList?.list_id === list.list_id ? `2px solid ${colors.primary}` : `1px solid ${colors.border}`,
                  borderRadius: '8px',
                  background: currentList?.list_id === list.list_id ? colors.primaryTint : '#fff',
                  padding: '16px',
                  fontWeight: 400,
                }}
                aria-current={currentList?.list_id === list.list_id ? 'true' : undefined}
              >
                <strong style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '18px', fontWeight: 600, display: 'block' }}>{list.name}</strong>
                <span style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '2px 10px',
                  borderRadius: '999px',
                  fontSize: '13px',
                  fontWeight: 600,
                  lineHeight: '20px',
                  border: '1px solid transparent',
                  background: list.is_ai_generated ? colors.accent : '#ECEAE2',
                  color: list.is_ai_generated ? colors.accentInk : '#3E4A43',
                  borderColor: list.is_ai_generated ? undefined : '#C9C4B2',
                }}>
                  {list.is_ai_generated ? 'AI generated' : 'Manual list'}
                </span>
                <span style={{ fontSize: '14px', color: colors.muted, marginLeft: '6px' }}>{list.items.length} items{list.list_id ? ` | ${list.list_id}` : ''}</span>
                {list.suggestion_note && (
                  <p style={{ fontSize: '14px', color: colors.muted, marginTop: '4px', margin: 0 }}>{list.suggestion_note}</p>
                )}
              </a>
            ))}
          </aside>

          {/* Main list content */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {currentList && (
              <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }} aria-labelledby="ld-title">
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
                      <h2 id="ld-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '26px', fontWeight: 600, margin: 0 }}>{currentList.name}</h2>
                      {currentList.is_ai_generated && (
                        <span style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '6px',
                          padding: '2px 10px',
                          borderRadius: '999px',
                          fontSize: '13px',
                          fontWeight: 600,
                          lineHeight: '20px',
                          background: colors.accent,
                          color: colors.accentInk,
                        }}>
                          AI generated
                        </span>
                      )}
                    </div>
                    {currentList.suggestion_note && (
                      <p style={{ fontSize: '14px', color: colors.muted, marginTop: '4px', margin: 0 }}>{currentList.suggestion_note} Nothing is added to your cart until you choose.</p>
                    )}
                  </div>
                  <button style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.surface, color: colors.primary, fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                    Rename list
                  </button>
                </div>

                {/* Items table */}
                <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '16px' }}>
                  <caption style={{ textAlign: 'left', fontFamily: "'Fraunces', Georgia, serif", fontSize: '20px', fontWeight: 600, paddingBottom: '8px' }}>Items in this list (editable)</caption>
                  <thead>
                    <tr>
                      <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', background: colors.surfaceAlt }}>Product</th>
                      <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', background: colors.surfaceAlt }}>Why it is here</th>
                      <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', background: colors.surfaceAlt }}>Quantity</th>
                      <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '14px', background: colors.surfaceAlt }}>Price</th>
                      <th scope="col" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '14px', background: colors.surfaceAlt }}>
                        <span style={{ position: 'absolute', left: '-9999px' }}>Actions</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {currentList.items.map((item) => (
                      <tr key={item.product_id}>
                        <th scope="row" style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', fontWeight: 400, verticalAlign: 'middle' }}>
                          <span style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '17px', fontWeight: 600 }}>{item.product_name}</span>
                          <br />
                          {item.is_organic && <FreshnessChip type="fresh" text="Organic" />}
                          {' '}
                          {item.freshness_text && <FreshnessChip type={item.freshness_status || 'fresh'} text={item.freshness_text} />}
                        </th>
                        <td style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', verticalAlign: 'middle' }}>
                          <ReasonChip text={item.source_reason_tag} />
                          <br />
                          <span style={{ fontSize: '14px', color: colors.muted }}>{item.reason_text}</span>
                        </td>
                        <td style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', verticalAlign: 'middle' }}>
                          <div style={{ display: 'inline-flex', alignItems: 'center', border: '1px solid #8A8570', borderRadius: '6px', background: '#fff' }} role="group" aria-label={`Quantity of ${item.product_name}`}>
                            <button
                              type="button"
                              onClick={() => updateQuantity(item.product_id, -1)}
                              aria-label={`Decrease quantity of ${item.product_name}`}
                              style={{ width: '44px', height: '44px', border: 0, background: 'transparent', fontSize: '20px', fontWeight: 700, color: colors.primary, cursor: 'pointer' }}
                            >
                              -
                            </button>
                            <output style={{ minWidth: '36px', textAlign: 'center', fontWeight: 700, fontSize: '17px' }}>{item.quantity}</output>
                            <button
                              type="button"
                              onClick={() => updateQuantity(item.product_id, 1)}
                              aria-label={`Increase quantity of ${item.product_name}`}
                              style={{ width: '44px', height: '44px', border: 0, background: 'transparent', fontSize: '20px', fontWeight: 700, color: colors.primary, cursor: 'pointer' }}
                            >
                              +
                            </button>
                          </div>
                        </td>
                        <td style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'right', fontSize: '15px', fontVariantNumeric: 'tabular-nums', verticalAlign: 'middle' }}>
                          ₹{item.price_inr.toFixed(2)}
                        </td>
                        <td style={{ padding: '12px', borderBottom: `1px solid ${colors.border}`, textAlign: 'left', fontSize: '15px', verticalAlign: 'middle' }}>
                          {item.available ? (
                            <a href="/shop/cart" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.surface, color: colors.primary, fontSize: '15px', fontWeight: 600, textDecoration: 'none', cursor: 'pointer' }} aria-label={`Add ${item.product_name} to cart`}>
                              Add to cart
                            </a>
                          ) : (
                            <span style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', background: '#ECEAE2', color: '#3E4A43', border: '1px solid #C9C4B2', fontSize: '15px', fontWeight: 600 }} aria-disabled="true">
                              Unavailable
                            </span>
                          )}
                          {' '}
                          <button
                            type="button"
                            onClick={() => removeItem(item.product_id)}
                            aria-label={`Remove ${item.product_name} from list`}
                            style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 12px', background: 'transparent', borderColor: 'transparent', color: '#8A1B14', fontSize: '15px', fontWeight: 600, border: 0, cursor: 'pointer' }}
                          >
                            Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                <p style={{ fontSize: '14px', color: colors.muted, marginTop: '8px', margin: 0 }}>No item in this list contains peanuts, matching the allergy saved on your profile.</p>

                {/* Add all to cart bar */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '16px', background: colors.primaryDark, color: '#fff', borderRadius: '8px', padding: '16px 20px', marginTop: '16px' }}>
                  <div>
                    <strong style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '20px' }}>
                      Add all to cart ({availableCount} items, ₹{totalAmount.toFixed(2)})
                    </strong>
                    <p style={{ fontSize: '14px', color: '#E3F0E7', margin: 0 }}>Review before adding. Items you removed or left out are not added.</p>
                  </div>
                  <a href="/shop/cart" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', background: colors.accent, color: colors.accentInk, border: `1px solid ${colors.accent}`, fontSize: '15px', fontWeight: 600, textDecoration: 'none', cursor: 'pointer' }}>
                    Add all to cart
                  </a>
                </div>
              </section>
            )}

            {/* Reorder reminders section */}
            <section style={{ background: colors.surface, border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '24px', boxShadow: '0 1px 2px rgba(27,42,33,.08)' }} aria-labelledby="rr-title">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
                  <h2 id="rr-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 600, margin: 0 }}>Reorder reminders</h2>
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '2px 10px', borderRadius: '999px', fontSize: '13px', fontWeight: 600, lineHeight: '20px', background: colors.accent, color: colors.accentInk }}>
                    AI suggested
                  </span>
                </div>
                <span style={{ fontSize: '14px', color: colors.muted }}>2 items due</span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px', marginTop: '12px' }}>
                <div style={{ border: '1px solid #8A8570', borderRadius: '8px', padding: '14px', background: '#fff' }}>
                  <strong style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '17px', fontWeight: 600 }}>Carrots, 500 g</strong>
                  <p style={{ display: 'flex', flexWrap: 'wrap', marginTop: '4px', margin: 0 }}>
                    <ReasonChip text="reorder_reminder" />
                  </p>
                  <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>You buy these every Sunday.</p>
                  <p style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px', margin: 0 }}>
                    <button style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.surface, color: colors.primary, fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                      Add to list
                    </button>
                    <a href="/shop/cart" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.primary, color: '#fff', fontSize: '15px', fontWeight: 600, textDecoration: 'none', cursor: 'pointer' }}>
                      Add to cart
                    </a>
                  </p>
                </div>
                <div style={{ border: '1px solid #8A8570', borderRadius: '8px', padding: '14px', background: '#fff' }}>
                  <strong style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '17px', fontWeight: 600 }}>Whole Wheat Bread, 400 g</strong>
                  <p style={{ display: 'flex', flexWrap: 'wrap', marginTop: '4px', margin: 0 }}>
                    <ReasonChip text="reorder_reminder" />
                  </p>
                  <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>Last bought 7 days ago.</p>
                  <p style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px', margin: 0 }}>
                    <button style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.surface, color: colors.primary, fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                      Add to list
                    </button>
                    <a href="/shop/cart" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.primary, color: '#fff', fontSize: '15px', fontWeight: 600, textDecoration: 'none', cursor: 'pointer' }}>
                      Add to cart
                    </a>
                  </p>
                </div>
              </div>
            </section>
          </div>
        </div>
      </main>

      {/* Generate dialog modal */}
      {showGenerateDialog && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '32px', zIndex: 1000 }} onClick={() => setShowGenerateDialog(false)}>
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="dlg-title"
            onClick={(e) => e.stopPropagation()}
            style={{ background: '#fff', borderRadius: '12px', border: `1px solid ${colors.border}`, boxShadow: '0 8px 24px rgba(27,42,33,.25)', maxWidth: '760px', width: '100%', padding: '32px' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 id="dlg-title" style={{ fontFamily: "'Fraunces', Georgia, serif", fontSize: '22px', fontWeight: 600, margin: 0 }}>Generate a shopping list</h3>
              <button
                onClick={() => setShowGenerateDialog(false)}
                style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 12px', background: 'transparent', borderColor: 'transparent', color: colors.primary, fontSize: '15px', fontWeight: 600, border: 0, cursor: 'pointer' }}
                aria-label="Close dialog"
              >
                Close
              </button>
            </div>
            <p style={{ fontSize: '14px', color: colors.muted, marginTop: '4px', margin: 0 }}>Focus stays inside this dialog and Escape closes it. The list is a draft you can edit.</p>

            <form onSubmit={handleGenerateList} style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
              <fieldset style={{ border: `1px solid ${colors.border}`, borderRadius: '8px', padding: '10px 14px', margin: 0 }}>
                <legend style={{ fontSize: '14px', fontWeight: 600, padding: '0 6px' }}>Mode</legend>
                {[
                  { value: 'weekly_reorder', label: 'Weekly reorder', desc: 'Repeat what you usually buy each week.' },
                  { value: 'diet_boost', label: 'Diet boost', desc: 'Add items that fit your saved diet.' },
                  { value: 'seasonal_refresh', label: 'Seasonal refresh', desc: 'Swap in what is in season now.' },
                ].map((mode) => (
                  <div
                    key={mode.value}
                    style={{
                      display: 'flex',
                      gap: '12px',
                      alignItems: 'flex-start',
                      border: generateMode === mode.value ? `2px solid ${colors.primary}` : `1px solid ${colors.border}`,
                      borderRadius: '8px',
                      padding: '12px',
                      background: generateMode === mode.value ? colors.primaryTint : '#fff',
                      marginTop: '8px',
                    }}
                  >
                    <input
                      type="radio"
                      name="mode"
                      id={`m-${mode.value}`}
                      value={mode.value}
                      checked={generateMode === mode.value}
                      onChange={(e) => setGenerateMode(e.target.value as typeof generateMode)}
                      style={{ width: '20px', height: '20px', marginTop: '2px', accentColor: colors.primary }}
                    />
                    <div>
                      <label htmlFor={`m-${mode.value}`} style={{ fontWeight: 700, display: 'block', cursor: 'pointer' }}>{mode.label}</label>
                      <span style={{ fontSize: '14px', color: colors.muted }}>{mode.desc}</span>
                    </div>
                  </div>
                ))}
              </fieldset>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  <label htmlFor="win" style={{ fontSize: '14px', fontWeight: 600 }}>Look back over (days, 7 to 90)</label>
                  <input
                    id="win"
                    name="sourceOrderWindowDays"
                    type="number"
                    min="7"
                    max="90"
                    value={sourceWindowDays}
                    onChange={(e) => setSourceWindowDays(parseInt(e.target.value))}
                    style={{ border: '1px solid #8A8570', borderRadius: '6px', padding: '0 12px', fontSize: '16px', background: '#fff', color: colors.ink, width: '100%', height: '44px' }}
                  />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  <label htmlFor="ln" style={{ fontSize: '14px', fontWeight: 600 }}>List name</label>
                  <input
                    id="ln"
                    name="targetListName"
                    value={listName}
                    onChange={(e) => setListName(e.target.value)}
                    style={{ border: '1px solid #8A8570', borderRadius: '6px', padding: '0 12px', fontSize: '16px', background: '#fff', color: colors.ink, width: '100%', height: '44px' }}
                  />
                </div>
              </div>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px' }}>
                <button type="submit" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.primary, color: '#fff', fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}>
                  Generate list
                </button>
                <button
                  type="button"
                  onClick={() => setShowGenerateDialog(false)}
                  style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '8px', minHeight: '44px', padding: '0 20px', borderRadius: '6px', border: `1px solid ${colors.primary}`, background: colors.surface, color: colors.primary, fontSize: '15px', fontWeight: 600, cursor: 'pointer' }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer style={{ background: colors.surfaceAlt, borderTop: `1px solid ${colors.border}`, padding: '24px 64px', color: colors.muted, fontSize: '14px' }}>
        <p style={{ margin: 0 }}>Delivering in Mumbai and Bengaluru only.</p>
        <p style={{ marginTop: '4px', margin: 0 }}>Prices in INR. Freshness information is indicative and based on harvest and expiry data.</p>
      </footer>
    </div>
  );
}
