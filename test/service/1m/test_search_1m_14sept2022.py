import pandas as pd

from src.service.dataset_builder import DatasetBuilder
from src.service.search1m import Search1m

dataset_builder = DatasetBuilder()
search = Search1m(n=60, p=1)

pd.set_option('display.max_rows', 100000)
pd.set_option('display.precision', 10)


def test_ftt():
    path = 'fixture/1m/FTT_USDT_1m_1663113600.0_1663192800.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    # df = df[0: 251]
    df = search.find_peaks(df)

    print(df)

def test_btc():
    path = 'fixture/1m/BTC_USDT_1m_1663113600.0_1663192800.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    # df = df[0: 251]
    df = search.find_peaks(df)

    print(df)

def test_ada():
    path = 'fixture/1m/ADA_USDT_1m_1663113600.0_1663192800.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    # df = df[0: 251]
    df = search.find_peaks(df)

    print(df)