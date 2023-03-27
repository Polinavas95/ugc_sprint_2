from kafka import KafkaConsumer  # type: ignore
from abc import ABC, abstractmethod
from loguru import logger
import time
from typing import Any, Generator


class UserMovieConsumer(ABC):
    @abstractmethod
    def message_generator(self) -> Generator[Any, None, None]:
        pass


class KafkaUserMovieConsumer(UserMovieConsumer):
    def __init__(self, topic: str, bootstrap_servers: str):
        self.topic = topic
        self.bootstrap_servers = [bootstrap_servers]

    def message_generator(self) -> Generator[Any, None, None]:
        while True:
            try:
                consumer = KafkaConsumer(
                    self.topic,
                    bootstrap_servers=self.bootstrap_servers,
                )
                break
            except Exception as e:
                logger.exception("Failed to connect to Kafka: {}", e)
                logger.info("Retrying in 5 seconds...")
                time.sleep(5)

        for message in consumer:
            yield message
