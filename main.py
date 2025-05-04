import time
from odds_api import fetch_odds
from arbitrage import detect_arbitrage
from notifier import notify_discord, format_message
from datetime import datetime

LIVE_GAME_MARGIN_THRESHOLD = 10  # percent

def log_arb_metadata(arb):
    game_time = arb.get("start_time", "N/A")
    is_live = arb.get("in_play", False)
    book1, book2 = arb["bookmakers"]
    o1 = arb["outcome1"]
    o2 = arb["outcome2"]

    last_update_1 = arb.get("book1_last_update", "N/A")
    last_update_2 = arb.get("book2_last_update", "N/A")

    print(f"🕒 Game Time: {game_time}")
    print(f"📡 Live Game: {'Yes' if is_live else 'No'}")
    print(f"📊 Bookmakers: {book1} vs {book2}")
    print(f"📆 Last Update (Book 1): {last_update_1}")
    print(f"📆 Last Update (Book 2): {last_update_2}")
    print(f"💰 Odds: {book1}: {arb['odds'][0]} | {book2}: {arb['odds'][1]}")
    print(f"📈 Profit Margin: {arb['profit_margin']:.2f}%")
    print("-" * 60)

def main():
    print("🟡 Starting arbitrage scan...")
    games = fetch_odds()
    print(f"📦 Retrieved {len(games)} games")

    total_arbs = 0
    for game in games:
        arbs = detect_arbitrage(game)
        for arb in arbs:
            is_live = arb.get("in_play", False)
            margin = arb["profit_margin"]

            # Filter: only allow live games if margin ≥ threshold
            if is_live and margin < LIVE_GAME_MARGIN_THRESHOLD:
                continue

            status = "LIVE" if is_live else "PREGAME"
            print(f"⚔️ Checking ({status}): {arb['teams'][0]} vs {arb['teams'][1]}")
            log_arb_metadata(arb)

            try:
                message = format_message(arb)
                notify_discord(message)
                print("✅ Sent to Discord")
            except Exception as e:
                print(f"[ERROR] Failed to send Discord message: {e}")

            total_arbs += 1

    if total_arbs == 0:
        print("🚫 No arbitrage opportunities found this run.")
    else:
        print(f"✅ Total arbitrage alerts sent: {total_arbs}")

if __name__ == "__main__":
    main()
