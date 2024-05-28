import json
import pandas as pd
from datetime import datetime
from pandas.core.api import DataFrame as DataFrame
from enum import Enum

import requests

class Granularity(Enum):
    ONE_MINUTE=60,
    FIVE_MINUTES=300,
    FIFTEEN_MINUTES=900,
    ONE_HOUR=3600,
    SIX_HOURS=21600,
    ONE_DAY=86400

class CoinbaseLoader:

    def __init__(self, endpoint="https://api.exchange.coinbase.com"):
        self._base_url = endpoint

    def get_pairs(self) -> pd.DataFrame:
        response = requests.get(f"{self._base_url}/products")
        if response.status_code != 200:
            raise RuntimeError(f"Unable to request data, status: {response.status_code}")
        pairs = pd.DataFrame(response.json())
        pairs.set_index('id', drop=True, inplace=True)
        return pairs

    def get_historical_data(self, pair: str, period: str, granularity: Granularity) -> DataFrame:
        params = {
            "start": (datetime.now() - pd.Timedelta(period)).isoformat(),
            "end": datetime.now().isoformat(),
            "granularity": granularity.value
        }
        response = requests.get(f"{self._base_url}/products/{pair}/candles", params=params)
        if response.status_code != 200:
            raise RuntimeError(f"Unable to request data, status: {response.status_code}")
        data = response.json()
        df = pd.DataFrame(data, columns=("timestamp", "low", "high", "open", "close", "volume"))
        df.set_index('timestamp', drop=True, inplace=True)
        return df

if __name__ == "__main__":
    loader = CoinbaseLoader()
    pairs = loader.get_pairs()
    print(pairs)
    data = loader.get_historical_data("btc-usdt", "1 day", Granularity.ONE_DAY)
    print(data.head())
