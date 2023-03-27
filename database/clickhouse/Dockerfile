# Скачивание образа locust для мониторинга работы БД
FROM python:3.10

WORKDIR /clickhouse

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt


COPY . .

CMD python -m init_database