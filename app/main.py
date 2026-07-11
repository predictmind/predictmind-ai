"""PredictMind AI service entrypoint (FastAPI).

Hosts the internal AI endpoints used by the backend: strategy generation,
news/sentiment analysis, and the PredictScore engine. See the AI Strategy
Engine document in the private predictmind/app repository.
"""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import FastAPI
from pydantic import BaseModel

from . import __version__
from .analysis.router import router as analysis_router

app = FastAPI(
    title="PredictMind AI",
    version=__version__,
    description="AI services for PredictMind: strategy generation, intelligence, PredictScore.",
)

app.include_router(analysis_router)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness probe used by the platform health checks."""
    return HealthResponse(
        status="ok",
        service="predictmind-ai",
        version=__version__,
        timestamp=datetime.now(UTC).isoformat(),
    )
