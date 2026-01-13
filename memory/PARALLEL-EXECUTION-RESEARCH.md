# 🦞 Parallel Execution Tools & Approaches - Deep Research

**Researched:** 2026-01-13 21:10 UTC  
**Purpose:** Find tools for running commands in parallel (exec, curl, etc.)

---

## Executive Summary

Researched parallel execution tools for running commands concurrently. Found **3 categories**:

1. **Shell/CLI Tools** - Built-in and command-line parallel execution
2. **Python Libraries** - Programmatic parallel processing
3. **Node.js Tools** - npm script parallel execution

**Top Recommendations:**
- **GNU parallel** - Most powerful CLI parallel tool
- **xargs -P** - Built-in, always available
- **Python concurrent.futures** - Built-in, no install needed
- **Dask** - Advanced parallel computing for Python

---

## Category 1: Shell/CLI Tools (Built-in)

### 1.1 `xargs -P` (Built-in)

**Purpose:** Run commands in parallel using xargs
**Available:** ✅ Already installed
**Key Features:**
- Built into macOS/Linux
- Parallel execution with `-P` flag
- Works with any command
- Simple syntax

**Usage:**
```bash
# Run 4 curl commands in parallel
echo -e "url1\nurl2\nurl3\nurl4" | xargs -P 4 -I {} curl -s {}

# Download 4 files in parallel
cat urls.txt | xargs -P 4 wget -q

# Run 4 API calls in parallel
echo -e "api1\napi2\napi3\napi4" | xargs -P 4 -I {} curl -s "https://api.example.com/{}"

# Parallel make
make -j4

# Parallel find results processing
find . -name "*.txt" | xargs -P 4 -I {} grep "pattern" {}
```

**How It Helps Me:**
- ✅ Already installed
- ✅ Simple parallelization
- ✅ Works with any command
- ✅ Controllable parallelism (`-P N`)

---

### 1.2 Background Jobs (Built-in)

**Purpose:** Run commands in background with `&`
**Available:** ✅ Already available
**Key Features:**
- Simple background execution
- Wait for completion with `wait`
- Control with job IDs

**Usage:**
```bash
# Run 4 commands in background
curl -s "https://api1" & pid1=$!
curl -s "https://api2" & pid2=$!
curl -s "https://api3" & pid3=$!
curl -s "https://api4" & pid4=$!

# Wait for all to complete
wait $pid1 $pid2 $pid3 $pid4

# Or wait for all background jobs
wait

# Check if all succeeded
if wait; then echo "All succeeded"; fi
```

**Advanced Pattern:**
```bash
# Run in parallel and capture results
results=()
for i in {1..4}; do
    curl -s "https://api$i" > "result_$i.txt" &
    pids+=($!)
done

# Wait for all and check results
for pid in "${pids[@]}"; do
    if ! wait $pid; then
        echo "Process $pid failed"
    fi
done
```

**How It Helps Me:**
- ✅ Already available
- ✅ Full control over processes
- ✅ Capture results to files
- ✅ Check individual process status

---

### 1.3 `wait` for Synchronization

**Purpose:** Wait for background jobs to complete
**Available:** ✅ Already available
**Key Features:**
- Wait for specific PIDs
- Wait for all jobs
- Return exit codes

**Usage:**
```bash
# Start parallel jobs
cmd1 & pid1=$!
cmd2 & pid2=$!
cmd3 & pid3=$!
cmd4 & pid4=$!

# Wait and get exit codes
failed=0
for pid in $pid1 $pid2 $pid3 $pid4; do
    if ! wait $pid; then
        ((failed++))
    fi
done

echo "$failed jobs failed"
```

---

### 1.4 GNU Parallel (Recommended Install)

**Purpose:** Advanced parallel command execution
**Installation:** `brew install parallel` or `apt install parallel`
**Key Features:**
- Much more powerful than xargs
- Built-in progress bar
- Job scheduling
- SSH distribution
- CSV input support

**Usage:**
```bash
# Basic parallel execution
parallel curl -s {} ::: url1 url2 url3 url4

# Parallel with 4 jobs
parallel -j 4 curl -s {} ::: url1 url2 url3 url4

# From file input
parallel -j 4 curl -s {} < urls.txt

# With progress bar
parallel --progress curl -s {} ::: url1 url2 url3 url4

# Keep order with --keep-order
parallel --keep-order -j 4 curl -s {} ::: url1 url2 url3 url4

# Dry run first
parallel --dry-run curl -s {} ::: url1 url2 url3 url4

# With headers
parallel --header : curl -s {url} ::: url1 url2

# Parallel wget
parallel wget -q {} ::: file1 file2 file3

# Parallel grep
find . -name "*.txt" | parallel grep "pattern" {}

# Semaphore/lock support
parallel --semaphore -j 2 --id "lock" curl -s {}
```

