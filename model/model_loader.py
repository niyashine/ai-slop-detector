import joblib
import os

MODEL_PATH = os.path.join("model", "classifier.pkl")

model = None


def load_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully")
    except Exception as e:
        print("Model not loaded:", e)


def predict(text):
    if model is None:
        return {
            "prediction": "Model not loaded",
            "confidence": 0,
            "reasons": ["Fallback mode active"]
        }

    prediction = model.predict([text])[0]

    return {
        "prediction": str(prediction),
        "confidence": 90,
        "reasons": ["ML model prediction"]
    }