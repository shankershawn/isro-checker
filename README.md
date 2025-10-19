# ISRO Mission Checker

## Overview
This project provides tools to check and monitor ISRO (Indian Space Research Organisation) missions using Python and Selenium. It is designed to automate the process of retrieving and verifying mission data, and can be run in a Docker container for consistency and portability.

## Features
- Automated mission data checking using Selenium WebDriver
- Custom logging to avoid duplicate log entries
- Dockerized environment for easy deployment

## Project Structure
```
com/
  __init__.py
  shankarsan/
    __init__.py
    isro/
      __init__.py
      mission-checker.py      # Main script for mission checking
      mission.png             # Project image/logo
      loggers/
        __init__.py
        NoDuplicateLogger.py  # Custom logger implementation
Dockerfile                   # Docker setup for the project
```

## Requirements
- Docker (recommended)
- Python 3.8+
- Firefox (installed in Docker image)
- geckodriver (installed in Docker image)
- Python packages: selenium, redis, schedule, selenium-firefox

## Setup
### Using Docker (Recommended)
1. Build the Docker image:
   ```sh
   docker build -t isro-missions .
   ```
2. Run the Docker container (local build):
   ```sh
   docker run -it isro-missions
   ```
3. Or run the prebuilt image from Docker Hub:
   ```sh
   docker run shankershawn/isro-mission-checker:latest
   ```

### Local Setup (Advanced)
1. Install Python 3.8+ and pip.
2. Install Firefox and geckodriver for your OS.
3. Install dependencies:
   ```sh
   pip install selenium redis schedule selenium-firefox
   ```

## Usage
Run the main mission checker script:
```sh
python com/shankarsan/isro/mission-checker.py
```

## Troubleshooting
- If you see `NoSuchDriverException`, ensure geckodriver and Firefox are installed and in your PATH.
- For Docker, make sure to rebuild the image after any changes to the Dockerfile.
- Run in headless mode if using in a server or CI environment.

## License
MIT License

## Author
Shankarsan Ganai
