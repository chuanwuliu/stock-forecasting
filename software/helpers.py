import pandas as pd


def batch_generator(s, hop='1D', seg_length=None, periods=None):
    """
    Get a generator of for iterating over the s with given frequency. For each iteration, it yield a sub-series.
     Note that the last iteration segment may be shorter that the given frequency.

    :param s: time series, Series or Dataframe
    :param hop: str or timedelta, default '1D'
    :param seg_length: str or timedelta, length of each segment. If not given, use hop, default None.
    :param periods: int, number of iteration periods. If the iteration periods is longer than the input series,
                    the function yields empty list.
    :return: yield a time series, Series or Dataframe

    Examples:

    >>> import pandas as pd
    >>> s = pd.Series(range(10), index=pd.date_range(start='2019-01-01', freq='1H', periods=10))
    >>> s
    2019-01-01 00:00:00    0
    2019-01-01 01:00:00    1
    2019-01-01 02:00:00    2
    2019-01-01 03:00:00    3
    2019-01-01 04:00:00    4
    2019-01-01 05:00:00    5
    2019-01-01 06:00:00    6
    2019-01-01 07:00:00    7
    2019-01-01 08:00:00    8
    2019-01-01 09:00:00    9
    Freq: H, dtype: int64
    >>> itr = batch_generator(s, hop='4H')
    >>> next(itr)
    2019-01-01 00:00:00    0
    2019-01-01 01:00:00    1
    2019-01-01 02:00:00    2
    2019-01-01 03:00:00    3
    Freq: H, dtype: int64
    >>> next(itr)
    2019-01-01 04:00:00    4
    2019-01-01 05:00:00    5
    2019-01-01 06:00:00    6
    2019-01-01 07:00:00    7
    Freq: H, dtype: int64
    >>> next(itr)
    2019-01-01 08:00:00    8
    2019-01-01 09:00:00    9
    Freq: H, dtype: int64
    >>> itr = batch_generator(s, hop='4H', seg_length='2H')
    >>> next(itr)
    2019-01-01 00:00:00    0
    2019-01-01 01:00:00    1
    Freq: H, dtype: int64
    >>> next(itr)
    2019-01-01 04:00:00    4
    2019-01-01 05:00:00    5
    Freq: H, dtype: int64
    >>> next(itr)
    2019-01-01 08:00:00    8
    2019-01-01 09:00:00    9
    Freq: H, dtype: int64
    """
    if seg_length is None:
        seg_length = hop
    td = pd.to_timedelta(hop)
    seg = pd.to_timedelta(seg_length)

    t0 = s.index[0]
    if periods:
        end = t0 + td * (periods - 1)
    else:
        end = s.index[-1]

    seg -= pd.to_timedelta(1, unit='ns')  # This is to avoid inclusion of last index when slicing pandas.Series
    while t0 <= end:
        t1 = t0 + seg
        s_sliced = s[t0:t1]
        t0 += td
        yield s_sliced