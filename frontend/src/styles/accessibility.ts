// WCAG 2.1 AA accessibility constants for GreenBasket AI

import { colors } from './colors';

export const accessibility = {
  // Touch target sizes (minimum 44px per WCAG 2.1 AA)
  minTouchTarget: 44,
  
  // Text sizes
  minTextSize: 14,          // Minimum for interactive elements
  minBodyTextSize: 16,      // Standard body text
  
  // Focus ring (3px solid #0B5A8A with 2px offset)
  focusRing: {
    width: '3px',
    style: 'solid',
    color: colors.info,  // #0B5A8A from wireframes
    offset: '2px',
  },
  
  // Contrast ratios (WCAG 2.1 AA requirements)
  contrastRatio: {
    primary: 14,     // Primary text must be >14:1
    secondary: 6,    // Secondary text must be >6:1
  },
  
  // ARIA live region politeness levels
  ariaLive: {
    polite: 'polite' as const,
    assertive: 'assertive' as const,
    off: 'off' as const,
  },
};

// Helper function to get focus ring style
export const getFocusRingStyle = () => ({
  outline: `${accessibility.focusRing.width} ${accessibility.focusRing.style} ${accessibility.focusRing.color}`,
  outlineOffset: accessibility.focusRing.offset,
});

export default accessibility;
