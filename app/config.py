"""
Configuration module for the Dazai application.

This module centralizes all configuration settings for the application,
using Pydantic's BaseSettings for environment variable validation.
"""
import os
from typing import List, Optional
from pydantic import BaseSettings, HttpUrl, validator


class AppSettings(BaseSettings):
    """Application-wide settings."""
    APP_TITLE: str = "Dazai API"
    APP_DESCRIPTION: str = "API for Japanese text generation and analysis using NLP models"
    APP_VERSION: str = "1.0.0"

    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


class NLPSettings(BaseSettings):
    """NLP model settings."""
    # Text generation settings
    MODEL_NAME: str = "rinna/japanese-gpt2-small"
    MAX_ADDITIONAL_TOKENS: int = 80
    DO_SAMPLE: bool = True

    # Style transfer settings
    STYLE_TRANSFER_MODEL: str = "sonoisa/t5-base-japanese"

    # Summarization settings
    SUMMARIZATION_MODEL: str = "sonoisa/t5-base-japanese-summarize"
    DEFAULT_SUMMARY_LENGTH: int = 100

    # Sentiment analysis settings
    SENTIMENT_MODEL: str = "daigo/bert-base-japanese-sentiment"

    class Config:
        env_file = ".env"
        case_sensitive = True


class TaskSettings(BaseSettings):
    """Google Cloud Tasks settings."""
    PROJECT_ID: Optional[str] = None
    QUEUE_ID: Optional[str] = None
    LOCATION_ID: Optional[str] = None
    TASK_URL: str = "http://localhost:8080"
    SERVICE_ACCOUNT_EMAIL: Optional[str] = None
    AUDIENCE: str = "http://localhost:8080"

    @validator('PROJECT_ID', 'QUEUE_ID', 'LOCATION_ID', 'SERVICE_ACCOUNT_EMAIL')
    def check_required_fields(cls, v, values, **kwargs):
        """Validate that required fields are present."""
        if v is None:
            field_name = kwargs.get('field').name
            raise ValueError(f"{field_name} is required for Google Cloud Tasks")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create instances of settings
app_settings = AppSettings()
nlp_settings = NLPSettings()

# Only create task_settings if environment variables are set
try:
    task_settings = TaskSettings()
    tasks_enabled = True
except ValueError:
    # Log warning but don't crash the application
    import logging
    logging.warning("Google Cloud Tasks configuration is incomplete. Task functionality will be disabled.")
    tasks_enabled = False
