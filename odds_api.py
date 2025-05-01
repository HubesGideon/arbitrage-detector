import requests
import os

API_KEY = os.getenv("ODDS_API_KEY")
SPORT_KEYS = ["baseball_mlb", "soccer_epl"]
MARKETS = ["h2h", "spreads", "totals"]
REGION = "us"
BOOKMAKERS = [
    "betmgm", "williamhill_us", "draftkings",
    "fanduel", "fanatics", "espnbet", "mybookieag"
]

def fetch_odds():
    all_odds = []
    for sport in SPORT_KEYS:
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        params = {
            "apiKey": API_KEY,
            "regions": REGION,
            "markets": ",".join(MARKETS),
            "oddsFormat": "decimal",
            "bookmakers": ",".join(BOOKMAKERS)
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            all_odds.extend(response.json())
        except Exception as e:
            print(f"[ERROR] Failed to fetch odds for {sport}: {e}")
    return all_odds
