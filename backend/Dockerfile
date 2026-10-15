# Multi-stage build for Python 3.11+ FastAPI backend
FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies for PostgreSQL support (optional)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifests
COPY pyproject.toml ./

# Copy application code BEFORE pip install (required by pyproject.toml packages declaration)
COPY app/ ./app/

# Install dependencies (default to base, override with INSTALL_SPEC build arg for postgres)
ARG INSTALL_SPEC=.
RUN pip install --no-cache-dir "$INSTALL_SPEC"

# Copy remaining application files
COPY alembic.ini ./
COPY alembic/ ./alembic/
COPY seed_data.py ./

# Copy entrypoint script
COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

# Expose port
EXPOSE 8000

# Set entrypoint to run migrations and CMD to start uvicorn
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
