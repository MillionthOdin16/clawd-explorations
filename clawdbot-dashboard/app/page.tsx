'use client';

import { useState, useEffect } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import SessionHeader from '@/components/SessionHeader';
import ToolCallStream from '@/components/ToolCallStream';
import MessageStream from '@/components/MessageStream';
import ReasoningPanel from '@/components/ReasoningPanel';
import TaskTracker from '@/components/TaskTracker';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { apiClient } from '@/lib';
import type { SessionStatus, ToolCall, Message, Task } from '@/lib/types';

export default function DashboardPage() {
  const [sessionStatus, setSessionStatus] = useState<SessionStatus | null>(null);
  const [toolCalls, setToolCalls] = useState<ToolCall[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isError, setIsError] = useState(false);
  const [reasoningCollapsed, setReasoningCollapsed] = useState(true);

  // Fetch data on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsError(false);
        const [status, tools, msgs, taskList] = await Promise.all([
          apiClient.getSessionStatus(),
          apiClient.getToolCalls(),
          apiClient.getMessages(),
          apiClient.getTasks(),
        ]);

        setSessionStatus(status);
        setToolCalls(tools);
        setMessages(msgs);
        setTasks(taskList);
      } catch (error) {
        console.error('Failed to fetch data:', error);
        setIsError(true);
      }
    };

    fetchData();

    // Poll for updates every 5 seconds
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <DashboardLayout>
      <ErrorBoundary>
        <div className="space-y-6">
          {/* Error State */}
          {isError && (
            <div className="rounded-lg border border-destructive bg-destructive/10 p-4 text-destructive">
              <p className="font-medium">Connection Error</p>
              <p className="text-sm">
                Unable to connect to Clawdbot Gateway. Please check your
                connection and try again.
              </p>
            </div>
          )}

          {/* Session Header */}
          {sessionStatus && (
            <SessionHeader sessionStatus={sessionStatus} />
          )}

          {/* Main Content Tabs */}
          <Tabs defaultValue="overview" className="space-y-4">
            <TabsList>
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="tools">Tool Calls</TabsTrigger>
              <TabsTrigger value="messages">Messages</TabsTrigger>
              <TabsTrigger value="tasks">Tasks</TabsTrigger>
            </TabsList>

            {/* Overview Tab */}
            <TabsContent value="overview" className="space-y-6">
              <div className="grid gap-6 lg:grid-cols-2">
                {/* Recent Tool Calls */}
                <div>
                  <h3 className="mb-4 text-lg font-semibold">Recent Tool Calls</h3>
                  <ToolCallStream toolCalls={toolCalls.slice(-10)} />
                </div>

                {/* Recent Messages */}
                <div>
                  <h3 className="mb-4 text-lg font-semibold">Recent Messages</h3>
                  <MessageStream messages={messages.slice(-10)} />
                </div>
              </div>

              {/* Reasoning Panel */}
              <div>
                <h3 className="mb-4 text-lg font-semibold">Reasoning Process</h3>
                <ReasoningPanel
                  reasoning="Analyzing current session state and planning next actions based on user requirements and system constraints."
                  isCollapsed={reasoningCollapsed}
                  onToggle={() => setReasoningCollapsed(!reasoningCollapsed)}
                />
              </div>

              {/* Task Overview */}
              <div>
                <h3 className="mb-4 text-lg font-semibold">Active Tasks</h3>
                <TaskTracker tasks={tasks} />
              </div>
            </TabsContent>

            {/* Tool Calls Tab */}
            <TabsContent value="tools">
              <ToolCallStream toolCalls={toolCalls} />
            </TabsContent>

            {/* Messages Tab */}
            <TabsContent value="messages">
              <MessageStream messages={messages} />
            </TabsContent>

            {/* Tasks Tab */}
            <TabsContent value="tasks">
              <TaskTracker tasks={tasks} />
            </TabsContent>
          </Tabs>
        </div>
      </ErrorBoundary>
    </DashboardLayout>
  );
}
