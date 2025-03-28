"""
Schema definitions for the Dazai application.

This module contains Pydantic models that define the structure of
request and response data for the API endpoints.
"""
from typing import List
from pydantic import BaseModel, HttpUrl, Field


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


class StyleTransferRequest(BaseModel):
    """Data model for style transfer request."""
    text: str
    target_style: str

    class Config:
        schema_extra = {
            "example": {
                "text": "今日はとても良い天気です。",
                "target_style": "meiji"
            }
        }


class StyleTransferResponse(BaseModel):
    """Data model for style transfer response."""
    transformed_text: str

    class Config:
        schema_extra = {
            "example": {
                "transformed_text": "今日はとても良い天気であります。"
            }
        }


class SummarizationRequest(BaseModel):
    """Data model for text summarization request."""
    text: str
    max_length: int = Field(default=100, ge=10, le=500)

    class Config:
        schema_extra = {
            "example": {
                "text": "長い文章をここに入力します。この文章は要約されます。",
                "max_length": 50
            }
        }


class SummarizationResponse(BaseModel):
    """Data model for text summarization response."""
    summary: str

    class Config:
        schema_extra = {
            "example": {
                "summary": "長い文章の要約。"
            }
        }


class SentimentAnalysisRequest(BaseModel):
    """Data model for sentiment analysis request."""
    text: str

    class Config:
        schema_extra = {
            "example": {
                "text": "この映画はとても面白かったです。"
            }
        }


class SentimentAnalysisResponse(BaseModel):
    """Data model for sentiment analysis response."""
    sentiment: str
    score: float
    details: dict

    class Config:
        schema_extra = {
            "example": {
                "sentiment": "positive",
                "score": 0.92,
                "details": {
                    "positive": 0.92,
                    "neutral": 0.07,
                    "negative": 0.01
                }
            }
        }
