FROM python:3.11.9-alpine
RUN mkdir /app
WORKDIR /app
RUN apk add git
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./src/ ./src/
ENTRYPOINT ["/usr/bin/env", "python3", "src/release_version_updater/main.py"]
