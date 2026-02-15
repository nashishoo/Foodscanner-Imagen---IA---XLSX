"""
Food Scanner - Logger Module
Robust logging configuration with file rotation
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

import config


def setup_logger(name: str = "foodscanner", verbose: bool = False) -> logging.Logger:
    """
    Setup and configure a logger with console and file handlers.
    
    Args:
        name: Logger name
        verbose: If True, set log level to DEBUG
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Set level
    level = logging.DEBUG if verbose else getattr(logging, config.LOG_LEVEL)
    logger.setLevel(level)
    
    # Simple ASCII-only formatters for Windows compatibility
    console_formatter = logging.Formatter(
        "%(levelname)s - %(message)s"
    )
    
    file_formatter = logging.Formatter(
        config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    
    # Console handler with UTF-8 encoding
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    try:
        console_handler.stream.reconfigure(encoding='utf-8')
    except:
        pass
    logger.addHandler(console_handler)
    
    # File handler with rotation
    log_file = config.LOGS_DIR / "foodscanner.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (uses module name if not provided)
        
    Returns:
        Logger instance
    """
    if name is None:
        name = __name__
    return logging.getLogger(name)
