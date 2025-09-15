# Use a base Python image
FROM python:3.10.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements
COPY requirements.txt .

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