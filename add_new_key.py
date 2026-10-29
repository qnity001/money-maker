import json

with open("watchlist_example.json", "r") as file:
    watchlist = json.load(file)

for value in watchlist.values():
    value["expiry_date"] = "2026-08"

with open("watchlist_example.json", "w") as file:
    json.dump(watchlist, file, indent=4)