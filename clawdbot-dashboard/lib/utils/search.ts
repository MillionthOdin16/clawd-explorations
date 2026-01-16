import type { ToolCall, Message, Task } from '../types';

/**
 * Search utilities
 */

/**
 * Search tool calls by text
 */
export function searchToolCalls(
  toolCalls: ToolCall[],
  query: string,
): ToolCall[] {
  if (!query.trim()) return toolCalls;

  const lowerQuery = query.toLowerCase();
  
  return toolCalls.filter((toolCall) => {
    return (
      toolCall.tool.toLowerCase().includes(lowerQuery) ||
      toolCall.id.toLowerCase().includes(lowerQuery) ||
      (toolCall.parameters && JSON.stringify(toolCall.parameters).toLowerCase().includes(lowerQuery)) ||
      (toolCall.error && toolCall.error.toLowerCase().includes(lowerQuery)) ||
      (toolCall.result && JSON.stringify(toolCall.result).toLowerCase().includes(lowerQuery))
    );
  });
}

/**
 * Search messages by text
 */
export function searchMessages(
  messages: Message[],
  query: string,
): Message[] {
  if (!query.trim()) return messages;

  const lowerQuery = query.toLowerCase();
  
  return messages.filter((message) => {
    return (
      message.content.toLowerCase().includes(lowerQuery) ||
      message.id.toLowerCase().includes(lowerQuery) ||
      message.reasoning?.toLowerCase().includes(lowerQuery)
    );
  });
}

/**
 * Search tasks by text
 */
export function searchTasks(
  tasks: Task[],
  query: string,
): Task[] {
  if (!query.trim()) return tasks;

  const lowerQuery = query.toLowerCase();
  
  return tasks.filter((task) => {
    return (
      task.description.toLowerCase().includes(lowerQuery) ||
      task.id.toLowerCase().includes(lowerQuery) ||
      task.status.toLowerCase().includes(lowerQuery)
    );
  });
}

/**
 * Search across all data types
 */
export function searchAll(data: {
  toolCalls: ToolCall[];
  messages: Message[];
  tasks: Task[];
}, query: string): {
  toolCalls: ToolCall[];
  messages: Message[];
  tasks: Task[];
  totalResults: number;
} {
  const results = {
    toolCalls: searchToolCalls(data.toolCalls, query),
    messages: searchMessages(data.messages, query),
    tasks: searchTasks(data.tasks, query),
    totalResults: 0,
  };

  results.totalResults = 
    results.toolCalls.length + 
    results.messages.length + 
    results.tasks.length;

  return results;
}

/**
 * Get search statistics
 */
export function getSearchStats(data: {
  toolCalls: ToolCall[];
  messages: Message[];
  tasks: Task[];
}, query: string): {
  toolCallMatches: number;
  messageMatches: number;
  taskMatches: number;
  totalMatches: number;
} {
  const toolCallMatches = searchToolCalls(data.toolCalls, query).length;
  const messageMatches = searchMessages(data.messages, query).length;
  const taskMatches = searchTasks(data.tasks, query).length;

  return {
    toolCallMatches,
    messageMatches,
    taskMatches,
    totalMatches: toolCallMatches + messageMatches + taskMatches,
  };
}

/**
 * Get time-based data summary
 */
export function getDataSummary(data: {
  toolCalls: ToolCall[];
  messages: Message[];
  tasks: Task[];
}): {
  totalToolCalls: number;
  totalMessages: number;
  totalTasks: number;
  successfulToolCalls: number;
  failedToolCalls: number;
  completedTasks: number;
  pendingTasks: number;
  inProgressTasks: number;
  sessionDuration: string | null;
} {
  const totalToolCalls = data.toolCalls.length;
  const successfulToolCalls = data.toolCalls.filter((t) => t.status === 'success').length;
  const failedToolCalls = data.toolCalls.filter((t) => t.status === 'error').length;
  
  const completedTasks = data.tasks.filter((t) => t.status === 'complete').length;
  const pendingTasks = data.tasks.filter((t) => t.status === 'pending').length;
  const inProgressTasks = data.tasks.filter((t) => t.status === 'in-progress').length;
  
  // Calculate session duration
  let sessionDuration: string | null = null;
  if (data.toolCalls.length > 1) {
    const first = new Date(data.toolCalls[0].timestamp).getTime();
    const last = new Date(data.toolCalls[data.toolCalls.length - 1].timestamp).getTime();
    const durationMs = last - first;
    const durationSecs = Math.floor(durationMs / 1000);
    
    if (durationSecs < 60) {
      sessionDuration = `${durationSecs}s`;
    } else if (durationSecs < 3600) {
      const mins = Math.floor(durationSecs / 60);
      const secs = durationSecs % 60;
      sessionDuration = `${mins}m ${secs}s`;
    } else {
      const hours = Math.floor(durationSecs / 3600);
      const mins = Math.floor((durationSecs % 3600) / 60);
      sessionDuration = `${hours}h ${mins}m`;
    }
  }
  
  return {
    totalToolCalls,
    totalMessages: data.messages.length,
    totalTasks: data.tasks.length,
    successfulToolCalls,
    failedToolCalls,
    completedTasks,
    pendingTasks,
    inProgressTasks,
    sessionDuration,
  };
}
