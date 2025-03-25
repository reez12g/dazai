"""
NLP service for text generation using GPT-2.

This module provides functionality for generating predictive text
using the GPT-2 language model.
"""
import logging
from typing import Optional

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

from app.config import nlp_settings

# Configure logging
logger = logging.getLogger(__name__)


class NLPService:
    """Natural Language Processing service for text generation using GPT-2."""

    def __init__(self):
        """Initialize the NLP service with lazy-loaded tokenizer and model."""
        self._tokenizer: Optional[GPT2Tokenizer] = None
        self._model: Optional[GPT2LMHeadModel] = None
        self.model_name = nlp_settings.MODEL_NAME

    @property
    def tokenizer(self) -> GPT2Tokenizer:
        """
        Lazy loading of tokenizer.

        Returns:
            The GPT-2 tokenizer
        """
        if self._tokenizer is None:
            logger.info(f"Loading tokenizer: {self.model_name}")
            self._tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        return self._tokenizer

    @property
    def model(self) -> GPT2LMHeadModel:
        """
        Lazy loading of model.

        Returns:
            The GPT-2 model
        """
        if self._model is None:
            logger.info(f"Loading model: {self.model_name}")
            self._model = GPT2LMHeadModel.from_pretrained(self.model_name)
        return self._model

    def generate_text(
        self,
        text: str,
        max_additional_tokens: int = None,
        do_sample: bool = None
    ) -> str:
        """
        Generate predictive text based on the input.

        Args:
            text: Input text to generate from
            max_additional_tokens: Maximum number of additional tokens to generate
            do_sample: Whether to use sampling for generation

        Returns:
            Generated text with special tokens removed
        """
        # Use settings from config if not explicitly provided
        if max_additional_tokens is None:
            max_additional_tokens = nlp_settings.MAX_ADDITIONAL_TOKENS

        if do_sample is None:
            do_sample = nlp_settings.DO_SAMPLE

        try:
            # Encode the input text
            input_ids = self.tokenizer.encode(text, return_tensors="pt")

            # Calculate the maximum length
            max_length = input_ids.size()[1] + max_additional_tokens

            # Generate text
            with torch.no_grad():
                output = self.model.generate(
                    input_ids,
                    do_sample=do_sample,
                    max_length=max_length,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            # Decode the output and clean it
            decoded_output = self.tokenizer.batch_decode(output)[0]
            cleaned_output = decoded_output.replace('</s>', '').replace('<unk>', '')

            return cleaned_output

        except Exception as e:
            logger.error(f"Error in generate_text: {str(e)}")
            # Return original text on error
            return text
