# Проектная работа 9 спринта

## Запуск проекта
Для запуска нужно:

### 1) Установить poetry 
```
pip install poetry
```

### 2) Последовательно развернуть сервисы через `make`:
Разворачивать обязательно в указанном порядке:
```
poetry run make run_kafka
poetry run make run_clickhouse
poetry run make run_elk
poetry run make run_user_api
```

* Добавьте файл `.env_user_api` и укажите в нём DNS для Sentry, который можно получить в своём аккаунте.

### 3) После этого сервис будет развёрнут.