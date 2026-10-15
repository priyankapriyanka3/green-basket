import React from 'react';
import { colors } from '../styles/colors';

interface WarningBannerProps {
  type?: 'warning' | 'error' | 'info' | 'success';
  children: React.ReactNode;
  className?: string;
}

export const WarningBanner: React.FC<WarningBannerProps> = ({ 
  type = 'warning', 
  children, 
  className = '' 
}) => {
  const getStyle = () => {
    switch (type) {
      case 'warning':
        return {
          backgroundColor: colors.accentTint, // marigold #FFF1CC
          borderColor: '#E3C26B',
          color: '#4F3600',
        };
      case 'error':
        return {
          backgroundColor: colors.status.errorBg,
          borderColor: colors.status.errorBorder,
          color: colors.status.errorText,
        };
      case 'info':
        return {
          backgroundColor: colors.status.infoBg,
          borderColor: colors.status.infoBorder,
          color: colors.status.infoText,
        };
      case 'success':
        return {
          backgroundColor: colors.status.freshBg,
          borderColor: colors.status.freshBorder,
          color: colors.status.freshText,
        };
      default:
        return {
          backgroundColor: colors.accentTint,
          borderColor: '#E3C26B',
          color: '#4F3600',
        };
    }
  };

  const style = getStyle();

  return (
    <div
      role="alert"
      className={`flex gap-2.5 px-4 py-3 rounded-md border text-sm ${className}`}
      style={{
        backgroundColor: style.backgroundColor,
        borderColor: style.borderColor,
        color: style.color,
        fontSize: '15px',
      }}
    >
      <div>{children}</div>
    </div>
  );
};
