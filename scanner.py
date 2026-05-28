from fyers_client import FyersClient

fy = FyersClient()

symbol = "WIPRO"
ath_value, ath_date = fy.get_ath_value(symbol)

print(f"Symbol: {symbol}")
print(f"ATH Value: {ath_value}")
print(f"ATH Month: {ath_date}")