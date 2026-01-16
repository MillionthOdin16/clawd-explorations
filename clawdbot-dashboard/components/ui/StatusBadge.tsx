import { CheckCircle2, XCircle, Clock, Play, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface StatusBadgeProps {
  status: 'running' | 'success' | 'error' | 'pending' | 'in-progress' | 'complete' | 'idle' | 'processing';
  className?: string;
}

/**
 * Consistent status badge across all components
 */
export function StatusBadge({ status, className }: StatusBadgeProps) {
  const getStatusColor = () => {
    switch (status) {
      case 'running':
      case 'in-progress':
        return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20';
      case 'success':
      case 'complete':
        return 'bg-green-500/10 text-green-500 border-green-500/20';
      case 'error':
        return 'bg-red-500/10 text-red-500 border-red-500/20';
      case 'pending':
        return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
      case 'idle':
        return 'bg-blue-500/10 text-blue-500 border-blue-500/20';
      case 'processing':
        return 'bg-purple-500/10 text-purple-500 border-purple-500/20';
      default:
        return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'running':
        return <Play className="h-3 w-3" />;
      case 'success':
        return <CheckCircle2 className="h-3 w-3" />;
      case 'error':
        return <XCircle className="h-3 w-3" />;
      case 'pending':
        return <Clock className="h-3 w-3" />;
      case 'in-progress':
        return <Loader2 className="h-3 w-3 animate-spin" />;
      case 'complete':
        return <CheckCircle2 className="h-3 w-3" />;
      default:
        return null;
    }
  };

  return (
    <div
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium',
        getStatusColor(),
        className,
      )}
    >
      {getStatusIcon()}
      <span className="capitalize">{status}</span>
    </div>
  );
}
