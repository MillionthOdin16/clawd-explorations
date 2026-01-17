'use client';

import * as React from 'react';
import { X, ChevronDown } from 'lucide-react';
import { Button } from './button';
import { Badge } from './badge';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from './popover';

export type FilterOption<T extends string> = {
  label: string;
  value: T;
  count?: number;
};

interface EnhancedFiltersProps<T extends string> {
  options: FilterOption<T>[];
  selected: T[];
  onChange: (selected: T[]) => void;
  label?: string;
  placeholder?: string;
  multiSelect?: boolean;
}

export function EnhancedFilters<T extends string>({
  options,
  selected,
  onChange,
  label = 'Filters',
  placeholder = 'Select filters...',
  multiSelect = true,
}: EnhancedFiltersProps<T>) {
  const [isOpen, setIsOpen] = React.useState(false);

  const toggleOption = (value: T) => {
    if (multiSelect) {
      if (selected.includes(value)) {
        onChange(selected.filter((v) => v !== value));
      } else {
        onChange([...selected, value]);
      }
    } else {
      onChange([value]);
      setIsOpen(false);
    }
  };

  const clearAll = () => {
    onChange([]);
  };

  const selectedCount = selected.length;

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium">{label}</span>
        {selectedCount > 0 && (
          <Badge variant="secondary">
            {selectedCount} {selectedCount === 1 ? 'selected' : 'selected'}
          </Badge>
        )}
      </div>

      <Popover open={isOpen} onOpenChange={setIsOpen}>
        <PopoverTrigger asChild>
          <Button variant="outline" className="w-full justify-between">
            {placeholder}
            {selectedCount > 0 && (
              <span className="text-muted-foreground">({selectedCount})</span>
            )}
            <ChevronDown className="h-4 w-4 ml-2" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-56 p-0" align="start">
          <div className="p-4">
            <div className="mb-3 flex items-center justify-between">
              <span className="text-sm font-semibold">
                {selectedCount} {selectedCount === 1 ? 'option' : 'options'} selected
              </span>
              {selectedCount > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearAll}
                  className="h-7 text-xs"
                >
                  Clear all
                </Button>
              )}
            </div>

            <div className="max-h-96 overflow-y-auto">
              <div className="space-y-1">
                {options.map((option) => {
                  const isSelected = selected.includes(option.value);
                  return (
                    <div
                      key={option.value}
                      onClick={() => toggleOption(option.value)}
                      className={`
                        relative flex items-center justify-between rounded-md px-3 py-2 text-sm
                        cursor-pointer transition-colors
                        ${
                          isSelected
                            ? 'bg-primary text-primary-foreground'
                            : 'hover:bg-muted'
                        }
                      `}
                    >
                      <span className="flex-1">{option.label}</span>
                      {option.count !== undefined && (
                        <Badge
                          variant="outline"
                          className={`h-5 text-xs ${
                            isSelected
                              ? 'border-primary-foreground/50 text-primary-foreground'
                              : ''
                          }`}
                        >
                          {option.count}
                        </Badge>
                      )}
                      {isSelected && (
                        <X className="h-3 w-3 ml-2" />
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </PopoverContent>
      </Popover>
    </div>
  );
}

interface DateRangeFilterProps {
  value?: { from?: Date; to?: Date };
  onChange: (range?: { from?: Date; to?: Date }) => void;
  label?: string;
}

export function DateRangeFilter({
  value,
  onChange,
  label = 'Date Range',
}: DateRangeFilterProps) {
  const [isOpen, setIsOpen] = React.useState(false);

  const handleFromDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const from = e.target.value ? new Date(e.target.value) : undefined;
    onChange({ from, to: value?.to });
  };

  const handleToDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const to = e.target.value ? new Date(e.target.value) : undefined;
    onChange({ from: value?.from, to });
  };

  const clearDateRange = () => {
    onChange(undefined);
  };

  const formatDate = (date?: Date) => {
    if (!date) return '';
    return date.toISOString().split('T')[0];
  };

  const isActive = value && (value.from || value.to);

  return (
    <div className="space-y-2">
      <span className="text-sm font-medium">{label}</span>
      <Popover open={isOpen} onOpenChange={setIsOpen}>
        <PopoverTrigger asChild>
          <Button variant="outline" className="w-full justify-between">
            {isActive
              ? `${formatDate(value.from)} - ${formatDate(value.to)}`
              : 'Select date range'}
            <ChevronDown className="h-4 w-4 ml-2" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-80 p-4" align="start">
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">
                From
              </label>
              <input
                type="date"
                value={formatDate(value?.from)}
                onChange={handleFromDateChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">
                To
              </label>
              <input
                type="date"
                value={formatDate(value?.to)}
                onChange={handleToDateChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>
            {isActive && (
              <Button
                variant="outline"
                size="sm"
                onClick={clearDateRange}
                className="w-full"
              >
                Clear date range
              </Button>
            )}
          </div>
        </PopoverContent>
      </Popover>
    </div>
  );
}
