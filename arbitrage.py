def detect_arbitrage(game):
    arbs = []
    for market in game.get("bookmakers", []):
        for sub_market in market.get("markets", []):
            market_type = sub_market["key"]
            outcomes = sub_market["outcomes"]
            if len(outcomes) != 2:
                continue
            arbs += compare_with_other_books(game, market_type, sub_market, market["title"])
    return arbs

def compare_with_other_books(game, market_type, base_market, base_bookmaker_name):
    arbs_found = []
    base_outcomes = base_market["outcomes"]
    for book in game.get("bookmakers", []):
        for market in book.get("markets", []):
            if market["key"] != market_type:
                continue
            outcomes = market["outcomes"]
            if len(outcomes) != 2:
                continue
            try:
                inv_sum = (1 / base_outcomes[0]["price"]) + (1 / outcomes[1]["price"])
                if inv_sum < 1:
                    arbs_found.append({
                        "teams": game["teams"],
                        "market": market_type,
                        "bookmakers": (base_bookmaker_name, book["title"]),
                        "odds": (base_outcomes[0]["price"], outcomes[1]["price"]),
                        "profit_margin": (1 - inv_sum) * 100
                    })
            except:
                continue
    return arbs_found
