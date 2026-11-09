# IS601 Module 10 — multi-stage build to keep packaging tools
# and their vendored dependency inventories out of the runtime image.
# Python 3.11 matches the existing GitHub Actions Python version.
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build
COPY requirements.txt ./requirements.txt

# Install the existing application's dependencies in a virtual environment.
RUN python -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --no-cache-dir -r requirements.txt \
    && rm -rf \
       /opt/venv/lib/python3.11/site-packages/pip \
       /opt/venv/lib/python3.11/site-packages/pip-*.dist-info \
       /opt/venv/lib/python3.11/site-packages/setuptools \
       /opt/venv/lib/python3.11/site-packages/setuptools-*.dist-info \
       /opt/venv/lib/python3.11/site-packages/wheel \
       /opt/venv/lib/python3.11/site-packages/wheel-*.dist-info

# Final image starts clean. We only copy the finished venv, not
# the builder's packaging tools, pip cache, or vendor SBOMs.
FROM python:3.11-slim-bookworm AS runtime

ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Remove packaging tools that ship in the base runtime Python image.
# No pip is needed to run FastAPI, psycopg or the existing pytest tests.
RUN rm -rf \
       /usr/local/lib/python3.11/site-packages/pip \
       /usr/local/lib/python3.11/site-packages/pip-*.dist-info \
       /usr/local/lib/python3.11/site-packages/setuptools \
       /usr/local/lib/python3.11/site-packages/setuptools-*.dist-info \
       /usr/local/lib/python3.11/site-packages/wheel \
       /usr/local/lib/python3.11/site-packages/wheel-*.dist-info \
       /usr/local/lib/python3.11/ensurepip

COPY --from=builder /opt/venv /opt/venv

WORKDIR /code
COPY app/ ./app/
COPY tests/ ./tests/

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
