#!/bin/bash
# Script to run ISRO Mission Checker tests

set -e

echo "================================"
echo "ISRO Mission Checker Test Suite"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Project root: $PROJECT_ROOT"
echo ""

# Change to project root
cd "$PROJECT_ROOT"

# Check if requirements are installed
echo -e "${BLUE}Checking dependencies...${NC}"
if ! python -c "import pytest" 2>/dev/null; then
    echo "Installing test dependencies..."
    pip install -r requirements-test.txt
fi
echo -e "${GREEN}Dependencies OK${NC}"
echo ""

# Run tests based on argument
if [ "$1" = "coverage" ]; then
    echo -e "${BLUE}Running tests with coverage report...${NC}"
    pytest --cov=com --cov-report=html --cov-report=term-missing -v
    echo ""
    echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"

elif [ "$1" = "fast" ]; then
    echo -e "${BLUE}Running fast unit tests...${NC}"
    pytest tests/test_no_duplicate_logger.py tests/test_email_utils.py -v

elif [ "$1" = "integration" ]; then
    echo -e "${BLUE}Running integration tests...${NC}"
    pytest tests/test_integration.py -v

elif [ "$1" = "verbose" ]; then
    echo -e "${BLUE}Running all tests with verbose output...${NC}"
    pytest -vv --tb=long

elif [ "$1" = "quiet" ]; then
    echo -e "${BLUE}Running all tests quietly...${NC}"
    pytest -q

elif [ "$1" = "file" ] && [ ! -z "$2" ]; then
    echo -e "${BLUE}Running tests in $2...${NC}"
    pytest "tests/$2" -v

elif [ "$1" = "marker" ] && [ ! -z "$2" ]; then
    echo -e "${BLUE}Running tests marked with '$2'...${NC}"
    pytest -m "$2" -v

else
    echo -e "${BLUE}Running all tests...${NC}"
    pytest -v
fi

echo ""
echo -e "${GREEN}Test run completed!${NC}"

