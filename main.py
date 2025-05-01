from odds_api import fetch_odds
from arbitrage import detect_arbitrage
from notifier import notify_discord, format_message

def main():
    print("🟡 Starting arbitrage scan...")
    games = fetch_odds()
    print(f"📦 Retrieved {len(games)} games")
    
    found = 0
    for game in games:
        arbs = detect_arbitrage(game)
        for arb in arbs:
            found += 1
            print(f"🔍 Arbitrage found: {arb['teams']} - {arb['profit_margin']:.2f}%")
            notify_discord(format_message(arb))
    
    if found == 0:
        print("🚫 No arbitrage opportunities found this run.")

if __name__ == "__main__":
    main()
