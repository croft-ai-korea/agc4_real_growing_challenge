# Use Ubuntu 22.04 as the base image
#FROM ubuntu:22.04
FROM python:3.9-bullseye


RUN python -m pip install --upgrade pip

# Update and install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages

RUN pip3 install --no-cache-dir \
    pandas \
    plotly \
    pyyaml \
    torch \
    requests \
    numpy \
    matplotlib \
    psycopg2-binary

# Install Node.js and PM2
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g pm2

RUN pip3 install --no-cache-dir  plotly pyyaml matplotlib

# Set the working directory
WORKDIR /app

# Add the Python script
#COPY . /app

ENV PYTHONPATH=/app

ENV     timescale_db=postgres
ENV     timescale_user=postgres
ENV     timescale_password=admin1234
ENV     timescale_host=timescaledb
ENV     timescale_port=5432

ENV     letsgrow_username=Agrifusion
ENV     letsgrow_password=78G\$dV32La
ENV     letsgrow_endpoint=https://api.letsgrow.com/
ENV     letsgrow_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZ3JpZnVzaW9uIiwianRpIjoiMTYzZDFhMzUtMzhlYS00NmIyLTg5MWItYjAyYzVlZjE2ZDkyIiwiaWF0IjoiMDgvMDQvMjAyNCAwNzoxMTo1NiIsImV4cCI6MTcyMjg0MTkxNiwiaXNzIjoiTGV0c0dyb3ciLCJhdWQiOiJMZXRzR3JvdyJ9.SbFQ-OtOtKPrMjgbXGGZVha_tPk2qO5d7OEkPDQr1bo


# Run the Python script at container startup and prevent the container from stopping
# CMD ["sh", "-c", "pm2 start scheduler.config.js && tail -f /dev/null"]
CMD ["sh", "-c", "tail -f /dev/null"]