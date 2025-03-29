"""
Sentiment analysis service for Japanese text.

This module provides functionality for analyzing sentiment in Japanese text
using NLP techniques.
"""
import logging
import re
from typing import Dict, Optional, Tuple

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from app.config import nlp_settings

# Configure logging
logger = logging.getLogger(__name__)


class SentimentService:
    """
    Service for analyzing sentiment in Japanese text.

    This service uses a pre-trained model to analyze the sentiment of
    Japanese text, classifying it as positive, negative, or neutral.
    """

    def __init__(self):
        """Initialize the Sentiment service with lazy-loaded tokenizer and model."""
        self._tokenizer = None
        self._model = None
        self.model_name = nlp_settings.SENTIMENT_MODEL
        self.labels = ["negative", "neutral", "positive"]

    @property
    def tokenizer(self):
        """
        Lazy loading of tokenizer.

        Returns:
            The BERT tokenizer
        """
        if self._tokenizer is None:
            try:
                logger.info(f"Loading tokenizer: {self.model_name}")
                self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            except Exception as e:
                logger.error(f"Error loading tokenizer: {str(e)}")
                raise
        return self._tokenizer

    @property
    def model(self):
        """
        Lazy loading of model.

        Returns:
            The BERT model
        """
        if self._model is None:
            try:
                logger.info(f"Loading model: {self.model_name}")
                self._model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise
        return self._model

    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze the sentiment of the input text.

        Args:
            text: Input text to analyze

        Returns:
            Dictionary containing sentiment analysis results
        """
        try:
            # Clean and prepare the text
            cleaned_text = self._preprocess_text(text)

            # Tokenize the input
            inputs = self.tokenizer(
                cleaned_text, return_tensors="pt", truncation=True, max_length=512
            )

            # Get sentiment prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                scores = torch.nn.functional.softmax(outputs.logits, dim=1)
                scores_dict = {self.labels[i]: float(scores[0][i]) for i in range(len(self.labels))}

            # Determine the dominant sentiment
            sentiment, score = self._get_dominant_sentiment(scores_dict)

            return {"sentiment": sentiment, "score": score, "details": scores_dict}

        except Exception as e:
            logger.error(f"Error in analyze_sentiment: {str(e)}")
            # Return neutral sentiment on error
            return {
                "sentiment": "neutral",
                "score": 1.0,
                "details": {"positive": 0.0, "neutral": 1.0, "negative": 0.0},
            }

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for sentiment analysis.

        Args:
            text: Input text to preprocess

        Returns:
            Preprocessed text
        """
        # Remove URLs
        text = re.sub(r"https?://\S+|www\.\S+", "", text)

        # Remove HTML tags
        text = re.sub(r"<.*?>", "", text)

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def _get_dominant_sentiment(self, scores: Dict[str, float]) -> Tuple[str, float]:
        """
        Get the dominant sentiment from scores.

        Args:
            scores: Dictionary of sentiment scores

        Returns:
            Tuple of (sentiment_label, score)
        """
        # Find the sentiment with the highest score
        dominant_sentiment = max(scores.items(), key=lambda x: x[1])
        return dominant_sentiment

    def get_emotion_keywords(self, sentiment: str) -> Dict[str, list]:
        """
        Get emotion-related keywords based on sentiment.

        Args:
            sentiment: The sentiment category (positive, negative, neutral)

        Returns:
            Dictionary of emotion keywords by category
        """
        emotion_keywords = {
            "positive": {
                "joy": ["喜び", "嬉しい", "楽しい", "幸せ", "満足"],
                "excitement": ["興奮", "ワクワク", "熱狂", "感動", "驚き"],
                "gratitude": ["感謝", "ありがとう", "恩", "謝意", "御礼"],
            },
            "negative": {
                "anger": ["怒り", "憤り", "不満", "イライラ", "憎しみ"],
                "sadness": ["悲しみ", "悲しい", "寂しい", "憂鬱", "落ち込む"],
                "fear": ["恐怖", "不安", "心配", "怖い", "恐れ"],
            },
            "neutral": {
                "calm": ["冷静", "平静", "穏やか", "落ち着き", "安定"],
                "contemplative": ["思慮", "考察", "熟考", "内省", "検討"],
            },
        }

        return emotion_keywords.get(sentiment, emotion_keywords["neutral"])
