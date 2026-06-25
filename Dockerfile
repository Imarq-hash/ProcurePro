# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=10000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create logs directory
RUN mkdir -p logs

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Run migrations
RUN python manage.py migrate --noinput || true

# Expose port
EXPOSE 10000

# Run gunicorn
CMD ["gunicorn", "procurepro_project.wsgi:application", "--bind", "0.0.0.0:10000", "--workers", "4", "--timeout", "120"]
