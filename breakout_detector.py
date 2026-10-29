import csv
from fyers_client import FyersClient
import json
import math
import time
from datetime import datetime, timedelta

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

def detect_breakout():
    fy = FyersClient()
    symbols = get_symbol_list()
    
    try:
        with open("watchlist.json", "r") as file:
            watchlist = json.load(file)
    except FileNotFoundError:
        watchlist = {}

    with open("ath_cache.json", "r") as file:
        ath_cache = json.load(file)

    # Remove expired watchlist entries
    today = datetime.now().strftime("%Y-%m")

    for symbol in list(watchlist.keys()):
        expiry_str = watchlist[symbol].get("expiry_date", "")
        if expiry_str:
            expiry_dt = datetime.strptime(expiry_str, "%Y-%m")
            today_dt = datetime.strptime(today, "%Y-%m")
            if expiry_dt < today_dt:
                del watchlist[symbol]
                print(f"Expired: {symbol}")

    for symbol in symbols:

        candles = fy.fetch_range_data(symbol, "2026-06-01", "2026-06-30", "1M")
        candle = candles[0]
        print(candle)

        close_value = candle[4]
        if close_value > ath_cache[symbol]["ath_value"]:
            print(f"{symbol} breakout detected")

            ath_cache[symbol]["consecutive_breakouts"] += 1
            if ath_cache[symbol]["consecutive_breakouts"] >= 3:
                ath_cache[symbol]["strong_breakout"] = True

            epoch = candle[0]
            new_ath_datetime = datetime.fromtimestamp(epoch)
            new_ath_date = new_ath_datetime.strftime("%Y-%m")
            expiry_date = (new_ath_datetime + timedelta(days=93)).strftime("%Y-%m")
            breakout_class = get_month_difference(new_ath_date, ath_cache[symbol]["ath_date"])
            print(breakout_class)

            watchlist[symbol] = {
                "breakout_month": new_ath_date,
                "breakout_high": candle[2],
                "entry_trigger": math.ceil(candle[2] * 1.001),
                "breakout_class": breakout_class,
                "expiry_date": expiry_date
            }
            ath_cache[symbol]["ath_value"] = candle[2]
            ath_cache[symbol]["ath_date"] = new_ath_date
        else:
            ath_cache[symbol]["consecutive_breakouts"] = 0
            ath_cache[symbol]["strong_breakout"] = False
        time.sleep(1)

    with open("ath_cache.json", "w") as file:
        json.dump(ath_cache, file, indent=4)

    with open("watchlist.json", "w") as file:
        json.dump(watchlist, file, indent=4)

if __name__ == "__main__":
    detect_breakout()