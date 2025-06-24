FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY log-collector.py .
COPY logcollector.config.json .

CMD ["python", "log-collector.py"]