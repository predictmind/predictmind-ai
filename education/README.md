# PredictMind AI — Education Notes

Beginner-friendly walkthroughs of the **AI service** code, written so a smart
10-year-old with no coding background could follow along and re-write it.

This service is different from the others: the rest of PredictMind is written in
**TypeScript/NestJS**, but the AI service is written in **Python** with a tool
called **FastAPI**. Python is a very popular language for AI and math work.

Read the files **in order** — they follow the real order we built and changed
things, including a bug we hit and fixed. When a later step changes something from
an earlier one, we explain the change *in the later step* rather than rewriting
the earlier note, so you can follow the whole journey.

| # | File | What it covers |
| --- | --- | --- |
| 1 | [01-fastapi-and-docker.md](01-fastapi-and-docker.md) | The FastAPI scaffold (health endpoint) + how it runs in Docker as a non-root user |
| 2 | [02-build-and-ci-fix.md](02-build-and-ci-fix.md) | A real bug: adding the education folder broke the build, and how we fixed the packaging |
| 3 | [03-glossary.md](03-glossary.md) | Dictionary of every term used in these notes |

Glossary terms are defined the first time they appear in each note.
