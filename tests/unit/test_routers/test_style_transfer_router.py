"""
Unit tests for the style transfer router.

This module contains tests for the style transfer API endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers.style_transfer import router, get_style_transfer_service
from app.models.schemas import StyleTransferRequest, StyleTransferResponse


@pytest.fixture
def app():
    """Create a FastAPI app with the style transfer router."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return TestClient(app)


@pytest.fixture
def mock_style_transfer_service():
    """Create a mock style transfer service."""
    mock_service = MagicMock()
    mock_service.transform_text.return_value = "変換されたテキスト"
    mock_service.get_available_styles.return_value = ["meiji", "taisho", "formal", "casual"]
    return mock_service


class TestStyleTransferRouter:
    """Test cases for the style transfer router."""

    def test_transfer_style_success(self, client, mock_style_transfer_service):
        """Test successful style transfer."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_style_transfer_service] = lambda: mock_style_transfer_service

        # Make the request
        response = client.post(
            "/style_transfer/",
            json={"text": "これはテストです。", "target_style": "meiji"}
        )

        # Verify the response
        assert response.status_code == 200
        assert response.json() == {"transformed_text": "変換されたテキスト"}

        # Verify the service was called with the correct parameters
        mock_style_transfer_service.transform_text.assert_called_once_with(
            text="これはテストです。",
            target_style="meiji"
        )

        # Clean up
        app.dependency_overrides.clear()

    def test_transfer_style_validation_error(self, client, mock_style_transfer_service):
        """Test validation error in style transfer request."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_style_transfer_service] = lambda: mock_style_transfer_service

        # Make a request with missing required field
        response = client.post(
            "/style_transfer/",
            json={"text": "これはテストです。"}  # Missing target_style
        )

        # Verify the response
        assert response.status_code == 422  # Unprocessable Entity

        # The service should not be called
        mock_style_transfer_service.transform_text.assert_not_called()

        # Clean up
        app.dependency_overrides.clear()

    def test_transfer_style_value_error(self, client, mock_style_transfer_service):
        """Test value error in style transfer."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_style_transfer_service] = lambda: mock_style_transfer_service

        # Make the service raise a ValueError
        mock_style_transfer_service.transform_text.side_effect = ValueError("Invalid style")

        # Make the request
        response = client.post(
            "/style_transfer/",
            json={"text": "これはテストです。", "target_style": "invalid_style"}
        )

        # Verify the response
        assert response.status_code == 400  # Bad Request
        assert "Invalid style" in response.json()["detail"]

        # Clean up
        app.dependency_overrides.clear()

    def test_transfer_style_unexpected_error(self, client, mock_style_transfer_service):
        """Test unexpected error in style transfer."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_style_transfer_service] = lambda: mock_style_transfer_service

        # Make the service raise an unexpected error
        mock_style_transfer_service.transform_text.side_effect = Exception("Unexpected error")

        # Make the request
        response = client.post(
            "/style_transfer/",
            json={"text": "これはテストです。", "target_style": "meiji"}
        )

        # Verify the response
        assert response.status_code == 500  # Internal Server Error
        assert "unexpected error" in response.json()["detail"].lower()

        # Clean up
        app.dependency_overrides.clear()

    def test_get_available_styles_success(self, client, mock_style_transfer_service):
        """Test getting available styles."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_style_transfer_service] = lambda: mock_style_transfer_service

        # Make the request
        response = client.get("/style_transfer/available_styles")

        # Verify the response
        assert response.status_code == 200
        assert response.json() == ["meiji", "taisho", "formal", "casual"]

        # Verify the service was called
        mock_style_transfer_service.get_available_styles.assert_called_once()

        # Clean up
        app.dependency_overrides.clear()

    def test_get_available_styles_error(self, client, mock_style_transfer_service):
        """Test error in getting available styles."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_style_transfer_service] = lambda: mock_style_transfer_service

        # Make the service raise an error
        mock_style_transfer_service.get_available_styles.side_effect = Exception("Service error")

        # Make the request
        response = client.get("/style_transfer/available_styles")

        # Verify the response
        assert response.status_code == 500  # Internal Server Error
        assert "unexpected error" in response.json()["detail"].lower()

        # Clean up
        app.dependency_overrides.clear()
