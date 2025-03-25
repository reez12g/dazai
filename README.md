# Dazai API

API for predictive text generation using GPT-2.

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
│   └── tasks.py            # Task management endpoints
├── services/               # Business logic
│   ├── __init__.py
│   ├── cliche_service.py   # Literary cliche service
│   ├── nlp_service.py      # NLP text generation service
│   └── task_service.py     # Google Cloud Tasks service
└── utils/                  # Utility functions
    ├── __init__.py
    ├── exceptions.py       # Custom exception classes
    ├── logging.py          # Logging configuration
    └── middleware.py       # FastAPI middleware
```

## Key Improvements

1. **Modular Structure**: Code is organized into logical modules with clear responsibilities.
2. **Dependency Injection**: FastAPI's dependency injection system is used for services.
3. **Centralized Configuration**: All settings are managed in one place using Pydantic.
4. **Improved Error Handling**: Custom exceptions and middleware for consistent error responses.
5. **Better Logging**: Centralized logging configuration.
6. **Type Hints**: Consistent type annotations throughout the codebase.
7. **Documentation**: Improved docstrings and comments.

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
