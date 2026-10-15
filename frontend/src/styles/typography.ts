// Typography constants for GreenBasket AI matching wireframe fonts

export const typography = {
  // Font families matching wireframe
  fontFamilies: {
    display: 'Fraunces, Georgia, serif',          // --gb-display
    body: 'Source Sans 3, Segoe UI, system-ui, sans-serif',  // --gb-body
  },
  
  // Font sizes (minimum 14px for interactive text per WCAG 2.1 AA)
  fontSize: {
    xs: '13px',      // Small labels
    sm: '14px',      // Minimum for interactive elements
    base: '16px',    // Body text
    lg: '18px',      // Large body
    xl: '20px',      // Subheadings
    '2xl': '24px',   // H2
    '3xl': '30px',   // H1
    '4xl': '36px',   // Hero
  },
  
  // Font weights
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  
  // Line heights
  lineHeight: {
    tight: 1.2,      // Headings
    normal: 1.5,     // Body
    relaxed: 1.75,
  },
};

export default typography;
