from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_news_analyze_returns_full_shape():
    response = client.post(
        "/internal/ai/news/analyze",
        json={"title": "Bitcoin ETF approved as BTC rallies to record high"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["sentiment"] == "positive"
    assert 0 <= body["impact"] <= 100
    assert body["impact_level"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    assert "BTC" in body["symbols"]
    assert -1 <= body["compound"] <= 1


def test_news_analyze_negative():
    response = client.post(
        "/internal/ai/news/analyze",
        json={"title": "Solana network exploited", "summary": "Funds drained in a hack"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["sentiment"] == "negative"
    assert "SOL" in body["symbols"]


def test_sentiment_analyze_aggregates():
    response = client.post(
        "/internal/ai/sentiment/analyze",
        json={
            "symbol": "BTC",
            "texts": [
                "Bitcoin surges to new highs",
                "BTC rallies on strong adoption",
                "Exchange hacked, bitcoin dumped",
            ],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["bullish"] + body["bearish"] + body["neutral"] == 100
    assert 0 <= body["confidence"] <= 100


def test_sentiment_analyze_empty():
    response = client.post("/internal/ai/sentiment/analyze", json={"texts": []})
    assert response.status_code == 200
    assert response.json() == {"bullish": 0, "bearish": 0, "neutral": 0, "confidence": 0}
