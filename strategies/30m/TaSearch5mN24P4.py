from SearchStrategy import SearchStrategy


class TaSearch5mN24P4(SearchStrategy):
    n = 24
    p = 4
    minimal_roi = {
        "0": 0.015
    }
    stoploss = -0.25
    timeframe = '30m'