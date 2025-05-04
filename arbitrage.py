def detect_arbitrage(game):
    from collections import defaultdict

    arbs = []
    home_team = game.get("home_team", "Home")
    away_team = game.get("away_team", "Away")
    teams = (home_team, away_team)

    best_by_side = defaultdict(dict)

    for book1 in game.get("bookmakers", []):
        for market1 in book1.get("markets", []):
            for book2 in game.get("bookmakers", []):
                if book1["title"] == book2["title"]:
                    continue
                for market2 in book2.get("markets", []):
                    if market1["key"] != market2["key"]:
                        continue
                    try:
                        outcomes1 = {o.get("name"): o for o in market1.get("outcomes", [])}
                        outcomes2 = {o.get("name"): o for o in market2.get("outcomes", [])}

                        if home_team not in outcomes1 or away_team not in outcomes2:
                            continue

                        outcome1 = outcomes1[home_team]
                        outcome2 = outcomes2[away_team]

                        o1 = outcome1["price"]
                        o2 = outcome2["price"]

                        market_type = market1["key"]
                        point1 = outcome1.get("point")
                        point2 = outcome2.get("point")

                        # Skip mirror spreads
                        if market_type == "spreads":
                            if point1 is None or point2 is None:
                                continue
                            if abs(point1) != abs(point2) or (point1 > 0) == (point2 > 0):
                                continue

                        # Skip mismatched totals
                        if market_type == "totals":
                            if point1 is None or point2 is None:
                                continue
                            if point1 != point2:
                                continue

                        inv_sum = (1 / o1) + (1 / o2)
                        profit_margin = (1 - inv_sum) * 100

                        if profit_margin >= 2:
                            # Deduplication key
                            if market_type == "spreads":
                                key = (market_type, outcome1.get("name", ""), point1, book1["title"])
                            elif market_type == "totals":
                                key = (market_type, outcome1.get("name", ""), point1, book1["title"])
                            elif market_type == "h2h":
                                underdog_team = outcome1["name"] if o1 > o2 else outcome2["name"]
                                key = ("h2h", underdog_team)
                            else:
                                key = (market_type, book1["title"])

                            existing = best_by_side.get(key)
                            if not existing or profit_margin > existing["profit_margin"]:
                                best_by_side[key] = {
                                    "teams": teams,
                                    "market": market_type,
                                    "bookmakers": (book1["title"], book2["title"]),
                                    "odds": (o1, o2),
                                    "profit_margin": profit_margin,
                                    "outcome1": outcome1,
                                    "outcome2": outcome2
                                }
                    except:
                        continue

    return list(best_by_side.values())
