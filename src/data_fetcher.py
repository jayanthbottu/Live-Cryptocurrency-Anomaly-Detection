# src/data_fetcher.py
from binance import Client
import pandas as pd
from config.settings import BINANCE_API_KEY, BINANCE_API_SECRET

class BinanceDataFetcher:
    def __init__(self):
        self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    
    def get_klines(self, symbol: str, interval: str, limit: int = 100):
        """Fetch OHLCV data from Binance"""
        klines = self.client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]