from fastapi import FastAPI
import logging
import json
from datetime import datetime
import random
import os

app = FastAPI()

# Ensure /app/logs directory exists
os.makedirs("/app/logs", exist_ok=True)

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("payment-service")

# JSON formatter
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": "payment-service",
            "env": "staging",
            "logLevel": record.levelname,
            "message": record.msg,
            "rawLog": record.msg,
            "metadata": getattr(record, "metadata", {})
        }
        return json.dumps(log_entry)

# StreamHandler for stdout
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(JSONFormatter())
logger.addHandler(stream_handler)

# FileHandler for /app/logs/payment-service.log
file_handler = logging.FileHandler("/app/logs/payment-service.log")
file_handler.setFormatter(JSONFormatter())
logger.addHandler(file_handler)

def structured_log(level: str, message: str, metadata: dict = {}):
    logger.log(logging.getLevelName(level), message, extra={"metadata": metadata})

@app.get("/process")
async def process_payment():
    if random.choice([True, False]):
        structured_log("INFO", "Payment processed successfully", {"transaction_id": random.randint(1000, 9999)})
        return {"status": "success"}
    else:
        structured_log("ERROR", "Payment gateway failure", {"error_code": 502})
        return {"status": "error"}

@app.get("/refund")
async def refund():
    structured_log("WARNING", "Refund initiated", {"transaction_id": random.randint(1000, 9999)})
    return {"status": "success"}