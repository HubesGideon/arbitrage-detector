def detect_arbitrage(game):
    books = game['bookmakers']
    for i in range(len(books)):
        for j in range(i + 1, len(books)):
            try:
                team1_odds = books[i]['markets'][0]['outcomes'][0]['price']
                team2_odds = books[j]['markets'][0]['outcomes'][1]['price']
                inv_sum = (1 / team1_odds) + (1 / team2_odds)
                if inv_sum < 1:
                    return {
                        "teams": game['teams'],
                        "bookmakers": (books[i]['title'], books[j]['title']),
                        "odds": (team1_odds, team2_odds),
                        "profit_margin": (1 - inv_sum) * 100
                    }
            except:
                continue
    return None

