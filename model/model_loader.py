import joblib
import os
from model.feature_extractor import extract_features

MODEL_PATH = "model/classifier.pkl"

model = None


def load_model():
    global model
    print("Loading model...")
    try:
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully")
        print("MODEL TYPE:", type(model))
        print("HAS predict_proba:", hasattr(model, "predict_proba"))
    except Exception as e:
        print("Model not loaded:", e)


def predict(text):
    global model

    if model is None:
        return {
            "prediction": "Model not loaded",
            "confidence": 0,
            "reasons": ["Fallback mode active"]
        }

    try:
        features = extract_features(text)
        features = [features]

        # prediction
        prediction = model.predict(features)[0]

        # convert numeric label → human readable label
        label_map = {
            0: "Human",
            1: "AI"
        }

        prediction_label = label_map.get(prediction, str(prediction))

        # REAL confidence using probabilities
        proba = model.predict_proba(features)[0]

        confidence = int(max(proba) * 100)

        return {
            "prediction": prediction_label,
            "confidence": confidence,
            "reasons": ["Logistic Regression probability-based prediction"]
        }

    except Exception as e:
        return {
            "prediction": "Error",
            "confidence": 0,
            "reasons": [str(e)]
        }