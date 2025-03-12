# # Use a minimal and secure Python base image
# FROM python:3.11-slim AS base

# # Set environment variables to optimize Python behavior
# ENV PYTHONUNBUFFERED=1 \
#     PYTHONFAULTHANDLER=1 \
#     PIP_NO_CACHE_DIR=1 \
#     PIP_DISABLE_PIP_VERSION_CHECK=1

# # Set the working directory
# WORKDIR /src/app

# # Install system dependencies (pin versions and avoid extra packages)
# # hadolint ignore=DL3008
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc=12.2.0-14 \
#     libpq-dev=15.2-1 \
#     && rm -rf /var/lib/apt/lists/*

# # Copy and install dependencies from `requirements.txt`
# COPY requirements.txt .
# # hadolint ignore=DL3013
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the application source code
# COPY . .

# # Set required environment variables (modify if needed)
# ENV RABBITMQ_HOST="rabbitmq" \
#     RABBITMQ_EXCHANGE="stock_exchange" \
#     RABBITMQ_ROUTING_KEY="moving_avg" \
#     AWS_REGION="us-east-1" \
#     AWS_SQS_QUEUE_URL=""

# # Define the default command (modify as needed)
# CMD ["python", "-m", "src.app"]
# Use official lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies first to leverage Docker caching
COPY requirements.txt requirements-dev.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY src ./src

# Set environment variables (confirming RabbitMQ configuration)
ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_EXCHANGE=stock_analysis
ENV RABBITMQ_ROUTING_KEY=candlestick
ENV RABBITMQ_USER=guest
ENV RABBITMQ_PASSWORD=guest
ENV RABBITMQ_QUEUE=stock_analysis_queue

# Expose necessary ports (if needed, adjust based on RabbitMQ setup)
EXPOSE 5672 15672

# Command to start the application
CMD ["python", "-u", "src/app/main.py"]
