import requests

# 🔐 Your Odds API Key
odds_api_key = "133b4b56ea3d83d2daa6e6e4a7c86737"

# 🎾 All supported tennis tournaments
INCLUDED_SPORTS = [
    "tennis_atp_aus_open_singles",
    "tennis_atp_canadian_open",
    "tennis_atp_china_open",
    "tennis_atp_cincinnati_open",
    "tennis_atp_dubai",
    "tennis_atp_french_open",
    "tennis_atp_indian_wells",
    "tennis_atp_madrid_open",
    "tennis_atp_miami_open",
    "tennis_atp_monte_carlo_masters",
    "tennis_atp_paris_masters",
    "tennis_atp_qatar_open",
    "tennis_atp_shanghai_masters",
    "tennis_atp_us_open",
    "tennis_atp_wimbledon",
    "tennis_wta_aus_open_singles",
    "tennis_wta_canadian_open",
    "tennis_wta_china_open",
    "tennis_wta_cincinnati_open",
    "tennis_wta_dubai",
    "tennis_wta_french_open",
    "tennis_wta_indian_wells",
    "tennis_wta_madrid_open",
    "tennis_wta_miami_open",
    "tennis_wta_qatar_open",
    "tennis_wta_us_open",
    "tennis_wta_wimbledon",
    "tennis_wta_wuhan_open"
]

# ✅ Legal Kansas books + MyBookie
BOOKMAKER_WHITELIST = [
    "fanduel",
    "draftkings",
    "betmgm",
    "caesars",
    "espn",
    "fanatics",
    "mybookieag"
]

def fetch_odds():
    results = []
    for sport in INCLUDED_SPORTS:
        print(f"🔎 Fetching odds for: {sport}")
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        params = {
            "apiKey": odds_api_key,
            "regions": "us",
            "markets": "h2h,spreads,totals",
            "oddsFormat": "decimal",
            "dateFormat": "iso",
            "bookmakers": ",".join(BOOKMAKER_WHITELIST),
            "inPlayOnly": "false"  # ✅ Testing live + pregame
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"❌ Failed for {sport}: {response.status_code} - {response.text}")
            continue

        data = response.json()
        print(f"📦 {sport} returned {len(data)} game(s)")
        for game in data:
            game["sport_key"] = sport
            results.append(game)

    print(f"✅ Total games found: {len(results)}")
    return results

