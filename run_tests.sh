#!/bin/bash
# Script to run tests with coverage reporting

# Set up colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Installing test dependencies...${NC}"
pip install -r requirements/requirements-test.txt

echo -e "${YELLOW}Running tests with coverage...${NC}"
# Run tests with mocked dependencies
python -m pytest --cov=app tests/ "$@"

# Check if the tests passed
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"

    # Generate HTML coverage report
    echo -e "${YELLOW}Generating HTML coverage report...${NC}"
    python -m pytest --cov=app --cov-report=html tests/ > /dev/null 2>&1

    echo -e "${GREEN}Coverage report generated in htmlcov/ directory${NC}"
    echo -e "${YELLOW}Open htmlcov/index.html in your browser to view the report${NC}"
else
    echo -e "${RED}Tests failed!${NC}"
    exit 1
fi

echo -e "${YELLOW}Note: Tests are running with mocked dependencies.${NC}"
echo -e "${YELLOW}This allows testing without installing heavy NLP libraries.${NC}"
echo -e "${YELLOW}For full integration testing with actual models, install all dependencies:${NC}"
echo -e "${YELLOW}pip install -r requirements/requirements.txt${NC}"
