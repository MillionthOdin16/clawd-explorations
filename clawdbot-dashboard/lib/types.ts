// Gateway API Types

export interface SessionStatus {
  sessionId: string;
  createdAt: string;
  model: string;
  status: 'running' | 'idle' | 'processing';
  runtime: {
    host: string;
    os: string;
    nodeVersion: string;
  };
}

export interface ToolCall {
  id: string;
  timestamp: string;
  tool: string;
  status: 'running' | 'success' | 'error';
  parameters?: Record<string, unknown>;
  result?: unknown;
  error?: string;
}

export interface Message {
  id: string;
  timestamp: string;
  role: 'user' | 'assistant';
  content: string;
  reasoning?: string;
}

export interface Task {
  id: string;
  description: string;
  status: 'pending' | 'in-progress' | 'complete';
  priority?: number;
  completedAt?: string;
}

// Component Props Types

export interface ToolCallStreamProps {
  toolCalls: ToolCall[];
  filter?: string;
  statusFilter?: 'running' | 'success' | 'error' | 'all';
}

export interface MessageStreamProps {
  messages: Message[];
  autoScroll?: boolean;
}

export interface SessionHeaderProps {
  sessionStatus: SessionStatus;
  isConnected: boolean;
}

export interface ReasoningPanelProps {
  reasoning?: string;
  isCollapsed?: boolean;
  onToggle?: () => void;
}

export interface TaskTrackerProps {
  tasks: Task[];
  statusFilter?: 'pending' | 'in-progress' | 'complete' | 'all';
}

export interface DashboardLayoutProps {
  children: React.ReactNode;
}

// UI Types

export type Status = SessionStatus['status'];
export type ToolCallStatus = ToolCall['status'];
export type TaskStatus = Task['status'];
export type MessageRole = Message['role'];
