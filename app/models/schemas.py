"""
Schema definitions for the Dazai application.

This module contains Pydantic models that define the structure of
request and response data for the API endpoints.
"""
from pydantic import BaseModel, HttpUrl


class SentenceMaterial(BaseModel):
    """Data model for sentence generation request."""
    text: str
    response_url: HttpUrl
    
    class Config:
        schema_extra = {
            "example": {
                "text": "今日の天気は",
                "response_url": "https://example.com/webhook"
            }
        }


class ResponseMessage(BaseModel):
    """Data model for API responses."""
    text: str
    
    class Config:
        schema_extra = {
            "example": {
                "text": "信じられているから走るのだ。少し考えてみよう。"
            }
        }


class TaskResponse(BaseModel):
    """Data model for task creation responses."""
    status: str
    
    class Config:
        schema_extra = {
            "example": {
                "status": "Text generated and sent successfully"
            }
        }
