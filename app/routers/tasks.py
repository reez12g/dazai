"""
Tasks router for asynchronous task endpoints.

This module contains endpoints for creating and managing asynchronous tasks.
"""
import logging
from fastapi import APIRouter, Form, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from app.models.schemas import ResponseMessage
from app.services.task_service import TaskService
from app.services.cliche_service import ClicheService
from app.config import tasks_enabled

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/predictive_sentences_task", tags=["Tasks"])


def get_task_service():
    """Dependency for TaskService."""
    return TaskService()


def get_cliche_service():
    """Dependency for ClicheService."""
    return ClicheService()


@router.post("/", response_model=ResponseMessage)
async def create_predictive_sentences_task(
    text: str = Form(...),
    response_url: str = Form(...),
    task_service: TaskService = Depends(get_task_service),
    cliche_service: ClicheService = Depends(get_cliche_service)
) -> JSONResponse:
    """
    Create a Cloud Task for asynchronous sentence generation.

    Args:
        text: The input text to generate from
        response_url: The URL to send the generated text to
        task_service: Injected TaskService
        cliche_service: Injected ClicheService

    Returns:
        A JSON response with a random cliche message
    """
    if not tasks_enabled:
        logger.warning("Task creation attempted but tasks are disabled")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Task service is not available"
        )
        
    try:
        task_service.create_task(text=text, response_url=response_url)
        return JSONResponse(content={"text": cliche_service.get_random_cliche()})
    except ValueError as e:
        logger.error(f"Configuration error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )
