def detect_arbitrage(game):
    arbs = []
    home_team = game.get("home_team", "Home")
    away_team = game.get("away_team", "Away")
    teams = (home_team, away_team)

    for book1 in game.get("bookmakers", []):
        for market1 in book1.get("markets", []):
            for book2 in game.get("bookmakers", []):
                if book1["title"] == book2["title"]:
                    continue
                for market2 in book2.get("markets", []):
                    if market1["key"] != market2["key"]:
                        continue
                    try:
                        # Ensure both markets have at least 2 outcomes
                        if len(market1["outcomes"]) < 2 or len(market2["outcomes"]) < 2:
                            continue

                        outcome1 = market1["outcomes"][0]
                        outcome2 = market2["outcomes"][1]

                        o1 = outcome1["price"]
                        o2 = outcome2["price"]

                        inv_sum = (1 / o1) + (1 / o2)
                        profit_margin = (1 - inv_sum) * 100

                        if profit_margin >= 2:
                            arbs.append({
                                "teams": teams,
                                "market": market1["key"],
                                "bookmakers": (book1["title"], book2["title"]),
                                "odds": (o1, o2),
                                "profit_margin": profit_margin,
                                "outcome1": outcome1,
                                "outcome2": outcome2
                            })
                    except:
                        continue
    return arbs
