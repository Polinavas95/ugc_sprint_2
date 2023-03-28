from random import choice, randint
from typing import Callable
from uuid import uuid4

from faker import Faker

LIKE = 1
DISLIKE = 0
START_DATE = '-30d'
END_DATE = 'now'
fake = Faker()


def fake_like_event(user_id: str = None, movie_id: str = None) -> dict:
    """Генерация события установки лайков"""
    return {
        'user_id': user_id if user_id else str(uuid4()),
        'movie_id': movie_id if movie_id else str(uuid4()),
        'type': choice([LIKE, DISLIKE]),
        'datetime': fake.date_time_between(start_date=START_DATE, end_date=END_DATE),
    }


def fake_review_event(user_id: str = None, movie_id: str = None) -> dict:
    """Генерация события добавления рецензии к фильму"""
    return {
        'user_id': user_id if user_id else str(uuid4()),
        'movie_id': movie_id if movie_id else str(uuid4()),
        'review': fake.text(),
        'rating': randint(0, 10),
        'datetime': fake.date_time_between(start_date=START_DATE, end_date=END_DATE),
    }


def fake_bookmark_event(user_id: str = None, movie_id: str = None) -> dict:
    """Генерация события закладки пользователя"""
    return {
        'user_id': user_id if user_id else str(uuid4()),
        'movie_id': movie_id if movie_id else str(uuid4()),
        'datetime': fake.date_time_between(start_date=START_DATE, end_date=END_DATE),
    }


def fake_batch(event_faker: Callable, user_size: int, batch_size: int) -> list[dict]:
    """Генерация батча событий."""
    users = [str(uuid4()) for _ in range(user_size)]
    return [event_faker(user_id=choice(users)) for _ in range(batch_size)]


def fake_users_batch(event_faker: Callable, users: list, batch_size: int) -> list[dict]:
    """Генерация батча событий с фиксированными юзерами."""
    return [event_faker(user_id=choice(users)) for _ in range(batch_size)]
