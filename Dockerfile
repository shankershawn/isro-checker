FROM python:latest

RUN apt-get update && apt-get install -y firefox-esr

# Download geckodriver for x86_64 (linux64 bundle)
RUN GECKODRIVER_VERSION=v0.33.0 \
    && wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz \
    && tar -xvzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

RUN pip install --upgrade pip
RUN pip install selenium redis schedule selenium-firefox

COPY . .

CMD python com/shankarsan/isro/mission-checker.py