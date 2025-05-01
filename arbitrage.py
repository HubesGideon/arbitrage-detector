def detect_arbitrage(game):
    arbs = []
    for book1 in game.get("bookmakers", []):
        for market1 in book1.get("markets", []):
            for book2 in game.get("bookmakers", []):
                if book1["title"] == book2["title"]:
                    continue
                for market2 in book2.get("markets", []):
                    if market1["key"] != market2["key"]:
                        continue
                    try:
                        o1 = market1["outcomes"][0]["price"]
                        o2 = market2["outcomes"][1]["price"]
                        inv_sum = (1 / o1) + (1 / o2)
                        profit_margin = (1 - inv_sum) * 100
                        if profit_margin >= 2:
                            arbs.append({
                                "teams": game["teams"],
                                "market": market1["key"],
                                "bookmakers": (book1["title"], book2["title"]),
                                "odds": (o1, o2),
                                "profit_margin": profit_margin
                            })
                    except:
                        continue
    return arbs
