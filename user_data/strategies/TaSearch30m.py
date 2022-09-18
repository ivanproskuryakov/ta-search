import sys
import pandas as pd
from datetime import datetime

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.persistence import Order, PairLocks, Trade
from freqtrade.strategy.interface import IStrategy

from TaSearch import TaSearch


class SearchStrategy(IStrategy):
    search: TaSearch
    n: int
    p: float
    n = 24
    p = 4
    minimal_roi = {
        "0": 0.015
    }
    stoploss = -0.25
    timeframe = '30m'

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.search = TaSearch(n=self.n, p=self.p)

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df = self.search.find_extremes(df)

        df['buy'] = df.apply(lambda row: self.__populate_buy(row), axis=1)
        df['sell'] = df.apply(lambda row: self.__populate_sell(row), axis=1)

        return df

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['buy'] == 'buy'), 'buy'] = 1

        return df

    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['sell'] == 'sell'), 'sell'] = 1
        df.loc[(df['sell'] == 'sell'), 'exit_tag'] = 'sell_signal_search'

        return df

    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: datetime, **kwargs) -> bool:
        """
        https://www.freqtrade.io/en/stable/strategy-advanced/
        Reject force-sells with negative profit
        This is just a sample, please adjust to your needs
        (this does not necessarily make sense, assuming you know when you're force-selling)
        """

        if exit_reason == 'exit_signal' and trade.calc_profit_ratio(rate) < 0:
            return False

        return True

    def __populate_buy(self, row: pd.DataFrame):
        if row['ex_min_percentage'] \
                and row['ex_min_percentage'] < -self.p \
                and 10 < row['rsi_7'] < 25 \
                and row['macd'] < 0 \
                and row['macdsignal'] < 0 \
                and row['macdhist'] < 0:
            return 'buy'
        else:
            return ''

    def __populate_sell(self, row: pd.DataFrame):
        if row['macd'] > row['macdsignal'] > row['macdhist']:
            return f'sell'
        else:
            return ''
