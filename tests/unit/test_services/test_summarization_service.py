"""
Unit tests for the SummarizationService.

This module contains tests for the text summarization service functionality.
"""
import pytest
from unittest.mock import patch, MagicMock

from app.services.summarization_service import SummarizationService
from app.config import nlp_settings


class TestSummarizationService:
    """Test cases for SummarizationService."""

    def test_summarize_text(self, summarization_service, sample_long_japanese_text):
        """Test summarizing text."""
        # Set up the mock to return a specific summary
        summarization_service._tokenizer.decode.return_value = "これは要約されたテキストです。"

        # Call the method
        result = summarization_service.summarize_text(sample_long_japanese_text)

        # Verify the result
        assert result == "これは要約されたテキストです。"

        # Verify the model was called with the correct input
        summarization_service._tokenizer.assert_called_once()
        summarization_service._model.generate.assert_called_once()

    def test_summarize_text_with_custom_length(self, summarization_service, sample_long_japanese_text):
        """Test summarizing text with a custom max length."""
        # Set up the mock
        summarization_service._tokenizer.decode.return_value = "カスタム長さの要約。"

        # Call the method with a custom max_length
        custom_length = 50
        result = summarization_service.summarize_text(sample_long_japanese_text, max_length=custom_length)

        # Verify the result
        assert result == "カスタム長さの要約。"

        # Verify the model was called with the correct max_length
        summarization_service._model.generate.assert_called_once()
        # Extract the kwargs from the call
        _, kwargs = summarization_service._model.generate.call_args
        assert kwargs["max_length"] == custom_length

    def test_summarize_short_text(self, summarization_service):
        """Test summarizing text that is too short."""
        short_text = "短いテキスト。"  # Short text

        # Call the method
        result = summarization_service.summarize_text(short_text)

        # For short text, it should return the original text
        assert result == short_text

        # The model should not be called
        summarization_service._tokenizer.assert_not_called()
        summarization_service._model.generate.assert_not_called()

    def test_summarize_text_error_handling(self, summarization_service, sample_long_japanese_text):
        """Test error handling during summarization."""
        # Make the model generate method raise an exception
        summarization_service._model.generate.side_effect = Exception("Model error")

        # Call the method
        result = summarization_service.summarize_text(sample_long_japanese_text)

        # Should return a truncated version of the original text
        assert result.endswith("...")
        assert len(result) <= nlp_settings.DEFAULT_SUMMARY_LENGTH + 3  # +3 for "..."

    def test_extract_keywords(self, summarization_service, sample_long_japanese_text):
        """Test extracting keywords from text."""
        # Set up the mock to return comma-separated keywords
        summarization_service._tokenizer.decode.return_value = "日本文学, 四季, 文化, 作家, 自然"

        # Call the method
        result = summarization_service.extract_keywords(sample_long_japanese_text)

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 5
        assert "日本文学" in result
        assert "四季" in result

        # Verify the model was called
        summarization_service._tokenizer.assert_called_once()
        summarization_service._model.generate.assert_called_once()

    def test_extract_keywords_with_custom_count(self, summarization_service, sample_long_japanese_text):
        """Test extracting a custom number of keywords."""
        # Set up the mock to return comma-separated keywords
        summarization_service._tokenizer.decode.return_value = "日本文学, 四季, 文化, 作家, 自然, 歴史, 芸術"

        # Call the method with a custom number of keywords
        num_keywords = 3
        result = summarization_service.extract_keywords(sample_long_japanese_text, num_keywords=num_keywords)

        # Verify the result has the correct number of keywords
        assert len(result) == num_keywords

    def test_extract_keywords_error_handling(self, summarization_service, sample_long_japanese_text):
        """Test error handling during keyword extraction."""
        # Make the model generate method raise an exception
        summarization_service._model.generate.side_effect = Exception("Model error")

        # Call the method
        result = summarization_service.extract_keywords(sample_long_japanese_text)

        # Should return an empty list on error
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.services.summarization_service.T5Tokenizer')
    @patch('app.services.summarization_service.T5ForConditionalGeneration')
    def test_lazy_loading(self, mock_model_cls, mock_tokenizer_cls):
        """Test lazy loading of tokenizer and model."""
        # Create a new service instance without pre-loaded models
        service = SummarizationService()

        # Accessing tokenizer should trigger loading
        tokenizer = service.tokenizer
        mock_tokenizer_cls.from_pretrained.assert_called_once()

        # Accessing model should trigger loading
        model = service.model
        mock_model_cls.from_pretrained.assert_called_once()

    @patch('app.services.summarization_service.T5Tokenizer')
    def test_tokenizer_loading_error(self, mock_tokenizer_cls):
        """Test error handling when tokenizer loading fails."""
        # Make tokenizer loading fail
        mock_tokenizer_cls.from_pretrained.side_effect = Exception("Tokenizer error")

        # Create a new service instance
        service = SummarizationService()

        # Accessing tokenizer should raise the exception
        with pytest.raises(Exception) as excinfo:
            tokenizer = service.tokenizer

        assert "Tokenizer error" in str(excinfo.value)

    @patch('app.services.summarization_service.T5ForConditionalGeneration')
    def test_model_loading_error(self, mock_model_cls, summarization_service):
        """Test error handling when model loading fails."""
        # Reset the model to None
        summarization_service._model = None

        # Make model loading fail
        mock_model_cls.from_pretrained.side_effect = Exception("Model error")

        # Accessing model should raise the exception
        with pytest.raises(Exception) as excinfo:
            model = summarization_service.model

        assert "Model error" in str(excinfo.value)
