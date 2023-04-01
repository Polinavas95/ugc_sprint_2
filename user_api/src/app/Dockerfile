FROM python:3.10

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
# реализация протокола Apache Kafka в библиотеке C,  \
# предоставляющая клиентам Producer, Consumer и Admin
    apk add build-base librdkafka-dev && \
    apk --no-cache add curl && \
    pip install --upgrade pip && \
    pip install -U setuptools

COPY requirements.txt .

RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

EXPOSE 8011

COPY . ./app
