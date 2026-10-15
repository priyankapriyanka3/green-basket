import React from 'react';
import { colors } from '../styles/colors';
import { typography } from '../styles/typography';
import { accessibility } from '../styles/accessibility';
import { FreshnessChip } from './FreshnessChip';

export interface ProductCardProps {
  productId: string;
  name: string;
  priceInr: string;
  unit: string;
  isOrganic: boolean;
  freshness?: {
    expiryDays?: number;
    harvestDate?: string;
    stockLevel?: 'available' | 'low_stock' | 'unavailable';
  };
  reviewSummary?: {
    averageRating: number;
    reviewCount: number;
    sentiment: string;
  };
  onAdd?: () => void;
  onView?: () => void;
  tileColor: string;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  productId,
  name,
  priceInr,
  unit,
  isOrganic,
  freshness,
  reviewSummary,
  onAdd,
  onView,
  tileColor,
}) => {
  const getFreshnessChips = () => {
    if (!freshness) return null;

    const chips: React.ReactNode[] = [];

    if (isOrganic) {
      chips.push(<FreshnessChip key="organic" type="fresh" text="Organic" />);
    }

    if (freshness.harvestDate && freshness.expiryDays !== undefined) {
      const harvestText = `Harvested ${freshness.harvestDate}, best within ${freshness.expiryDays} days`;
      chips.push(<FreshnessChip key="harvest" type="fresh" text={harvestText} />);
    } else if (freshness.expiryDays !== undefined && freshness.expiryDays <= 1) {
      chips.push(
        <FreshnessChip key="expiry" type="warning" text={`Expires in ${freshness.expiryDays} day`} />
      );
    }

    if (freshness.stockLevel === 'low_stock') {
      chips.push(<FreshnessChip key="stock" type="warning" text="Low stock: 3 left" />);
    } else if (freshness.stockLevel === 'unavailable') {
      chips.push(<FreshnessChip key="unavailable" type="unavailable" text="Unavailable" />);
    }

    return chips;
  };

  const getSentimentChip = (sentiment: string) => {
    if (sentiment === 'positive') {
      return <FreshnessChip type="fresh" text="positive" />;
    } else if (sentiment === 'negative') {
      return (
        <span
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            padding: '2px 10px',
            borderRadius: '999px',
            fontSize: '13px',
            fontWeight: 600,
            background: colors.status.errorBg,
            color: colors.status.errorText,
            border: `1px solid ${colors.status.errorBorder}`,
          }}
        >
          negative
        </span>
      );
    } else {
      return <FreshnessChip type="unavailable" text="neutral" />;
    }
  };

  return (
    <article
      style={{
        background: colors.surface,
        border: `1px solid ${colors.border}`,
        borderRadius: '8px',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        boxShadow: '0 1px 2px rgba(27, 42, 33, 0.08)',
      }}
    >
      <div
        style={{
          height: '96px',
          display: 'flex',
          alignItems: 'flex-end',
          padding: '12px',
          fontFamily: typography.fontFamilies.display,
          fontWeight: 600,
          fontSize: '17px',
          color: colors.primaryDark,
          background: tileColor,
        }}
        aria-hidden="true"
      >
        {name}
      </div>

      <div
        style={{
          padding: '14px',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px',
          flex: 1,
        }}
      >
        <h3
          style={{
            fontFamily: typography.fontFamilies.display,
            fontSize: '18px',
            fontWeight: 600,
            margin: 0,
          }}
        >
          <a
            href={`/shop/product/${productId}`}
            style={{
              color: 'inherit',
              textDecoration: 'none',
            }}
            onClick={(e) => {
              if (onView) {
                e.preventDefault();
                onView();
              }
            }}
          >
            {name}
          </a>
        </h3>

        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '8px',
            alignItems: 'center',
          }}
        >
          {getFreshnessChips()}
        </div>

        <p
          style={{
            fontFamily: typography.fontFamilies.display,
            fontSize: '20px',
            fontWeight: 700,
            margin: 0,
            fontVariantNumeric: 'tabular-nums',
          }}
        >
          ₹{priceInr}{' '}
          <small
            style={{
              fontFamily: typography.fontFamilies.body,
              fontSize: '14px',
              fontWeight: 400,
              color: colors.muted,
            }}
          >
            / {unit}
          </small>
        </p>

        {reviewSummary && (
          <p
            style={{
              fontSize: '14px',
              fontWeight: 600,
              margin: 0,
            }}
          >
            {reviewSummary.averageRating} out of 5{' '}
            <span style={{ color: colors.muted }}>({reviewSummary.reviewCount} reviews)</span>{' '}
            {getSentimentChip(reviewSummary.sentiment)}
          </p>
        )}

        {freshness?.stockLevel && (
          <FreshnessChip
            type={
              freshness.stockLevel === 'available'
                ? 'fresh'
                : freshness.stockLevel === 'low_stock'
                ? 'warning'
                : 'unavailable'
            }
            text={
              freshness.stockLevel === 'available'
                ? 'Available'
                : freshness.stockLevel === 'low_stock'
                ? 'low_stock'
                : 'unavailable: back in 2 days'
            }
          />
        )}

        <div
          style={{
            display: 'flex',
            gap: '8px',
            alignItems: 'center',
            marginTop: 'auto',
          }}
        >
          <button
            onClick={onAdd}
            disabled={freshness?.stockLevel === 'unavailable'}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              minHeight: `${accessibility.minTouchTarget}px`,
              padding: '0 20px',
              borderRadius: '6px',
              border: `1px solid ${colors.primary}`,
              background: freshness?.stockLevel === 'unavailable' ? colors.status.greyBg : colors.primary,
              color: freshness?.stockLevel === 'unavailable' ? colors.status.greyText : '#fff',
              fontFamily: typography.fontFamilies.body,
              fontWeight: 600,
              fontSize: '15px',
              textDecoration: 'none',
              cursor: freshness?.stockLevel === 'unavailable' ? 'not-allowed' : 'pointer',
              whiteSpace: 'nowrap',
            }}
            aria-label={`Add ${name} to cart`}
            aria-disabled={freshness?.stockLevel === 'unavailable'}
          >
            {freshness?.stockLevel === 'unavailable' ? 'Unavailable' : 'Add'}
          </button>
          <button
            onClick={onView}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              minHeight: `${accessibility.minTouchTarget}px`,
              padding: '0 12px',
              borderRadius: '6px',
              border: 'none',
              background: 'transparent',
              color: colors.primary,
              fontFamily: typography.fontFamilies.body,
              fontWeight: 600,
              fontSize: '15px',
              textDecoration: 'none',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
            }}
          >
            View
          </button>
        </div>
      </div>
    </article>
  );
};
