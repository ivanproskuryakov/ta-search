import pandas as pd

from src.service.dataset_builder import DatasetBuilder
from src.service.search import Search

dataset_builder = DatasetBuilder()
search = Search()

pd.set_option('display.max_rows', 100000)
pd.set_option('display.precision', 10)


def test_find_peaks():
    path = 'fixture/BTC_USDT-1h.json'

    df = dataset_builder.from_file(path)

    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    # df = df[["open", "high", "low", "close"]]
    # df = df[0:10]

    df = search.find_peaks(df, n=20)

    print(df)
