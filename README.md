# Проектная работа 9 спринта

https://github.com/Polinavas95/ugc_sprint_2

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
poetry run make run_api_ugc
```

* Добавьте файл `.env_user_api` и укажите в нём DNS для Sentry, который можно получить в своём аккаунте.

### 3) После этого сервис будет развёрнут.
