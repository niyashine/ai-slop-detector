from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from model.model_loader import predict, load_model

app = Flask(__name__)
CORS(app)

load_model()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text or len(text.split()) < 10:
            return jsonify({
                "prediction": "Too short",
                "confidence": 0,
                "reasons": ["Please enter at least 10–15 words for reliable prediction"]
            })

        result = predict(text)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "prediction": "Error",
            "confidence": 0,
            "reasons": [str(e)]
        })


if __name__ == "__main__":
    app.run(debug=True)