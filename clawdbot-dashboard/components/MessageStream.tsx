'use client';

import { useEffect, useRef } from 'react';
import { User, Bot, MessageSquare } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { EmptyState } from '@/components/ui/EmptyState';
import ReactMarkdown from 'react-markdown';
import type { MessageStreamProps, Message } from '@/lib/types';

interface MessageItemProps {
  message: Message;
}

function MessageItem({ message }: MessageItemProps) {
  const isUser = message.role === 'user';

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString();
  };

  return (
    <div className="mb-4">
      <div className="flex items-start gap-3">
        {isUser ? (
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10">
            <User className="h-5 w-5 text-primary" />
          </div>
        ) : (
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-green-500/10">
            <Bot className="h-5 w-5 text-green-500" />
          </div>
        )}

        <div className="flex-1 space-y-1">
          <div className="flex items-center gap-2">
            <span className="font-semibold">{isUser ? 'You' : 'Clawd'}</span>
            <span className="text-xs text-muted-foreground">
              {formatDate(message.timestamp)}
            </span>
          </div>

          <div className="prose prose-sm dark:prose-invert max-w-none">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>

          {message.reasoning && (
            <details className="mt-2">
              <summary className="cursor-pointer text-sm font-semibold text-muted-foreground hover:text-foreground">
                View Reasoning
              </summary>
              <div className="mt-2 rounded-lg bg-muted p-3">
                <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                  {message.reasoning}
                </p>
              </div>
            </details>
          )}
        </div>
      </div>
    </div>
  );
}

export default function MessageStream({
  messages,
  autoScroll = true,
}: MessageStreamProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    if (autoScroll && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages.length, autoScroll]);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5" />
            <span>Message Stream</span>
          </div>
          <Badge variant="secondary">{messages.length} messages</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[500px]">
          <div ref={scrollRef} className="space-y-4 pr-4">
            {messages.length === 0 ? (
              <EmptyState
                icon={<MessageSquare className="h-12 w-12" />}
                title="No messages yet"
                description="Messages will appear here as you chat with Clawdbot"
              />
            ) : (
              messages.map((message) => (
                <MessageItem key={message.id} message={message} />
              ))
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
