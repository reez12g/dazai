"""
Style transfer service for text style transformation.

This module provides functionality for transforming text into different
literary styles using NLP techniques.
"""
import logging
import re
from typing import Dict, List, Optional

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

from app.config import nlp_settings

# Configure logging
logger = logging.getLogger(__name__)


class StyleTransferService:
    """
    Service for transforming text into different literary styles.

    This service uses a fine-tuned T5 model to transform text between different
    Japanese literary styles, such as formal, casual, Meiji era, etc.
    """

    def __init__(self):
        """Initialize the Style Transfer service with lazy-loaded tokenizer and model."""
        self._tokenizer: Optional[T5Tokenizer] = None
        self._model: Optional[T5ForConditionalGeneration] = None
        self.model_name = nlp_settings.STYLE_TRANSFER_MODEL

        # Define available styles with their descriptions and prefixes
        self.styles: Dict[str, Dict[str, str]] = {
            "meiji": {
                "description": "Meiji era literary style (1868-1912)",
                "prefix": "明治文体に変換: "
            },
            "taisho": {
                "description": "Taisho era literary style (1912-1926)",
                "prefix": "大正文体に変換: "
            },
            "showa": {
                "description": "Showa era literary style (1926-1989)",
                "prefix": "昭和文体に変換: "
            },
            "formal": {
                "description": "Formal, polite Japanese",
                "prefix": "丁寧な文体に変換: "
            },
            "casual": {
                "description": "Casual, conversational Japanese",
                "prefix": "カジュアルな文体に変換: "
            },
            "academic": {
                "description": "Academic, scholarly Japanese",
                "prefix": "学術的な文体に変換: "
            },
            "poetic": {
                "description": "Poetic, literary Japanese",
                "prefix": "詩的な文体に変換: "
            }
        }

        # Rules for style transformation when model is not available
        self.transformation_rules: Dict[str, Dict[str, List[tuple]]] = {
            "formal": {
                "patterns": [
                    (r"だ([。、])", r"です\1"),
                    (r"([^ま])す([。、])", r"\1します\2"),
                    (r"だよ", r"ですよ"),
                    (r"だね", r"ですね"),
                    (r"([^ま])せん", r"\1しません"),
                    (r"俺", r"私"),
                    (r"僕", r"私"),
                    (r"([^ま])した([。、])", r"\1しました\2"),
                ]
            },
            "casual": {
                "patterns": [
                    (r"です([。、])", r"だ\1"),
                    (r"ます([。、])", r"る\1"),
                    (r"ですよ", r"だよ"),
                    (r"ですね", r"だね"),
                    (r"しません", r"しない"),
                    (r"しました", r"した"),
                ]
            },
            "meiji": {
                "patterns": [
                    (r"です", r"であります"),
                    (r"ます", r"まする"),
                    (r"ません", r"ませぬ"),
                    (r"だ([。、])", r"である\1"),
                    (r"私は", r"吾輩は"),
                    (r"彼は", r"彼奴は"),
                    (r"それは", r"其は"),
                    (r"これは", r"此は"),
                ]
            }
        }

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

    def get_available_styles(self) -> List[str]:
        """
        Get a list of available literary styles for transformation.

        Returns:
            A list of available style names
        """
        return list(self.styles.keys())

    def transform_text(self, text: str, target_style: str) -> str:
        """
        Transform text into the specified literary style.

        Args:
            text: Input text to transform
            target_style: Target literary style

        Returns:
            Transformed text in the target style

        Raises:
            ValueError: If the target style is not supported
        """
        # Validate the target style
        if target_style not in self.styles:
            available_styles = ", ".join(self.styles.keys())
            raise ValueError(f"Unsupported style: {target_style}. Available styles: {available_styles}")

        try:
            # Try to use the model for transformation
            return self._transform_with_model(text, target_style)
        except Exception as e:
            logger.warning(f"Model-based transformation failed: {str(e)}. Falling back to rule-based transformation.")
            # Fall back to rule-based transformation
            return self._transform_with_rules(text, target_style)

    def _transform_with_model(self, text: str, target_style: str) -> str:
        """
        Transform text using the T5 model.

        Args:
            text: Input text to transform
            target_style: Target literary style

        Returns:
            Transformed text in the target style
        """
        # Prepare the input with the style prefix
        style_prefix = self.styles[target_style]["prefix"]
        input_text = f"{style_prefix}{text}"

        # Tokenize the input
        inputs = self.tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)

        # Generate the transformed text
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=512,
                num_beams=5,
                early_stopping=True
            )

        # Decode and return the transformed text
        transformed_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return transformed_text

    def _transform_with_rules(self, text: str, target_style: str) -> str:
        """
        Transform text using rule-based transformations.

        Args:
            text: Input text to transform
            target_style: Target literary style

        Returns:
            Transformed text in the target style
        """
        # If we don't have rules for this style, return the original text
        if target_style not in self.transformation_rules:
            logger.warning(f"No transformation rules available for style: {target_style}")
            return text

        transformed_text = text

        # Apply each transformation pattern
        for pattern, replacement in self.transformation_rules[target_style]["patterns"]:
            transformed_text = re.sub(pattern, replacement, transformed_text)

        return transformed_text
