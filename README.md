# Dazai API

API for Japanese text generation and analysis using NLP models.

## Project Structure

The project has been refactored to follow a more modular and maintainable structure:

```
app/
├── __init__.py
├── main.py                 # Application entry point
├── config.py               # Centralized configuration
├── models/                 # Data models
│   ├── __init__.py
│   └── schemas.py          # Pydantic models for requests/responses
├── routers/                # API endpoints
│   ├── __init__.py
│   ├── general.py          # General endpoints
│   ├── generation.py       # Text generation endpoints
│   ├── tasks.py            # Task management endpoints
│   ├── style_transfer.py   # Text style transformation endpoints
│   ├── summarization.py    # Text summarization endpoints
│   └── sentiment.py        # Sentiment analysis endpoints
├── services/               # Business logic
│   ├── __init__.py
│   ├── cliche_service.py   # Literary cliche service
│   ├── nlp_service.py      # NLP text generation service
│   ├── task_service.py     # Google Cloud Tasks service
│   ├── style_transfer_service.py  # Text style transformation service
│   ├── summarization_service.py   # Text summarization service
│   └── sentiment_service.py       # Sentiment analysis service
└── utils/                  # Utility functions
    ├── __init__.py
    ├── exceptions.py       # Custom exception classes
    ├── logging.py          # Logging configuration
    └── middleware.py       # FastAPI middleware
```

## Features

1. **Predictive Text Generation**: Generate Japanese text using the rinna/japanese-gpt2-small model.
2. **Text Style Transfer**: Transform text into different literary styles (Meiji era, formal, casual, etc.).
3. **Text Summarization**: Create concise summaries of longer Japanese texts.
4. **Sentiment Analysis**: Analyze the sentiment and emotional tone of Japanese text.
5. **Task Management**: Asynchronous processing with Google Cloud Tasks.
6. **Literary Cliches**: Generate literary cliches in Japanese.

## Key Improvements

1. **Modular Structure**: Code is organized into logical modules with clear responsibilities.
2. **Dependency Injection**: FastAPI's dependency injection system is used for services.
3. **Centralized Configuration**: All settings are managed in one place using Pydantic.
4. **Improved Error Handling**: Custom exceptions and middleware for consistent error responses.
5. **Better Logging**: Centralized logging configuration.
6. **Type Hints**: Consistent type annotations throughout the codebase.
7. **Documentation**: Improved docstrings and comments.
8. **Multiple NLP Models**: Support for various pre-trained models for different NLP tasks.

## Code Quality

The project uses several linting and code quality tools to maintain high code standards.

### Linting Tools

- **flake8**: Checks for PEP 8 compliance and common programming errors
- **black**: Enforces a consistent code style
- **isort**: Sorts imports according to conventions
- **mypy**: Performs static type checking

### Running Linters

```bash
# Install linting dependencies
pip install -r requirements/requirements-lint.txt

# Run all linting checks
./run_lint.sh

# Automatically fix formatting and import issues
./fix_lint.sh

# Run individual linters
black .           # Format code with black
isort .           # Sort imports
flake8 .          # Check code style with flake8
mypy app          # Run type checking
```

### Linting with Tests

You can also run linting checks before running tests:

```bash
./run_tests.sh --lint
```

For detailed information about the linting setup and how to fix common issues, see [LINTING.md](LINTING.md).

## Testing

The project includes a comprehensive test suite for unit and integration testing.

### Test Structure

```
tests/
├── conftest.py            # Shared pytest fixtures
├── README.md              # Testing documentation
├── unit/                  # Unit tests
│   ├── test_services/     # Service layer tests
│   ├── test_routers/      # API endpoint tests
│   └── test_models/       # Data model tests
└── integration/           # Integration tests
```

### Running Tests

```bash
# Install test dependencies
pip install -r requirements/requirements-test.txt

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app tests/

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Use the test script (generates HTML coverage report)
./run_tests.sh
```

## Running the Application

### Local Development

```bash
# Install dependencies
pip install -r requirements/requirements.txt

# Run the application
uvicorn app.main:app --reload
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## Environment Variables

The application uses the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| APP_TITLE | Application title | "Dazai API" |
| APP_DESCRIPTION | Application description | "API for predictive text generation using GPT-2" |
| APP_VERSION | Application version | "1.0.0" |
| CORS_ORIGINS | Allowed CORS origins | ["http://localhost", "http://localhost:8080", "http://127.0.0.1:8080"] |
| MODEL_NAME | NLP model name | "rinna/japanese-gpt2-small" |
| MAX_ADDITIONAL_TOKENS | Maximum tokens to generate | 80 |
| DO_SAMPLE | Whether to use sampling for generation | true |
| PROJECT_ID | Google Cloud project ID | None |
| QUEUE_ID | Google Cloud Tasks queue ID | None |
| LOCATION_ID | Google Cloud Tasks location ID | None |
| TASK_URL | URL for task processing | "http://localhost:8080" |
| SERVICE_ACCOUNT_EMAIL | Google Cloud service account email | None |
| AUDIENCE | Audience for OIDC token | "http://localhost:8080" |

## Models Used

- **Text Generation**: rinna/japanese-gpt2-small
- **Style Transfer**: sonoisa/t5-base-japanese
- **Summarization**: sonoisa/t5-base-japanese-summarize
- **Sentiment Analysis**: daigo/bert-base-japanese-sentiment
