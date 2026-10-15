import React, { useState } from 'react';
import { colors } from '../styles/colors';
import { typography } from '../styles/typography';
import { accessibility } from '../styles/accessibility';
import { FreshnessChip } from './FreshnessChip';
import { ReasonChip } from './ReasonChip';

export interface RecommendationCardProps {
  productId: string;
  name: string;
  priceInr: string;
  unit: string;
  isOrganic: boolean;
  reasonTag: string;
  reasonText: string;
  freshness?: {
    expiryDays?: number;
    harvestDate?: string;
    stockLevel?: 'available' | 'low_stock' | 'unavailable';
  };
  onAdd?: () => void;
  onAddToList?: () => void;
  tileColor: string;
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({
  productId,
  name,
  priceInr,
  unit,
  isOrganic,
  reasonTag,
  reasonText,
  freshness,
  onAdd,
  onAddToList,
  tileColor,
}) => {
  const [expanded, setExpanded] = useState(false);

  const getFreshnessChips = () => {
    const chips: React.ReactNode[] = [];

    if (isOrganic) {
      chips.push(<FreshnessChip key="organic" type="fresh" text="Organic" />);
    }

    if (freshness?.harvestDate && freshness?.expiryDays !== undefined) {
      const harvestText = `Harvested ${freshness.harvestDate}, best within ${freshness.expiryDays} days`;
      chips.push(<FreshnessChip key="harvest" type="fresh" text={harvestText} />);
    } else if (freshness?.expiryDays !== undefined && freshness.expiryDays <= 1) {
      chips.push(
        <FreshnessChip key="expiry" type="warning" text={`Expires in ${freshness.expiryDays} day`} />
      );
    }

    if (freshness?.stockLevel === 'low_stock') {
      chips.push(<FreshnessChip key="stock" type="warning" text="Low stock: 3 left" />);
    } else if (freshness?.stockLevel === 'unavailable') {
      chips.push(<FreshnessChip key="unavailable" type="unavailable" text="Unavailable until Mon" />);
    }

    return chips;
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
          height: '112px',
          display: 'flex',
          alignItems: 'flex-end',
          padding: '12px',
          fontFamily: typography.fontFamilies.display,
          fontWeight: 600,
          fontSize: '18px',
          color: colors.primaryDark,
          background: tileColor,
        }}
        aria-hidden="true"
      >
        {name}
      </div>

      <div
        style={{
          padding: '16px',
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
            fontSize: '22px',
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

        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '8px',
          }}
        >
          <ReasonChip text={reasonTag} />
        </div>

        <p
          style={{
            fontSize: '14px',
            color: colors.muted,
            margin: 0,
          }}
        >
          {reasonText}
        </p>

        <button
          onClick={() => setExpanded(!expanded)}
          type="button"
          aria-expanded={expanded}
          style={{
            fontSize: '14px',
            fontWeight: 600,
            background: 'none',
            border: 0,
            color: colors.primary,
            padding: 0,
            minHeight: '32px',
            textAlign: 'left',
            textDecoration: 'underline',
            cursor: 'pointer',
            fontFamily: typography.fontFamilies.body,
          }}
        >
          Why am I seeing this?
        </button>

        {expanded && (
          <p
            style={{
              fontSize: '14px',
              background: colors.surfaceAlt,
              borderRadius: '6px',
              padding: '8px 12px',
              margin: 0,
            }}
          >
            {reasonText}
          </p>
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
              borderColor: freshness?.stockLevel === 'unavailable' ? colors.status.greyBorder : colors.primary,
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
            onClick={onAddToList}
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
            aria-label={`Add ${name} to a list`}
          >
            Add to list
          </button>
        </div>
      </div>
    </article>
  );
};
