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

        for year in range(2018, 2025):
            ranges.append((f"{year}-01-01", f"{year}-12-31"))

        ranges.append(("2026-01-01", "2026-04-01"))

        return ranges