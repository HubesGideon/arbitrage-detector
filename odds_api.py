import requests
import os

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/"

def fetch_odds(markets=["h2h", "spreads", "totals"]):
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": ",".join(markets),
        "oddsFormat": "decimal"
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()
