import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { colors } from '../styles/colors';
import { typography } from '../styles/typography';
import { accessibility } from '../styles/accessibility';
import { FreshnessChip } from '../components/FreshnessChip';
import apiClient from '../api/client';
import type { LoginRequest, LoginResponse } from '../api/types';

export const OnboardingLogin: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  
  const [phoneNumber, setPhoneNumber] = useState('9876543210');
  const [otpOrPassword, setOtpOrPassword] = useState('Demo@123');
  const [roleHint, setRoleHint] = useState<'shopper' | 'operator'>('shopper');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validatePhoneNumber = (phone: string): boolean => {
    // 10 digit validation
    return /^\d{10}$/.test(phone);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Client-side validation
    if (!validatePhoneNumber(phoneNumber)) {
      setError('Enter a 10 digit mobile number, for example 9876543210.');
      return;
    }

    setIsSubmitting(true);

    try {
      const requestData: LoginRequest = {
        phoneNumber: `+91${phoneNumber}`,
        otpOrPassword,
        roleHint,
      };

      // Use the login function from AuthContext
      await login(requestData);

      // Redirect based on role
      if (roleHint === 'operator') {
        navigate('/ops');
      } else {
        navigate('/shop');
      }
    } catch (err: any) {
      // Handle API errors
      if (err.code === 'INVALID_CREDENTIALS') {
        setError('We could not sign you in with those details. Check your number and code and try again.');
      } else if (err.code === 'ACCOUNT_INACTIVE') {
        setError('This account is not active. Contact support.');
      } else if (err.code === 'TOO_MANY_ATTEMPTS') {
        setError('Too many attempts. Try again in 15 minutes.');
      } else if (err.code === 'PHONE_FORMAT_INVALID') {
        setError('Enter a 10 digit mobile number, for example 9876543210.');
      } else {
        setError('An error occurred. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      style={{
        width: '100%',
        minWidth: '1440px',
        background: colors.background,
      }}
    >
      {/* Skip to main content */}
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
            href="/"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              fontFamily: typography.fontFamilies.display,
              fontWeight: 700,
              fontSize: '22px',
              color: '#fff',
              textDecoration: 'none',
              whiteSpace: 'nowrap',
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
                fontFamily: typography.fontFamilies.display,
                fontWeight: 700,
                fontSize: '20px',
              }}
              aria-hidden="true"
            >
              G
            </span>
            GreenBasket AI
          </a>
          <span
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
              whiteSpace: 'nowrap',
            }}
          >
            Language: English (India)
          </span>
        </div>
      </header>

      {/* Main Content */}
      <main
        id="main"
        style={{
          padding: '32px 64px 48px',
        }}
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1.1fr 1fr',
            gap: '32px',
            alignItems: 'stretch',
          }}
        >
          {/* Left: Intro Panel */}
          <section
            style={{
              borderRadius: '8px',
              padding: '48px',
              color: '#fff',
              background: 'linear-gradient(160deg, #143F28 0%, #1F5C3A 70%, #2F7A4D 100%)',
              display: 'flex',
              flexDirection: 'column',
              gap: '24px',
              position: 'relative',
            }}
            aria-labelledby="intro-title"
          >
            <FreshnessChip type="warning" text="AI suggested, always with a reason" />

            <h1
              id="intro-title"
              style={{
                color: '#fff',
                fontSize: '40px',
                fontFamily: typography.fontFamilies.display,
                fontWeight: 600,
                lineHeight: 1.2,
                margin: 0,
              }}
            >
              Fresh groceries, planned around the way you eat.
            </h1>

            <p style={{ color: '#E8F2EB', fontSize: '18px', margin: 0 }}>
              Order fruit, vegetables, dairy and pantry staples from verified farms. GreenBasket AI shows you what is fresh today and why it suggests each item.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
              {[
                { num: '1', title: 'Fresh produce with harvest and expiry cues', desc: 'Every fruit and vegetable shows when it was harvested and how long it keeps.' },
                { num: '2', title: 'Suggestions that always say why', desc: 'Recommendations show the reason behind every suggestion, such as a weekly reorder or your diet.' },
                { num: '3', title: 'Delivery windows that respect your address', desc: 'Pick a slot only after we confirm your address is serviceable.' },
              ].map((item) => (
                <div key={item.num} style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
                  <span
                    style={{
                      flex: '0 0 36px',
                      height: '36px',
                      borderRadius: '50%',
                      background: colors.accent,
                      color: colors.accentInk,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontFamily: typography.fontFamilies.display,
                      fontWeight: 700,
                      fontSize: '18px',
                    }}
                    aria-hidden="true"
                  >
                    {item.num}
                  </span>
                  <div>
                    <strong style={{ display: 'block', fontSize: '18px', color: '#fff' }}>
                      {item.title}
                    </strong>
                    <span style={{ color: '#E8F2EB', fontSize: '15px' }}>{item.desc}</span>
                  </div>
                </div>
              ))}
            </div>

            <div
              style={{
                background: 'rgba(255, 255, 255, 0.1)',
                border: '1px solid rgba(255, 255, 255, 0.35)',
                borderRadius: '8px',
                padding: '16px',
              }}
              aria-label="Freshness example"
            >
              <p style={{ fontSize: '14px', color: '#E8F2EB', marginBottom: '8px' }}>
                Example from today's catalog: Organic Bananas, 1 dozen
              </p>
              <FreshnessChip type="fresh" text="Harvested 13 Oct, best within 4 days" />
            </div>

            <p style={{ fontWeight: 700, color: '#FFE9B0', fontSize: '16px', margin: 0 }}>
              Now delivering in Mumbai and Bengaluru
            </p>
          </section>

          {/* Right: Sign-in Form */}
          <section
            style={{
              background: colors.surface,
              border: `1px solid ${colors.border}`,
              borderRadius: '8px',
              padding: '32px',
              boxShadow: '0 1px 2px rgba(27, 42, 33, 0.08)',
            }}
            aria-labelledby="signin-title"
          >
            <form
              onSubmit={handleSubmit}
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '20px',
              }}
            >
              <div>
                <h2
                  id="signin-title"
                  style={{
                    fontFamily: typography.fontFamilies.display,
                    fontSize: '28px',
                    fontWeight: 600,
                    margin: 0,
                  }}
                >
                  Welcome back
                </h2>
                <p style={{ color: colors.muted, marginTop: '6px' }}>
                  Sign in to reorder your usual basket and check on deliveries.
                </p>
              </div>

              {error && (
                <div
                  role="alert"
                  style={{
                    display: 'flex',
                    gap: '10px',
                    padding: '12px 16px',
                    borderRadius: '6px',
                    border: `1px solid ${colors.status.errorBorder}`,
                    background: colors.status.errorBg,
                    color: colors.status.errorText,
                    fontSize: '15px',
                  }}
                >
                  <div>
                    <strong>We could not sign you in.</strong>
                    <br />
                    {error}
                  </div>
                </div>
              )}

              {/* Phone Number */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <label
                  htmlFor="phone"
                  style={{
                    fontSize: '14px',
                    fontWeight: 600,
                    color: colors.ink,
                  }}
                >
                  Phone number
                </label>
                <div style={{ display: 'flex', alignItems: 'stretch', gap: 0 }}>
                  <span
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      padding: '0 12px',
                      border: `1px solid #8A8570`,
                      borderRight: 0,
                      borderRadius: '6px 0 0 6px',
                      background: colors.surfaceAlt,
                      fontWeight: 700,
                    }}
                    aria-hidden="true"
                  >
                    +91
                  </span>
                  <input
                    id="phone"
                    name="phoneNumber"
                    type="tel"
                    inputMode="numeric"
                    autoComplete="tel-national"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    style={{
                      height: `${accessibility.minTouchTarget}px`,
                      width: '100%',
                      border: `1px solid #8A8570`,
                      borderRadius: '0 6px 6px 0',
                      padding: '0 14px',
                      fontSize: '16px',
                      fontFamily: typography.fontFamilies.body,
                      background: '#fff',
                      color: colors.ink,
                    }}
                    aria-describedby="phone-hint"
                  />
                </div>
                <span
                  id="phone-hint"
                  style={{
                    fontSize: '13px',
                    color: colors.muted,
                  }}
                >
                  Enter your 10 digit mobile number. The +91 prefix is fixed.
                </span>
              </div>

              {/* OTP or Password */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <label
                  htmlFor="secret"
                  style={{
                    fontSize: '14px',
                    fontWeight: 600,
                    color: colors.ink,
                  }}
                >
                  OTP or password
                </label>
                <div style={{ display: 'flex', alignItems: 'stretch', gap: 0 }}>
                  <input
                    id="secret"
                    name="otpOrPassword"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete="one-time-code"
                    value={otpOrPassword}
                    onChange={(e) => setOtpOrPassword(e.target.value)}
                    style={{
                      height: `${accessibility.minTouchTarget}px`,
                      width: '100%',
                      border: `1px solid #8A8570`,
                      borderRadius: '6px 0 0 6px',
                      padding: '0 14px',
                      fontSize: '16px',
                      fontFamily: typography.fontFamilies.body,
                      background: '#fff',
                      color: colors.ink,
                    }}
                    aria-describedby="secret-hint"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-pressed={showPassword}
                    aria-controls="secret"
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      minHeight: `${accessibility.minTouchTarget}px`,
                      padding: '0 20px',
                      borderRadius: '0 6px 6px 0',
                      border: `1px solid ${colors.primary}`,
                      background: colors.surface,
                      color: colors.primary,
                      fontFamily: typography.fontFamilies.body,
                      fontWeight: 600,
                      fontSize: '15px',
                      cursor: 'pointer',
                    }}
                  >
                    {showPassword ? 'Hide' : 'Show'}
                  </button>
                </div>
                <span
                  id="secret-hint"
                  style={{
                    fontSize: '13px',
                    color: colors.muted,
                  }}
                >
                  Use the 6 digit code we send you, or your password.
                </span>
              </div>

              {/* Role Selection */}
              <fieldset
                style={{
                  border: `1px solid ${colors.border}`,
                  borderRadius: '8px',
                  padding: '12px 16px 16px',
                  margin: 0,
                }}
              >
                <legend
                  style={{
                    fontSize: '14px',
                    fontWeight: 600,
                    padding: '0 6px',
                  }}
                >
                  I am signing in as
                </legend>
                <label
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    minHeight: `${accessibility.minTouchTarget}px`,
                    fontSize: '16px',
                  }}
                >
                  <input
                    type="radio"
                    name="roleHint"
                    value="shopper"
                    checked={roleHint === 'shopper'}
                    onChange={() => setRoleHint('shopper')}
                    style={{
                      width: '20px',
                      height: '20px',
                      accentColor: colors.primary,
                    }}
                  />
                  Shopper
                </label>
                <label
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    minHeight: `${accessibility.minTouchTarget}px`,
                    fontSize: '16px',
                  }}
                >
                  <input
                    type="radio"
                    name="roleHint"
                    value="operator"
                    checked={roleHint === 'operator'}
                    onChange={() => setRoleHint('operator')}
                    style={{
                      width: '20px',
                      height: '20px',
                      accentColor: colors.primary,
                    }}
                  />
                  Operator (store operations)
                </label>
              </fieldset>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isSubmitting}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  minHeight: '48px',
                  padding: '0 20px',
                  borderRadius: '6px',
                  border: `1px solid ${colors.primary}`,
                  background: isSubmitting ? colors.status.greyBg : colors.primary,
                  color: isSubmitting ? colors.status.greyText : '#fff',
                  fontFamily: typography.fontFamilies.body,
                  fontWeight: 600,
                  fontSize: '17px',
                  cursor: isSubmitting ? 'not-allowed' : 'pointer',
                  width: '100%',
                }}
              >
                {isSubmitting ? 'Signing in...' : 'Sign in'}
              </button>

              <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>
                Shoppers continue to Home (/shop). Operators continue to Operations (/ops).
              </p>
              <p style={{ fontSize: '14px', color: colors.muted, margin: 0 }}>
                Your diet and allergy details are only visible to you.
              </p>
            </form>
          </section>
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
