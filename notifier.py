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
        return "🟢"
    elif margin >= 5:
        return "🟡"
    else:
        return "🔴"

def format_line_label(outcome, market_type):
    name = outcome.get("name", "")
    line = outcome.get("point")
    if market_type == "totals" and line is not None:
        return f"{name} {line:.1f}"  # e.g., Over 2.5
    elif market_type == "spreads" and line is not None:
        sign = "+" if line > 0 else ""
        return f"{name} {sign}{line:.1f}"  # e.g., Team +3.5
    return name

def format_message(arb):
    team1, team2 = arb["teams"]
    book1, book2 = arb["bookmakers"]
    o1, o2 = arb["odds"]
    margin = arb["profit_margin"]
    market = arb["market"]
    outcome1 = arb.get("outcome1", {})
    outcome2 = arb.get("outcome2", {})

    if market in ["spreads", "totals"]:
        label1 = format_line_label(outcome1, market)
        label2 = format_line_label(outcome2, market)
        odds1 = decimal_to_american(o1)
        odds2 = decimal_to_american(o2)
        odds_text = f"{book1} {label1}: {odds1} | {book2} {label2}: {odds2}"
    else:
        odds_text = f"{book1}: {decimal_to_american(o1)} | {book2}: {decimal_to_american(o2)}"

    return (
        f"{color_by_margin(margin)} Arbitrage Opportunity ({market})\n"
        f"{team1} vs {team2}\n"
        f"{odds_text}\n"
        f"Profit Margin: {margin:.2f}%"
    )

def notify_discord(message):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"[ERROR] Failed to send Discord message: {e}")
