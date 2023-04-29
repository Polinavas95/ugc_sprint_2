import requests


def test_get_reviews():
    url = "http://localhost:8000/reviews"
    movie_id = "a9a36a44-1f11-4eaa-89a1-566fbf94dc6c"
    response = requests.get(f"{url}/{movie_id}")
    assert response.status_code == 200
    assert len(response.json()) >= 0


def test_add_review():
    url = "http://localhost:8000/reviews"
    movie_id = "a9a36a44-1f11-4eaa-89a1-566fbf94dc6c"
    text = "Test review"
    response = requests.post(f"{url}/{movie_id}", json={"text": text})
    assert response.status_code == 200
    assert response.json()["text"] == text


def test_add_like():
    url = "http://localhost:8000/reviews"
    review_id = "98b2d06e-6f31-4428-8ab9-b31a319921d6"
    response = requests.post(f"{url}/like/{review_id}")
    assert response.status_code == 200
    assert response.json().keys() == {"like_by"}


def test_add_dislike():
    url = "http://localhost:8000/reviews"
    review_id = "98b2d06e-6f31-4428-8ab9-b31a319921d6"
    response = requests.post(f"{url}/dislike/{review_id}")
    assert response.status_code == 200
    assert response.json().keys() == {"dislike_by"}
