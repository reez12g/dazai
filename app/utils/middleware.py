"""
Middleware for the Dazai application.

This module contains middleware components for the FastAPI application,
such as exception handlers and request/response processors.
"""
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.utils.exceptions import DazaiError

# Configure logging
logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Set up exception handlers for the application.

    Args:
        app: The FastAPI application
    """

    @app.exception_handler(DazaiError)
    async def dazai_exception_handler(request: Request, exc: DazaiError) -> JSONResponse:
        """
        Handle custom DazaiError exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            A JSON response with the error details
        """
        logger.error(f"DazaiError: {exc.message}", exc_info=True)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.message,
                **({"extra": exc.details} if exc.details else {})
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """
        Handle request validation errors.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            A JSON response with the validation error details
        """
        logger.error(f"Validation error: {exc.errors()}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Validation error",
                "errors": exc.errors()
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Handle all other exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            A JSON response with a generic error message
        """
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected error occurred"
            }
        )
