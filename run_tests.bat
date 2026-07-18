@echo off
REM Script to run ISRO Mission Checker tests on Windows

setlocal enabledelayedexpansion

echo ================================
echo ISRO Mission Checker Test Suite
echo ================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo Project root: %PROJECT_ROOT%
echo.

REM Change to project root
cd /d %PROJECT_ROOT%

REM Check if requirements are installed
echo Checking dependencies...
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo Installing test dependencies...
    pip install -r requirements-test.txt
)
echo Dependencies OK
echo.

REM Run tests based on argument
if "%1"=="coverage" (
    echo Running tests with coverage report...
    pytest --cov=com --cov-report=html --cov-report=term-missing -v
    echo.
    echo Coverage report generated in htmlcov\index.html
) else if "%1"=="fast" (
    echo Running fast unit tests...
    pytest tests\test_no_duplicate_logger.py tests\test_email_utils.py -v
) else if "%1"=="integration" (
    echo Running integration tests...
    pytest tests\test_integration.py -v
) else if "%1"=="verbose" (
    echo Running all tests with verbose output...
    pytest -vv --tb=long
) else if "%1"=="quiet" (
    echo Running all tests quietly...
    pytest -q
) else if "%1"=="file" (
    if not "%2"=="" (
        echo Running tests in %2...
        pytest "tests\%2" -v
    ) else (
        echo Please specify a test file
        echo Usage: %0 file test_filename.py
    )
) else if "%1"=="marker" (
    if not "%2"=="" (
        echo Running tests marked with '%2'...
        pytest -m %2 -v
    ) else (
        echo Please specify a marker
        echo Usage: %0 marker marker_name
    )
) else (
    echo Running all tests...
    pytest -v
)

echo.
echo Test run completed!
endlocal