**Advanced Examples:**
```bash
# Parallel API calls with rate limiting
parallel -j 5 --delay 0.2 curl -s {} ::: $(seq 1 100)

# Distribute across SSH hosts
parallel -S host1,host2 curl -s {} ::: urls

# Collect results
parallel --halt soon,fail=1 curl -s {} ::: urls
```

**How It Helps Me:**
- ✅ Much more powerful than xargs
- ✅ Progress visualization
- ✅ Order preservation
- ✅ SSH distribution
- ✅ Easy installation

---

### 1.5 Process Substitution

**Purpose:** Run commands on multiple inputs in parallel
**Available:** ✅ Built into bash
**Key Features:**
- Simple syntax
- No external tools needed
- Works with while/read loops

**Usage:**
```bash
# Process multiple files in parallel
while read url; do
    curl -s "$url" &
done < urls.txt
wait

# With named pipes
mkfifo pipe1 pipe2
cmd1 > pipe1 & pid1=$!
cmd2 > pipe2 & pid2=$!
cat pipe1 pipe2
wait $pid1 $pid2
```

---

## Category 2: Python Libraries (Programmatic)

### 2.1 `concurrent.futures` (Built-in)

**Purpose:** Parallel execution with ThreadPoolExecutor and ProcessPoolExecutor
**Available:** ✅ Built into Python 3.2+
**Key Features:**
- No install required
- Simple API
- Thread/process-based parallelism
- Futures for result handling

**Usage:**
```python
import concurrent.futures
import requests
import time

# ThreadPoolExecutor for I/O bound tasks (API calls, curl)
def fetch_url(url):
    response = requests.get(url)
    return response.text

urls = ["url1", "url2", "url3", "url4"]

# Run 4 parallel requests
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}
    results = {}
    for future in concurrent.futures.as_completed(futures):
        url = futures[future]
        try:
            results[url] = future.result()
        except Exception as e:
            results[url] = f"Error: {e}"

print(f"Completed {len(results)} requests")

# ProcessPoolExecutor for CPU-bound tasks
def cpu_task(n):
    return sum(i*i for i in range(n))

with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_task, [1000000, 2000000, 3000000, 4000000]))
```

**Advanced Pattern:**
```python
import concurrent.futures
import subprocess

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout

commands = ["curl -s url1", "curl -s url2", "curl -s url3", "curl -s url4"]

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(run_command, cmd) for cmd in commands]
    for future in concurrent.futures.as_completed(futures):
        returncode, output = future.result()
        if returncode == 0:
            print(f"Success: {output[:100]}")
        else:
            print(f"Failed")
```

**How It Helps Me:**
- ✅ Built-in (no install)
- ✅ Perfect for parallel curl/API calls
- ✅ Easy result handling
- ✅ Configurable parallelism

---

### 2.2 `multiprocessing` (Built-in)

**Purpose:** Process-based parallelism
**Available:** ✅ Built into Python
**Key Features:**
- Full process isolation
- CPU-bound tasks
- Queue-based communication

**Usage:**
```python
from multiprocessing import Pool, cpu_count

def task(arg):
    # Your task here
    return arg * 2

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        results = pool.map(task, [1, 2, 3, 4, 5])
    print(results)
```

---

### 2.3 `joblib` (Recommended Install)

**Purpose:** Computing with Python functions
**Installation:** `pip install joblib`
**Stars:** 4,304
**Key Features:**
- Simple parallel for loops
- Memory caching
- Easy serialization

**Usage:**
```python
from joblib import Parallel, delayed

def task(n):
    return n * n

# Run 4 parallel jobs
results = Parallel(n_jobs=4)(delayed(task)(i) for i in range(10))

# With backend selection
results = Parallel(n_jobs=4, backend="threading")(delayed(task)(i) for i in range(10))
```

**How It Helps Me:**
- ✅ Simple parallel loops
- ✅ Memory caching
- ✅ Easy to use

---

### 2.4 `Dask` (Advanced)

**Purpose:** Parallel computing with task scheduling
**Installation:** `pip install dask`
**Stars:** 13,709
**Key Features:**
- Larger-than-memory computations
- Task scheduling
- Distributed computing
- Integrates with pandas/numpy

**Usage:**
```python
import dask
import dask.bag as db

# Parallel operations on collections
data = ["url1", "url2", "url3", "url4"]

# Create a dask bag (parallel collection)
b = db.from_sequence(data, npartitions=4)

# Map function in parallel
results = b.map(lambda url: requests.get(url).text).compute()
```

**How It Helps Me:**
- ✅ Scalable to clusters
- ✅ Larger-than-memory
- ✅ Advanced scheduling

---

### 2.5 `Ray` (Advanced)

