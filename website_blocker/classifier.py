"""Pattern recognition: keyword-pattern scoring of page text into categories."""
import re

# Edit/extend these patterns freely.
CATEGORIES = {
    "social": ["follow", "followers", "timeline", "retweet", "story", "reels", "friends", "like and share"],
    "gaming": ["play now", "multiplayer", "leaderboard", "esports", "gameplay", "download game"],
    "gambling": ["casino", "betting", "jackpot", "poker", "slots", "wager", "sportsbook"],
    "video": ["watch now", "subscribe", "trending videos", "streaming", "episodes", "watch free"],
    "shopping": ["add to cart", "buy now", "free shipping", "deal of the day", "checkout"],
    "adult": ["adult content", "18+", "xxx", "nsfw"],
}


def score(text: str) -> dict:
    """Return {category: number of pattern hits}."""
    text = text.lower()
    result = {}
    for cat, patterns in CATEGORIES.items():
        hits = sum(len(re.findall(r"\b" + re.escape(p) + r"\b", text)) for p in patterns)
        if hits:
            result[cat] = hits
    return result


def classify(text: str, threshold: int = 3):
    """Categories whose hit count reaches the threshold, best first."""
    scores = score(text)
    matched = {c: n for c, n in scores.items() if n >= threshold}
    return sorted(matched.items(), key=lambda kv: kv[1], reverse=True), scores
