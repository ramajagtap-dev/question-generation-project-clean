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
    data = request.get_json()
    text = data.get("context", "")

    if not text:
        return jsonify({"error": "No input"}), 400

    # 🔥 Smart keyword-based logic
    questions = []

    if "India" in text:
        questions.append("What type of government does India have?")
        questions.append("What is the population of India?")
        questions.append("What makes India culturally diverse?")
    else:
        templates = [
            "What is the main topic of the paragraph?",
            "What important information is given?",
            "What can we learn from this text?",
            "Why is this topic important?"
        ]
        questions = random.sample(templates, 3)

    return jsonify({"questions": questions})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)