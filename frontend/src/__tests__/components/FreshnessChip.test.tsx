import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FreshnessChip } from '../../components/FreshnessChip';

describe('FreshnessChip', () => {
  it('renders fresh type chip with correct styling', () => {
    render(<FreshnessChip type="fresh" text="Organic" />);
    const chip = screen.getByText('Organic');
    expect(chip).toBeInTheDocument();
  });

  it('renders warning type chip with correct styling', () => {
    render(<FreshnessChip type="warning" text="Low stock: 3 left" />);
    const chip = screen.getByText('Low stock: 3 left');
    expect(chip).toBeInTheDocument();
  });

  it('renders unavailable type chip with correct styling', () => {
    render(<FreshnessChip type="unavailable" text="Unavailable" />);
    const chip = screen.getByText('Unavailable');
    expect(chip).toBeInTheDocument();
  });

  it('applies minimum touch target height', () => {
    render(<FreshnessChip type="fresh" text="Test" />);
    const chip = screen.getByText('Test');
    const styles = window.getComputedStyle(chip);
    expect(parseInt(styles.lineHeight)).toBeGreaterThanOrEqual(20);
  });
});
