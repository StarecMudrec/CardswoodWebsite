FROM python:3.11-slim

WORKDIR /app

# Install system deps (if in future you need SSL / locales etc., add here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Expose HTTP port used by the service
ENV PORT=8081
EXPOSE 8081

# Run the purchase_notify service
CMD ["python", "app.py"]

