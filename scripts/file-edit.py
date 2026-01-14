#!/usr/bin/env python3
"""
File Editing Utilities for Clawdbot

Provides partial reads, line-based editing, text-based editing, and verification.
Uses built-in tools (sed, diff, hashlib) where possible.

Usage:
    python file-edit.py read <path> [--start N] [--end N]
    python file-edit.py edit-line <path> <line> <content>
    python file-edit.py edit-range <path> <start> <end> <new_content>
    python file-edit.py edit-text <path> <old_text> <new_text> [--fuzzy]
    python file-edit.py verify <path1> <path2>
    python file-edit.py hash <path>
    python file-edit.py diff-text <old> <new>

Requirements:
    - Python 3.9+
    - Git (for diff verification)
    - sed (for line editing)
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result


def read_partial(path, start=None, end=None):
    """Read specific lines from a file using sed."""
    if start and end:
        cmd = f"sed -n '{start},{end}p' '{path}'"
    elif start:
        cmd = f"sed -n '{start},$p' '{path}'"
    elif end:
        cmd = f"sed -n '1,{end}p' '{path}'"
    else:
        cmd = f"cat '{path}'"
    
    result = run_command(cmd)
    return result.stdout


def edit_line(path, line_num, new_content):
    """Edit a specific line in a file using sed."""
    backup_path = f"{path}.backup.{os.getpid()}"
    run_command(f"cp '{path}' '{backup_path}'")
    
    try:
        escaped_content = new_content.replace("'", "'\\''")
        cmd = f"sed -i '{line_num}s/.*/{escaped_content}/' '{path}'"
        run_command(cmd)
        
        result = run_command(f"sed -n '{line_num}p' '{path}'")
        if new_content.strip() in result.stdout.strip():
            return True
        else:
            run_command(f"mv '{backup_path}' '{path}'")
            return False
    except Exception:
        run_command(f"mv '{backup_path}' '{path}'")
        raise
    finally:
        if os.path.exists(backup_path):
            os.remove(backup_path)


def edit_range(path, start_line, end_line, new_content):
    """Replace a range of lines with new content."""
    backup_path = f"{path}.backup.{os.getpid()}"
    run_command(f"cp '{path}' '{backup_path}'")
    
    try:
        run_command(f"sed -i '{start_line},{end_line}d' '{path}'")
        escaped_content = new_content.replace("'", "'\\''")
        run_command(f"sed -i '{start_line}i\\{escaped_content}' '{path}'")
        return True
    except Exception as e:
        run_command(f"mv '{backup_path}' '{path}'")
        raise
    finally:
        if os.path.exists(backup_path):
            os.remove(backup_path)


def edit_text(path, old_text, new_text, fuzzy=False):
    """
    Edit text content (not line-based) with optional fuzzy matching.
    
    Args:
        path: File path
        old_text: Text to find
        new_text: Text to replace with
        fuzzy: Use fuzzy matching for whitespace variations
    
    Returns:
        tuple: (success: bool, message: str)
    """
    content = Path(path).read_text()
    
    if old_text in content:
        new_content = content.replace(old_text, new_text)
        Path(path).write_text(new_content)
        return True, "Exact match edit successful"
    
    if fuzzy:
        # Try fuzzy matching - strip and normalize
        old_lines = [l.strip() for l in old_text.strip().split('\n') if l.strip()]
        content_lines = content.split('\n')
        
        for i, line in enumerate(content_lines):
            if all(ol in line for ol in old_lines if len(ol) > 5):
                for j in range(len(content_lines)):
                    test_match = '\n'.join(content_lines[j:j+len(old_lines)])
                    if old_text.strip() in test_match or test_match.strip() in old_text.strip():
                        new_content = content.replace(test_match, new_text)
                        Path(path).write_text(new_content)
                        return True, f"Fuzzy match edit successful at line {j+1}"
        
        return False, "No fuzzy match found"
    
    return False, "Text not found (try --fuzzy)"


def create_diff(old_text, new_text):
    """Create a unified diff between two text strings."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(old_text)
        old_path = f.name
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(new_text)
            new_path = f.name
        
        try:
            result = subprocess.run(
                f"diff -u '{old_path}' '{new_path}'",
                shell=True, capture_output=True, text=True
            )
            return result.stdout
        finally:
            os.remove(new_path)
    finally:
        os.remove(old_path)


