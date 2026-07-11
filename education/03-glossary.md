# 3. Glossary (the dictionary)

Simple meanings for the words in the AI service notes. This service is **Python**,
so some words differ from the TypeScript services.

| Word | Simple meaning |
| --- | --- |
| **Python** | A programming language that reads almost like English; great for AI/math. |
| **FastAPI** | A Python toolkit for building APIs quickly. |
| **API** | The menu of requests one program can send to another. |
| **Endpoint** | One item on that menu, e.g. `GET /health`. |
| **GET** | An HTTP request that just asks for information (no changes). |
| **Server** | A program that waits for requests and answers them. |
| **uvicorn** | The web server that actually runs our FastAPI app and answers requests. |
| **Pydantic** | A Python library that checks data is the right shape (a "mold"). |
| **BaseModel** | A Pydantic class you inherit from to describe a data shape. |
| **Model (Pydantic)** | A described data shape (e.g. `HealthResponse` with four text fields). |
| **str** | Short for "string" = text. |
| **Decorator** | A `@label` sticker above a function that gives it special behavior (e.g. `@app.get`). |
| **Function** | A named block of steps you can run (`def health(): ...`). |
| **Import** | Bringing in code others wrote so you don't rewrite it. |
| **UTC** | A worldwide standard clock, so times mean the same everywhere. |
| **pyproject.toml** | Python's list of libraries + settings (like `package.json`). |
| **pip** | Python's tool for downloading libraries. |
| **Dependency** | A library your code needs to work. |
| **Health check** | A tiny endpoint that answers "I'm alive" so systems can watch the service. |
| **Docker image** | A frozen, sealed box holding the app + everything it needs. |
| **Docker container** | A running copy of an image. |
| **Dockerfile** | The recipe that builds the image. |
| **Base image** | The starting image you build on top of (`python:3.11-slim`). |
| **slim image** | A stripped-down, smaller base image. |
| **Layer caching** | Docker reusing unchanged build steps to rebuild faster. |
| **root user** | The all-powerful admin user inside a container. |
| **Non-root user** | A limited user (`appuser`); safer — the "least privilege" habit. |
| **least privilege** | Giving code only the power it needs, nothing more. |
| **EXPOSE / port** | The numbered "door" the server listens on (ours: 8000). |
| **Ruff** | A fast Python linter/formatter (checks + tidies code). |
| **Pytest** | Python's testing tool. |
| **Single-stage / multi-stage build** | Building the image in one step vs several; Python here uses one for simplicity. |
| **setuptools** | The tool that packs a Python project so it can be installed. |
| **auto-discovery** | setuptools **guessing** which folders are your code. |
| **package (Python)** | A folder of Python code that can be imported (usually has `__init__.py`). |
| **build-system** | The `pyproject.toml` section naming which tool builds the project. |
| **editable install** | `pip install -e` — edits to the source update the installed copy live. |
| **virtual environment (venv)** | A private, throwaway Python sandbox for one project. |
| **CI** | Robots that auto-run lint/tests on every push. |

Back to the [index](README.md).
