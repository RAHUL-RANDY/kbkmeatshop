FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend codebase
COPY . /app/

# Environment Variables
ENV PORT=5001 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    USE_SQLITE_FALLBACK=true

# Expose API port
EXPOSE 5001

# Run entrypoint script to seed db if needed and start gunicorn
CMD ["sh", "-c", "python seed.py && gunicorn --config gunicorn_config.py run:app"]
