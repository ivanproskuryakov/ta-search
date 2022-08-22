import pandas as pd
import numpy as np
import talib.abstract as ta

from scipy.signal import argrelextrema


class Search:
    def find_peaks(self, df: pd.DataFrame) -> pd.DataFrame:
        n = 10  # number of points to be checked before and after

        macd, macdsignal, macdhist = ta.MACD(df['price_close'])

        df['RSI_20'] = ta.RSI(df['price_close'], timeperiod=20)
        df['RSI_50'] = ta.RSI(df['price_close'], timeperiod=50)
        df['RSI_100'] = ta.RSI(df['price_close'], timeperiod=100)

        df['macd'] = macd
        df['macdsignal'] = macdsignal
        df['macdhist'] = macdhist

        df['min'] = df.iloc[argrelextrema(df.price_close.values, np.less_equal, order=n)[0]]['price_close']
        df['max'] = df.iloc[argrelextrema(df.price_close.values, np.greater_equal, order=n)[0]]['price_close']

        return df
