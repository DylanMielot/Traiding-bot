import os
import pickle

import click
import pandas as pd
from binance.client import Client

FILE = 'data.bin'

COLUMNS = [
    'timestamp',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'close_time',
    'quote_av',
    'trades',
    'tb_base_av',
    'tb_quote_av',
    'ignore'
]


def fetch() -> pd.DataFrame:
    return pd.DataFrame(
        Client().get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "01 January 2020"),
        columns=COLUMNS
    )


def save(data_frame: pd.DataFrame) -> None:
    with open(FILE, mode='wb') as file:
        pickle.dump(data_frame, file)


def load() -> pd.DataFrame:
    with open(FILE, mode='rb') as file:
        return pickle.load(file)


if __name__ == '__main__':
    if os.path.exists(FILE) and not click.confirm(f'File "{FILE}" exists. Overwrite ?'):
        exit(0)
    else:
        print('Fetching data...')
        data = fetch()
        print('Fetch ok. Save.')
        save(data)
        print('Save successfull.')
