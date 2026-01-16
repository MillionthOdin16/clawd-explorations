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
 * Retry configuration
 */
interface RetryConfig {
  maxRetries: number;
  initialDelay: number;
  maxDelay: number;
  backoffMultiplier: number;
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 3,
  initialDelay: 1000,
  maxDelay: 10000,
  backoffMultiplier: 2,
};

/**
 * Sleep utility for retry delays
 */
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Retry with exponential backoff
 */
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  config: RetryConfig = DEFAULT_RETRY_CONFIG,
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 0; attempt < config.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      // Don't retry on certain errors
      if (
        error instanceof TypeError ||
        (error as Error).message?.includes('401') ||
        (error as Error).message?.includes('403')
      ) {
        throw lastError;
      }

      // Don't retry after last attempt
      if (attempt === config.maxRetries - 1) {
        break;
      }

      // Calculate delay with exponential backoff
      const delay = Math.min(
        config.initialDelay * Math.pow(config.backoffMultiplier, attempt),
        config.maxDelay,
      );

      console.warn(`Retry attempt ${attempt + 1}/${config.maxRetries} after ${delay}ms`);
      await sleep(delay);
    }
  }

  throw lastError;
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
   * Get request with authentication and retry logic
   */
  private async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return retryWithBackoff(async () => {
      try {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            ...(this.apiKey && { 'Authorization': `Bearer ${this.apiKey}` }),
          },
          signal: AbortSignal.timeout(30000), // 30 second timeout
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(
            `HTTP ${response.status}: ${response.statusText}${errorText ? ` - ${errorText}` : ''}`,
          );
        }

        const data = await response.json();
        return {
          success: true,
          data,
        };
      } catch (error) {
        if (error instanceof Error) {
          throw error;
        }
        throw new Error('Unknown error occurred');
      }
    });
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
  async getToolCalls(_after?: string): Promise<ToolCall[]> {
    // TODO: Replace with actual API call
    // const endpoint = _after ? `/api/session/tools?after=${_after}` : '/api/session/tools';
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
  async getMessages(after?: string, _limit: number = 50): Promise<Message[]> {
    // TODO: Replace with actual API call
    // const endpoint = after
    //   ? `/api/session/messages?after=${after}&limit=${_limit}`
    //   : `/api/session/messages?limit=${_limit}`;
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
