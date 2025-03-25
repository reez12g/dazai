"""
Task service for Google Cloud Tasks integration.

This module provides functionality for creating and managing
asynchronous tasks using Google Cloud Tasks.
"""
import json
import logging
from typing import Dict, Any, Optional

from google.cloud import tasks_v2
from google.api_core.exceptions import GoogleAPIError

from app.config import task_settings, tasks_enabled

# Configure logging
logger = logging.getLogger(__name__)


class TaskService:
    """Handles Google Cloud Task creation and management."""

    def __init__(self) -> None:
        """Initialize the Task service."""
        if not tasks_enabled:
            logger.warning("Task service initialized but tasks are disabled due to invalid configuration.")
            self.client = None
            return
            
        self.client = tasks_v2.CloudTasksClient()

    def create_task(self, text: str, response_url: str) -> Optional[tasks_v2.Task]:
        """
        Create a new Cloud Task for asynchronous processing.

        Args:
            text: The text to process
            response_url: The URL to send the result to

        Returns:
            The created task object or None if creation failed

        Raises:
            ValueError: If tasks are disabled due to invalid configuration
            GoogleAPIError: If task creation fails
        """
        if not tasks_enabled or self.client is None:
            error_msg = "Cannot create task: Tasks are disabled due to invalid configuration"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            # Create the task queue path
            parent = self.client.queue_path(
                task_settings.PROJECT_ID,
                task_settings.LOCATION_ID,
                task_settings.QUEUE_ID
            )

            # Define the task
            task: Dict[str, Any] = {
                "http_request": {
                    "http_method": tasks_v2.HttpMethod.POST,
                    "url": task_settings.TASK_URL,
                    "oidc_token": {
                        "service_account_email": task_settings.SERVICE_ACCOUNT_EMAIL,
                        "audience": task_settings.AUDIENCE,
                    },
                    "headers": {"Content-type": "application/json"}
                }
            }

            # Prepare the payload
            payload = json.dumps({
                "text": text,
                "response_url": response_url
            })

            # Add the payload to the task
            task["http_request"]["body"] = payload.encode()

            # Create the task
            response = self.client.create_task(request={"parent": parent, "task": task})

            logger.info(f"Task created: {response.name}")
            return response

        except GoogleAPIError as e:
            logger.error(f"Google API error creating task: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating task: {str(e)}")
            raise
