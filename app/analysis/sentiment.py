"""Real news sentiment + impact analysis for PredictMind (S7.2 / S7.3).

Upgrade over the news-service's v1 keyword counter: this uses **VADER**
(Valence Aware Dictionary and sEntiment Reasoner), a lexicon-and-grammar based
sentiment model. Unlike plain word counting, VADER understands negation
("not good"), boosters ("very good"), punctuation and capitalisation. We extend
its dictionary with crypto-specific terms so words like "hack" or "halving" carry
the right weight in this domain.

All functions here are pure (text in, numbers out) so they are trivial to test
and have no I/O.
"""

from __future__ import annotations

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Extra valence for crypto vocabulary VADER doesn't know well.
# Scale is VADER's: roughly -4 (very negative) .. +4 (very positive).
CRYPTO_LEXICON: dict[str, float] = {
    # negative
    "hack": -3.0,
    "hacked": -3.2,
    "exploit": -2.6,
    "exploited": -2.6,
    "rug": -3.4,
    "rugpull": -3.6,
    "scam": -3.0,
    "ban": -2.4,
    "banned": -2.6,
    "lawsuit": -2.0,
    "sue": -1.8,
    "bearish": -2.6,
    "dump": -2.0,
    "selloff": -2.2,
    "sell-off": -2.2,
    "crash": -3.0,
    "plunge": -2.6,
    "plummet": -2.6,
    "liquidation": -1.8,
    "liquidated": -1.8,
    "fud": -2.0,
    "delisted": -2.6,
    "fraud": -3.0,
    # positive
    "bullish": 2.6,
    "rally": 2.0,
    "rallies": 2.0,
    "surge": 2.2,
    "surges": 2.2,
    "soar": 2.4,
    "soars": 2.4,
    "moon": 2.2,
    "adoption": 1.6,
    "approval": 2.0,
    "approved": 2.0,
    "halving": 1.2,
    "partnership": 1.6,
    "upgrade": 1.2,
    "breakout": 1.6,
    "ath": 2.0,
    "rebound": 1.6,
}

# Terms that make a story market-moving regardless of direction (impact, not mood).
HIGH_IMPACT_TERMS: frozenset[str] = frozenset(
    {
        "sec",
        "etf",
        "halving",
        "regulation",
        "regulatory",
        "lawsuit",
        "hack",
        "ban",
        "crash",
        "fed",
        "court",
        "bankruptcy",
        "default",
        "approval",
    }
)

# Coins we recognise -> extra names/aliases to look for in text.
COIN_ALIASES: dict[str, list[str]] = {
    "BTC": ["bitcoin"],
    "ETH": ["ethereum", "ether"],
    "BNB": ["binance coin"],
    "SOL": ["solana"],
    "XRP": ["ripple"],
    "DOGE": ["dogecoin"],
    "ADA": ["cardano"],
    "AVAX": ["avalanche"],
    "MATIC": ["polygon"],
    "DOT": ["polkadot"],
}

# One shared analyzer, with our crypto words merged into VADER's dictionary.
_analyzer = SentimentIntensityAnalyzer()
_analyzer.lexicon.update(CRYPTO_LEXICON)

# VADER's conventional thresholds on the compound score (-1 .. +1).
_POSITIVE_THRESHOLD = 0.05
_NEGATIVE_THRESHOLD = -0.05


def compound_score(text: str) -> float:
    """VADER compound sentiment for text: -1 (very negative) .. +1 (very positive)."""
    if not text.strip():
        return 0.0
    return _analyzer.polarity_scores(text)["compound"]


def classify(text: str) -> str:
    """Map a compound score to positive / negative / neutral."""
    score = compound_score(text)
    if score >= _POSITIVE_THRESHOLD:
        return "positive"
    if score <= _NEGATIVE_THRESHOLD:
        return "negative"
    return "neutral"


def _tokens(text: str) -> set[str]:
    return {word for word in text.lower().replace("-", " ").split()}


def score_impact(text: str) -> int:
    """How market-moving is this story? 0-100.

    Blends sentiment *intensity* (a strong opinion moves markets more) with the
    presence of high-impact entities (SEC, ETF, hack, ...).
    """
    if not text.strip():
        return 0
    intensity = abs(compound_score(text)) * 40.0  # 0..40
    words = _tokens(text)
    hits = len(words & HIGH_IMPACT_TERMS)
    entity = min(60.0, hits * 20.0)  # 0..60
    return round(min(100.0, intensity + entity))


def impact_level(score: int) -> str:
    """Bucket a 0-100 impact score into the severity words (FR-011)."""
    if score >= 75:
        return "CRITICAL"
    if score >= 50:
        return "HIGH"
    if score >= 25:
        return "MEDIUM"
    return "LOW"


def detect_symbols(text: str) -> list[str]:
    """Which known coins does this text mention (by symbol or alias)?"""
    lower = text.lower()
    words = _tokens(text)
    found: list[str] = []
    for symbol, aliases in COIN_ALIASES.items():
        if symbol.lower() in words or any(alias in lower for alias in aliases):
            found.append(symbol)
    return found


def aggregate(texts: list[str]) -> dict[str, int]:
    """Aggregate a batch of texts into { bullish, bearish, neutral, confidence }.

    Confidence rises with how many texts we have and how strongly opinionated
    they are (average absolute compound), capped at 100.
    """
    total = len(texts)
    if total == 0:
        return {"bullish": 0, "bearish": 0, "neutral": 0, "confidence": 0}

    positive = 0
    negative = 0
    abs_sum = 0.0
    for text in texts:
        score = compound_score(text)
        abs_sum += abs(score)
        if score >= _POSITIVE_THRESHOLD:
            positive += 1
        elif score <= _NEGATIVE_THRESHOLD:
            negative += 1
    neutral = total - positive - negative
    avg_abs = abs_sum / total
    confidence = round(min(100.0, 30 + total * 4 + avg_abs * 40))

    return {
        "bullish": round(positive / total * 100),
        "bearish": round(negative / total * 100),
        "neutral": round(neutral / total * 100),
        "confidence": confidence,
    }
