# 3. Real News Sentiment & Impact (the AI service's first real brain)

Until now the AI service only said "I'm alive" (`/health`). This step gives it its
**first real job**: read a news story and judge it — is it good or bad news, how
big a deal is it, and which coins is it about? These are the E7 stories **S7.2
(sentiment classification)** and **S7.3 (impact scoring)**.

## The story so far (why this lives here)

Remember the news-service? It already tags news with a **v1 keyword counter**
(count happy words vs sad words). That was always meant to be temporary. This is
**version 2**, and it lives in the Python AI service because language understanding
is a "smart, heavy" job that belongs with the AI tools. Later (next step) the
news-service will *call* this service instead of using its own keyword counter.

So the journey is: **v1 keyword counter (news-service) → v2 VADER (here) → the
news-service calls here.** You're reading the middle step.

## The tool: VADER (not a neural network... yet)

We use **VADER** (Valence Aware Dictionary and sEntiment Reasoner). It's a real,
respected sentiment tool — not just word counting.

- A plain keyword counter sees "not good" and counts "good" → wrongly positive.
- VADER knows grammar tricks: **negation** ("not good" → negative), **boosters**
  ("very good" → more positive), CAPS and exclamation marks (!!!) add intensity.

It gives a **compound score** from **-1** (very negative) to **+1** (very
positive).

> **Why VADER and not a big AI model (like a transformer / "cryptoBERT")?** A
> transformer would understand language even better — but it needs a ~hundreds-of-
> MB model download, heavy libraries (PyTorch), lots of memory, and slow startup.
> That's a lot to run in a small container and test in CI. VADER is tiny, pure
> Python, instant, and works offline, so it's the right **first real** version.
> We note the transformer as a future upgrade — same pattern as v1 → v2 → v3.

### Making VADER crypto-smart

VADER's built-in dictionary is tuned for general/social text. It doesn't know that
"hack" is very bad or "halving" is mildly good in crypto. So we **teach it** by
adding a crypto word list:

```python
CRYPTO_LEXICON = {
    "hack": -3.0, "rugpull": -3.6, "bearish": -2.6, "crash": -3.0,   # bad
    "bullish": 2.6, "rally": 2.0, "halving": 1.2, "approval": 2.0,   # good
    # ... more ...
}
_analyzer = SentimentIntensityAnalyzer()
_analyzer.lexicon.update(CRYPTO_LEXICON)   # merge our words into VADER's dictionary
```

- The numbers are on VADER's scale (about -4 to +4). "rugpull" (-3.6) is strongly
  negative; "halving" (+1.2) mildly positive.
- **`.lexicon.update(...)`** merges our words in. It's like adding pages to a
  dictionary the tool already owns.

## The functions (all pure — text in, answer out)

Pure functions are easy to test and easy to move later, so we keep every decision
here with no database or internet.

### Sentiment

```python
def compound_score(text): return _analyzer.polarity_scores(text)["compound"]  # -1..+1

def classify(text):
    score = compound_score(text)
    if score >= 0.05:  return "positive"
    if score <= -0.05: return "negative"
    return "neutral"
```

- `0.05` / `-0.05` are VADER's **standard thresholds**: a tiny wobble around zero
  counts as neutral, not a real opinion. Using the conventional numbers means our
  results match how VADER is meant to be read.

### Impact (how market-moving, 0-100)

Impact is **not** the same as good/bad. A story can be very negative but tiny, or
huge but neutral. We combine two signals:

```python
def score_impact(text):
    intensity = abs(compound_score(text)) * 40      # strong opinion → up to 40
    hits = number of HIGH_IMPACT_TERMS in text      # sec, etf, hack, ban, lawsuit...
    entity = min(60, hits * 20)                     # market-moving words → up to 60
    return round(min(100, intensity + entity))
```

- **Intensity**: a strongly-worded story (very positive or very negative) tends to
  move markets more than a lukewarm one — so we use the *size* of the compound
  score, ignoring its direction (`abs`).
- **Entities**: words like "SEC", "ETF", "hack", "lawsuit" mean "this matters"
  regardless of mood. Each adds 20, capped at 60.
