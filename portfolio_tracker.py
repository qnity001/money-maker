from dotenv import load_dotenv
import json
import os

# This function stores active positions based on symbol and entry price
def add_active_position(symbol, entry_price):
    # Input is symbol and entry price
    # Get 30MA value by symbol input
    # Send entry and 30MA to get quantyity
    # Update active_positions.json
    pass

# This function calculates the quantity based on risk value
def calculate_quanity(entry, stoploss):
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

