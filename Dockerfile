# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.7-buster

# COPY config and cert files into known locations
COPY requirements.txt /
COPY /repost_bot/. /app/

# RUN provides a way to provision dependencies
RUN apt-get update -y && \
    yes | python -m pip install -U pip && \
    pip3 install -r /requirements.txt

# EXPOSE port to allow communication to/from server
EXPOSE 80

ENTRYPOINT [ "python3", "/app/repost_bot.py", "test" ]