import pandas as pd

from src.service.dataset_builder import DatasetBuilder
from src.service.search1m import Search1m

dataset_builder = DatasetBuilder()
search = Search1m(n=60, p=1)

pd.set_option('display.max_rows', 100000)
pd.set_option('display.precision', 10)


def test_link():
    path = 'fixture/1m/LINK_USDT_1m_1662660000.0_1662692400000.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    df = search.find_peaks(df)

    print(df)


def test_one():
    path = 'fixture/1m/ONE_USDT_1m_1662660000.0_1662692400000.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    df = search.find_peaks(df)

    print(df)