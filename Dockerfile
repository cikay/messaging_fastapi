# syntax=docker/dockerfile:1

FROM python:3.8-slim

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt requirements.txt

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--reload"]