- We `min(100, ...)` so it never exceeds 100. Then `impact_level` buckets it into
  LOW / MEDIUM / HIGH / CRITICAL (25/50/75 thresholds), matching FR-011.

### Which coins (symbol detection)

Same idea as the news-service: a map of symbols to everyday names
(`BTC → ["bitcoin"]`), then check if the text uses the symbol or any alias. (Kept
here too because services can't share code across repos — a small, deliberate
duplication.)

### Aggregate (many stories → one mood)

```python
def aggregate(texts):
    # classify each, then:
    # bullish% = positive/total, bearish% = negative/total, neutral% = rest
    # confidence = min(100, 30 + total*4 + avg_abs_compound*40)
```

- Turns a coin's recent headlines into `{ bullish, bearish, neutral, confidence }`.
- **Confidence** grows with **how many** stories there are *and* **how strongly
  opinionated** they are (average absolute compound). One wishy-washy headline =
  low confidence; fifty strong ones = high confidence.

## The API (`schemas.py` + `router.py`)

These are **internal** endpoints (under `/internal/ai/*`) — only other services
call them; the public gateway never exposes them.

```python
router = APIRouter(prefix="/internal/ai", tags=["news-intelligence"])

@router.post("/news/analyze")     # one article → sentiment + impact + symbols
@router.post("/sentiment/analyze")# many texts  → bullish/bearish/neutral/confidence
```

- **Pydantic schemas** (`NewsAnalyzeRequest`, etc.) describe and check the input
  and output shapes automatically. For example `impact` is declared
  `Field(ge=0, le=100)` — FastAPI guarantees the number stays in range.
- `NewsAnalyzeRequest.combined_text()` is a small helper: analyse the explicit
  `text` if given, otherwise stitch together `title + summary`. This makes the
  endpoint friendly to callers who have either.
- We wire the router into the app with one line in `main.py`:
  `app.include_router(analysis_router)`.

## Containerising it: a Dockerfile fix the earlier change forced 🧩

When we built the Docker image for this, it **failed**:

```text
error: package directory 'app' does not exist
```

Here's the chain of events (a great example of why we rebuild and test):

1. Two steps ago ([lesson 2](02-build-and-ci-fix.md)) we added
   `packages = ["app"]` to fix CI.
2. That line tells the installer "the `app` folder **is** the package." Fine for
   CI, which installs from the full project.
3. But the **Dockerfile** copied `pyproject.toml` and ran `pip install .`
   **before** copying the `app` folder. With the new rule, the installer now
   *demands* `app/` be present — and it wasn't there yet. 💥
4. We didn't notice back then because we didn't rebuild the image after the CI fix.

The fix: copy the code **before** installing.

```dockerfile
COPY pyproject.toml README.md ./
COPY app ./app                      # <-- now app/ exists before install
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .
```

> **Lesson:** a change that fixes one place (CI) can quietly break another (the
> Docker build). The cure is to **run it the way it really runs** — we rebuilt the
> image, saw the failure, and fixed it. (We also copy `README.md` because
> `pyproject.toml` names it as the project's readme, so the build wants it.)

## What we verified ✅

- `ruff` clean; **15 pytest tests** pass (sentiment, impact, symbols, aggregate,
  and both endpoints via FastAPI's TestClient).
- The **Docker image builds** (after the fix) and, running as a container, the
  endpoints returned real results:
  - "Bitcoin ETF approved as BTC rallies to record high" → **positive**, impact
    MEDIUM, symbols `[BTC]`, compound **+0.72**.
  - "Solana exchange hacked; funds drained; price crashes" → **negative**, symbols
    `[SOL]`, compound **-0.88**.
  - A mix of 3 BTC headlines → `{ bullish: 67, bearish: 33, neutral: 0,
    confidence: 68 }`.

## What's next (the step after this)

The AI service can now analyse news, but the news-service still uses its **v1
keyword** counter. The next step wires them together: the news-service will call
`POST /internal/ai/news/analyze` for each article, and fall back to v1 only if the
AI service is unreachable. That completes the v1 → v2 → integrated journey.

Next: the [glossary](04-glossary.md).
