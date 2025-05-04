def format_message(arb):
    from utils import color_by_margin, american_odds

    team1, team2 = arb["teams"]
    book1, book2 = arb["bookmakers"]
    o1, o2 = arb["odds"]
    market = arb["market"]
    pm = arb["profit_margin"]
    outcome1 = arb["outcome1"]
    outcome2 = arb["outcome2"]
    point1 = outcome1.get("point")
    point2 = outcome2.get("point")

    status_tag = "🟢 [LIVE]" if arb.get("in_play") else "⚪ [PREGAME]"
    color = color_by_margin(pm)

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
        f"{label1}  |  {label2}\n"
        f"Profit Margin: **{pm:.2f}%**"
    )
    return message
