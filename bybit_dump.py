import requests
from collections import OrderedDict

response = requests.get("https://api.bybit.com/derivatives/v3/public/instruments-info")
collection = response.json()['result']['list']

pairs = OrderedDict()

for item in collection:
    s = f'"{item["symbol"]}",'
    # s = f'"{item["baseCoin"]}/{item["quoteCoin"]}",'

    if s.find('USDT') > 0:
        print(s)