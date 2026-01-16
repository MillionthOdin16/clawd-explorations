import type { SessionStatus, ToolCall, Message, Task } from './types';

// API Configuration
const GATEWAY_API_URL = process.env.NEXT_PUBLIC_GATEWAY_API_URL || 'http://localhost:3000';
const API_KEY = process.env.NEXT_PUBLIC_GATEWAY_API_KEY || '';

// API Response Types
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

/**
 * API Client for Clawdbot Gateway
 */
export class ApiClient {
  private baseUrl: string;
  private apiKey: string;

  constructor(baseUrl: string = GATEWAY_API_URL, apiKey: string = API_KEY) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }

  /**
   * Get request with authentication
   */
  private async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...(this.apiKey && { 'Authorization': `Bearer ${this.apiKey}` }),
        },
      });

      if (!response.ok) {
        return {
          success: false,
          error: `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      const data = await response.json();
      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  /**
   * Get current session status
   */
  async getSessionStatus(): Promise<SessionStatus> {
    // TODO: Replace with actual API call
    // const response = await this.get<SessionStatus>('/api/session/status');
    // if (response.success && response.data) {
    //   return response.data;
    // }
    // throw new Error(response.error || 'Failed to fetch session status');

    // Mock data for POC
    return {
      sessionId: 'session-abc123',
      createdAt: new Date().toISOString(),
      model: 'zai/glm-4.7',
      status: 'running',
      runtime: {
        host: 'instance-20250109-1732',
        os: 'Linux 5.15.0-305.176.4.el9uek.aarch64 (arm64)',
        nodeVersion: 'v22.20.0',
      },
    };
  }

  /**
   * Get tool calls with optional filter
   */
  async getToolCalls(after?: string): Promise<ToolCall[]> {
    // TODO: Replace with actual API call
    // const endpoint = after ? `/api/session/tools?after=${after}` : '/api/session/tools';
    // const response = await this.get<ToolCall[]>(endpoint);
    // if (response.success && response.data) {
    //   return response.data;
    // }
    // throw new Error(response.error || 'Failed to fetch tool calls');

    // Mock data for POC
    return [
      {
        id: 'tool-1',
        timestamp: new Date(Date.now() - 5000).toISOString(),
        tool: 'read',
        status: 'success',
        parameters: { path: '/home/opc/clawd/README.md' },
        result: 'File content...',
      },
      {
        id: 'tool-2',
        timestamp: new Date(Date.now() - 3000).toISOString(),
        tool: 'exec',
        status: 'success',
        parameters: { command: 'ls -la' },
        result: 'Directory listing...',
      },
      {
        id: 'tool-3',
        timestamp: new Date().toISOString(),
        tool: 'write',
        status: 'running',
        parameters: { path: '/tmp/test.txt', content: 'Hello' },
      },
    ];
  }

  /**
   * Get messages with pagination
   */
  async getMessages(after?: string, limit: number = 50): Promise<Message[]> {
    // TODO: Replace with actual API call
    // const endpoint = after
    //   ? `/api/session/messages?after=${after}&limit=${limit}`
    //   : `/api/session/messages?limit=${limit}`;
    // const response = await this.get<Message[]>(endpoint);
    // if (response.success && response.data) {
    //   return response.data;
    // }
    // throw new Error(response.error || 'Failed to fetch messages');

    // Mock data for POC
    return [
      {
        id: 'msg-1',
        timestamp: new Date(Date.now() - 10000).toISOString(),
        role: 'user',
        content: 'Hello, how are you doing?',
      },
      {
        id: 'msg-2',
        timestamp: new Date(Date.now() - 8000).toISOString(),
        role: 'assistant',
        content: 'I\'m doing great! I just helped deploy a Minecraft server and I\'m now working on a web dashboard. How can I help you today?',
      },
    ];
  }

  /**
   * Get tasks with optional filter
   */
  async getTasks(): Promise<Task[]> {
    // TODO: Replace with actual API call
    // const response = await this.get<Task[]>('/api/session/tasks');
    // if (response.success && response.data) {
    //   return response.data;
    // }
    // throw new Error(response.error || 'Failed to fetch tasks');

    // Mock data for POC
    return [
      {
        id: 'task-1',
        description: 'Initialize Next.js project',
        status: 'complete',
        priority: 10,
        completedAt: new Date(Date.now() - 60000).toISOString(),
      },
      {
        id: 'task-2',
        description: 'Create TypeScript types',
        status: 'in-progress',
        priority: 8,
      },
      {
        id: 'task-3',
        description: 'Implement API client',
        status: 'pending',
        priority: 7,
      },
    ];
  }
}

// Create singleton instance
export const apiClient = new ApiClient();
