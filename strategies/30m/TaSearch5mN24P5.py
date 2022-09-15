from SearchStrategy import SearchStrategy


class TaSearch5mN24P5(SearchStrategy):
    n = 24
    p = 5
    minimal_roi = {
        "0": 0.015
    }
    stoploss = -0.25
    timeframe = '30m'
