#!/bin/bash
# Script to automatically fix linting issues

# Set up colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Installing linting dependencies...${NC}"
pip install -r requirements/requirements-lint.txt

echo -e "${YELLOW}Fixing import sorting with isort...${NC}"
isort .

echo -e "${YELLOW}Formatting code with black...${NC}"
black .

echo -e "${GREEN}Automatic fixes applied!${NC}"
echo -e "${YELLOW}Running linting checks to see remaining issues...${NC}"
echo ""

# Run the linting script to see remaining issues
./run_lint.sh

echo ""
echo -e "${YELLOW}Note: Some issues require manual fixes:${NC}"
echo -e "  - Add missing type annotations (especially return types)"
echo -e "  - Install missing type stubs for libraries"
echo -e "  - Fix unreachable code"
echo -e "  - Fix other mypy issues"
