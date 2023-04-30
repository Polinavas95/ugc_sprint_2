import datetime
import uuid
from http import HTTPStatus

import pytest
import requests

BASE_URL = "http://localhost:8011"
token = "my_bearer_token"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
query = {
    'movie_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
    'review_id': '3fa85f64-5717-4562-b3fc-2c963f66afa9',
    'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa4',
    'created': '2000-02-03 05:35:02',
    'text': 'text',
    'like_by': ['3fa85f64-5717-4562-b3fc-2c963f66afa6', '3fa85f74-5717-4562-b3dc-2c963k66afa7'],
    'dislike_by': ['3fa85f64-5717-4562-b3fc-2c963f66afa6', '3fa85f74-5717-4562-b3dc-2c963k66afa7'],
    'rating': 4.3,
}
movie_id = uuid.uuid4()


def test_add_review_assert_error():
    text = 'text'
    url = f"{BASE_URL}/api/v1/review/{movie_id}/?text={text}"
    response = requests.post(url, headers=headers)
    assert response.json()['movie_id'] == str(movie_id)
    assert response.json()['text'] == text


def test_add_like():
    url = BASE_URL
    review_id = "98b2d06e-6f31-4428-8ab9-b31a319921d6"
    print(f"{url}/api/v1/review/like/?review_id={review_id}")
    response = requests.post(f"{url}/api/v1/review/like/{review_id}/?movie_id={movie_id}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"like_by": [{"user_id": 1}]}


def test_add_dislike():
    url = BASE_URL
    review_id = "98b2d06e-6f31-4428-8ab9-b31a319921d6"
    response = requests.post(f"{url}/api/v1/review/dislike/{review_id}/?movie_id={movie_id}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"dislike_by": [{"user_id": 1}]}
