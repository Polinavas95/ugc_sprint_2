from database.kafka_broker.kafka_consumer import KafkaUserMovieConsumer
from loguru import logger

consumer = KafkaUserMovieConsumer(
    topic="user_movie",
    bootstrap_servers="localhost:29092",
)

for message in consumer.message_generator():
    logger.info("Received message: {}", message)