**Purpose:** Distributed computing for AI workloads
**Installation:** `pip install ray`
**Stars:** 40,748
**Key Features:**
- Distributed execution
- AI/ML optimized
- Actor model
- Task dependencies

**Usage:**
```python
import ray

ray.init()

@ray.remote
def fetch_url(url):
    return requests.get(url).text

# Launch 4 parallel tasks
results = ray.get([fetch_url.remote(url) for url in urls])
```

**How It Helps Me:**
- ✅ Very powerful
- ✅ Distributed by default
- ✅ Great for AI workloads
- ❌ Overkill for simple parallelization

---

### 2.6 `Celery` (Advanced)

**Purpose:** Distributed task queue
**Installation:** `pip install celery`
**Stars:** 27,866
**Key Features:**
- Task queues
- Distributed execution
- Result storage
- Scheduling

**Usage:**
```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost')

@app.task
def fetch_url(url):
    return requests.get(url).text

# Queue tasks
result = fetch_url.delay("https://api.example.com")
result.get()  # Get result
```

**How It Helps Me:**
- ✅ Production-grade
- ✅ Task queues
- ✅ Scheduling
- ❌ Requires message broker (Redis)

---

## Category 3: Node.js Tools

### 3.1 `concurrently` (NPM)

**Purpose:** Run commands concurrently
**Installation:** `npm install -g concurrently`
**Stars:** 7,615
**Key Features:**
- Simple parallel execution
- Cross-platform
- Prefix coloring
- Kill on failure

**Usage:**
```bash
# Run 3 commands in parallel
concurrently "npm run watch-js" "npm run watch-less" "npm run server"

# With success condition
concurrently "npm run test" "npm run build" --success=first

# Kill others on failure
concurrently "cmd1" "cmd2" --kill-others-on-fail

# With custom prefix
concurrently "cmd1" "cmd2" --prefix "[name]"
```

**How It Helps Me:**
- ✅ Great for npm scripts
- ✅ Visual feedback
- ✅ Easy error handling

---

### 3.2 `npm-run-all` (NPM)

**Purpose:** Run multiple npm-scripts in parallel or sequential
**Installation:** `npm install -g npm-run-all`
**Stars:** 5,841
**Key Features:**
- Parallel and sequential execution
- Pattern matching
- npm script integration

**Usage:**
```bash
# Run all in parallel
npm-run-all --parallel task1 task2 task3

# Run all sequentially
npm-run-all --sequential task1 task2 task3

# Pattern matching
npm-run-all --parallel watch:*
```

**How It Helps Me:**
- ✅ Great for npm scripts
- ✅ Pattern support
- ✅ Sequential option

---

## Comparison: Tools by Use Case

### Use Case 1: Parallel Curl/API Calls

| Tool | Installation | Ease | Best For |
|------|--------------|------|----------|
| **`xargs -P`** | Built-in | Easy | Simple parallelization |
| **GNU parallel** | Install | Medium | Advanced features |
| **Python concurrent.futures** | Built-in | Easy | Programmatic control |
| **Background + wait** | Built-in | Easy | Quick scripts |

**Recommendation:** Use `xargs -P` for simple cases, `concurrent.futures` for programmatic control.

---

### Use Case 2: Parallel File Processing

| Tool | Installation | Ease | Best For |
|------|--------------|------|----------|
| **GNU parallel** | Install | Medium | Complex workflows |
| **xargs -P** | Built-in | Easy | Simple processing |
| **Python multiprocessing** | Built-in | Medium | CPU-bound tasks |
| **find + xargs** | Built-in | Easy | File operations |

**Recommendation:** Use `find ... | xargs -P 4` for file processing.

---

### Use Case 3: Parallel Script Execution

| Tool | Installation | Ease | Best For |
|------|--------------|------|----------|
| **Background + wait** | Built-in | Easy | Bash scripts |
| **GNU parallel** | Install | Medium | Complex dependencies |
| **concurrently** | npm | Easy | npm scripts |

**Recommendation:** Use `cmd & pid=$!; wait $pid` for simple cases.

---

### Use Case 4: Batch Operations

| Tool | Installation | Ease | Best For |
|------|--------------|------|----------|
| **GNU parallel** | Install | Medium | Large batches |
| **Python concurrent.futures** | Built-in | Easy | Programmatic batches |
| **xargs -P** | Built-in | Easy | Simple batches |

**Recommendation:** Use `concurrent.futures` for Python scripts.

---

## Quick Reference

### Bash One-Liners

