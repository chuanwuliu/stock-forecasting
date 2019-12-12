import os
import pandas as pd

data_dir = os.environ['ASX_DATA_DIR']
columns = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']


def read_dates():
    """
    Read the list of trading dates from the ASX data set.

    :return: list, dates
    """
    dates = list()
    for fname in os.listdir(data_dir):
        file = os.path.join(data_dir, fname)
        dfi = pd.read_csv(file, header=None, names=columns, parse_dates=['date'])
        date = dfi.date[0]
        dates.append(date)
    dates.sort()
    return dates


def read_stock_data(ticker, dates=None):
    """
    Read stock data from the ASX data set.

    :param ticker: str, ticker
    :param dates: list-like, time index of the return data frame
    :return: DataFrame
    """
    df = pd.DataFrame(columns=columns)
    for fname in os.listdir(data_dir):
        file = os.path.join(data_dir, fname)
        dfi = pd.read_csv(file, header=None, names=columns, parse_dates=['date'])
        if ticker in dfi['ticker'].values:
            df = df.append(dfi[dfi['ticker'] == ticker])
    df = df.set_index('date')
    df.name = ticker
    df = df.drop(columns=['ticker'])
    if dates:
        df_full = pd.DataFrame(index=dates, columns=df.columns)
        df_full.loc[df.index] = df
        df = df_full
    df = df.sort_index()
    return df
