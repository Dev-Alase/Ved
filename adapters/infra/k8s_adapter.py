def normalize(raw_logs):
    normalized_logs = []
    for line in raw_logs.splitlines():
        if line.strip():
            normalized_log = {
                "timestamp": "",
                "service": "kubernetes",
                "message": line.strip(),
                "level": "INFO"
            }
            # Attempt to extract timestamp if present (e.g., "2025-06-24T14:00:00.123456Z Some message")
            parts = line.split(" ", 1)
            if len(parts) > 1 and parts[0].endswith('Z'):
                normalized_log["timestamp"] = parts[0]
                normalized_log["message"] = parts[1].strip()
            normalized_logs.append(normalized_log)
    return normalized_logs