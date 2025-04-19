FROM python:3.12.8-alpine

# Install system deps + Python build tools
RUN apk add --no-cache gcc musl-dev libffi-dev bash

WORKDIR /usr/src/app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add your app and entrypoint
COPY cashman ./cashman
COPY bootstrap.sh ./
RUN chmod +x bootstrap.sh

EXPOSE 5000

CMD ["./bootstrap.sh"]