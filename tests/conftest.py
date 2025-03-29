"""
Shared pytest fixtures for the Dazai API tests.

This module contains fixtures that can be used across different test modules.
"""
import pytest
from unittest.mock import MagicMock, patch

# Mock external modules before importing services
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
mock_config.nlp_settings = mock_nlp_settings
sys.modules['app.config'] = mock_config

# Now import services
from app.services.style_transfer_service import StyleTransferService
from app.services.summarization_service import SummarizationService
from app.services.sentiment_service import SentimentService


@pytest.fixture
def mock_t5_tokenizer():
    """Mock T5Tokenizer for testing."""
    mock = MagicMock()
    mock.return_value = {"input_ids": MagicMock()}
    mock.decode.return_value = "Mocked decoded text"
    return mock


@pytest.fixture
def mock_t5_model():
    """Mock T5ForConditionalGeneration for testing."""
    mock = MagicMock()
    mock.generate.return_value = [MagicMock()]
    return mock


@pytest.fixture
def mock_bert_tokenizer():
    """Mock BERT tokenizer for testing."""
    mock = MagicMock()
    mock.return_value = {"input_ids": MagicMock(), "attention_mask": MagicMock()}
    return mock


@pytest.fixture
def mock_bert_model():
    """Mock BERT model for testing."""
    mock = MagicMock()
    mock.return_value = MagicMock(logits=MagicMock())
    return mock


@pytest.fixture
def style_transfer_service(mock_t5_tokenizer, mock_t5_model):
    """Fixture for StyleTransferService with mocked dependencies."""
    with patch('app.services.style_transfer_service.T5Tokenizer') as mock_tokenizer_cls, \
         patch('app.services.style_transfer_service.T5ForConditionalGeneration') as mock_model_cls, \
         patch('app.services.style_transfer_service.torch'):
        
        mock_tokenizer_cls.from_pretrained.return_value = mock_t5_tokenizer
        mock_model_cls.from_pretrained.return_value = mock_t5_model
        
        service = StyleTransferService()
        service._tokenizer = mock_t5_tokenizer
        service._model = mock_t5_model
        
        return service


@pytest.fixture
def summarization_service(mock_t5_tokenizer, mock_t5_model):
    """Fixture for SummarizationService with mocked dependencies."""
    with patch('app.services.summarization_service.T5Tokenizer') as mock_tokenizer_cls, \
         patch('app.services.summarization_service.T5ForConditionalGeneration') as mock_model_cls, \
         patch('app.services.summarization_service.torch'):
        
        mock_tokenizer_cls.from_pretrained.return_value = mock_t5_tokenizer
        mock_model_cls.from_pretrained.return_value = mock_t5_model
        
        service = SummarizationService()
        service._tokenizer = mock_t5_tokenizer
        service._model = mock_t5_model
        
        return service


@pytest.fixture
def sentiment_service(mock_bert_tokenizer, mock_bert_model):
    """Fixture for SentimentService with mocked dependencies."""
    with patch('app.services.sentiment_service.AutoTokenizer') as mock_tokenizer_cls, \
         patch('app.services.sentiment_service.AutoModelForSequenceClassification') as mock_model_cls, \
         patch('app.services.sentiment_service.torch'):
        
        mock_tokenizer_cls.from_pretrained.return_value = mock_bert_tokenizer
        mock_model_cls.from_pretrained.return_value = mock_bert_model
        
        # Create a mock for torch.nn.functional.softmax
        mock_softmax = MagicMock()
        mock_softmax.return_value = MagicMock()
        mock_softmax.return_value.__getitem__.return_value = [0.1, 0.2, 0.7]
        
        with patch('app.services.sentiment_service.torch.nn.functional.softmax', mock_softmax):
            service = SentimentService()
            service._tokenizer = mock_bert_tokenizer
            service._model = mock_bert_model
            
            return service


@pytest.fixture
def sample_japanese_text():
    """Sample Japanese text for testing."""
    return "これは日本語のサンプルテキストです。テストに使用されます。"


@pytest.fixture
def sample_long_japanese_text():
    """Sample long Japanese text for testing summarization."""
    return """
    これは日本語の長いサンプルテキストです。要約のテストに使用されます。
    この文章は十分に長くする必要があります。そうでなければ、要約サービスは
    テキストが短すぎると判断して、元のテキストをそのまま返す可能性があります。
    したがって、この文章にはいくつかの段落と、さまざまな情報が含まれています。
    
    日本の文学は世界的に有名です。夏目漱石、芥川龍之介、川端康成、三島由紀夫、
    村上春樹など、多くの著名な作家がいます。彼らの作品は、日本の文化、社会、
    歴史を反映しています。
    
    日本の四季は鮮明で、それぞれ独自の美しさがあります。春には桜が咲き、
    夏には蝉の声が響き、秋には紅葉が山々を彩り、冬には雪が静かに降り積もります。
    この四季の変化は、日本の文化や芸術に大きな影響を与えてきました。
    """
