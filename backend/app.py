from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API Running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    text = data.get("context")

    return jsonify({
        "input": text,
        "question": "What is the main idea of the given text?"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)