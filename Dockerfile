FROM python:3.12-slim

# uv binary copied from the official uv image — pinned, no pip-install needed
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# uv settings:
#  - compile bytecode for faster container startup
#  - copy (not symlink) packages, since the build cache mount is ephemeral
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# --- dependency layer (cached unless lock/manifest changes) ---
# install deps WITHOUT the project first, so editing source doesn't reinstall deps
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# --- project layer ---
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# put the venv's executables on PATH so `uvicorn`/`celery` resolve directly
ENV PATH="/app/.venv/bin:$PATH"

# default command; compose overrides per-service
CMD ["uvicorn", "project_chaac.api.main:app", "--host", "0.0.0.0", "--port", "8000"]