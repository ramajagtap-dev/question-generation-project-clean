from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API Running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    text = data.get("context")

    if not text:
        return jsonify({"error": "No input"}), 400

    # 🔥 Simple dynamic questions (NO AI = FAST + STABLE)
    templates = [
        "What is the main topic of the paragraph?",
        "What important information is given?",
        "What can we learn from this text?",
        "What is described in the paragraph?",
        "Why is this topic important?"
    ]

    questions = random.sample(templates, 3)

    return jsonify({"questions": questions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)