FROM  python:3.10-slim-buster as builder

WORKDIR /app

COPY app .

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

LABEL maintainer="mail@ebarsukovl.com"


CMD ["python", "main.py", "-d"]
