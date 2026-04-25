from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

HF_API_KEY = os.environ.get("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/")
def home():
    return "AI Question Generator Running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    text = data.get("context", "")

    if not text:
        return jsonify({"error": "No input"}), 400

    prompt = f"""
Generate 3 questions from this text:

{text}
"""

    try:
        result = query({"inputs": prompt})

        # extract output safely
        output = result[0]["generated_text"] if isinstance(result, list) else str(result)

        questions = output.split("?")

        return jsonify({
            "questions": [q.strip() + "?" for q in questions if len(q.strip()) > 5]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)