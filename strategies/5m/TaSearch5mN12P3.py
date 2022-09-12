from SearchStrategy import SearchStrategy


class TaSearch5mN12P3(SearchStrategy):
    n = 12
    p = 3
    minimal_roi = {
        "0": 0.1
    }
    stoploss = -0.15
    timeframe = '5m'