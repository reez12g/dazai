import json
import logging
import os
from typing import Any, Dict, Optional

from google.api_core.exceptions import GoogleAPIError
from google.cloud import tasks_v2

# Configure logging
logger = logging.getLogger(__name__)


# Load environment variables with better defaults and documentation
class Config:
    """Configuration for Google Cloud Tasks."""

    PROJECT_ID = os.getenv("PROJECT_ID")
    QUEUE_ID = os.getenv("QUEUE_ID")
    LOCATION_ID = os.getenv("LOCATION_ID")
    TASK_URL = os.getenv("DAZAI_PREDICTIVE_SENTENCES_URL", "http://localhost:8080")
    SERVICE_ACCOUNT_EMAIL = os.getenv("SERVICE_ACCOUNT_EMAIL")
    AUDIENCE = os.getenv("DAZAI_ENDPOINT", "http://localhost:8080")

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        required_vars = ["PROJECT_ID", "QUEUE_ID", "LOCATION_ID", "SERVICE_ACCOUNT_EMAIL"]
        missing = [var for var in required_vars if getattr(cls, var) is None]

        if missing:
            logger.warning(f"Missing required environment variables: {', '.join(missing)}")
            return False
        return True


class Task:
    """Handles Google Cloud Task creation and management."""

    def __init__(self) -> None:
        """Initialize the Task client."""
        self.client = tasks_v2.CloudTasksClient()
        self.config_valid = Config.validate()

        if not self.config_valid:
            logger.warning(
                "Task service initialized with invalid configuration. "
                "Tasks may not be created properly."
            )

    def create_task(self, text: str, response_url: str) -> Optional[tasks_v2.Task]:
        """
        Create a new Cloud Task for asynchronous processing.

        Args:
            text: The text to process
            response_url: The URL to send the result to

        Returns:
            The created task object or None if creation failed

        Raises:
            ValueError: If configuration is invalid
            GoogleAPIError: If task creation fails
        """
        if not self.config_valid:
            error_msg = "Cannot create task: Invalid configuration"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            # Create the task queue path
            parent = self.client.queue_path(Config.PROJECT_ID, Config.LOCATION_ID, Config.QUEUE_ID)

            # Define the task
            task: Dict[str, Any] = {
                "http_request": {
                    "http_method": tasks_v2.HttpMethod.POST,
                    "url": Config.TASK_URL,
                    "oidc_token": {
                        "service_account_email": Config.SERVICE_ACCOUNT_EMAIL,
                        "audience": Config.AUDIENCE,
                    },
                    "headers": {"Content-type": "application/json"},
                }
            }

            # Prepare the payload
            payload = json.dumps({"text": text, "response_url": response_url})

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
