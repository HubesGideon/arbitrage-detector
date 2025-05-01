import requests
import os

API_KEY = os.getenv("ODDS_API_KEY")

def fetch_odds():
    url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/"
    params = {
        'apiKey': API_KEY,
        'regions': 'us',
        'markets': 'h2h',
        'oddsFormat': 'decimal'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

