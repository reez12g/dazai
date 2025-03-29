# Dazai API Linting Guide

This document provides information about the linting setup for the Dazai API project and guidance on how to fix common linting issues.

## Linting Tools

The project uses the following linting tools:

1. **flake8**: Checks for PEP 8 compliance and common programming errors
2. **black**: Enforces a consistent code style
3. **isort**: Sorts imports according to conventions
4. **mypy**: Performs static type checking

## Running Linters

You can run all linters at once using:

```bash
./run_lint.sh
```

To automatically fix formatting and import issues:

```bash
./fix_lint.sh
```

You can also run linting checks before running tests:

```bash
./run_tests.sh --lint
```

## Configuration Files

- `.flake8`: Configuration for flake8
- `pyproject.toml`: Configuration for black and isort
- `mypy.ini`: Configuration for mypy

## Common Issues and How to Fix Them

### Import Sorting (isort)

Import sorting issues can be automatically fixed by running:

```bash
isort .
```

The import order should be:

1. Standard library imports
2. Third-party imports
3. Local application imports

Each group should be separated by a blank line.

### Code Formatting (black)

Code formatting issues can be automatically fixed by running:

```bash
black .
```

Black enforces a consistent code style, including:

- Line length of 100 characters
- Consistent use of quotes
- Consistent spacing
- Consistent formatting of data structures

### Type Annotations (mypy)

Type annotation issues require manual fixes. Common issues include:

1. **Missing return type annotations**:

   ```python
   # Incorrect
   def get_data():
       return {"key": "value"}
       
   # Correct
   def get_data() -> dict[str, str]:
       return {"key": "value"}
   ```

2. **Missing parameter type annotations**:

   ```python
   # Incorrect
   def process_text(text):
       return text.upper()
       
   # Correct
   def process_text(text: str) -> str:
       return text.upper()
   ```

3. **Optional parameters**:

   ```python
   # Incorrect
   def generate_text(prompt, max_length=100):
       pass
       
   # Correct
   def generate_text(prompt: str, max_length: int = 100) -> str:
       pass
   ```

4. **Missing library stubs**:

   For third-party libraries without type stubs, you can install them:

   ```bash
   pip install types-requests
   pip install types-google-cloud-ndb
   ```

   Or add type ignores for specific imports:

   ```python
   import some_module  # type: ignore
   ```

### Code Style (flake8)

Common flake8 issues include:

1. **Line length**: Keep lines under 100 characters
2. **Unused imports**: Remove imports that aren't used
3. **Undefined names**: Fix variable names that aren't defined
4. **Docstring issues**: Add or fix docstrings according to Google style

## Gradual Improvement

You don't need to fix all linting issues at once. Consider:

1. First, run `./fix_lint.sh` to automatically fix formatting and import issues
2. Focus on fixing type annotations in new code
3. Gradually add type annotations to existing code
4. Address flake8 issues as you work on files

## CI/CD Integration

Consider adding linting checks to your CI/CD pipeline to ensure code quality:

```yaml
# Example GitHub Actions workflow step
- name: Run linting
  run: |
    pip install -r requirements/requirements-lint.txt
    ./run_lint.sh
```

## IDE Integration

Most modern IDEs support these linting tools:

- **VS Code**: Install the Python, Pylance, and Black Formatter extensions
- **PyCharm**: Enable flake8, black, isort, and mypy in settings
- **Vim/Neovim**: Use ALE or similar plugins

Configure your IDE to run these tools on save for the best development experience.
