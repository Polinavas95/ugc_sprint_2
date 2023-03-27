import time
from clickhouse_driver import Client  # type: ignore
from clickhouse_driver.errors import Error  # type: ignore


# Подключение к БД
from loguru import logger


def connection() -> Client:
    while True:
        try:
            click_client = Client(host="clickhouse-node1")
            return click_client
        except Error as e:
            logger.error(e)
            logger.info("Just trying to connect...")
            time.sleep(1)


# Инициализация кластера
def init_cluster(click_client: Client) -> None:
    # Создание базы
    # Кластер company_cluster описан в конфигурациях нод 1-4 в папке data
    click_client.execute(
        "CREATE DATABASE IF NOT EXISTS analysis ON CLUSTER company_cluster"
    )
    # Создание дистрибутивной реплицированной таблицы (с 4 шардами)
    # с названием БД analysis, таблицей data_analysis_repl
    # Из-за rand() строка данных будет отправлена на случайный шард
    click_client.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis.data_analysis ON CLUSTER company_cluster 
        (id Int64, user_id Int32, movie_id Int32, event String, viewed_frame Int64, date Date) 
        ENGINE = Distributed('company_cluster', analysis, data_analysis_repl, rand());
        """
    )


if __name__ == "__main__":
    logger.info("Connect to clickhouse...")
    client = connection()
    logger.info("Init cluster...")
    init_cluster(client)
    logger.info("Success init")
