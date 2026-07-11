# 4. Glossary (the dictionary)

Simple meanings for the words in the AI service notes. This service is **Python**,
so some words differ from the TypeScript services.

| Word | Simple meaning |
| --- | --- |
| **Python** | A programming language that reads almost like English; great for AI/math. |
| **FastAPI** | A Python toolkit for building APIs quickly. |
| **API** | The menu of requests one program can send to another. |
| **Endpoint** | One item on that menu, e.g. `GET /health`. |
| **GET / POST** | HTTP requests: GET asks for info; POST sends data to be processed. |
| **Server** | A program that waits for requests and answers them. |
| **uvicorn** | The web server that actually runs our FastAPI app and answers requests. |
| **Router** | A group of related endpoints you attach to the app (`APIRouter`). |
| **Internal endpoint** | A `/internal/*` route only other services call; not exposed publicly. |
| **Pydantic** | A Python library that checks data is the right shape (a "mold"). |
| **BaseModel** | A Pydantic class you inherit from to describe a data shape. |
| **Field(ge=, le=)** | A Pydantic rule: a number must be within a range (e.g. 0-100). |
| **Model (Pydantic)** | A described data shape (e.g. `HealthResponse`). |
| **str** | Short for "string" = text. |
| **Decorator** | A `@label` sticker above a function that gives it special behavior. |
| **Function** | A named block of steps you can run (`def health(): ...`). |
| **Pure function** | A function whose output depends only on its input; easy to test. |
| **Import** | Bringing in code others wrote so you don't rewrite it. |
| **UTC** | A worldwide standard clock, so times mean the same everywhere. |
| **pyproject.toml** | Python's list of libraries + settings (like `package.json`). |
| **pip** | Python's tool for downloading libraries. |
| **Dependency** | A library your code needs to work. |
| **Health check** | A tiny endpoint that answers "I'm alive" so systems can watch the service. |
| **VADER** | A lexicon+grammar sentiment tool; understands negation, boosters, CAPS. |
| **Lexicon** | A dictionary of words with sentiment weights; we add crypto words to VADER's. |
| **Compound score** | VADER's overall sentiment number, from -1 (negative) to +1 (positive). |
| **Sentiment** | Whether text sounds positive, negative, or neutral. |
| **Threshold** | The cutoff (±0.05) that turns a score into positive/negative/neutral. |
| **Impact** | How market-moving a story is: 0-100, bucketed LOW/MEDIUM/HIGH/CRITICAL. |
| **Intensity** | How strong an opinion is (size of the compound score). |
| **Entity term** | A market-moving word (SEC, ETF, hack) that raises impact regardless of mood. |
| **Aggregate** | Combine many texts into one summary (bullish/bearish/neutral %). |
| **Confidence** | How much to trust an aggregate (more/stronger texts → higher). |
| **Transformer / cryptoBERT** | A heavier neural sentiment model; a possible future upgrade over VADER. |
| **Docker image / container** | A frozen package / a running copy of it. |
| **Dockerfile** | The recipe that builds the image. |
| **Base image / slim image** | The image you build on / a stripped-down smaller one. |
| **Layer caching** | Docker reusing unchanged build steps to rebuild faster. |
| **root / non-root user** | All-powerful admin vs a limited user; we run as limited (`appuser`). |
| **least privilege** | Giving code only the power it needs, nothing more. |
| **EXPOSE / port** | The numbered "door" the server listens on (ours: 8000). |
| **Ruff** | A fast Python linter/formatter (checks + tidies code). |
| **Pytest / TestClient** | Python's testing tool / FastAPI's helper to call endpoints in tests. |
| **Single-stage / multi-stage build** | Building the image in one step vs several. |
| **setuptools** | The tool that packs a Python project so it can be installed. |
| **auto-discovery** | setuptools **guessing** which folders are your code. |
| **package (Python)** | A folder of Python code that can be imported (usually has `__init__.py`). |
| **build-system** | The `pyproject.toml` section naming which tool builds the project. |
| **editable install** | `pip install -e` — edits to the source update the installed copy live. |
| **virtual environment (venv)** | A private, throwaway Python sandbox for one project. |
| **CI** | Robots that auto-run lint/tests on every push. |

Back to the [index](README.md).
