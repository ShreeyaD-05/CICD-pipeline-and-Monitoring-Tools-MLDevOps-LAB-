import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from app import app, model_accuracy


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Iris Flower Predictor" in response.data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_predict_setosa(client):
    payload = {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.get_json()["species"] == "setosa"


def test_predict_virginica(client):
    payload = {"sepal_length": 6.9, "sepal_width": 3.1, "petal_length": 5.8, "petal_width": 2.1}
    response = client.post("/predict", json=payload)
    assert response.get_json()["species"] == "virginica"


def test_predict_bad_input(client):
    response = client.post("/predict", json={"sepal_length": "abc"})
    assert response.status_code == 400


def test_metrics_endpoint(client):
    client.post("/predict", json={"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"iris_predictions_total" in response.data


def test_model_accuracy_is_good():
    assert model_accuracy >= 0.90