```bash
# Parallel curl (4 at a time)
cat urls.txt | xargs -P 4 curl -s -O

# Parallel wget
find . -name "*.zip" | xargs -P 4 wget -q

# Parallel grep
find . -name "*.txt" | xargs -P 4 grep "pattern"

# Parallel make
make -j4

# Parallel git operations
for repo in repo1 repo2 repo3; do
    git -C "$repo" pull &
done
wait

# Parallel file downloads
for url in $(cat urls.txt); do
    curl -s "$url" -o "$(basename $url)" &
done
wait

# With progress (requires pv)
cat urls.txt | xargs -P 4 -I {} sh -c 'curl -s {} | pv -qL 1000 > $(basename {})'
```

### Python One-Liners

```python
# Parallel curl with concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import subprocess

def run_cmd(cmd):
    subprocess.run(cmd, shell=True)

cmds = ["curl url1", "curl url2", "curl url3", "curl url4"]
with ThreadPoolExecutor(max_workers=4) as e:
    list(e.map(run_cmd, cmds))

# Parallel API calls
import concurrent.futures, requests

urls = ["url1", "url2", "url3", "url4"]
with ThreadPoolExecutor(max_workers=4) as e:
    results = list(e.map(lambda u: requests.get(u).text, urls))
```

### GNU Parallel Examples

```bash
# Basic
parallel curl -s {} ::: url1 url2 url3

# From file
parallel -j 4 curl -s {} < urls.txt

# With progress
parallel --progress curl -s {} ::: url1 url2

# Keep order
parallel --keep-order -j 4 curl -s {} ::: url1 url2

# Dry run
parallel --dry-run curl -s {} ::: url1 url2
```

---

## Implementation Plan for Clawdbot

### Phase 1: Use Built-in Tools (Today)

1. **Use `xargs -P` for parallel execution**
   ```bash
   cat urls.txt | xargs -P 4 curl -s
   ```

2. **Use background jobs for complex scripts**
   ```bash
   cmd1 & pid1=$!
   cmd2 & pid2=$!
   wait $pid1 $pid2
   ```

3. **Use `concurrent.futures` for programmatic control**
   ```python
   with ThreadPoolExecutor(max_workers=4) as e:
       results = list(e.map(task, items))
   ```

---

### Phase 2: Install GNU Parallel (This Week)

```bash
# Via Homebrew
brew install parallel

# Or via apt
sudo apt install parallel
```

**Add to AGENTS.md:**
```markdown
## Parallel Execution

### Bash (Built-in)
```bash
# Parallel curl (4 at a time)
cat urls.txt | xargs -P 4 curl -s

# Background jobs
cmd1 & pid1=$!
cmd2 & pid2=$!
wait $pid1 $pid2
```

### Python (Built-in)
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as e:
    results = list(e.map(task, items))
```
```

---

## Research Findings Summary

### Best Tools for My Use Case

| Use Case | Best Tool | Installation |
|----------|-----------|--------------|
| Parallel curl | `xargs -P` | Built-in |
| Parallel exec | `background + wait` | Built-in |
| Parallel API calls | `concurrent.futures` | Built-in |
| Complex workflows | `GNU parallel` | Install |
| npm scripts | `concurrently` | npm |

### Recommended Actions

1. **Today:** Use `xargs -P` and background jobs (already available)
2. **This week:** Install GNU parallel for advanced features
3. **Done:** Created `scripts/parallel-exec.py` wrapper script ✅

---

## 🆕 Custom Script Created

**File:** `scripts/parallel-exec.py`

A wrapper script using Python `concurrent.futures` for easy parallel execution:

```bash
# Parallel curl from file (4 workers)
python scripts/parallel-exec.py curl urls.txt -w 4

# Parallel command execution (4 workers)
python scripts/parallel-exec.py exec commands.txt -w 4

# Parallel API calls (8 workers)
python scripts/parallel-exec.py api endpoints.txt -w 8

# Parallel file downloads (4 workers)
python scripts/parallel-exec.py download urls.txt ./downloads -w 4

# Parallel git operations (4 workers)
python scripts/parallel-exec.py git repos.txt "pull" -w 4
```

**Features:**
- Built on `concurrent.futures.ThreadPoolExecutor` (no install needed)
- Configurable worker count (`-w N`)
- Progress output
- Error handling with failed item reporting
- Output directory support for curl/api results

---

## References

### Shell Tools
- GNU parallel - https://www.gnu.org/software/parallel/
- xargs man - https://man7.org/linux/man-pages/man1/xargs.1.html

### Python Libraries
- concurrent.futures - https://docs.python.org/3/library/concurrent.futures.html
- joblib - https://joblib.readthedocs.io/
- Dask - https://dask.org/
- Ray - https://ray.io/
- Celery - https://docs.celeryq.dev/

### Node.js Tools
- concurrently - https://github.com/open-cli-tools/concurrently
- npm-run-all - https://github.com/mysticatea/npm-run-all

---

*This document is indexed by qmd for semantic search.*

🦞
