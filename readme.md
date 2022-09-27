## Description

FreqTrade trade entry indicator detection library and strategies. For running a strategy copy the files from
user_data/strategies to your freqtrade bot directory and run as usual.

```
freqtrade trade --config config.usdt.1m.json --strategy TaSearch1m --db-url sqlite:///TaSearch1mN60P1.sqlite
freqtrade trade --config config.usdt.1m.json --strategy TaSearch1m --db-url sqlite:///search1mStrategy.sqlite

freqtrade trade --config config.usdt.30m.json --strategy TaSearch30m --db-url sqlite:///search30mStrategy.sqlite
freqtrade trade --config config.usdt.30m.json --strategy TaSearch30m --db-url sqlite:///TaSearch5mN24P5.sqlite

freqtrade trade --config config.usdt.5m.json --strategy TaSearch5m --db-url sqlite:///search5mStrategy.sqlite   
```

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

The project comes with a handy command which dowloads timeseries data 

```
python download.py AUTO 30m 1660485600 1660572000
```

```
python -m pytest test

python -m pytest -s test/service/test_search_5m.py
python -m pytest -s test/service/test_search_1m.py

```