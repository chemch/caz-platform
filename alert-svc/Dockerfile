# syntax=docker/dockerfile:1

FROM python:3.12.8-alpine AS base

# Install build dependencies and pipenv in a single layer for caching
RUN apk add --no-cache gcc musl-dev libffi-dev && \
    pip install --no-cache-dir pipenv

# Builder stage: install dependencies to a virtualenv
FROM base AS builder
WORKDIR /usr/src/app

# Copy Pipfile and Pipfile.lock first for better cache utilization
COPY --link Pipfile Pipfile.lock ./

# Install dependencies into a virtualenv managed by pipenv
RUN --mount=type=cache,target=/root/.cache/pip \
    pipenv install --deploy --system

# Final stage: minimal runtime image
FROM python:3.12.8-alpine AS final

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /usr/src/app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code and bootstrap script
COPY --link cashman ./cashman
COPY --link bootstrap.sh ./

# Ensure bootstrap.sh is executable
RUN chmod +x bootstrap.sh

# Expose the Flask port
EXPOSE 5002

USER appuser

ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
