from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from fyers_client import FyersClient
import json
import time

def get_symbol_list():
    symbols = []
    with open("ind_nifty500list.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            symbols.append(row["Symbol"])
    return symbols

def create_ath_cache():

    symbols = get_symbol_list()
    ath_cache = {}

    with ThreadPoolExecutor(max_workers=3) as executor:
        
        futures = []
        for symbol in symbols:
            print(symbol)
            future = executor.submit(FyersClient.get_ath_value, symbol)
            future.symbol = symbol
            futures.append(future)
            time.sleep(0.5)

        for future in as_completed(futures):
            symbol = future.symbol
            try:
                ath_value, ath_date = future.result()
                ath_cache[symbol] = {
                    "ath_value": ath_value,
                    "ath_date": ath_date
                }
            except:
                ath_cache[symbol] = {
                    "ath_value": None,
                    "ath_date": None
                }

    with open("ath_cache.json", "w") as file:
        json.dump(ath_cache, file, indent=4)

    print("ATH Values stored in JSON successfully")

if __name__ == "__main__":
    create_ath_cache()