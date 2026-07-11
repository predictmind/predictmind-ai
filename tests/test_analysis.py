from app.analysis import sentiment


def test_classify_positive():
    assert sentiment.classify("Bitcoin rallies to a record high on ETF approval") == "positive"


def test_classify_negative():
    assert sentiment.classify("Major exchange hacked; token price crashes") == "negative"


def test_classify_neutral_or_empty():
    assert sentiment.classify("") == "neutral"


def test_crypto_lexicon_makes_hack_negative():
    # Plain VADER barely reacts to "hack"; our lexicon should push it negative.
    assert sentiment.compound_score("protocol hack") < 0


def test_impact_scores_strong_news_higher():
    strong = sentiment.score_impact("SEC lawsuit and hack trigger market crash")
    mild = sentiment.score_impact("Project publishes a small blog update")
    assert strong > mild
    assert 0 <= strong <= 100


def test_impact_level_buckets():
    assert sentiment.impact_level(0) == "LOW"
    assert sentiment.impact_level(30) == "MEDIUM"
    assert sentiment.impact_level(60) == "HIGH"
    assert sentiment.impact_level(90) == "CRITICAL"


def test_detect_symbols_by_symbol_and_name():
    found = sentiment.detect_symbols("BTC and Ethereum both rise")
    assert "BTC" in found
    assert "ETH" in found


def test_detect_symbols_none():
    assert sentiment.detect_symbols("General stock market news") == []


def test_aggregate_empty():
    assert sentiment.aggregate([]) == {
        "bullish": 0,
        "bearish": 0,
        "neutral": 0,
        "confidence": 0,
    }


def test_aggregate_percentages_cover_sample():
    agg = sentiment.aggregate(
        [
            "Bitcoin surges to new highs",
            "Ethereum rallies on upgrade",
            "Exchange hacked, funds stolen",
            "Network maintenance scheduled",
        ]
    )
    assert agg["bullish"] + agg["bearish"] + agg["neutral"] == 100
    assert 0 <= agg["confidence"] <= 100
