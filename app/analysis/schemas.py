"""Request/response shapes for the internal news-intelligence endpoints."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Sentiment = Literal["positive", "negative", "neutral"]
ImpactLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class NewsAnalyzeRequest(BaseModel):
    """One article to analyse. Provide title (+ optional summary), or raw text."""

    title: str = ""
    summary: str | None = None
    text: str | None = None

    def combined_text(self) -> str:
        """The text we actually analyse: explicit `text`, else title + summary."""
        if self.text:
            return self.text
        return f"{self.title} {self.summary or ''}".strip()


class NewsAnalyzeResponse(BaseModel):
    sentiment: Sentiment
    impact: int = Field(ge=0, le=100)
    impact_level: ImpactLevel
    symbols: list[str]
    compound: float = Field(ge=-1, le=1)


class SentimentAnalyzeRequest(BaseModel):
    """A batch of texts (e.g. one coin's recent headlines) to summarise."""

    symbol: str | None = None
    texts: list[str] = Field(default_factory=list)


class SentimentAnalyzeResponse(BaseModel):
    bullish: int = Field(ge=0, le=100)
    bearish: int = Field(ge=0, le=100)
    neutral: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
