# Use a base Python image
FROM python:3.10.13-slim

RUN python -m venv /opt/venv

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Build prerequisites for psycopg2 from source
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . /app/src

# Copy start script
COPY ./scripts/start /start
RUN chmod +x /start && sed -i 's/\r$//' /start

# Copy initialize script
COPY ./scripts/initialize /initialize
RUN chmod +x /initialize && sed -i 's/\r$//' /initialize

# Copy start migrate script
COPY ./scripts/migrate /migrate
RUN chmod +x /migrate && sed -i 's/\r$//' /migrate
