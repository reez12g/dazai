"""
Custom exceptions for the Dazai application.

This module defines custom exception classes that can be used
throughout the application for more specific error handling.
"""
from typing import Any, Dict, Optional


class DazaiError(Exception):
    """Base exception class for all Dazai application errors."""
    
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        """
        Initialize the exception.
        
        Args:
            message: The error message
            status_code: The HTTP status code to return
            details: Additional details about the error
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ConfigurationError(DazaiError):
    """Exception raised for errors in the application configuration."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Initialize with a 500 status code."""
        super().__init__(message, 500, details)


class TaskError(DazaiError):
    """Exception raised for errors in task creation or execution."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Initialize with a 500 status code."""
        super().__init__(message, 500, details)


class ExternalServiceError(DazaiError):
    """Exception raised for errors when communicating with external services."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Initialize with a 502 status code."""
        super().__init__(message, 502, details)


class NLPError(DazaiError):
    """Exception raised for errors in NLP processing."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Initialize with a 500 status code."""
        super().__init__(message, 500, details)
