def get_risk_level(probability):

    if probability >= 80:
        return "🔴 High Risk"

    elif probability >= 50:
        return "🟡 Medium Risk"

    return "🟢 Low Risk"


def get_reason(text):

    spam_keywords = [

        "free",
        "winner",
        "win",
        "offer",
        "claim",
        "click",
        "reward",
        "bonus",
        "cash",
        "urgent",
        "prize",
        "limited"

    ]

    text = text.lower()

    reasons = []

    for word in spam_keywords:

        if word in text:
            reasons.append(f"Contains suspicious keyword '{word}'")

    if len(reasons) == 0:
        reasons.append("No suspicious keywords detected.")

    return reasons