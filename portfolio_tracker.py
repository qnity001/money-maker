# This function stores active positions based on symbol and entry price
def add_active_position(symbol, entry_price):
    # Input is symbol and entry price
    # Get 30MA value by symbol input
    # Send entry and 30MA to get quantyity
    # Update active_positions.json
    pass

# This function calcualte the 30MA value based on 30 weeks candle
def calculate_30MA(symbol):
    # Call Fyers API (class) to get 30 week data candles
    # Update Fyers Client to return the 30 week data
    # Calculate the mean of 30 candles
    pass

# This function calculates the quantity based on risk value
def calculate_quanity(entry, stoploss):
    # Get portfolio value from .env
    # Calculate risk_per_trade = portfolio_value * 0.01
    # Calculate risk_for_symbol = entry - stoploss
    # Return qty = risk_per_trade / risk_for_symbol
    pass

# This function updates the watchlist for active positions
def update_watchlist(symbol):
    # Load watchlist.json
    # Remove the symbol key from watchlist json
    pass

