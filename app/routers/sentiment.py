"""Sentiment analysis router for sentiment analysis endpoints.

This module contains endpoints for analyzing sentiment in Japanese text.
"""
import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.schemas import SentimentAnalysisRequest, SentimentAnalysisResponse
from app.services.sentiment_service import SentimentService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/sentiment", tags=["Sentiment Analysis"])


def get_sentiment_service() -> SentimentService:
    """Dependency for SentimentService."""
    return SentimentService()


# Create a dependency
sentiment_service_dependency = Depends(get_sentiment_service)


@router.post("/", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(
    request: SentimentAnalysisRequest,
    sentiment_service: SentimentService = sentiment_service_dependency,
) -> Dict[str, str]:
    """Analyze sentiment in Japanese text.

    Args:
        request: Object containing text to analyze
        sentiment_service: Injected SentimentService

    Returns:
        A dictionary with sentiment analysis results
    """
    try:
        result = sentiment_service.analyze_sentiment(text=request.text)
        return result
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during sentiment analysis",
        )


@router.post("/emotion_keywords", response_model=Dict[str, List[str]])
async def get_emotion_keywords(
    request: SentimentAnalysisRequest,
    sentiment_service: SentimentService = sentiment_service_dependency,
) -> Dict[str, List[str]]:
    """Get emotion-related keywords based on text sentiment.

    Args:
        request: Object containing text to analyze
        sentiment_service: Injected SentimentService

    Returns:
        A dictionary of emotion keywords by category
    """
    try:
        # First analyze the sentiment
        sentiment_result = sentiment_service.analyze_sentiment(text=request.text)

        # Then get emotion keywords based on the dominant sentiment
        emotion_keywords = sentiment_service.get_emotion_keywords(
            sentiment=sentiment_result["sentiment"]
        )

        return emotion_keywords
    except Exception as e:
        logger.error(f"Error getting emotion keywords: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving emotion keywords",
        )
