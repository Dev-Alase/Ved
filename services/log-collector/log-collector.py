import json
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import importlib

# Dynamic adapter loading
def load_adapter(adapter_name):
    try:
        # Add the project root to sys.path if not already included
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # Default to general adapter if no specific adapter is provided
        if not adapter_name or adapter_name == "default":
            return importlib.import_module("adapters.common.general_adapter").normalize
        # Import the specified adapter module using the dotted path
        module = importlib.import_module(f"adapters.{adapter_name}")
        return module.normalize
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Adapter {adapter_name} not found: {e}")

class LogHandler(FileSystemEventHandler):
    def __init__(self, config, api_endpoint):
        self.config = config
        self.api_endpoint = api_endpoint
        self.adapters = {source.get("adapter", "default"): load_adapter(source.get("adapter", "default")) for source in config["sources"]}
        self.last_positions = {source["path"]: 0 for source in config["sources"]}  # Track last read position
        self.last_processed = {source["path"]: 0 for source in config["sources"]}  # Track last processed time

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.log'):
            return
        for source in self.config["sources"]:
            if event.src_path.endswith(source["path"].split('/')[-1]):
                current_time = time.time()
                # Debounce: Skip if processed within the last 0.5 seconds
                if current_time - self.last_processed[source["path"]] < 0.5:
                    continue
                with open(event.src_path, 'r') as f:
                    # Move to the last read position
                    f.seek(self.last_positions[source["path"]])
                    new_logs = f.read()
                    if new_logs:  # Only process if there are new lines
                        normalized_logs = self.adapters[source.get("adapter", "default")](new_logs)
                        self.send_to_api(normalized_logs, source["path"])
                        # Update the last position to the end of the file
                        self.last_positions[source["path"]] = f.tell()
                        # Update the last processed time
                        self.last_processed[source["path"]] = current_time

    def send_to_api(self, normalized_logs, source_path):
        try:
            response = requests.post(self.api_endpoint, json=normalized_logs, timeout=10)
            response.raise_for_status()
            print(f"Successfully sent logs from {source_path} to {self.api_endpoint}")
        except requests.RequestException as e:
            print(f"Failed to send logs from {source_path}: {e}")

class LogCollector:
    def __init__(self, config_path):
        # Use relative path to config file within the script's directory
        self.config_path = os.path.join(os.path.dirname(__file__), config_path)
        self.config = self.load_config(self.config_path)
        self.api_endpoint = self.config["api_endpoint"]
    
    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            return json.load(f)

    def collect_logs(self):
        event_handler = LogHandler(self.config, self.api_endpoint)
        observer = Observer()
        for source in self.config["sources"]:
            observer.schedule(event_handler, source["path"], recursive=False)
        observer.start()
        print("Started monitoring log files...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    collector = LogCollector("logcollector.config.json")
    collector.collect_logs()