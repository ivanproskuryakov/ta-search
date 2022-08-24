import pandas as pd
import numpy as np
import talib.abstract as ta

from scipy import signal
from src.service.util import Utility
from src.parameters import ASSET_RULE


class Search:
    utility: Utility

    def __init__(self):
        self.utility = Utility()

    def comparator(self, a, b):
        print(a, b)
        return np.less_equal

    def find_peaks(self, df: pd.DataFrame, asset: str) -> pd.DataFrame:
        n = 24  # number of points to be checked before and after

        df['rsi_7'] = ta.RSI(df['close'], timeperiod=7)
        df['rsi_20'] = ta.RSI(df['close'], timeperiod=20)

        macd, macdsignal, macdhist = ta.MACD(df['close'])

        df['macd'] = macd
        df['macdsignal'] = macdsignal
        df['macdhist'] = macdhist

        df['buy'] = ''
        df['ex_min_percentage'] = ''
        df['ex_min'] = df.iloc[signal.argrelextrema(df.close.values, np.less_equal, order=n)[0]]['close']
        df['ex_max'] = df.iloc[signal.argrelextrema(df.close.values, np.greater_equal, order=n)[0]]['close']

        # df['ex_max_p'] = 0
        # RSI_7 < 35
        # macd < 0 or macdsignal < 0 or macdhist < 0

        ex_min = df.query(f'ex_min > 0')
        ex_min_index = ex_min.index.values.tolist()
        ex_min_index.reverse()

        for id in ex_min_index:
            max = df.query(f'index < {id} and ex_max > 0')
            last = max[-1:]
            per = float(
                self.utility.diff_percentage(v1=ex_min.loc[id]['close'], v2=last['close'])
            )

            df['ex_min_percentage'].loc[id] = -per

        df['buy'] = df.apply(lambda row: self.valuation_buy(row, asset), axis=1)

        return df

    def valuation_buy(self, row: pd.DataFrame, asset: str):
        if row['ex_min_percentage'] and row['ex_min_percentage'] < -ASSET_RULE['1h'][asset]['percentage_buy']:
            return 'buy'
        else:
            return ''
