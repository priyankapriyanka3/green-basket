import React from 'react';
import { colors } from '../styles/colors';
import { accessibility } from '../styles/accessibility';

export interface FreshnessChipProps {
  type: 'fresh' | 'warning' | 'unavailable';
  text: string;
}

export const FreshnessChip: React.FC<FreshnessChipProps> = ({ type, text }) => {
  const getStyles = () => {
    switch (type) {
      case 'fresh':
        return {
          background: colors.status.freshBg,
          color: colors.status.freshText,
          border: `1px solid ${colors.status.freshBorder}`,
        };
      case 'warning':
        return {
          background: colors.status.warningBg,
          color: colors.status.warningText,
          border: `1px solid ${colors.status.warningBorder}`,
        };
      case 'unavailable':
        return {
          background: colors.status.greyBg,
          color: colors.status.greyText,
          border: `1px solid ${colors.status.greyBorder}`,
        };
    }
  };

  const styles = getStyles();

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
        padding: '2px 10px',
        borderRadius: '999px',
        fontSize: '13px',
        fontWeight: 600,
        lineHeight: '20px',
        whiteSpace: 'nowrap',
        ...styles,
      }}
    >
      {text}
    </span>
  );
};
