from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from model.model_loader import predict

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    result = predict(text)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)