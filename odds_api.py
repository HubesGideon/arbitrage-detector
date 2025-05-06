# Tennis-only arbitrage odds fetcher for May 2025

odds_api_key = "133b4b56ea3d83d2daa6e6e4a7c86737"

INCLUDED_SPORTS = [
    "tennis_atp_italian_open",
    "tennis_atp_geneva_open",
    "tennis_atp_hamburg_open",
    "tennis_atp_french_open",
    "tennis_wta_italian_open",
    "tennis_wta_strasbourg",
    "tennis_wta_morocco_open",
    "tennis_wta_french_open"
]

BOOKMAKER_WHITELIST = [
    "fanduel", "draftkings", "betmgm", "caesars", "espn", "fanatics", "mybookieag"
]

import requests

def fetch_odds():
    results = []
    for sport in INCLUDED_SPORTS:
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        params = {
            "apiKey": odds_api_key,
            "regions": "us",
            "markets": "h2h,spreads,totals",
            "oddsFormat": "decimal",
            "dateFormat": "iso",
            "bookmakers": ",".join(BOOKMAKER_WHITELIST),
            "inPlayOnly": "true"  # ✅ Live odds only
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"❌ Failed to fetch odds for {sport}: {response.status_code} - {response.text}")
            continue

        data = response.json()
        for game in data:
            game["sport_key"] = sport
            results.append(game)

    return results
