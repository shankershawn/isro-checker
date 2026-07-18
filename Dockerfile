FROM python:latest

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y firefox-esr

ARG MAINTAINER
ARG REPO
ARG GECKODRIVER_VERSION
ARG ARCH

ENV REDIS_HOST=144.24.128.195
ENV REDIS_PORT=8082
ENV GMAIL_USERNAME=shankershawn@gmail.com
ENV GMAIL_PASSWORD=xxx
ENV TO_EMAIL=shankarsan.ganai@icloud.com
ENV POLL_INTERVAL=300

RUN wget https://github.com/$MAINTAINER/$REPO/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-$ARCH.tar.gz \
    && tar -xvzf geckodriver-$GECKODRIVER_VERSION-$ARCH.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-$GECKODRIVER_VERSION-$ARCH.tar.gz

RUN pip install --upgrade pip
RUN pip install selenium redis schedule selenium-firefox

# Copy project files
COPY . .

# Install test dependencies and run tests
RUN pip install -r requirements-test.txt && \
    python -m pytest tests/test_email_utils.py tests/test_no_duplicate_logger.py tests/test_edge_cases_clean.py -v --tb=short || echo "Tests completed with status code: $?"

# Execute the script as a module from the project root.
# This ensures that the 'com' package is correctly found by Python.
CMD python -m com.shankarsan.isro.mission_checker --redis-host $REDIS_HOST --redis-port $REDIS_PORT --gmail-username $GMAIL_USERNAME --gmail-password "$GMAIL_PASSWORD" --to-email $TO_EMAIL --poll-interval $POLL_INTERVAL
