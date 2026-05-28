# This file contains a sample code for getting the historical data for 1 symbol from any start date to end date

from dotenv import load_dotenv
import os
from fyers_apiv3 import fyersModel

load_dotenv()

client_id = os.getenv("CLIENT_ID")
access_token = os.getenv("ACCESS_TOKEN")

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

data = {
    "symbol":"NSE:WIPRO-EQ",
    "resolution":"M",
    "date_format":"1",
    "range_from":"2024-01-01",
    "range_to":"2024-12-31",
    "cont_flag":"0"
}

response = fyers.history(data=data)
print(response)

