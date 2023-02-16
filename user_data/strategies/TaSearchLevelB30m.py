import pandas as pd
import numpy as np
import talib.abstract as ta

from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
from scipy import signal

from freqtrade.persistence.trade_model import Trade
from freqtrade.strategy.interface import IStrategy

# Stable ?

class TaSearchLevelB30m(IStrategy):
    minimal_roi = {
        "0": 1
    }
    stoploss = -0.05
    can_short: bool = True

    trailing_stop = True
    trailing_stop_positive = 0.05
    trailing_stop_positive_offset = 0.20
    trailing_only_offset_is_reached = True

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        pd.set_option('display.max_rows', 100000)
        pd.set_option('display.precision', 10)
        pd.set_option('mode.chained_assignment', None)

        df['rsi_7'] = ta.RSI(df['close'], timeperiod=7).round(2)
        df['level_min'] = 0
        df['level_max'] = 0

        # logging.getLogger('freqtrade').info(metadata)

        df = self.do_long(df)
        df = self.do_short(df)

        return df

    def do_long(self, df: pd.DataFrame) -> pd.DataFrame:
        n = 200
        df['buy_min'] = df.iloc[signal.argrelextrema(df.close.values, np.less_equal, order=n)[0]]['close']

        times = df.query(f'buy_min > 0')
        prices = []

        if len(times) > 0:
            for i, row in df.iterrows():
                if df['buy_min'].loc[i] > 0:
                    close = df['close'].loc[i]

                    chunk = df[:i - 1]
                    chunk['buy_min'] = chunk.iloc[signal.argrelextrema(chunk.close.values, np.less_equal, order=n)[0]]['close']

                    time_chunk = chunk.query(f'buy_min > 0')

                    for x, row in time_chunk.iterrows():
                        close_chunk = row['close']
                        diff = self.diff_percentage(close_chunk, close)

                        if diff < 0.5:
                            prices.append(close)
                            df['level_min'].loc[i] = 1

                    for p in prices:
                        diff = self.diff_percentage(p, close)

                        if diff < 0.5:
                            # print(close, close_chunk, diff, ' +++++ ', i, x)
                            df['level_min'].loc[i] = 1

        return df

    def do_short(self, df: pd.DataFrame) -> pd.DataFrame:
        n = 200
        df['buy_max'] = df.iloc[signal.argrelextrema(df.close.values, np.greater_equal, order=n)[0]]['close']

        times = df.query(f'buy_max > 0')
        prices = []

        if len(times) > 0:
            for i, row in df.iterrows():
                if df['buy_max'].loc[i] > 0:
                    close = df['close'].loc[i]

                    chunk = df[:i - 1]
                    chunk['buy_max'] = chunk.iloc[signal.argrelextrema(chunk.close.values, np.greater_equal, order=n)[0]]['close']

                    time_chunk = chunk.query(f'buy_max > 0')

                    for x, row in time_chunk.iterrows():
                        close_chunk = row['close']
                        diff = self.diff_percentage(close_chunk, close)

                        if diff < 0.5:
                            prices.append(close)
                            df['level_max'].loc[i] = 1

                    for p in prices:
                        diff = self.diff_percentage(p, close)

                        if diff < 0.5:
                            # print(close, close_chunk, diff, ' +++++ ', i, x)
                            df['level_max'].loc[i] = 1

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
            (df['rsi_7'] < 10),
            'exit_short'
        ] = 1
        df.loc[
            (df['rsi_7'] > 90),
            'exit_long'
        ] = 1

        return df

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: Optional[str],
                 side: str, **kwargs) -> float:

        return 5.0

    def diff_percentage(self, v2, v1) -> float:
        diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100
        diff = np.round(diff, 4)

        return np.abs(diff)
