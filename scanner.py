import yfinance as yf

ticker = yf.Ticker("APOLLOHOSP.NS")
data = ticker.history(period="max")
ath_date = data['High'].idxmax()
print(f"ATH date: {ath_date}")
print(data['High'].max())