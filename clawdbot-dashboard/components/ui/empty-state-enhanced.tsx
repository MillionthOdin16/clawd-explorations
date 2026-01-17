import { cn } from '@/lib/utils';
import { Button } from './button';
import { RefreshCw, Search, ListTodo, MessageSquare, Zap } from 'lucide-react';

interface EmptyStateProps {
  icon?: React.ReactNode;
  title?: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  className?: string;
}

export function EmptyState({
  icon,
  title = 'No data found',
  description,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div className={cn('flex min-h-[400px] flex-col items-center justify-center p-8 text-center', className)}>
      {icon && (
        <div className="mb-4 text-muted-foreground/70">
          {icon}
        </div>
      )}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold text-foreground">
          {title}
        </h3>
        {description && (
          <p className="max-w-md text-sm text-muted-foreground">
            {description}
          </p>
        )}
      </div>
      {action && (
        <div className="mt-6">
          <Button onClick={action.onClick} variant="outline">
            {action.label}
          </Button>
        </div>
      )}
    </div>
  );
}

// Pre-configured empty states for common scenarios

export function EmptyToolCalls({ onRefresh }: { onRefresh?: () => void } = {}) {
  return (
    <EmptyState
      icon={<MessageSquare className="h-12 w-12" />}
      title="No tool calls yet"
      description="Tool calls will appear here as Clawdbot executes commands and APIs."
      action={onRefresh ? { label: 'Refresh', onClick: onRefresh } : undefined}
    />
  );
}

export function EmptyMessages({ onRefresh }: { onRefresh?: () => void } = {}) {
  return (
    <EmptyState
      icon={<ListTodo className="h-12 w-12" />}
      title="No messages yet"
      description="Messages will appear here as you chat with Clawdbot."
      action={onRefresh ? { label: 'Refresh', onClick: onRefresh } : undefined}
    />
  );
}

export function EmptyTasks({ onRefresh }: { onRefresh?: () => void } = {}) {
  return (
    <EmptyState
      icon={<Zap className="h-12 w-12" />}
      title="No tasks yet"
      description="Tasks will appear here as Clawdbot processes work."
      action={onRefresh ? { label: 'Refresh', onClick: onRefresh } : undefined}
    />
  );
}

export function EmptySearchResults({ onClearSearch }: { onClearSearch?: () => void } = {}) {
  return (
    <EmptyState
      icon={<Search className="h-12 w-12" />}
      title="No results found"
      description="Try adjusting your search terms or filters to find what you're looking for."
      action={onClearSearch ? { label: 'Clear Search', onClick: onClearSearch } : undefined}
    />
  );
}

export function ConnectionError({ onRetry }: { onRetry?: () => void } = {}) {
  return (
    <EmptyState
      icon={<Zap className="h-12 w-12 text-destructive" />}
      title="Connection Error"
      description="Unable to connect to Clawdbot Gateway. Please check your connection and try again."
      action={onRetry ? { label: 'Retry Connection', onClick: onRetry } : undefined}
    />
  );
}

export function LoadingState({
  title = 'Loading...',
  description = 'Please wait while we fetch your data.'
}: {
  title?: string;
  description?: string;
}) {
  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center p-8 text-center">
      <div className="mb-4">
        <RefreshCw className="h-12 w-12 animate-spin text-muted-foreground/70" />
      </div>
      <div className="space-y-2">
        <h3 className="text-lg font-semibold text-foreground">
          {title}
        </h3>
        {description && (
          <p className="max-w-md text-sm text-muted-foreground">
            {description}
          </p>
        )}
      </div>
    </div>
  );
}
