FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# hadolint ignore=DL3008
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
