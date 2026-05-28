import csv

def get_symbol_list():
    symbols = []
    with open("ind_nifty50list.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            symbols.extend(row["Symbol"])
    return symbols

from fyers_client import FyersClient

fy = FyersClient()

symbol = "WIPRO"
ath_value, ath_date = fy.get_ath_value(symbol)

print(f"Symbol: {symbol}")
print(f"ATH Value: {ath_value}")
print(f"ATH Month: {ath_date}")