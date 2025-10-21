FROM python:latest

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y firefox-esr

ARG MAINTAINER
ARG REPO
ARG GECKODRIVER_VERSION
ARG ARCH

RUN wget https://github.com/$MAINTAINER/$REPO/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-$ARCH.tar.gz \
    && tar -xvzf geckodriver-$GECKODRIVER_VERSION-$ARCH.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-$GECKODRIVER_VERSION-$ARCH.tar.gz

RUN pip install --upgrade pip
RUN pip install selenium redis schedule selenium-firefox

COPY . .

CMD python com/shankarsan/isro/mission-checker.py
