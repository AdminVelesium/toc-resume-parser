FROM python:3.10-slim

# Install system-level dependencies required for pycurl, pycairo, pygobject, etc.
RUN apt-get update && apt-get install -y \
    gcc \
    libcurl4-openssl-dev \
    libssl-dev \
    libffi-dev \
    curl \
    build-essential \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    libgirepository1.0-dev \
    gir1.2-glib-2.0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

