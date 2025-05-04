def color_by_margin(margin):
    """
    Returns an emoji color based on profit margin:
    - 🟢 ≥ 10%
    - 🟡 ≥ 5%
    - 🔴 ≥ 2%
    """
    if margin >= 10:
        return "🟢"
    elif margin >= 5:
        return "🟡"
    elif margin >= 2:
        return "🔴"
    else:
        return ""

def american_odds(decimal_odds):
    """
    Converts decimal odds to American format (e.g., 2.40 → +140, 1.91 → -110)
    """
    if decimal_odds >= 2:
        return f"+{int((decimal_odds - 1) * 100)}"
    else:
        return f"{int(-100 / (decimal_odds - 1))}"
