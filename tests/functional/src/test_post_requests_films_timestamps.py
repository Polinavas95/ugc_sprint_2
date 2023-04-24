from http import HTTPStatus
from requests import post, get
import time

from functional.settings import get_settings

test_url = f'{get_settings().service_url}/api/v1/movies/event'


def test_success_get_request():
    """
    Сервис UGC должен возвращать статус 200 при успешной передаче времени просмотра фильма.
    """
    response = get(url=test_url)

    assert response.status_code == HTTPStatus.OK


def test_success_send_1000_rows_to_kafka(clickhouse_client):
    """
    вставка total_insert строк и проверка того, что все 1к строк попали в ClickHouse.
    """
    total_insert = 100

    query = f'SELECT COUNT(*) as count FROM {get_settings.click_db}.{get_settings.click_table}'

    start_count_rows = clickhouse_client.query(query).first_item.get('count')

    for i in range(1, total_insert):
        data = {
            'movie_id': 'test_film_id',
            'user_id': 'test_user_id',
            'event': str(i),
            'viewed_frame': '123',
            'date': 'date',
            'timezone': 'UTC'
        }
        post(url=test_url, json=data)

    # sleep before data gets to clickhouse table
    time.sleep(10)
    count_rows_after_insert = clickhouse_client.query(query).first_item.get('count')

    assert (count_rows_after_insert - start_count_rows) == total_insert


def test_invalid_json_body_send_to_kafka():
    """
    Сервис UGC должен возвращать ошибку 422 при передаче некорректного тела запроса.
    """
    test_incorrect_data = {"film_id": "id3", "user_id": "id2", "incorrect_field": 1}
    response = post(url=test_url, json=test_incorrect_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
