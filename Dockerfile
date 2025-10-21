FROM python:3.12.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# system deps we will need for media/ocr/transcoding etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
libmagic1 \
    build-essential \
    gcc \
    libpq-dev \
    ffmpeg \
    tesseract-ocr \
    poppler-utils \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*


# copy requirements & install
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy entrypoint and project
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]
