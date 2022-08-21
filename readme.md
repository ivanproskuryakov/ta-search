## Description

Trade entry indicator detection library 

### Installation

```
python -m venv .env
source .env/bin/activate

pip install -r requirements-mac.txt
pip install --force-reinstall -r requirements-mac.txt
```

### Commands

```
python download.py AUTO 1h 1660485600 1660572000
```


### Testing

Same as with training, tests require `ta_test` db for prevention of spoiling training or dev databases.

```
psql -U postgres
create database ta_test;
``` 

Running tests

```
ENV=test python -m pytest test
ENV=test python -m pytest --log-cli-level DEBUG -s test/service/dataset_builder.py
ENV=test python -m pytest -s test/service/dataset_builder.py

```