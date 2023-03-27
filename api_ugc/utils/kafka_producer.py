import time
from abc import ABC, abstractmethod
from datetime import datetime
from random import choice
from uuid import uuid4

from fastapi import Security
from kafka import KafkaProducer  # type: ignore
from loguru import logger

from models.event import EventForUGS, orjson_dumps, EventView
from utils.auth import auth


class UserMovieProducer(ABC):
    @abstractmethod
    def send_generated_event(self) -> None:
        pass


class KafkaUserMovieProducer(UserMovieProducer):
    def __init__(self, topic: str, bootstrap_servers: str):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers

        while True:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=self.bootstrap_servers,
                )
                break
            except Exception as e:
                logger.exception("Failed to connect to Kafka: {}", e)
                logger.info("Retrying in 5 seconds...")
                time.sleep(5)

    def send_generated_event(self) -> EventForUGS:
        event_raw = self.generate_event(
            event=self.generate_event_type(),
            viewed_frame=int(datetime.now().timestamp()),
            ip="123.123.123.123",
        )
        event = event_raw.dict()
        user_id = event["event_view"]["user_id"]
        movie_id = event["event_view"]["movie_id"]
        event_string = orjson_dumps(event, default={})

        logger.info(
            "Sending message to Kafka. Topic: {}, Value: {}", self.topic, event_string
        )
        self.producer.send(
            topic=self.topic,
            value=event_string.encode(),
            key=f"{user_id}+{movie_id}".encode(),
        )
        logger.info("Message sent to Kafka")
        return event_raw

    def generate_event_type(self) -> str:
        return choice(["opened", "closed", "paused", "resumed"])

    def generate_event(
        self,
        event: str,
        viewed_frame: int,
        ip: str,
    ) -> EventForUGS:
        return EventForUGS(
            event_view=EventView(
                movie_id=uuid4(),
                user_id=Security(auth),
                event=event,
                viewed_frame=viewed_frame,
                date=datetime.now(),
                timezone="UTC",
            ),
            ip=ip,
            event_type="movie_watch_history",
            timezone="UTC",
        )
