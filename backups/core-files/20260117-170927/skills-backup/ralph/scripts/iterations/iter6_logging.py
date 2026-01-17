#!/usr/bin/env python3
"""
Ralph Logging Configuration
Provides logging to file with rotation.
"""

import os
import sys
import logging
import logging.handlers
from pathlib import Path

# Default paths
LOGS_DIR = Path("/home/opc/clawd/skills/ralph/logs")
RALPH_LOG = LOGS_DIR / "ralph.log"


def setup_logging(name="ralph", level=logging.INFO):
    """Set up logging with file rotation."""
    # Create logs directory
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # File handler with rotation (10MB max, 5 backup files)
    file_handler = logging.handlers.RotatingFileHandler(
        RALPH_LOG, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name="ralph"):
    """Get or create logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logging(name)
    return logger


# Example usage:
# from logging_config import get_logger
# logger = get_logger("spec-executor")
# logger.info("Task started")
# logger.error("Task failed", exc_info=True)
