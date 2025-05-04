import requests
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def decimal_to_american(odds):
    if odds >= 2.0:
        return f"+{int((odds - 1) * 100)}"
    else:
        return f"-{int(100 / (odds - 1))}"

def color_by_margin(margin):
    if margin >= 10:
        return "🟢"  # Green
    elif margin >= 5:
        return "🟡"  # Yellow
    else:
        return "🔴"  # Red

def format_outcome(bookmaker_data, outcome_index, market_type):
    try:
        outcome = bookmaker_data["markets"][0]["outcomes"][outcome_index]
        name = outcome.get("name", "")
        line = outcome.get("point")
        price = outcome["price"]
        american_odds = decimal_to_american(price)

        label = name
        if market_type == "totals":
            # name is typically 'Over' or 'Under'
            if line is not None:
                label = f"{name} {line:.1f}"
        elif market_type == "spreads":
            # name is team name, line is point spread
            if line is not None:
                sign = "+" if line > 0 else ""
                label = f"{name} {sign}{line:.1f}"

        return f"{bookmaker_data['title']} {label.strip()}: {american_odds}"
    except:
        return f"{bookmaker_data['title']}: ERR"

def format_message(arb):
    team1, team2 = arb["teams"]
    book1, book2 = arb["bookmakers"]
    o1, o2 = arb["odds"]
    margin = arb["profit_margin"]
    market = arb["market"]

    if market in ["spreads", "totals"]:
        line1 = format_outcome({"title": book1, "markets": [{"outcomes": [{"price": o1}]}]}, 0, market)
        line2 = format_outcome({"title": book2, "markets": [{"outcomes": [{"price": o2}]}]}, 1, market)
        odds_text = f"{line1} | {line2}"
    else:
        odds_text = f"{book1}: {decimal_to_american(o1)} | {book2}: {decimal_to_american(o2)}"

    return (
        f"{color_by_margin(margin)} Arbitrage Opportunity ({market})\n"
        f"{team1} vs {team2}\n"
        f"{odds_text}\n"
        f"Profit Margin: {margin:.2f}%"
    )

def notify_discord(message):
    payload = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"[ERROR] Failed to send Discord message: {e}")
