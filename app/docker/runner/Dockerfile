FROM python:3.11-slim

RUN useradd -m -u 1000 runner

WORKDIR /app

COPY runner.py .

USER runner

CMD ["python", "runner.py"]