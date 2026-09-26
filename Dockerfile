FROM python:3.12-slim-trixie

# Install uv from its official image, as documented at docs.astral.sh/uv.
COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    TZ=Europe/Berlin

WORKDIR /app

# ZoneInfo requires the system timezone database.
RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Install the locked project dependencies without development dependencies.
RUN uv sync --locked --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "memento_mori_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
