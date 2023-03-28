import time
from typing import Callable
from uuid import uuid4

from pymongo import MongoClient

from config import Settings
from fake_data import (
    fake_batch,
    fake_users_batch,
    fake_like_event,
    fake_review_event,
    fake_bookmark_event,
)

settings = Settings()
print('connect to database...')
client = MongoClient('127.0.0.1', 27017)
mongo_db = client['ugc_db']
print('Success...')


def insert_step(
        faker: Callable,
        collection_name: str,
        batch_size: int,
        iterations: int = settings.ITERATIONS_NUMBER,
) -> None:
    """Тестирование вставки."""
    collection = mongo_db.get_collection(collection_name)
    statistics = []
    for _ in range(iterations):
        batch = fake_batch(faker, settings.USERS_IN_BATCH, batch_size)
        start = time.time()
        collection.insert_many(batch)
        end = time.time()
        statistics.append(end - start)
    mean_batch = sum(statistics) / len(statistics)
    print(
        f'Statistics for {collection_name} batch_size={batch_size}: batch={mean_batch} sec, '
        f'item={mean_batch/batch_size} sec.',
    )


def insert(faker: Callable, collection_name: str) -> None:
    """Тестирование вставки с разным размером батча."""
    batch_sizes = [1, 10, 50, 100, 200, 500, 1000, 2000, 5000]
    for batch_size in batch_sizes:
        insert_step(faker, collection_name, batch_size)


def read_data(faker: Callable, collection_name: str, users_size: int) -> None:
    """Тестирование чтения."""
    statistics = []
    collection = mongo_db.get_collection(collection_name)
    users = [str(uuid4()) for _ in range(users_size)]

    for i in range(0, settings.TEST_RECORDS_SIZE, settings.OPTIMAL_BATCH_SIZE):
        print(i)
        batch = fake_users_batch(faker, users, batch_size=settings.OPTIMAL_BATCH_SIZE)
        collection.insert_many(batch)

    for user in users:
        start = time.time()
        _ = list(collection.find({'user_id': user}))
        statistics.append(time.time() - start)

    mean_batch = sum(statistics) / len(statistics)
    print(
        f'Statistics read for {collection_name} for ~{int(settings.TEST_RECORDS_SIZE/users_size)} records: {mean_batch} sec',
    )


if __name__ == '__main__':
    print('insert def run')
    insert(fake_like_event, settings.MONGO_COLLECTION_LIKE)
    insert(fake_review_event, settings.MONGO_COLLECTION_REVIEW)
    insert(fake_bookmark_event, settings.MONGO_COLLECTION_BOOKMARK)

    print('read def run')
    read_data(fake_like_event, settings.MONGO_COLLECTION_LIKE, 20)
    read_data(fake_review_event, settings.MONGO_COLLECTION_REVIEW, 20)
    read_data(fake_bookmark_event, settings.MONGO_COLLECTION_BOOKMARK, 20)
