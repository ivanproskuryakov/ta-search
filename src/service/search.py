import pandas as pd
import numpy as np
import talib.abstract as ta

from scipy import signal
from src.service.util import Utility


class Search:
    utility: Utility

    def __init__(self):
        self.utility = Utility()

    def find_peaks(self, df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
        """
        Parameters
        ----------
        n : int
            Number of points to be checked before and after
            Default is 20
        """

        df['id'] = range(0, len(df))
        df['rsi_7'] = ta.RSI(df['close'], timeperiod=7)
        df['rsi_20'] = ta.RSI(df['close'], timeperiod=24)

        macd, macdsignal, macdhist = ta.MACD(df['close'])

        df['macd'] = macd
        df['macdsignal'] = macdsignal
        df['macdhist'] = macdhist

        df['buy'] = ''
        df['ex_min_percentage'] = ''
        df['ex_max_percentage'] = ''
        df['ex_min'] = df.iloc[signal.argrelextrema(df.close.values, np.less_equal, order=n)[0]]['close']
        df['ex_max'] = df.iloc[signal.argrelextrema(df.close.values, np.greater_equal, order=n)[0]]['close']
        df['sell'] = ''

        ex_min = df.query(f'ex_min > 0')
        ex_min_index = ex_min.index.values.tolist()

        for id in ex_min_index:
            max = df.query(f'index > {id} and ex_max > 0')
            first = max[0:1]
            if first.size > 0:
                per = float(
                    self.utility.diff_percentage(
                        v1=ex_min.loc[id]['close'],
                        v2=first['close']
                    )
                )

                df['ex_max_percentage'].loc[id] = per

        ex_min_index.reverse()

        for id in ex_min_index:
            max = df.query(f'index < {id} and ex_max > 0')
            last = max[-1:]
            per = float(
                self.utility.diff_percentage(
                    v1=ex_min.loc[id]['close'],
                    v2=last['close']
                )
            )
            df['ex_min_percentage'].loc[id] = -per

        df['buy'] = df.apply(lambda row: self.populate_buy(row), axis=1)
        df['sell'] = df.apply(lambda row: self.populate_sell(row, ex_min_index[-1]), axis=1)

        # clean NaN
        df['ex_min'] = df['ex_min'].apply(lambda x: x if float(x) > 0 else '')
        df['ex_max'] = df['ex_max'].apply(lambda x: x if float(x) > 0 else '')

        return df

    def populate_buy(self, row: pd.DataFrame):
        if row['ex_min_percentage'] and row['macd'] < row['macdhist']:
            return 'buy'
        else:
            return ''

    def populate_sell(self, row: pd.DataFrame, min_index: pd.DataFrame):
        if float(row['ex_max']) > 0 \
                and (row['macd'] > row['macdsignal'] > row['macdhist']) \
                and row['id'] > min_index:
            return f'sell'
        else:
            return ''

# and ((row['macd'] > row['macdsignal'] > row['macdhist']) or row['rsi_7'] > 80)
