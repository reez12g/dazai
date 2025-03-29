"""
Unit tests for the schema models.

This module contains tests for the Pydantic models used in the API.
"""
import pytest
from pydantic import ValidationError

from app.models.schemas import (
    ResponseMessage,
    SentenceMaterial,
    SentimentAnalysisRequest,
    SentimentAnalysisResponse,
    StyleTransferRequest,
    StyleTransferResponse,
    SummarizationRequest,
    SummarizationResponse,
    TaskResponse,
)


class TestSentenceMaterial:
    """Test cases for SentenceMaterial schema."""

    def test_valid_data(self):
        """Test valid data validation."""
        data = {"text": "今日の天気は", "response_url": "https://example.com/webhook"}
        model = SentenceMaterial(**data)
        assert model.text == data["text"]
        assert str(model.response_url) == data["response_url"]

    def test_invalid_url(self):
        """Test invalid URL validation."""
        data = {"text": "今日の天気は", "response_url": "not-a-url"}  # Invalid URL
        with pytest.raises(ValidationError):
            SentenceMaterial(**data)

    def test_missing_fields(self):
        """Test missing required fields."""
        # Missing text
        data = {"response_url": "https://example.com/webhook"}
        with pytest.raises(ValidationError):
            SentenceMaterial(**data)

        # Missing response_url
        data = {"text": "今日の天気は"}
        with pytest.raises(ValidationError):
            SentenceMaterial(**data)


class TestResponseMessage:
    """Test cases for ResponseMessage schema."""

    def test_valid_data(self):
        """Test valid data validation."""
        data = {"text": "信じられているから走るのだ。少し考えてみよう。"}
        model = ResponseMessage(**data)
        assert model.text == data["text"]

    def test_missing_text(self):
        """Test missing text field."""
        data = {}
        with pytest.raises(ValidationError):
            ResponseMessage(**data)


class TestTaskResponse:
    """Test cases for TaskResponse schema."""

    def test_valid_data(self):
        """Test valid data validation."""
        data = {"status": "Text generated and sent successfully"}
        model = TaskResponse(**data)
        assert model.status == data["status"]

    def test_missing_status(self):
        """Test missing status field."""
        data = {}
        with pytest.raises(ValidationError):
            TaskResponse(**data)


class TestStyleTransferRequest:
    """Test cases for StyleTransferRequest schema."""

    def test_valid_data(self):
        """Test valid data validation."""
        data = {"text": "今日はとても良い天気です。", "target_style": "meiji"}
        model = StyleTransferRequest(**data)
        assert model.text == data["text"]
        assert model.target_style == data["target_style"]

    def test_missing_fields(self):
        """Test missing required fields."""
        # Missing text
        data = {"target_style": "meiji"}
        with pytest.raises(ValidationError):
            StyleTransferRequest(**data)

        # Missing target_style
        data = {"text": "今日はとても良い天気です。"}
        with pytest.raises(ValidationError):
            StyleTransferRequest(**data)


class TestStyleTransferResponse:
    """Test cases for StyleTransferResponse schema."""

    def test_valid_data(self):
        """Test valid data validation."""
        data = {"transformed_text": "今日はとても良い天気であります。"}
        model = StyleTransferResponse(**data)
        assert model.transformed_text == data["transformed_text"]

    def test_missing_transformed_text(self):
        """Test missing transformed_text field."""
        data = {}
        with pytest.raises(ValidationError):
            StyleTransferResponse(**data)


class TestSummarizationRequest:
    """Test cases for SummarizationRequest schema."""

    def test_valid_data(self):
        """Test valid data validation."""
        data = {"text": "長い文章をここに入力します。この文章は要約されます。", "max_length": 50}
        model = SummarizationRequest(**data)
        assert model.text == data["text"]
        assert model.max_length == data["max_length"]

    def test_default_max_length(self):
        """Test default max_length value."""
        data = {"text": "長い文章をここに入力します。この文章は要約されます。"}
        model = SummarizationRequest(**data)
        assert model.text == data["text"]
        assert model.max_length == 100  # Default value

    def test_invalid_max_length(self):
        """Test invalid max_length values."""
        # Too small
        data = {"text": "長い文章をここに入力します。", "max_length": 5}  # Below minimum (10)
        with pytest.raises(ValidationError):
            SummarizationRequest(**data)

        # Too large
        data = {"text": "長い文章をここに入力します。", "max_length": 600}  # Above maximum (500)
        with pytest.raises(ValidationError):
            SummarizationRequest(**data)

    def test_missing_text(self):
        """Test missing text field."""
        data = {"max_length": 50}
        with pytest.raises(ValidationError):
            SummarizationRequest(**data)


class TestSummarizationResponse:
    """Test cases for SummarizationResponse schema."""

    def test_valid_data(self):
        """Test valid data validation."""
        data = {"summary": "長い文章の要約。"}
        model = SummarizationResponse(**data)
        assert model.summary == data["summary"]

    def test_missing_summary(self):
        """Test missing summary field."""
        data = {}
        with pytest.raises(ValidationError):
            SummarizationResponse(**data)


class TestSentimentAnalysisRequest:
    """Test cases for SentimentAnalysisRequest schema."""

    def test_valid_data(self):
        """Test valid data validation."""
        data = {"text": "この映画はとても面白かったです。"}
        model = SentimentAnalysisRequest(**data)
        assert model.text == data["text"]

    def test_missing_text(self):
        """Test missing text field."""
        data = {}
        with pytest.raises(ValidationError):
            SentimentAnalysisRequest(**data)


class TestSentimentAnalysisResponse:
    """Test cases for SentimentAnalysisResponse schema."""

    def test_valid_data(self):
        """Test valid data validation."""
        data = {
            "sentiment": "positive",
            "score": 0.92,
            "details": {"positive": 0.92, "neutral": 0.07, "negative": 0.01},
        }
        model = SentimentAnalysisResponse(**data)
        assert model.sentiment == data["sentiment"]
        assert model.score == data["score"]
        assert model.details == data["details"]

    def test_missing_fields(self):
        """Test missing required fields."""
        # Missing sentiment
        data = {"score": 0.92, "details": {"positive": 0.92, "neutral": 0.07, "negative": 0.01}}
        with pytest.raises(ValidationError):
            SentimentAnalysisResponse(**data)

        # Missing score
        data = {
            "sentiment": "positive",
            "details": {"positive": 0.92, "neutral": 0.07, "negative": 0.01},
        }
        with pytest.raises(ValidationError):
            SentimentAnalysisResponse(**data)

        # Missing details
        data = {"sentiment": "positive", "score": 0.92}
        with pytest.raises(ValidationError):
            SentimentAnalysisResponse(**data)
