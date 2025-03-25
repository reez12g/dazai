"""
Main module for the Dazai API application.

This module initializes and configures the FastAPI application,
sets up middleware, and includes all routers.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import app_settings
from app.routers import general, tasks, generation
from app.utils.logging import setup_logging
from app.utils.middleware import setup_exception_handlers

# Set up logging
setup_logging()

# Configure logger for this module
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=app_settings.APP_TITLE,
    description=app_settings.APP_DESCRIPTION,
    version=app_settings.APP_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Set up exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(general.router)
app.include_router(tasks.router)
app.include_router(generation.router)

# Log application startup
logger.info(f"Application {app_settings.APP_TITLE} v{app_settings.APP_VERSION} initialized")

if __name__ == "__main__":
    import uvicorn
    from app.utils.logging import get_log_config

    logger.info("Starting application in standalone mode")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        log_config=get_log_config(),
        reload=True
    )
