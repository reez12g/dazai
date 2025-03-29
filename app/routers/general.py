"""
General router for basic API endpoints.

This module contains the root endpoint and other general-purpose endpoints.
"""
import logging
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.schemas import ResponseMessage
from app.services.cliche_service import ClicheService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["General"])


def get_cliche_service():
    """Dependency for ClicheService."""
    return ClicheService()


@router.get("/", response_model=ResponseMessage)
async def read_root(cliche_service: ClicheService = Depends(get_cliche_service)) -> Dict[str, str]:
    """
    Root endpoint that returns a random cliche.

    Returns:
        A dictionary with a random cliche message
    """
    try:
        return {"text": cliche_service.get_random_cliche()}
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred"
        )
