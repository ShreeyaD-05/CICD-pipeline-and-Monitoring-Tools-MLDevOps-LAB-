"""Iris Flower Prediction web app with Prometheus monitoring."""
import json
import os
import time

import joblib
from flask import Flask, Response, g, jsonify, render_template, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

import train as train_module

app = Flask(__name__)

# ---------- Load (or create) the model ----------
if not os.path.exists(train_module.MODEL_PATH):
    train_module.train()

bundle = joblib.load(train_module.MODEL_PATH)
model = bundle["model"]
target_names = bundle["target_names"]

try:
    with open(train_module.METRICS_PATH) as f:
        model_accuracy = json.load(f)["accuracy"]
except (FileNotFoundError, KeyError):
    model_accuracy = 0.0

# ---------- Prometheus metrics ----------
REQUEST_COUNT = Counter("iris_http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("iris_http_request_duration_seconds", "Request latency in seconds", ["endpoint"])
PREDICTION_COUNT = Counter("iris_predictions_total", "Total predictions by species", ["species"])
MODEL_ACCURACY = Gauge("iris_model_accuracy", "Accuracy of the model on the test set")
MODEL_ACCURACY.set(model_accuracy)

FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def record_metrics(response):
    endpoint = request.path
    if endpoint != "/metrics":
        REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
        REQUEST_LATENCY.labels(endpoint).observe(time.time() - g.start)
    return response


def parse_features(data):
    """Return a list of 4 floats or raise ValueError."""
    values = []
    for name in FEATURES:
        if name not in data or str(data[name]).strip() == "":
            raise ValueError(f"Missing value: {name}")
        value = float(data[name])
        if not 0 < value < 20:
            raise ValueError(f"{name} must be between 0 and 20")
        values.append(value)
    return values


@app.route("/")
def home():
    return render_template("index.html", accuracy=model_accuracy)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or request.form
    try:
        values = parse_features(data)
    except ValueError as err:
        if request.is_json:
            return jsonify({"error": str(err)}), 400
        return render_template("index.html", accuracy=model_accuracy, error=str(err)), 400

    index = int(model.predict([values])[0])
    species = target_names[index]
    PREDICTION_COUNT.labels(species).inc()

    if request.is_json:
        return jsonify({"species": species, "input": values})
    return render_template("index.html", accuracy=model_accuracy, species=species, values=values)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "model_accuracy": model_accuracy})


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
