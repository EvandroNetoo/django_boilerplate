FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PATH="/root/.cargo/bin/:$PATH"

WORKDIR /app
ADD . /app

RUN uv venv

ENV PATH="/app/.venv/bin:$PATH"

RUN uv sync --dev

CMD ["uv", "run", "python", "boilerplate/manage.py", "runserver", "0.0.0.0:8000"]
