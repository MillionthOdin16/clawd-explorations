#!/usr/bin/env python3
"""
LittleClawd Memory Optimization Script
Run this on LittleClawd to free memory and clean up
"""
import subprocess
import os

def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {e}"

def check_memory():
    """Show current memory usage"""
    print("🦞 LittleClawd Memory Optimization")
    print("=" * 50)
    print("\n1. Current Memory Status:")
    print("-" * 50)
    print(run_command("free -h"))

def clear_caches():
    """Clear system caches"""
    print("\n2. Clearing System Caches:")
    print("-" * 50)

    # Clear page cache, dentries, and inodes
    print("Clearing page cache, dentries, and inodes...")
    result = run_command("sudo sync && sudo sysctl vm.drop_caches=1 2>&1 || echo 'Requires sudo access'")
    print(result)

    # Clear yum/dnf cache
    print("\nClearing DNF cache...")
    result = run_command("sudo dnf clean all 2>&1 | tail -5")
    print(result)

def clear_logs():
    """Clear log files"""
    print("\n3. Cleaning Log Files:")
    print("-" * 50)

    # Clear journal logs (keep last 2 days)
    print("Rotating journal logs (keeping last 2 days)...")
    result = run_command("sudo journalctl --vacuum-time=2d 2>&1 | tail -5")
    print(result)

    # Compress old logs
    print("\nCompressing old logs in /var/log...")
    result = run_command("sudo find /var/log -name '*.log' -mtime +7 -type f -exec gzip {} \\; 2>&1 | head -10")
    print(result)

def clear_temp():
    """Clear temporary files"""
    print("\n4. Cleaning Temporary Files:")
    print("-" * 50)

    # Clear /tmp
    print("Cleaning /tmp directory...")
    result = run_command("sudo rm -rf /tmp/* 2>&1")
    print(result)

    # Clear user temp
    print("Cleaning user temporary files...")
    result = run_command("rm -rf ~/.cache/* 2>&1")
    print(result)

def check_processes():
    """Check top memory consumers"""
    print("\n5. Top Memory Consumers:")
    print("-" * 50)
    result = run_command("ps aux --sort=-%mem | head -15")
    print(result)

def main():
    """Run optimization"""
    try:
        check_memory()
        clear_caches()
        clear_logs()
        clear_temp()
        check_processes()

        print("\n6. Memory After Optimization:")
        print("-" * 50)
        print(run_command("free -h"))

        print("\n✅ Optimization Complete!")
        print("\nNote: Rebooting would free more memory, but requires manual action.")
        print("Run 'sudo reboot' if memory is still insufficient.")

    except Exception as e:
        print(f"\n❌ Error during optimization: {e}")

if __name__ == "__main__":
    main()
