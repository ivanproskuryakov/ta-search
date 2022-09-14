import pandas as pd
import numpy as np
import talib.abstract as ta

from scipy import signal


class Search1m:
    n: int
    p: float

    def __init__(self, n: int, p: float):
        self.n = n
        self.p = p
        pd.set_option('display.max_rows', 100000)
        pd.set_option('display.precision', 10)
        pd.set_option('mode.chained_assignment', None)

    def find_peaks(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parameters
        ----------
        n : int
            Number of points to be checked before and after
        """

        df['id'] = range(0, len(df))
        df['rsi_7'] = ta.RSI(df['close'], timeperiod=7)
        df['rsi_30'] = ta.RSI(df['close'], timeperiod=30)
        df['rsi_90'] = ta.RSI(df['close'], timeperiod=90)

        macd, macdsignal, macdhist = ta.MACD(df['close'])

        df['macd'] = macd
        df['macdsignal'] = macdsignal
        df['macdhist'] = macdhist

        df['buy'] = ''
        df['ex_min_percentage'] = ''
        df['ex_min'] = df.iloc[signal.argrelextrema(df.close.values, np.less_equal, order=self.n)[0]]['close']
        df['ex_max_percentage'] = ''
        df['ex_max'] = df.iloc[signal.argrelextrema(df.close.values, np.greater_equal, order=self.n)[0]]['close']
        df['sell'] = ''

        # find Min
        # -----

        ex_min = df.query(f'ex_min > 0')
        ex_min_index = ex_min.index.values.tolist()
        ex_min_index.reverse()

        for id in ex_min_index:
            max = df.query(f'index < {id} and ex_max > 0')
            last = max[-1:]

            if last.size > 0:
                per = float(
                    self.__diff_percentage(
                        v1=ex_min.loc[id]['close'],
                        v2=last['close']
                    )
                )
                df['ex_min_percentage'].loc[id] = -per

        # find Max
        # -----
        ex_max = df.query(f'ex_max > 0')
        ex_max_index = ex_max.index.values.tolist()
        ex_max_index.reverse()

        for id in ex_max_index:
            max = df.query(f'index < {id} and ex_min > 0')
            last = max[-1:]

            if last.size > 0:
                per = float(
                    self.__diff_percentage(
                        v2=ex_max.loc[id]['close'],
                        v1=last['close']
                    )
                )
                df['ex_max_percentage'].loc[id] = per

        df['buy'] = df.apply(lambda row: self.__populate_buy(row), axis=1)
        df['sell'] = df.apply(lambda row: self.__populate_sell(row), axis=1)

        # clean NaN
        df['ex_min'] = df['ex_min'].apply(lambda x: x if float(x) > 0 else '')
        df['ex_max'] = df['ex_max'].apply(lambda x: x if float(x) > 0 else '')

        return df

    def __populate_buy(self, row: pd.DataFrame):
        if row['ex_min_percentage'] \
                and row['ex_min_percentage'] < -self.p \
                and 10 < row['rsi_7'] < 25 \
                and row['rsi_30'] < 35 \
                and row['rsi_90'] < 45 \
                and row['macd'] < 0 \
                and row['macdsignal'] < 0 \
                and row['macdhist'] < 0:
            return 'buy'
        else:
            return ''

    def __populate_sell(self, row: pd.DataFrame):
        if row['ex_max_percentage'] \
                and row['rsi_7'] > 75 \
                and row['macd'] > 0 \
                and row['macdsignal'] > 0 \
                and row['macdhist'] > 0:
            return 'sell'
        else:
            return ''

    def __diff_percentage(self, v2, v1) -> float:
        diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100
        diff = np.round(diff, 4)

        return diff
