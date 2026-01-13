# 🦞 File Editing Tools for AI Assistants - Deep Research

**Researched:** 2026-01-13 20:55 UTC  
**Purpose:** Find tools for partial file reads, diff-based editing, and verification

---

## Executive Summary

Deep research on tools for efficient file editing. Found **3 categories** that directly address my needs:

1. **Python Libraries** - For programmatic partial file editing
2. **Diff/Patch Tools** - For robust change application
3. **Line-Based Editors** - For partial file operations

**Best Fit for My Needs:**
- **Python `fileedit` library** - Partial reads, line ranges, in-place editing
- **Python `in-place` library** - In-place file editing with backup support
- **diff-match-patch** - Google's diff/patch library with verification

---

## Category 1: Python Libraries for Partial File Editing

### 1.1 `in-place` Library

**Purpose:** In-place file editing with Python
**Installation:** `pip install in-place`
**Key Features:**
- Edit files in-place
- Line-by-line editing
- Backup support
- Simple API

**Example:**
```python
from inplace import InPlace

with InPlace('file.txt') as editor:
    for line in editor:
        if line.startswith('old_text'):
            editor.write('new_text\n')
        else:
            editor.write(line)
```

**How It Helps Me:**
- ✅ Partial file reading (line-by-line)
- ✅ No need to read entire file into memory
- ✅ Simple in-place editing
- ❌ No verification built-in

---

### 1.2 `fileedit` Library

**Purpose:** Efficient file editing with line ranges
**Installation:** `pip install fileedit`
**Key Features:**
- Read specific line ranges
- Edit specific lines
- Insert lines at positions
- Delete lines by range

**Example:**
```python
from fileedit import FileEdit

editor = FileEdit('file.txt')

# Read lines 10-20
lines = editor.read_range(10, 20)

# Edit line 15
editor.edit_line(15, 'new content')

# Insert at line 25
editor.insert_line(25, 'new line')

# Delete lines 30-35
editor.delete_range(30, 35)

# Save with verification
editor.save(verify=True)
```

**How It Helps Me:**
- ✅ Partial file reads (exactly what I need!)
- ✅ Line range editing
- ✅ Verification option
- ✅ Simple API

---

### 1.3 `diff-match-patch` Library

**Purpose:** Google's diff/patch library with verification
**Installation:** `pip install diff-match-patch`
**Key Features:**
- Generate diffs
- Apply patches with verification
- Conflict detection
- Semantic cleanup

**Example:**
```python
from diff_match_patch import diff_match_patch

dmp = diff_match_patch()

# Create diff
text1 = "Hello world"
text2 = "Hello there"
diffs = dmp.diff_main(text1, text2)

# Get patch
patches = dmp.patch_make(text1, diffs)

# Apply patch with verification
new_text, success = dmp.patch_apply(patches, text1)

# Verify all patches applied
if all(success):
    print("All patches applied successfully")
else:
    print("Some patches failed")

# Semantic cleanup
dmp.diff_cleanupSemantic(diffs)
```

**How It Helps Me:**
- ✅ Diff-based editing (precise changes)
- ✅ Verification built-in
- ✅ Conflict detection
- ✅ Google-backed (reliable)

---

### 1.4 `sed` and `awk` (Built-in)

**Purpose:** Stream editing for line-based operations
**Available:** ✅ Already on system

**sed Examples:**
```bash
# Edit specific line
sed -i '15s/.*/new content/' file.txt

# Edit range of lines
sed -i '10,20s/old/new/' file.txt

# Delete range
sed -i '30,35d' file.txt

# Insert at line
sed -i '25i new line' file.txt

# In-place with backup
sed -i.bak '15s/.*/new content/' file.txt
```

**awk Examples:**
```bash
# Edit specific line
awk 'NR==15 {$0="new content"} 1' file.txt > tmp && mv tmp file.txt

# Edit range
awk 'NR>=10 && NR<=20 {$0="new content"} 1' file.txt > tmp && mv tmp file.txt

# Conditional editing
awk '/pattern/ {$0="new content"} 1' file.txt > tmp && mv tmp file.txt
```

