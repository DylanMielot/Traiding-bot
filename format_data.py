import pandas as pd
import ta


def format_data(data_frame: pd.DataFrame) -> pd.DataFrame:
    # set index column
    data_frame = data_frame.set_index(data_frame['timestamp'])
    data_frame.index = pd.to_datetime(data_frame.index, unit='ms')

    # format to numeric values
    data_frame['close'] = pd.to_numeric(data_frame['close'])
    data_frame['high'] = pd.to_numeric(data_frame['high'])
    data_frame['low'] = pd.to_numeric(data_frame['low'])
    data_frame['open'] = pd.to_numeric(data_frame['open'])

    # add simple mean averages
    data_frame['SMA200'] = ta.trend.sma_indicator(data_frame['close'], 200)
    data_frame['SMA600'] = ta.trend.sma_indicator(data_frame['close'], 600)

    # remove useless
    del data_frame['timestamp']
    del data_frame['ignore']
    del data_frame['close_time']
    del data_frame['quote_av']
    del data_frame['trades']
    del data_frame['tb_base_av']
    del data_frame['tb_quote_av']

    return data_frame
