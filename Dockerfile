# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Update and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir \
    pandas \
    matplotlib \
    torch \
    requests \
    numpy \
    psycopg2-binary \
    matplotlib

# Install Node.js and PM2
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g pm2

# Set the working directory
WORKDIR /app

# Add the Python script
COPY strategy_5min_test.py /app/strategy_5min_test.py
COPY strategy_day_test.py /app/strategy_day_test.py
COPY scheduler.config.js /app/scheduler.config.js
COPY sample_code.py /app/sample_code.py
COPY final_challenge /app/final_challenge

# Run the Python script at container startup and prevent the container from stopping
CMD ["sh", "-c", "pm2 start scheduler.config.js && tail -f /dev/null"]