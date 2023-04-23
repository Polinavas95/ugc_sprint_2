FROM python:3.10-alpine

WORKDIR /etl_ugc

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ['python', 'app.py']