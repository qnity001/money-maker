import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel

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
    
    def fetch_one_year_data(self, symbol, start_date, end_date):

        data = {
        "symbol": f"NSE:{symbol}-EQ",
        "resolution": "1M",
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
    
    def fetch_full_history(self, symbol):

        all_candles = []
        year_ranges = self.get_year_ranges()

        for start, end in year_ranges:
            candles = self.fetch_one_year_data(symbol, start, end)
            all_candles.extend(candles)
            print(f"Fetched {len(candles)} months")
        
        return all_candles

    def get_ath_value(self, symbol):

        candles = self.fetch_full_history(symbol)

        if not candles:
            return None, None
        
        ath_candle = max(candles, key=lambda x: x[2])

        epoch = ath_candle[0]
        ath_value = ath_candle[2]
        ath_date = datetime.fromtimestamp(epoch).strftime("%Y-%m")

        return ath_value, ath_date

