import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import StatusBadge from '@/components/ui/StatusBadge';

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

  it('should render pending status correctly', () => {
    render(<StatusBadge status="pending" />);
    expect(screen.getByText('pending')).toBeInTheDocument();
  });

  it('should render in-progress status correctly', () => {
    render(<StatusBadge status="in-progress" />);
    expect(screen.getByText('in-progress')).toBeInTheDocument();
  });

  it('should render complete status correctly', () => {
    render(<StatusBadge status="complete" />);
    expect(screen.getByText('complete')).toBeInTheDocument();
  });

  it('should render idle status correctly', () => {
    render(<StatusBadge status="idle" />);
    expect(screen.getByText('idle')).toBeInTheDocument();
  });

  it('should render processing status correctly', () => {
    render(<StatusBadge status="processing" />);
    expect(screen.getByText('processing')).toBeInTheDocument();
  });

  it('should apply custom className', () => {
    const { container } = render(
      <StatusBadge status="running" className="custom-class" />
    );
    expect(container.firstChild).toHaveClass('custom-class');
  });
});