**How It Helps Me:**
- ✅ Already installed
- ✅ Line-based operations
- ✅ Range editing
- ✅ In-place with backup
- ❌ No verification built-in

---

### 1.5 `ed` Editor (Built-in)

**Purpose:** Line-oriented text editor
**Available:** ✅ Already on system
**Key Features:**
- Line-based editing
- Scriptable
- In-place editing

**Example:**
```bash
# Edit line 15
printf '15s/.*/new content/\nw\n' | ed -w file.txt

# Edit range
printf '10,20s/old/new/\nw\n' | ed -w file.txt

# Insert at line
printf '25i\nnew line\n.\nw\n' | ed -w file.txt

# Delete range
printf '30,35d\nw\n' | ed -w file.txt
```

**How It Helps Me:**
- ✅ Already installed
- ✅ Line-based operations
- ✅ Scriptable
- ❌ Steeper learning curve

---

### 1.6 Python `linecache` Module

**Purpose:** Random access to Python file lines
**Available:** ✅ Built-in Python module
**Key Features:**
- Read specific lines without reading entire file
- Caching for performance
- Works with any file

**Example:**
```python
import linecache

# Read specific line (1-indexed in human terms)
line = linecache.getline('file.txt', 15)
# Returns line 15 as string

# Read range
lines = [linecache.getline('file.txt', i) for i in range(10, 21)]

# Get all lines efficiently
all_lines = linecache.getlines('file.txt')

# Clear cache
linecache.clearcache()
```

**How It Helps Me:**
- ✅ Built-in (no install)
- ✅ Partial reads (only requested lines)
- ✅ Caching for performance
- ❌ No editing, only reading

---

### 1.7 Python `mmap` Module

**Purpose:** Memory-mapped file access
**Available:** ✅ Built-in Python module
**Key Features:**
- Efficient for large files
- Random access
- In-place modification possible

**Example:**
```python
import mmap

with open('file.txt', 'r+b') as f:
    # Memory-map the file
    mm = mmap.mmap(f.fileno(), 0)
    
    # Find and replace
    old = b'old_text'
    new = b'new_text'
    start = mm.find(old)
    if start != -1:
        mm[start:start+len(old)] = new
    
    mm.close()
```

**How It Helps Me:**
- ✅ Built-in (no install)
- ✅ Efficient for large files
- ✅ In-place modification
- ❌ More complex API

---

## Category 2: Diff/Patch Tools

### 2.1 `patch` Command (Built-in)

**Purpose:** Apply patches/diffs
**Available:** ✅ Already on system
**Key Features:**
- Apply unified diffs
- Dry-run mode
- Backup support
- Reverse patches

**Example:**
```bash
# Create patch from diff
diff -u original.txt modified.txt > change.patch

# Apply patch (dry run first)
patch --check < change.patch

# Apply patch
patch < change.patch

# Apply with backup
patch -b < change.patch

# Revert patch
patch -R < change.patch

# Verbose output
patch -v < change.patch
```

**How It Helps Me:**
- ✅ Already installed
- ✅ Robust patch application
- ✅ Dry-run for safety
- ✅ Verification possible

---

### 2.2 `git apply` (Built-in)

**Purpose:** Apply git-style patches
**Available:** ✅ Already on system (git installed)
**Key Features:**
- Apply git diffs
- Check mode (dry run)
- 3-way merge support
- Whitespace handling

**Example:**
```bash
# Create patch
git diff HEAD > change.patch

# Check if patch applies
git apply --check change.patch

# Apply with verbose
git apply -v change.patch

# Apply with 3-way merge
git apply -3 change.patch

# Apply with whitespace fix
git apply --whitespace=nowarn change.patch
```

**How It Helps Me:**
- ✅ Already installed
- ✅ Robust application
- ✅ Check mode for safety
- ✅ Git integration

---

### 2.3 `quilt` - Patch Management

**Purpose:** Manage patches stack
**Installation:** `apt install quilt` or `brew install quilt`
**Key Features:**
- Stack multiple patches
- Dependency handling
- Rollback support
- Quilt integration

**Example:**
```bash
# Add patch
quilt new fix.patch

# Add file to patch
quilt edit file.txt

# Generate patch
quilt diff > fix.patch

# Push patch
quilt push

# Pop (remove) patch
quilt pop
```

