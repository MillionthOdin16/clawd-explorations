'use client';

import { useState } from 'react';
import { CheckCircle2, Clock, Circle, ListTodo } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import type { TaskTrackerProps, TaskStatus, Task } from '@/lib/types';

interface TaskItemProps {
  task: Task;
}

function TaskItem({ task }: TaskItemProps) {
  const getStatusIcon = (status: TaskStatus) => {
    switch (status) {
      case 'complete':
        return <CheckCircle2 className="h-5 w-5 text-green-500" />;
      case 'in-progress':
        return <Clock className="h-5 w-5 text-blue-500 animate-pulse" />;
      case 'pending':
        return <Circle className="h-5 w-5 text-gray-400" />;
      default:
        return <Circle className="h-5 w-5" />;
    }
  };

  const getStatusColor = (status: TaskStatus) => {
    switch (status) {
      case 'complete':
        return 'bg-green-500/10 text-green-500 border-green-500/20';
      case 'in-progress':
        return 'bg-blue-500/10 text-blue-500 border-blue-500/20';
      case 'pending':
        return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
      default:
        return '';
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="border-b last:border-b-0">
      <div className="flex items-start gap-3 p-4 hover:bg-muted/50">
        {getStatusIcon(task.status)}
        <div className="flex-1 space-y-2">
          <p className="font-medium">{task.description}</p>
          <div className="flex items-center gap-2">
            <Badge
              variant="outline"
              className={getStatusColor(task.status)}
            >
              {task.status}
            </Badge>
            {task.priority && (
              <Badge variant="secondary">Priority: {task.priority}</Badge>
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
              <div className="flex h-[300px] items-center justify-center text-muted-foreground">
                No tasks found
              </div>
            ) : (
              filteredTasks.map((task) => (
                <TaskItem key={task.id} task={task} />
              ))
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
