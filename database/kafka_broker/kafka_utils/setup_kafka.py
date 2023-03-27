from kafka.admin import KafkaAdminClient, NewTopic  # type: ignore
from loguru import logger
import time

from config import get_settings  # type: ignore

if __name__ == '__main__':
    while True:
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=get_settings().kafka_settings.kafka_broker,
            )
            break
        except Exception as e:
            logger.exception('Failed to connect to Kafka: {}', e)
            logger.info('Retrying in 5 seconds...')
            time.sleep(5)
    kafka_name = get_settings().kafka_settings.kafka_topic_name
    if kafka_name not in admin_client.list_topics():
        logger.info('Creating topic: {}', kafka_name)
        topic_list = [
            NewTopic(name=kafka_name, num_partitions=1, replication_factor=1)
        ]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    else:
        logger.info('Topic already exists: {}', kafka_name)
