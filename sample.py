# This file contains a sample code for getting the historical data for 1 symbol

from dotenv import load_dotenv
import os
from fyers_apiv3 import fyersModel
from fyers_client import FyersClient
from datetime import timedelta, datetime

load_dotenv()

client_id = os.getenv("CLIENT_ID")
access_token = os.getenv("ACCESS_TOKEN")

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

def get_monthly_ranged_data(symbol):
    data = {
        "symbol":f"NSE:{symbol}-EQ",
        "resolution":"M",
        "date_format":"1",
        "range_from":"2026-05-01",
        "range_to":"2026-05-31",
        "cont_flag":"0"
    }

    response = fyers.history(data=data)
    print(response)

def get_ath_of_symbol(symbol):
    print(FyersClient.get_ath_value(symbol))

def get_30_weeks_data(symbol):
    today = datetime.now()
    start = today - timedelta(days=230)
    today_str = today.strftime("%Y-%m-%d")
    start_str = start.strftime("%Y-%m-%d")

    data = {
        "symbol":f"NSE:{symbol}-EQ",
        "resolution":"1W",
        "date_format":"1",
        "range_from":start_str,
        "range_to": today_str,
        "cont_flag":"0"
    }

    response = fyers.history(data=data)
        
    if response.get("s") != "ok":
        print(f"Error fetching {symbol} from {start_str} to {today_str}: {response}")
        return []
        
    candles = response.get("candles", [])
    return candles[-30:]

def calculate_30MA(symbol):
        candles = get_30_weeks_data(symbol)
        closes = [candle[4] for candle in candles]
        sum_value = sum(closes)
        sma_30 = round((sum_value / 30), 2)
        print(sma_30)

if __name__ == "__main__":
    symbol = "WELCORP"
    #get_monthly_ranged_data(symbol)
    calculate_30MA(symbol)