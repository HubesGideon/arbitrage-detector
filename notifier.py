def format_message(arb):
    team1, team2 = arb["teams"]
    book1, book2 = arb["bookmakers"]
    odds1, odds2 = arb["odds"]
    return (
        f"🟢 Arbitrage Opportunity ({arb['market']})!\n"
        f"{team1} vs {team2}\n"
        f"{book1}: {odds1} | {book2}: {odds2}\n"
        f"Profit Margin: {arb['profit_margin']:.2f}%"
    )
