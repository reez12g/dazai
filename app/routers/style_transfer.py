"""
Style transfer router for text style transformation endpoints.

This module contains endpoints for transforming text into different literary styles.
"""
import logging
from typing import Dict, List
from fastapi import APIRouter, HTTPException, status, Depends

from app.models.schemas import StyleTransferRequest, StyleTransferResponse
from app.services.style_transfer_service import StyleTransferService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/style_transfer", tags=["Style Transfer"])


def get_style_transfer_service():
    """Dependency for StyleTransferService."""
    return StyleTransferService()


@router.post("/", response_model=StyleTransferResponse)
async def transfer_style(
    request: StyleTransferRequest,
    style_transfer_service: StyleTransferService = Depends(get_style_transfer_service)
) -> Dict[str, str]:
    """
    Transform text into a specified literary style.

    Args:
        request: Object containing text to transform and target style
        style_transfer_service: Injected StyleTransferService

    Returns:
        A dictionary with the transformed text
    """
    try:
        transformed_text = style_transfer_service.transform_text(
            text=request.text,
            target_style=request.target_style
        )
        return {"transformed_text": transformed_text}
    except ValueError as e:
        logger.error(f"Invalid style transfer request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in style transfer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during style transfer"
        )


@router.get("/available_styles", response_model=List[str])
async def get_available_styles(
    style_transfer_service: StyleTransferService = Depends(get_style_transfer_service)
) -> List[str]:
    """
    Get a list of available literary styles for transformation.

    Args:
        style_transfer_service: Injected StyleTransferService

    Returns:
        A list of available style names
    """
    try:
        return style_transfer_service.get_available_styles()
    except Exception as e:
        logger.error(f"Error retrieving available styles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving available styles"
        )
