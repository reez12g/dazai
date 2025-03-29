"""
Unit tests for the sentiment router.

This module contains tests for the sentiment analysis API endpoints.
"""
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.models.schemas import SentimentAnalysisRequest, SentimentAnalysisResponse
from app.routers.sentiment import get_sentiment_service, router


@pytest.fixture
def app():
    """Create a FastAPI app with the sentiment router."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return TestClient(app)


@pytest.fixture
def mock_sentiment_service():
    """Create a mock sentiment service."""
    mock_service = MagicMock()

    # Mock analyze_sentiment method
    mock_service.analyze_sentiment.return_value = {
        "sentiment": "positive",
        "score": 0.85,
        "details": {"positive": 0.85, "neutral": 0.10, "negative": 0.05},
    }

    # Mock get_emotion_keywords method
    mock_service.get_emotion_keywords.return_value = {
        "joy": ["喜び", "嬉しい", "楽しい"],
        "excitement": ["興奮", "ワクワク", "熱狂"],
    }

    return mock_service


class TestSentimentRouter:
    """Test cases for the sentiment router."""

    def test_analyze_sentiment_success(self, client, mock_sentiment_service):
        """Test successful sentiment analysis."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_sentiment_service] = lambda: mock_sentiment_service

        # Make the request
        response = client.post("/sentiment/", json={"text": "この映画はとても面白かったです。"})

        # Verify the response
        assert response.status_code == 200
        result = response.json()
        assert result["sentiment"] == "positive"
        assert result["score"] == 0.85
        assert "details" in result
        assert result["details"]["positive"] == 0.85

        # Verify the service was called with the correct parameters
        mock_sentiment_service.analyze_sentiment.assert_called_once_with(text="この映画はとても面白かったです。")

        # Clean up
        app.dependency_overrides.clear()

    def test_analyze_sentiment_validation_error(self, client, mock_sentiment_service):
        """Test validation error in sentiment analysis request."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_sentiment_service] = lambda: mock_sentiment_service

        # Make a request with missing required field
        response = client.post("/sentiment/", json={})  # Missing text field

        # Verify the response
        assert response.status_code == 422  # Unprocessable Entity

        # The service should not be called
        mock_sentiment_service.analyze_sentiment.assert_not_called()

        # Clean up
        app.dependency_overrides.clear()

    def test_analyze_sentiment_unexpected_error(self, client, mock_sentiment_service):
        """Test unexpected error in sentiment analysis."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_sentiment_service] = lambda: mock_sentiment_service

        # Make the service raise an unexpected error
        mock_sentiment_service.analyze_sentiment.side_effect = Exception("Unexpected error")

        # Make the request
        response = client.post("/sentiment/", json={"text": "この映画はとても面白かったです。"})

        # Verify the response
        assert response.status_code == 500  # Internal Server Error
        assert "unexpected error" in response.json()["detail"].lower()

        # Clean up
        app.dependency_overrides.clear()

    def test_get_emotion_keywords_success(self, client, mock_sentiment_service):
        """Test successful emotion keywords retrieval."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_sentiment_service] = lambda: mock_sentiment_service

        # Set up the mock to first analyze sentiment, then get keywords
        mock_sentiment_service.analyze_sentiment.return_value = {
            "sentiment": "positive",
            "score": 0.85,
            "details": {},
        }

        # Make the request
        response = client.post("/sentiment/emotion_keywords", json={"text": "この映画はとても面白かったです。"})

        # Verify the response
        assert response.status_code == 200
        result = response.json()
        assert "joy" in result
        assert "excitement" in result
        assert "喜び" in result["joy"]

        # Verify the service methods were called in the correct order
        mock_sentiment_service.analyze_sentiment.assert_called_once_with(text="この映画はとても面白かったです。")
        mock_sentiment_service.get_emotion_keywords.assert_called_once_with(sentiment="positive")

        # Clean up
        app.dependency_overrides.clear()

    def test_get_emotion_keywords_error(self, client, mock_sentiment_service):
        """Test error in emotion keywords retrieval."""
        # Override the dependency
        app = client.app
        app.dependency_overrides[get_sentiment_service] = lambda: mock_sentiment_service

        # Make the service raise an error
        mock_sentiment_service.analyze_sentiment.side_effect = Exception("Service error")

        # Make the request
        response = client.post("/sentiment/emotion_keywords", json={"text": "この映画はとても面白かったです。"})

        # Verify the response
        assert response.status_code == 500  # Internal Server Error
        assert "unexpected error" in response.json()["detail"].lower()

        # Clean up
        app.dependency_overrides.clear()
