#!/bin/bash
# Script to run linting tools

# Set up colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Installing linting dependencies...${NC}"
pip install -r requirements/requirements-lint.txt

# Function to run a command and check its exit status
run_check() {
    local cmd="$1"
    local name="$2"

    echo -e "${YELLOW}Running $name...${NC}"
    eval "$cmd"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}$name passed!${NC}"
        return 0
    else
        echo -e "${RED}$name failed!${NC}"
        return 1
    fi
}

# Track overall success
OVERALL_SUCCESS=0

# Run isort check
run_check "isort --check-only --diff ." "isort"
OVERALL_SUCCESS=$((OVERALL_SUCCESS + $?))

# Run black check
run_check "black --check ." "black"
OVERALL_SUCCESS=$((OVERALL_SUCCESS + $?))

# Run flake8
run_check "flake8 ." "flake8"
OVERALL_SUCCESS=$((OVERALL_SUCCESS + $?))

# Run mypy
run_check "mypy app" "mypy"
OVERALL_SUCCESS=$((OVERALL_SUCCESS + $?))

# Print summary
echo ""
if [ $OVERALL_SUCCESS -eq 0 ]; then
    echo -e "${GREEN}All linting checks passed!${NC}"
else
    echo -e "${RED}Some linting checks failed!${NC}"
    echo -e "${YELLOW}Fix the issues and run the script again.${NC}"

    # Provide help for fixing issues
    echo -e "\n${YELLOW}To automatically fix some issues:${NC}"
    echo -e "  - Run ${GREEN}isort .${NC} to sort imports"
    echo -e "  - Run ${GREEN}black .${NC} to format code"
    echo -e "  - For flake8 and mypy issues, you'll need to fix them manually"
fi

exit $OVERALL_SUCCESS
