#!/usr/bin/env python3
"""
File Editing - Optimized for Clawdbot usage

Usage:
    fe read <path> [--start N] [--end N]
    fe line <path> <n> <content>
    fe text <path> <old> <new> [--fuzzy]
    fe range <path> <start> <end> <new>
    fe verify <p1> <p2>
    fe hash <path>

Examples:
    fe read path.md --start 10 --end 20
    fe line path.md 15 "new content"
    fe text path.md "old" "new" --fuzzy
    fe verify a.txt b.txt
"""

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

def cmd(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Error: {r.stderr}", file=sys.stderr)
        sys.exit(1)
    return r.stdout

def fe_read(path, start=None, end=None):
    if start and end:
        out = cmd(f"sed -n '{start},{end}p' '{path}'")
    elif start:
        out = cmd(f"sed -n '{start},$p' '{path}'")
    elif end:
        out = cmd(f"sed -n '1,{end}p' '{path}'")
    else:
        out = cmd(f"cat '{path}'")
    print(out, end='')

def fe_line(path, n, content):
    esc = content.replace("'", "'\\''")
    cmd(f"sed -i '{n}s/.*/{esc}/' '{path}'")
    print(f"Line {n} updated")

def fe_text(path, old, new, fuzzy=False):
    c = Path(path).read_text()
    if old in c:
        Path(path).write_text(c.replace(old, new))
        print("Done")
        return
    if fuzzy:
        ol = [l.strip() for l in old.strip().split('\n') if l.strip()]
        cl = c.split('\n')
        for i in range(len(cl)):
            tm = '\n'.join(cl[i:i+len(ol)])
            if old.strip() in tm or tm.strip() in old.strip():
                Path(path).write_text(c.replace(tm, new))
                print(f"Done (fuzzy match)")
                return
        print("Not found", file=sys.stderr)
    else:
        print("Not found", file=sys.stderr)
    sys.exit(1)

def fe_range(path, start, end, new):
    cmd(f"sed -i '{start},{end}d' '{path}'")
    esc = new.replace("'", "'\\''")
    cmd(f"sed -i '{start}i\\{esc}' '{path}'")
    print(f"Lines {start}-{end} replaced")

def fe_verify(p1, p2):
    r = cmd(f"diff -q '{p1}' '{p2}'")
    if r.returncode == 0:
        print("Identical")
    else:
        print("Different", file=sys.stderr)
        sys.exit(1)

def fe_hash(path):
    h = hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]
    print(h)

def main():
    p = argparse.ArgumentParser(prog='fe', description='File editing optimized for Clawdbot')
    sp = p.add_subparsers(dest='cmd', help='Commands')
    
    # read
    rp = sp.add_parser('read', help='Read file')
    rp.add_argument('path')
    rp.add_argument('--start', type=int)
    rp.add_argument('--end', type=int)
    
    # line
    lp = sp.add_parser('line', help='Edit line')
    lp.add_argument('path')
    lp.add_argument('n', type=int)
    lp.add_argument('content')
    
    # text
    tp = sp.add_parser('text', help='Edit text')
    tp.add_argument('path')
    tp.add_argument('old')
    tp.add_argument('new')
    tp.add_argument('--fuzzy', action='store_true')
    
    # range
    rp = sp.add_parser('range', help='Edit range')
    rp.add_argument('path')
    rp.add_argument('start', type=int)
    rp.add_argument('end', type=int)
    rp.add_argument('new')
    
    # verify
    vp = sp.add_parser('verify', help='Verify files')
    vp.add_argument('p1')
    vp.add_argument('p2')
    
    # hash
    hp = sp.add_parser('hash', help='Hash file')
    hp.add_argument('path')
    
    a = p.parse_args()
    
    if a.cmd == 'read':
        fe_read(a.path, a.start, a.end)
    elif a.cmd == 'line':
        fe_line(a.path, a.n, a.content)
    elif a.cmd == 'text':
        fe_text(a.path, a.old, a.new, a.fuzzy)
    elif a.cmd == 'range':
        fe_range(a.path, a.start, a.end, a.new)
    elif a.cmd == 'verify':
        fe_verify(a.p1, a.p2)
    elif a.cmd == 'hash':
        fe_hash(a.path)
    else:
        p.print_help()

if __name__ == '__main__':
    main()
