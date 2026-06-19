# predictmind-ai

AI services for **PredictMind** — AI-Powered Market Intelligence & Strategy Research Platform.

Part of the PredictMind platform. Product and architecture documentation lives in the private [`predictmind/app`](https://github.com/predictmind/app) repository (see the AI Strategy Engine and AI Research Methodology documents).

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn
- Pydantic v2
- Ruff (lint) + Pytest

## Getting started

```bash
python -m venv .venv
. .venv/Scripts/activate    # Windows
# source .venv/bin/activate # macOS / Linux

pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

Health check: `GET http://localhost:8000/health`.

## Commands

| Command | Purpose |
| --- | --- |
| `uvicorn app.main:app --reload` | Run the dev server |
| `ruff check .` | Lint |
| `ruff format .` | Format |
| `pytest` | Run tests |

## Quality & security

- **CI** runs Ruff lint and Pytest on every push and PR.
- **CodeQL** code scanning (security + code-quality queries).
- **Dependabot** keeps dependencies and Actions up to date.

## License

Proprietary — © PredictMind. All rights reserved.
