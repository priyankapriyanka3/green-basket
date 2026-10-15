import React from 'react';
import { colors } from '../styles/colors';

export interface ReasonChipProps {
  text: string;
}

export const ReasonChip: React.FC<ReasonChipProps> = ({ text }) => {
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
        background: colors.surface,
        color: colors.primaryDark,
        border: `1px solid ${colors.primary}`,
      }}
    >
      {text}
    </span>
  );
};
