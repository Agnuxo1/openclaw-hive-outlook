FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default runtime duration (5.5 hours)
ENV RUN_DURATION=19800

CMD ["python", "main.py"]
