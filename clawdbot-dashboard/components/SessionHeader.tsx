'use client';

import { Clock, Cpu, Database, Activity } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { StatusBadge } from '@/components/ui/StatusBadge';
import type { SessionHeaderProps } from '@/lib/types';

export default function SessionHeader({
  sessionStatus,
}: Omit<SessionHeaderProps, 'isConnected'>) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <Card>
      <CardContent className="p-6">
        <div className="space-y-4">
          {/* Session Info */}
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <Activity className="h-5 w-5" />
                <h2 className="text-xl font-semibold">Session Status</h2>
              </div>
              <p className="text-sm text-muted-foreground">
                Session ID: {sessionStatus.sessionId}
              </p>
            </div>
            <StatusBadge status={sessionStatus.status} />
          </div>

          {/* Details Grid */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {/* Created At */}
            <div className="space-y-1">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Clock className="h-4 w-4" />
                <span>Created</span>
              </div>
              <p className="text-sm font-medium">
                {formatDate(sessionStatus.createdAt)}
              </p>
            </div>

            {/* Model */}
            <div className="space-y-1">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Database className="h-4 w-4" />
                <span>Model</span>
              </div>
              <p className="text-sm font-medium">{sessionStatus.model}</p>
            </div>

            {/* Host */}
            <div className="space-y-1">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Cpu className="h-4 w-4" />
                <span>Host</span>
              </div>
              <p className="text-sm font-medium">{sessionStatus.runtime.host}</p>
            </div>

            {/* OS */}
            <div className="space-y-1">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Activity className="h-4 w-4" />
                <span>Runtime</span>
              </div>
              <p className="text-sm font-medium">
                {sessionStatus.runtime.os} ({sessionStatus.runtime.nodeVersion})
              </p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
