"""
ACDSYN Structured Logging System
Provides robust, configurable logging for ecosystem tracking
"""
import sys
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
import structlog

from config import LogLevel, get_config

class LogContext(str, Enum):
    """Logging contexts for different system components"""
    SYNTHESIS = "synthesis"
    COMMUNICATION = "communication"
    FEEDBACK = "feedback"
    DOMAIN = "domain"
    SYSTEM = "system"
    ERROR = "error"

class ACDSYNLogger:
    """Centralized logging system with structured logging"""
    
    def __init__(self):
        self.config = get_config()
        self._configure_logging()
        
    def _configure_logging(self):
        """Configure structured logging based on config"""
        timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
        pre_chain = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            timestamper,
        ]
        
        # Configure based on format
        if self.config.log_format == "json":
            renderer = structlog.processors.JSONRenderer()
        else:
            renderer = structlog.dev.ConsoleRenderer()
            
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                *pre