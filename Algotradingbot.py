import numpy as np
import pandas as pd

import yfinance as yf
from datetime import datetime, timedelta
import time

class TradingStrategy:
    def __init__(self, symbol):
        """Initialize with stock symbol."""
        self.symbol = symbol
    
    def get_live_data(self):
        """Fetch real-time stock data."""
        stock = yf.Ticker(self.symbol)
        data = stock.history(period='1d', interval='1m')

        if data.empty:
            raise ValueError(f"No data available for the symbol {self.symbol}.")

        latest_data = data.iloc[-1]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {
            "Timestamp": timestamp,
            "Open": latest_data['Open'],
            "High": latest_data['High'],
            "Low": latest_data['Low'],
            "Close": latest_data['Close'],
            "Symbol": self.symbol
        }
    
    def simple_strategy(self, data):
        """Basic trading strategy using OHLC values."""
        if data['Close'] > data['Open']:
            return "BUY"
        elif data['Close'] < data['Open']:
            return "SELL"
        else:
            return "HOLD"

    def start_trading(self):
        """Start Algo Trading bot."""
        print("Starting The Algo-Bot...")
        print("Waiting for the next minute...")
        while True:
            try:
                now = datetime.now()
                next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
                time_wait = (next_minute - now).total_seconds()
                time.sleep(time_wait)

                live_data = self.get_live_data()
                decision = self.simple_strategy(live_data)

                print(f"{live_data['Timestamp']} Symbol: {live_data['Symbol']} , "
                      f"O: {live_data['Open']:.4f} , H: {live_data['High']:.4f} , "
                      f"L: {live_data['Low']:.4f} , C: {live_data['Close']:.4f} - {decision}")
            
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)  # Retry after a delay

# Example usage
if __name__ == "__main__":
    symbol = "NVDA"
    strategy = TradingStrategy(symbol)
    strategy.start_trading()