from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import random

app = Flask(__name__)
CORS(app)

HF_API_KEY = os.environ.get("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def query_hf(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/")
def home():
    return "Advanced AI Question Generator Running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    text = data.get("context", "")

    if not text:
        return jsonify({"error": "No input provided"}), 400

    prompt = f"""
Generate 3 different questions, 3 MCQs with options, and difficulty level (easy/medium/hard) from this text:

{text}

Format:
Question:
MCQ:
Difficulty:
"""

    try:
        result = query_hf({
            "inputs": prompt
        })

        output = result[0]["generated_text"]

        # simple parsing
        questions = []
        mcqs = []

        for line in output.split("\n"):
            if "?" in line:
                questions.append(line.strip())
            if "MCQ" in line:
                mcqs.append(line.strip())

        return jsonify({
            "questions": questions[:5],
            "mcqs": mcqs[:5],
            "raw": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)