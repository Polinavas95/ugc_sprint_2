FROM python:3.10-alpine

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
COPY --from=uwsgi-builder /root/wheels /root/wheels

RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

COPY . .

RUN rm -rf /root/wheels
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]