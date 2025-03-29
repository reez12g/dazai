"""
Unit tests for the summarization router.

This module contains tests for the text summarization API endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers.summarization import router, get_summarization_service
from app.models.schemas import SummarizationRequest, SummarizationResponse


@pytest.fixture
def app():
    """Create a FastAPI app with the summarization router."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return TestClient(app)


@pytest.fixture
def mock_summarization_service():
    """Create a mock summarization service."""
    mock_service = MagicMock()
    mock_service.summarize_text.return_value = "要約されたテキスト"
    mock_service.extract_keywords.return_value = ["キーワード1", "キーワード2", "キーワード3"]
    return mock_service


class TestSummarizationRouter:
    """Test cases for the summarization router."""

    def test_summarize_text_success(self, client, mock_summarization_service):
        """Test successful text summarization."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_summarization_service] = lambda: mock_summarization_service

        # Make the request
        response = client.post(
            "/summarization/",
            json={"text": "これは長いテキストです。要約が必要です。", "max_length": 50}
        )

        # Verify the response
        assert response.status_code == 200
        assert response.json() == {"summary": "要約されたテキスト"}

        # Verify the service was called with the correct parameters
        mock_summarization_service.summarize_text.assert_called_once_with(
            text="これは長いテキストです。要約が必要です。",
            max_length=50
        )

        # Clean up
        app.dependency_overrides.clear()

    def test_summarize_text_validation_error(self, client, mock_summarization_service):
        """Test validation error in summarization request."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_summarization_service] = lambda: mock_summarization_service

        # Make a request with invalid max_length (below minimum)
        response = client.post(
            "/summarization/",
            json={"text": "これはテキストです。", "max_length": 5}  # min is 10
        )

        # Verify the response
        assert response.status_code == 422  # Unprocessable Entity

        # The service should not be called
        mock_summarization_service.summarize_text.assert_not_called()

        # Clean up
        app.dependency_overrides.clear()

    def test_summarize_text_value_error(self, client, mock_summarization_service):
        """Test value error in summarization."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_summarization_service] = lambda: mock_summarization_service

        # Make the service raise a ValueError
        mock_summarization_service.summarize_text.side_effect = ValueError("Invalid text")

        # Make the request
        response = client.post(
            "/summarization/",
            json={"text": "これはテキストです。", "max_length": 50}
        )

        # Verify the response
        assert response.status_code == 400  # Bad Request
        assert "Invalid text" in response.json()["detail"]

        # Clean up
        app.dependency_overrides.clear()

    def test_summarize_text_unexpected_error(self, client, mock_summarization_service):
        """Test unexpected error in summarization."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_summarization_service] = lambda: mock_summarization_service

        # Make the service raise an unexpected error
        mock_summarization_service.summarize_text.side_effect = Exception("Unexpected error")

        # Make the request
        response = client.post(
            "/summarization/",
            json={"text": "これはテキストです。", "max_length": 50}
        )

        # Verify the response
        assert response.status_code == 500  # Internal Server Error
        assert "unexpected error" in response.json()["detail"].lower()

        # Clean up
        app.dependency_overrides.clear()

    def test_extract_keywords_success(self, client, mock_summarization_service):
        """Test successful keyword extraction."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_summarization_service] = lambda: mock_summarization_service

        # Make the request
        response = client.post(
            "/summarization/keywords",
            json={"text": "これはキーワード抽出のテストです。", "max_length": 50}
        )

        # Verify the response
        assert response.status_code == 200
        assert response.json() == ["キーワード1", "キーワード2", "キーワード3"]

        # Verify the service was called with the correct parameters
        mock_summarization_service.extract_keywords.assert_called_once_with(
            text="これはキーワード抽出のテストです。",
            num_keywords=5  # Fixed value in the router
        )

        # Clean up
        app.dependency_overrides.clear()

    def test_extract_keywords_error(self, client, mock_summarization_service):
        """Test error in keyword extraction."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_summarization_service] = lambda: mock_summarization_service

        # Make the service raise an error
        mock_summarization_service.extract_keywords.side_effect = Exception("Service error")

        # Make the request
        response = client.post(
            "/summarization/keywords",
            json={"text": "これはキーワード抽出のテストです。", "max_length": 50}
        )

        # Verify the response
        assert response.status_code == 500  # Internal Server Error
        assert "unexpected error" in response.json()["detail"].lower()

        # Clean up
        app.dependency_overrides.clear()
