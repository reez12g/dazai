"""
Summarization service for text summarization.

This module provides functionality for summarizing Japanese text
using NLP techniques.
"""
import logging
from typing import Optional

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

from app.config import nlp_settings

# Configure logging
logger = logging.getLogger(__name__)


class SummarizationService:
    """
    Service for summarizing Japanese text.

    This service uses a pre-trained T5 model to generate concise summaries
    of longer Japanese texts.
    """

    def __init__(self):
        """Initialize the Summarization service with lazy-loaded tokenizer and model."""
        self._tokenizer: Optional[T5Tokenizer] = None
        self._model: Optional[T5ForConditionalGeneration] = None
        self.model_name = nlp_settings.SUMMARIZATION_MODEL

    @property
    def tokenizer(self) -> T5Tokenizer:
        """
        Lazy loading of tokenizer.

        Returns:
            The T5 tokenizer
        """
        if self._tokenizer is None:
            try:
                logger.info(f"Loading tokenizer: {self.model_name}")
                self._tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            except Exception as e:
                logger.error(f"Error loading tokenizer: {str(e)}")
                raise
        return self._tokenizer

    @property
    def model(self) -> T5ForConditionalGeneration:
        """
        Lazy loading of model.

        Returns:
            The T5 model
        """
        if self._model is None:
            try:
                logger.info(f"Loading model: {self.model_name}")
                self._model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise
        return self._model

    def summarize_text(self, text: str, max_length: int = None) -> str:
        """
        Summarize the input text.

        Args:
            text: Input text to summarize
            max_length: Maximum length of the summary in tokens

        Returns:
            Summarized text

        Raises:
            ValueError: If the input text is too short to summarize
        """
        # Use settings from config if not explicitly provided
        if max_length is None:
            max_length = nlp_settings.DEFAULT_SUMMARY_LENGTH

        # Check if the text is long enough to summarize
        if len(text) < 50:
            logger.warning("Text is too short to summarize meaningfully")
            return text

        try:
            # Prepare the input with the summarization prefix
            input_text = f"要約: {text}"

            # Tokenize the input
            inputs = self.tokenizer(
                input_text, return_tensors="pt", max_length=1024, truncation=True
            )

            # Generate the summary
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    max_length=max_length,
                    min_length=10,
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True,
                )

            # Decode and return the summary
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return summary

        except Exception as e:
            logger.error(f"Error in summarize_text: {str(e)}")
            # Return a simple truncated version on error
            return text[:max_length] + "..."

    def extract_keywords(self, text: str, num_keywords: int = 5) -> list:
        """
        Extract key phrases or keywords from the text.

        Args:
            text: Input text to extract keywords from
            num_keywords: Number of keywords to extract

        Returns:
            List of extracted keywords
        """
        try:
            # Prepare the input with the keyword extraction prefix
            input_text = f"キーワード抽出: {text}"

            # Tokenize the input
            inputs = self.tokenizer(
                input_text, return_tensors="pt", max_length=1024, truncation=True
            )

            # Generate the keywords
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"], max_length=50, num_beams=4, early_stopping=True
                )

            # Decode the output
            keywords_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Split into individual keywords and limit to the requested number
            keywords = [kw.strip() for kw in keywords_text.split(",")]
            return keywords[:num_keywords]

        except Exception as e:
            logger.error(f"Error in extract_keywords: {str(e)}")
            # Return empty list on error
            return []
