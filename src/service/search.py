import pandas as pd
import numpy as np
import talib.abstract as ta

from scipy import signal


class Search:
    def find_peaks(self, df: pd.DataFrame) -> pd.DataFrame:
        n = 20  # number of points to be checked before and after

        df['RSI_7'] = ta.RSI(df['close'], timeperiod=7)
        df['RSI_20'] = ta.RSI(df['close'], timeperiod=20)

        macd, macdsignal, macdhist = ta.MACD(df['close'])

        df['macd'] = macd
        df['macdsignal'] = macdsignal
        df['macdhist'] = macdhist

        df['argrelextrema_min'] = df.iloc[signal.argrelextrema(df.close.values, np.less_equal, order=n)[0]]['close']
        df['argrelextrema_max'] = df.iloc[signal.argrelextrema(df.close.values, np.greater_equal, order=n)[0]]['close']

        df['argrelmin'] = df.iloc[signal.argrelmin(df.close.values, order=5)[0]]['close']
        df['find_peaks'] = df.iloc[signal.find_peaks(df.close.values, distance=10)[0]]['close']

        return df
