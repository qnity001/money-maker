import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel
import time

# Load environment variables from .env file
load_dotenv()

class FyersClient:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.access_token = os.getenv("ACCESS_TOKEN")

        self.fyers = fyersModel.FyersModel(client_id=self.client_id, is_async=False, token=self.access_token, log_path="")

    def get_year_ranges(self):
        
        ranges = []
        
        ranges.append(("2017-07-03", "2017-12-31"))

        for year in range(2018, 2026):
            ranges.append((f"{year}-01-01", f"{year}-12-31"))

        ranges.append(("2026-01-01", "2026-04-01"))

        return ranges
    
    def fetch_range_data(self, symbol, start_date, end_date, resolution):

        data = {
        "symbol": f"NSE:{symbol}-EQ",
        "resolution": resolution,
        "date_format": "1",
        "range_from": start_date,
        "range_to": end_date,
        "cont_flag": 0
    }
        
        response = self.fyers.history(data=data)
        
        if response.get("s") != "ok":
            print(f"Error fetching {symbol} from {start_date} to {end_date}: {response}")
            return []
        
        return response.get("candles", [])
    
    def fetch_full_monthly_history(self, symbol):

        all_candles = []
        year_ranges = self.get_year_ranges()

        for start, end in year_ranges:
            candles = self.fetch_range_data(symbol, start, end, "1M")
            time.sleep(1)
            all_candles.extend(candles)
            print(f"Fetched {len(candles)} months")
        
        return all_candles

    @staticmethod
    def get_ath_value(symbol):

        fy = FyersClient()
        candles = fy.fetch_full_history(symbol)

        if not candles:
            return None, None
        
        ath_candle = max(candles, key=lambda x: x[2])

        epoch = ath_candle[0]
        ath_value = ath_candle[2]
        ath_date = datetime.fromtimestamp(epoch).strftime("%Y-%m")

        return ath_value, ath_date

    def fetch_thirty_week_history(self, symbol):
        today = datetime.now()
        start = today - timedelta(days=230)
        today_str = today.strftime("%Y-%m-%d")
        start_str = start.strftime("%Y-%m-%d")

        candles = self.fetch_range_data(symbol, start_str, today_str, "1W")
        return candles[-30:]
    
    def calculate_30MA(self, symbol):
        candles = self.fetch_thirty_week_history(symbol)
        closes = [candle[4] for candle in candles]
        sum_value = sum(closes)
        sma_30 = round((sum_value / 30), 2)
        return sma_30
    
    def fetch_last_week_candle(self, symbol):
        today = datetime.now()
        start = today - timedelta(days=10)
        today_str = today.strftime("%Y-%m-%d")
        start_str = start.strftime("%Y-%m-%d")

        candles = self.fetch_range_data(symbol, start_str, today_str, "1W")
        return candles[-1:]