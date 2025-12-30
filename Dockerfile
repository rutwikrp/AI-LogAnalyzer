FROM python:3.11-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# Install only required dependency
RUN pip install --no-cache-dir requests

# Copy application code
COPY app/ app/

# Create log directory (for demo / local bind mount)
RUN mkdir -p /var/log/app && chown -R app:app /var/log/app

# Switch to non-root user
USER app

# Default environment variables
ENV LOG_FILE_PATH=/var/log/app/app.log
ENV WINDOW_SIZE_SECONDS=30
ENV BASELINE_WINDOWS=5
ENV ERROR_SPIKE_MULTIPLIER=2.0
ENV ALERT_COOLDOWN_SECONDS=120

CMD ["python", "app/main.py"]
