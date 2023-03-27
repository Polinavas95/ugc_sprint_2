import logging

from clickhouse_driver import Client  # type: ignore
from clickhouse_driver.errors import Error  # type: ignore

from config.backoff import backoff_function
from typing import Any


class ETLClickhouseDriver:
    def __init__(self, host: str, db: str, tables: list[str]):
        self.host = host
        self.db = db
        self.tables = tables
        self.client = self.get_ch_client()

    @backoff_function(Error)
    def get_ch_client(self) -> Client:
        return Client.from_url(self.host)

    def ch_database_init(self) -> None:
        self.client.execute(
            f'CREATE DATABASE IF NOT EXISTS {self.db} ON CLUSTER company_cluster'
        )
        for table in self.tables:
            self.client.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.db}.{table} ON CLUSTER company_cluster
                (timezone String, ip String, user_id UUID, movie_id UUID, event String, viewed_frame Int64, date Date) 
                Engine=MergeTree()
                ORDER BY user_id
                """
            )

    def ch_load(self, data: dict[str, Any]) -> bool:
        for event_type, batch in data.items():
            try:
                self.client.execute(
                    f'INSERT INTO {self.db}.{event_type} VALUES',
                    batch,
                    types_check=True,
                )
            except KeyError as ch_err:
                logging.exception(msg='KeyError', exc_info=ch_err)

        return True
