# 1. The AI Service: FastAPI + Docker

This service is the "brain" of PredictMind. Later it will do smart things like
suggest trading strategies and score coins. Right now it's a tiny **skeleton**
(a starting shell) with just one endpoint that says "I'm alive." We'll grow it
from here.

New words:
- **Python** — a programming language that reads almost like English. Very
  popular for AI and math.
- **FastAPI** — a Python toolkit for building **APIs** quickly.
- **API** (Application Programming Interface) — a menu of requests one program can
  send to another. Like a waiter: you ask for something, it brings a result.
- **endpoint** — one item on that menu, e.g. `GET /health`.

## Why Python here, but TypeScript everywhere else?

Most PredictMind services talk to users and databases — TypeScript/NestJS is great
for that. But AI and data work has the best tools in **Python** (libraries for
math, machine learning, etc.). So we use "the right tool for each job." The
services still talk to each other over the network, so mixing languages is fine.

## The code (`app/main.py`)

```python
from datetime import UTC, datetime
from fastapi import FastAPI
from pydantic import BaseModel
from . import __version__

app = FastAPI(
    title="PredictMind AI",
    version=__version__,
    description="AI services for PredictMind: strategy generation, intelligence, PredictScore.",
)
```

- **`from ... import ...`** — this brings in tools other people already wrote so we
  don't reinvent them. Like grabbing a calculator instead of doing sums by hand.
- **`app = FastAPI(...)`** — creates our application object. `app` is the whole
  service; we hang endpoints off it. The `title`/`description` show up in the
  automatic documentation FastAPI generates for free.

```python
class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
```

- **`class HealthResponse(BaseModel)`** — describes the *shape* of the answer we
  send back: four pieces of text (`str` means "string" = text).
- **`BaseModel`** comes from **Pydantic**, a library that **checks data is the
  right shape**. If we accidentally tried to send a number where text was
  promised, Pydantic would catch it. Think of it as a mold that the data must fit.

```python
@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness probe used by the platform health checks."""
    return HealthResponse(
        status="ok",
        service="predictmind-ai",
        version=__version__,
        timestamp=datetime.now(UTC).isoformat(),
    )
```

- **`@app.get("/health")`** — the `@` thing is a **decorator**: a sticker that
  says "run this function when someone does a GET request to `/health`." A **GET**
  request just means "please give me some info" (no changes made).
- **`response_model=HealthResponse`** — promises the answer will match that mold.
- **`datetime.now(UTC)`** — the current time in **UTC** (a worldwide standard
  clock, so times mean the same thing everywhere, no timezone confusion).
- **Why a health endpoint at all?** Automated systems ping `/health` to check the
  service is awake. If it stops answering, they restart it. It's the service's
  "say ahh" checkup.

## What it needs to run (`pyproject.toml`)

```toml
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
]
```

- **`pyproject.toml`** is Python's shopping list of libraries (like `package.json`
  in the Node services). `pip install` reads it and downloads them.
- **`uvicorn`** — the actual web **server** that runs our FastAPI app and listens
  for requests. FastAPI writes the logic; uvicorn answers the door.
- **`>=0.115.0`** means "this version or newer."

## Running it in Docker (`Dockerfile`)

We package the service into its own **Docker image** (a sealed box with Python and
our code), so it runs the same everywhere.

```dockerfile
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .

COPY app ./app

RUN useradd --create-home --uid 1001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Line by line:

- **`FROM python:3.11-slim`** — start from a small official Python image. "slim"
  means stripped down = smaller and faster.
- **`PYTHONDONTWRITEBYTECODE=1`** — don't leave little `.pyc` cache files lying
  around (keeps the box clean).
- **`PYTHONUNBUFFERED=1`** — print logs immediately instead of holding them in a
  buffer, so we can see what's happening in real time.
- **`COPY pyproject.toml ./` then `RUN pip install`** — copy the shopping list
  first and install. Because this happens *before* copying the code, Docker can
  **cache** the installed libraries and skip re-downloading them every time we
  only change our own code. Faster rebuilds.
- **`--no-cache-dir`** — don't keep pip's download cache in the image (smaller
  image).
- **`COPY app ./app`** — now copy our actual code.
- **`useradd ... appuser` + `USER appuser`** — **this is the important fix.** By
  default a container runs as **root** (the all-powerful admin). If someone found
  a bug, running as root lets them do far more damage. So we create a plain user
  named `appuser` and switch to it. Now the service runs with the least power it
  needs — a security habit called **least privilege**. Every other PredictMind
  service already runs as a non-root user (`node`); this makes the AI service
  match.
  - **`--uid 1001`** just picks an ID number for the user.
  - **`chown -R appuser:appuser /app`** gives that user ownership of the app files
    so it can read them.
- **`EXPOSE 8000`** — note this port matches everything else: our code listens on
  8000, the Dockerfile documents 8000, and the compose file maps 8000. Keeping
  these three in sync avoids "why can't I reach it?" headaches.
- **`CMD [...]`** — the command that starts the server when the container boots.
  `--host 0.0.0.0` means "accept connections from outside the container" (not just
  from inside itself).

## Why a single stage here (not two)?

The Node services use a **two-stage** build (compile in one stage, ship a slim
second stage). Python doesn't compile to a separate output folder the same way —
we install libraries and run the source directly — so one stage is fine and
simpler here. If the image grows large later, we can split it then. We pick the
simplest thing that's correct.

## What we verified ✅

- The image **builds successfully**, including the new non-root user step.
- The service is designed to answer `GET /health` with `{status: "ok", ...}`.

## Recap

- The AI service is a **Python + FastAPI** skeleton with one `/health` endpoint.
- **Pydantic** guarantees the answer's shape; **uvicorn** serves it.
- The **Dockerfile** installs deps first (for caching), copies code, and — most
  importantly — runs as a **non-root user** for safety, on port **8000** to match
  the rest of the platform.

Back to the [index](README.md).
