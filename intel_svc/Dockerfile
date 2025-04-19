FROM python:3.12.8-alpine

# Install system deps + Python build tools
RUN apk add --no-cache \
    bash \
    gcc \
    libffi-dev \
    musl-dev

# Set the working directory
WORKDIR /usr/src/app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire alert_svc codebase including app/, main.py, config.py, bootstrap.sh
COPY . ./alert_svc
WORKDIR /usr/src/app/alert_svc

# Ensure bootstrap.sh is executable
RUN chmod +x bootstrap.sh

EXPOSE 5002

CMD ["./bootstrap.sh"]