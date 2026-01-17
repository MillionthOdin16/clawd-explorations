import { cn } from '@/lib/utils';

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={cn('animate-pulse rounded-md bg-muted', className)}
      role="presentation"
    />
  );
}

interface SkeletonTextProps extends SkeletonProps {
  lines?: number;
  className?: string;
}

export function SkeletonText({
  lines = 3,
  className,
  ...props
}: SkeletonTextProps) {
  return (
    <div className={cn('space-y-2', className)}>
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="space-y-2">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
        </div>
      ))}
    </div>
  );
}

interface SkeletonCardProps extends SkeletonProps {
  children?: React.ReactNode;
  className?: string;
}

export function SkeletonCard({
  children,
  className,
  ...props
}: SkeletonCardProps) {
  return (
    <div
      className={cn(
        'rounded-lg border bg-card p-6',
        className,
      )}
      {...props}
    >
      {children || (
        <>
          <Skeleton className="mb-4 h-6 w-1/2" />
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <Skeleton className="h-5 w-5 rounded-full" />
              <div className="flex-1 space-y-2">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-3/4" />
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

interface SkeletonListProps extends SkeletonProps {
  items?: number;
  className?: string;
}

export function SkeletonList({
  items = 5,
  className,
  ...props
}: SkeletonListProps) {
  return (
    <div className={cn('space-y-4', className)} {...props}>
      {Array.from({ length: items }).map((_, i) => (
        <div key={i} className="flex items-start gap-3 p-4 rounded-lg border bg-muted/30">
          <Skeleton className="h-5 w-5 rounded-full flex-shrink-0" />
          <div className="flex-1 space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
          </div>
        </div>
      ))}
    </div>
  );
}

interface SkeletonSummaryProps extends SkeletonProps {
  cards?: number;
  className?: string;
}

export function SkeletonSummary({
  cards = 4,
  className,
  ...props
}: SkeletonSummaryProps) {
  return (
    <div className={cn('grid gap-4 md:grid-cols-2 lg:grid-cols-4', className)} {...props}>
      {Array.from({ length: cards }).map((_, i) => (
        <div key={i} className="space-y-2 p-4 rounded-lg border bg-muted/30">
          <Skeleton className="h-4 w-1/2" />
          <Skeleton className="h-8 w-2/3" />
          <Skeleton className="h-3 w-full" />
        </div>
      ))}
    </div>
  );
}
