import os
import pandas as pd

asx_data_dir = os.environ['ASX_DATA_DIR']
fmt = "%Y%m%d"


class PriceData:
    """
    Prices Data class
    """

    def __init__(self, ticker):
        self._sticker = ticker
        self._df = read_stock_prices(ticker)

    @property
    def df(self):
        return self._df

    @property
    def open(self):
        return self._df['open']

    @property
    def high(self):
        return self._df['high']

    @property
    def low(self):
        return self._df['low']

    @property
    def close(self):
        return self._df['close']

    @property
    def volumn(self):
        return self._df['volumn']

    @property
    def future_close_return(self):
        return self.close / self.close.shift(1) - 1

    @property
    def close_return(self):
        return self.close / self.close.shift(-1) - 1

    @property
    def high_low_ratio(self):
        return self.high / self.low


def read_stock_prices(ticker):
    columns = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(columns=columns)
    for fname in os.listdir(asx_data_dir):
        file = os.path.join(asx_data_dir, fname)
        dfi = pd.read_csv(file, header=None, names=columns, parse_dates=['date'])
        if ticker in dfi['ticker'].values:
            df = df.append(dfi[dfi['ticker'] == ticker])
    df = df.set_index('date')
    df = df.drop(columns=['ticker'])
    df.name = ticker
    df = df.sort_index()
    return df

