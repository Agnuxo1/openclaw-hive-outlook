# Project: openclaw-hive-outlook
# Author: Francisco Angulo de Lafuente
# ORCID: https://orcid.org/0009-0001-1634-7063
# Copyright year: 2026 (year of the first tracked commit)
# Attribution recorded: 2026-11-04
# License scope: unresolved; this header grants no license.

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default runtime duration (5.5 hours)
ENV RUN_DURATION=19800

CMD ["python", "main.py"]
