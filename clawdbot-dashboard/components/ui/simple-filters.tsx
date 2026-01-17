'use client';

import * as React from 'react';
import { X } from 'lucide-react';

export type FilterOption<T extends string> = {
  label: string;
  value: T;
  count?: number;
};

interface SimpleFilterProps<T extends string> {
  options: FilterOption<T>[];
  selected: T[];
  onChange: (selected: T[]) => void;
  label?: string;
  placeholder?: string;
  multiSelect?: boolean;
}

export function SimpleFilter<T extends string>({
  options,
  selected,
  onChange,
  label = 'Filters',
  placeholder = 'Select filters...',
  multiSelect = true,
}: SimpleFilterProps<T>) {
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
          <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full">
            {selectedCount} selected
          </span>
        )}
      </div>

      {isOpen && (
        <div className="relative inline-block">
          <div className="absolute z-50 mt-2 w-56 rounded-md border bg-background shadow-lg max-h-96 overflow-y-auto">
            <div className="p-2 space-y-1">
              <div className="mb-2 flex items-center justify-between border-b pb-2">
                <span className="text-sm font-semibold">
                  {selectedCount} {selectedCount === 1 ? 'option' : 'options'} selected
                </span>
                {selectedCount > 0 && (
                  <button
                    onClick={clearAll}
                    className="text-xs hover:underline text-muted-foreground"
                  >
                    Clear all
                  </button>
                )}
              </div>

              {options.map((option) => {
                const isSelected = selected.includes(option.value);
                return (
                  <div
                    key={option.value as string}
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
                      <span
                        className={`h-5 text-xs ${
                          isSelected
                            ? 'border-primary-foreground/50 text-primary-foreground'
                            : ''
                        }`}
                      >
                        {option.count}
                      </span>
                    )}
                    {isSelected && <X className="h-3 w-3 ml-2" />}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="w-full flex items-center justify-between rounded-md border px-3 py-2 text-sm transition-colors hover:bg-muted"
        >
          <span>{placeholder}</span>
          {selectedCount > 0 && (
            <span className="text-muted-foreground">({selectedCount})</span>
          )}
          <svg className="h-4 w-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      )}

      {isOpen && (
        <button
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 z-40 bg-black/20"
          aria-label="Close dropdown"
        />
      )}
    </div>
  );
}

interface DateRangeFilterSimpleProps {
  value?: { from?: Date; to?: Date };
  onChange: (range?: { from?: Date; to?: Date }) => void;
  label?: string;
}

export function DateRangeFilterSimple({
  value,
  onChange,
  label = 'Date Range',
}: DateRangeFilterSimpleProps) {
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

      {isOpen && (
        <div className="relative inline-block">
          <div className="absolute z-50 mt-2 w-80 rounded-md border bg-background shadow-lg">
            <div className="p-4 space-y-4">
              <div className="mb-3 flex items-center justify-between border-b pb-2">
                <span className="text-sm font-semibold">
                  {isActive ? formatDate(value.from) + ' - ' + formatDate(value.to) : 'Select date range'}
                </span>
                {isActive && (
                  <button
                    onClick={clearDateRange}
                    className="text-xs hover:underline text-muted-foreground"
                  >
                    Clear
                  </button>
                )}
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium block">
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
                <label className="text-sm font-medium block">
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
                <button
                  onClick={clearDateRange}
                  className="w-full mt-2"
                >
                  Clear date range
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="w-full flex items-center justify-between rounded-md border px-3 py-2 text-sm transition-colors hover:bg-muted"
        >
          <span>
            {isActive
              ? formatDate(value.from) + ' - ' + formatDate(value.to)
              : 'Select date range'}
          </span>
          <svg className="h-4 w-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      )}

      {isOpen && (
        <button
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 z-40 bg-black/20"
          aria-label="Close dropdown"
        />
      )}
    </div>
  );
}
