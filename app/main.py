from flask import Flask, jsonify
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import threading
import time
from .metrics import collect_metrics

app = Flask(__name__)

def loop():
    while True:
        collect_metrics()
        time.sleep(5)

t = threading.Thread(target=loop, daemon=True)
t.start()

@app.route("/")
def home():
    return jsonify({"message": "URL monitoring app running"})

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)