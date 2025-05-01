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

    total_arbs = 0
    for game in games:
        team1 = game.get("home_team", "Home")
        team2 = game.get("away_team", "Away")
        print(f"⚔️ Checking: {team1} vs {team2}")

        arbs = detect_arbitrage(game)
        if arbs:
            print(f"🔍 Found {len(arbs)} arbitrage opportunity(ies) for this game")
            for arb in arbs:
                total_arbs += 1
                print(f"➡️  {arb['market']} | {arb['bookmakers'][0]} vs {arb['bookmakers'][1]} | {arb['profit_margin']:.2f}%")
                try:
                    notify_discord(format_message(arb))
                    print("✅ Sent to Discord")
                except Exception as e:
                    print(f"[ERROR] Failed to send Discord message: {e}")
        else:
            best_margin = get_best_margin(game)
            if best_margin is not None:
                print(f"📉 Closest profit margin found: {best_margin:.2f}%")

    if total_arbs == 0:
        print("🚫 No arbitrage opportunities found this run.")

def get_best_margin(game):
    best = None
    for book1 in game.get("bookmakers", []):
        for market1 in book1.get("markets", []):
            for book2 in game.get("bookmakers", []):
                if book1["title"] == book2["title"]:
                    continue
                for market2 in book2.get("markets", []):
                    if market1["key"] != market2["key"]:
                        continue
                    try:
                        if len(market1["outcomes"]) != 2 or len(market2["outcomes"]) != 2:
                            continue
                        o1 = market1["outcomes"][0]["price"]
                        o2 = market2["outcomes"][1]["price"]
                        inv_sum = (1 / o1) + (1 / o2)
                        margin = (1 - inv_sum) * 100
                        if best is None or margin > best:
                            best = margin
                    except:
                        continue
    return best

if __name__ == "__main__":
    main()
