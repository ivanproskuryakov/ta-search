import os
from binance import Client, enums

from src.service.util import Utility

"""
https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data

Taker - an order that trades immediately before going on the order book
Maker - an order that goes on the order book partially or fully

0 Open time,

1 Open,
2 High,
3 Low,
4 Close,
5 Volume,

6 Close time,

7 Quote asset volume,
8 Number of trades,
9 Taker buy base asset volume,
10 Taker buy quote asset volume,

11 Ignore


[
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
]
"""


class KLines:
    utility: Utility

    def __init__(self):
        self.utility = Utility()

    def build_klines(
            self,
            market: str,
            asset: str,
            klines_type: enums.HistoricalKlinesType,
            interval: str,
            start_at: float,
            end_at: float = None,
    ):
        if 'API_KEY' in os.environ:
            client = Client(
                api_key=os.environ['API_KEY'],
                api_secret=os.environ['API_SECRET'],
            )
        else:
            client = Client()

        symbol = asset + market

        klines = client.get_historical_klines(
            symbol=symbol,
            interval=interval,
            klines_type=klines_type,
            start_str=str(start_at),
            end_str=str(end_at),
        )
        collection = []

        for current in klines:
            time_open = current[0] / 1000
            price_open = self.utility.round(current[1], 10)
            price_high = self.utility.round(current[2], 10)
            price_low = self.utility.round(current[3], 10)
            price_close = self.utility.round(current[4], 10)

            # price_diff = self.utility.diff_percentage(price_close, price_open)
            # price_positive = 1 if price_diff > 0 else 0

            volume = self.utility.round(float(current[5]), 1)
            time_close = current[6] / 1000

            quote_asset_volume = self.utility.round(float(current[7]), 0)
            trades = self.utility.round(float(current[8]), 0)
            volume_taker = self.utility.round(float(current[9]), 0)

            # date = datetime.utcfromtimestamp(time_open)

            item = {
                'price_open': price_open,
                'price_high': price_high,
                'price_low': price_low,
                'price_close': price_close,
                # 'price_diff': price_diff,
                # 'price_positive': price_positive,

                'time_open': time_open,
                'time_close': time_close,

                # 'time_month': date.month,
                # 'time_hour': date.hour,
                # 'time_day': date.day,
                # 'time_minute': date.minute,

                'trades': trades,
                'volume': volume,
                'volume_taker': volume_taker,
                # 'volume_maker': volume_maker,

                'quote_asset_volume': quote_asset_volume,
            }

            collection.append(item)

        return collection
