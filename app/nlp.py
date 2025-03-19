from typing import Optional
import logging
import torch
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,  # Using GPT2Tokenizer instead of T5Tokenizer for consistency
)

logger = logging.getLogger(__name__)

class NLP:
    """Natural Language Processing class for text generation using GPT-2."""

    MODEL_NAME = "rinna/japanese-gpt2-small"

    def __init__(self):
        """Initialize the NLP class with tokenizer and model."""
        self._tokenizer = None
        self._model = None

    @property
    def tokenizer(self):
        """Lazy loading of tokenizer."""
        if self._tokenizer is None:
            logger.info(f"Loading tokenizer: {self.MODEL_NAME}")
            self._tokenizer = GPT2Tokenizer.from_pretrained(self.MODEL_NAME)
        return self._tokenizer

    @property
    def model(self):
        """Lazy loading of model."""
        if self._model is None:
            logger.info(f"Loading model: {self.MODEL_NAME}")
            self._model = GPT2LMHeadModel.from_pretrained(self.MODEL_NAME)
        return self._model

    def predictive_sentences(self, text: str, max_additional_tokens: int = 80, do_sample: bool = True) -> str:
        """
        Generate predictive text based on the input.

        Args:
            text: Input text to generate from
            max_additional_tokens: Maximum number of additional tokens to generate
            do_sample: Whether to use sampling for generation

        Returns:
            Generated text with special tokens removed
        """
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
            logger.error(f"Error in predictive_sentences: {str(e)}")
            return text  # Return original text on error
