import pandas as pd

from src.service.dataset_builder import DatasetBuilder
from src.service.search import Search

dataset_builder = DatasetBuilder()
search = Search()

pd.set_option('display.max_rows', 100000)
pd.set_option('display.precision', 10)


def test_find_peaks_auto_1h_short():
    path = 'fixture/AUTO_USDT_1h_1660485600.0_1660572000.0.json'

    df = dataset_builder.from_file(path)
    df = df[["open", "high", "low", "close"]]
    df = search.find_peaks(df, n=20)

    print(df)


def test_find_peaks_ldo_1h():
    path = 'fixture/LDO_USDT_1h_1660521600.0_1661212800.0.json'

    df = dataset_builder.from_file(path)
    df = df[["open", "high", "low", "close"]]
    df = search.find_peaks(df, n=20)

    print(df)


def test_find_peaks_ldo_1h_crop():
    path = 'fixture/LDO_USDT_1h_1660521600.0_1661212800.0.json'

    df = dataset_builder.from_file(path)
    df = df[0: 155]
    df = df[["open", "high", "low", "close"]]
    df = search.find_peaks(df, n=20)

    print(df)


def test_find_peaks_btc_1h():
    path = 'fixture/BTC_USDT_1h_1657411200.0_1658534400.0.json'

    df = dataset_builder.from_file(path)
    df = df[["open", "high", "low", "close"]]
    df = search.find_peaks(df, n=20)

    print(df)


def test_find_peaks_btc_1h_crop():
    path = 'fixture/BTC_USDT_1h_1657411200.0_1658534400.0.json'

    df = dataset_builder.from_file(path)
    df = df[0: 300]
    df = df[["open", "high", "low", "close"]]
    df = search.find_peaks(df, n=20)

    print(df)


def test_find_peaks_shib_1h():
    path = 'fixture/SHIB_USDT_1h_1654819200.0_1655856000.0.json'

    df = dataset_builder.from_file(path)
    df = df[["open", "high", "low", "close"]]
    df = search.find_peaks(df, n=20)

    print(df)


def test_find_peaks_shib_1h_crop():
    path = 'fixture/SHIB_USDT_1h_1654819200.0_1655856000.0.json'

    df = dataset_builder.from_file(path)
    df = df[["close"]]
    df = df[0: 280]
    df = search.find_peaks(df, n=20)

    print(df)


def test_find_peaks_eth_1h():
    path = 'fixture/ETH_USDT_1h_1658448000.0_1658966400.0.json'

    df = dataset_builder.from_file(path)
    df = df[["close"]]
    df = search.find_peaks(df)

    print(df)


def test_find_peaks_eth_1h_crop():
    path = 'fixture/ETH_USDT_1h_1658448000.0_1658966400.0.json'

    df = dataset_builder.from_file(path)
    df = df[["close"]]
    df = df[0: 130]
    df = search.find_peaks(df, n=20)

    print(df)
