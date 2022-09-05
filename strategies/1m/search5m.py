import pandas as pd
import numpy as np
import talib.abstract as ta

from scipy import signal


class Search5m:
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
        df['ex_min'] = df.iloc[signal.argrelextrema(df.close.values, np.less_equal, order=self.n)[0]]['close']
        df['ex_max'] = df.iloc[signal.argrelextrema(df.close.values, np.greater_equal, order=self.n)[0]]['close']
        df['sell'] = ''

        ex_min = df.query(f'ex_min > 0')
        ex_min_index = ex_min.index.values.tolist()

        for id in ex_min_index:
            max = df.query(f'index > {id} and ex_max > 0')
            first = max[0:1]

            if first.size > 0:
                per = float(
                    self.__diff_percentage(
                        v1=ex_min.loc[id]['close'],
                        v2=first['close']
                    )
                )

                df['ex_max_percentage'].loc[id] = per

        ex_min_index.reverse()

        for id in ex_min_index:
            max = df.query(f'index < {id} and ex_max > 0')
            last = max[-1:]

            # not last maximum, but first after the previous minumum
            # not from maximum, but from MACD sell

            if last.size > 0:
                per = float(
                    self.__diff_percentage(
                        v1=ex_min.loc[id]['close'],
                        v2=last['close']
                    )
                )
                df['ex_min_percentage'].loc[id] = -per

        df['buy'] = df.apply(lambda row: self.__populate_buy(row), axis=1)
        df['sell'] = df.apply(lambda row: self.__populate_sell(row), axis=1)

        # clean NaN
        df['ex_min'] = df['ex_min'].apply(lambda x: x if float(x) > 0 else '')
        df['ex_max'] = df['ex_max'].apply(lambda x: x if float(x) > 0 else '')

        df['buy'] = df['buy'].eq(df['buy'].shift()).apply(lambda x: '' if x else 'buy')

        return df

    def __populate_buy(self, row: pd.DataFrame):
        if row['ex_min_percentage'] \
                and float(row['ex_min_percentage']) < -self.p \
                and row['macd'] < row['macdsignal'] < row['macdhist'] \
                and row['rsi_7'] < 35:
            return 'buy'
        else:
            return ''

    def __populate_sell(self, row: pd.DataFrame):
        if row['rsi_7'] > 80:
            # row['macd'] > row['macdsignal'] > row['macdhist'] \
            #     or row['rsi_7'] > 90:
            # row['macd'] > row['macdhist'] or row['macdsignal'] > row['macdhist']:
            # and (row['macd'] > row['macdhist'] or row['macdsignal'] > row['macdhist']):
            return 'sell'
        else:
            return ''

    def __diff_percentage(self, v2, v1) -> float:
        diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100
        diff = np.round(diff, 4)

        return diff
