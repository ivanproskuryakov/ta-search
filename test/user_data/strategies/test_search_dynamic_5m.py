from src.service.dataset_builder import DatasetBuilder
from user_data.strategies.TaSearchDynamic5m import TaSearchDynamic5m

dataset_builder = DatasetBuilder()
strategy = TaSearchDynamic5m({})


# def test_ldo():
#     path = 'fixture/LDO_USDT_5m_1666310400.0_1667210709.0.json'
#
#     df = dataset_builder.from_file(path)
#     df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
#     df = strategy.populate_indicators(df, {})
#     df = strategy.populate_buy_trend(df, {})
#     df = strategy.populate_sell_trend(df, {})
#
#     print(df)
#     # assert df.loc[2545]['buy'] == 1

# def test_xrp():
#     path = 'fixture/XRP_USDT_5m_1669852800.0_1670112000.0.json'
#
#     df = dataset_builder.from_file(path)
#     df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
#     df = strategy.populate_indicators(df, {})
#     df = strategy.populate_buy_trend(df, {})
#     df = strategy.populate_sell_trend(df, {})
#
#     print(df)
#     assert df.loc[644]['ex_min_percentage'] == -2.1928

def test_twt():
    path = 'fixture/TWT_USDT_5m_1671926400.0_1672099200.0.json'

    df = dataset_builder.from_file(path)
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    df = strategy.populate_indicators(df, {})
    df = strategy.populate_buy_trend(df, {})
    df = strategy.populate_sell_trend(df, {})

    print(df)
    assert df.loc[196]['ex_min_percentage'] == -11.3241
    assert df.loc[196]['volume'] == 249249.0
    assert df.loc[196]['volume_mean'] == 62648.0
    assert df.loc[197]['buy'] == 1