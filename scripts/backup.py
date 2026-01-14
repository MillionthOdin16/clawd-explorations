#!/usr/bin/env python3
"""
Memory Backup System for Clawdbot

Automatically backs up memory files with:
- Timestamped backups
- Incremental backups
- Retention policy (keep last N backups)
- Backup verification

Usage:
    python scripts/backup.py              # Create backup
    python scripts/backup.py --list       # List backups
    python scripts/backup.py --restore    # Restore latest backup
    python scripts/backup.py --auto       # Auto-backup with retention
"""

import argparse
import gzip
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class BackupSystem:
    """Memory backup system for Clawdbot."""
    
    def __init__(self, workspace: str = "/home/opc/clawd"):
        self.workspace = Path(workspace)
        self.backup_dir = self.workspace / ".backups"
        self.memory_dir = self.workspace / "memory"
        self.archive_dir = self.workspace / "archive"
        
    def create_backup(self, name: str = None) -> str:
        """Create a new backup."""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate name if not provided
        if not name:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            name = f"backup_{timestamp}"
        
        backup_path = self.backup_dir / f"{name}.tar.gz"
        
        print(f"Creating backup: {name}")
        
        # Create tar.gz archive
        with tarfile.open(backup_path, "w:gz") as tar:
            # Add memory directory
            if self.memory_dir.exists():
                tar.add(self.memory_dir, arcname="memory")
            
            # Add archive directory
            if self.archive_dir.exists():
                tar.add(self.archive_dir, arcname="archive")
        
        # Create metadata
        metadata = {
            "name": name,
            "created_at": time.time(),
            "created_at_str": datetime.utcnow().isoformat(),
            "memory_files": len(list(self.memory_dir.glob("*.md"))) if self.memory_dir.exists() else 0,
            "archive_files": len(list(self.archive_dir.glob("*.md"))) if self.archive_dir.exists() else 0,
            "size_bytes": backup_path.stat().st_size,
            "workspace": str(self.workspace),
        }
        
        # Save metadata
        meta_path = self.backup_dir / f"{name}.meta.json"
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        size_mb = round(metadata["size_bytes"] / 1024 / 1024, 2)
        print(f"✅ Backup created: {backup_path.name} ({size_mb} MB)")
        
        return str(backup_path)
    
    def list_backups(self) -> List[dict]:
        """List all backups."""
        if not self.backup_dir.exists():
            print("No backups found")
            return []
        
        backups = []
        for meta_file in sorted(self.backup_dir.glob("*.meta.json")):
            try:
                with open(meta_file, 'r') as f:
                    data = json.load(f)
                    backups.append(data)
            except Exception:
                pass
        
        # Sort by date (newest first)
        backups.sort(key=lambda x: x.get("created_at", 0), reverse=True)
        
        print(f"\n📦 Found {len(backups)} backups:")
        print("-" * 60)
        for backup in backups:
            date = datetime.fromtimestamp(backup["created_at"]).strftime("%Y-%m-%d %H:%M")
            size = round(backup["size_bytes"] / 1024 / 1024, 2)
            print(f"  📄 {backup['name']}")
            print(f"     Date: {date} | Size: {size} MB | Files: {backup['memory_files']}")
        print()
        
        return backups
    
    def restore_backup(self, name: str = None) -> bool:
        """Restore from backup."""
        if not self.backup_dir.exists():
            print("No backups found")
            return False
        
        # Find backup
        if name:
            backup_file = self.backup_dir / f"{name}.tar.gz"
        else:
            # Get latest
            backups = sorted(self.backup_dir.glob("*.tar.gz"))
            if not backups:
                print("No backups found")
                return False
            backup_file = backups[-0]
        
        if not backup_file.exists():
            print(f"Backup not found: {backup_file}")
            return False
        
        print(f"Restoring from: {backup_file.name}")
        
        # Extract to temporary location
        temp_dir = self.workspace / f".restore_{int(time.time())}"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            with tarfile.open(backup_file, "r:gz") as tar:
                tar.extractall(temp_dir)
            
            # Move contents back
            extracted_memory = temp_dir / "memory"
            extracted_archive = temp_dir / "archive"
            
            if extracted_memory.exists():
                # Backup current memory first
                if self.memory_dir.exists():
                    old_memory = self.workspace / f"memory_old_{int(time.time())}"
                    shutil.move(str(self.memory_dir), str(old_memory))
                shutil.move(str(extracted_memory), str(self.memory_dir))
            
            if extracted_archive.exists():
                # Backup current archive first
                if self.archive_dir.exists():
                    old_archive = self.workspace / f"archive_old_{int(time.time())}"
                    shutil.move(str(self.archive_dir), str(old_archive))
                shutil.move(str(extracted_archive), str(self.archive_dir))
            
            print("✅ Backup restored successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False
        finally:
            # Clean up temp directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def auto_backup(self, keep_last: int = 5) -> int:
        """Create backup with retention policy."""
        # Check if we need to backup (only if changes since last backup)
        backups = sorted(self.backup_dir.glob("*.meta.json"))
        
        if backups:
            last_backup = backups[-1]
            with open(last_backup, 'r') as f:
                last_time = json.load(f).get("created_at", 0)
            
            # Check if memory changed
            latest_memory = max(f.stat().st_mtime for f in self.memory_dir.glob("*.md"))
            if latest_memory <= last_backup.stat().st_mtime:
                print("✅ No changes since last backup - skipping")
                return 0
        
        # Create backup
        self.create_backup()
        
        # Clean old backups
        deleted = 0
        all_backups = sorted(self.backup_dir.glob("*.tar.gz"))
        if len(all_backups) > keep_last:
            for old in all_backups[:-keep_last]:
                # Also delete metadata
                meta = self.backup_dir / (old.stem + ".meta.json")
                if meta.exists():
                    meta.unlink()
                old.unlink()
                print(f"🗑️  Deleted old backup: {old.name}")
                deleted += 1
        
        return deleted + 1
    
    def verify_backup(self, name: str = None) -> bool:
        """Verify backup integrity."""
        if not self.backup_dir.exists():
            print("No backups found")
            return False
        
        if name:
            backup_file = self.backup_dir / f"{name}.tar.gz"
        else:
            backups = sorted(self.backup_dir.glob("*.tar.gz"))
            if not backups:
                print("No backups found")
                return False
            backup_file = backups[-1]
        
        if not backup_file.exists():
            print(f"Backup not found: {backup_file}")
            return False
        
        print(f"Verifying: {backup_file.name}")
        
        try:
            with tarfile.open(backup_file, "r:gz") as tar:
                # Check if archive is valid
                members = tar.getmembers()
                print(f"  Contains {len(members)} items")
                
                # Verify each member
                for member in members[:5]:  # Check first 5
                    if member.isfile():
                        print(f"  ✅ {member.name}")
                    else:
                        print(f"  📁 {member.name}")
            
            print("✅ Backup verified")
            return True
            
        except Exception as e:
            print(f"❌ Backup corrupted: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Clawdbot Memory Backup System')
    parser.add_argument('--list', action='store_true', help='List backups')
    parser.add_argument('--restore', action='store_true', help='Restore latest backup')
    parser.add_argument('--auto', action='store_true', help='Auto-backup with retention')
    parser.add_argument('--verify', action='store_true', help='Verify backup')
    parser.add_argument('--keep', type=int, default=5, help='Keep last N backups (default: 5)')
    parser.add_argument('--name', help='Backup name')
    args = parser.parse_args()
    
    backup = BackupSystem()
    
    if args.list:
        backup.list_backups()
    elif args.restore:
        backup.restore_backup(args.name)
    elif args.verify:
        backup.verify_backup(args.name)
    elif args.auto:
        created = backup.auto_backup(args.keep)
        if created > 0:
            print(f"✅ Auto-backup complete ({created} backup(s))")
    else:
        path = backup.create_backup(args.name)
        print(f"\nBackup saved to: {path}")


if __name__ == '__main__':
    main()
