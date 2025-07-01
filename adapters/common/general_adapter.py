import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load a lightweight model and tokenizer (pre-trained for classification)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=4)

def normalize(raw_logs):
    normalized_logs = []
    # Basic regex patterns for common log fields
    timestamp_pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*?Z)'
    service_pattern = r'(?<=from\s)([\w-]+)|(?<=service\s)([\w-]+)'
    level_pattern = r'(ERROR|CRITICAL|INFO|DEBUG|WARNING|SUCCESS)'

    for line in raw_logs.splitlines():
        if not line.strip():
            continue
        normalized_log = {
            "timestamp": "",
            "service": "unknown",
            "message": line.strip(),
            "level": "INFO"
        }

        # Extract fields using regex
        timestamp_match = re.search(timestamp_pattern, line)
        if timestamp_match:
            normalized_log["timestamp"] = timestamp_match.group(1)

        service_match = re.search(service_pattern, line)
        if service_match:
            normalized_log["service"] = service_match.group(0) or "unknown"

        level_match = re.search(level_pattern, line, re.IGNORECASE)
        if level_match:
            normalized_log["level"] = level_match.group(0).upper()

        # Use AI model to infer missing or ambiguous fields
        if not normalized_log["level"] in ["ERROR", "CRITICAL", "INFO", "DEBUG", "WARNING", "SUCCESS"]:
            inputs = tokenizer(line, return_tensors="pt", truncation=True, padding=True, max_length=128)
            with torch.no_grad():
                outputs = model(**inputs)
                predicted_class = torch.argmax(outputs.logits, dim=1).item()
                levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
                normalized_log["level"] = levels[predicted_class]

        normalized_logs.append(normalized_log)

    return normalized_logs