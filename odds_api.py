import requests
import os

API_KEY = os.getenv("ODDS_API_KEY")

# Specify markets per sport
SPORT_MARKETS = {
    "baseball_mlb": ["h2h", "spreads", "totals"],
    "soccer_epl": ["spreads", "totals"]  # ⚠️ h2h skipped due to 3-way
}

REGION = "us"
BOOKMAKERS = [
    "betmgm", "williamhill_us", "draftkings",
    "fanduel", "fanatics", "espnbet", "mybookieag"
]

def fetch_odds():
    all_odds = []
    for sport, markets in SPORT_MARKETS.items():
        for market in markets:
            url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
            params = {
                "apiKey": API_KEY,
                "regions": REGION,
                "markets": market,
                "oddsFormat": "decimal",
                "bookmakers": ",".join(BOOKMAKERS)
            }
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                all_odds.extend(response.json())
            except Exception as e:
                print(f"[ERROR] Failed to fetch odds for {sport} ({market}): {e}")
    return all_odds
