import csv
from fyers_client import FyersClient
import json
import time
from datetime import datetime

def get_symbol_list():
    symbols = []
    with open("ind_nifty500list.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            symbols.append(row["Symbol"])
    return symbols

def get_month_difference(date1, date2):
    parsed_date1 = datetime.strptime(date1, "%Y-%m")
    parsed_date2 = datetime.strptime(date2, "%Y-%m")

    difference = (parsed_date1.year - parsed_date2.year) * 12 + (parsed_date1.month - parsed_date2.month)
    if difference >= 30:
        return f"A Class Breakout ({difference} months)"
    elif difference > 3:
        return f"B Class Breakout ({difference} months)"
    else:
        return f"C Class Breakout ({difference} months)"

fy = FyersClient()
symbols = get_symbol_list()
watchlist = {}

with open("ath_cache.json", "r") as file:
    ath_cache = json.load(file)

for symbol in symbols:

    candles = fy.fetch_range_data(symbol, "2026-05-01", "2026-05-31")
    candle = candles[0]
    print(candle)

    close_value = candle[4]
    if close_value > ath_cache[symbol]["ath_value"]:
        print(f"{symbol} breakout detected")

        epoch = candle[0]
        ath_date = datetime.fromtimestamp(epoch).strftime("%Y-%m")
        print(f"ATH Month: {ath_date}")
        breakout_class = get_month_difference(ath_date, ath_cache[symbol]["ath_date"])
        print(breakout_class)

        watchlist[symbol] = {
            "breakout_month": ath_date,
            "breakout_high": candle[2],
            "entry_trigger": candle[2] * 1.01,
            "breakout_class": breakout_class
        }
        ath_cache[symbol] = {
            "ath_value": candle[2],
            "ath_date": ath_date
        }
    time.sleep(1)

with open("ath_cache.json", "w") as file:
    json.dump(ath_cache, file, indent=4)

with open("watchlist.json", "w") as file:
    json.dump(watchlist, file, indent=4)
