"""Logging configuration for HealthPipe."""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (usually __name__)
        level: Optional logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level or logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        logger.setLevel(level or logging.INFO)
    
    return logger