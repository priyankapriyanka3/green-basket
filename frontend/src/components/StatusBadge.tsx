import React from 'react';
import { colors } from '../styles/colors';

interface StatusBadgeProps {
  status: 'payment_pending' | 'confirmed' | 'packed' | 'out_for_delivery' | 'delivered' | 'cancelled' | 'payment_failed';
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, className = '' }) => {
  const getStatusStyle = () => {
    switch (status) {
      case 'confirmed':
        return {
          backgroundColor: colors.status.freshBg,
          color: colors.status.freshText,
          borderColor: colors.status.freshBorder,
        };
      case 'out_for_delivery':
        return {
          backgroundColor: colors.status.infoBg,
          color: colors.status.infoText,
          borderColor: colors.status.infoBorder,
        };
      case 'delivered':
        return {
          backgroundColor: colors.status.freshBg,
          color: colors.status.freshText,
          borderColor: colors.status.freshBorder,
        };
      case 'payment_pending':
        return {
          backgroundColor: colors.status.warningBg,
          color: colors.status.warningText,
          borderColor: colors.status.warningBorder,
        };
      case 'packed':
        return {
          backgroundColor: colors.accentTint,
          color: colors.accentInk,
          borderColor: '#EBCB7A',
        };
      case 'cancelled':
      case 'payment_failed':
        return {
          backgroundColor: colors.status.greyBg,
          color: colors.status.greyText,
          borderColor: colors.status.greyBorder,
        };
      default:
        return {
          backgroundColor: colors.status.greyBg,
          color: colors.status.greyText,
          borderColor: colors.status.greyBorder,
        };
    }
  };

  const style = getStatusStyle();

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border ${className}`}
      style={{
        backgroundColor: style.backgroundColor,
        color: style.color,
        borderColor: style.borderColor,
        lineHeight: '20px',
      }}
    >
      {status.replace(/_/g, ' ')}
    </span>
  );
};
