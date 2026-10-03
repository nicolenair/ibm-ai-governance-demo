"""SageMaker inference script for the hiring model.

Scores a logistic regression with numpy from exported parameters (model.json) and
returns the same JSON shape as the built-in Linear Learner:
{"predictions": [{"score": p, "predicted_label": 0.0|1.0}]}
"""
import io
import json
import os

import numpy as np


def model_fn(model_dir):
    with open(os.path.join(model_dir, "model.json")) as f:
        return {k: np.asarray(v, dtype=float) for k, v in json.load(f).items()}


def input_fn(body, content_type):
    if isinstance(body, (bytes, bytearray)):
        body = body.decode("utf-8")
    if content_type and content_type.startswith("application/json"):
        payload = json.loads(body)
        instances = payload["instances"] if isinstance(payload, dict) else payload
        rows = [i["features"] if isinstance(i, dict) else i for i in instances]
        return np.asarray(rows, dtype=float)
    return np.loadtxt(io.StringIO(body), delimiter=",", ndmin=2)


def predict_fn(data, model):
    z = ((data - model["mean"]) / model["scale"]) @ model["coef"] + model["intercept"]
    return 1.0 / (1.0 + np.exp(-z))


def output_fn(scores, accept):
    predictions = [{"score": float(s), "predicted_label": float(s >= 0.5)} for s in scores]
    return json.dumps({"predictions": predictions}), "application/json"
