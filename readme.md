## Description

FreqTrade trade bot entry indicator detection library. 
To run a strategy copy the files from user_data/strategies to your freqtrade bot directory and run as usual.

```
freqtrade trade --config config.usdt.1m.json --strategy TaSearch1m --db-url sqlite:///search1mStrategy.sqlite
freqtrade trade --config config.usdt.30m.json --strategy TaSearch30m --db-url sqlite:///search30mStrategy.sqlite
```

![model predict](doc/freqtrade_1m.png)

### Installation

For development and testing purposes project copy the repository with git clone and install the needed following the
commands below.

```
python -m venv .env
source .env/bin/activate

pip install -r requirements.txt
pip install --force-reinstall -r requirements.txt
```

### Testing

The command to download time series data for time-interval.
```
python download.py AUTO 30m 1660485600 1660572000
```

Running tests
```
python -m pytest test
python -m pytest -s test/user_data/strategies/1m/test_search_1m.py

```