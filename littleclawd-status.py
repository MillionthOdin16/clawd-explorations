#!/usr/bin/env python3
"""LittleClawd status script"""
import time
import os
import sys

print("LittleClawd is alive! 🦞")
print(f"Current time: {time.ctime()}")
print(f"Working directory: {os.getcwd()}")
print(f"Python version: {sys.version.split()[0]}")
print("I'm ready to help!")
