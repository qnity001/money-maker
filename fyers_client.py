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