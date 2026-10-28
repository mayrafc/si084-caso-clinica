FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends bash curl ca-certificates fonts-dejavu-core && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir reportlab==4.4.3 pymupdf==1.26.5
WORKDIR /caso
