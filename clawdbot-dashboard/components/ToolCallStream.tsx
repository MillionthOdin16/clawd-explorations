'use client';

import { useState, useEffect, useRef } from 'react';
import { ChevronDown, ChevronRight, CheckCircle, XCircle, Clock, Play } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Button } from '@/components/ui/button';
import type { ToolCallStreamProps, ToolCallStatus, ToolCall } from '@/lib/types';

interface ToolCallItemProps {
  toolCall: ToolCall;
  isExpanded: boolean;
  onToggle: () => void;
}

function ToolCallItem({ toolCall, isExpanded, onToggle }: ToolCallItemProps) {
  const getStatusIcon = (status: ToolCallStatus) => {
    switch (status) {
      case 'running':
        return <Play className="h-4 w-4 text-yellow-500" />;
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString();
  };

  return (
    <div className="border-b">
      <div
        className="flex cursor-pointer items-center gap-3 p-4 hover:bg-muted/50"
        onClick={onToggle}
      >
        {getStatusIcon(toolCall.status)}
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="font-mono font-medium">{toolCall.tool}</span>
            <Badge variant="outline">{toolCall.status}</Badge>
          </div>
          <p className="text-xs text-muted-foreground">{formatDate(toolCall.timestamp)}</p>
        </div>
        {isExpanded ? (
          <ChevronDown className="h-4 w-4" />
        ) : (
          <ChevronRight className="h-4 w-4" />
        )}
      </div>

      {isExpanded && (
        <div className="border-t p-4 space-y-2 bg-muted/30">
          <div>
            <p className="mb-1 text-sm font-semibold">Parameters</p>
            <pre className="overflow-x-auto rounded bg-background p-2 text-xs">
              {JSON.stringify(toolCall.parameters, null, 2)}
            </pre>
          </div>
          {toolCall.result && (
            <div>
              <p className="mb-1 text-sm font-semibold">Result</p>
              <pre className="overflow-x-auto rounded bg-background p-2 text-xs">
                {JSON.stringify(toolCall.result, null, 2)}
              </pre>
            </div>
          )}
          {toolCall.error && (
            <div>
              <p className="mb-1 text-sm font-semibold text-red-500">Error</p>
              <p className="text-sm text-red-500">{toolCall.error}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function ToolCallStream({
  toolCalls,
  filter = '',
  statusFilter = 'all',
}: ToolCallStreamProps) {
  const [filterText, setFilterText] = useState(filter);
  const [selectedStatus, setSelectedStatus] = useState(statusFilter);
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest tool call
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [toolCalls.length]);

  const toggleExpanded = (id: string) => {
    setExpandedItems((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const filteredToolCalls = toolCalls.filter((toolCall) => {
    const matchesText =
      !filterText ||
      toolCall.tool.toLowerCase().includes(filterText.toLowerCase()) ||
      JSON.stringify(toolCall.parameters).toLowerCase().includes(filterText.toLowerCase());

    const matchesStatus =
      selectedStatus === 'all' || toolCall.status === selectedStatus;

    return matchesText && matchesStatus;
  });

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Tool Call Stream</span>
          <Badge variant="secondary">{filteredToolCalls.length} calls</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Filters */}
        <div className="flex gap-2">
          <Input
            placeholder="Filter tool calls..."
            value={filterText}
            onChange={(e) => setFilterText(e.target.value)}
            className="flex-1"
          />
          <Button
            variant="outline"
            size="sm"
            onClick={() => setSelectedStatus(selectedStatus === 'all' ? 'running' : 'all')}
          >
            {selectedStatus === 'all' ? 'Show All' : 'Show Running'}
          </Button>
        </div>

        {/* Status Quick Filters */}
        <div className="flex gap-2">
          {['all', 'running', 'success', 'error'].map((status) => (
            <Button
              key={status}
              variant={selectedStatus === status ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedStatus(status as any)}
            >
              {status}
            </Button>
          ))}
        </div>

        <Separator />

        {/* Tool Call List */}
        <ScrollArea className="h-[500px]">
          <div ref={scrollRef}>
            {filteredToolCalls.length === 0 ? (
              <div className="p-8 text-center text-muted-foreground">
                No tool calls found
              </div>
            ) : (
              filteredToolCalls.map((toolCall) => (
                <ToolCallItem
                  key={toolCall.id}
                  toolCall={toolCall}
                  isExpanded={expandedItems.has(toolCall.id)}
                  onToggle={() => toggleExpanded(toolCall.id)}
                />
              ))
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
