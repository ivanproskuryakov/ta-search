import pandas as pd

from src.service.dataset_builder import DatasetBuilder
from src.service.search1m import Search1m

dataset_builder = DatasetBuilder()
search = Search1m(n=60, p=1)

pd.set_option('display.max_rows', 100000)
pd.set_option('display.precision', 10)


def test_find_peaks_btc_1m_crop():
    path = 'fixture/BTC_USDT_1m_1662271200.0_1662285600.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    df = search.find_peaks(df)

    print(df)

def test_find_peaks_eth_1m_crop():
    path = 'fixture/ETH_USDT_1m_1662271200.0_1662285600.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    df = search.find_peaks(df)

    print(df)


def test_find_peaks_ada_1m_crop():
    path = 'fixture/ADA_USDT_1m_1662271200.0_1662285600.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    df = search.find_peaks(df)

    print(df)
