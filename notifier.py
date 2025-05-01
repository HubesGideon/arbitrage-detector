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

def format_message(arb):
    team1, team2 = arb["teams"]
    book1, book2 = arb["bookmakers"]
    odd1, odd2 = arb["odds"]
    margin = arb["profit_margin"]

    return (
        f"{color_by_margin(margin)} Arbitrage Opportunity ({arb['market']})\n"
        f"{team1} vs {team2}\n"
        f"{book1}: {decimal_to_american(odd1)} | {book2}: {decimal_to_american(odd2)}\n"
        f"Profit Margin: {margin:.2f}%"
    )

def notify_discord(message):
    payload = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"[ERROR] Failed to send Discord message: {e}")
