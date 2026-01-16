import { describe, it, expect } from 'vitest';
import { debounce, throttle } from '@/lib/utils/debounce';

describe('debounce', () => {
  it('should create a debounced function', () => {
    const fn = vi.fn();
    const debouncedFn = debounce(fn, 100);

    expect(typeof debouncedFn).toBe('function');
  });

  it('should delay function execution', async () => {
    const fn = vi.fn();
    const debouncedFn = debounce(fn, 100);

    debouncedFn();

    // Function should not be called immediately
    expect(fn).not.toHaveBeenCalled();

    // Wait for debounce delay
    await new Promise((resolve) => setTimeout(resolve, 150));

    // Function should be called after delay
    expect(fn).toHaveBeenCalledTimes(1);
  });

  it('should cancel previous calls when called rapidly', async () => {
    const fn = vi.fn();
    const debouncedFn = debounce(fn, 100);

    // Call rapidly
    debouncedFn();
    debouncedFn();
    debouncedFn();
    debouncedFn();

    // Wait for debounce delay
    await new Promise((resolve) => setTimeout(resolve, 150));

    // Function should only be called once
    expect(fn).toHaveBeenCalledTimes(1);
  });
});

describe('throttle', () => {
  it('should create a throttled function', () => {
    const fn = vi.fn();
    const throttledFn = throttle(fn, 100);

    expect(typeof throttledFn).toBe('function');
  });

  it('should limit function execution rate', async () => {
    const fn = vi.fn();
    const throttledFn = throttle(fn, 100);

    // Call rapidly
    throttledFn();
    throttledFn();
    throttledFn();

    // Function should only be called once immediately
    expect(fn).toHaveBeenCalledTimes(1);

    // Wait for throttle period
    await new Promise((resolve) => setTimeout(resolve, 150));

    // Should be able to call again
    throttledFn();
    expect(fn).toHaveBeenCalledTimes(2);
  });

  it('should ignore calls within throttle period', async () => {
    const fn = vi.fn();
    const throttledFn = throttle(fn, 100);

    // Call initially
    throttledFn();

    expect(fn).toHaveBeenCalledTimes(1);

    // Call within throttle period
    await new Promise((resolve) => setTimeout(resolve, 50));
    throttledFn();

    // Should still be 1 call (second call ignored)
    expect(fn).toHaveBeenCalledTimes(1);

    // Wait for throttle period to end
    await new Promise((resolve) => setTimeout(resolve, 150));

    // Third call should execute
    throttledFn();
    expect(fn).toHaveBeenCalledTimes(2);
  });
});
