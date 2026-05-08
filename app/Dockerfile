# Use the official Python slim image — small footprint, official support
FROM python:3.12-slim

# Don't write .pyc files and don't buffer stdout — better for containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install dependencies first (this layer caches when requirements don't change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Create a non-root user and switch to it (security best practice)
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Document the port the app listens on
EXPOSE 8000

# Run the app
CMD ["python", "app.py"]
