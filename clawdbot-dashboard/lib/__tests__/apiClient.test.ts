import { describe, it, expect, beforeEach, vi } from 'vitest';
import { ApiClient } from '../apiClient';
import type { SessionStatus, ToolCall, Message, Task } from '../types';

// Mock fetch
global.fetch = vi.fn();

describe('ApiClient', () => {
  let apiClient: ApiClient;
  let mockFetch: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    mockFetch = vi.fn();
    global.fetch = mockFetch;
    apiClient = new ApiClient('http://test-api', 'test-key');
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('constructor', () => {
    it('should initialize with default values', () => {
      const client = new ApiClient();
      // Client is created without error
      expect(client).toBeDefined();
    });

    it('should initialize with custom values', () => {
      const client = new ApiClient('http://custom-api', 'custom-key');
      expect(client).toBeDefined();
    });
  });

  describe('getSessionStatus', () => {
    it('should return session status', async () => {
      const status: SessionStatus = await apiClient.getSessionStatus();

      expect(status).toBeDefined();
      expect(status.sessionId).toBeDefined();
      expect(status.model).toBeDefined();
      expect(status.status).toBeDefined();
      expect(status.runtime).toBeDefined();
    });

    it('should have required fields in session status', async () => {
      const status: SessionStatus = await apiClient.getSessionStatus();

      expect(status.sessionId).toBeTypeOf('string');
      expect(status.createdAt).toBeTypeOf('string');
      expect(status.model).toBeTypeOf('string');
      expect(status.status).toBeOneOf(['running', 'idle', 'processing']);
      expect(status.runtime).toHaveProperty('host');
      expect(status.runtime).toHaveProperty('os');
      expect(status.runtime).toHaveProperty('nodeVersion');
    });
  });

  describe('getToolCalls', () => {
    it('should return array of tool calls', async () => {
      const toolCalls: ToolCall[] = await apiClient.getToolCalls();

      expect(Array.isArray(toolCalls)).toBe(true);
      expect(toolCalls.length).toBeGreaterThan(0);
    });

    it('should return tool calls with required fields', async () => {
      const toolCalls: ToolCall[] = await apiClient.getToolCalls();

      if (toolCalls.length > 0) {
        const toolCall = toolCalls[0];
        expect(toolCall.id).toBeDefined();
        expect(toolCall.timestamp).toBeDefined();
        expect(toolCall.tool).toBeDefined();
        expect(toolCall.status).toBeDefined();
        expect(toolCall.status).toBeOneOf(['running', 'success', 'error']);
      }
    });

    it('should include optional parameters field', async () => {
      const toolCalls: ToolCall[] = await apiClient.getToolCalls();

      if (toolCalls.length > 0) {
        const toolCall = toolCalls[0];
        if (toolCall.parameters) {
          expect(toolCall.parameters).toBeTypeOf('object');
        }
      }
    });
  });

  describe('getMessages', () => {
    it('should return array of messages', async () => {
      const messages: Message[] = await apiClient.getMessages();

      expect(Array.isArray(messages)).toBe(true);
      expect(messages.length).toBeGreaterThan(0);
    });

    it('should return messages with required fields', async () => {
      const messages: Message[] = await apiClient.getMessages();

      if (messages.length > 0) {
        const message = messages[0];
        expect(message.id).toBeDefined();
        expect(message.timestamp).toBeDefined();
        expect(message.role).toBeDefined();
        expect(message.role).toBeOneOf(['user', 'assistant']);
        expect(message.content).toBeDefined();
      }
    });

    it('should include optional reasoning field', async () => {
      const messages: Message[] = await apiClient.getMessages();

      if (messages.length > 0) {
        const message = messages[0];
        if (message.reasoning) {
          expect(message.reasoning).toBeTypeOf('string');
        }
      }
    });
  });

  describe('getTasks', () => {
    it('should return array of tasks', async () => {
      const tasks: Task[] = await apiClient.getTasks();

      expect(Array.isArray(tasks)).toBe(true);
      expect(tasks.length).toBeGreaterThan(0);
    });

    it('should return tasks with required fields', async () => {
      const tasks: Task[] = await apiClient.getTasks();

      if (tasks.length > 0) {
        const task = tasks[0];
        expect(task.id).toBeDefined();
        expect(task.description).toBeDefined();
        expect(task.status).toBeDefined();
        expect(task.status).toBeOneOf(['pending', 'in-progress', 'complete']);
      }
    });

    it('should include optional priority and completedAt fields', async () => {
      const tasks: Task[] = await apiClient.getTasks();

      if (tasks.length > 0) {
        const task = tasks[0];
        if (task.priority !== undefined) {
          expect(task.priority).toBeTypeOf('number');
        }
        if (task.completedAt) {
          expect(task.completedAt).toBeTypeOf('string');
        }
      }
    });
  });

  describe('data limits', () => {
    it('should not return more than 500 tool calls', async () => {
      // Mock data respects MAX_TOOL_CALLS limit
      const toolCalls: ToolCall[] = await apiClient.getToolCalls();
      expect(toolCalls.length).toBeLessThanOrEqual(500);
    });

    it('should not return more than 1000 messages', async () => {
      // Mock data respects MAX_MESSAGES limit
      const messages: Message[] = await apiClient.getMessages();
      expect(messages.length).toBeLessThanOrEqual(1000);
    });
  });
});
