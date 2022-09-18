import pandas as pd

from src.service.dataset_builder import DatasetBuilder
from src.service.search30m import Search30m

dataset_builder = DatasetBuilder()
search5m = Search30m(n=24, p=4)

pd.set_option('display.max_rows', 100000)
pd.set_option('display.precision', 10)


def test_ocean():
    path = 'fixture/30m/OCEAN_USDT_30m_1662336000.0_1663113600.0.json'

    df = dataset_builder.from_file(path)
    df = df[["date", "close"]]
    # df = df[0:362]
    df = search5m.find_peaks(df)

    print(df)
