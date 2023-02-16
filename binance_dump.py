import requests
from collections import OrderedDict

response = requests.get("https://www.binance.com/bapi/asset/v1/public/asset-service/product/get-exchange-info")
collection = response.json()['data']

pairs = OrderedDict()

for i in collection:
    if i['quoteAsset'] not in pairs:
        pairs[i['quoteAsset']] = []

    pairs[i['quoteAsset']].append(i['baseAsset'])

for p in pairs:
    file = open('data/' + p + '.txt', 'w')
    lines = []

    for a in pairs.get(p):
        lines.append('"{a}/{p}",\n'.format(
            a=a,
            p=p
        ))

    file.writelines(lines)
    file.close()