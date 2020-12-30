FROM python:3.8-buster

RUN \
    apt-get update && \
    apt-get install -y binutils libproj-dev && \
    rm -rf /var/lib/apt/lists/*

ENV WORKON_HOME /opt/venvs/pnia

WORKDIR /source

EXPOSE 8000