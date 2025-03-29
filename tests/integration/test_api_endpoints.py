"""
Integration tests for the API endpoints.

This module contains tests that verify the integration between
API endpoints and services.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Mock external modules
import sys

# Mock NLP libraries
sys.modules['torch'] = MagicMock()
sys.modules['transformers'] = MagicMock()
sys.modules['fugashi'] = MagicMock()
sys.modules['tensorflow'] = MagicMock()

# Mock Google Cloud libraries
google_mock = MagicMock()
api_core_mock = MagicMock()
exceptions_mock = MagicMock()
cloud_mock = MagicMock()
tasks_v2_mock = MagicMock()
protobuf_mock = MagicMock()

# Set up the nested structure
google_mock.api_core = api_core_mock
api_core_mock.exceptions = exceptions_mock
google_mock.cloud = cloud_mock
cloud_mock.tasks_v2 = tasks_v2_mock
google_mock.protobuf = protobuf_mock

# Add the mocks to sys.modules
sys.modules['google'] = google_mock
sys.modules['google.api_core'] = api_core_mock
sys.modules['google.api_core.exceptions'] = exceptions_mock
sys.modules['google.cloud'] = cloud_mock
sys.modules['google.cloud.tasks_v2'] = tasks_v2_mock
sys.modules['google.protobuf'] = protobuf_mock

# Mock config to avoid Pydantic version issues
class MockSettings:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Create mock settings
mock_app_settings = MockSettings(
    APP_TITLE="Dazai API",
    APP_DESCRIPTION="API for Japanese text generation and analysis using NLP models",
    APP_VERSION="1.0.0",
    CORS_ORIGINS=["http://localhost", "http://localhost:8080", "http://127.0.0.1:8080"]
)

mock_nlp_settings = MockSettings(
    MODEL_NAME="rinna/japanese-gpt2-small",
    MAX_ADDITIONAL_TOKENS=80,
    DO_SAMPLE=True,
    STYLE_TRANSFER_MODEL="sonoisa/t5-base-japanese",
    SUMMARIZATION_MODEL="sonoisa/t5-base-japanese-summarize",
    DEFAULT_SUMMARY_LENGTH=100,
    SENTIMENT_MODEL="daigo/bert-base-japanese-sentiment"
)

# Mock the config module
mock_config = MagicMock()
mock_config.app_settings = mock_app_settings
mock_config.nlp_settings = mock_nlp_settings
sys.modules['app.config'] = mock_config

# Import app after mocking
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    return TestClient(app)


class TestStyleTransferEndpoints:
    """Integration tests for style transfer endpoints."""

    @patch('app.services.style_transfer_service.StyleTransferService._transform_with_model')
    def test_style_transfer_endpoint(self, mock_transform, client):
        """Test the style transfer endpoint with mocked model."""
        # Mock the model transformation to avoid actual model loading
        mock_transform.return_value = "明治文体に変換されたテキスト"

        # Make the request
        response = client.post(
            "/style_transfer/",
            json={"text": "これはテストです。", "target_style": "meiji"}
        )

        # Verify the response
        assert response.status_code == 200
        assert "transformed_text" in response.json()
        assert response.json()["transformed_text"] == "明治文体に変換されたテキスト"


class TestSummarizationEndpoints:
    """Integration tests for summarization endpoints."""

    @patch('app.services.summarization_service.SummarizationService.summarize_text')
    def test_summarization_endpoint(self, mock_summarize, client):
        """Test the summarization endpoint with mocked service."""
        # Mock the summarization method
        mock_summarize.return_value = "要約されたテキスト"

        # Make the request
        response = client.post(
            "/summarization/",
            json={"text": "これは長いテキストです。要約が必要です。", "max_length": 50}
        )

        # Verify the response
        assert response.status_code == 200
        assert "summary" in response.json()
        assert response.json()["summary"] == "要約されたテキスト"

    @patch('app.services.summarization_service.SummarizationService.extract_keywords')
    def test_keyword_extraction_endpoint(self, mock_extract, client):
        """Test the keyword extraction endpoint with mocked service."""
        # Mock the keyword extraction method
        mock_extract.return_value = ["キーワード1", "キーワード2", "キーワード3"]

        # Make the request
        response = client.post(
            "/summarization/keywords",
            json={"text": "これはキーワード抽出のテストです。"}
        )

        # Verify the response
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 3
        assert "キーワード1" in response.json()


class TestSentimentEndpoints:
    """Integration tests for sentiment analysis endpoints."""

    @patch('app.services.sentiment_service.SentimentService.analyze_sentiment')
    def test_sentiment_analysis_endpoint(self, mock_analyze, client):
        """Test the sentiment analysis endpoint with mocked service."""
        # Mock the sentiment analysis method
        mock_analyze.return_value = {
            "sentiment": "positive",
            "score": 0.85,
            "details": {
                "positive": 0.85,
                "neutral": 0.10,
                "negative": 0.05
            }
        }

        # Make the request
        response = client.post(
            "/sentiment/",
            json={"text": "この映画はとても面白かったです。"}
        )

        # Verify the response
        assert response.status_code == 200
        result = response.json()
        assert result["sentiment"] == "positive"
        assert result["score"] == 0.85
        assert "details" in result

    @patch('app.services.sentiment_service.SentimentService.analyze_sentiment')
    @patch('app.services.sentiment_service.SentimentService.get_emotion_keywords')
    def test_emotion_keywords_endpoint(self, mock_keywords, mock_analyze, client):
        """Test the emotion keywords endpoint with mocked service."""
        # Mock the sentiment analysis method
        mock_analyze.return_value = {
            "sentiment": "positive",
            "score": 0.85,
            "details": {}
        }

        # Mock the emotion keywords method
        mock_keywords.return_value = {
            "joy": ["喜び", "嬉しい", "楽しい"],
            "excitement": ["興奮", "ワクワク", "熱狂"]
        }

        # Make the request
        response = client.post(
            "/sentiment/emotion_keywords",
            json={"text": "この映画はとても面白かったです。"}
        )

        # Verify the response
        assert response.status_code == 200
        result = response.json()
        assert "joy" in result
        assert "excitement" in result
        assert "喜び" in result["joy"]
