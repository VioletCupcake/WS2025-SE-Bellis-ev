# B-EV Case Management System - Docker Image
# Python 3.12 with Django 5.0

FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL client
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ ./src/

# Copy entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose Django development server port
EXPOSE 8002

# Set working directory to Django project
WORKDIR /app/src

# Entrypoint handles migrations, seeding, and server start
ENTRYPOINT ["/app/entrypoint.sh"]
