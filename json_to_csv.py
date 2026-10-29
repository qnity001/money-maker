import json
import csv

# Load JSON
with open("watchlist.json", "r") as f:
    data = json.load(f)

rows = []
for idx, (symbol, details) in enumerate(data.items(), start=1):
    row = {
        "s_no": idx,
        "symbol": symbol,
        "breakout_month": details.get("breakout_month", ""),
        "breakout_high": details.get("breakout_high", ""),
        "entry_trigger": details.get("entry_trigger", ""),
        "breakout_class": details.get("breakout_class", ""),
        "expiry_date": details.get("expiry_date", "")
    }
    rows.append(row)

# Write CSV
with open("watchlist.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Converted {len(rows)} entries to watchlist.csv")