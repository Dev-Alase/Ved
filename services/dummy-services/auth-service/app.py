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
logger = logging.getLogger("auth-service")

# JSON formatter
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": "auth-service",
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

# FileHandler for /app/logs/auth-service.log
file_handler = logging.FileHandler("/app/logs/auth-service.log")
file_handler.setFormatter(JSONFormatter())
logger.addHandler(file_handler)

def structured_log(level: str, message: str, metadata: dict = {}):
    logger.log(logging.getLevelName(level), message, extra={"metadata": metadata})

@app.get("/login")
async def login():
    if random.choice([True, False]):
        structured_log("INFO", "User login successful", {"user_id": random.randint(1, 100)})
        return {"status": "success"}
    else:
        structured_log("ERROR", "User not found", {"error_code": 404})
        return {"status": "error"}

@app.get("/logout")
async def logout():
    structured_log("WARNING", "User session expired", {"session_id": "xyz123"})
    return {"status": "success"}