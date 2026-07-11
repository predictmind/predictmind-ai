"""Internal AI endpoints for news intelligence (see API spec §11).

These live under /internal/ai/* and are called east-west by the news-service,
never directly by the public. The gateway does not expose /internal/*.
"""

from __future__ import annotations

from fastapi import APIRouter

from . import sentiment
from .schemas import (
    NewsAnalyzeRequest,
    NewsAnalyzeResponse,
    SentimentAnalyzeRequest,
    SentimentAnalyzeResponse,
)

router = APIRouter(prefix="/internal/ai", tags=["news-intelligence"])


@router.post("/news/analyze", response_model=NewsAnalyzeResponse)
def analyze_news(req: NewsAnalyzeRequest) -> NewsAnalyzeResponse:
    """Classify one article: sentiment, impact (0-100 + level), and coins mentioned."""
    text = req.combined_text()
    impact = sentiment.score_impact(text)
    return NewsAnalyzeResponse(
        sentiment=sentiment.classify(text),
        impact=impact,
        impact_level=sentiment.impact_level(impact),
        symbols=sentiment.detect_symbols(text),
        compound=round(sentiment.compound_score(text), 4),
    )


@router.post("/sentiment/analyze", response_model=SentimentAnalyzeResponse)
def analyze_sentiment(req: SentimentAnalyzeRequest) -> SentimentAnalyzeResponse:
    """Summarise a batch of texts into bullish/bearish/neutral percentages."""
    agg = sentiment.aggregate(req.texts)
    return SentimentAnalyzeResponse(**agg)
