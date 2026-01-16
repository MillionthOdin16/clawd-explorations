'use client';

import { ChevronDown, ChevronRight, Brain } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import type { ReasoningPanelProps } from '@/lib/types';

export default function ReasoningPanel({
  reasoning,
  isCollapsed = true,
  onToggle,
}: ReasoningPanelProps) {
  if (!reasoning) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5" />
            <span>Reasoning Process</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            No reasoning data available
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="h-5 w-5" />
            <span>Reasoning Process</span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={onToggle}
            className="gap-2"
          >
            {isCollapsed ? (
              <>
                <span>Expand</span>
                <ChevronDown className="h-4 w-4" />
              </>
            ) : (
              <>
                <span>Collapse</span>
                <ChevronRight className="h-4 w-4" />
              </>
            )}
          </Button>
        </CardTitle>
      </CardHeader>
      {!isCollapsed && (
        <CardContent>
          <ScrollArea className="h-[300px]">
            <div className="space-y-2 pr-4">
              <div className="rounded-lg bg-muted p-4">
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {reasoning}
                </p>
              </div>
            </div>
          </ScrollArea>
        </CardContent>
      )}
    </Card>
  );
}
