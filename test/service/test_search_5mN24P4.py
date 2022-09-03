import pandas as pd

from src.service.dataset_builder import DatasetBuilder
from src.service.search5m import Search5m

dataset_builder = DatasetBuilder()
search5m = Search5m(n=24, p=4)

pd.set_option('display.max_rows', 100000)
pd.set_option('display.precision', 10)


def test_find_peaks_auto_5m():
    path = 'fixture/AUTO_USDT_5m_1660485600.0_1660572000.0.json'

    df = dataset_builder.from_file(path)
    df = df[["open", "high", "low", "close"]]
    df = search5m.find_peaks(df)

    print(df)

def test_find_peaks_btc_30_aug_2022():
    path = 'fixture/BTC_USDT_5m_1661818393.0_1661904013000.0.json'

    df = dataset_builder.from_file(path)
    df = df[["open", "high", "low", "close"]]
    df = search5m.find_peaks(df)

    print(df)

def test_find_peaks_sol_30_aug_2022():
    path = 'fixture/SOL_USDT_5m_1661818393.0_1661904013000.0.json'

    df = dataset_builder.from_file(path)
    df = df[["open", "high", "low", "close"]]
    df = search5m.find_peaks(df)

    print(df)

def test_find_peaks_xrp_30_aug_2022():
    path = 'fixture/XRP_USDT_5m_1661818393.0_1661904013000.0.json'

    df = dataset_builder.from_file(path)
    df = df[["open", "high", "low", "close"]]
    df = search5m.find_peaks(df)

    print(df)
