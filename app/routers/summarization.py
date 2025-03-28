"""
Summarization router for text summarization endpoints.

This module contains endpoints for summarizing Japanese text.
"""
import logging
from typing import Dict, List
from fastapi import APIRouter, HTTPException, status, Depends

from app.models.schemas import SummarizationRequest, SummarizationResponse
from app.services.summarization_service import SummarizationService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/summarization", tags=["Summarization"])


def get_summarization_service():
    """Dependency for SummarizationService."""
    return SummarizationService()


@router.post("/", response_model=SummarizationResponse)
async def summarize_text(
    request: SummarizationRequest,
    summarization_service: SummarizationService = Depends(get_summarization_service)
) -> Dict[str, str]:
    """
    Summarize Japanese text.

    Args:
        request: Object containing text to summarize and max length
        summarization_service: Injected SummarizationService

    Returns:
        A dictionary with the summarized text
    """
    try:
        summary = summarization_service.summarize_text(
            text=request.text,
            max_length=request.max_length
        )
        return {"summary": summary}
    except ValueError as e:
        logger.error(f"Invalid summarization request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in summarization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during summarization"
        )


@router.post("/keywords", response_model=List[str])
async def extract_keywords(
    request: SummarizationRequest,
    summarization_service: SummarizationService = Depends(get_summarization_service)
) -> List[str]:
    """
    Extract keywords from Japanese text.

    Args:
        request: Object containing text to extract keywords from
        summarization_service: Injected SummarizationService

    Returns:
        A list of extracted keywords
    """
    try:
        keywords = summarization_service.extract_keywords(
            text=request.text,
            num_keywords=5  # Fixed number of keywords
        )
        return keywords
    except Exception as e:
        logger.error(f"Error in keyword extraction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during keyword extraction"
        )
