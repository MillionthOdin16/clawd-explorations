'use client';

import { useState } from 'react';
import { ListTodo } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { EmptyState } from '@/components/ui/EmptyState';
import type { TaskTrackerProps, TaskStatus, Task } from '@/lib/types';

interface TaskItemProps {
  task: Task;
}

function TaskItem({ task }: TaskItemProps) {
  const formatDate = (dateString?: string) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="border-b last:border-b-0">
      <div className="flex items-start gap-3 p-4 hover:bg-muted/50">
        <StatusBadge status={task.status} />
        <div className="flex-1 space-y-2">
          <p className="font-medium">{task.description}</p>
          <div className="flex items-center gap-2">
            {task.priority && (
              <span className="text-xs text-muted-foreground">
                Priority: {task.priority}
              </span>
            )}
          </div>
          {task.completedAt && (
            <p className="text-xs text-muted-foreground">
              Completed: {formatDate(task.completedAt)}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default function TaskTracker({
  tasks,
  statusFilter = 'all',
}: TaskTrackerProps) {
  const [selectedStatus, setSelectedStatus] = useState<TaskStatus | 'all'>(
    statusFilter
  );

  const filteredTasks = tasks.filter((task) => {
    return selectedStatus === 'all' || task.status === selectedStatus;
  });

  const statusCounts = {
    all: tasks.length,
    pending: tasks.filter((t) => t.status === 'pending').length,
    'in-progress': tasks.filter((t) => t.status === 'in-progress').length,
    complete: tasks.filter((t) => t.status === 'complete').length,
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ListTodo className="h-5 w-5" />
            <span>Task Tracker</span>
          </div>
          <Badge variant="secondary">{filteredTasks.length} tasks</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Status Filters */}
        <div className="flex gap-2">
          {(['all', 'pending', 'in-progress', 'complete'] as const).map(
            (status) => (
              <Button
                key={status}
                variant={selectedStatus === status ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedStatus(status)}
                className="capitalize"
              >
                {status} ({statusCounts[status]})
              </Button>
            )
          )}
        </div>

        {/* Task List */}
        <ScrollArea className="h-[400px]">
          <div>
            {filteredTasks.length === 0 ? (
              <EmptyState
                icon={<ListTodo className="h-12 w-12" />}
                title="No tasks found"
                description="Tasks will appear here as Clawdbot processes work"
              />
            ) : (
              filteredTasks.map((task) => <TaskItem key={task.id} task={task} />)
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
