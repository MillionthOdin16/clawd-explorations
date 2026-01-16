import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { EmptyState } from '@/components/ui/EmptyState';

// Mock react-window to avoid complexity
vi.mock('react-window', () => ({
  FixedSizeList: ({ children, itemCount }: any) => (
    <div data-testid="virtualized-list" data-count={itemCount}>
      {Array.from({ length: itemCount }).map((_, index) =>
        children({ index, style: {} })
      )}
    </div>
  ),
}));

describe('UI Components', () => {
  describe('StatusBadge', () => {
    it('should render running status correctly', () => {
      render(<StatusBadge status="running" />);
      expect(screen.getByText('running')).toBeInTheDocument();
    });

    it('should render success status correctly', () => {
      render(<StatusBadge status="success" />);
      expect(screen.getByText('success')).toBeInTheDocument();
    });

    it('should render error status correctly', () => {
      render(<StatusBadge status="error" />);
      expect(screen.getByText('error')).toBeInTheDocument();
    });

    it('should render idle status correctly', () => {
      render(<StatusBadge status="idle" />);
      expect(screen.getByText('idle')).toBeInTheDocument();
    });

    it('should render processing status correctly', () => {
      render(<StatusBadge status="processing" />);
      expect(screen.getByText('processing')).toBeInTheDocument();
    });
  });

  describe('EmptyState', () => {
    it('should render with title only', () => {
      render(<EmptyState title="No data" />);
      expect(screen.getByText('No data')).toBeInTheDocument();
    });

    it('should render with title and description', () => {
      render(
        <EmptyState
          title="No data found"
          description="Please try again later"
        />
      );
      expect(screen.getByText('No data found')).toBeInTheDocument();
      expect(
        screen.getByText('Please try again later')
      ).toBeInTheDocument();
    });

    it('should render with icon', () => {
      render(
        <EmptyState
          icon={<span data-testid="test-icon">Icon</span>}
          title="Empty"
        />
      );
      expect(screen.getByTestId('test-icon')).toBeInTheDocument();
    });
  });
});
