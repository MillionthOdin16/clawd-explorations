'use client';

import { useState, useEffect } from 'react';
import { Activity, Wifi, WifiOff, Moon, Sun } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTheme } from 'next-themes';
import { apiClient } from '@/lib';

/**
 * Connection status indicator
 */
function ConnectionStatus({ isConnected }: { isConnected: boolean }) {
  return (
    <div className="flex items-center gap-2 text-sm">
      {isConnected ? (
        <>
          <Wifi className="h-4 w-4 text-green-500" />
          <span className="text-green-500">Connected</span>
        </>
      ) : (
        <>
          <WifiOff className="h-4 w-4 text-red-500" />
          <span className="text-red-500">Disconnected</span>
        </>
      )}
    </div>
  );
}

/**
 * Header with theme toggle and connection status
 */
function DashboardHeader({
  isConnected,
  onToggleTheme,
  theme,
}: {
  isConnected: boolean;
  onToggleTheme: () => void;
  theme: string | undefined;
}) {
  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Activity className="h-5 w-5" />
          <h1 className="text-lg font-semibold">Clawdbot Dashboard</h1>
        </div>
        <div className="flex items-center gap-4">
          <ConnectionStatus isConnected={isConnected} />
          <Button variant="ghost" size="icon" onClick={onToggleTheme}>
            {theme === 'dark' ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            )}
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>
      </div>
    </header>
  );
}

interface DashboardLayoutProps {
  children: React.ReactNode;
}

/**
 * Main dashboard layout with theme support
 */
export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const { theme, setTheme } = useTheme();
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Simulate connection check
    const checkConnection = async () => {
      try {
        await apiClient.getSessionStatus();
        setIsConnected(true);
      } catch {
        setIsConnected(false);
      }
    };

    checkConnection();
    const interval = setInterval(checkConnection, 5000);

    return () => clearInterval(interval);
  }, []);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader
        isConnected={isConnected}
        onToggleTheme={toggleTheme}
        theme={theme}
      />
      <main className="container mx-auto p-4">{children}</main>
    </div>
  );
}
