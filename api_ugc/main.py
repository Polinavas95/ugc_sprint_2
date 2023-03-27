from config.config import get_settings
from utils.kafka_producer import KafkaUserMovieProducer  # type: ignore
from fastapi import FastAPI

settings = get_settings()
app = FastAPI()
producer = KafkaUserMovieProducer(
    topic=settings.kafka_settings.kafka_topic_name,
    bootstrap_servers=settings.kafka_settings.kafka_broker,
)
