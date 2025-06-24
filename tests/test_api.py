from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/logs', methods=['POST'])
def receive_logs():
    logs = request.get_json()
    print(f"Received logs: {json.dumps(logs, indent=2)}")
    return {"status": "success"}, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)