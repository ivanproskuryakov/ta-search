import pandas as pd
import numpy as np
import talib.abstract as ta

from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
from scipy import signal

from freqtrade.persistence.trade_model import Trade
from freqtrade.strategy.interface import IStrategy

# +++++++++

class TaLevelB5m(IStrategy):
    minimal_roi = {
        "0": 1
    }
    stoploss = -0.03
    can_short = True

    trailing_stop = True
    trailing_stop_positive = 0.15
    trailing_stop_positive_offset = 0.2
    trailing_only_offset_is_reached = True

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        pd.set_option('display.max_rows', 100000)
        pd.set_option('display.precision', 10)
        pd.set_option('mode.chained_assignment', None)

        df['rsi_7'] = ta.RSI(df['close'], timeperiod=7).round(2)
        df['level_min'] = 0
        df['level_max'] = 0

        print(metadata)

        df = self.do_long(df)
        df = self.do_short(df)

        return df

    def do_long(self, df: pd.DataFrame) -> pd.DataFrame:
        n = 250
        df['buy_min'] = df.iloc[signal.argrelextrema(df.close.values, np.less_equal, order=n)[0]]['close']

        x_times = df.query(f'buy_min > 0')

        if len(x_times) > 0:
            x = x_times.index[-1]
            x_close = df['close'].loc[x]

            chunk = df[:x - 1]
            chunk['buy_min'] = chunk.iloc[signal.argrelextrema(chunk.close.values, np.less_equal, order=n)[0]]['close']
            chunk_times = chunk.query(f'buy_min > 0')

            if len(chunk_times) > 0:
                y = chunk_times.index[-1]
                y_close = chunk_times['close'].loc[y]

                diff_close_xy = self.diff_percentage(x_close, y_close)
                dist_xy = x - y

                # if dist_xy > 1 and diff_close_xy < 0.1 and x_close > y_close: # level
                if dist_xy > 20 and diff_close_xy < 0.1:
                    for i, row in df.iterrows():
                        dist_xi = i - x

                        if 1 < dist_xi < 4:
                            i_close = df['close'].loc[i]
                            is_rising = df['open'].loc[i] < df['close'].loc[i] \
                                        and df['open'].loc[i - 1] < df['close'].loc[i - 1]
                                        # and df['open'].loc[i - 2] < df['close'].loc[i - 2]

                            diff_close_xi = self.diff_percentage(x_close, i_close)

                            if is_rising and i_close > x_close and 0 < diff_close_xi < 1:
                                print(y, x, i, '---', diff_close_xy, diff_close_xi, 'long')
                                df['level_min'].loc[i] = i

        return df

    def do_short(self, df: pd.DataFrame) -> pd.DataFrame:
        n = 250
        df['buy_max'] = df.iloc[signal.argrelextrema(df.close.values, np.greater_equal, order=n)[0]]['close']

        x_times = df.query(f'buy_max > 0')

        if len(x_times) > 0:
            x = x_times.index[-1]
            x_close = df['close'].loc[x]

            chunk = df[:x - 1]
            chunk['buy_max'] = chunk.iloc[signal.argrelextrema(chunk.close.values, np.greater_equal, order=n)[0]][
                'close']
            chunk_times = chunk.query(f'buy_max > 0')

            if len(chunk_times) > 0:
                y = chunk_times.index[-1]
                y_close = chunk_times['close'].loc[y]

                diff_close_xy = self.diff_percentage(x_close, y_close)

                dist_xy = x - y

                # if dist_xy > 1 and diff_close_xy < 0.1 and x_close < y_close: # level
                if dist_xy > 20 and diff_close_xy < 0.1:
                    for i, row in df.iterrows():
                        dist_xi = i - x

                        if 1 < dist_xi < 4:
                            i_close = df['close'].loc[i]
                            is_falling = df['open'].loc[i] > df['close'].loc[i] \
                                         and df['open'].loc[i - 1] > df['close'].loc[i - 1]
                                         # and df['open'].loc[i - 2] > df['close'].loc[i - 2]

                            diff_close_xi = self.diff_percentage(x_close, i_close)

                            if is_falling and i_close < x_close and 0 < diff_close_xi < 1:
                                print(y, x, i, '---', diff_close_xy, diff_close_xi, 'short')
                                df['level_max'].loc[i] = i

        return df

    def populate_entry_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['level_max'] > 0),
            'enter_short'
        ] = 1
        df.loc[
            (df['level_min'] > 0),
            'enter_long'
        ] = 1

        return df

    def populate_exit_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['rsi_7'] < 2),
            'exit_short'
        ] = 1
        df.loc[
            (df['rsi_7'] > 98),
            'exit_long'
        ] = 1

        return df

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: Optional[str],
                 side: str, **kwargs) -> float:

        return 20

    def diff_percentage(self, v2, v1) -> float:
        diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100
        diff = np.round(diff, 4)

        return np.abs(diff)