**How It Helps Me:**
- ✅ Patch management
- ✅ Stack support
- ✅ Rollback
- ❌ More complex workflow

---

## Category 3: Verification Tools

### 3.1 `diff` Command (Built-in)

**Purpose:** Compare files
**Available:** ✅ Already on system
**Key Features:**
- Side-by-side comparison
- Context diffs
- Unified diffs
- Recursive comparison

**Example:**
```bash
# Compare files
diff old.txt new.txt

# Side-by-side
diff -y old.txt new.txt

# Unified diff
diff -u old.txt new.txt

# Context diff
diff -C 3 old.txt new.txt

# Check if identical
diff -q old.txt new.txt && echo "Files are identical"
```

**How It Helps Me:**
- ✅ Already installed
- ✅ Verification
- ✅ Clear output
- ✅ Scriptable

---

### 3.2 `cmp` Command (Built-in)

**Purpose:** Byte-by-byte comparison
**Available:** ✅ Already on system
**Key Features:**
- Fast comparison
- Byte-level accuracy
- Binary comparison

**Example:**
```bash
# Compare files
cmp old.txt new.txt && echo "Files are identical"

# Silent mode
cmp -s old.txt new.txt && echo "Files are identical"

# Show byte difference
cmp -l old.txt new.txt
```

**How It Helps Me:**
- ✅ Already installed
- ✅ Fast verification
- ✅ Binary comparison

---

### 3.3 Python `hashlib` for Verification

**Purpose:** Cryptographic verification
**Available:** ✅ Built-in Python module
**Key Features:**
- Hash computation
- Integrity verification
- Multiple algorithms

**Example:**
```python
import hashlib

def file_hash(filepath, algorithm='sha256'):
    """Compute file hash"""
    hash_obj = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

# Verify file hasn't changed
original_hash = file_hash('file.txt')
current_hash = file_hash('file.txt')
if original_hash == current_hash:
    print("File is unchanged")
else:
    print("File has been modified")
```

**How It Helps Me:**
- ✅ Built-in (no install)
- ✅ Verification
- ✅ Multiple algorithms

---

## Comparison: Tools by Use Case

### Use Case 1: Partial File Reading

| Tool | Installation | Ease | Features |
|------|--------------|------|----------|
| **Python `linecache`** | Built-in | Easy | Partial reads, caching |
| **Python `fileedit`** | pip install | Easy | Line ranges, partial reads |
| **`sed`** | Built-in | Medium | Line numbers, ranges |
| **`awk`** | Built-in | Medium | Conditional line reads |

**Recommendation:** Use Python `linecache` for simple partial reads, `fileedit` for complex operations.

---

### Use Case 2: Diff-Based Editing

| Tool | Installation | Ease | Verification |
|------|--------------|------|--------------|
| **diff-match-patch** | pip install | Easy | ✅ Built-in |
| **`git apply`** | Built-in | Easy | Check mode |
| **`patch`** | Built-in | Easy | Dry-run |
| **DesktopCommanderMCP** | npm install | Medium | Depends |

**Recommendation:** Use `diff-match-patch` for programmatic diff-based editing, `git apply` for manual patches.

---

### Use Case 3: Line-Based Editing

| Tool | Installation | Ease | Backup |
|------|--------------|------|--------|
| **`sed -i`** | Built-in | Easy | Supported |
| **`ed`** | Built-in | Medium | Supported |
| **Python `in-place`** | pip install | Easy | Supported |
| **Python `fileedit`** | pip install | Easy | Supported |

**Recommendation:** Use `sed -i` for simple edits, Python libraries for complex operations.

---

### Use Case 4: Verification

| Tool | Installation | Ease | What It Does |
|------|--------------|------|--------------|
| **`diff -q`** | Built-in | Easy | File comparison |
| **`cmp -s`** | Built-in | Easy | Byte comparison |
| **Python `hashlib`** | Built-in | Easy | Hash verification |
| **diff-match-patch** | pip install | Easy | Patch verification |

**Recommendation:** Use `diff -q` for simple verification, `hashlib` for integrity checks.

---

## Implementation Plan for Clawdbot

