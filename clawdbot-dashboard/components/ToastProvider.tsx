'use client';

import * as React from 'react';
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface ToastProps {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
  onClose?: () => void;
}

interface ToastContextType {
  toasts: ToastProps[];
  addToast: (toast: Omit<ToastProps, 'id'>) => string;
  removeToast: (id: string) => void;
  clearAll: () => void;
}

const ToastContext = React.createContext<ToastContextType | undefined>(undefined);

export function useToast() {
  const context = React.useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}

interface ToastProviderProps {
  children: React.ReactNode;
}

let toastIdCounter = 0;

export function ToastProvider({ children }: ToastProviderProps) {
  const [toasts, setToasts] = React.useState<ToastProps[]>([]);

  const addToast = React.useCallback(
    (toast: Omit<ToastProps, 'id'>) => {
      const id = `toast-${toastIdCounter++}`;
      const newToast: ToastProps = {
        ...toast,
        id,
        duration: toast.duration || 3000,
      };

      setToasts((prev) => [...prev, newToast]);

      if (newToast.duration && newToast.duration > 0) {
        setTimeout(() => {
          setToasts((prev) => prev.filter((t) => t.id !== id));
        }, newToast.duration);
      }

      return id;
    },
    []
  );

  const removeToast = React.useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const clearAll = React.useCallback(() => {
    setToasts([]);
  }, []);

  const value: ToastContextType = React.useMemo(
    () => ({
      toasts,
      addToast,
      removeToast,
      clearAll,
    }),
    [toasts, addToast, removeToast, clearAll]
  );

  return (
    <ToastContext.Provider value={value}>
      {children}
      {toasts.length > 0 && <ToastContainer toasts={toasts} onRemove={removeToast} />}
    </ToastContext.Provider>
  );
}

interface ToastContainerProps {
  toasts: ToastProps[];
  onRemove: (id: string) => void;
}

function ToastContainer({ toasts, onRemove }: ToastContainerProps) {
  return (
    <div className="fixed top-0 right-0 z-[100] flex flex-col gap-2 p-4 w-full max-w-md pointer-events-none">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} onRemove={onRemove} />
      ))}
    </div>
  );
}

interface ToastItemProps {
  toast: ToastProps;
  onRemove: (id: string) => void;
}

function ToastItem({ toast, onRemove }: ToastItemProps) {
  const [isVisible, setIsVisible] = React.useState(false);

  React.useEffect(() => {
    setIsVisible(true);
  }, []);

  const getIcon = () => {
    switch (toast.type) {
      case 'success':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'error':
        return <XCircle className="h-5 w-5 text-red-500" />;
      case 'warning':
        return <AlertCircle className="h-5 w-5 text-yellow-500" />;
      case 'info':
        return <Info className="h-5 w-5 text-blue-500" />;
      default:
        return <Info className="h-5 w-5 text-blue-500" />;
    }
  };

  const getColors = () => {
    switch (toast.type) {
      case 'success':
        return 'bg-green-50 border-green-200 text-green-900 dark:bg-green-900/20 dark:border-green-800 dark:text-green-100';
      case 'error':
        return 'bg-red-50 border-red-200 text-red-900 dark:bg-red-900/20 dark:border-red-800 dark:text-red-100';
      case 'warning':
        return 'bg-yellow-50 border-yellow-200 text-yellow-900 dark:bg-yellow-900/20 dark:border-yellow-800 dark:text-yellow-100';
      case 'info':
        return 'bg-blue-50 border-blue-200 text-blue-900 dark:bg-blue-900/20 dark:border-blue-800 dark:text-blue-100';
      default:
        return 'bg-blue-50 border-blue-200 text-blue-900 dark:bg-blue-900/20 dark:border-blue-800 dark:text-blue-100';
    }
  };

  return (
    <div
      className={cn(
        'pointer-events-auto w-full rounded-lg border shadow-lg transition-all duration-300',
        getColors(),
        isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-full'
      )}
      role="alert"
      aria-live="polite"
    >
      <div className="flex items-start gap-3 p-4">
        <div className="flex-shrink-0 mt-0.5">
          {getIcon()}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold">{toast.title}</p>
          {toast.message && (
            <p className="mt-1 text-sm opacity-90 line-clamp-2">
              {toast.message}
            </p>
          )}
        </div>
        <button
          onClick={() => onRemove(toast.id)}
          className="h-6 w-6 flex-shrink-0 opacity-70 hover:opacity-100 rounded-full p-1 hover:bg-black/5 dark:hover:bg-white/5"
          aria-label="Close notification"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}

export function useSuccessToast() {
  const toast = useToast();
  return React.useCallback(
    (title: string, message?: string, duration?: number) => {
      return toast.addToast({ type: 'success', title, message, duration });
    },
    [toast]
  );
}

export function useErrorToast() {
  const toast = useToast();
  return React.useCallback(
    (title: string, message?: string, duration?: number) => {
      return toast.addToast({ type: 'error', title, message, duration });
    },
    [toast]
  );
}

export function useWarningToast() {
  const toast = useToast();
  return React.useCallback(
    (title: string, message?: string, duration?: number) => {
      return toast.addToast({ type: 'warning', title, message, duration });
    },
    [toast]
  );
}

export function useInfoToast() {
  const toast = useToast();
  return React.useCallback(
    (title: string, message?: string, duration?: number) => {
      return toast.addToast({ type: 'info', title, message, duration });
    },
    [toast]
  );
}
