FROM  python:3.10-slim-buster as builder

LABEL maintainer="mail@ebarsukovl.com"

WORKDIR /app

COPY app .

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

ARG DOCKER=True

CMD ["python", "main.py", "-d"]
