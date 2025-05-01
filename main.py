from odds_api import fetch_odds
from arbitrage import detect_arbitrage
from notifier import notify_discord

def main():
    games = fetch_odds()
    for game in games:
        arb = detect_arbitrage(game)
        if arb:
            msg = (
                f"🟢 Arbitrage Opportunity!\n"
                f"{arb['teams'][0]} vs {arb['teams'][1]}\n"
                f"Bookmakers: {arb['bookmakers']}\n"
                f"Odds: {arb['odds']}\n"
                f"Profit Margin: {arb['profit_margin']:.2f}%"
            )
            notify_discord(msg)

if __name__ == "__main__":
    main()

