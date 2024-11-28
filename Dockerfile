FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --dev

ADD . /app

RUN uv venv

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --dev

FROM python:3.13-slim-bookworm
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
