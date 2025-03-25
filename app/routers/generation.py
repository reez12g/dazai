"""
Generation router for text generation endpoints.

This module contains endpoints for generating predictive text.
"""
import json
import logging
from typing import Dict
import requests
from fastapi import APIRouter, HTTPException, status, Depends

from app.models.schemas import SentenceMaterial, TaskResponse
from app.services.nlp_service import NLPService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/predictive_sentences", tags=["Generation"])


def get_nlp_service():
    """Dependency for NLPService."""
    return NLPService()


@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=TaskResponse)
async def generate_predictive_sentences(
    sentence_material: SentenceMaterial,
    nlp_service: NLPService = Depends(get_nlp_service)
) -> Dict[str, str]:
    """
    Generate predictive text and send it to the specified URL.

    Args:
        sentence_material: Object containing text to generate from and response URL
        nlp_service: Injected NLPService

    Returns:
        A dictionary with status information
    """
    try:
        # Generate the text
        generated_text = nlp_service.generate_text(text=sentence_material.text)

        # Prepare the payload
        payload = json.dumps({
            "text": generated_text,
            "response_type": "in_channel"
        })

        # Send the response
        response = requests.post(
            str(sentence_material.response_url),
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        # Check if the request was successful
        response.raise_for_status()

        return {"status": "Text generated and sent successfully"}
    except requests.RequestException as e:
        logger.error(f"Error sending response: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to send response to the provided URL"
        )
    except Exception as e:
        logger.error(f"Error in predictive_sentences: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during text generation"
        )
