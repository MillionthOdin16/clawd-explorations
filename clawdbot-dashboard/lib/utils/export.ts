import type { SessionStatus, ToolCall, Message, Task } from '../types';

/**
 * Data export utilities
 */

/**
 * Export data to JSON file
 */
export function exportToJSON<T>(data: T[], filename: string): void {
  const json = JSON.stringify(data, null, 2);
  downloadJSON(json, filename);
}

/**
 * Export data to CSV file
 */
export function exportToCSV(data: Record<string, unknown>[], filename: string): void {
  if (data.length === 0) return;

  const headers = Object.keys(data[0]);
  const csv = [
    headers.join(','),
    ...data.map((row) =>
      headers.map((header) => {
        const value = row[header];
        // Escape values with commas
        if (typeof value === 'string' && (value.includes(',') || value.includes('\n'))) {
          return `"${value.replace(/"/g, '""')}"`;
        }
        return value ?? '';
      }).join(','),
    ),
  ].join('\n');

  downloadCSV(csv, filename);
}

/**
 * Download JSON file
 */
function downloadJSON(json: string, filename: string): void {
  const blob = new Blob([json], { type: 'application/json' });
  downloadBlob(blob, filename);
}

/**
 * Download CSV file
 */
function downloadCSV(csv: string, filename: string): void {
  const blob = new Blob([csv], { type: 'text/csv' });
  downloadBlob(blob, filename);
}

/**
 * Generic download helper
 */
function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

/**
 * Export all session data
 */
export function exportSessionData(data: {
  sessionStatus?: SessionStatus;
  toolCalls: ToolCall[];
  messages: Message[];
  tasks: Task[];
}): void {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  
  // Export individual files
  if (data.toolCalls.length > 0) {
    exportToJSON(data.toolCalls, `tool-calls-${timestamp}.json`);
  }
  
  if (data.messages.length > 0) {
    exportToJSON(data.messages, `messages-${timestamp}.json`);
  }
  
  if (data.tasks.length > 0) {
    exportToJSON(data.tasks, `tasks-${timestamp}.json`);
  }
  
  // Export complete session
  if (data.sessionStatus) {
    const completeSession = {
      sessionStatus: data.sessionStatus,
      toolCalls: data.toolCalls,
      messages: data.messages,
      tasks: data.tasks,
      exportedAt: new Date().toISOString(),
    };
    // Export complete session as a single object
    const json = JSON.stringify(completeSession, null, 2);
    downloadJSON(json, `complete-session-${timestamp}.json`);
  }
}
