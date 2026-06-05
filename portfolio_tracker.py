from dotenv import load_dotenv
from datetime import datetime
from fyers_client import FyersClient
import json
import os

fy = FyersClient()

# This function stores active positions based on symbol and entry price
def add_active_position(symbol, entry_price, fy):
    thirty_ma_value = fy.calculate_30MA(symbol)
    quantity = calculate_quantity(entry_price, thirty_ma_value)
    investment_amount = entry_price * quantity

    if entry_price <= thirty_ma_value:
        raise ValueError("Entry price must be above stop loss")

    if quantity <= 0:
        raise ValueError("Invalid quantity calculated")

    try:
        with open("active_positions.json", "r") as file:
            active_positions = json.load(file)
    except FileNotFoundError:
        active_positions = {}

    active_positions[symbol] = {
        "entry_price": entry_price,
        "stop_loss": thirty_ma_value,
        "quantity": quantity,
        "entry_date": datetime.today().strftime("%Y-%m-%d"),
        "investment_amount": investment_amount
    }

    with open("active_positions.json", "w") as file:
        json.dump(active_positions, file, indent=4)
    print("{symbol} bought successfully and added to active positions")

# This function calculates the quantity based on risk value
def calculate_quantity(entry, stoploss):
    load_dotenv()
    portfolio_value = os.getenv("PORTFOLIO_VALUE")
    risk_per_trade = portfolio_value * 0.01
    risk_for_symbol = entry - stoploss
    return risk_per_trade / risk_for_symbol

# This function updates the watchlist for active positions
def update_watchlist(symbol):
    with open("watchlist.json", "r") as file:
        watchlist = json.load(file)
    
    deleted = watchlist.pop(symbol, None)

    with open("watchlist.json", "w") as file:
        json.dump(file)

