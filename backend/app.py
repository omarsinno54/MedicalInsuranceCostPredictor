from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for browser requests

# Load your model once when the server starts
model_path = "./model.pkl"

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except FileNotFoundError:
    print(f"Error: Model file {model_path} not found!")
    model = None


@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        # Get data from request
        data = request.json

        # Create feature array in the order your model expects
        # Adjust this based on your model's expected input format
        features_list = [
            data["age"],
            int(data["bmi"]),
            int(data["children"]),
            0 if data["sex"] == "male" else 1,
            1 if data["smoker"] == "yes" else 0,
        ]

        # Northwest, Southeast, Southwest
        region = data["region"]
        regions_bool = [
            region == "northwest",
            region == "southeast",
            region == "southwest",
        ]

        features_list.extend(regions_bool)

        features = np.array([features_list])

        # Make prediction
        prediction = model.predict(features)[0]
        prediction = 10**prediction

        # Return prediction as JSON
        return jsonify({"prediction": float(prediction), "status": "success"})

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 400


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": model is not None})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5010)
