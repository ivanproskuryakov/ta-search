from SearchStrategy import SearchStrategy


class TaSearch1mN60P1(SearchStrategy):
    n = 60
    p = 0.7
    minimal_roi = {
        "0": 0.005
    }
    stoploss = -0.1