def verify_files(path1, path2):
    """Verify two files are identical."""
    result = run_command(f"diff -q '{path1}' '{path2}'", check=False)
    
    if result.returncode == 0:
        return True, "Files are identical"
    else:
        diff_result = run_command(f"diff -u '{path1}' '{path2}'")
        return False, f"Files differ:\n{diff_result.stdout}"


def file_hash(path, algorithm='sha256'):
    """Compute cryptographic hash of a file."""
    hash_obj = hashlib.new(algorithm)
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description='File editing utilities for Clawdbot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Read lines 10-20 from a file
  file-edit.py read /path/to/file.txt --start 10 --end 20
  
  # Edit line 15 (PREFERRED when you know the line)
  file-edit.py edit-line /path/to/file.txt 15 "new content"
  
  # Edit text content (when you know the text, not the line)
  file-edit.py edit-text /path/to/file.txt "old text" "new text"
  
  # Fuzzy edit (handles whitespace variations)
  file-edit.py edit-text /path/to/file.txt "old text" "new text" --fuzzy
  
  # Verify files are identical
  file-edit.py verify /path/to/file1.txt /path/to/file2.txt
  
  # Compute file hash
  file-edit.py hash /path/to/file.txt
        """
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read partial file content')
    read_parser.add_argument('path', help='File path')
    read_parser.add_argument('--start', type=int, help='Start line (1-indexed)')
    read_parser.add_argument('--end', type=int, help='End line (1-indexed)')
    
    # Edit-line command
    edit_parser = subparsers.add_parser('edit-line', help='Edit a specific line')
    edit_parser.add_argument('path', help='File path')
    edit_parser.add_argument('line', type=int, help='Line number (1-indexed)')
    edit_parser.add_argument('content', help='New content for the line')
    
    # Edit-text command (NEW - replaces safe-edit.py)
    text_parser = subparsers.add_parser('edit-text', help='Edit text content with optional fuzzy matching')
    text_parser.add_argument('path', help='File path')
    text_parser.add_argument('old', help='Text to find')
    text_parser.add_argument('new', help='Text to replace with')
    text_parser.add_argument('--fuzzy', action='store_true', help='Use fuzzy matching')
    
    # Edit-range command
    range_parser = subparsers.add_parser('edit-range', help='Replace a range of lines')
    range_parser.add_argument('path', help='File path')
    range_parser.add_argument('start', type=int, help='Start line (1-indexed)')
    range_parser.add_argument('end', type=int, help='End line (1-indexed)')
    range_parser.add_argument('content', help='New content to replace the range')
    
    # Diff-text command
    diff_parser = subparsers.add_parser('diff-text', help='Create diff between two texts')
    diff_parser.add_argument('old', help='Original text')
    diff_parser.add_argument('new', help='New text')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify files are identical')
    verify_parser.add_argument('path1', help='First file path')
    verify_parser.add_argument('path2', help='Second file path')
    
    # Hash command
    hash_parser = subparsers.add_parser('hash', help='Compute file hash')
    hash_parser.add_argument('path', help='File path')
    hash_parser.add_argument('--algorithm', default='sha256', help='Hash algorithm')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'read':
            content = read_partial(args.path, args.start, args.end)
            print(content, end='')
        
        elif args.command == 'edit-line':
            success = edit_line(args.path, args.line, args.content)
            if success:
                print(f"Line {args.line} updated successfully")
            else:
                print(f"Failed to update line {args.line}")
                sys.exit(1)
        
        elif args.command == 'edit-text':
            success, message = edit_text(args.path, args.old, args.new, getattr(args, 'fuzzy', False))
            print(message)
            if not success:
                sys.exit(1)
        
        elif args.command == 'edit-range':
            success = edit_range(args.path, args.start, args.end, args.content)
            if success:
                print(f"Lines {args.start}-{args.end} replaced successfully")
            else:
                print(f"Failed to replace lines {args.start}-{args.end}")
                sys.exit(1)
        
        elif args.command == 'diff-text':
            diff = create_diff(args.old, args.new)
            print(diff)
        
        elif args.command == 'verify':
            identical, message = verify_files(args.path1, args.path2)
            print(message)
            if not identical:
                sys.exit(1)
        
        elif args.command == 'hash':
            hash_value = file_hash(args.path, args.algorithm)
            print(hash_value)
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
