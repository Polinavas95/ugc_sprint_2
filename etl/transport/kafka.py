from kafka import KafkaConsumer  # type: ignore
from kafka.errors import KafkaError  # type: ignore

from config.backoff import backoff_function


class ETLKafkaConsumer:
    def __init__(self, host: list[str], topics: list[str], group_id: str, auto_commit: bool):
        self.host = host
        self.topics = topics
        self.group_id = group_id
        self.auto_commit = auto_commit

    @backoff_function(ConnectionError, KafkaError)
    def get_consumer(self) -> KafkaConsumer:
        return KafkaConsumer(
            *self.topics,
            bootstrap_servers=self.host,
            enable_auto_commit=self.auto_commit,
            group_id=self.group_id,
        )
