import sys
import pandas as pd
from datetime import datetime

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.persistence import Order, PairLocks, Trade
from freqtrade.strategy.interface import IStrategy

from search30m import Search30m


class SearchStrategy(IStrategy):
    search: Search30m
    n: int
    p: float

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.search = Search30m(n=self.n, p=self.p)

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df = self.search.find_peaks(df)

        return df

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['buy'] == 'buy'), 'buy'] = 1

        return df

    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['sell'] == 'sell'), 'sell'] = 1

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

        if exit_reason == 'exit_signal' and trade.calc_profit_ratio(rate) > 0:
            return True

        return False
