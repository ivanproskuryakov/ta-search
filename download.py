import sys
import json

from binance import enums
from src.service.klines import KLines
from src.parameters import market

kLines = KLines()

asset = sys.argv[1]
interval = sys.argv[2]
start_at = float(sys.argv[3])
end_at = float(sys.argv[4])

collection = kLines.build_klines(
    asset=asset,
    market=market,
    interval=interval,
    klines_type=enums.HistoricalKlinesType.SPOT,
    start_at=start_at,
    end_at=end_at,
)

text = json.dumps(collection)

file = open(f'fixture/{asset}_{market}_{interval}_{start_at}_{end_at}.json', 'w')
file.write(text)
file.close()
