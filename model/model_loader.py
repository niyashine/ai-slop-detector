import joblib
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
        feature_values = extract_features(text)

        word_count = feature_values[0]
        avg_sentence_length = feature_values[1]
        vocab_diversity = feature_values[2]
        readability = feature_values[3]

        features = [feature_values]

        prediction = model.predict(features)[0]

        label_map = {
            0: "Human",
            1: "AI"
        }

        prediction_label = label_map.get(prediction, str(prediction))

        proba = model.predict_proba(features)[0]
        confidence = int(max(proba) * 100)

        reasons = []

        # HUMAN
        if prediction_label == "Human":

            if vocab_diversity > 0.75:
                reasons.append("High vocabulary diversity indicates natural human writing style")

            if avg_sentence_length < 15:
                reasons.append("Shorter sentence structures suggest conversational human writing")

            if readability > 60:
                reasons.append("High readability indicates natural human flow")

            if word_count > 300:
                reasons.append("Long-form human writing provides strong confidence in classification")

        # AI
        elif prediction_label == "AI":

            if vocab_diversity < 0.5:
                reasons.append("Low vocabulary diversity suggests repetitive AI-generated patterns")

            if avg_sentence_length > 20:
                reasons.append("Long uniform sentence structures are typical of AI-generated text")

            if readability < 40:
                reasons.append("Lower readability suggests structured machine-generated writing")

            if word_count > 200:
                reasons.append("Long-form text strengthens statistical confidence of AI detection")

        # FINAL SAFETY FALLBACK
        if not reasons:
            reasons.append("Prediction based on learned language patterns")

        return {
            "prediction": prediction_label,
            "confidence": confidence,
            "reasons": reasons
        }

    except Exception as e:
        return {
            "prediction": "Error",
            "confidence": 0,
            "reasons": [str(e)]
        }