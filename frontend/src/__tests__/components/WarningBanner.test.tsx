import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { WarningBanner } from '../../components/WarningBanner';

describe('WarningBanner', () => {
  it('renders warning type with marigold background', () => {
    render(<WarningBanner type="warning">Test warning message</WarningBanner>);
    const banner = screen.getByRole('alert');
    expect(banner).toBeInTheDocument();
    expect(banner).toHaveTextContent('Test warning message');
    expect(banner).toHaveStyle({ backgroundColor: '#FFF1CC' });
  });

  it('renders error type with red background', () => {
    render(<WarningBanner type="error">Test error message</WarningBanner>);
    const banner = screen.getByRole('alert');
    expect(banner).toBeInTheDocument();
    expect(banner).toHaveStyle({ backgroundColor: '#FBE4E1' });
  });

  it('renders info type with blue background', () => {
    render(<WarningBanner type="info">Test info message</WarningBanner>);
    const banner = screen.getByRole('alert');
    expect(banner).toBeInTheDocument();
    expect(banner).toHaveStyle({ backgroundColor: '#E0EFF8' });
  });

  it('renders success type with green background', () => {
    render(<WarningBanner type="success">Test success message</WarningBanner>);
    const banner = screen.getByRole('alert');
    expect(banner).toBeInTheDocument();
    expect(banner).toHaveStyle({ backgroundColor: '#E3F0E7' });
  });
});
