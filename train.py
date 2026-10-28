"""Train a simple model on the Iris dataset and save it."""
import json

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

MODEL_PATH = "model.joblib"
METRICS_PATH = "metrics.json"


def train():
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))

    joblib.dump({"model": model, "target_names": list(iris.target_names)}, MODEL_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump({"accuracy": round(float(accuracy), 4)}, f)

    print(f"Model trained. Test accuracy = {accuracy:.4f}")
    return accuracy


if __name__ == "__main__":
    train()
