from odds_api import fetch_odds
from arbitrage import detect_arbitrage
from notifier import notify_discord, format_message

def main():
    games = fetch_odds()
    for game in games:
        arbs = detect_arbitrage(game)
        for arb in arbs:
            notify_discord(format_message(arb))

if __name__ == "__main__":
    main()
