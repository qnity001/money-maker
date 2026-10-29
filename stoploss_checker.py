from datetime import datetime,  timedelta
from fyers_client import FyersClient
import json

with open("ath_cache.json", "r") as file:
    ath_cache = json.load(file)

with open("active_positions.json", "r") as file:
    active_positions = json.load(file)

try:
    with open("exited_positions.json", "r") as file:
        exited_positions = json.load(file)
except FileNotFoundError:
    exited_positions = {}

fy = FyersClient()

for symbol, fields in active_positions.items():
    sma_30 = fy.calculate_30MA(symbol)
    this_week_candle = fy.fetch_last_week_candle(symbol)
    this_week_close = this_week_candle[4]

    if this_week_close < sma_30:
        if symbol not in exited_positions:
            exited_positions[symbol] = []
        exited_positions[symbol].append({
            "entry_date": active_positions[symbol]["entry_date"],
            "exit_date": (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "entry_price": active_positions[symbol]["entry_price"],
            "exit_price": sma_30, # Exit price
            "quantity": active_positions[symbol]["quantity"],
            "original_breakout_class": active_positions[symbol]["breakout_class"],
            "pnl": active_positions[symbol]["quantity"] * (sma_30 - active_positions[symbol]["entry_price"])
        })
        
        # Remove from active positions
        del active_positions[symbol]

        # Update ath_cache of active_position to false
        ath_cache[symbol]["active_position"] = False

    else:
        # Change stoploss price in active positions to the new 30ma price
        active_positions[symbol]["stoploss"] = sma_30

    # json.dump exited_positions
    with open("exited_positions.json", "w") as file:
        json.dump(exited_positions, file, indent=4)

    # json.dump ath_cache
    with open("ath_cache.json", "w") as file:
        json.dump(ath_cache, file, indent=4)
        
    # json.dump active_positions
    with open("active_positions.json", "w") as file:
        json.dump(active_positions, file, indent=4)