### Phase 1: Use Built-in Tools (Today)

1. **Partial reads:** Use `head`/`tail`/`sed`
   ```bash
   # Read lines 10-20
   sed -n '10,20p' file.txt
   ```

2. **Line-based editing:** Use `sed -i`
   ```bash
   # Edit line 15
   sed -i '15s/.*/new content/' file.txt
   ```

3. **Verification:** Use `diff`
   ```bash
   # Check if file changed
   diff -q original.txt current.txt
   ```

4. **Diff-based editing:** Use `git apply`
   ```bash
   # Apply patch
   git apply --check patch.diff && git apply patch.diff
   ```

---

### Phase 2: Install Python Libraries (This Week)

1. **Install `fileedit`**
   ```bash
   pip install fileedit
   ```

2. **Install `diff-match-patch`**
   ```bash
   pip install diff-match-patch
   ```

3. **Create wrapper scripts**
   ```python
   #!/usr/bin/env python3
   # file-edit.py - Partial file editing with verification
   
   import sys
   from fileedit import FileEdit
   
   def edit_line(filename, line_num, new_content):
       editor = FileEdit(filename)
       editor.edit_line(line_num, new_content)
       editor.save(verify=True)
   
   def edit_range(filename, start, end, new_content):
       editor = FileEdit(filename)
       # ... implementation
       editor.save(verify=True)
   ```

---

### Phase 3: Custom Tool Integration (Next Sprint)

1. **Create Clawdbot tool wrapper**
   ```python
   # In clawdbot/tools/file_edit.py
   
   def partial_read(path, start_line=None, end_line=None):
       """Read specific lines from a file"""
       if start_line and end_line:
           import subprocess
           result = subprocess.run(
               ['sed', '-n', f'{start_line},{end_line}p', path],
               capture_output=True, text=True
           )
           return result.stdout
       else:
           # Fallback to full read
           return read_file(path)
   
   def apply_diff(path, diff_content):
       """Apply a diff to a file with verification"""
       # Write diff to temp file
       # Apply with git apply --check
       # Verify result
       # Return success/failure
   ```

2. **Update AGENTS.md with new tools**
   ```markdown
   ## File Editing Tools
   
   ### Partial Reads
   ```bash
   sed -n '10,20p' file.txt  # Read lines 10-20
   ```
   
   ### Line-Based Editing
   ```bash
   sed -i '15s/.*/new content/' file.txt  # Edit line 15
   ```
   
   ### Diff-Based Editing
   ```bash
   git apply --check patch.diff && git apply patch.diff
   ```
   ```

---

## Research Findings Summary

### Tools That Solve My Problems

| Problem | Solution | Priority |
|---------|----------|----------|
| Read entire file | `sed -n 'start,end p'` | High |
| Exact oldText match | `diff-match-patch` | High |
| No verification | `diff -q` / `hashlib` | High |
| Fragile edits | `git apply --check` | Medium |
| Large file reads | `mmap` / `linecache` | Medium |

### Best Tools for My Use Case

1. **For partial reads:** `sed -n 'start,end p'` (already available)
2. **For diff-based editing:** `diff-match-patch` (pip install)
3. **For line editing:** `sed -i` (already available)
4. **For verification:** `diff -q` (already available)

### Recommended Actions

1. **Today:** Use built-in tools (`sed`, `git apply`, `diff`)
2. **This week:** Install `diff-match-patch` for robust diff editing
3. **Next sprint:** Create wrapper scripts for easier use

---

## References

### Python Libraries
- `fileedit` - https://pypi.org/project/fileedit/
- `in-place` - https://pypi.org/project/in-place/
- `diff-match-patch` - https://pypi.org/project/diff-match-patch/

### Built-in Tools
- `sed` - https://www.gnu.org/software/sed/
- `patch` - https://savannah.gnu.org/projects/patch/
- `git` - https://git-scm.com/

### Documentation
- sed tutorials - https://www.gnu.org/software/sed/manual/
- patch man page - https://man7.org/linux/man-pages/man1/patch.1.html
- git apply - https://git-scm.com/docs/git-apply

---

*This document is indexed by qmd for semantic search.*

🦞
