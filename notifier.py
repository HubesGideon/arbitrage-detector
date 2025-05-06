import requests
from utils import color_by_margin, american_odds

DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1367538763194171472/2fhnOWu65y1r9xnzJN_lqcSjUKj2we9J1ZVHZOUesBYt4tlOlDYT6f6HE9lmFJYGSskT"  # Replace this

def notify_discord(message):
    payload = {
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)
    if response.status_code != 204:
        raise Exception(f"Discord returned {response.status_code}: {response.text}")

def format_message(arb):
    team1, team2 = arb["teams"]
    book1, book2 = arb["bookmakers"]
    o1, o2 = arb["odds"]
    market = arb["market"]
    pm = arb["profit_margin"]
    outcome1 = arb["outcome1"]
    outcome2 = arb["outcome2"]
    point1 = outcome1.get("point")
    point2 = outcome2.get("point")

    # ⬇️ Format tournament and round info
    sport_key = arb.get("sport_key", "unknown")
    tournament_name = sport_key.replace("tennis_", "").replace("_", " ").title()

    round_name = arb.get("round", None)
    round_line = f"🎾 Round: {round_name}\n" if round_name else ""

    status_tag = "🟢 [LIVE]" if arb.get("in_play") else "⚪ [PREGAME]"
    color = color_by_margin(pm)

    # Format based on market
    if market == "spreads" and point1 is not None and point2 is not None:
        label1 = f"{book1} {point1:+}: {american_odds(o1)}"
        label2 = f"{book2} {point2:+}: {american_odds(o2)}"
    elif market == "totals" and point1 is not None:
        label1 = f"{book1} {outcome1['name']} {point1}: {american_odds(o1)}"
        label2 = f"{book2} {outcome2['name']} {point2}: {american_odds(o2)}"
    else:
        label1 = f"{book1}: {american_odds(o1)}"
        label2 = f"{book2}: {american_odds(o2)}"

    message = (
        f"{status_tag} **{color} Arbitrage Opportunity ({market})**\n"
        f"{team1} vs {team2}\n"
        f"🏟️ Tournament: {tournament_name}\n"
        f"{round_line}"
        f"{label1}  |  {label2}\n"
        f"Profit Margin: **{pm:.2f}%**"
    )
    return message
