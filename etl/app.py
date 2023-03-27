import json
import time

from clickhouse_driver.errors import Error  # type: ignore
from kafka import KafkaConsumer  # type: ignore
from kafka.errors import KafkaError  # type: ignore

from config.backoff import backoff_function, logger
from config.settings import get_settings
from transport.ch import ETLClickhouseDriver
from transport.kafka import ETLKafkaConsumer
from transport.transform import transform, order_batches
from typing import Any

settings = get_settings()


@backoff_function(ConnectionError)
def connect_ch() -> ETLClickhouseDriver:
    return ETLClickhouseDriver(**settings.ch_settings.dict())


@backoff_function(ConnectionError)
def connect_kafka() -> KafkaConsumer:
    return ETLKafkaConsumer(**settings.kafka_settings.dict()).get_consumer()


def run(
    kafka_consumer: KafkaConsumer, driver: ETLClickhouseDriver, batch_size: int = 100
) -> None:
    batches_backup: list[tuple[str, dict[str, Any]]] = []
    batches: list[tuple[str, dict[str, Any]]] = []
    driver.ch_database_init()
    while True:
        try:
            batches = batches_backup
            batches = []
            flush_start = time.time()
            while len(batches) < batch_size:
                for msg in kafka_consumer:
                    logger.info("Got message from Kafka")
                    value = json.loads(msg.value)
                    batches.append(transform(value))
                    # Если длина партии < 1000 или прошло больше 29 секунд
                    if len(batches) >= 1000 or (time.time() - flush_start) > 29:
                        # Попытка загрузки в ClickHouse
                        logger.info("Uploading batch to clickhouse...")
                        result = driver.ch_load(order_batches(batches))
                        if not result:
                            continue
                        # Отдельная фиксация каждого смещения
                        else:
                            kafka_consumer.commit()
                            logger.info("Batch uploaded to clickhouse")

                        batches = []
                        flush_start = time.time()

        except KafkaError as kafka_error:
            logger.error("Got Kafka error: {0}".format(kafka_error))

        except Error as ch_error:
            logger.error("Got ClickHouse error: {0}".format(ch_error))
        finally:
            batches_backup = batches
            logger.info("Stop to transport data")


if __name__ == "__main__":
    logger.info("Start to transport data")
    logger.info("Connect to Kafka")
    consumer = connect_kafka()
    logger.info("Connect to ClickHouse")
    ch_driver = connect_ch()
    logger.info("Databases start to work")
    run(consumer, ch_driver, batch_size=settings.app.batch_size)
    logger.info("Finished loading")
