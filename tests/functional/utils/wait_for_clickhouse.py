import logging
import os

import backoff
import clickhouse_connect


def clickhouse_conn_backoff_hdlr(details):
    logging.info(
        "\t\n ==> Clickhouse connection Error. "
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "Details: {args}".format(**details)
    )


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=clickhouse_connect.driver.exceptions.Error,
    on_backoff=clickhouse_conn_backoff_hdlr,
    max_tries=10,
)
def check_clickhouse_connection():
    clickhouse_host = os.getenv('CLICKHOUSE_HOST', default='localhost')
    client = clickhouse_connect.get_client(host=clickhouse_host, username='default')
    client.ping()


if __name__ == '__main__':
    check_clickhouse_connection()
