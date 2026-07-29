FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --ignore-installed --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app ./app
COPY backend_service ./backend_service
COPY requirements.txt ./requirements.txt
RUN groupadd --system app \
    && useradd --system --gid app --create-home --home-dir /home/appuser appuser \
    && chown -R appuser:app /app
USER appuser
EXPOSE 8002
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import sys, urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8002/health', timeout=3).status < 500 else 1)"
ENTRYPOINT ["uvicorn"]
CMD ["backend_service.main:app", "--host", "0.0.0.0", "--port", "8002"]
