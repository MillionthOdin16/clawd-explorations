import { describe, it, expect } from 'vitest';
import { searchToolCalls, searchMessages, searchTasks, getDataSummary } from '@/lib/utils/search';
import type { ToolCall, Message, Task } from '@/lib/types';

describe('searchToolCalls', () => {
  const mockToolCalls: ToolCall[] = [
    {
      id: '1',
      timestamp: new Date().toISOString(),
      tool: 'read',
      status: 'success',
      parameters: { path: '/test/file.txt' },
      result: 'content',
    },
    {
      id: '2',
      timestamp: new Date().toISOString(),
      tool: 'write',
      status: 'error',
      parameters: { path: '/other/file.txt' },
      error: 'Permission denied',
    },
    {
      id: '3',
      timestamp: new Date().toISOString(),
      tool: 'exec',
      status: 'running',
      parameters: { command: 'ls -la' },
    },
  ];

  it('should return all tool calls when query is empty', () => {
    const results = searchToolCalls(mockToolCalls, '');

    expect(results).toEqual(mockToolCalls);
  });

  it('should search by tool name', () => {
    const results = searchToolCalls(mockToolCalls, 'read');

    expect(results).toHaveLength(1);
    expect(results[0].tool).toBe('read');
  });

  it('should search by tool name (case insensitive)', () => {
    const results = searchToolCalls(mockToolCalls, 'READ');

    expect(results).toHaveLength(1);
    expect(results[0].tool).toBe('read');
  });

  it('should search by parameters', () => {
    const results = searchToolCalls(mockToolCalls, 'file.txt');

    expect(results).toHaveLength(2);
  });

  it('should search by error message', () => {
    const results = searchToolCalls(mockToolCalls, 'Permission');

    expect(results).toHaveLength(1);
    expect(results[0].error).toContain('Permission');
  });

  it('should return empty array when no matches', () => {
    const results = searchToolCalls(mockToolCalls, 'nonexistent');

    expect(results).toHaveLength(0);
  });
});

describe('searchMessages', () => {
  const mockMessages: Message[] = [
    {
      id: '1',
      timestamp: new Date().toISOString(),
      role: 'user',
      content: 'Hello, how are you?',
    },
    {
      id: '2',
      timestamp: new Date().toISOString(),
      role: 'assistant',
      content: 'I am doing great!',
      reasoning: 'User is greeting me',
    },
    {
      id: '3',
      timestamp: new Date().toISOString(),
      role: 'user',
      content: 'Can you help me with a task?',
    },
  ];

  it('should return all messages when query is empty', () => {
    const results = searchMessages(mockMessages, '');

    expect(results).toEqual(mockMessages);
  });

  it('should search by content', () => {
    const results = searchMessages(mockMessages, 'Hello');

    expect(results).toHaveLength(1);
    expect(results[0].content).toContain('Hello');
  });

  it('should search by content (case insensitive)', () => {
    const results = searchMessages(mockMessages, 'HELLO');

    expect(results).toHaveLength(1);
  });

  it('should search by reasoning', () => {
    const results = searchMessages(mockMessages, 'greeting');

    expect(results).toHaveLength(1);
    expect(results[0].reasoning).toContain('greeting');
  });

  it('should return empty array when no matches', () => {
    const results = searchMessages(mockMessages, 'nonexistent');

    expect(results).toHaveLength(0);
  });
});

describe('searchTasks', () => {
  const mockTasks: Task[] = [
    {
      id: '1',
      description: 'Create API client',
      status: 'complete',
      priority: 10,
      completedAt: new Date().toISOString(),
    },
    {
      id: '2',
      description: 'Build dashboard',
      status: 'in-progress',
      priority: 8,
    },
    {
      id: '3',
      description: 'Add testing',
      status: 'pending',
      priority: 7,
    },
  ];

  it('should return all tasks when query is empty', () => {
    const results = searchTasks(mockTasks, '');

    expect(results).toEqual(mockTasks);
  });

  it('should search by description', () => {
    const results = searchTasks(mockTasks, 'API');

    expect(results).toHaveLength(1);
    expect(results[0].description).toContain('API');
  });

  it('should search by status', () => {
    const results = searchTasks(mockTasks, 'complete');

    expect(results).toHaveLength(1);
    expect(results[0].status).toBe('complete');
  });

  it('should return empty array when no matches', () => {
    const results = searchTasks(mockTasks, 'nonexistent');

    expect(results).toHaveLength(0);
  });
});

describe('getDataSummary', () => {
  const mockData = {
    toolCalls: [
      {
        id: '1',
        timestamp: new Date(Date.now() - 5000).toISOString(),
        tool: 'read',
        status: 'success',
      },
      {
        id: '2',
        timestamp: new Date().toISOString(),
        tool: 'write',
        status: 'error',
      },
    ] as ToolCall[],
    messages: [
      {
        id: '1',
        timestamp: new Date().toISOString(),
        role: 'user' as const,
        content: 'Hello',
      },
      {
        id: '2',
        timestamp: new Date().toISOString(),
        role: 'assistant' as const,
        content: 'Hi',
      },
    ] as Message[],
    tasks: [
      {
        id: '1',
        description: 'Task 1',
        status: 'complete',
        priority: 10,
        completedAt: new Date().toISOString(),
      },
      {
        id: '2',
        description: 'Task 2',
        status: 'in-progress',
        priority: 8,
      },
      {
        id: '3',
        description: 'Task 3',
        status: 'pending',
        priority: 7,
      },
    ] as Task[],
  };

  it('should calculate total counts correctly', () => {
    const summary = getDataSummary(mockData);

    expect(summary.totalToolCalls).toBe(2);
    expect(summary.totalMessages).toBe(2);
    expect(summary.totalTasks).toBe(3);
  });

  it('should calculate tool call statistics', () => {
    const summary = getDataSummary(mockData);

    expect(summary.successfulToolCalls).toBe(1);
    expect(summary.failedToolCalls).toBe(1);
  });

  it('should calculate task statistics', () => {
    const summary = getDataSummary(mockData);

    expect(summary.completedTasks).toBe(1);
    expect(summary.inProgressTasks).toBe(1);
    expect(summary.pendingTasks).toBe(1);
  });

  it('should calculate session duration', () => {
    const summary = getDataSummary(mockData);

    expect(summary.sessionDuration).not.toBeNull();
    expect(summary.sessionDuration).toContain('s');
  });

  it('should handle empty data', () => {
    const summary = getDataSummary({
      toolCalls: [],
      messages: [],
      tasks: [],
    });

    expect(summary.totalToolCalls).toBe(0);
    expect(summary.totalMessages).toBe(0);
    expect(summary.totalTasks).toBe(0);
    expect(summary.sessionDuration).toBeNull();
  });

  it('should handle single tool call', () => {
    const summary = getDataSummary({
      ...mockData,
      toolCalls: [mockData.toolCalls[0]],
    });

    expect(summary.totalToolCalls).toBe(1);
    expect(summary.sessionDuration).toBeNull();
  });
});
