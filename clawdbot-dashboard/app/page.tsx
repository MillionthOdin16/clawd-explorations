'use client';

import { useState, useEffect, useMemo } from 'react';
import { Search, Download, BarChart3, RefreshCw, X } from 'lucide-react';
import DashboardLayout from '@/components/DashboardLayout';
import SessionHeader from '@/components/SessionHeader';
import ToolCallStream from '@/components/ToolCallStream';
import MessageStream from '@/components/MessageStream';
import ReasoningPanel from '@/components/ReasoningPanel';
import TaskTracker from '@/components/TaskTracker';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { apiClient } from '@/lib';
import { searchAll, getDataSummary, exportSessionData } from '@/lib/utils';
import type { SessionStatus, ToolCall, Message, Task } from '@/lib/types';

export default function DashboardPage() {
  const [sessionStatus, setSessionStatus] = useState<SessionStatus | null>(null);
  const [toolCalls, setToolCalls] = useState<ToolCall[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isError, setIsError] = useState(false);
  const [reasoningCollapsed, setReasoningCollapsed] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearch, setShowSearch] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);

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

  // Search functionality
  const searchResults = useMemo(() => {
    if (!searchQuery.trim()) {
      return { toolCalls, messages, tasks, totalResults: 0 };
    }
    return searchAll({ toolCalls, messages, tasks }, searchQuery);
  }, [toolCalls, messages, tasks, searchQuery]);

  // Data summary
  const summary = useMemo(() => {
    return getDataSummary({ toolCalls, messages, tasks });
  }, [toolCalls, messages, tasks]);

  // Manual refresh
  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
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
      console.error('Refresh failed:', error);
    } finally {
      setIsRefreshing(false);
    }
  };

  // Export data
  const handleExport = () => {
    exportSessionData({ 
      sessionStatus: sessionStatus || undefined, 
      toolCalls, 
      messages, 
      tasks 
    });
  };

  // Display data (search or original)
  const displayData = searchQuery.trim() ? searchResults : { toolCalls, messages, tasks, totalResults: 0 };

  return (
    <DashboardLayout>
      <ErrorBoundary>
        <div className="space-y-6">
          {/* Search Bar */}
          <div className="flex items-center gap-2">
            {showSearch ? (
              <>
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    placeholder="Search across all data..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                    autoFocus
                  />
                  {searchQuery && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="absolute right-2 top-1/2 h-6 -translate-y-1/2"
                      onClick={() => setSearchQuery('')}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                </div>
                {searchQuery && (
                  <Badge variant="secondary">
                    {searchResults.totalResults} results
                  </Badge>
                )}
                <Button variant="outline" onClick={() => { setShowSearch(false); setSearchQuery(''); }}>
                  <X className="h-4 w-4" />
                </Button>
              </>
            ) : (
              <Button variant="outline" onClick={() => setShowSearch(true)}>
                <Search className="mr-2 h-4 w-4" />
                Search
              </Button>
            )}

            {/* Action Buttons */}
            <div className="flex gap-2">
              <Button variant="outline" onClick={handleRefresh} disabled={isRefreshing}>
                <RefreshCw className={`mr-2 h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
              <Button onClick={handleExport}>
                <Download className="mr-2 h-4 w-4" />
                Export
              </Button>
            </div>
          </div>

          {/* Data Summary Card */}
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-muted-foreground" />
                <h3 className="font-semibold">Session Summary</h3>
              </div>
              <div className="mt-4 grid gap-4 md:grid-cols-4 lg:grid-cols-6">
                <div>
                  <p className="text-sm text-muted-foreground">Tool Calls</p>
                  <p className="text-2xl font-bold">{summary.totalToolCalls}</p>
                  <p className="text-xs text-muted-foreground">
                    {summary.successfulToolCalls} success / {summary.failedToolCalls} failed
                  </p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Messages</p>
                  <p className="text-2xl font-bold">{summary.totalMessages}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Tasks</p>
                  <p className="text-2xl font-bold">{summary.totalTasks}</p>
                  <p className="text-xs text-muted-foreground">
                    {summary.completedTasks} done / {summary.inProgressTasks} active
                  </p>
                </div>
                {summary.sessionDuration && (
                  <div>
                    <p className="text-sm text-muted-foreground">Duration</p>
                    <p className="text-2xl font-bold">{summary.sessionDuration}</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Error State */}
          {isError && (
            <div className="rounded-lg border border-destructive bg-destructive/10 p-4 text-destructive">
              <p className="font-medium">Connection Error</p>
              <p className="text-sm">
                Unable to connect to Clawdbot Gateway. Please check your connection and try again.
              </p>
            </div>
          )}

          {/* Session Header */}
          {sessionStatus && (
            <SessionHeader sessionStatus={sessionStatus} />
          )}

          {/* Search Results */}
          {searchQuery && (
            <Card>
              <CardContent className="p-4">
                <p className="text-sm text-muted-foreground">
                  Showing {searchResults.toolCalls.length} tool calls, {searchResults.messages.length} messages, {searchResults.tasks.length} tasks matching &quot;{searchQuery}&quot;
                </p>
              </CardContent>
            </Card>
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
                  <ToolCallStream toolCalls={displayData.toolCalls.slice(-10)} />
                </div>

                {/* Recent Messages */}
                <div>
                  <h3 className="mb-4 text-lg font-semibold">Recent Messages</h3>
                  <MessageStream messages={displayData.messages.slice(-10)} />
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
                <TaskTracker tasks={displayData.tasks} />
              </div>
            </TabsContent>

            {/* Tool Calls Tab */}
            <TabsContent value="tools">
              <ToolCallStream toolCalls={displayData.toolCalls} />
            </TabsContent>

            {/* Messages Tab */}
            <TabsContent value="messages">
              <MessageStream messages={displayData.messages} />
            </TabsContent>

            {/* Tasks Tab */}
            <TabsContent value="tasks">
              <TaskTracker tasks={displayData.tasks} />
            </TabsContent>
          </Tabs>
        </div>
      </ErrorBoundary>
    </DashboardLayout>
  );
}
