import click
import pandas as pd

from fetch import load
from format_data import format_data

USDT: float = 1000.0
BTC: float = 0.0


def is_sma200_greater_sma600(data_frame: pd.DataFrame, index: int) -> bool:
    return bool(data_frame['SMA200'][index] > data_frame['SMA600'][index])


def format_btc_action(action: str, data_frame: pd.DataFrame, index: int) -> str:
    return f"{index}: {action} BTC at {data_frame['close'][index]}$"


def compute(data_frame: pd.DataFrame, initial_usdt: float, initial_btc: float) -> float:
    usdt = initial_usdt
    btc = initial_btc
    last_index = data_frame.first_valid_index()

    for index, _ in data_frame.iterrows():

        if is_sma200_greater_sma600(data_frame, last_index) and USDT > 10:
            btc = usdt / data_frame['close'][index]
            btc = btc - 0.0007 * btc
            usdt = 0
            action = format_btc_action('Buy', data_frame, index)
            color = 'green'

        # simplified sma200 < sma600 by using elif
        elif btc > 0.0001:
            usdt = btc * data_frame['close'][index]
            usdt = usdt - 0.0007 * usdt
            btc = 0
            action = format_btc_action('Sell', data_frame, index)
            color = 'red'

        else:
            action = format_btc_action('Do nothing with', data_frame, index)
            color = 'yellow'

        click.secho(action, fg=color)
        last_index = index

    return float(usdt + btc * data_frame['close'].iloc[-1])


if __name__ == '__main__':
    data_frame = load()
    data_frame = format_data(data_frame)

    usdt_value = compute(data_frame, USDT, BTC)
    usdt_buy_and_hold = data_frame['close'].iloc[-1] / data_frame['close'].iloc[0] * 1000

    print('Final results:')
    print(f'{usdt_value=} USDT')
    print(f'{usdt_buy_and_hold=} USDT')
