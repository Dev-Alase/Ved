def normalize(raw_logs):
    import json
    normalized_logs = []
    for line in raw_logs.splitlines():
        try:
            log_data = json.loads(line)
            normalized_log = {
                "timestamp": log_data.get("timestamp", ""),
                "service": log_data.get("service", "unknown"),
                "message": log_data.get("message", line),
                "level": log_data.get("level", "INFO")
            }
            normalized_logs.append(normalized_log)
        except json.JSONDecodeError:
            normalized_logs.append({
                "timestamp": "",
                "service": "unknown",
                "message": line,
                "level": "ERROR"
            })
    return normalized_logs