# ISRO Mission Checker

## Overview
ISRO Mission Checker is a Python-based automation tool for monitoring and verifying Indian Space Research Organisation (ISRO) missions. It leverages Selenium WebDriver for browser automation and includes custom logging and utility modules. The project is fully containerized for easy deployment on both x86_64 and ARM (Raspberry Pi) platforms.

## Features
- Automated mission data retrieval and verification using Selenium
- Custom logger to prevent duplicate log entries
- Email utility for notifications
- Dockerized for consistent, cross-platform deployment

## Project Structure
```
Dockerfile
README.md
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
      util/
        __init__.py
        EmailUtils.py         # Utilities for email notifications
```

## Requirements
- Docker (recommended)
- Python 3.8+
- Firefox (installed in Docker image)
- geckodriver (installed in Docker image)
- Python packages: selenium, redis, schedule, selenium-firefox

## Setup
### Using Docker (Recommended)
#### For Raspberry Pi/ARM:
```sh
docker build --build-arg "MAINTAINER=jamesmortensen" --build-arg "REPO=geckodriver-arm-binaries" --build-arg "GECKODRIVER_VERSION=v0.34.0" --build-arg "ARCH=linux-armv7l" -t shankershawn/isro-mission-checker:linux-armv7l .
docker run -it shankershawn/isro-mission-checker:linux-armv7l
```
#### For Linux x86_64:
```sh
docker build --build-arg "MAINTAINER=mozilla" --build-arg "REPO=geckodriver" --build-arg "GECKODRIVER_VERSION=v0.34.0" --build-arg "ARCH=linux64" -t shankershawn/isro-mission-checker:linux64 .
docker run -it shankershawn/isro-mission-checker:linux64
```
#### Or run the prebuilt image from Docker Hub:
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
- Check logs for details (custom logger prevents duplicate entries).

## License
MIT License

## Author
Shankarsan Ganai
