from odds_api import fetch_odds
from arbitrage import detect_arbitrage
from notifier import notify_discord, format_message

def main():
    print("🟡 Starting arbitrage scan...")

    try:
        games = fetch_odds()
        print(f"📦 Retrieved {len(games)} games")
    except Exception as e:
        print(f"[ERROR] Failed to fetch odds: {e}")
        return

    found = 0
    for game in games:
        arbs = detect_arbitrage(game)
        if arbs:
            print(f"🔍 {len(arbs)} arbitrage opportunity(ies) found for: {game['teams']}")
        for arb in arbs:
            found += 1
            print(f"➡️  {arb['market']} | {arb['bookmakers'][0]} vs {arb['bookmakers'][1]} | {arb['profit_margin']:.2f}%")
            try:
                notify_discord(format_message(arb))
                print("✅ Sent to Discord")
            except Exception as e:
                print(f"[ERROR] Failed to send Discord message: {e}")

    if found == 0:
        print("🚫 No arbitrage opportunities found this run.")

if __name__ == "__main__":
    main()
