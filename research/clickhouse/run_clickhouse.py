import time
from typing import Callable
from uuid import uuid4


from research.clickhouse.ch_adapter import settings, ClickhouseAdapter
from research.fake_data import (
    fake_batch,
    fake_users_batch,
    fake_like_event,
    fake_review_event,
    fake_bookmark_event
)

adapter = ClickhouseAdapter(host=settings.CLICKHOUSE_HOST, user=settings.USER_CH, password=settings.PASSWORD_CH)


def init_clickhouse(
        fields: dict[str, str], table: str,
) -> None:
    """Инициализация таблицы в ClickHouse."""
    adapter.create_db(settings.SHARD_DB, cluster=settings.CLICKHOUSE_CLUSTER)
    adapter.create_db(settings.REPLICA_DB, cluster=settings.CLICKHOUSE_CLUSTER)
    adapter.create_table_distributed(
        table_name=table,
        fields=fields,
        partition_by=None,
        order_by='user_id',
    )


def ch_insert_step(
        faker: Callable,
        collection_name: str,
        batch_size: int,
        iterations: int = settings.ITERATIONS_NUMBER,
) -> None:
    """Тестирование вставки."""
    statistics = []
    for _ in range(iterations):
        batch = fake_batch(faker, settings.USERS_IN_BATCH, batch_size)
        start = time.time()
        step_data = []
        str_key = ""
        for value in batch:
            str_key = ", ".join(value.keys())
            step_data.append(tuple(value.values()))
        adapter.execute(f"""INSERT INTO {collection_name} ({str_key}) VALUES""", step_data)
        end = time.time()
        statistics.append(end - start)
    mean_batch = sum(statistics) / len(statistics)
    print(
        f'Statistics for {collection_name} batch_size={batch_size}: batch={mean_batch} sec, '
        f'item={mean_batch / batch_size} sec.',
    )


def ch_insert(faker: Callable, collection_name: str) -> None:
    """Тестирование вставки с разным размером батча."""
    batch_sizes = [1, 10, 50, 100, 200, 500, 1000, 2000, 5000]
    for batch_size in batch_sizes:
        ch_insert_step(faker, collection_name, batch_size)


def ch_read_data(faker: Callable, collection_name: str, users_size: int) -> None:
    """Тестирование чтения."""
    statistics = []
    users = [str(uuid4()) for _ in range(users_size)]

    for _ in range(0, settings.TEST_RECORDS_SIZE, settings.OPTIMAL_BATCH_SIZE):
        batch = fake_users_batch(faker, users, batch_size=settings.OPTIMAL_BATCH_SIZE)
        adapter.execute(f"""INSERT INTO {collection_name} (user_id) VALUES""", batch)

    for user in users:
        start = time.time()
        _ = list(adapter.execute(f'SELECT * FROM {collection_name} WHERE user_id = "{user}"'))
        statistics.append(time.time() - start)

    mean_batch = sum(statistics) / len(statistics)
    print(
        f'Statistics read for {collection_name} for ~{int(settings.TEST_RECORDS_SIZE / users_size)}'
        f' records: {mean_batch} sec',
    )


if __name__ == '__main__':
    # лайки
    init_clickhouse(fields={
        'user_id': 'String',
        'film_id': 'String',
        'type': 'UInt32',
        'datetime': 'DateTime',
    }, table=settings.COLLECTION_LIKE)
    # отзывы
    init_clickhouse(fields={
        'user_id': 'String',
        'film_id': 'String',
        'text': '"String',
        'rating': 'UInt32',
        'datetime': 'DateTime',
    }, table=settings.COLLECTION_REVIEW)
    # закладки
    init_clickhouse(fields={
        'user_id': 'String',
        "film_id": 'String',
        'datetime': 'DateTime',
    }, table=settings.COLLECTION_BOOKMARK)

    ch_insert(fake_like_event, settings.COLLECTION_LIKE)
    ch_insert(fake_review_event, settings.COLLECTION_REVIEW)
    ch_insert(fake_bookmark_event, settings.COLLECTION_BOOKMARK)

    ch_read_data(fake_like_event, settings.COLLECTION_LIKE, 20)
    ch_read_data(fake_review_event, settings.COLLECTION_REVIEW, 20)
    ch_read_data(fake_bookmark_event, settings.COLLECTION_BOOKMARK, 20)
