# 2. A Real Bug We Hit: Adding Notes Broke the Build

This lesson is a **story of a mistake and its fix**, kept here on purpose. Real
coding is full of these, and seeing *why* something broke teaches more than
pretending it never happened.

## What we had before this step

In [step 1](01-fastapi-and-docker.md) we had:
- `app/` — our code (a Python **package**, because it has an `__init__.py`).
- `pyproject.toml` — the shopping list, with **no special packaging settings**.
- A working `Dockerfile`.

At that point the project built fine. Our automated robots (**CI** — the helpers
that run our lint and tests on every push) were happy. ✅

## What we changed — and how it broke

To follow the project's teaching rule, we **added an `education/` folder** (the
very notes you're reading). Harmless, right? It's just text files.

But the next CI run **failed** during "Install dependencies" with this message:

```text
error: Multiple top-level packages discovered in a flat-layout: ['app', 'education'].
```

### Why did text files break a Python install?

New word: **setuptools** — the tool that packs Python projects. When you run
`pip install .`, setuptools tries to **guess** which folders are your code (your
"packages"). This guessing is called **auto-discovery**.

- Before: the only top-level folder that looked like code was `app`. Easy guess. ✅
- (There was already a `tests/` folder too, but setuptools **ignores** common
  names like `tests` automatically.)
- After: now there were **two** unignored top-level folders — `app` **and**
  `education`. setuptools thought, "Which one is the real package? I won't guess
  between two — I'll stop." 🛑

So it wasn't the *content* of the notes; it was simply having a **second
top-level folder** that confused the auto-guesser.

## The fix (this step): stop guessing, tell it directly

Instead of letting setuptools guess, we **tell it exactly** which folder is our
package. We added this to `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
# Only "app" is our importable package. Without this, setuptools auto-discovery
# trips over other top-level folders (e.g. "education") and refuses to build.
packages = ["app"]
```

Line by line:

- **`[build-system]`** — spells out *what tool* builds this project
  (`setuptools`) and which version. Before, this was left unsaid and Python
  guessed a default. Saying it out loud is clearer and more reliable.
- **`[tool.setuptools]` → `packages = ["app"]`** — the actual fix. "Our code is
  the `app` folder. Full stop. Don't look at anything else." Now `education/` is
  simply ignored, the same way `tests/` was.

## Why this fix (and not another)?

There were a few options:

1. **Explicitly list the package** (what we did): `packages = ["app"]`. Simplest,
   clearest, and it won't break again if we add more non-code folders later
   (docs, scripts, etc.). ✅
2. **Tell it to exclude `education`** (`exclude = ["education*"]`): works, but we'd
   have to remember to exclude every *new* non-code folder forever. Fragile.
3. **Move code into a `src/` folder** ("src-layout"): a tidy, professional layout,
   but it's a bigger change to paths, imports, and the Dockerfile — too much churn
   just to fix this small problem right now.

We picked option 1 because it's the least code, the easiest to understand, and
the most future-proof for our situation. (We can still move to `src/` later if the
project grows.)

## How we made sure it really works

A big lesson from the previous step was: **test the way it really runs.** The
Docker image had built fine *even while this bug existed*, because the Dockerfile
installs dependencies **before** copying the code, so setuptools never saw two
folders at once. The bug only showed up in CI, which installs from the full
project folder.

So this time we copied exactly what CI does, on our own machine:

1. Made a fresh, empty **virtual environment** (a clean, isolated Python setup, so
   our test isn't polluted by other installed things).
2. Ran `pip install -e ".[dev]"` — it **installed cleanly** (no "multiple
   packages" error). ✅
3. Ran `ruff check .` — **all checks passed**. ✅
4. Ran `pytest -q` — **1 test passed**. ✅

Then we pushed, and CI went green.

New words:
- **editable install** (`pip install -e`) — installs your project so that editing
  the source updates the installed copy immediately (great while developing).
- **virtual environment (venv)** — a private, throwaway Python sandbox for one
  project, so its libraries don't mix with others.

## The takeaway

- Adding a folder can change how build tools **discover** your code.
- When a tool is **guessing**, it's safer to **tell it explicitly** what you mean.
- Always reproduce the *exact* environment that failed (here: CI) — the Docker
  build passing was a false sense of safety.

Next: the [glossary](03-glossary.md) of every term used in these notes.
